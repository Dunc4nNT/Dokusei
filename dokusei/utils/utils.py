import random
from collections import Counter
from datetime import timedelta
from enum import Enum
from typing import Literal, NamedTuple

import asyncpg
import discord


def format_timedelta(time: timedelta) -> str:
    days, remainder = divmod(time.seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    days_str = f"{days} day" if days == 1 else f"{days} days"
    hours_str = f"{hours} hour" if hours == 1 else f"{hours} hours"
    minutes_str = f"{minutes} minute" if minutes == 1 else f"{minutes} minutes"
    seconds_str = f"{seconds} second" if seconds == 1 else f"{seconds} seconds"

    if time.seconds >= 86400:
        return f"{days_str}, {hours_str}, {minutes} and {seconds_str}"
    elif time.seconds >= 3600:
        return f"{hours_str}, {minutes_str} and {seconds_str}"
    elif time.seconds >= 60:
        return f"{minutes_str} and {seconds_str}"
    else:
        return seconds_str


def interaction_cooldown_key(
    interaction: discord.Interaction,
) -> discord.User | discord.Member:
    return interaction.user


def roll_die(sides: int, quantity: int) -> Counter[int]:
    counter: Counter[int] = Counter()
    for _ in range(quantity):
        counter[random.randint(1, sides)] += 1

    return counter


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.micro}{self.releaselevel[0] if self.releaselevel != 'final' else ''}"


class RunMode(Enum):
    DEVELOPMENT = 1
    PRODUCTION = 2


class GuessTheTypes(Enum):
    tank = "tank"
    horror_character = "horror_character"


class GuessTheDifficulties(Enum):
    easy = "easy"
    hard = "hard"


class GuessTheChoice(NamedTuple):
    name: str
    correct: bool


async def generate_guessthe_choices(
    type: GuessTheTypes,
    difficulty: GuessTheDifficulties,
    pool: asyncpg.Pool,
    last_answer: str = "",
) -> tuple[GuessTheChoice, str, list[GuessTheChoice]]:
    answer, image = await _generate_random_answer(type, pool, last_answer)
    if difficulty == "hard":
        choices = await _generate_random_options(type, answer.name, 24, pool)
    else:
        choices = await _generate_random_options(type, answer.name, 3, pool)
    choices.append(answer)
    random.shuffle(choices)

    return answer, image, choices


async def _generate_random_answer(
    type: GuessTheTypes, pool: asyncpg.Pool, last_answer: str
) -> tuple[GuessTheChoice, str]:
    match type:
        case GuessTheTypes.tank:
            result = await pool.fetch(
                "SELECT tank_name, image_link FROM tank_image WHERE tank_name != $1 ORDER BY RANDOM() LIMIT 1",
                last_answer,
            )
            return GuessTheChoice(result[0].get("tank_name", "N/A"), True), result[
                0
            ].get("image_link", "N/A")
        case _:
            raise ValueError


async def _generate_random_options(
    type: GuessTheTypes, correct_answer: str, n: int, pool: asyncpg.Pool
) -> list[GuessTheChoice]:
    match type:
        case GuessTheTypes.tank:
            query = "SELECT name FROM tank WHERE name != $1 ORDER BY RANDOM() LIMIT $2"
            result = await pool.fetch(query, correct_answer, n)
            return [GuessTheChoice(res["name"], False) for res in result]
        case _:
            raise ValueError


class TankInfo(NamedTuple):
    name: str
    manufactured: bool
    type: str
    country: str


async def get_tank_info(name: str, pool: asyncpg.Pool) -> TankInfo:
    result = await pool.fetch(
        "SELECT name, manufactured, type, country FROM tank WHERE name = $1", name
    )
    tank = result[0]
    return TankInfo(tank["name"], tank["manufactured"], tank["type"], tank["country"])
