import unicodedata
from functools import reduce
import pickle
import json

#Adding stopwords form file stopwords.txt in a list for further stopwords processing.
stop_words_list = []
stop_words_file = open("stopwords.txt", "r").read().split()
for item in stop_words_file:
    if item in stop_words_list:
        continue
    else:
        stop_words_list.append(item)

STOP_WORDS = frozenset(stop_words_list)

#Doing Document Processing by word cleanup, normalization and stop word removal

def word_split(text):

    word_list = []
    word_current = []
    windex = None

    for i, c in enumerate(text):
        if c.isalnum():
            word_current.append(c)
            windex = i
        elif word_current:
            word = u''.join(word_current)
            word_list.append((windex - len(word) + 1, word))
            word_current = []

    if word_current:
        word = u''.join(word_current)
        word_list.append((windex - len(word) + 1, word))

    return word_list

def words_cleanup(words):

    cleaned_words = []
    for index, word in words:
        if word in STOP_WORDS:
            continue
        cleaned_words.append((index, word))
    return cleaned_words

def words_normalize(words):

    normalized_words = []
    for index, word in words:
        wnormalized = word.lower()
        normalized_words.append((index, wnormalized))
    return normalized_words

def word_index(text):

    words = word_split(text)
    words = words_normalize(words)
    words = words_cleanup(words)
    return words

def inverted_index(text):

    inverted = {}

    for index, word in word_index(text):
        locations = inverted.setdefault(word, [])
        locations.append(index)

    return inverted

def inverted_index_add(inverted, doc_id, doc_index):

    for word, locations in doc_index.items():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted


def writeIndex(inverted):
    json.dump(inverted, open("Inverted_Index.txt", 'w'))

if __name__ == '__main__':

    doc1 = open("Documents/doc1.txt", "r")
    doc1 = doc1.read()

    doc2 = open("Documents/doc2.txt", "r")
    doc2 = doc2.read()

    doc3 = open("Documents/doc3.txt", "r")
    doc3 = doc3.read()

    # Creating and Saving Inverted Index

    inverted = {}
    documents = {'doc1':doc1, 'doc2':doc2, 'doc3':doc3}
    for doc_id, text in documents.items():
        doc_index = inverted_index(text)
        inverted_index_add(inverted, doc_id, doc_index)

    print("\n---------------------Positional Inverted Index---------------------\n")
    print("     Token             Document : Location\n")

    # Printing the Inverted-Index
    for word, doc_locations in inverted.items():
        print ("%10s ----> %10s " % (word, doc_locations))

    writeIndex(inverted)