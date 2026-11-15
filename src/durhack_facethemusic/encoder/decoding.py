import musicpy as mp
import musicpy.daw as mpd

def split(hexadec):
    hexadec = int(hexadec, base=16)
    dig2 = hexadec%16
    dig1 = int((hexadec - dig2)/16)
    return (dig1,dig2)

def splitBin(splithex):
    binArr = []
    for pair in splithex:
        for num in pair:
            num = bin(num)
            num = str(num)[2:]
            num = num.ljust(4, '0')
            binArr.append(num)
    binStr = ''.join(binArr)
    chord1 = [binStr[i] for i in range(0,len(binStr),4)]
    chord2 = [binStr[i+1] for i in range(0,len(binStr)-1,4)]
    chord3 = [binStr[i+3] for i in range(0,len(binStr)-3,4)]
    chord4 = [binStr[i+4] for i in range(0,len(binStr)-4,4)]
    return(chord1, chord2, chord3, chord4)

def encode_data(data):
    key = data[0]
    diffs = [round((data[i+1]-data[i])*1000) for i in range(len(data)-1)]

    signs = []
    for diff in diffs:
        if diff < 0:
            signs.append(-1)
        elif diff > 0:
            signs.append(1)
        else:
            signs.append(0)

    unsignedHex = [hex(abs(diffs[i])) for i in range(len(diffs))]


    splitHex = list(map(split,unsignedHex))[:10]
    splitHex = splitBin(splitHex)

    track1 = ['C5' for _ in range(len(data))]
    duration1 = []
    track2 = ['E5' for _ in range(len(data))]
    duration2 = []
    track3 = ['G6' for _ in range(len(data))]
    duration3 = []

    for i in range(track1):
        if i == 0:
            if splitHex[0][i] == '0':
                duration1.append(1/4)
                track1.pop(-1)
            if splitHex[1][i] == '0':
                duration2.append(1/4)
                track2.pop(-1)
            if splitHex[2][i] == '0':
                duration3.append(1/4)
                track3.pop(-1)
        else:
            if splitHex[0][i] == '0':
                track1[i] = 0
                duration[-1] += 1/4
                track1.pop(-1)
            if splitHex[1][i] == '0':
                track1[i] = 0
                duration[-1] += 1/4
                track2.pop(-1)
            if splitHex[2][i] == '0':
                track1[i] = 0
                duration[-1] += 1/4
                track3.pop(-1)

    chord1 = mp.C(','.join(track1), interval = duration1, duration = duration1)
    chord2 = mp.C(','.join(track2), interval = duration2, duration = duration2)
    chord3 = mp.C(','.join(track3), interval = duration3, duration = duration3)

    piece = mp.P(tracks=[chord1,chord2,chord3])

    song = mpd.daw(num=3)
    song.load(0, './data/GeneralUser-GS.sf2')
    song.load(1, './data/GeneralUser-GS.sf2')
    song.load(2, './data/GeneralUser-GS.sf2')
    return pydub.effects.normalize(song.export(music, action="get"))
