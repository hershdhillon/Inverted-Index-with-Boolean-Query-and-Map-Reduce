#!/usr/bin/python
import sys
#Input From Standard Inpit
for line in sys.stdin:

    # Remove Whitespace
    line = line.strip()

    # Split Line in Words
    words = line.split()

    documentId = words.pop(0)
    lineNumber = words.pop(0)

    for index in range( len(words) ):
        word = words[ index ]
        print("{0}, {1}, {2}, {3}".format( word, documentId, lineNumber, index ))
