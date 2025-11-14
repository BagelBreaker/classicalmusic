from music21 import *
from rapidfuzz import *
import json

def scoreSort(e):
    return e[0];

with open('notes.json', 'r') as f:
    pieces = json.load(f)

noteInput = input("Type in notes here: ")
rhythmInput = input("Type in rhythms here: ")

#partial ratio
scores = []
for piece in pieces:
    pitchScore = fuzz.partial_ratio(noteInput,piece[3])
    scores.append((pitchScore, piece))
scores.sort(key=scoreSort, reverse=True)
topPieces = [scores[0][1],scores[1][1],scores[2][1]]
print("Top 3 Results: \n" + scores[0][1]+" "+scores[1][1]+" "+scores[2][1])








    