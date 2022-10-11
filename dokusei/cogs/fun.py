from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from dokusei.utils.checks import CooldownOwnerBypass
from dokusei.utils.views.fun import CoinflipView, coinflip_embed

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class Fun(commands.Cog):
    def __init__(self, client: DokuseiBot) -> None:
        self.client = client

    fun_group = app_commands.Group(name="fun", description="Fun commands.")

    @fun_group.command()
    @app_commands.checks.dynamic_cooldown(CooldownOwnerBypass(rate=1, per=30))
    async def coinflip(self, interaction: discord.Interaction) -> None:
        """Flips a coin."""
        embed = await coinflip_embed()

        await interaction.response.send_message(
            embed=embed,
            view=CoinflipView(interaction.user, cooldown=1),
        )


async def setup(client: DokuseiBot):
    await client.add_cog(Fun(client))
