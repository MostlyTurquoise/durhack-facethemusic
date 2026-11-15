import musicpy as mp
import musicpy.daw as mpd
import pydub.effects

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
    chord3 = [binStr[i+2] for i in range(0,len(binStr)-2,4)]
    chord4 = [binStr[i+3] for i in range(0,len(binStr)-3,4)]
    return(chord1, chord2, chord3, chord4)

def encode_data(data):
    key = data[0]
    normalize = lambda x : (x-min(data))/(max(data)-min(data))
    data = list(map(normalize,data))
    #print(data)
    #print(list(map(lambda x : round(x*1000), data)))
    diffs = [round((data[i+1]-data[i])*1000) for i in range(len(data)-1)]

    signs = []
    for diff in diffs:
        if diff < 0:
            signs.append(-1)
        elif diff > 0:
            signs.append(1)
        else:
            signs.append(0)
    
    #print(diffs)

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
    track4 = mp.C('B6')
    count4 = len(data)
    duration4 = []

    for i in range(len(data)):
        if i == 0:
            if splitHex[0][i] == '0':
                count1 -= 1
            if splitHex[1][i] == '0':
                count2 -= 1
            if splitHex[2][i] == '0':
                count3 -= 1
            if splitHex[3][i] == '0':
                count4 -= 1

            duration1.append(1/4)
            duration2.append(1/4)
            duration3.append(1/4)
            duration4.append(1/4)
        else:
            if splitHex[0][i] == '0':
                duration1[-1] += 1/4
                count1 -= 1
            else:
                duration1.append(1/4)
            if splitHex[1][i] == '0':
                duration2[-1] += 1/4
                count2 -= 1
            else:
                duration2.append(1/4)
            if splitHex[2][i] == '0':
                duration3[-1] += 1/4
                count3 -= 1
            else:
                duration3.append(1/4)
            if splitHex[3][i] == '0':
                duration4[-1] += 1/4
                count4 -= 1
            else:
                duration4.append(1/4)

    chordlist1 = []
    print(duration1)
    for i in range(count1):
        chordlist1.append(track1)
        chordlist1[i].set(duration1[i],duration1[i])
    chordlist2 = []
    for i in range(count2):
        chordlist2.append(track2)
        chordlist2[i].set(duration2[i],duration2[i])
    chordlist3 = []
    for i in range(count3):
        chordlist3.append(track3)
        chordlist3[i].set(duration3[i],duration3[i])
    chordlist4 = []
    for i in range(count4):
        chordlist4.append(track4)
        chordlist4[i].set(duration4[i],duration4[i])

        

    print('a')
    chord1 = mp.concat(chordlist1)
    print('1')
    chord2 = mp.concat(chordlist2)
    print('2')
    chord3 = mp.concat(chordlist3)
    print('3')
    chord4 = mp.concat(chordlist4)
    print('b')
    piece = mp.P(tracks=[chord1,chord2,chord3,chord4], bpm=120)
    print('b')

    song = mpd.daw(4)
    song.load(0, "./data/GeneralUser-GS.sf2")
    song.load(1, "./data/GeneralUser-GS.sf2")
    song.load(2, "./data/GeneralUser-GS.sf2")
    song.load(3, "./data/GeneralUser-GS.sf2")
    #print('c')
    return song.export(piece, action="get")
