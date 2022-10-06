from discord.ext import commands


class ButtonOnCooldown(commands.CommandError):
    def __init__(self, time_left: float):
        self.time_left = time_left
