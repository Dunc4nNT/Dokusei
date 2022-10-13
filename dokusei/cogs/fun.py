from __future__ import annotations

import random
from typing import TYPE_CHECKING, Annotated, Optional
from urllib.parse import quote_plus

import discord
from discord import app_commands
from discord.ext import commands

from dokusei.resources.eightball import RESPONSES
from dokusei.utils.checks import CooldownOwnerBypass
from dokusei.utils.utils import roll_die
from dokusei.utils.views.fun import (
    CoinflipView,
    DiceRollView,
    ImportTransformer,
    ImportView,
    coinflip_embed,
    diceroll_embed,
    import_embed,
)

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class Fun(commands.Cog):
    def __init__(self, client: DokuseiBot) -> None:
        self.client = client

    fun_group = app_commands.Group(name="fun", description="Fun commands.")

    @fun_group.command()
    @app_commands.checks.dynamic_cooldown(CooldownOwnerBypass(rate=1, per=3))
    async def coinflip(self, interaction: discord.Interaction) -> None:
        """Flips a coin."""
        embed = await coinflip_embed()

        await interaction.response.send_message(
            embed=embed,
            view=CoinflipView(
                author=interaction.user, interaction=interaction, cooldown=3
            ),
        )

    @fun_group.command(name="import")
    async def importthis(
        self,
        interaction: discord.Interaction,
        module: app_commands.Transform[str, ImportTransformer],
    ) -> None:
        """Import this

        :param module: the module to import
        """
        embed = await import_embed(module)

        await interaction.response.send_message(
            embed=embed,
            view=ImportView(author=interaction.user, interaction=interaction),
        )

    @fun_group.command()
    async def lmgtfy(self, interaction: discord.Interaction, query: str) -> None:
        """Let Me Google That For You.

        :param query: what to google
        """
        url = f"https://letmegooglethat.com/?q={quote_plus(query)}"
        await interaction.response.send_message(content=url)

    @fun_group.command()
    async def eightball(self, interaction: discord.Interaction, question: str) -> None:
        """Ask eightball a yes/no question.

        :param question: the question you have
        """
        embed = discord.Embed(
            title="Magic 8 Ball",
            description=f"**Question**: {question}\n"
            f"**Answer**: {random.choice(RESPONSES)}",
            colour=0x3F3368,
            timestamp=discord.utils.utcnow(),
        )

        await interaction.response.send_message(embed=embed)

    @fun_group.command()
    @app_commands.checks.dynamic_cooldown(CooldownOwnerBypass(rate=1, per=3))
    async def diceroll(
        self,
        interaction: discord.Interaction,
        sides: Annotated[int, Optional[app_commands.Range[int, 3, 120]]] = 6,
        quantity: Annotated[int, Optional[app_commands.Range[int, 1, 1000]]] = 1,
    ) -> None:
        """Roll a die.

        :param sides: amount of sides the die has, 3 <= sides <= 120, default 6
        :param quantity: amount of die to roll, 1 <= quantity <= 1000, default 1
        """
        result = roll_die(sides, quantity)
        embed = await diceroll_embed(sides, quantity, result)
        await interaction.response.send_message(
            embed=embed,
            view=DiceRollView(
                author=interaction.user,
                interaction=interaction,
                sides=sides,
                quantity=quantity,
                result=result,
                cooldown=3,
            ),
        )

    @fun_group.command()
    async def mock(self, interaction: discord.Interaction, message: str) -> None:
        """MoCk A mEsSaGe.

        :param message: content to mock
        """
        mock_msg = ""
        for char in message:
            if random.getrandbits(1):
                mock_msg += char.lower()
            else:
                mock_msg += char.upper()

        await interaction.response.send_message(content=mock_msg)


async def setup(client: DokuseiBot):
    await client.add_cog(Fun(client))
