import asyncio
import logging
import textwrap
from datetime import datetime
from typing import Any

import aiohttp
import asyncpg
import discord
from discord import app_commands
from discord.ext import commands, tasks

from dokusei.utils.config_manager import Config
from dokusei.utils.errors import TransformerError


class DokuseiBot(commands.Bot):
    user: discord.ClientUser

    def __init__(
        self,
        initial_extensions: list[str],
        session: aiohttp.ClientSession,
        db_pool: asyncpg.Pool,
        config: Config,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(command_prefix=_get_prefix, *args, **kwargs)
        self.initial_extensions = initial_extensions
        self.session = session
        self.db_pool = db_pool
        self.config = config
        self.global_logger = logging.getLogger(__name__)
        self.logging_handler = DokuseiLogger(self)
        logging.getLogger().addHandler(self.logging_handler)
        self._logging_queue = asyncio.Queue()
        self.logging_webhook = discord.Webhook.from_url(
            self.config["bot"]["logging_webhook"], session=self.session
        )

    async def setup_hook(self) -> None:
        self.send_log_record.start()
        self.tree.on_error = self.on_app_command_error
        self.app_info = await self.application_info()
        self.owner_id = self.app_info.owner.id
        self.counters = {
            "code_stats": {"files": 0, "spaghetti": 0, "comments": 0, "blank": 0},
        }

        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except commands.ExtensionError as error:
                self.global_logger.exception(
                    f"Failed to load extension: %s".format(extension), error
                )

    async def on_ready(self):
        if not hasattr(self, "start_time"):
            self.start_time = discord.utils.utcnow()

        self.global_logger.info(f"Ready: {self.user} ({self.user.id})")

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if ctx.command:
            if ctx.command.has_error_handler():
                return
        if ctx.cog:
            if ctx.cog.has_error_handler():
                return

        ignored_errors = (
            commands.CommandNotFound,
            commands.CheckFailure,
            commands.CheckAnyFailure,
        )

        if isinstance(error, ignored_errors):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.message.reply(f"Command `{ctx.command}` has been disabled.")
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.message.reply(
                    f"Command `{ctx.command}` cannot be used in private messages."
                )
            except discord.HTTPException:
                pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.message.reply(
                f"Command `{ctx.command}` failed to process, {error}"
            )
        else:
            await ctx.message.reply(
                f"Something went wrong while processing `{ctx.command}`."
            )

            self.global_logger.error(
                f"Ignoring exception in command {ctx.command}", exc_info=error
            )

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        if interaction.command:
            if interaction.command._has_any_error_handlers():
                return

        # TODO: figure out a way to check if an error handler already exists inside the interaction's cog

        if isinstance(error, app_commands.CommandNotFound):
            await interaction.response.send_message(
                "This command is temporarily disabled.", ephemeral=True
            )
        elif isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)
        elif isinstance(error, app_commands.MissingRole) or isinstance(
            error, app_commands.MissingAnyRole
        ):
            await interaction.response.send_message(
                "You are missing the required role(s) to run this command",
                ephemeral=True,
            )
        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                "A check has failed, possible causes for this could be:\n"
                "- You do not have the required role(s)\n"
                "- You do not have the required permissions\n"
                "- The command is disabled\n"
                "- You are banned from using commands",
                ephemeral=True,
            )
        elif isinstance(error, TransformerError):
            await interaction.response.send_message(str(error))
        else:
            await interaction.response.send_message(
                "Something went wrong while processing this interaction.",
                ephemeral=True,
            )

            self.global_logger.error(
                "Ignoring exception in interaction.", exc_info=error
            )

    def add_log_record(self, record: logging.LogRecord) -> None:
        self._logging_queue.put_nowait(record)

    @tasks.loop(seconds=0)
    async def send_log_record(self) -> None:
        record: logging.LogRecord = await self._logging_queue.get()

        emojis = {
            "DEBUG": "🔧",
            "INFO": "ℹ️",
            "WARNING": "⚠️",
            "ERROR": "❗",
            "CRITICAL": "‼️",
        }
        log_time = datetime.utcfromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        message = textwrap.shorten(
            f"{emojis.get(record.levelname, '🤷')}`{log_time}` **{record.name}** {record.message if hasattr(record, 'message') else ''}",
            2000,
        )

        await self.logging_webhook.send(
            message,
            username=f"{self.user.display_name} Logging",
            avatar_url=self.user.display_avatar,
        )


class DokuseiLogger(logging.Handler):
    def __init__(self, client: DokuseiBot) -> None:
        super().__init__(logging.INFO)
        self.client = client

    def emit(self, record: logging.LogRecord) -> None:
        self.client.add_log_record(record)


def _get_prefix(client: DokuseiBot, message: discord.Message):
    prefixes = ["-", "!"]

    return commands.when_mentioned_or(*prefixes)(client, message)
