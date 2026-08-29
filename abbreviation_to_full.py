
import os
os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
os.environ["PHONEMIZER_ESPEAK_PATH"] = r"C:\Program Files\eSpeak NG"
import argparse
import sys
from pathlib import Path
import time
import logging

# ── Dependency checks ────────────────────────────────────────────────────────
try:
    from phonemizer import phonemize
    from phonemizer.backend import EspeakBackend
    from phonemizer.separator import Separator
except ImportError:
    sys.exit(
        "Missing dependency 'phonemizer'.\n"
        "Install it with: pip install phonemizer\n"
        "Also install espeak-ng: sudo apt-get install espeak-ng  (or brew install espeak-ng)"
    )

try:
    from langdetect import detect, LangDetectException
except ImportError:
    sys.exit("Missing dependency 'langdetect'.\nInstall it with: pip install langdetect")

# ── Constants ─────────────────────────────────────────────────────────────────
SOURCE_DIR = Path("translated")
OUTPUT_DIR = Path("ipa")
os.makedirs("kana", exist_ok=True)
KANA_DIR = Path("kana")

LANG_MAP: dict[str,str]={
    "afrikaans": "af",
    "albanian": "sq",
    "amharic": "am",
    "arabic": "ar",
    "armenian": "hy",
    "assamese": "as",
    "aymara": "ay",
    "azerbaijani": "az",
    "bambara": "bm",
    "basque": "eu",
    "belarusian": "be",
    "bengali": "bn",
    "bhojpuri": "bho",
    "bosnian": "bs",
    "bulgarian": "bg",
    "catalan": "ca",
    "cebuano": "ceb",
    "chichewa": "ny",
    "chinese (simplified)": "cmn",
    "chinese (traditional)": "cmn",
    "corsican": "co",
    "croatian": "hr",
    "czech": "cs",
    "danish": "da",
    "dhivehi": "dv",
    "dogri": "doi",
    "dutch": "nl",
    "english": "en",
    "esperanto": "eo",
    "estonian": "et",
    "ewe": "ee",
    "filipino": "tl",
    "finnish": "fi",
    "french": "fr",
    "frisian": "fy",
    "galician": "gl",
    "georgian": "ka",
    "german": "de",
    "greek": "el",
    "guarani": "gn",
    "gujarati": "gu",
    "haitian creole": "ht",
    "hausa": "ha",
    "hawaiian": "haw",
    "hebrew": "iw", #Another exceppition on abbreviation
    "hindi": "hi",
    "hmong": "hmn",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "ilocano": "ilo",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    "japanese": "ja",
    "javanese": "jw",
    "kannada": "kn",
    "kazakh": "kk",
    "khmer": "km",
    "kinyarwanda": "rw",
    "konkani": "gom",
    "korean": "ko",
    "krio": "kri",
    "kurdish (kurmanji)": "ku",
    "kurdish (sorani)": "ckb",
    "kyrgyz": "ky",
    "lao": "lo",
    "latin": "la",
    "latvian": "lv",
    "lingala": "ln",
    "lithuanian": "lt",
    "luganda": "lg",
    "luxembourgish": "lb",
    "macedonian": "mk",
    "maithili": "mai",
    "malagasy": "mg",
    "malay": "ms",
    "malayalam": "ml",
    "maltese": "mt",
    "maori": "mi",
    "marathi": "mr",
    "meiteilon (manipuri)": "mni-Mtei",
    "mizo": "lus",
    "mongolian": "mn",
 #   "myanmar": "my",
    "nepali": "ne",
    "norwegian": "no",
    "odia (oriya)": "or",
    "oromo": "om",
    "pashto": "ps",
    "persian": "fa",
    "polish": "pl",
    "portuguese": "pt",
    "punjabi": "pa",
    "quechua": "qu",
    "romanian": "ro",
    "russian": "ru",
    "samoan": "sm",
    "sanskrit": "sa",
    "scots gaelic": "gd",
    "sepedi": "nso",
    "serbian": "sr",
    "sesotho": "st",
    "shona": "sn",
    "sindhi": "sd",
    "sinhala": "si",
    "slovak": "sk",
    "slovenian": "sl",
    "somali": "so",
    "spanish": "es",
    "sundanese": "su",
    "swahili": "sw",
    "swedish": "sv",
    "tajik": "tg",
    "tamil": "ta",
    "tatar": "tt",
    "telugu": "te",
    "thai": "th",
    "tigrinya": "ti",
    "tsonga": "ts",
    "turkish": "tr",
    "turkmen": "tk",
    "twi": "ak",
    "ukrainian": "uk",
    "urdu": "ur",
    "uyghur": "ug",
    "uzbek": "uz",
    "vietnamese": "vi",
    "welsh": "cy",
    "xhosa": "xh",
    "yiddish": "yi",
    "yoruba": "yo",
    "zulu": "zu",
}

SUPPORTED_ESPEAK = EspeakBackend.supported_languages()
output_path = Path("Failed_languages")
names = []
text = output_path.read_text(encoding="utf-8")
for (language,tag) in LANG_MAP.items():
    if text.find(f"{tag}.txt") != -1:
      lang = tag
      names.append(f"{language}")
print(names)
list = Path("list_of_languages")
list.write_text("\n".join(names), encoding="utf-8")
