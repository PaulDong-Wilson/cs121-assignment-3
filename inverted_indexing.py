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
    HTML_tags = ['b', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']     #<b>:  Defines bold text
                                                                                            # <strong>: Defines important text 
                                                                                            # <h1> to <h6>: Defines HTML headings
                                                                                            # <title>: Defines a title for the document
    ## Treverse each JSON file and tokenize
    saving_path = os.path.join(os.getcwd(), "paths.txt")

    path = os.getcwd() + '\\DEV'

    for folder, subfolders, files in os.walk(path):
        for each_file in files:
            # create set for holding important text for different tags
            important_text = set()
            # create set for stemmers
            stemming_set = defaultdict(int)
            path = os.path.join(folder, each_file)

            # Open JSON file
            with open (path, 'r', encoding = "utf8") as json_file: #encode in utf8
                json_content = json.load(json_file) # takes a file object json_file and returns the json object
                url = json_content['url']

                soup = BeautifulSoup(json_content['content'], 'lxml')
                content = soup.get_text()

                # Tokenizing and stemming using Porter Stemmer
                ps = PorterStemmer()
                words_collection = [] #all the words

                for token in re.split('[^a-zA-Z0-9]', content):
                    if token.isalnum() and len(token) > 2: #sequence character and len >=3
                        # add token to list words_collection
                        words_collection.append(token)
                        # apply Porter stemmer for this token
                        token_stem = ps.stem(token.lower())
                        # add token_stem to stemming set
                        stemming_set[token_stem] += 1

                # add important text from list HTML tags
                for i in soup.find_all(HTML_tags):
                    line = i.get_text()
                    #split each line ang get token
                    for token_tag in re.split('[^a-zA-Z0-9]', line):
                        if token_tag.isalnum() and len(token_tag) > 2: #sequence character and len >=3
                            # apply Porter stemmer for this token_tag
                            token_tag_stem = ps.stem(token_tag.lower())
                            # add token_tag_stem to important_text set
                            important_text.add(token_tag_stem)
                
                # write key, url, path to file
                with open(saving_path, 'a+', encoding="utf8") as f: # read and adding
                    writing_file = f"{{'{document_id}': [{repr(url)}, {repr(path)}]}}"
                    f.write(writing_file + "\n")

                # Iterate through the set
                #for stem in stemming_set:
                    #inverted_dict[stem].append(document_id)
                indexed_docs_count += 1
                document_id += 1
    print("\n important text: ", important_text)
      
if __name__ == "__main__":
    indexed_docs_count = 0                      # Total number of documents
    #inverted_dict = defaultdict(list)        # Inverted index
    document_id = 1                     # Continuous value of document_id, starting at 1

    indexing()

    # Print number of indexed document
    print("\nNumber of indexed document:", indexed_docs_count)
    #print("\nimportant text:", document_id)
    #print("inverted_dict: ", inverted_dict)

   

