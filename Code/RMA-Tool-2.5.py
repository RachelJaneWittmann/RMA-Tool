import pandas as pd
import re

class ReparativeMetadataAuditToolCLI:
    """A tool for auditing metadata and identifying matches based on a provided lexicon."""

    def __init__(self):
        """Initialize the audit tool."""
        self.lexicon_df = None
        self.metadata_df = None
        self.columns = []  # List of all available columns in the metadata
        self.categories = []  # List of all available categories in the lexicon
        self.selected_columns = []  # List of columns selected for matching
        self.identifier_column = None  # Identifier column used to uniquely identify rows

    def load_lexicon(self, file_path):
        """Load the lexicon file.

        Parameters:
        file_path (str): Path to the lexicon CSV file. (Input your own file path here)

        """
        try:
            self.lexicon_df = pd.read_csv(file_path, encoding='latin1')
            print("Lexicon loaded successfully.")
        except Exception as e:
            print(f"An error occurred while loading lexicon: {e}")

    def load_metadata(self, file_path):
        """Load the metadata file.

        Parameters:
        file_path (str): Path to the metadata CSV file. (Input your own file path here)

        """
        try:
            self.metadata_df = pd.read_csv(file_path, encoding='latin1')
            print("Metadata loaded successfully.")
        except Exception as e:
            print(f"An error occurred while loading metadata: {e}")

    def select_columns(self, columns):
        """Select columns from the metadata for matching.

        Parameters:
        columns (list of str): List of column names. (Input your own column names here)

        """
        self.selected_columns = columns

    def select_identifier_column(self, column):
        """Select the identifier column used for uniquely identifying rows.

        Parameters:
        column (str): Name of the identifier column. (Input your own identifier column here)

        """
        self.identifier_column = column

    def select_categories(self, categories):
        """Select categories from the lexicon for matching.

        Parameters:
        categories (list of str): List of category names. (Input your own category names here)

        """
        self.categories = categories

    def perform_matching(self):
        """Perform matching between selected columns and categories."""
        if self.lexicon_df is None or self.metadata_df is None:
            print("Please load lexicon and metadata files first.")
            return

        matches = self.find_matches(self.selected_columns, self.categories)
        matches_df = pd.DataFrame(matches, columns=['Identifier', 'Term', 'Category', 'Column'])
        print(matches_df)

    def find_matches(self, selected_columns, selected_categories):
        """Find matches between metadata and lexicon based on selected columns and categories.

        Parameters:
        selected_columns (list of str): List of column names from metadata for matching.
        selected_categories (list of str): List of categories from the lexicon for matching.

        Returns:
        list of tuple: List of tuples containing matched results (Identifier, Term, Category, Column).

        """
        matches = []
        lexicon_df = self.lexicon_df[self.lexicon_df['category'].isin(selected_categories)]
        for index, row in self.metadata_df.iterrows():
            for col in selected_columns:
                if isinstance(row[col], str):
                    for term, category in zip(lexicon_df['term'], lexicon_df['category']):
                        if re.search(r'\b' + re.escape(term.lower()) + r'\b', row[col].lower()):
                            matches.append((row[self.identifier_column], term, category, col))
                            break
        return matches

# Example usage:
print("1. Initialize the tool:")
tool = ReparativeMetadataAuditToolCLI()

print("\n2. Load lexicon and metadata files:")
tool.load_lexicon("lexicon.csv")  # Input your own file path here
tool.load_metadata("metadata.csv")  # Input your own file path here

print("\n3. Select columns for matching:")
tool.select_columns(["column1", "column2"])  # Input your own column names here

print("\n4. Select the identifier column:")
tool.select_identifier_column("ID")  # Input your own identifier column here

print("\n5. Select categories for matching:")
tool.select_categories(["Category1", "Category2"])  # Input your own category names here

print("\n6. Perform matching and view results:")
tool.perform_matching()