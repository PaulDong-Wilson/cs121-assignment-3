import inverted_indexing
import ranker
import file_system


def run_indexer() -> None:
    # Get the url and text map for each document in the collection (one at a time)
    for next_url, next_text_map in inverted_indexing.indexing():
        # Get the token frequencies for all works in the text map
        token_frequencies = ranker.rank_document(next_text_map)

        # Loop through the tokens and their frequencies, and index them under the current document URL
        for next_token, next_frequency in token_frequencies.items():
            file_system.addPage_index_file(next_token, next_url, next_frequency)


if __name__ == "__main__":
    # Run the indexer and report the total amount of documents indexed, and the amount of unique words seen
    run_indexer()

    print(f"Number of indexed documents: {inverted_indexing.indexed_docs_count}" +
          f"\nNumber of unique words: {len(ranker.seen_words)}")
