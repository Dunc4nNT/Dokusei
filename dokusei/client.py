import configparser
import logging
from typing import Any

import aiohttp
import asyncpg
import discord
from discord.ext import commands


class DokuseiBot(commands.Bot):
    user: discord.ClientUser

    def __init__(
        self,
        initial_extensions: list[str],
        session: aiohttp.ClientSession,
        db_pool: asyncpg.Pool,
        config: configparser.ConfigParser,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(command_prefix=_get_prefix, *args, **kwargs)
        self.initial_extensions = initial_extensions
        self.session = session
        self.db_pool = db_pool
        self.config = config
        self.global_logger = logging.getLogger(__name__)

    async def setup_hook(self) -> None:
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
                    f"Failed to load extension: {extension}", error
                )

        if (
            self.config["DEV"]["TEST_GUILD_ID"]
            and self.config["DEV"]["MODE"] == "development"
        ):
            guild = discord.Object(self.config["DEV"]["TEST_GUILD_ID"])
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        if not hasattr(self, "start_time"):
            self.start_time = discord.utils.utcnow()

        self.global_logger.info(f"Ready: {self.user} ({self.user.id})")

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
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


def _get_prefix(client: DokuseiBot, message: discord.Message):
    prefixes = ["-", "!"]

    return commands.when_mentioned_or(*prefixes)(client, message)
