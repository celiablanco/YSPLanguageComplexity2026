# YSP Language Efficiency — Section 1: Translation

## Folder contents
- translated_output.csv — master table, 133 languages + English baseline row
- translated_files/ — one .txt per language, named {language}_{language_code}.txt
- translated_files/language_code_lookup.csv — language name to code reference
- character_analysis/character_statistics.csv — per-language word/character stats
- character_analysis/full_133_ranking_chart.png — character efficiency bar chart
- character_analysis/environment_info.txt — Python/library versions used

## Column definitions (translated_output.csv)
| Column | Meaning |
|---|---|
| language | Language name |
| language_code | ISO-style code (e.g. 'ja') — use this to key into IPA libraries |
| translated_text | Full translated text |
| char_count | Character count of translated text |
| file_size | Raw UTF-8 byte size |
| compressed_size | zlib/DEFLATE compressed byte size |
| compression_ratio | compressed_size / file_size (lower = more redundant text) |
| status | 'success' or 'failed: <error>' |

character_statistics.csv adds: word_count, avg_characters_per_word, unique_characters.

## Source text
Federalist Papers (Project Gutenberg), cleaned to 77,902 characters.

## Next step (Section 2 — IPA Conversion, )
Read translated_output.csv, use language_code to map into IPA libraries, add an ipa_text column, save as translated_with_ipa.csv.
