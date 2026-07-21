import os
import pandas as pd

TRANSLATED_DIR = "ipa"

files = sorted([f for f in os.listdir(TRANSLATED_DIR) if f.endswith(".txt")])

print(f"Found {len(files)} translated files")

import re
from collections import Counter

def analyze_text(text):

    # Unicode characters (code points)
    character_count = len(text)

    # Ignore spaces for some analyses
    characters_no_space = [c for c in text if not c.isspace()]

    character_count_no_spaces = len(characters_no_space)

    # Unique characters
    unique_characters = len(set(characters_no_space))

    # Words
    words = text.split()
    word_count = len(words)

    # Sentences
    sentences = re.split(r'[.!?。！？]+', text)
    sentences = [s for s in sentences if s.strip()]
    sentence_count = len(sentences)

    avg_chars_per_word = (
        character_count_no_spaces / word_count
        if word_count else 0
    )

    avg_words_per_sentence = (
        word_count / sentence_count
        if sentence_count else 0
    )

    avg_chars_per_sentence = (
        character_count_no_spaces / sentence_count
        if sentence_count else 0
    )

    return {
        "Character Count": character_count,
        "Character Count (No Spaces)": character_count_no_spaces,
        "Unique Characters": unique_characters,
        "Word Count": word_count,
        "Sentence Count": sentence_count,
        "Characters / Word": avg_chars_per_word,
        "Words / Sentence": avg_words_per_sentence,
        "Characters / Sentence": avg_chars_per_sentence,
    }

results = []

for file in files:

    language = file.replace(".txt","")

    with open(os.path.join(TRANSLATED_DIR,file),
              encoding="utf-8") as f:

        text = f.read()

    stats = analyze_text(text)

    stats["Language"] = language

    results.append(stats)

df = pd.DataFrame(results)

df = df.sort_values("Language")

df.head()



pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)



df.to_csv("character_statistics.csv", index=False)

print("Saved as character_statistics.csv")

import matplotlib.pyplot as plt

plt.figure(figsize=(20,6))

plt.bar(df["Language"], df["Character Count"])

plt.xticks(rotation=90)

plt.ylabel("Character Count")

plt.title("Character Count Across 133 Languages")

plt.tight_layout()
plt.savefig("character_analysis_v2/Character_Count_Across_133_Languages.png", dpi=300, bbox_inches="tight")


plt.show()

plt.figure(figsize=(20,6))

plt.bar(df["Language"], df["Unique Characters"])

plt.xticks(rotation=90)

plt.ylabel("Unique Characters")

plt.title("Unique Characters Used")

plt.tight_layout()
plt.savefig("character_analysis_v2/unique_characters.png", dpi=300, bbox_inches="tight")

plt.show()

plt.figure(figsize=(20,6))

plt.bar(df["Language"], df["Characters / Word"])

plt.xticks(rotation=90)

plt.ylabel("Characters per Word")

plt.title("Average Characters per Word")

plt.tight_layout()
plt.savefig("character_analysis_v2/average_characters_per_word.png", dpi=300, bbox_inches="tight")

plt.show()

from collections import Counter

for file in files[:5]:  # First 5 languages for testing

    language = file.replace(".txt", "")

    with open(os.path.join(TRANSLATED_DIR, file),
              encoding="utf-8") as f:

        text = f.read()

    chars = [c for c in text if not c.isspace()]

    freq = Counter(chars)

    print(f"\n{language}")
    print(freq.most_common(20))

    import unicodedata

for file in files[:5]:

    language = file.replace(".txt","")

    with open(os.path.join(TRANSLATED_DIR,file),
              encoding="utf-8") as f:

        text = f.read()

    unique = sorted(set(text))

    print("\n", language)

    for c in unique[:20]:

        if c.strip():

            print(
                c,
                hex(ord(c)),
                unicodedata.name(c,"Unknown")
            )