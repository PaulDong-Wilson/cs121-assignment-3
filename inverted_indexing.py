import re, os, nltk, json, requests, sys, time
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from collections import defaultdict
import ast
import math

def indexing():
    global indexed_docs_count
    global inverted_dict
    global document_id

    ## list of HTML tags for important text:
    HTML_tags = ['b', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']    #<b>:  Defines bold text
                                                                                # <strong>: Defines important text 
                                                                                # <h1> to <h6>: Defines HTML headings
                                                                                # <title>: Defines a title for the document
    ## Treverse each JSON file and tokenize
    path = os.getcwd() + '\\DEV'

    for folder, files in os.walk(path):
        for each_file in files:
            # create set to store tokenized and stemming words
            stemming_set = set()
            path = os.path.join(folder, each_file)

            # Open JSON file
            with open (path, 'r', encoding = "utf8") as json_file: #encode in utf8
                json_data = json.load(json_file)
                soup = BeautifulSoup(json_data['content'], 'lxml')
                content = soup.get_text()

                # Tokenizing and stemming using Porter Stemmer
                ps = PorterStemmer()
                for token in re.split('[^a-zA-Z0-9]', content):
                    if token.isalnum() and len(token) > 2: #sequence character and len >=3
                        # apply Porter stemmer and add to set
                        stemming_set.add(ps.stem(token.lower()))

                # Iterate through the set
                for stem in stemming_set:
                    inverted_dict[stem].append(document_id)
                indexed_docs_count += 1
                document_id += 1
      
if __name__ == "__main__":
    indexed_docs_count = 0                      # Total number of documents
    inverted_dict = defaultdict(list)        # Inverted index
    document_id = 1                     # Continuous value of document_id, starting at 1

    indexing()

    # Print number of indexed document
    print("\nNumber of indexed document:", indexed_docs_count)
    print("\nDocument ID:", document_id)
    print("inverted_dict: ", inverted_dict)

   

