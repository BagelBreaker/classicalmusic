from music21 import *
from rapidfuzz import *
import os, json, traceback
#rhythm:
#notes
#composer
#year
def check_zeroes(b):
    if b == 0:
        return False
    return True
pieces = {}
# composerList = ['bach','beethoven','chopin','coreli','handel','haydn','joplin','monteverdi','mozart','palestrina','schumann_clara','schumann_robert','verdi'] # and so on... ADD THIS LATER
composerList = ['mozart']
OUT_FILE = os.path.join(os.path.dirname(__file__), 'notes.json')
for composer in composerList:
    paths = corpus.getComposer(composer)
    for mf in paths:
        try:
            print("Processing:", mf)
            s = corpus.parse(mf)
            key = s.analyze('key')
            a = None
            title = s.metadata.title or s.metadata.movementName or s.metadata.movementNumber or None
            if s.parts and len(s.parts) > 0:
                a = s.parts[0]
                print("First part accessed")
            else:
                a = s
            # notes = s.flatten().notes


            noteNames = []
            noteRhythms = []
            noteNamesString = ""
            noteRhythmsString = ""
            for n in a.recurse():
                ql = None
                if hasattr(n,'tie') and n.tie is not None:
                    
                    if hasattr(n,'staccato') or hasattr(n,'tenuto') or n.tie.type != 'stop':
                        print("tie found, skipping", n.nameWithOctave)
                    else:
                        if isinstance(n,chord.Chord):
                            noteNamesString+=n.sortAscending().pitches[-1].nameWithOctave+""
                        else:
                            noteNamesString += n.nameWithOctave + " "
                        print("tie found, adding",n.nameWithOctave)
                        ql = round(n.quarterLength,3)
                        if check_zeroes(ql) == False:
                            continue
                        noteRhythmsString+=str(ql)+" "
                    continue
                elif isinstance(n, note.Rest):
                    noteNamesString+="R "
                    continue
                if isinstance(n,chord.Chord):
                    #If the note is a chord then we choose the top note
                    # noteNames.append(n.sortAscending().pitches[-1].nameWithOctave)
                    noteNamesString += n.sortAscending().pitches[-1].nameWithOctave + " "
                elif isinstance(n,note.Note):
                    # noteNames.append(n.nameWithOctave)
                    noteNamesString += n.nameWithOctave + " "
                # noteRhythms.append(n.quarterLength)
                ql = n.quarterLength
                ql = round(ql,3)
                if check_zeroes(ql) == False:
                    continue
                noteRhythmsString += str(ql) + " "


            pieces[str(mf)] = {
                'composer': composer,
                'key': key.tonic.name,
                'mode': key.mode,
                'notes': noteNamesString,
                'rhythms': noteRhythmsString,
                'title': title
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
