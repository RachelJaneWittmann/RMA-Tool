# Reparative Metadata Audit Tool

## Background

## Credits and Acknowledgments
This tool was inspired by the Duke University Libraries Description Audit Tool, developed by [Noah Huffman](https://github.com/noahgh221) at the Rubenstein Library, and expanded by [Miriam Shams-Rainey](https://github.com/mshamsrainey). See: [Description-Audit](https://github.com/duke-libraries/description-audit/tree/main). 

Code developed by [Kaylee Alexander](https://github.com/kayleealexander) in collaboration with ChatGPT 3.5, [Rachel Wittmann](https://github.com/RachelJaneWittmann), and [Anna Neatrour](https://github.com/aneatrour) at the University of Utah's J. Willard Marriot Library.

## About the Tool
This Python tool is designed to parse XML files containing Open Archives Initiative (OAI) feed metadata for library special collections, extract the data, tokenize and preprocess it, and then write the extracted data into a CSV file. Then, it matches the tokens against a lexicon and appends corresponding lexicon categories (Aggrandizement, Race Euphemisms, Race Terms, Slavery Terms, Gender Terms, LGBTQ, Mental Illness, and Disability) to each row in the CSV output. It is intended to facilitate reparative metadata practices. 

### Dependencies 
1. **Python 3.x**: The programming language used to write the code.
2. **NLTK (Natural Language Toolkit)**: Library for natural language processing, used for tokenization and stopword removal.
3. **Tkinter**: Standard GUI toolkit for Python, used for creating the graphical user interface.
4. **xml.etree.ElementTree**: Part of Python's standard library, used for parsing XML files.
5. **csv**: Part of Python's standard library, used for reading and writing CSV files.
6. **string**: Part of Python's standard library, used for string operations.
7. **os**: Part of Python's standard library, used for removing temporary files.

### The Lexicon

### Sample Data

### Using the GUI
