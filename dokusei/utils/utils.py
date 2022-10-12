import random
from collections import Counter
from datetime import timedelta

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
