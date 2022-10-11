from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote_plus

import discord
from discord import app_commands
from discord.ext import commands

from dokusei.utils.checks import CooldownOwnerBypass
from dokusei.utils.views.fun import (
    CoinflipView,
    ImportTransformer,
    ImportView,
    coinflip_embed,
    import_embed,
)

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class Fun(commands.Cog):
    def __init__(self, client: DokuseiBot) -> None:
        self.client = client

    fun_group = app_commands.Group(name="fun", description="Fun commands.")

    @fun_group.command()
    @app_commands.checks.dynamic_cooldown(CooldownOwnerBypass(rate=1, per=1))
    async def coinflip(self, interaction: discord.Interaction) -> None:
        """Flips a coin."""
        embed = await coinflip_embed()

        await interaction.response.send_message(
            embed=embed,
            view=CoinflipView(interaction.user, cooldown=1),
        )

    @fun_group.command(name="import")
    async def importthis(
        self,
        interaction: discord.Interaction,
        *,
        module: app_commands.Transform[str, ImportTransformer],
    ) -> None:
        """Import this

        :param module: the module to import
        """
        embed = await import_embed(module)

        await interaction.response.send_message(
            embed=embed, view=ImportView(interaction.user)
        )

    @fun_group.command()
    async def lmgtfy(self, interaction: discord.Interaction, *, query: str) -> None:
        """Let Me Google That For You.

        :param query: what to google
        """
        url = f"https://letmegooglethat.com/?q={quote_plus(query)}"
        await interaction.response.send_message(content=url)


async def setup(client: DokuseiBot):
    await client.add_cog(Fun(client))
