from collections import defaultdict
import math

seen_words = set()


def rank_document(text_map: {str: [str]}) -> {str: int}:
    # To hold the frequencies of all tokens in the given text map
    token_frequencies = defaultdict(int)

    # Loop through the token lists in the text map (ignoring the tags for now)
    for next_token_list in text_map.values():
        # Loop through the next token list
        for next_token in next_token_list:
            # Increment the current token's frequency
            token_frequencies[next_token] += 1

            # Save that the current token has been seen (if unique)
            seen_words.add(next_token)

    return token_frequencies


def calculate_tf_idf_weight(term_frequency: int, document_frequency: int, collection_size: int,) -> float:
    """ TODO for later
    Calculates the tf-idf weight for a query term for a particular document.

    :param term_frequency: The amount of times the term appears in the specified document.
    :param document_frequency: The amount of documents that the query term appears in overall.
    :param collection_size: The amount of documents in the collection overall.
    :return: The tf-idf weight for the query term.
    """

    inverse_document_frequency = math.log(collection_size / document_frequency, 10)

    return term_frequency * inverse_document_frequency

