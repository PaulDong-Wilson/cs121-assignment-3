import inverted_indexing
import file_system
import math
import heapq
from collections import defaultdict


def normalize_vector(vector) -> None:
    """
    Normalizes the given vector list in place.

    :param vector: The vector to normalize
    :return: None
    """

    # Calculate the length of the given vector
    vector_length = math.sqrt(sum(value ** 2 for value in vector))

    # If that vector's length was not 0 (i.e., it was not the zero vector)
    if vector_length != 0:
        # Loop through the vector's values and divide them by the length
        for i in range(len(vector)):
            vector[i] = vector[i] / vector_length


class DocumentVector:
    """
    Stores a document's docID and its frequency vector for calculating cosine similarity with a query vector.
    """

    def __init__(self, docID: str, vector: [float] = []):
        # Store the docID and vector for this DocumentVector
        self.docID = docID
        self.vector = vector

        # Calculate the number of zeros contained in the specified vector (if any)
        self.num_zeros = sum(1 for value in self.vector if value == 0)

    def extend_vector(self, score_map: {str: float}) -> None:
        """
        Extends the dimension of this DocumentVector using the specified score_map. If this DocumentVector's
        docID is not in the score_map, the extended dimension of this vector will hold a value of 0. Otherwise,
        the tf-idf value associated with this docID in the score_map will be set as the new dimensional value.

        :param score_map: A mapping of docIDs to tf-idf scores.
        :return: None
        """

        # If this docID is in the score map, add that score to the vector list and delete this docID from the
        # score map
        if self.docID in score_map:
            self.vector.append(score_map[self.docID])
            del score_map[self.docID]

        # Otherwise, append a zero to the vector list for this DocumentVector and increment the number of zeros
        else:
            self.vector.append(0)
            self.num_zeros += 1

    def get_cosine_similarity(self, query_vector: [float]):
        """
        Calculates the cosine similarity this DocumentVector has with the specified query_vector.
        The length of the query_vector must be equal to the length of this DocumentVector's vector.

        :param query_vector: The query vector to get the cosine similarity to this DocumentVector for.
        :return: The cosine similarity score between this DocumentVector and the query vector.
        """
        # Assert that the length of the query and document vectors are the same
        assert len(query_vector) == len(self.vector),\
            f"Document.get_cosine_similarity: Length of query_vector({repr(query_vector)})" \
            f" does not equal length of self.vector({repr(self.vector)})!"

        # If they are, return the cosine similarity (the sum of the product of each corresponding value in both vectors)
        return sum((query_vector[i] * self.vector[i]) for i in range(len(query_vector)))


def ranked_search_query(search_query, number_of_documents: int = 10):
    # To hold the frequency of each query term
    query_frequencies = defaultdict(int)

    # To hold the query terms, in order
    query_vector = []

    # To hold each ranked score / docID pair for the query
    document_scores_heap = []

    # To hold the vector for each document that partially (or fully) contains the query
    document_vectors = []

    # To hold the number of terms already processed
    terms_processed = 0

    # Process each of the query terms
    for next_query_term in inverted_indexing.tokenize(search_query):
        # If this query term has not been seen before, capture its ordering and set its frequency to one
        if next_query_term not in query_frequencies:
            query_vector.append(next_query_term)
            query_frequencies[next_query_term] += 1

        # Otherwise, this query term has been seen before; increment its frequency and move to the next term
        else:
            query_frequencies[next_query_term] += 1
            terms_processed += 1
            continue

        # To hold the document IDs in the postings and their associated tf-idf scores
        next_score_map = {}

        # Get the posting for the current query term
        term_posting = file_system.get_pages(next_query_term)

        # If the token was found--
        if type(term_posting) is list:
            # Parse out the term and document frequency from the posting
            term, document_frequency = term_posting[0].split(", ")

            # Loop through the rest of the posting and parse out the document ids and the tf-idf score
            for i in range(1, len(term_posting)):
                next_document_id, next_token_frequency, next_tf_idf_score = term_posting[i].split(", ")
                next_score_map[next_document_id] = float(next_tf_idf_score)

        # Loop through the current DocumentVectors and extend their vector, given the constructed score map
        for next_document_vector in document_vectors:
            next_document_vector.extend_vector(next_score_map)

        # The remaining tf-idf scores in the score map go to DocumentVectors that have not been seen yet,
        # construct new DocumentVectors for those tf-idf scores
        for next_doc_id, next_tf_idf_score in next_score_map.items():
            new_vector = [0.0 for i in range(terms_processed)] # Assume all zeros for all previous query terms
            new_vector.append(next_tf_idf_score)
            document_vectors.append(DocumentVector(next_doc_id, new_vector))

        # Increment the number of terms processed
        terms_processed += 1

    # Replace the query terms with their frequencies, then normalize the values
    for i in range(len(query_vector)):
        query_vector[i] = query_frequencies[query_vector[i]]
    normalize_vector(query_vector)

    # Loop through the DocumentVectors for this query
    for next_document_vector in document_vectors:
        # Normalize the values in the current DocumentVector
        normalize_vector(next_document_vector.vector)

        # Get the cosine similarity score between the current DocumentVector and the query vector
        ranked_score = next_document_vector.get_cosine_similarity(query_vector)

        # Add the score / docID pair to the heap (with a negative score to create a MaxHeap)
        document_scores_heap.append((-ranked_score, next_document_vector.docID))

    # Heapify the document scores into a MaxHeap
    heapq.heapify(document_scores_heap)

    # Pop the required amount of results from the heap, then return them
    results = []

    for i in range(number_of_documents):
        try:
            results.append(heapq.heappop(document_scores_heap)[1])
        except IndexError:
            break

    return results


def boolean_search_query(search_query, number_of_documents: int = 5):
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
                next_document_id, next_token_frequency, next_tf_idf_score = results[i].split(", ")
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

