from __future__ import annotations

import random

import discord

from dokusei.utils.views.base import BaseView


class CoinflipView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
        *,
        cooldown: float,
    ):
        super().__init__(author=author, cooldown=cooldown)

        self.add_item(
            FlipAgainButton(
                style=discord.ButtonStyle.primary, label="Flip Again", emoji="🔁"
            )
        )


class FlipAgainButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction) -> None:
        embed = await coinflip_embed()

        await interaction.response.edit_message(embed=embed)


async def coinflip_embed() -> discord.Embed:
    result = random.choice(["Heads", "Tails"])

    embed = discord.Embed(
        title="Coinflip",
        description=f"The coin landed on **{result}**.",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )

    return embed
