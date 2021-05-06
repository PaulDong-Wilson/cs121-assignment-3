import inverted_indexing
import ranker
import file_system
import re
import os


def sieve(postings: [(str, str, int)]):
    # To hold the different batches to send to the file system
    batch1 = [[], [], []]
    batch2 = [[], [], []]
    batch3 = [[], [], []]
    batch4 = [[], [], []]
    batch5 = [[], [], []]

    # Loop through the tokens, urls, and frequencies in the postings
    for next_token, next_url, next_frequency in postings:
        # Sieve the next posting into the correct batch, according to its starting character
        if len(next_token) == 0:
            print(f"BAD POSTING: token({next_token}), url({next_url}), frequency({next_frequency})")
        if re.match(r"[0-9]", next_token[0]) is not None:
            batch1[0].append(next_token)
            batch1[1].append(next_url)
            batch1[2].append(next_frequency)
        elif re.match(r"[a-f]", next_token[0]) is not None:
            batch2[0].append(next_token)
            batch2[1].append(next_url)
            batch2[2].append(next_frequency)
        elif re.match(r"[g-m]", next_token[0]) is not None:
            batch3[0].append(next_token)
            batch3[1].append(next_url)
            batch3[2].append(next_frequency)
        elif re.match(r"[n-s]", next_token[0]) is not None:
            batch4[0].append(next_token)
            batch4[1].append(next_url)
            batch4[2].append(next_frequency)
        elif re.match(r"[t-z]", next_token[0]) is not None:
            batch5[0].append(next_token)
            batch5[1].append(next_url)
            batch5[2].append(next_frequency)
        else:
            print(f"BAD POSTING: token({next_token}), url({next_url}), frequency({next_frequency})")

    # Return the batches as a combined 5-tuple
    return batch1, batch2, batch3, batch4, batch5


def run_indexer() -> None:
    # To hold the postings to sieve into the next batches to send to the file system
    postings = []

    # Used for determining when to send the next batches to the file system
    docs_since_last_indexing = 0

    # Get the url and text map for each document in the collection (one at a time)
    for next_url, next_text_map in inverted_indexing.indexing():
        # Assign an id to the next url (based on how many documents have been downloaded already), and save the
        # id and url association to the document_ids file
        with open("document_ids.txt", "a") as document_id_stream:
            print(f"{inverted_indexing.indexed_docs_count}; {next_url}", file=document_id_stream)

        # Get the token frequencies for all works in the text map
        token_frequencies = ranker.rank_document(next_text_map)

        # Add the postings for the ranked tokens to the postings list
        for next_token, next_frequency in token_frequencies.items():
            postings.append((next_token, str(inverted_indexing.indexed_docs_count), next_frequency))

        # If 10000 documents have been processed since the last set of batches were sent to the file system--
        if docs_since_last_indexing >= 10000:
            # Sieve the current list of postings into the five different term-range batches
            batches = sieve(postings)

            # Separate the batches and send them to the file system individually
            for tokens, urls, frequencies in batches:
                file_system.addPage_index_file(tokens, urls, frequencies)

            # Reset the postings list and amount of documents since the last
            postings.clear()
            docs_since_last_indexing = 0

        # Otherwise, increment the amount of documents processed since the last set of batches were sent out
        else:
            docs_since_last_indexing += 1

        print(f"Current number of indexed documents: {inverted_indexing.indexed_docs_count}")

    # If there are still more postings to send to the file system, send the remaining postings in a last set of batches
    if len(postings) > 0:
        batches = sieve(postings)
        for tokens, urls, frequencies in batches:
            file_system.addPage_index_file(tokens, urls, frequencies)


if __name__ == "__main__":
    # Run the indexer and report the total amount of documents indexed, and the amount of unique words seen
    run_indexer()

    # Calculate the size of the resulting index on disk (in KBs)
    # File size calculation setup adapted from https://amiradata.com/python-get-file-size-in-kb-mb-or-gb/
    files = ["index_0-9.txt", "index_a-f.txt", "index_g-m.txt", "index_n-s.txt", "index_t-z.txt", "document_ids.txt"]
    file_system_size = round(sum(os.path.getsize(next_file) for next_file in files) / 1024, 3)

    # Printout the indexer report
    print(f"\nNumber of indexed documents: {inverted_indexing.indexed_docs_count}" +
          f"\nNumber of unique words: {len(ranker.seen_words)}"
          f"\nSize of index on disk: {file_system_size} KB")


