from pathlib import Path                                                        # used to make file path compatible with all type of operating system

data_folder = Path("data/")                                                     # one can also use d:\\udemy\\python15Project\\proj2\\data in windows

import json

word = input("Enter word to search definition: ")

filename = "D"+word[0].upper()+".json"
file_to_open = data_folder / filename
with open(file_to_open) as f:
    data = json.load(f)

word = word.upper()
# print("MEANINGS:\n\t{}".format(data[word]['MEANINGS']))
# print("ANTONYMS:\n\t{}".format(data[word]['ANTONYMS']))
# print("SYNONYMS:\n\t{}".format(data[word]['SYNONYMS']))
# print(data[word])

# if word in data:
#     print("\nWord:", word)
#
#     print("\nMEANINGS:")
#     for key in data[word]['MEANINGS']:
#         print('\t', key + ':')  #, data[word]['MEANINGS'][key])
#         for i in data[word]['MEANINGS'][key]:
#             print('\t\t',i)
#     print("ANTONYMS:\n\t{}".format(data[word]['ANTONYMS']))
#     print("SYNONYMS:\n\t{}".format(data[word]['SYNONYMS']))
# else:
#     print("No definition present.")

def printNestedDefinition(word):
    if isinstance(word, list):
        for i in word:
            printNestedDefinition(i)
    else:
        print('\t\t',word)
    # print('\t\t'.join([str(i) for i in word]))

def printNestedOther(word):
    if isinstance(word, list):
        for i in word:
            printNestedOther(i)
    else:
        print('\t',word)

def printMeanings(word):
    print("\nMEANINGS:")
    if word['MEANINGS'] == {}:
        print()
    else:
        for key in word['MEANINGS']:
            print('\t', key + ':')                                                  #, data[word]['MEANINGS'][key])
            for i in word['MEANINGS'][key]:
                # print('\t\t',i)
                printNestedDefinition(i)

def printAntonyms(word):
    print("ANTONYMS:")
    if word['ANTONYMS'] == []:
        print()
    else:
        printNestedOther(word['ANTONYMS'])

def printSynonyms(word):
    print("SYNONYMS:")
    if word['SYNONYMS'] == []:
        print()
    else:
        printNestedOther(word['SYNONYMS'])

def translate(word):
    print("\nWord:", word)
    printMeanings(data[word])
    printAntonyms(data[word])
    printSynonyms(data[word])

# import bisect

# def find_closest(data, expected):
#     res = bisect.bisect_left(list(data.keys()), expected)
#     return res

from difflib import get_close_matches

def find_closest(data, expected):
    res = get_close_matches(expected, list(data.keys()), cutoff=0.7)
    return res

def mapToExistingData(word):
    if word.upper() in data:
        translate(word.upper())
    elif word.title() in data:
        translate(word.title())
    elif word.lower() in data:
        translate(word.lower())
    elif len(find_closest(data,word))>0:
        print("\nNo definition present for your input \"{}\". Now showing close result: ".format(word)+"\nDo you want to continue with \"{}\" word.".format(find_closest(data, word)[0]))
        decide = input("Press \'y\' for yes and \'n\' for no: ")
        if decide == 'y':
            # find_closest(data, word)
            closeWord = find_closest(data,word)
            # translate(list(data)[closeWord-1])                                    Use when use bisect library
            firstClose = closeWord[0]
            translate(firstClose)
        elif decide == 'n':
            print("No definition present.")
        else:
            print("You input wrong choice. Now Exiting!")
    else:
        print("No definition present.")

mapToExistingData(word)
