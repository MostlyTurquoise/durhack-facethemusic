import musicpy as mp
import musicpy.daw as mpd
import pydub


def encode_data(data: list[float]) -> pydub.AudioSegment:
    chord_progression_position = int(str(data[0])[-1])
    key = get_key(data[0])

    chords = mp.chord(notes=[])
    for i in data[::10]:
        key = get_key(i)
        chord = get_chord_progression(key, chord_progression_position)
        chords = chords + chord

    song = mpd.daw(3, name="audio")
    song.load(0, "./data/GeneralUser-GS.sf2")
    return song.export(chords, mode='mp3', action='get')

def get_key(data: float) -> str:
    keys = ["C", "D", "G", "F"]
    key_position = int(str(data)[-1])%len(keys)
    return keys[key_position]

def get_chord_progression(key: str, chord_progression_position: int) -> mp.chord:
    scale = mp.scale(key, "major")
    I = scale.get_chord("I")
    IV = scale.get_chord("IV")
    VI = scale.get_chord("VI")
    V = scale.get_chord("V")
    vi = scale.get_chord("vi")
    ii = scale.get_chord("ii")
    bVII = scale.get_chord("bVII")
    chord_progressions = [-1,(I+vi+IV+V),(I+V+vi+IV),(ii+V+I),(I+IV+ii+V),(I+vi+ii+V),
                          (I+IV+I+V+I+IV+I+V+I),(I+V+VI+V),(I+IV+bVII+IV),(I+V+bVII+IV)]
    return chord_progressions[chord_progression_position]

def main():
    test = [1.293782, 1.293777, 1.293799, 1.293809, 1.293774, 1.29368, 1.293424, 1.293419, 1.293466,
            1.293465, 1.293489, 1.293451]
    encode_data(test)

if __name__=="__main__":
    main()