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
        for token in dict:
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

# returns list of pages associated with given token
# return value = ["token, doc_count", "doc_id1, term_freq1", "doc_id2, term_freq2", ...]
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
        # line anatomy:
        # key, doc_count; doc_id, term_frequency; doc_id, term_frequency
        list = line.split("; ")
        if list[0].split(", ")[0] == token:
            file.close()
            return list
    file.close()
    return False

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
