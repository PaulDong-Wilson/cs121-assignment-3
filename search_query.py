import ast
import operator
import os
import inverted_indexing
import file_system
from nltk.stem import PorterStemmer





def find_searchquery(searchquery):
    open_index = os.path.join(os.getcwd(), "test.txt")
    
    tokens = list(inverted_indexing.tokenize(searchquery))
    
    found = [False for w in tokens]
    documents = [dict() for w in tokens]

    with open(open_index, 'r') as f:
        while True:
            try:
                line = f.readline()
                
                if not line:
                    break
                #sample line: {'emphysema': {'1725': 2, '3027': 2, '25223': 1, '32922': 1, '49911': 3}}
                # ast.literal_eval(node_or_string) safely evaluate an expression node or a string containing a Python literal or container display
                word_dict = ast.literal_eval(line)
                #output dictionary: {'emphysema': {'1725': 2, '3027': 2, '25223': 1, '32922': 1, '49911': 3}}
                #print(word_dict)
                token, postings_dict = list(word_dict.items())[0]
                #list(word_dict.items())[0] = ('emphysema', {'1725': 2, '3027': 2, '25223': 1, '32922': 1, '49911': 3})
                for i in range(len(tokens)):
                    if tokens[i] == token:
                        found[i] = True
                        documents[i] = postings_dict
                else:
                    continue
            except EOFError:
                print("Reached end of file.")
                break
            except Exception as e:
                print("Exception popped up")
                print(e)

    set_docs = [set() for x in tokens]
    counter = 0
    for t_dict in documents:
        set_docs[counter] = set(t_dict.keys())       
        counter += 1

    final_set = set.intersection(*set_docs)
    print("final_set: ", final_set)
    print(f"# of documents: {len(final_set)}")
    final_dict = dict()
    for t in final_set:
        t_list = [d[t] for d in documents]
        final_dict[t] = sum(t_list)

    return final_dict 

def get_top_num_ids(final_dict, number):
    sort_dict = sorted(final_dict.items(), key=operator.itemgetter(1), reverse=True)[:number]
    final_final_dict = [int(k) for k in dict(sort_dict).keys()]
    return final_final_dict
    
if __name__ == "__main__":
    #word_dict = ast.literal_eval("{'emphysema': {'1725': 2, '3027': 2, '25223': 1, '32922': 1, '49911': 3}}")
    #print(type(word_dict))
    #token, postings_dict = list(word_dict.items())[0]
    #print(list(word_dict.items())[0])
    a = find_searchquery("emphysema")
    b = get_top_num_ids(a, 2)
    print(b)

