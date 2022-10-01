from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dokusei import DokuseiBot


class ConfigManager:
    def __init__(self, client: DokuseiBot):
        self.client = client
