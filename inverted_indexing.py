import re, os, json
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from collections import defaultdict
from urllib.parse import urldefrag

indexed_docs_count = 0                      # Total number of documents


def tokenize(text: str) -> str:
    # Stemming using Porter Stemmer
    ps = PorterStemmer()

    # Process the tokens and add them under the current tag
    for next_token in re.split(r"[\s\-–]", text):
        next_token = next_token.lower()  # Set tokens to lower case
        next_token = re.sub(r"[.,?:!;()\[\]{}\"']", "", next_token)  # Remove special characters
        token_stem = ps.stem(next_token)  # Stem the tokens

        # If, after processing, the next token is not empty, and only contains alphanumeric
        # characters, yield the current yoken
        if re.match(r"^[a-z0-9]+$", next_token) is not None:
            yield token_stem


def indexing():
    # So that the total number of indexed documents can be changed
    global indexed_docs_count

    ## list of HTML tags for important text:
    HTML_tags = ['b', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title', 'p']     # <b>:  Defines bold text
                                                                                      # <strong>: Defines important text
                                                                                      # <h1> to <h6>: Defines HTML headings
                                                                                      # <title>: Defines a title for the document
                                                                                      # <p>: Defines standard paragraph text

    # Get the path for the collection
    collection_path = os.path.join(os.getcwd() + f"{os.path.sep}DEV")

    # Loop through the sub-folders of the collection
    for folder, subfolders, files in os.walk(collection_path):
        # Loop through the files in the next sub-folder
        for each_file in files:
            # To hold the text associations and the document's url
            text_map = defaultdict(list)
            url = ""

            # Get the path to the file
            file_path = os.path.join(folder, each_file)

            # Open JSON file
            with open(file_path, 'r', encoding = "utf8") as json_file: #encode in utf8
                json_content = json.load(json_file) # takes a file object json_file and returns the json object

                # Get the encoding for the current document content
                encoding = json_content["encoding"].strip().lower()

                # If the encoding is not a known English/Latin encoding, skip the document
                if encoding not in {"utf-8", "ascii", "iso-8859-1", "windows-1252", "utf-16", "utf-8-sig"}:
                    continue

                # Parse out the document url and remove its fragment (if any)
                url = urldefrag(json_content['url'])[0]

                # Parse out the document content and parse its HTML
                soup = BeautifulSoup(json_content['content'], 'lxml')

                # Loop through the different important HTML tags for text
                for next_tag in HTML_tags:
                    # Find all content under the next tag
                    for next_tag_content in soup.find_all(next_tag):
                        # Get the text from this tag's content
                        next_tag_text = next_tag_content.get_text()

                        # Process the tokens and add them under the current tag
                        for next_token in tokenize(next_tag_text):
                            text_map[next_tag].append(next_token)

            # Increment the number of indexed documents, then yield its url and text map
            indexed_docs_count += 1
            yield url, text_map

      
if __name__ == "__main__":
    for next_url, next_text_map in indexing():
        # print(f"({repr(next_url)}, {next_text_map})")
        pass

    # Print number of indexed document
    print("\nNumber of indexed document:", indexed_docs_count)

   

