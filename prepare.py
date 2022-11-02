import asyncio
from pathlib import Path

import asyncpg

from config import config


class Migrations:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool
        self.migrations = sorted(list(Path("migrations").glob("*.sql")))
        self.initial_data = sorted(list(Path("dokusei/resources/sql").glob("*.sql")))

    async def migrate(self) -> None:
        async with (self.pool.acquire() as connection, connection.transaction()):
            for migration in self.migrations:
                raw_sql = migration.read_text("utf-8")
                await self.pool.execute(raw_sql)

    async def create_initial_data(self) -> None:
        async with (self.pool.acquire() as connection, connection.transaction()):
            for data_file in self.initial_data:
                raw_sql = data_file.read_text("utf-8")
                await self.pool.execute(raw_sql)


async def main():
    async with asyncpg.create_pool(
        host=config["database"]["host"],
        port=config["database"]["port"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        database=config["database"]["database"],
    ) as pool:
        migrations = Migrations(pool)

        await migrations.migrate()
        await migrations.create_initial_data()


if __name__ == "__main__":
    asyncio.run(main())
