from collections import defaultdict
import math

seen_words = set()


def rank_document(text_map: {str: [str]}, tag_weights: {str: int}) -> {str: int}:
    # To hold the frequencies of all tokens in the given text map
    token_frequencies = defaultdict(int)

    # Loop through the tags in the given text_map, along with their associated token list
    for next_tag, next_token_list in text_map.items():
        # Get the weight for the next tag
        next_tag_weight = 1
        if next_tag in tag_weights:
            next_tag_weight = tag_weights[next_tag]

        # Loop through the next token list
        for next_token in next_token_list:
            # Increment the current token's frequency by the weight of the current tag
            token_frequencies[next_token] += next_tag_weight

            # Save that the current token has been seen (if unique)
            seen_words.add(next_token)

    return token_frequencies


def calculate_tf_idf_weight(term_frequency: int, document_frequency: int, collection_size: int,) -> float:
    """
    Calculates the tf-idf weight for a query term for a particular document.

    :param term_frequency: The amount of times the term appears in the specified document.
    :param document_frequency: The amount of documents that the query term appears in overall.
    :param collection_size: The amount of documents in the collection overall.
    :return: The tf-idf weight for the query term.
    """

    # If any of the arguments were zero, default to returning zero
    if (term_frequency == 0) or (document_frequency == 0) or (collection_size == 0):
        return 0

    # Calculate the weighted document and term frequencies, then return their product
    weighted_document_frequency = math.log(collection_size / document_frequency, 10)
    weighted_term_frequency = 1 + math.log(term_frequency, 10)

    return weighted_term_frequency * weighted_document_frequency

