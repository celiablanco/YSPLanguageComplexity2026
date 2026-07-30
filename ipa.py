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
    "myanmar": "my",
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
            preserve_empty_lines= True
        )
    time.sleep(0.2)

    return "\n".join(ipa)


def process_folder(forced_lang: str | None, with_stress: bool, separator: str):
    SOURCE_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    txt_files = sorted(SOURCE_DIR.glob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in '{SOURCE_DIR}/'. Add files and try again.")
        return

    print(f"Found {len(txt_files)} file(s) → saving IPA output to '{OUTPUT_DIR}/'\n")
    success, failed, skipped = [], [], []

    for file in txt_files:
        lang = None
        print(f"[{file.name}]")
        out_path= f"{file.stem}_ipa.txt"
        if os.path.exists(out_path):
            print(f"{file.name} -> already done, skipping")
            continue

        text = file.read_text(encoding="utf-8")

        if not text.strip():
            print("  Skipped (empty file).\n")
            skipped.append(file.name)
            continue

        # Determine language
        if forced_lang:
            lang = forced_lang
            print(f"  Language: {lang} (forced)")
        else:
            try:
                for (language,tag) in LANG_MAP.items():
                    if file.name.find(f"_{tag}.txt") != -1:
                        lang = tag
                        break
            except LangDetectException:
                    return None
            
            if not lang:
                    print("  Could not detect language — skipping.\n")
                    failed.append(file.name)
                    continue
            print(f"  Detected language: {lang}")

        if lang not in SUPPORTED_ESPEAK.keys():
            print(f"  Language '{lang}' not supported by espeak-ng — skipping.\n")
            failed.append(file.name)
            continue

        try:
            text = text.splitlines()
            ipa_text = convert_ipa(text, lang, with_stress, separator)
            out_path = OUTPUT_DIR / f"{SUPPORTED_ESPEAK[lang]}.txt"
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
    parser = argparse.ArgumentParser(
        description="Convert all .txt files in 'translated/' to IPA and save to 'ipa/'."
    )
    parser.add_argument(
        "--lang",
        default=None,
        help="Force a specific espeak-ng language tag for all files (e.g. 'en-us', 'fr-fr', 'de'). "
             "Defaults to auto-detection.",
    )
    parser.add_argument(
        "--no-stress",
        action="store_true",
        help="Omit stress markers (ˈ and ˌ) from the IPA output.",
    )
    parser.add_argument(
        "--separator",
        default=" ",
        help="String placed between IPA words (default: single space).",
    )

    args = parser.parse_args()

    if args.lang and args.lang not in SUPPORTED_ESPEAK:
        sys.exit(
            f"Language tag '{args.lang}' is not supported by espeak-ng.\n"
            "Run: python -c \"from phonemizer.backend import EspeakBackend; "
            "print(list(EspeakBackend.supported_languages().keys()))\" to see all options."
        )

    process_folder(
        forced_lang=args.lang,
        with_stress=not args.no_stress,
        separator=args.separator,
    )


if __name__ == "__main__":
    main()