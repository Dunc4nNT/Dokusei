import discord
from discord import app_commands


def owner_only():
    async def actual_check(interaction: discord.Interaction):
        return await interaction.client.is_owner(interaction.user)  # type: ignore

    return app_commands.check(actual_check)
