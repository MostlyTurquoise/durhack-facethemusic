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
        print("checking", number)
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
        print(weights)
    return sequence

def createMelody(sequence,scale):
    melody = []
    for num in sequence:
        melody.append(getNote(scale,num))
    chords = []
    main = mp.chord(','.join(list(map(lambda x : x.name + str(x.num), melody))), duration=[1/4 for i in range(len(melody))], interval=[1/4 for i in range(len(melody))])
    for i in range(0,len(melody),4):
        root = mp.note(melody[i].name)
        try:
            fifth = root + 7
            third = scale[scale.index(root) + 2]
        except:
            third = root + 3
            fifth = third + 3
        chords.append(mp.chord(root.name + '3' + ',' + third.name + '3' + ',' + fifth.name + '3', duration=1))
    piece = mp.piece(tracks=[main, mp.concat(chords,'|')])
    return piece

def encode_data(data):
    scale = getKey(data)
    normalizedData = list(map(lambda x : (x-min(data))/(max(data)-min(data)), data))
    sequence = createSequence(1,len(data),normalizedData)
    melody = createMelody(sequence,scale)
    
    song = mpd.daw(3,name='test')
    song.load(0, './data/GeneralUser-GS.sf2')
    song.load(1, './data/GeneralUser-GS.sf2')
    aud = mpd.audio(melody, song, channel_num=2) + 10
    aud.export("text.mp3", format="mp3")

sampledata = [161.721, 161.7105, 161.7105, 161.7105, 161.7105, 161.7105, 161.7105, 161.711, 161.7146, 161.7152, 161.7255, 161.715, 161.7205, 161.7215, 161.7296, 161.7365, 161.7225, 161.7225, 161.7223, 161.7223, 161.7224, 161.7248, 161.7246, 161.7246, 161.7246, 161.7316, 161.7311, 161.7311, 161.7301, 161.7303]
song = encode_data(sampledata)
