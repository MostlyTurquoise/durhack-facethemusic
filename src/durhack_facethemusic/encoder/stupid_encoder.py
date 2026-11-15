import time

import musicpy as mp
import musicpy.daw as mpd
import musicpy.primitives
import musicpy.piece_class
import itertools

import pydub.effects

LOW_FREQ = 400
HIGH_FREQ = 800


def encode_data(data: list[float]):
    wip_data = data[::10]
    lowest = min(data)
    data_range = max(data) - lowest
    wip_data = [(d - lowest) / data_range for d in wip_data]
    note_data: list[musicpy.primitives.note] = [
        mp.chord(
            notes=[
                mp.N(
                    mp.freq_to_note(LOW_FREQ + d * (HIGH_FREQ - LOW_FREQ), to_str=True)
                )
            ],
            interval=[0],
            duration=1,
        )
        for d in wip_data
    ]
    music: musicpy.piece_class.piece = mp.build(
        [list(itertools.accumulate(note_data, lambda a, b: a + b))[-1], 15],
        bpm=600,
    )

    song = mpd.daw(3, name="hii")
    song.load(0, "./data/GeneralUser-GS.sf2")
    print(song.instruments(0).all_instruments())
    song.instruments(0).change(bank=0, preset=11)
    time.sleep(1)
    return pydub.effects.normalize(song.export(music, action="get"))
