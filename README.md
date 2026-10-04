# YSPLanguageComplexity2026
Repo for code and data for YSP26 Language Complexity project

The project title is "Comparative Exploration of Language Efficiency", it has the objective of exploring the efficiency of enconding of written languages.

# This tree branch contains **IPA (International Phonetic Alphabet) related content.**

### _character_statistics.csv_ is the data of the length and frequency of characters of all files after being converted to IPA. 
    - "Character_Count" is the amount of characters in each files.
    - "Character_Count_(No_Spaces)" is the amount of characters excluding whitespaces.
    - "Unique_Characters" is how many different IPA symbols were used.
    - "Character_Frequency" is a Counter type of Dictionary that contains how many times each symbol appeared (No whitespaces).
    - "Source_Language" is the language of the original file before it was translated to all languages. Currently there are 9 different Source Languages: Arabic, Chinese, English, Japanese, Korean, Portuguese, Quechua, Russian and Spanish.
    - "Language" is the final language of the file which was converted to the IPA.

### _ipa.py_ is the code that converts all files into IPA. 
    The source and output locations have to be specified inside the code in `SOURCE_DIR` and `OUTPUT_DIR`

### _ipa_analysis.py_ is the code that produces _character_statistics.csv_ and plots some graphs.

### _translate.py_ is the code used to translate the source files to all languages.

### _HumanRights_IPA_ contains all files converted to IPA.

### _HumanRights_translated_ contains the files translated from the source languages to all available languages.
