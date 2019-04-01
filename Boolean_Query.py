import re
import os
import cProfile, pstats, io
import collections
from nltk import word_tokenize

# Defining functions for Intersection, Union and Compliment Queries to perfrom Boolean Search

class Operator:

    def intersection(result, term):

        return result.intersection(term)

    def union(result, term):
        return result.union(term)

    def compliment(result, term):

        return result.difference(term)

# Define Boolean Query Class

class BooleanQuery:

    OPERATORS = {'and' : Operator.intersection,
                 'or' : Operator.union,
                 'not': Operator.compliment
                }

    def __init__(self, InvertedIndexObject):
        self.InvertedIndexObject = InvertedIndexObject
        self.reg = re.compile("( and | or )")

    def Tokenize(self, query):
        return self.reg.split(query)

    def search(self, query):
        query = [x.strip()  for x in  self.Tokenize(query.lower())]
        query.reverse()
        term = query.pop()
        compliment = set()
        result = set()
        if "not" in term:
            compliment.update(self.InvertedIndexObject.get_posting(term[4:]))
        else:
            if self.InvertedIndexObject.inverted_index.__contains__(term):
                result.update(self.InvertedIndexObject.get_posting(term))
        try:
            while True:
                term = query.pop()
                if "not" in term:
                    term = term[14:]
                    compliment.update(self.InvertedIndexObject.get_posting(term[4:].strip()))
                else:
                    if term in BooleanQuery.OPERATORS.keys():
                        next_term = query.pop()
                        if "not" in next_term:
                            compliment.update(self.InvertedIndexObject.get_posting(next_term[14:].strip()))
                            continue
                        else:
                            result = BooleanQuery.OPERATORS[term](result,self.InvertedIndexObject.get_posting(next_term))
                    else:
                        result.update(self.InvertedIndexObject.get_posting(term))

        except IndexError:
            pass

        if compliment != set():
            result = self.OPERATORS["not"](result, compliment)
            compliment.clear()

        print("Documents Found : ")
        print([self.InvertedIndexObject.index[x] for x in result])

# Loading Inverted Index

def readIndex():
    inverted_index = {}
    inverted_index = json.load(open("Inverted_Index.txt"))
    return inverted_index

# Defining the Inverted Index Class.

class InvertedIndex:
    def __init__(self, dir="documents"):
        self.dir = dir
        self.inverted_index = collections.defaultdict(dict)
        self.index = dict()
        self.build()

    def get_posting(self, term):
        if self.inverted_index.__contains__(term):
            return self.inverted_index[term]['posting']

    def get_frequency(self, term):
        if self.inverted_index.__contains__(term):
            return self.inverted_index[term]['frequency']

    def build(self):
        count = 0
        try:
            for doc_id, document in enumerate(os.listdir(self.dir)):
                self.index[doc_id] = document
                with open(str(self.dir + os.path.sep + document), 'r') as f:
                    for line in f:
                        count += 1
                        print(count, end="\r")
                        for term in word_tokenize(line.rstrip("\n")):
                            try:
                                if not self.inverted_index.__contains__(term):
                                    raise NameError
                                self.inverted_index[term]['frequency'] += 1
                                self.inverted_index[term]['posting'].add(doc_id)

                            except NameError:
                                self.inverted_index[term] = {'frequency': 1, 'posting': set([doc_id])}
        except:
            print(count, end="\r")

# Main Class

def main():
    pr = cProfile.Profile()
    pr.enable()
    index = InvertedIndex()
    boolean_query = BooleanQuery(index)
# While loop will exit if user enters exit or end
    while True:
        try:
            query = input("Enter Query :: ").strip()
            if query.lower() == 'exit'or'end':
                exit()
            else:
                boolean_query.search(query)
        except KeyboardInterrupt:
            break

    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

if __name__ == '__main__':
    main()