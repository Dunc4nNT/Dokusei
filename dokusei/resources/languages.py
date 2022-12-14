from typing import TypedDict

LANG_CODES_LINK: str = "https://cloud.google.com/translate/docs/languages"


class LanguageDict(TypedDict):
    name: str
    flag: str
    top: bool


LANGUAGES: dict[str, LanguageDict] = {
    "af": {"name": "Afrikaans", "flag": "πΏπ¦", "top": True},
    "sq": {"name": "Albanian", "flag": "π¦π±", "top": False},
    "am": {"name": "Amharic", "flag": "πͺπΉ", "top": False},
    "ar": {"name": "Arabic", "flag": "πΈπ¦", "top": True},
    "hy": {"name": "Armenian", "flag": "π¦π²", "top": False},
    "as": {"name": "Assamese", "flag": "", "top": False},
    "ay": {"name": "Aymara", "flag": "", "top": False},
    "az": {"name": "Azerbaijani", "flag": "π¦πΏ", "top": False},
    "bm": {"name": "Bambara", "flag": "", "top": False},
    "eu": {"name": "Basque", "flag": "", "top": False},
    "be": {"name": "Belarusian", "flag": "π§πΎ", "top": False},
    "bn": {"name": "Bengali", "flag": "π§π©", "top": False},
    "bho": {"name": "Bhojpuri", "flag": "", "top": False},
    "bs": {"name": "Bosnian", "flag": "π§π¦", "top": False},
    "bg": {"name": "Bulgarian", "flag": "π§π¬", "top": False},
    "ca": {"name": "Catalan", "flag": "", "top": False},
    "ceb": {"name": "Cebuano", "flag": "", "top": False},
    "zh-cn": {"name": "Chinese (Simplified)", "flag": "π¨π³", "top": True},
    "zh-tw": {"name": "Chinese (Traditional)", "flag": "π¨π³", "top": True},
    "co": {"name": "Corsican", "flag": "", "top": False},
    "hr": {"name": "Croatian", "flag": "π­π·", "top": False},
    "cs": {"name": "Czech", "flag": "π¨πΏ", "top": False},
    "da": {"name": "Danish", "flag": "π©π°", "top": True},
    "dv": {"name": "Dhivehi", "flag": "π²π»", "top": False},
    "doi": {"name": "Dogri", "flag": "", "top": False},
    "nl": {"name": "Dutch", "flag": "π³π±", "top": True},
    "en": {"name": "English", "flag": "π¬π§", "top": True},
    "eo": {"name": "Esperanto", "flag": "", "top": False},
    "et": {"name": "Estonian", "flag": "πͺπͺ", "top": False},
    "ee": {"name": "Ewe", "flag": "", "top": False},
    "fil": {"name": "Filipino (Tagalog)", "flag": "π΅π­", "top": False},
    "fi": {"name": "Finnish", "flag": "π«π?", "top": True},
    "fr": {"name": "French", "flag": "π«π·", "top": True},
    "fy": {"name": "Frisian", "flag": "", "top": False},
    "gl": {"name": "Galician", "flag": "", "top": False},
    "ka": {"name": "Georgian", "flag": "π¬πͺ", "top": False},
    "de": {"name": "German", "flag": "π©πͺ", "top": True},
    "el": {"name": "Greek", "flag": "π¬π·", "top": False},
    "gn": {"name": "Guarani", "flag": "", "top": False},
    "gu": {"name": "Gujarati", "flag": "", "top": False},
    "ht": {"name": "Haitian Creole", "flag": "π­πΉ", "top": False},
    "ha": {"name": "Hausa", "flag": "", "top": False},
    "haw": {"name": "Hawaiian", "flag": "", "top": False},
    "he": {"name": "Hebrew", "flag": "π?π±", "top": True},
    "hi": {"name": "Hindi", "flag": "π?π³", "top": True},
    "hmn": {"name": "Hmong", "flag": "", "top": False},
    "hu": {"name": "Hungarian", "flag": "π­πΊ", "top": True},
    "is": {"name": "Icelandic", "flag": "π?πΈ", "top": False},
    "ig": {"name": "Igbo", "flag": "", "top": False},
    "ilo": {"name": "Ilocano", "flag": "", "top": False},
    "id": {"name": "Indonesian", "flag": "π?π©", "top": True},
    "ga": {"name": "Irish", "flag": "π?πͺ", "top": False},
    "it": {"name": "Italian", "flag": "π?πΉ", "top": True},
    "ja": {"name": "Japanese", "flag": "π―π΅", "top": True},
    "jv": {"name": "Javanese", "flag": "", "top": False},
    "kn": {"name": "Kannada", "flag": "", "top": False},
    "kk": {"name": "Kazakh", "flag": "π°πΏ", "top": False},
    "km": {"name": "Khmer", "flag": "", "top": False},
    "rw": {"name": "Kinyarwanda", "flag": "", "top": False},
    "gom": {"name": "Konkani", "flag": "", "top": False},
    "ko": {"name": "Korean", "flag": "π°π·", "top": True},
    "kri": {"name": "Krio", "flag": "", "top": False},
    "ku": {"name": "Kurdish", "flag": "π?πΆ", "top": False},
    "ckb": {"name": "Kurdish (Sorani)", "flag": "π?πΆ", "top": False},
    "ky": {"name": "Kyrgyz", "flag": "π°π¬", "top": False},
    "lo": {"name": "Lao", "flag": "π±π¦", "top": False},
    "la": {"name": "Latin", "flag": "", "top": True},
    "lv": {"name": "Latvian", "flag": "π±π»", "top": False},
    "ln": {"name": "Lingala", "flag": "", "top": False},
    "lt": {"name": "Lithuanian", "flag": "π±πΉ", "top": False},
    "lg": {"name": "Luganda", "flag": "", "top": False},
    "lb": {"name": "Luxembourgish", "flag": "π±πΊ", "top": False},
    "mk": {"name": "Macedonian", "flag": "π²π°", "top": False},
    "mai": {"name": "Maithili", "flag": "", "top": False},
    "mg": {"name": "Malagasy", "flag": "", "top": False},
    "ms": {"name": "Malay", "flag": "π²πΎ", "top": False},
    "ml": {"name": "Malayalam", "flag": "", "top": False},
    "mt": {"name": "Maltese", "flag": "π²πΉ", "top": False},
    "mi": {"name": "Maori", "flag": "", "top": False},
    "mr": {"name": "Marathi", "flag": "", "top": False},
    "mni-Mtei": {"name": "Meiteilon (Manipuri)", "flag": "", "top": False},
    "lus": {"name": "Mizo", "flag": "", "top": False},
    "mn": {"name": "Mongolian", "flag": "π²π³", "top": False},
    "my": {"name": "Myanmar (Burmese)", "flag": "π²π²", "top": False},
    "ne": {"name": "Nepali", "flag": "π³π΅", "top": False},
    "no": {"name": "Norwegian", "flag": "π³π΄", "top": False},
    "ny": {"name": "Nyanja (Chichewa)", "flag": "π²πΌ", "top": False},
    "or": {"name": "Odia (Oriya)", "flag": "", "top": False},
    "om": {"name": "Oromo", "flag": "πͺπΉ", "top": False},
    "ps": {"name": "Pashto", "flag": "π¦π«", "top": False},
    "fa": {"name": "Persian", "flag": "π?π·", "top": False},
    "pl": {"name": "Polish", "flag": "π΅π±", "top": True},
    "pt": {"name": "Portuguese", "flag": "π΅πΉ", "top": True},
    "pa": {"name": "Punjabi", "flag": "π΅π°", "top": False},
    "qu": {"name": "Quechua", "flag": "", "top": False},
    "ro": {"name": "Romanian", "flag": "π·π΄", "top": True},
    "ru": {"name": "Russian", "flag": "π·πΊ", "top": True},
    "sm": {"name": "Samoan", "flag": "πΌπΈ", "top": False},
    "sa": {"name": "Sanskrit", "flag": "", "top": False},
    "gd": {"name": "Scots Gaelic", "flag": "π΄σ §σ ’σ ³σ £σ ΄σ Ώ", "top": False},
    "nso": {"name": "Sepedi", "flag": "", "top": False},
    "sr": {"name": "Serbian", "flag": "π·πΈ", "top": False},
    "st": {"name": "Sesotho", "flag": "π±πΈ", "top": False},
    "sn": {"name": "Shona", "flag": "", "top": False},
    "sd": {"name": "Sindhi", "flag": "", "top": False},
    "si": {"name": "Sinhala (Sinhalese)", "flag": "π±π°", "top": False},
    "sk": {"name": "Slovak", "flag": "πΈπ°", "top": False},
    "sl": {"name": "Slovenian", "flag": "πΈπ?", "top": False},
    "so": {"name": "Somali", "flag": "πΈπ΄", "top": False},
    "es": {"name": "Spanish", "flag": "πͺπΈ", "top": True},
    "su": {"name": "Sundanese", "flag": "", "top": False},
    "sw": {"name": "Swahili", "flag": "πΉπΏ", "top": False},
    "sv": {"name": "Swedish", "flag": "πΈπͺ", "top": True},
    "tl": {"name": "Tagalog (Filipino)", "flag": "π΅π­", "top": False},
    "tg": {"name": "Tajik", "flag": "πΉπ―", "top": False},
    "ta": {"name": "Tamil", "flag": "", "top": False},
    "tt": {"name": "Tatar", "flag": "", "top": False},
    "te": {"name": "Telugu", "flag": "", "top": False},
    "th": {"name": "Thai", "flag": "πΉπ­", "top": False},
    "ti": {"name": "Tigrinya", "flag": "πͺπ·", "top": False},
    "ts": {"name": "Tsonga", "flag": "", "top": False},
    "tr": {"name": "Turkish", "flag": "πΉπ·", "top": False},
    "tk": {"name": "Turkmen", "flag": "πΉπ²", "top": False},
    "ak": {"name": "Twi (Akan)", "flag": "", "top": False},
    "uk": {"name": "Ukrainian", "flag": "πΊπ¦", "top": False},
    "ur": {"name": "Urdu", "flag": "π΅π°", "top": False},
    "ug": {"name": "Uyghur", "flag": "", "top": False},
    "uz": {"name": "Uzbek", "flag": "πΊπΏ", "top": False},
    "vi": {"name": "Vietnamese", "flag": "π»π³", "top": True},
    "cy": {"name": "Welsh", "flag": "π΄σ §σ ’σ ·σ ¬σ ³σ Ώ", "top": False},
    "xh": {"name": "Xhosa", "flag": "", "top": False},
    "yi": {"name": "Yiddish", "flag": "", "top": False},
    "yo": {"name": "Yoruba", "flag": "", "top": False},
    "zu": {"name": "Zulu", "flag": "", "top": False},
}

LANGUAGES_BY_NAME: dict[str, str] = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Assamese": "as",
    "Aymara": "ay",
    "Azerbaijani": "az",
    "Bambara": "bm",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bhojpuri": "bho",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-cn",
    "Chinese (Traditional)": "zh-tw",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dhivehi": "dv",
    "Dogri": "doi",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Ewe": "ee",
    "Filipino (Tagalog)": "fil",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Guarani": "gn",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Ilocano": "ilo",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Konkani": "gom",
    "Korean": "ko",
    "Krio": "kri",
    "Kurdish": "ku",
    "Kurdish (Sorani)": "ckb",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lingala": "ln",
    "Lithuanian": "lt",
    "Luganda": "lg",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Maithili": "mai",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Meiteilon (Manipuri)": "mni-Mtei",
    "Mizo": "lus",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or",
    "Oromo": "om",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Quechua": "qu",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Sanskrit": "sa",
    "Scots Gaelic": "gd",
    "Sepedi": "nso",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala (Sinhalese)": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog (Filipino)": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Tigrinya": "ti",
    "Tsonga": "ts",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Twi (Akan)": "ak",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}
