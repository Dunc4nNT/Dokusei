from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Literal, Optional

import discord
from discord.ext import commands

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class Developer(commands.Cog):
    def __init__(self, client: DokuseiBot) -> None:
        self.client: DokuseiBot = client
        self.logger: logging.Logger = logging.getLogger(__name__)

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.client.is_owner(ctx.author)

    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        """Shuts the bot down."""
        await ctx.send("Attempting to shut down cleanly...")
        self.logger.info("Shutdown: Manual")

        await self.client.close()

    @commands.command()
    async def load(
        self,
        ctx: commands.Context,
        *,
        module: str = commands.parameter(
            description="The module to load",
        ),
    ):
        """Loads the specified module."""
        try:
            await self.client.load_extension(f"dokusei.cogs.{module}")
        except commands.ExtensionError as error:
            await ctx.message.reply(f"{error.__class__.__name__}: {error}")
        else:
            await ctx.send(f"Module `{module}` has been loaded.")

    @commands.command()
    async def unload(
        self,
        ctx: commands.Context,
        *,
        module: str = commands.parameter(
            description="The module to unload",
        ),
    ):
        """Unloads the specified module."""
        try:
            await self.client.unload_extension(f"dokusei.cogs.{module}")
        except commands.ExtensionError as error:
            await ctx.message.reply(f"{error.__class__.__name__}: {error}")
        else:
            await ctx.send(f"Module `{module}` has been unloaded.")

    @commands.command()
    async def reload(
        self,
        ctx: commands.Context,
        *,
        module: str = commands.parameter(
            default=None,
            description="The module to reload, reloads all if nothing is specified",
        ),
    ):
        """Reloads the specified module, reload everything if no module is specified."""
        if module:
            try:
                await self.client.reload_extension(f"dokusei.cogs.{module}")
            except commands.ExtensionError as error:
                await ctx.message.reply(f"{error.__class__.__name__}: {error}")
            else:
                await ctx.send(f"Module `{module}` has been reloaded.")
        else:
            modules = [ext for ext in self.client.extensions.keys()]
            for module in modules:
                try:
                    await self.client.reload_extension(f"{module}")
                except commands.ExtensionError as error:
                    await ctx.message.reply(f"{error.__class__.__name__}: {error}")
            await ctx.send("Reloaded all modules.")

    @commands.command()
    async def modules(self, ctx: commands.Context):
        """Shows all the loaded modules."""
        await ctx.send(
            f"""The loaded modules are: {', '.join(f"`{ext.replace('dokusei.cogs.', '')}`" for ext in self.client.extensions.keys())}."""
        )

    @commands.command()
    @commands.guild_only()
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object] = commands.parameter(
            default=None, description="Guild IDs to sync, separated by space"
        ),
        spec: Optional[Literal["~", "*", "^"]] = commands.parameter(
            default=None,
            description="Sync guild (~), copy and sync (*), clear and sync (^)",
        ),
    ) -> None:
        """Syncs slash commands, syncs globally if no arguments are provided."""
        if guilds:
            count = 0
            for guild in guilds:
                try:
                    await self.client.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    count += 1

            await ctx.send(f"Synced slash commands in {count}/{len(guilds)} guilds.")
            return

        match spec:
            case "~":
                synced = await self.client.tree.sync(guild=ctx.guild)
                await ctx.message.reply(
                    f"Synced {len(synced)} slash command (groups) to the current guild."
                )
            case "*":
                self.client.tree.copy_global_to(guild=ctx.guild)  # type: ignore
                synced = await self.client.tree.sync(guild=ctx.guild)
                await ctx.message.reply(
                    f"Copied and synced {len(synced)} slash commands (groups) to the current guild."
                )
            case "^":
                self.client.tree.clear_commands(guild=ctx.guild)
                await self.client.tree.sync(guild=ctx.guild)
                await ctx.message.reply(
                    "Cleared guild slash commands and synced them with the global slash commands."
                )
            case _:
                synced = await self.client.tree.sync()
                await ctx.message.reply(
                    f"Synced {len(synced)} slash command (groups) globally."
                )


async def setup(client: DokuseiBot):
    await client.add_cog(Developer(client))
