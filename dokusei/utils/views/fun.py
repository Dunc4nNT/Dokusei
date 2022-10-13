from __future__ import annotations

import random
from collections import Counter
from typing import Optional

import discord
from discord import app_commands

from dokusei.resources.imports import IMPORTS
from dokusei.utils.errors import TransformerError
from dokusei.utils.utils import roll_die
from dokusei.utils.views.base import BaseView


class CoinflipView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
        interaction: discord.Interaction,
        cooldown: float = 0,
        timeout: Optional[float] = 180,
    ):
        super().__init__(
            author=author,
            original_interaction=interaction,
            cooldown=cooldown,
            timeout=timeout,
        )

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

    return discord.Embed(
        title="Coinflip",
        description=f"The coin landed on **{result}**.",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )


class ImportView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
        interaction: discord.Interaction,
        cooldown: float = 0,
        timeout: Optional[float] = 180,
    ):
        super().__init__(
            author=author,
            original_interaction=interaction,
            cooldown=cooldown,
            timeout=timeout,
        )

        self.add_item(ImportSelect())


class ImportSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=key, description=f"Import {key}.", value=key)
            for key in IMPORTS.keys()
        ][:25]
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
            placeholder="from dokusei.utils.views.fun import ImportSelect",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        embed = await import_embed(self.values[0])

        await interaction.response.edit_message(embed=embed)


class ImportTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str, /) -> str:
        if value in IMPORTS:
            return value
        raise TransformerError(
            "```\n"
            "Traceback (most recent call last):\n"
            '  File "<stdin>", line 1, in <module>\n'
            f"ModuleNotFoundError: No module named '{value}'\n\n"
            f"Please use one of the following modules: {', '.join(key for key in IMPORTS.keys())}```"
        )

    async def autocomplete(
        self, interaction: discord.Interaction, value: str, /
    ) -> list[app_commands.Choice[str]]:
        if not value:
            return [app_commands.Choice(name=key, value=key) for key in IMPORTS.keys()][
                :25
            ]

        return [
            app_commands.Choice(name=key, value=key)
            for key in IMPORTS.keys()
            if key.lower().startswith(value.lower())
        ][:25]


async def import_embed(module: str) -> discord.Embed:
    return discord.Embed(
        title=f"Import {module}",
        description=f"```\n{IMPORTS[module]}```",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )


class DiceRollView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
        interaction: discord.Interaction,
        sides: int,
        quantity: int,
        result: Counter[int],
        cooldown: float = 0,
        timeout: Optional[float] = 180,
    ) -> None:
        super().__init__(
            author=author,
            original_interaction=interaction,
            cooldown=cooldown,
            timeout=timeout,
        )
        self.sides = sides
        self.quantity = quantity
        self.result = result

        self.add_item(DiceRollRepeatButton(self.sides, self.quantity))
        self.add_item(DiceRollResultsButton(self.sides, self.quantity, self.result))
        self.add_item(DiceRollSelect(self.quantity))


class DiceRollSelect(discord.ui.Select):
    def __init__(self, quantity: int) -> None:
        options = [
            discord.SelectOption(
                label=str(x),
                description=f"Roll an {x}-sided die {quantity} times.",
                value=str(x),
            )
            for x in {
                3,
                4,
                5,
                6,
                7,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
                24,
                30,
                34,
                48,
                50,
                60,
                100,
                120,
            }
        ]
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
            placeholder="Roll a different sided die",
        )
        self.quantity = quantity

    async def callback(self, interaction: discord.Interaction) -> None:
        result = roll_die(int(self.values[0]), self.quantity)
        embed = await diceroll_embed(int(self.values[0]), self.quantity, result)

        await interaction.response.edit_message(
            embed=embed,
            view=DiceRollView(
                author=interaction.user,
                interaction=interaction,
                sides=int(self.values[0]),
                quantity=self.quantity,
                result=result,
            ),
        )


class DiceRollRepeatButton(discord.ui.Button):
    def __init__(self, sides: int, quantity: int) -> None:
        super().__init__(
            style=discord.ButtonStyle.primary, label="Roll Again", emoji="🔁"
        )
        self.sides = sides
        self.quantity = quantity

    async def callback(self, interaction: discord.Interaction) -> None:
        result = roll_die(self.sides, self.quantity)
        embed = await diceroll_embed(self.sides, self.quantity, result)

        await interaction.response.edit_message(
            embed=embed,
            view=DiceRollView(
                author=interaction.user,
                interaction=interaction,
                sides=self.sides,
                quantity=self.quantity,
                result=result,
            ),
        )


class DiceRollResultsButton(discord.ui.Button):
    def __init__(self, sides: int, quantity: int, result: Counter[int]) -> None:
        super().__init__(
            style=discord.ButtonStyle.primary, label="Show All Results", emoji="📝"
        )
        self.sides = sides
        self.quantity = quantity
        self.result = result

    async def callback(self, interaction: discord.Interaction) -> None:
        formatted_result = "**Side** | **Amount of times**\n"
        for k, v in self.result.most_common():
            formatted_result += f"{k} | {v}\n"

        embed = discord.Embed(
            title="Dice Roll Results",
            description=f"Rolled a {self.sides}-sided die {self.quantity} times.\n\n{formatted_result}",
            colour=0x3F3368,
            timestamp=discord.utils.utcnow(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def diceroll_embed(
    sides: int, quantity: int, result: Counter[int]
) -> discord.Embed:
    mc_value, mc_amount = result.most_common(1)[0]

    return discord.Embed(
        title="Coinflip",
        description=f"You rolled a {sides}-sided die {quantity} times.\n"
        f"The most common side it landed on was **{mc_value}**, which was rolled **{mc_amount}** times.\n\n"
        '**\\*** *Only shows the most common result, for all results click the button "Show All Results".*',
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )
