from typing import TypedDict

from dokusei.utils.utils import RunMode, VersionInfo


class BotConfig(TypedDict):
    token: str
    description: str
    stats_webhook: str
    logging_webhook: str


class TranslateConfig(TypedDict):
    primary_language: str


class DatabaseConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str
    database: str


class LinksConfig(TypedDict):
    repository: str
    website: str
    docs: str
    dashboard: str
    support: str


class DevConfig(TypedDict):
    mode: RunMode
    version: VersionInfo


class Config(TypedDict):
    bot: BotConfig
    translate: TranslateConfig
    database: DatabaseConfig
    links: LinksConfig
    dev: DevConfig
