from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from dokusei.utils import translate
from dokusei.utils.checks import CooldownOwnerBypass
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

    @app_commands.checks.dynamic_cooldown(CooldownOwnerBypass(rate=1, per=30))
    async def translate_ctx_menu(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """Translate a message using context menus.

        :param message: what to translate
        """
        translate_response = await translate(
            message.content,
            self.client.config["TRANSLATE"]["PRIMARY_LANGUAGE"],
            self.client.session,
        )

        embed = await translation_embed(translate_response, message.jump_url)

        await interaction.response.send_message(
            embed=embed,
            view=TranslationView(
                interaction.user,
                translate_response,
                message.jump_url,
                cooldown=30,
            ),
            ephemeral=True,
        )

    utility_group = app_commands.Group(name="utility", description="Utility commands.")

    @utility_group.command()
    @app_commands.checks.dynamic_cooldown(CooldownOwnerBypass(rate=1, per=30))
    async def translate(
        self,
        interaction: discord.Interaction,
        language: app_commands.Transform[str, TranslateTransformer],
        message: str,
    ) -> None:
        """Translate a message to the given language.

        :param language: language to translate the message into
        :param message: what to translate
        """
        translate_response = await translate(message, language, self.client.session)

        embed = await translation_embed(translate_response)

        await interaction.response.send_message(
            embed=embed,
            view=TranslationView(interaction.user, translate_response, cooldown=30),
        )


async def setup(client: DokuseiBot):
    await client.add_cog(Utility(client))
