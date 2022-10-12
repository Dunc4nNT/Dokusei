from __future__ import annotations

from typing import Optional

import discord
from discord import app_commands

from dokusei.resources import LANG_CODES_LINK, LANGUAGES, LANGUAGES_BY_NAME
from dokusei.utils.errors import TransformerError
from dokusei.utils.translator import TranslateResponse, translate
from dokusei.utils.views.base import BaseView


class TranslationView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
        interaction: discord.Interaction,
        translate_response: TranslateResponse,
        original_message_link: str = "",
        cooldown: float = 0,
        timeout: Optional[float] = 180,
    ):
        super().__init__(
            author=author,
            original_interaction=interaction,
            cooldown=cooldown,
            timeout=timeout,
        )

        self.add_item(TranslationSelect(translate_response, original_message_link))


class TranslationSelect(discord.ui.Select):
    def __init__(
        self, translate_response: TranslateResponse, original_message_link: str = ""
    ):
        self.translate_response = translate_response
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
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
            placeholder="Select a different language",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        translate_response: TranslateResponse = await translate(
            self.translate_response.source_message,
            self.values[0],
            interaction.client.session,  # type: ignore
        )

        embed = await translation_embed(translate_response, self.original_message_link)

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
            app_commands.Choice(name=k, value=v)
            for k, v in LANGUAGES_BY_NAME.items()
            if k.lower().startswith(value.lower())
        ][:25]


async def translation_embed(
    translate_response: TranslateResponse,
    original_message_link: str = "",
) -> discord.Embed:
    return discord.Embed(
        title="Translation",
        description=f"Translated [a message]({original_message_link}) from {LANGUAGES[translate_response.source_language_code]['flag']} {translate_response.source_language} ({translate_response.confidence*100}% confidence) to {LANGUAGES[translate_response.translated_language_code]['flag']} {translate_response.translated_language}.\n\n```\n{translate_response.translated_message}```",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )
