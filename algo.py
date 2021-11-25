import re
import json
import note_seq
import streamlit as st
from note_seq.protobuf import music_pb2

# import necessary tables from .json as dictionary
with open('data/chordSelection.json', 'r') as fp:
    chordSelection = json.load(fp)

with open('data/freqLetter.json', 'r') as fp:
    freqLetter = json.load(fp)
    
with open('data/noteFreqTableColl.json', 'r') as fp:
    chordCollection = json.load(fp)
    
with open('data/notePitch.json', 'r') as fp:
    notePitch = json.load(fp)
        
# helper functions
def clean(strval):
  lower = strval.lower()
  s = re.sub(r'[^a-z ]', '', lower)
  s = s.split()
  return s

def chordSelect(l):
  select = None

  for key in chordSelection:
    if l in chordSelection[key]:
      select = key
  
  return select

def normalize(arr):

  arr = [list(item) for item in arr]
  sum = 0
  
  for el in arr:
    sum = sum + el[1]

  for el in arr:
    el[1] = el[1] / sum
  
  return arr

def findDestruct(noteList, letterList, nextLetter):

  cumLetter = 0
  
  for el in letterList:
    cumLetter = cumLetter + el[1]
    if el[0] == nextLetter:
      break
  
  idx = 0
  cumNote = letterList[idx][1]

  while cumNote < cumLetter:
    idx += 1
    if idx == 6:
      break
    cumNote += noteList[idx][1]

  note = noteList[idx][0]

  return note

def addNote(prevNote, prevLetter, nextLetter, major='c'):
  
  majorTable = chordCollection[major]
  nextNote = None

  # note pair
  noteList = list(majorTable[prevNote].items())
  noteList.sort(key = lambda el:el[1], reverse = True)
  noteList = normalize(noteList)
  # print(noteList)

  # letter pair
  letterList = list(freqLetter[prevLetter].items())
  letterList.sort(key = lambda el:el[1], reverse = True)
  # print(letterList)

  nextNote = findDestruct(noteList, letterList, nextLetter)

  return nextNote

def convertPitch(seq):
    
    songMidi = []

    for el in seq:
        songMidi.append(notePitch[el])
        
    return songMidi

def pitchToNS(seq, velocity=80, qpm=60):
  # Initialize note sequence
  genMusic = music_pb2.NoteSequence()

  # Add pitch to sequence
  start = 0.0
  for p in range(len(seq)):

    genMusic.notes.add(pitch = seq[p], start_time = start, end_time = start + 0.5, velocity = 80)
    start += 0.5
  
  genMusic.total_time = start
  genMusic.tempos.add(qpm = 60);

  return genMusic

def generateSong(inputText):

    songSeq = []
    
    word = ""
        
    for el in inputText:
        word = word + el
        
    word = word.replace(" ", "")
    
    # st.write(word)

    chord = None
    for i in range (len(word)):
        if chord == None:
            chord = chordSelect(word[i])
            # print("CHORD: ", chord)
            songSeq.append(chord)
        else:
            next = addNote(songSeq[-1], word[i - 1], word[i], major=chord)
            songSeq.append(next)
            
    # st.write(songSeq)

    songSeq.append(chord)
    songMidi = convertPitch(songSeq)
    
    gen = pitchToNS(songMidi)
    
    return gen
    
    

