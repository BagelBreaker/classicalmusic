from music21 import *
from rapidfuzz import *
import json


def scoreSort(e):
    return e[0]

with open('notes.json', 'r') as f:
    pieces = json.load(f)

noteInput = input("Type in notes here: ")
rhythmInput = input("Type in rhythms here: ")

#partial ratio
scores = []
for filename, piece in pieces.items():
    pitchScore = fuzz.partial_ratio(noteInput,piece["notes"])
    scores.append((pitchScore, piece))
scores.sort(key=scoreSort, reverse=True)
topPieces = [scores[0][1],scores[1][1],scores[2][1]]
# print("Top 3 Results: \n" + str(scores[0][1]) + " " +str(scores[1][1]) + " "+str(scores[2][1]))
print("Top 3 Results: \n" + str(scores[0][1]['title'])+" "+ str(scores[1][1]['title'])+" "+str(scores[2][1]['title']))


    







    