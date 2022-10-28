from typing import Literal, Optional

import asyncpg
import discord

from dokusei.utils.utils import GuessTheChoice, GuessTheTypes, generate_guessthe_choices
from dokusei.utils.views.base import BaseView


class GuessTheView(BaseView):
    def __init__(
        self,
        author: discord.User | discord.Member,
        interaction: discord.Interaction,
        type: GuessTheTypes,
        answer: GuessTheChoice,
        image: str,
        choices: list[GuessTheChoice],
        difficulty: Literal["easy", "hard"],
        pool: asyncpg.Pool,
        cooldown: float = 0,
        timeout: Optional[float] = 180,
    ):
        super().__init__(
            author=author,
            original_interaction=interaction,
            cooldown=cooldown,
            timeout=timeout,
        )
        self.type = type
        self.answer = answer
        self.image = image
        self.choices = choices
        self.difficulty = difficulty
        self.pool = pool

        if len(self.choices) < 5:
            for choice in self.choices:
                self.add_item(GuessTheButton(choice))
        else:
            self.add_item(GuessTheSelect(choices))


class GuessTheReplayButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(
            style=discord.ButtonStyle.primary, label="Play Again", emoji="🔁"
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if not self.view:
            raise AttributeError("GuessTheReplayButton is not used inside of a view")

        answer, image, choices = await generate_guessthe_choices(
            self.view.type,
            self.view.difficulty,
            self.view.pool,
            last_answer=self.view.answer.name,
        )
        embed = await guess_the_start_embed(self.view.type, image)
        await interaction.response.edit_message(
            embed=embed,
            view=GuessTheView(
                author=interaction.user,
                interaction=interaction,
                type=self.view.type,
                answer=answer,
                image=image,
                choices=choices,
                difficulty=self.view.difficulty,
                pool=self.view.pool,
            ),
        )


class GuessTheButton(discord.ui.Button):
    def __init__(
        self,
        choice: GuessTheChoice,
    ) -> None:
        super().__init__(
            style=discord.ButtonStyle.primary,
            label=choice.name,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if not self.view:
            raise AttributeError("GuessTheButton is not used inside of a view")

        embed = await guess_the_finish_embed(
            self.view.type, self.view.answer, self.view.image, self.label  # type: ignore
        )
        self.view.clear_items()
        self.view.add_item(GuessTheReplayButton())

        await interaction.response.edit_message(embed=embed, view=self.view)


class GuessTheSelect(discord.ui.Select):
    def __init__(self, choices: list[GuessTheChoice]):
        super().__init__(
            min_values=1,
            max_values=1,
            options=[discord.SelectOption(label=choice.name) for choice in choices],
            placeholder="Select a tank",
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        if not self.view:
            raise RuntimeError("GuessTheSelect is not used inside of a view")

        embed = await guess_the_finish_embed(
            self.view.type, self.view.answer, self.view.image, self.values[0]
        )
        self.view.clear_items()
        self.view.add_item(GuessTheReplayButton())

        await interaction.response.edit_message(embed=embed, view=self.view)


async def guess_the_start_embed(type: GuessTheTypes, image: str) -> discord.Embed:
    embed = discord.Embed(
        title=f"Guess The {type.value.capitalize()}",
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )
    embed.set_image(url=image)

    return embed


async def guess_the_finish_embed(
    type: GuessTheTypes, answer: GuessTheChoice, image: str, chosen: str
) -> discord.Embed:
    if answer.name == chosen:
        description = (
            f"You chose the correct answer! It is indeed a(n) **{answer.name}**"
        )
    else:
        description = f"That answer is incorrect, the correct answer is **{answer.name}**.\nYou chose **{chosen}**."
    embed = discord.Embed(
        title=f"Guess The {type.value.capitalize()}",
        description=description,
        colour=0x3F3368,
        timestamp=discord.utils.utcnow(),
    )
    embed.set_image(url=image)

    return embed
