from __future__ import annotations

import random

import discord
from discord import app_commands

from dokusei.resources.imports import IMPORTS
from dokusei.utils.errors import TransformerError
from dokusei.utils.views.base import BaseView


class CoinflipView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
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

    return discord.Embed(
        title="Coinflip",
        description=f"The coin landed on **{result}**.",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )


class ImportView(BaseView):
    def __init__(self, author: discord.User | discord.Member):
        super().__init__(author=author)

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
