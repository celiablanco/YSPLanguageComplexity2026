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
from collections import Counter, OrderedDict
from typing import Any, Dict


def analyze_text(text):

    text_count = Counter(text)
    # Unicode characters (code points)
    character_count = text_count.total()

    # Ignore spaces for some analyses
    characters_no_space = [c for c in text if not c.isspace()]
    characters_no_space.count
    character_count_no_spaces = len(characters_no_space)

    # Unique_Characters
    unique_characters =len(list(text_count))

    
    #Character_frequency
    del text_count[' ']
    del text_count['\n']
    freq = text_count

    return {
        "Character_Count": character_count,
        "Character_Count_(No_Spaces)": character_count_no_spaces,
        "Unique_Characters": unique_characters,
        "Character_Frequency": freq
    }

results = []

for file in files:
    
    text = file.read_text()
    stats : dict[Any,Any]
    stats = analyze_text(text)
    for lang in SOURCE_LANGUAGES:
            if file.name.find(f"{lang}") != -1:
                source_language = lang
                break
            else: source_language= 'Not found'
    stats["Source_Language"] = source_language

    language = file.name.removesuffix(".txt")
    language = language.replace(f"{SOURCE_FILENAME}","")
    language = language.replace(f"{source_language}","")
    stats["Language"] = language

    results.append(stats)

df = pd.DataFrame(results)

df = df.sort_values("Character_Count")

print(df.describe())


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)



df.to_csv("character_statistics.csv", index=False)

print("Saved as character_statistics.csv")

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as mpl
import matplotlib.patches as mpatches

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
colors_legend= []
for lang, color in colors.items():
     colors_legend.append(mpatches.Patch(color = color, label = lang))


def create_graph(graph: pd.DataFrame, axis_x: pd.DataFrame, axis_y: pd.DataFrame, title: str ='None'):
        
    plt.figure(figsize =(20,10))
    plt.scatter(axis_x, axis_y, c = color_list)
    plt.legend(handles = colors_legend)
    plt.grid(axis='y')
    plt.xticks(rotation=90)
#    plt.ylabel(f"{axis_y}")
#    plt.ylabel(f"Character_Count_(No_Spaces)")
    plt.title(f"{title}")
    plt.tight_layout()
    plt.savefig(f"character_analysis_v2/{title}.png", dpi=200, bbox_inches="tight")
    plt.close()

    return 
def create_subplot(graph: pd.DataFrame):
    i=1
    plt.subplots(3,3, sharey= True, figsize = [50,40])

    for lang in colors:
        plt.subplot(3,3,i)
        source = graph[graph["Source_Language"] == lang]

        plt.scatter(source["Language"], source["Character_Count_(No_Spaces)"], c = colors[lang])
        plt.grid(axis = 'both')
        plt.xticks(rotation=90)
        plt.ylabel("Language")
        plt.title(f"{lang}")

        i+=1

    plt.suptitle(f"Languages Across {num_files} Languages")
    plt.tight_layout()
    
    plt.savefig(f"character_analysis_v2/Character_Count_(No_Spaces) per language before translation.png", dpi=300, bbox_inches="tight")
    return
#create_graph(df,"Language", "Character_Count")
df.sort_values("Character_Count_(No_Spaces)")
create_graph(df,df["Language"], df["Character_Count_(No_Spaces)"], "Character Count (no spaces)")
#df = df.sort_values("Unique_Characters")

#create_subplot(df)

############Unique Characters################
df.sort_values("Unique_Characters")
create_graph(df,df["Language"], df["Unique_Characters"], "Unique characters amount")

#############Frequency##################
total_frequency = Counter()
for counter in df["Character_Frequency"]:
     total_frequency= total_frequency + counter
total_frequency = OrderedDict(total_frequency.most_common())
plt.figure(figsize= (20,8))
plt.bar(list(total_frequency.keys()),list(total_frequency.values()))
plt.savefig(f"character_analysis_v2/Total_Frequency", dpi=300, bbox_inches="tight")
plt.title("Total Frequency of Characters")



'''

x=np.array(df["Language"])
y=np.array(df["Character_Count"])
plt.scatter(x,y, color = 'blue')
plt.grid(axis='y')
plt.xticks(rotation=90)
y=np.array(df["Character_Count_(No_Spaces)"])
plt.scatter(x,y,color = 'red')
plt.grid(axis='y')
plt.xticks(rotation=90)

plt.ylabel("Character_Count")
plt.title(f"Character_Count With (Blue) and Without (Red) Spaces Across {num_files} Languages")
plt.tight_layout()
plt.savefig(f"character_analysis_v2/IPA Character_Count With and Without Spaces for {num_files} Languages.png", dpi=300, bbox_inches="tight")


import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


data= []
for file in files[:5]:  # First 5 languages for testing
    
    language = file.name.replace(".txt", "")

    text = file.read_text()


    freq = Counter(text)
    lang_map = {language:freq}
    print(lang_map)
    data.append(lang_map)

    
char_freq= pd.DataFrame(data)
print(char_freq.head())
char_freq.to_csv("character_frequency.csv", index=False)
#create_graph(char_freq, char_freq[''])
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