# Language Efficiency Analysis

Part of the YSP 2026 Language Complexity project.

## Contents
- `source/input.txt` — original English paragraph (from *The Old Man and the Sea*)
- `translated/` — the same paragraph translated into 133 languages, one `.txt` file per language (named by language code, e.g. `es.txt`, `zh-CN.txt`, `ja.txt`)

## How it was made
Translations were generated automatically using the `deep-translator` Python
library (Google Translate backend), looping through all 133 languages it
supports.

## Next steps
This output feeds into:
- Task 2: file size / compression measurement per language
- Task 3: IPA phonetic conversion per language
- Task 4: character complexity scoring per language's script


## Task 2: File Size & Compression Measurement

For all 133 translated files, we measured:
1. **Raw size** — the exact byte size of the text file as saved (UTF-8 encoded)
2. **Compressed size** — the byte size after zlib compression (same family as ZIP)
3. **Compression ratio** — compressed ÷ raw (lower = more redundant/compressible text)

### Method
- Used Python's built-in `zlib` library, `zlib.compress(data, level=9)` for maximum compression
- Measured all 133 language files automatically via a loop, no manual work

### Key findings
- **Smallest raw files:** Chinese (Simplified & Traditional) — each character encodes a
  whole syllable/concept, needing far fewer characters than Latin-alphabet languages
- **Largest raw files:** Indic/Southeast Asian scripts (Tamil, Malayalam, Kannada, Khmer,
  Burmese) — multi-byte UTF-8 encoding plus more verbose grammar structures push these
  up to ~3x the size of Chinese for the same paragraph
- **Compression behavior varies by script:** Chinese text was already near its most
  compact form (raw ≈ compressed), while some Indic scripts showed less internal
  repetition to compress away despite their larger raw size

### Files
- `sizes.csv` — full results table (language, raw size, compressed size, ratio)
- `file_sizes_all.png` — bar chart of all 133 languages, raw size only
- `file_sizes_comparison.png` — bar chart comparing raw vs compressed size per language
