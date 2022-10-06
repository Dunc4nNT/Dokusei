from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from dokusei.resources import LANG_CODES_LINK, LANGUAGES
from dokusei.utils.errors import ButtonOnCooldown, TransformerError
from dokusei.utils.translator import translate
from dokusei.utils.utils import interaction_cooldown_key

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class TranslationView(discord.ui.View):
    def __init__(
        self,
        client: DokuseiBot,
        source_language_code,
        source_language,
        source_message,
        translated_language_code,
        translated_language,
        translated_message,
        confidence,
        original_message_link="",
        *,
        timeout: int = 300,
    ):
        super().__init__(timeout=timeout)
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.cooldown = commands.CooldownMapping.from_cooldown(
            1, 30.0, interaction_cooldown_key
        )

        self.add_item(
            TranslationSelect(
                client,
                source_language_code,
                source_language,
                source_message,
                translated_language_code,
                translated_language,
                translated_message,
                confidence,
                original_message_link,
            )
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        time_left = self.cooldown.update_rate_limit(interaction)

        if time_left:
            raise ButtonOnCooldown(time_left)

        return True

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item,
    ) -> None:
        if isinstance(error, ButtonOnCooldown):
            time_left = round(error.time_left, 2)
            await interaction.response.send_message(
                f"You are on cooldown. Try again in {time_left}s",
                ephemeral=True,
            )
        else:
            return await super().on_error(interaction, error, item)


class TranslationSelect(discord.ui.Select):
    def __init__(
        self,
        client,
        source_language_code,
        source_language,
        source_message,
        translated_language_code,
        translated_language,
        translated_message,
        confidence,
        original_message_link="",
    ):
        self.client = client
        self.source_language_code = source_language_code
        self.source_language = source_language
        self.source_message = source_message
        self.translated_language_code = translated_language_code
        self.translated_language = translated_language
        self.translated_message = translated_message
        self.confidence = confidence
        self.original_message_link = original_message_link
        options = [
            discord.SelectOption(
                label=LANGUAGES[language_code]["name"],
                emoji=LANGUAGES[language_code]["flag"]
                if LANGUAGES[language_code]["flag"]
                else "❓",
                description=f"Translate to {LANGUAGES[language_code]['name']}.",
                value=language_code,
            )
            for language_code in LANGUAGES
            if LANGUAGES[language_code]["top"] is True
        ][:25]
        super().__init__(min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        (
            source_language_code,
            source_language,
            source_message,
            translated_language_code,
            translated_language,
            translated_message,
            confidence,
        ) = await translate(
            self.source_message,
            self.values[0],
            self.client.session,
        )

        embed = await translation_embed(
            source_language_code,
            source_language,
            translated_language_code,
            translated_language,
            translated_message,
            confidence,
            self.original_message_link,
        )

        await interaction.response.edit_message(embed=embed)


class TranslateTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str, /) -> str:
        if value in LANGUAGES:
            return value
        raise TransformerError(
            f'"{value}" is not a language, please check <{LANG_CODES_LINK}> for a list of all the available languages.'
        )

    async def autocomplete(
        self, interaction: discord.Interaction, value: str, /
    ) -> list[app_commands.Choice[str]]:
        if not value:
            return [
                app_commands.Choice(name=language["name"], value=lang_code)
                for lang_code, language in LANGUAGES.items()
                if language["top"] is True
            ][:25]

        return [
            app_commands.Choice(name=language["name"], value=lang_code)
            for lang_code, language in LANGUAGES.items()
            if language["name"].lower().startswith(value.lower())
        ][:25]


async def translation_embed(
    source_language_code,
    source_language,
    translated_language_code,
    translated_language,
    translated_message,
    confidence,
    original_message_link="",
) -> discord.Embed:
    embed = discord.Embed(
        title="Translation",
        description=f"Translated [a message]({original_message_link}) from {LANGUAGES[source_language_code]['flag']} {source_language} ({confidence*100}% confidence) to {LANGUAGES[translated_language_code]['flag']} {translated_language}.\n\n```\n{translated_message}```",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )

    return embed
