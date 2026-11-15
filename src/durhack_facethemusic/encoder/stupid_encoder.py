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
    note_data: list[musicpy.primitives.note] = [
        mp.chord(
            notes=[
                mp.N(
                    mp.freq_to_note(
                        LOW_FREQ + (d - lowest) / data_range * (HIGH_FREQ - LOW_FREQ),
                        to_str=True,
                    )
                )
            ],
            interval=[0],
            duration=1,
        )
        for d in wip_data
    ]
    music: musicpy.piece_class.piece = mp.build(
        [sum(note_data, start=mp.chord(notes=[])), 15],
        bpm=600,
    )

    song = mpd.daw(3, name="hii")
    song.load(0, "./data/GeneralUser-GS.sf2")
    return pydub.effects.normalize(song.export(music, action="get"))
