from music21 import *

s = corpus.parse('bach/bwv66.6')
print(s.analyze('key'))

notes = s.flatten().notes

for note in notes:
    print(note.nameWithOctave)

    