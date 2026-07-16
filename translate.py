#!/usr/bin/env python3
"""
translate_file.py

Reads a text file and translates its contents into any target language.

Setup:
    pip install deep-translator

Usage:
    python translate_file.py input.txt es
    python translate_file.py input.txt fr --output translated_fr.txt
    python translate_file.py input.txt ja --source en

Notes:
    - Target/source languages can be given as language codes (e.g. "es", "fr", "ja")
      or full names (e.g. "spanish", "french", "japanese").
    - Source defaults to "auto" (auto-detect).
    - Large files are automatically split into chunks to respect the
      translation service's character limits, then reassembled.
"""

import argparse
import sys
from pathlib import Path
import os

try:
    from deep_translator import GoogleTranslator
except ImportError:
    sys.exit(
        "Missing dependency 'deep-translator'.\n"
        "Install it with: pip install deep-translator"
    )

MAX_CHUNK_SIZE = 1500  # stay safely under the translator's ~5000 char limit


def chunk_text(text: str, max_size: int = MAX_CHUNK_SIZE):
    """Split text into chunks without breaking in the middle of a paragraph
    or sentence whenever possible."""
    paragraphs = text.split("\n")
    chunks = []
    current = ""

    for para in paragraphs:
        candidate = current + ("\n" if current else "") + para

        if len(candidate) <= max_size:
            current = candidate
            continue

        # current paragraph addition would overflow the chunk
        if current:
            chunks.append(current)
            current = ""

        # if a single paragraph itself is too long, split it further
        if len(para) > max_size:
            for i in range(0, len(para), max_size):
                chunks.append(para[i : i + max_size])
        else:
            current = para

    if current:
        chunks.append(current)

    return chunks


def translate_file(input_path: str, target_lang: str, source_lang: str = "auto", output_path: Path = None):
    in_path = Path(input_path)
    if not in_path.exists():
        sys.exit(f"Input file not found: {input_path}")

    text = in_path.read_text(encoding="utf-8")
    if not text.strip():
        sys.exit("Input file is empty.")

    translator = GoogleTranslator(source=source_lang, target=target_lang) #Don't initiate a bunch of these, instead change the translator.source/translator.target
    chunks = chunk_text(text)

    translated_chunks = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"Translating chunk {i}/{len(chunks)}...")
        translated_chunks.append(translator.translate(chunk))

    translated_text = "\n".join(translated_chunks)
    if output_path is None:
        output_path = '.'
    filename = str(f"{in_path.stem}_{target_lang}{in_path.suffix}")

    Path(output_path,filename).write_text(translated_text, encoding="utf-8")
    print(f"\nDone. Translated file saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Translate a text file into any language.")
    #parser.add_argument("input_file", help="Path to the text file to translate")
    #parser.add_argument("target_language", help="Target language code or name (e.g. 'es', 'french')")
    #parser.add_argument("--source", default="auto", help="Source language code (default: auto-detect)")
    #parser.add_argument("--output", default=None, help="Path for the translated output file")
    
    target_languages = {
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
    "chinese (simplified)": "zh-CN",
    "chinese (traditional)": "zh-TW",
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
    output= Path("translated")
    for filename in os.listdir('source'):
        for language in target_languages:
            translate_file(os.path.join('source',filename),language,'auto',output)
    args = parser.parse_args()
    'translate_file(args.input_file, args.target_language, args.source, args.output)'


if __name__ == "__main__":
    main()