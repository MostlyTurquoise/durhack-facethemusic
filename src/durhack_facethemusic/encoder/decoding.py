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
    normalize = lambda x : (x-min(data))/(max(data)-min(data))
    data = list(map(normalize,data))
    print(data)
    print(list(map(lambda x : round(x*1000), data)))
    diffs = [round((data[i+1]-data[i])*1000) for i in range(len(data)-1)]

    signs = []
    for diff in diffs:
        if diff < 0:
            signs.append(-1)
        elif diff > 0:
            signs.append(1)
        else:
            signs.append(0)
    
    print(diffs)

    unsignedHex = [hex(abs(diffs[i])) for i in range(len(diffs))]


    splitHex = list(map(split,unsignedHex))
    splitHex = splitBin(splitHex)

    track1 = mp.C('C5')
    count1 = len(data)
    duration1 = []
    track2 = mp.C('E5')
    count2 = len(data)
    duration2 = []
    track3 = mp.C('G6')
    count3 = len(data)
    duration3 = []

    for i in range(len(data)):
        if i == 0:
            if splitHex[0][i] == '0':
                duration1.append(1/4)
                count1 -= 1
            if splitHex[1][i] == '0':
                duration2.append(1/4)
                count2 -= 1
            if splitHex[2][i] == '0':
                duration3.append(1/4)
                count3 -= 1
        else:
            if splitHex[0][i] == '0':
                duration1[-1] += 1/4
                count1 -= 1
            if splitHex[1][i] == '0':
                duration2[-1] += 1/4
                count2 -= 1
            if splitHex[2][i] == '0':
                duration3[-1] += 1/4
                count3 -= 1

    print('a')
    chord1 = [track1 for i in range(count1)]
    print('1')
    chord2 = [track2 for i in range(count2)]
    chord3 = [track3 for i in range(count3)]
    print('b')
    piece = mp.P(tracks=[chord1,chord2,chord3])
    print('b')

    song = mpd.daw(num=3)
    song.load(0, "./data/GeneralUser-GS.sf2")
    song.load(1, "./data/GeneralUser-GS.sf2")
    song.load(2, "./data/GeneralUser-GS.sf2")
    print('c')
    return pydub.effects.normalize(song.export(piece, action="get"))
