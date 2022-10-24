from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from dokusei.utils.utils import format_timedelta
from dokusei.utils.views.botinfo import BotInfoView, client_info_embed

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class Informatic(commands.Cog):
    def __init__(self, client: DokuseiBot) -> None:
        self.client = client

    infobot_group = app_commands.Group(
        name="bot", description="Informatic bot-related commands."
    )

    @infobot_group.command()
    async def ping(self, interaction: discord.Interaction) -> None:
        """Shows the latency between discord and the bot."""
        await interaction.response.send_message(
            f"`{round(self.client.latency * 1000)}ms` latency to the Discord API."
        )

    @infobot_group.command()
    async def dashboard(self, interaction: discord.Interaction) -> None:
        """Sends a link to the dashboard."""
        await interaction.response.send_message(
            f"Dashboard: {self.client.config['links']['dashboard']}"
        )

    @infobot_group.command()
    async def website(self, interaction: discord.Interaction) -> None:
        """Sends a link to the website."""
        await interaction.response.send_message(
            f"Website: {self.client.config['links']['website']}"
        )

    @infobot_group.command()
    async def documentation(self, interaction: discord.Interaction) -> None:
        """Sends a link to the documentation."""
        await interaction.response.send_message(
            f"Documentation: {self.client.config['links']['docs']}",
        )

    @infobot_group.command()
    async def support(self, interaction: discord.Interaction) -> None:
        """Sends a link to the support server."""
        await interaction.response.send_message(
            f"Support: {self.client.config['links']['support']}"
        )

    @infobot_group.command()
    async def uptime(self, interaction: discord.Interaction) -> None:
        """Shows the time passed since the bot started."""
        uptime = discord.utils.utcnow() - self.client.start_time
        td = format_timedelta(uptime)

        await interaction.response.send_message(
            f"Up since {discord.utils.format_dt(self.client.start_time, 'f')}, which is {td} ago."
        )

    @infobot_group.command(name="info")
    async def botinfo(self, interaction: discord.Interaction) -> None:
        """Displays some info about the bot."""
        embed = await client_info_embed(self.client)
        await interaction.response.send_message(
            embed=embed,
            view=BotInfoView(
                author=interaction.user,
                interaction=interaction,
                client=self.client,
            ),
        )


async def setup(client: DokuseiBot):
    await client.add_cog(Informatic(client))
