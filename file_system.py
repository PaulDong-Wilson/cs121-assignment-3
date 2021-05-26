import ranker

# File structure
#       -- each line is a token entry
# key, doc_count; doc_id, term_frequency; doc_id, term_frequency
def addPage_index_file(keys, urls, freqs):
    filename = ""

    # finds what file the key would be in
    x = keys[0][0].lower()
    if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9':
        filename = "index_0-9.txt"
    elif x == 'a' or x == 'b' or x == 'c' or x == 'd' or x == 'e' or x == 'f':
        filename = "index_a-f.txt"
    elif x == 'g' or x == 'h' or x == 'i' or x == 'j' or x == 'k' or x == 'l' or x == 'm':
        filename = "index_g-m.txt"
    elif x == 'n' or x == 'o' or x == 'p' or x == 'q' or x == 'r' or x == 's':
        filename = "index_n-s.txt"
    else:
        filename = "index_t-z.txt"
    file = ""
    # load in file into dic
    dic = {}
    docFreqs = {}
    try :
        file = open(filename, "r")
        for line in file:
            line = line[:-1]  # strips newline from end of line
            list = line.split("; ")
            t = list[0].split(", ")
            docFreqs.update({t[0]: t[1]})
            dic.update({t[0]: list[1:]})
    # if file doesn't exist create it
    except IOError:
        file = open(filename, "w")
        file.close()

    # populate dic with given arrays
    for key, url, freq in zip(keys, urls, freqs):
        postings = dic.get(key, 500)
        if postings == 500:
            arr = []
            arr.append(str(url+", "+str(freq)))
            docFreqs.update({key: 1})
            dic.update({key: arr})
        else:
            df = int(docFreqs.get(key)) + 1
            docFreqs.update({key: df})
            postings.append(str(url+", "+str(freq)))
            dic.update({key: postings})

    # write dic to file
    file = open(filename, "w")
    for token, postings in dic.items():
        # sort postings
        postingDict = {}
        for posting in postings:
            p = posting.split(", ")
            postingDict.update({p[0]: int(p[1])})

        sortedPostings = []
        for k in sorted(postingDict, key=lambda x: (int(x))):
            sortedPostings.append(k + ", " + str(postingDict[k]))

        postings = ""
        try:
            postings = "; ".join(sortedPostings)
        except TypeError:
            pass
        file.write(token+", "+str(docFreqs.get(token))+"; "+postings+"\n")
    file.close()

# updates whole index to include tf-idf for each docID, tf pair
# key, df; docID, tf, tf-idf; ...
def add_tf_idf():
    files = ["index_0-9.txt","index_a-f.txt","index_g-m.txt","index_n-s.txt","index_t-z.txt"]
    collection_size = get_index_total()
    for file in files:
        # load in file into dict
        dict = {}
        docFreqs = {}
        index = open(file, "r")

        # reads index file line by line
        for line in index:
            line = line[:-1]  # strips newline from end of line
            list = line.split("; ")
            term_info = list[0].split(", ")
            t, df = term_info[0], int(term_info[1])
            postings = list[1:]
            new_postings = []

            # adds tf-idf to posting pair
            for posting in postings:
                arr = posting.split(", ")
                docId = arr[0]
                tf = int(arr[1])
                tf_idf = ranker.calculate_tf_idf_weight(tf, df, collection_size)
                new_postings.append(docId+", "+str(tf)+", "+str(round(tf_idf, 3)))

            docFreqs.update({t: df})
            dict.update({t: new_postings})
        index.close()
        index = open(file, "w")

        # updates index file
        for token in sorted(dict):
            postings = ""
            try:
                postings = "; ".join(dict.get(token))
            except TypeError:
                postings
            index.write(token + ", " + str(docFreqs.get(token)) + "; " + postings + "\n")
        index.close()


# returns the total number of pages indexed
def make_index_info():
    try:
        totalPageNum = 0;
        file = open("document_ids.txt", "r")
        for entry in file:
            list = entry.split("; ")
            if len(list) > 1:
                totalPageNum = totalPageNum + 1
        file.close()
        file = open("index_info.txt", "w")
        file.write(str(totalPageNum))
        file.close()
        return True
    except IOError:
        return False

# returns the total number of pages indexed
def get_index_total():
    try:
        indexInfo = open("index_info.txt", "r")
        totalPageNum = indexInfo.readline().rstrip()
        return int(totalPageNum)
    except IOError:
        return 0

def get_pages(token):
    # finds what file the key would be in
    x = token[0].lower()
    if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9':
        filename = "index_0-9.txt"
    elif x == 'a' or x == 'b' or x == 'c' or x == 'd' or x == 'e' or x == 'f':
        filename = "index_a-f.txt"
    elif x == 'g' or x == 'h' or x == 'i' or x == 'j' or x == 'k' or x == 'l' or x == 'm':
        filename = "index_g-m.txt"
    elif x == 'n' or x == 'o' or x == 'p' or x == 'q' or x == 'r' or x == 's':
        filename = "index_n-s.txt"
    else:
        filename = "index_t-z.txt"
    file = open(filename, "r")
    # searches file to find line with matching key
    for line in file:
        line = line[:-1]
        list = line.split("; ")
        if list[0].split(", ")[0] == token:
            file.close()
            return list
    file.close()
    return False

def is_not_in_index(query_token: str, index_token: str):
    sortedStrings = sorted([query_token, index_token])
    # if query_token is not in the index, then sortedStrings == [query_token, index_token]
    if sortedStrings[0] == query_token:
        return True
    else:
        return False

def get_pages_for_tokens(tokens: [str], filename: str):
    """
            Calculates the cosine similarity this DocumentVector has with the specified query_vector.
            The length of the query_vector must be equal to the length of this DocumentVector's vector.

            :param tokens: List of tokens that are all in the same file.
            :param filename: Name of file to read from.
            :return: List of entries from the inverted index.
                format: [ ["token, df", "docId, tf, tf-idf", ...], ...]
    """
    # make sure list is in alphabetical order
    sortedTokens = sorted(tokens)
    count = 0
    file = open(filename, "r")
    returnList = []
    # searches file to find line with matching key
    for line in file:
        line = line[:-1]
        list = line.split("; ")
        index_token = list[0].split(", ")[0]

        # checks if sortedTokens[count] exists in the list by comparing it to token
        while is_not_in_index(sortedTokens[count], index_token):
            count = count+1
            if count == len(sortedTokens):
                file.close()
                return returnList

        if index_token == sortedTokens[count]:
            count = count+1
            returnList.append(list)
            if count == len(sortedTokens):
                file.close()
                return returnList
    file.close()
    return returnList

# combines all index files into 1 file called "index_combined.txt"
def combine_index_files():
    filenames = ["index_0-9.txt", "index_a-f.txt", "index_g-m.txt", "index_n-s.txt", "index_t-z.txt"]
    with open("index_combined.txt", "w") as outfile:
        for filename in filenames:
            with open(filename, "r") as infile:
                for line in infile:
                    outfile.write(line)


# Builds the positional index to facilitate file seeking
def build_positional_index():
    # To hold the positional ranges for each word start
    positional_index = {}

    location = 0
    previous_word_start = ""

    # The index file to generate a positional index for
    index_file = "index_combined.txt"

    # Open the index file and get the word starts within it
    with open(index_file, "r") as file_stream:

        # Loop through the lines in the file
        for next_line in file_stream:
            # Get all characters from the current line up to (but not including) the first comma
            # Strip the remaining characters
            clean_line = next_line[0:next_line.find(",")].rstrip()

            # If the line is empty, simply continue to the next one
            if len(clean_line) == 0:
                continue

            # To hold the next word start
            next_word_start = ""

            # If the line only has one character, set it as the word start for this line
            if len(clean_line) == 1:
                next_word_start = clean_line

            # If the first character of this word matches the second character, simply set the first character
            # as the word start
            elif clean_line[0] == clean_line[1]:
                next_word_start = clean_line[0]

            # Otherwise, use the first two characters as the start of this word
            else:
                next_word_start = clean_line[0:2]

            # If the current word start has not been seen yet
            if next_word_start not in positional_index:
                # If this word start is the first word start
                if len(positional_index) == 0:

                    # simply add associate it with the current location
                    positional_index[next_word_start] = location

                # Otherwise, complete the end location for the previous word start, and enter the current location
                # for this word start
                else:
                    positional_index[previous_word_start] = (positional_index[previous_word_start], location)
                    positional_index[next_word_start] = location

                # Set the current word start as the new previous word start
                previous_word_start = next_word_start

            # Keep track of the current location
            location += len(next_line) + 1

    # Complete the end range of the last word start
    positional_index[previous_word_start] = (positional_index[previous_word_start], location)

    # Output the ranges to the file
    with open("positional_index.txt", "w") as file_stream:
        for next_start, next_range in sorted(positional_index.items(), key=lambda x: (x[0])):
            print(f"{next_start}; {repr(next_range)}", file=file_stream)


def read_positional_index() -> {str: (int, int)}:
    # To hold the positional index as it is read in
    positional_index = {}

    # Open and read in the positional index file, then return it
    with open("positional_index.txt", "r") as file_stream:
        # Loop through each of the lines in the file
        for next_line in file_stream:
            # Split the line into its separate parts
            line_parts = next_line.rstrip().split("; ")

            # If the line was empty, continue to the next line
            if len(line_parts) == 0:
                continue

            # Differentiate the line parts as the next word start and next range
            next_start, next_range = line_parts

            # Associate the next word start with its positional range
            positional_index[next_start] = eval(next_range)

    return positional_index


def seek_postings_for(terms: {str}, positional_index: {str: (int, int)}) -> {str: [str]}:
    # To hold the read postings for the given terms
    postings = {}

    # To hold the locations of each term's 1-character or 2-character word start
    locations = {}

    # Loop through the terms and determine the starting positions of their word starts
    for next_term in terms:

        if (len(next_term) == 1) and (next_term in positional_index):
            locations[next_term] = positional_index[next_term]

        elif next_term[0:2] in positional_index:
            locations[next_term] = positional_index[next_term[0:2]]

        # If the current term's word start is not in the positional index, the term is not in the index at all
        # Set its posting to None
        else:
            postings[next_term] = None

    # Open the index in BINARY mode, then seek through it looking for the term postings
    with open("index_combined.txt", "rb") as file_stream:

        # Loop through the terms and term location ranges
        for next_word, next_range in sorted(locations.items(), key=lambda x: (x[0])):
            # Differentiate the start and end point of this term's location range
            next_start, next_end = next_range

            # Seek to the new starting point from the current position
            # (it's VERY important that this seek is relative to the current position)
            file_stream.seek(next_start - file_stream.tell(), 1)

            # Loop while the current location in the file is not at the end of this term's location range
            while file_stream.tell() < next_end:
                # Clean up the line and parse out the term
                clean_line = file_stream.readline().decode('utf-8').rstrip()
                read_word = clean_line[0:clean_line.find(",")]

                # If the term is the next word to be found, split out its posting and associate it with the term,
                # and add it to the set of found terms
                if next_word == read_word:
                    postings[next_word] = clean_line.split("; ")
                    break

    # Return the postings associated with each of the given terms (or None, if no posting was in the index for the term)
    return postings


if __name__ == "__main__":
    x = get_index_total()
    print(x)

    addPage_index_file(["test", "zebra"], ["url1","url2"], [10,2])
    x = get_index_total()
    print(x)
    x = get_pages("test")
    print(x)
    x = get_pages("zebra")
    print(x)


    addPage_index_file(["test", "zebra"], ["url3","url4"], [5,6])
    x = get_index_total()
    print(x)
    x = get_pages("test")
    print(x)
    x = get_pages("zebra")
    print(x)
