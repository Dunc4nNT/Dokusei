import logging

import discord
from discord.ext import commands

from dokusei.utils.errors import ButtonOnCooldown
from dokusei.utils.utils import interaction_cooldown_key


class BaseView(discord.ui.View):
    def __init__(
        self,
        *,
        cooldown: float = 10,
        timeout: int = 300,
    ):
        super().__init__(timeout=timeout)

        self.logger: logging.Logger = logging.getLogger(__name__)
        self.cooldown = commands.CooldownMapping.from_cooldown(
            1, cooldown, interaction_cooldown_key
        )

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if await interaction.client.is_owner(interaction.user):  # type: ignore
            return True

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
