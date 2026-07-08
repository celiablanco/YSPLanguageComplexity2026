#!/usr/bin/env python3
"""
to_ipa.py

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
    python to_ipa.py
    python to_ipa.py --lang es            # force a single language for all files
    python to_ipa.py --no-stress          # omit stress markers (ˈ ˌ)
    python to_ipa.py --separator " | "   # custom separator between words
"""
import os
os.environ["PHONEMIZER_ESPEAK_LIBRARY"] = r"C:\Program Files\eSpeak NG\libespeak-ng.dll"
import argparse
import sys
from pathlib import Path

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

# Maps common langdetect ISO-639-1 codes → espeak-ng language tags
LANG_MAP: dict[str, str] = {
    "af": "af",
    "ar": "ar",
    "bg": "bg",
    "bn": "bn",
    "bs": "bs",
    "ca": "ca",
    "cs": "cs",
    "cy": "cy",
    "da": "da",
    "de": "de",
    "el": "el",
    "en": "en-us",
    "eo": "eo",
    "es": "es",
    "et": "et",
    "eu": "eu",
    "fa": "fa",
    "fi": "fi",
    "fr": "fr-fr",
    "ga": "ga",
    "gu": "gu",
    "he": "he",
    "hi": "hi",
    "hr": "hr",
    "hu": "hu",
    "hy": "hy",
    "id": "id",
    "is": "is",
    "it": "it",
    "ja": "ja",
    "ka": "ka",
    "kn": "kn",
    "ko": "ko",
    "lt": "lt",
    "lv": "lv",
    "mk": "mk",
    "ml": "ml",
    "mr": "mr",
    "ms": "ms",
    "mt": "mt",
    "my": "my",
    "nb": "nb",
    "ne": "ne",
    "nl": "nl",
    "or": "or",
    "pa": "pa",
    "pl": "pl",
    "pt": "pt",
    "ro": "ro",
    "ru": "ru",
    "si": "si",
    "sk": "sk",
    "sl": "sl",
    "sq": "sq",
    "sr": "sr",
    "sv": "sv",
    "sw": "sw",
    "ta": "ta",
    "te": "te",
    "th": "th",
    "tl": "es",   # Tagalog — approximate with Spanish phonology
    "tr": "tr",
    "uk": "uk",
    "ur": "ur",
    "uz": "uz",
    "vi": "vi",
    "zh-cn": "cmn",
    "zh-tw": "cmn",
    "zh": "cmn",
}

SUPPORTED_ESPEAK = set(EspeakBackend.supported_languages().keys())


def detect_language(text: str) -> str | None:
    """Return the best-matching espeak-ng language tag for the given text."""
    try:
        lang_code = detect(text)
    except LangDetectException:
        return None

    espeak_tag = LANG_MAP.get(lang_code)

    # If not in our map, try the raw code directly against espeak's list
    if not espeak_tag:
        if lang_code in SUPPORTED_ESPEAK:
            espeak_tag = lang_code
        else:
            # Try prefix match (e.g. "zh-cn" → "cmn")
            prefix = lang_code.split("-")[0]
            matches = [tag for tag in SUPPORTED_ESPEAK if tag == prefix or tag.startswith(prefix + "-")]
            espeak_tag = matches[0] if matches else None

    return espeak_tag


def convert_to_ipa(text: str, lang: str, with_stress: bool, separator: str) -> str:
    """Convert a block of text to IPA using the espeak-ng backend."""
    lines = text.splitlines()
    ipa_lines = []

    for line in lines:
        if not line.strip():
            ipa_lines.append("")
            continue

        ipa = phonemize(
            line,
            backend="espeak",
            language=lang,
            with_stress=with_stress,
            njobs=1,
            separator=Separator(word=separator, phone="", syllable=""),
        )
        ipa_lines.append(ipa.strip())

    return "\n".join(ipa_lines)


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
        print(f"[{file.name}]")
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
            lang = detect_language(text)
            if not lang:
                print("  Could not detect language — skipping.\n")
                failed.append(file.name)
                continue
            print(f"  Detected language: {lang}")

        if lang not in SUPPORTED_ESPEAK:
            print(f"  Language '{lang}' not supported by espeak-ng — skipping.\n")
            failed.append(file.name)
            continue

        try:
            ipa_text = convert_to_ipa(text, lang, with_stress, separator)
            out_path = OUTPUT_DIR / f"{file.stem}_ipa.txt"
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