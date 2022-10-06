from typing import Optional

import discord
from discord import app_commands


def owner_only():
    async def actual_check(interaction: discord.Interaction) -> bool:
        return await interaction.client.is_owner(interaction.user)  # type: ignore

    return app_commands.check(actual_check)


class CooldownOwnerBypass:
    def __init__(self, rate: float, per: float) -> None:
        self.rate = rate
        self.per = per

    async def __call__(
        self, interaction: discord.Interaction
    ) -> Optional[app_commands.Cooldown]:
        if await interaction.client.is_owner(interaction.user):  # type: ignore
            return None
        return app_commands.Cooldown(self.rate, self.per)
