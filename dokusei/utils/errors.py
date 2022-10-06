from discord import app_commands
from discord.ext import commands


class ButtonOnCooldown(commands.CommandError):
    def __init__(self, time_left: float):
        self.time_left = time_left


class TransformerError(app_commands.AppCommandError):
    pass
