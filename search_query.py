import inverted_indexing
import file_system


def find_search_query(search_query, number_of_documents: int = 5):
    # To hold the sets of document IDs from each token in the search query found in the index
    set_docs = []

    # Loop through the tokens produced by tokenizing the query
    for next_query_token in inverted_indexing.tokenize(search_query):

        # Get the postings associated with the next token in the index
        results = file_system.get_pages(next_query_token)

        # If the token was found--
        if type(results) is list:

            # Parse out the token and document frequency from the posting
            token, document_frequency = results[0].split(", ")

            # To hold the document IDs in the posting
            next_document_id_set = set()

            # Loop through the rest of the posting and parse out the document ids and token frequencies
            for i in range(1, len(results)):
                next_document_id, next_token_frequency = results[i].split(", ")
                next_document_id_set.add(next_document_id)

            # Add the document ID set for this token to the list of all sets
            set_docs.append(next_document_id_set)

        # Otherwise, the token is not in the index; thus, we know no links contain the query for AND Binary Searching
        # Simply return an empty list
        else:
            return []

    # Intersect all document IDs lists (thus, producing only IDs common to all of the sets)
    final_set = set.intersection(*set_docs)

    # To hold the list of document IDs that contained ALL query tokens
    document_list = []

    # Read in the specified number of document IDs into the list, then return it
    final_set_iterator = iter(final_set)
    for i in range(number_of_documents):
        try:
            document_list.append(next(final_set_iterator))
        except StopIteration:
            break

    return document_list


"""
def get_top_num_ids(final_dict, number):
    sort_dict = sorted(final_dict.items(), key=operator.itemgetter(1), reverse=True)[:number]
    final_final_dict = [int(k) for k in dict(sort_dict).keys()]
    return final_final_dict
"""


if __name__ == "__main__":
    #word_dict = ast.literal_eval("{'emphysema': {'1725': 2, '3027': 2, '25223': 1, '32922': 1, '49911': 3}}")
    #print(type(word_dict))
    #token, postings_dict = list(word_dict.items())[0]
    #print(list(word_dict.items())[0])
    a = find_search_query("emphysema")
    #b = get_top_num_ids(a, 2)
    #print(b)

