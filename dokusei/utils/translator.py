from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from aiohttp import ClientSession

from dokusei.resources.languages import LANGUAGES


class TranslateResponse(NamedTuple):
    source_language_code: str
    source_language: str
    source_message: str
    translated_language_code: str
    translated_language: str
    translated_message: str
    confidence: float


async def translate(message: str, language: str, session: ClientSession):
    base_url = "https://clients5.google.com/translate_a/single"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }
    params = {
        "dj": "1",
        "dt": ["t", "sp", "ld", "bd"],
        "client": "dict-chrome-ex",
        "sl": "auto",
        "tl": language,
        "q": message,
    }

    async with session.get(base_url, headers=headers, params=params) as resp:
        if resp.status != 200:
            text = await resp.text()
            raise Exception("Error code while translating", text)

        data = await resp.json()
        source_language_code = data.get("src", "Unknown")
        if source_language_code in LANGUAGES:
            source_language = LANGUAGES[source_language_code]["name"]
        else:
            source_language = "Unknown"
        source_message = ""
        translated_message = ""
        confidence = data.get("confidence", 0.0)

        for sentence in data.get("sentences", []):
            source_message += sentence["orig"] + " "
            translated_message += sentence["trans"]
        if len(translated_message) == 0:
            raise Exception("Google sent no translation")

        return TranslateResponse(
            source_language_code=source_language_code,
            source_language=source_language,
            source_message=source_message,
            translated_language_code=language,
            translated_language=LANGUAGES[language]["name"],
            translated_message=translated_message,
            confidence=round(confidence, 4),
        )
