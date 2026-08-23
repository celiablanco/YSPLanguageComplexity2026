# Character-Complexity
Calculate and compare complexity of Unicode characters in multiple texts in multiple languages

Texts for analysis should be in UTF-8 .txt format, in one folder

Extract_text_from_pdf.ipynb can be used to convert PDF files to text files, examples in Test-Files
Some PDF files are images and require different processing to be converted: so far Hindi and Hebrew gave unresolved issues

Code:
            
Run once: 
Build_Unicode_Database.ipynb
builds database of Unicode characters
output: unicode_character_database.pkl

then run once:
Assign_fonts.ipynb
builds database of Noto fonts assigned to Unicode character database
can be updated to use other fonts but Noto is currently default for entire pipeline
input: unicode_character_database.pkl
output: noto_font_table.pkl and unicode_to_notofonts_map.pkl

then run to update as needed: Glyph_Complexity_Calc.ipynb
Specify fonts and calculate the complexity of every character in that font. Output: glyph_complexity_database.pkl

then run Text_Complexity_Calc.ipynb
input: folder of text files for analysis, glyph_complexity_database.pkl, noto_font_table.pkl and unicode_to_notofonts_map.pkl
Calculates complexity of entire set of uploaded texts
UDHR translations used for testing in folder Test-Files
