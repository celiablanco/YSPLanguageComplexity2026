import os
import pandas as pd

TRANSLATED_DIR = "HumanRights_IPA"

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

df = df.sort_values("Character Count")

df.head()



pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)



df.to_csv("character_statistics.csv", index=False)

print("Saved as character_statistics.csv")

import matplotlib.pyplot as plt
import numpy as np

plt.figure(figsize =(50,10))
plt.scatter(df["Language"], df["Character Count"])
plt.grid(axis='y')
plt.xticks(rotation=90)
plt.ylabel("Character Count")
plt.title(f"Character Count Across {len(files)} Languages")
plt.tight_layout()
plt.savefig(f"character_analysis_v2/IPA Character_Count for {len(files)} Languages.png", dpi=300, bbox_inches="tight")

plt.figure(figsize =(50,10))
plt.scatter(df["Language"], df["Character Count (No Spaces)"])
plt.grid(axis='y')
plt.xticks(rotation=90)
plt.ylabel("Character Count (No Spaces)")
plt.title(f"Character Count (No Spaces) Across {len(files)} Languages")
plt.tight_layout()
plt.savefig(f"character_analysis_v2/IPA Character Count (No Spaces) for {len(files)} Languages.png", dpi=300, bbox_inches="tight")

x=np.array(df["Language"])
y=np.array(df["Character Count"])
plt.scatter(x,y, color = 'blue')
plt.grid(axis='y')
plt.xticks(rotation=90)
y=np.array(df["Character Count (No Spaces)"])
plt.scatter(x,y,color = 'red')
plt.grid(axis='y')
plt.xticks(rotation=90)

plt.ylabel("Character Count")
plt.title(f"Character Count With (Blue) and Without (Red) Spaces Across {len(files)} Languages")
plt.tight_layout()
plt.savefig(f"character_analysis_v2/IPA Character Count With and Without Spaces for {len(files)} Languages.png", dpi=300, bbox_inches="tight")



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