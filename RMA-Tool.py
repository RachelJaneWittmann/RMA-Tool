import xml.etree.ElementTree as ET
import csv
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

def parse_xml_to_csv(xml_file, csv_file):
    """
    Parses an XML file containing specific metadata and writes the extracted data into a CSV file.

    Parameters:
    - xml_file (str): File path of the XML input file.
    - csv_file (str): File path of the CSV output file.

    Note:
    - Make sure the XML file follows a specific structure with predefined namespaces.
    - Ensure that the CSV file path points to a writable location.
    """

    # Define namespaces
    namespaces = {
        'oai': 'http://www.openarchives.org/OAI/2.0/',
        'qdc': 'http://worldcat.org/xmlschemas/qdc-1.0/',
        'dcterms': 'http://purl.org/dc/terms/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }
    
    # Load stopwords and punctuation
    stop_words = set(stopwords.words('english'))
    punctuation = set(string.punctuation)
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Open CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write headers
        writer.writerow(['Identifier', 'Title', 'Subject', 'IdentifierURL', 'Token'])
        
        # Extract data from XML and write to CSV
        for record in root.findall('.//oai:record', namespaces):
            identifier = record.find('./oai:metadata/qdc:qualifieddc/dc:identifier', namespaces).text if record.find('./oai:metadata/qdc:qualifieddc/dc:identifier', namespaces) is not None else ""
            title = record.find('./oai:metadata/qdc:qualifieddc/dc:title', namespaces).text if record.find('./oai:metadata/qdc:qualifieddc/dc:title', namespaces) is not None else ""
            subject = record.find('./oai:metadata/qdc:qualifieddc/dc:subject', namespaces).text if record.find('./oai:metadata/qdc:qualifieddc/dc:subject', namespaces) is not None else ""
            identifier_url = record.find('./oai:metadata/qdc:qualifieddc/dc:identifier', namespaces).text if record.find('./oai:metadata/qdc:qualifieddc/dc:identifier', namespaces) is not None else ""
            
            # Tokenize and preprocess title and subject
            title_tokens = [word for word in word_tokenize(title.lower()) if word not in stop_words and word not in punctuation and not word.isdigit() and word != '--'] if title else []
            subject_tokens = [word for word in word_tokenize(subject.lower()) if word not in stop_words and word not in punctuation and not word.isdigit() and word != '--'] if subject else []
            
            # Write each token as a separate row with other columns filled down
            for token in title_tokens:
                writer.writerow([identifier, title, subject, identifier_url, token])
                
            for token in subject_tokens:
                writer.writerow([identifier, title, subject, identifier_url, token])

# Define file paths
xml_file_path = "PATH_TO_XML_FILE"  # Insert path to your XML file
csv_file_path = "PATH_TO_CSV_FILE"  # Insert path to desired CSV output file

# Parse XML and write to CSV
parse_xml_to_csv(xml_file_path, csv_file_path)

print("Conversion from XML to CSV successfully completed.")

def load_lexicon_from_csv(file_path):
    """
    Loads lexicon categories and terms from a CSV file into a dictionary.

    Parameters:
    - file_path (str): File path of the CSV input file.

    Returns:
    - lexicon (dict): Dictionary containing lexicon categories as keys and lists of terms as values.

    Note:
    - The CSV file should have lexicon categories as column headers and terms listed under each category.
    """

    lexicon = {
        "Aggrandizement": [],
        "RaceEuphemisms": [],
        "RaceTerms": [],
        "SlaveryTerms": [],
        "GenderTerms": [],
        "LGBTQ": [],
        "MentalIllness": [],
        "Disability": []
    }
    
    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row
        
        for row in csv_reader:
            if len(row) == 8:
                lexicon["Aggrandizement"].append(row[0])
                lexicon["RaceEuphemisms"].append(row[1])
                lexicon["RaceTerms"].append(row[2])
                lexicon["SlaveryTerms"].append(row[3])
                lexicon["GenderTerms"].append(row[4])
                lexicon["LGBTQ"].append(row[5])
                lexicon["MentalIllness"].append(row[6])
                lexicon["Disability"].append(row[7])
            else:
                print("Invalid row format. Skipping...")
    
    return lexicon

def search_and_append_lexicon_category(lexicon, input_csv_file, output_csv_file):
    """
    Searches for lexicon term matches in an input CSV file, appends lexicon categories to each row, and writes the modified data into an output CSV file.

    Parameters:
    - lexicon (dict): Dictionary containing lexicon categories as keys and lists of terms as values.
    - input_csv_file (str): File path of the input CSV file.
    - output_csv_file (str): File path of the output CSV file.

    Note:
    - The input CSV file should contain a 'Token' column where lexicon term matches will be searched.
    - The output CSV file will have an additional column 'LexiconCategory' appended to each row, indicating the matched lexicon categories.
    """

    # Load lexicon
    lexicon = load_lexicon_from_csv(lexicon)

    # Open input CSV file for reading and output CSV file for writing
    with open(input_csv_file, 'r', newline='', encoding='utf-8') as input_csv, \
         open(output_csv_file, 'w', newline='', encoding='utf-8') as output_csv:
        
        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)
        
        # Write headers to the output CSV file
        headers = next(reader)
        headers.append('LexiconCategory')
        writer.writerow(headers)
        
        # Iterate over rows in the input CSV file
        for row in reader:
            token = row[4]  # Assuming token is in the 5th column
            # Search for matches between token and terms in the lexicon
            matching_categories = [category for category, terms in lexicon.items() if token in terms]
            # Append lexicon category to the row
            row.append(', '.join(matching_categories))
            # Write the modified row to the output CSV file
            writer.writerow(row)

    # Open the output CSV file again to remove rows without a LexiconCategory
    with open(output_csv_file, 'r', newline='', encoding='utf-8') as output_csv:
        reader = csv.reader(output_csv)
        # Filter rows based on presence of LexiconCategory
        rows_to_keep = [row for row in reader if row[-1] != '']  # Assuming LexiconCategory is the last column
        # Write filtered rows back to the output CSV file
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as updated_output_csv:
            writer = csv.writer(updated_output_csv)
            writer.writerows(rows_to_keep)

# File paths
lexicon_file_path = "PATH_TO_LEXICON_CSV_FILE"  # Insert path to your lexicon CSV file
input_csv_file_path = "PATH_TO_INPUT_CSV_FILE"  # Insert path to your input CSV file
output_csv_file_path = "PATH_TO_OUTPUT_CSV_FILE"  # Insert path to desired output CSV file

# Search for matches, append lexicon category, and remove rows without a LexiconCategory
search_and_append_lexicon_category(lexicon_file_path, input_csv_file_path, output_csv_file_path)

print("Reparative Metadata Audit successfully completed.")
