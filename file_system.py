
# File structure
#       -- each line is a token entry
# key; doc_url, term_frequency; doc_url, term_frequency
def addPage_index_file(keys, urls, freqs):
    filename = ""
    indexInfo = ""
    totalPageNum = 0

    try :
        indexInfo = open("index_info.txt", "r")
        totalPageNum = indexInfo.readline()
    except IOError:
        indexInfo = open("index_info.txt", "w")
        indexInfo.write("0")

    indexInfo.close()

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
    try :
        file = open(filename, "r")
        for line in file:
            line = line[:-1]  # strips newline from end of line
            list = line.split("; ")
            postings = list[1:]
            dic.update({list[0]: list[1:]})
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
            dic.update({key: arr})
        else:
            postings.append(str(url+", "+str(freq)))
            dic.update({key: postings})

    # write dic to file
    file = open(filename, "w")
    for token in dic:
        postings = ""
        try:
            postings = "; ".join(dic.get(token))
        except TypeError:
            postings
        file.write(token+"; "+postings+"\n")
    file.close()

    # update index_info file
    indexInfo = open("index_info.txt", "w")
    totalPageNum = int(totalPageNum) + len(keys)
    indexInfo.write(str(totalPageNum))
    indexInfo.close()



# returns the total number of pages indexed
def get_index_total():
    try:
        indexInfo = open("index_info.txt", "r")
        totalPageNum = indexInfo.readline()
        return totalPageNum
    except IOError:
        return 0

# returns list of pages associated with given token
# return value = ["dev_url1, term_freq1", "dev_url2, term_freq2", ...]
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
        # key; doc_url1, term_freq1; doc_url2, term_freq2
        list = line.split("; ")
        if list[0] == token:
            file.close()
            return list[1:]
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
