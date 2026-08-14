import os
import pandas as pd
from pathlib import Path
TRANSLATED_DIR = Path("HumanRights_IPA")
SOURCE_FILENAME = "HumanRights"
SOURCE_LANGUAGES ={
    "(Arabic)",
    '(Chinese)',
    '(English)',
    '(Japanese)',
    '(Korean)',
    '(Portuguese)',
    '(Quechua)',
    '(Russian)',
    '(Spanish)'
}

files = sorted(TRANSLATED_DIR.glob("*.txt"))
num_files = len(files)
print(f"Found {num_files} translated files")

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
    
    
    text = file.read_text()

    stats = analyze_text(text)
    for lang in SOURCE_LANGUAGES:
            if file.name.find(f"{lang}") != -1:
                source_language = lang
                break
            else: source_language= 'Not found'
    stats["Source_Language"] = source_language

    language = file.name.replace(".txt","")
    language = file.name.replace(f"{SOURCE_FILENAME}","")
    stats["Language"] = language

    results.append(stats)

df = pd.DataFrame(results)

df = df.sort_values("Character Count")

df.head()
print(df.describe())


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)



df.to_csv("character_statistics.csv", index=False)

print("Saved as character_statistics.csv")

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib as mpl
from cycler import cycler
num_plots = num_files

colormap = mpl.colormaps["Set1"]

colors = {
    '(Arabic)' : 'red',
    '(Chinese)': 'blue',
    '(English)': 'orange',
    '(Japanese)': 'purple',
    '(Korean)': 'green',
    '(Portuguese)': 'cyan',
    '(Quechua)': 'grey',
    '(Russian)': 'maroon',
    '(Spanish)': 'brown'
}

print(colors)
color_list = [colors[lang] for lang in df["Source_Language"]]



def create_graph(graph: pd.DataFrame, axis_x: str ='', axis_y: str =''):
        
    plt.figure(figsize =(50,10))
    plt.scatter(graph[axis_x], graph[axis_y])
    plt.grid(axis='y')
    plt.xticks(rotation=90)
    plt.ylabel(f"{axis_y}")
    plt.title(f"{axis_y} Across {num_files} Languages")
    plt.tight_layout()
#    plt.savefig(f"character_analysis_v2/IPA {axis_y} for {num_files} Languages.png", dpi=300, bbox_inches="tight")

    return 
def create_subplot(graph: pd.DataFrame):
    i=1
    plt.subplots(3,3, sharey= True, figsize = [50,40])

    for lang in colors:
        plt.subplot(3,3,i)
        source = graph[graph["Source_Language"] == lang]

        plt.scatter(source["Language"], source["Character Count"], c = colors[lang])
        plt.grid(axis = 'both')
        plt.xticks(rotation=90)
        plt.ylabel("Language")
        plt.title(f"{lang}")

        i+=1

    plt.suptitle(f"Languages Across {num_files} Languages")
    plt.tight_layout()
    
    plt.savefig(f"character_analysis_v2/Subplotted.png", dpi=300, bbox_inches="tight")
    return
#create_graph(df,"Language", "Character Count")
#create_graph(df,"Language", "Character Count (No Spaces)")
#df = df.sort_values("Unique Characters")
#create_graph(df,"Language", "Unique Characters")
create_subplot(df)
'''
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
plt.title(f"Character Count With (Blue) and Without (Red) Spaces Across {num_files} Languages")
plt.tight_layout()
plt.savefig(f"character_analysis_v2/IPA Character Count With and Without Spaces for {num_files} Languages.png", dpi=300, bbox_inches="tight")



from collections import Counter

for file in files[:5]:  # First 5 languages for testing

    language = file.name.replace(".txt", "")

    text = file.read_text()

    chars = [c for c in text if not c.isspace()]

    freq = Counter(chars)

    print(f"\n{language}")
    print(freq.most_common(20))

    import unicodedata

for file in files[:5]:

    language = file.name.replace(".txt","")

    text = file.read_text()

    unique = sorted(set(text))

    print("\n", language)

    for c in unique[:20]:

        if c.strip():

            print(
                c,
                hex(ord(c)),
                unicodedata.name(c,"Unknown")
            )
'''