import re, os, json
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from collections import defaultdict
from urllib.parse import urldefrag

indexed_docs_count = 0                      # Total number of documents


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

                # Parse out the document url and remove its fragment (if any)
                url = urldefrag(json_content['url'])[0]

                # Parse out the document content and parse its HTML
                soup = BeautifulSoup(json_content['content'], 'lxml')

                # Tokenizing and stemming using Porter Stemmer
                ps = PorterStemmer()

                # Loop through the different important HTML tags for text
                for next_tag in HTML_tags:
                    # Find all content under the next tag
                    for next_tag_content in soup.find_all(next_tag):
                        # Get the text from this tag's content
                        next_tag_text = next_tag_content.get_text()

                        # Split the text into alphanumeric sequences, stem them, and add them to the text map under
                        # the current tag
                        for next_token in re.split('[^a-zA-Z0-9]', next_tag_text):
                            token_stem = ps.stem(next_token.lower())
                            if token_stem.isalnum() and len(token_stem) > 2: #sequence character and len >=3
                                text_map[next_tag].append(token_stem)

            # Increment the number of indexed documents, then yield its url and text map
            indexed_docs_count += 1
            yield url, text_map

      
if __name__ == "__main__":
    for next_url, next_text_map in indexing():
        # print(f"({repr(next_url)}, {next_text_map})")
        pass

    # Print number of indexed document
    print("\nNumber of indexed document:", indexed_docs_count)

   

