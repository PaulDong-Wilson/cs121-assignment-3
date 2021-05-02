
# File structure
#       -- each line is a token entry
# key; number_of_pages; doc_url, term_frequency; doc_url, term_frequency
# key, [doc_url, term_frequency]
# key, [doc_url, term_frequency]
def addPage_index_file(key, url, freq):
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
    x = key[0].lower()
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
    try :
        file = open(filename, "r")
        output = ""
        exists = False
        # searches file to find line with matching key
        for line in file:
            line = line[:-1] # strips newline from end of line
            # line anatomy:
            # key; numberOfPages; doc_url1, term_freq1; doc_url2, term_freq2
            list = line.split("; ")
            if list[0] == key:
                exists = True
                numberOfPages = list[1]
                pages = list[2:]

                #output += key + "; " + list[1]+1
                #for page in pages:
                #    output += "; " + page
                output += key + "; " + str(int(numberOfPages)+1) + "; "
                for page in pages:
                    output += page + "; "
                output += url + ", " + str(freq) + "\n"
            else:
                output += line + "\n"
        file.close()
        # key does not exist in file
        if exists == False:
            file = open(filename, "w")
            output += key + "; 1; " + url + ", " + str(freq) + "\n"
            file.write(output)
        # rewrites the file with updated information
        else:
            file = open(filename, "w")
            file.write(output)
    # if file doesn't exist, create it with 1 entry
    except IOError:
        file = open(filename, "w")
        out = key + "; 1; " + url + ", " + str(freq) + "\n"
        file.write(out)
    file.close()

    indexInfo = open("index_info.txt", "w")
    totalPageNum = int(totalPageNum) + 1
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
        # key; numberOfPages; doc_url1, term_freq1; doc_url2, term_freq2
        list = line.split("; ")
        if list[0] == token:
            file.close()
            return list[2:]
    file.close()
    return False

if __name__ == "__main__":
    x = get_index_total()
    print(x)
    addPage_index_file("test", "url1", 10)
    x = get_index_total()
    print(x)
    addPage_index_file("zebra", "url3", 10)
    x = get_index_total()
    print(x)
    x = get_pages("test")
    print(x)
    x = get_pages("zebra")
    print(x)
    addPage_index_file("test", "url2", 5)
    x = get_index_total()
    print(x)
    x = get_pages("test")
    print(x)
    x = get_pages("zebra")
    print(x)
    addPage_index_file("123", "url2", 2)
    x = get_index_total()
    print(x)
    addPage_index_file("abc", "url2", 15)
    x = get_index_total()
    print(x)
    x = get_pages("test")
    print(x)
