import csv
import os

from music21 import converter
from music21.chord import Chord
from music21.harmony import chordSymbolFigureFromChord


def get_harmonies(path):
    s = converter.parse(path)
    cc = s.chordify()
    harmonies = []
    for c in cc.flat.getElementsByClass(Chord):
        harmonies.append(chordSymbolFigureFromChord(c))
    return harmonies


def process_folder_to_csv(csv_name='data/chords.csv', folder_name='db/Wikifonia', first_n=None):
    files = os.listdir(folder_name)
    n = len(files)
    csv_filename = csv_name

    if first_n:
        process_n = first_n
    else:
        process_n = n
    with open(csv_filename, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for i, fname in enumerate(files):
            print(f'{i}/{n}', end='\r', flush=True)
            try:
                song_harmonies = get_harmonies(f'{folder_name}/{fname}')
                writer.writerow([fname, str(song_harmonies)])
                if i % 10 == 0:
                    f.flush()
            except Exception as err:
                print(err)
            finally:
                if i == process_n:
                    f.flush()
                    print(f"Done! Processed {process_n} files")
                    break
