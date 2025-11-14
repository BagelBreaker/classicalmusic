from music21 import *
from rapidfuzz import *
import os, json, traceback
#rhythm:
#notes
#composer
#year
pieces = {}
composerList = ['mozart'] # and so on... ADD THIS LATER
OUT_FILE = os.path.join(os.path.dirname(__file__), 'notes.json')
for composer in composerList:
    paths = corpus.getComposer(composer)
    for mf in paths:
        try:
            print("Processing:", mf)
            s = corpus.parse(mf)
            key = s.analyze('key')
            notes = s.flatten().notes
            
            noteNames = []
            noteRhythms = []
            for n in s.recurse():
                if isinstance(n,chord.Chord):
                    #If the note is a chord then we choose the top note
                    noteNames.append(n.sortAscending().pitches[-1].nameWithOctave)
                elif isinstance(n,note.Note):
                    noteNames.append(n.nameWithOctave)
                noteRhythms.append(n.quarterLength)
                    
            
            pieces[str(mf)] = {
                'composer': composer,
                'key': key.tonic.name,
                'mode': key.mode,
                'notes': noteNames,
                'rhythms': noteRhythms
            }
            print(f"Processed {mf}")
        except Exception as e:
            print(f"Error processing {mf}: {e}")
            traceback.print_exc()

try:
    with open('notes.json', 'w', encoding='utf-8') as f:
        json.dump(pieces, f, default=str, indent=4)
    print("JSON data created successfully.")
    print(f"Total entries written to JSON: {len(pieces)}")
    print(os.path.abspath('notes.json'))
    print(os.path.getsize('notes.json'))
except Exception as e:
    print(f"Error creating JSON data: {e}")
    traceback.print_exc()

with open('notes.json', 'r') as f:
    preview = f.read(500)
print("Preview of file:\n", preview[:500])
