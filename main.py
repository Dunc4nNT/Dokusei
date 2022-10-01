import asyncio
import logging
import logging.handlers
from pathlib import Path

import aiohttp
import asyncpg
import discord

from config import config
from dokusei import DokuseiBot


async def setup_logging() -> None:
    Path("./logs").mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()

    discord.utils.setup_logging()
    logging.getLogger("discord").setLevel(logging.INFO)

    if config["DEV"]["MODE"] == "development":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.handlers.TimedRotatingFileHandler(
        Path("./logs/dokusei.log"), encoding="utf-8", when="midnight"
    )
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


async def main() -> None:
    await setup_logging()

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    initial_extensions = [
        f"dokusei.cogs.{ext.name[:-3]}"
        for ext in list(Path("dokusei/cogs").glob("*.py"))
        if ext.name != "__init__.py"
    ]

    async with aiohttp.ClientSession() as session, asyncpg.create_pool(
        dsn=config["DATABASE"]["DSN"], command_timeout=30
    ) as pool:
        async with DokuseiBot(
            description=config["BOT"]["DESCRIPTION"],
            intents=intents,
            initial_extensions=initial_extensions,
            session=session,
            db_pool=pool,
            config=config,
        ) as client:
            await client.start(config["BOT"]["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
