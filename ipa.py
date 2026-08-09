#!/usr/bin/env python3
""" ipa.py

Reads all .txt files from a 'translated/' folder, auto-detects each file's
language, converts the text to standard IPA notation, and saves the results
to an 'ipa/' folder.

Setup:
    # System dependency (needed once):
    sudo apt-get install espeak-ng        # Debian/Ubuntu/WSL
    brew install espeak-ng                # macOS

    # Python packages:
    pip install phonemizer langdetect

Usage:
    python ipa.py
    python ipa.py --lang es            # force a single language for all files
    python ipa.py --no-stress          # omit stress markers (ˈ ˌ)
    python ipa.py --separator " | "   # custom separator between words
"""
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
SOURCE_DIR = Path("HumanRights_translated")
OUTPUT_DIR = Path("HumanRights_IPA")

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
    "hebrew": "iw",
    "hindi": "hi",
    "hmong": "hmn",
    "hungarian": "hu",
    "icelandic": "is",
    "igbo": "ig",
    "ilocano": "ilo",
    "indonesian": "id",
    "irish": "ga",
    "italian": "it",
    #"japanese": "ja",
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

def lang_detect(filename: str):
  if filename.find(f"zh-CN.txt") != -1:
      lang = 'yue'
      return lang
  if filename.find(f"zh-TW.txt") != -1:
      lang = 'cmn'
      return lang
  for (language,tag) in LANG_MAP.items():
    if filename.find(f"{tag}.txt") != -1:
      lang = tag
      if lang not in SUPPORTED_ESPEAK.keys():
        prefix = tag.split("-")[0]
        matches = [code for code in SUPPORTED_ESPEAK if code == prefix or code.startswith(prefix + "-")]
        if matches:
          lang = matches[0] 
      return lang
  #2 exceptions where the GoogleTranslate tag doesn't match ESPEAK, didn't know a better way to do it
  #I put Cantonese on Simplified Chinese / and Mandarin on Tradicional Chinese
  
  return None

def convert_ipa(text: list[str], lang: str, with_stress: bool, separator: str) -> str:
    """Convert a block of text to IPA using the espeak-ng backend."""

    ipa_lines = []
    

    ipa = phonemize(
            text,
            backend="espeak",
            language=lang,
            with_stress=with_stress,
            njobs=1,
            separator=Separator(word=separator, phone="", syllable=""),
            language_switch= 'remove-flags',
            preserve_empty_lines= True,
            words_mismatch= 'warn',
            logger = logging.getLogger()
        )
    logging.info('Language is %s', lang)
    
    time.sleep(0.2)

    return "\n".join(ipa)


def process_folder():
    SOURCE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    txt_files = sorted(SOURCE_DIR.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in '{SOURCE_DIR}/'. Add files and try again.")
        return

    print(f"Found {len(txt_files)} file(s) → saving IPA output to '{OUTPUT_DIR}/'\n")
    success, failed, skipped = [], [], []

    for file in txt_files:
        print(f"[{file.name}]")
        lang = lang_detect(file.name)

        if not lang:
            print("  Could not detect language — skipping.\n")
            failed.append(file.name)
            continue
        print(f"  Detected language: {lang}")
        if lang not in SUPPORTED_ESPEAK.keys():
            print(f"  Language '{lang}' not supported by espeak-ng — skipping.\n")
            failed.append(file.name)
            continue

        language_fullname = SUPPORTED_ESPEAK[lang]
        out_path= f"{file.stem}{language_fullname}.txt"
        out_path = OUTPUT_DIR / out_path

        if os.path.exists(out_path):
            print(f"{file.name} -> already done, skipping")
            continue

        text = file.read_text(encoding="utf-8")

        if not text.strip():
            print("  Skipped (empty file).\n")
            skipped.append(file.name)
            continue

        try:
            text = text.splitlines()
            ipa_text = convert_ipa(text, lang, with_stress = False, separator = " ")
            out_path = OUTPUT_DIR / f"{file.stem}{SUPPORTED_ESPEAK[lang]}.txt"
            out_path.write_text(ipa_text, encoding="utf-8")
            print(f"  Saved → {out_path}\n")
            success.append(file.name)
        except Exception as e:
            print(f"  ERROR: {e}\n")
            failed.append(file.name)

    # ── Summary ───────────────────────────────────────────────────────────────
    print("─" * 45)
    print(f"Done. {len(success)} converted | {len(skipped)} skipped | {len(failed)} failed.")
    if failed:
        print("Failed files:")
        for f in failed:
            print(f"  • {f}")


def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    process_folder()
    
if __name__ == "__main__":
    main()