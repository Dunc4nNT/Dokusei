import logging
from typing import Any, Optional

import discord
from discord.ext import commands

from dokusei.utils.errors import ButtonOnCooldown
from dokusei.utils.utils import interaction_cooldown_key


class BaseView(discord.ui.View):
    def __init__(
        self,
        author: discord.User | discord.Member,
        original_interaction: discord.Interaction,
        cooldown: float = 0,
        timeout: Optional[float] = 180,
    ):
        super().__init__(timeout=timeout)

        self.author = author
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.original_interaction = original_interaction
        self.cooldown = commands.CooldownMapping.from_cooldown(
            1, cooldown, interaction_cooldown_key
        )

    async def on_timeout(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.url:
                    continue

            self.remove_item(item)

        await self.original_interaction.edit_original_response(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if await interaction.client.is_owner(interaction.user):  # type: ignore
            return True

        if interaction.user.id != self.author.id:
            await interaction.response.send_message(
                "You're not the author of that interaction, please use the command yourself to use buttons.",
                ephemeral=True,
            )
            return False

        time_left = self.cooldown.update_rate_limit(interaction)

        if time_left:
            raise ButtonOnCooldown(time_left)

        return True

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[Any],
    ) -> None:
        if isinstance(error, ButtonOnCooldown):
            time_left = round(error.time_left, 2)
            await interaction.response.send_message(
                f"You are on cooldown. Try again in {time_left}s",
                ephemeral=True,
            )
        else:
            return await super().on_error(interaction, error, item)
