from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from dokusei.utils import translate
from dokusei.utils.views import TranslateTransformer, TranslationView, translation_embed

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class Utility(commands.Cog):
    def __init__(self, client: DokuseiBot) -> None:
        self.client = client
        self.ctx_menu = app_commands.ContextMenu(
            name="Translate Message", callback=self.translate_ctx_menu
        )
        self.client.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.client.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    async def translate_ctx_menu(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        (
            source_language_code,
            source_language,
            source_message,
            translated_language_code,
            translated_language,
            translated_message,
            confidence,
        ) = await translate(
            message.content,
            self.client.config["TRANSLATE"]["PRIMARY_LANGUAGE"],
            self.client.session,
        )

        embed = await translation_embed(
            source_language_code,
            source_language,
            translated_language_code,
            translated_language,
            translated_message,
            confidence,
            message.jump_url,
        )

        await interaction.response.send_message(
            embed=embed,
            view=TranslationView(
                self.client,
                source_language_code,
                source_language,
                source_message,
                translated_language_code,
                translated_language,
                translated_message,
                confidence,
                message.jump_url,
            ),
            ephemeral=True,
        )

    utility_group = app_commands.Group(name="utility", description="Utility commands.")

    @utility_group.command()
    @app_commands.checks.cooldown(1, 30.0, key=lambda i: (i.guild_id, i.user.id))
    async def translate(
        self,
        interaction: discord.Interaction,
        language: app_commands.Transform[str, TranslateTransformer],
        *,
        message: str,
    ) -> None:
        (
            source_language_code,
            source_language,
            source_message,
            translated_language_code,
            translated_language,
            translated_message,
            confidence,
        ) = await translate(
            message,
            language,
            self.client.session,
        )

        embed = await translation_embed(
            source_language_code,
            source_language,
            translated_language_code,
            translated_language,
            translated_message,
            confidence,
        )

        await interaction.response.send_message(
            embed=embed,
            view=TranslationView(
                self.client,
                source_language_code,
                source_language,
                source_message,
                translated_language_code,
                translated_language,
                translated_message,
                confidence,
            ),
        )


async def setup(client: DokuseiBot):
    await client.add_cog(Utility(client))
