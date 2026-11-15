import musicpy as mp
import musicpy.daw as mpd
import pydub
import io
import random

def getKey(data):
    keykey = data[0]
    keykey *= 100
    keykey = round(keykey)
    keykey %= 14
    if keykey > 7:
        mode = 'major'
    else:
        mode = 'minor'
    keykey %= 7
    key = chr(keykey + 65) + '5'
    notes = mp.scale(key, mode)
    return notes

def getNote(scale, number):
    notes = scale.notes
    while number < 0 or number >= 8:
        if number < 0:
            notes = list(map(lambda x : x-12, notes))
            number += 8
        else:
            notes = list(map(lambda x : x+12, notes))
            number -= 8
    if number % 1 != 0:
        note = notes[int(number-0.5)]
        note = note + 1
    else:
        note = notes[int(number)]

    return note


def calcWeights(diff, weights):
    if diff < 0:
        for i in range(4):
            weights[i] = weights[i]*(1-diff*4)
    elif diff > 0:
        for i in range(4):
            weights[i + 5] *= (1+diff*4)
    return weights

def createSequence(start,length, normalizedData):
    prevWeights = [2,3,4,5,1,5,4,3,2]
    options = [-4,-3,-2,-1,0,1,2,3,4]
    sequence = [start]
    for i in range(length-1):
        diff = (normalizedData[i]-normalizedData[i+1])
        weights = calcWeights(diff, prevWeights)
        nextChoice = random.choices(options, weights=weights)[0]
        nextNote = sequence[i] + nextChoice
        if weights[0] > 100:
            for i in range(4):
                weights[i] *= 0.7
                if i in (0,1):
                    weights[i] *= 1.25
            nextNote += 0.5
        elif weights[-1] > 100:
            for i in range(4):
                weights[i + 5] *= 0.7
                if i in (7,8):
                    weights[i] *= 1.25
            nextNote = sequence[i] + 7
        sequence.append(nextNote)
        prevWeights = weights
    return sequence

def createMelody(sequence,scale):
    melody = []
    for num in sequence:
        melody.append(getNote(scale,num))
    chords = []
    main = mp.chord(','.join(list(map(lambda x : x.name + str(x.num), melody))), duration=[1/4 for i in range(len(melody))], interval=[1/4 for i in range(len(melody))])
    for i in range(0,len(melody),4):
        #print(i)
        root = mp.note(melody[i].name)
        try:
            third = scale[scale.index(root) + 2]
        except:
            third = root + 3
        fifth = third + 3
        chords.append(mp.chord(root.name + '3' + ',' + third.name + '3' + ',' + fifth.name + '3', duration=1))
    chordTrack = mp.concat(chords)
    piece = mp.piece(tracks=[main, chordTrack])
    return piece

def encode_data(data):
    #print('starting')
    scale = getKey(data)
    #print('retrieved scale')
    normalizedData = list(map(lambda x : (x-min(data))/(max(data)-min(data)), data))
    sequence = createSequence(1,len(data),normalizedData)
    #print('created sequence')
    melody = createMelody(sequence,scale)
    #print('created piece')
    
    song = mpd.daw(2)
    song.load(0, './data/GeneralUser-GS.sf2')
    song.load(1, './data/GeneralUser-GS.sf2')
    #print('hera?')
    return pydub.effects.normalize(song.export(melody, action="get"))
