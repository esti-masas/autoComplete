import linecache
import string
from dataclasses import dataclass
from weighted_levenshtein import levenshtein, optimal_string_alignment, damerau_levenshtein

import numpy as np

from Include.Initialization import sentences, initialize


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int


def get_best_k_completions(prefix: str):
    suggestions=[]
    #in case there is perfect match
    insert_costs = np.ones(128, dtype=np.float64)  # make an array of all 1's of size 128, the number of ASCII characters
    delete_costs = np.ones(128, dtype=np.float64)
    substitute_costs = np.ones((128,128), dtype=np.float64)
    alphabet = string.ascii_letters+"0123456789 "
    prefix = ''.join(filter(lambda i: i in alphabet, prefix))

    prefixsize=len(prefix.split())
    if prefixsize<=6:
        for i in sentences[prefixsize]:  # list of dictionaries
            for j in i.values():  # list of sentences
                for w in j:  # one sentence
                    w = ''.join(filter(lambda i: i in alphabet, w))
                    if w.lower().startswith(prefix.lower()) or levenshtein(prefix.lower(), w.lower(), insert_costs=insert_costs,
                                                                   delete_costs=delete_costs,
                                                                   substitute_costs=substitute_costs) == 0 :
                        filename = list(i.keys())[0][0]
                        offset = list(i.keys())[0][1]
                        complete_sentence = linecache.getline(filename, offset)[:-1]
                        suggestions.append(
                            AutoCompleteData(complete_sentence, filename.split("\\")[-1], offset, len(prefix) * 2))
                        # delete char
                    elif levenshtein(prefix.lower(), w.lower(), delete_costs=delete_costs) == 1 or levenshtein(
                            prefix.lower(), w.lower(), insert_costs=insert_costs) == 1:
                        filename = list(i.keys())[0][0]
                        offset = list(i.keys())[0][1]
                        complete_sentence = linecache.getline(filename, offset)[:-1]
                        # check the score according the place
                        if w.lower()[0] != prefix.lower()[0]:
                            score = len(prefix) * 2 - 10
                        elif len(w) >= 2 and  len(prefix) >= 2 and w.lower()[1] != prefix.lower()[1] :
                            score = len(prefix) * 2 - 8
                        elif len(w) >= 3  and len(prefix) >= 3  and w.lower()[2] != prefix.lower()[2] :
                            score = len(prefix) * 2 - 6
                        elif len(w) >= 4 and len(prefix) >= 4 and w.lower()[3] != prefix.lower()[3] :
                            score = len(prefix) * 2 - 4
                        else:
                            score = len(prefix) * 2 - 2
                        suggestions.append(AutoCompleteData(complete_sentence, filename.split("\\")[-1], offset, score))

                    elif levenshtein(prefix.lower(), w.lower(), substitute_costs=substitute_costs) == 1:
                        # check the score according the place
                        filename = list(i.keys())[0][0]
                        offset = list(i.keys())[0][1]
                        complete_sentence = linecache.getline(filename, offset)[:-1]
                        # check the score according the place
                        if w.lower()[0] != prefix.lower()[0]:
                            score = len(prefix) * 2 - 5
                        elif len(w) >= 2 and  len(prefix) >= 2 and w.lower()[1] != prefix.lower()[1] :
                            score = len(prefix) * 2 - 4
                        elif len(w) >= 3  and len(prefix) >= 3 and w.lower()[2] != prefix.lower()[2] :
                            score = len(prefix) * 2 - 3
                        elif len(w) >= 4 and len(prefix) >= 4 and w.lower()[3] != prefix.lower()[3] :
                            score = len(prefix) * 2 - 2
                        else:
                            score = len(prefix) * 2 - 1
                        suggestions.append(AutoCompleteData(complete_sentence, filename.split("\\")[-1], offset, score))
    else:
        suggestions=get_best_k_completions(' '.join(prefix.split()[0:6]))
    return sorted(suggestions,reverse=True,key=get_score)[0:5]


def get_score(element):
    return element.score

if __name__=="__main__":
    #get path
    print("Loading the files and preparing the system...")
    initialize(r"2021-archive\2021-archive\python-3.8.4-docs-text\c-api")
    prefix=input("The system is ready. Enter your text:\n")
    while(True):
        while prefix[-1]!="#":
           completions=get_best_k_completions(prefix)
           if len(completions)>0:
               print("Here are "+ str(len(completions)) +" suggestions:")
               for c in completions:
                   print((str(completions.index(c)+1))+". "+c.completed_sentence+" ("+c.source_text+" "+ str(c.offset)+")")
           else:
               print("No suggestion")
           prefix+=input(prefix)
        prefix = input("The system is ready. Enter your text:\n")









