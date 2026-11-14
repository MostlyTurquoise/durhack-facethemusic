import musicpy as mp
import musicpy.daw as mpd
import musicpy.primitives
import musicpy.piece_class
import musicpy.scale_class
import musicpy.chord_class
import itertools
import random
import typing as t

import pydub.effects

LOW_FREQ = 400
HIGH_FREQ = 800

one = "Imaj7"
two = "ii7"
three = "iii7"
four = "IV7"
five = "V7"
six = "vi7"
seven = "vii7"

TRANSITION_TABLE: dict[str, dict[str, float]] = {
    one: {one: 0, two: 5, three: 3, four: 2, five: 1, six: 6, seven: 0},
    two: {two: 2, two: 0, three: 2, four: 4, five: 8, six: 2, seven: 0},
    three: {one: 2, two: 1, three: 0, four: 4, five: 2, six: 6, seven: 0},
    four: {one: 5, two: 2, three: 1, four: 0, five: 7, six: 2, seven: 0},
    five: {one: 13, two: 1, three: 1, four: 4, five: 0, six: 4, seven: 0},
    six: {one: 1, two: 5, three: 1, four: 2, five: 6, six: 0, seven: 0},
    seven: {one: 4, two: 2, three: 1, four: 3, five: 3, six: 6, seven: 0},
}


def lerp(a, b, proportion):
    return a * (1 - proportion) + b * proportion


def get_mixed_likely_chord(
    current: str,
    mix: float,
    generator: random.Random,
    last_three: list[str | None] | None = None,
) -> str:
    row = TRANSITION_TABLE[current]
    row_mixed = {
        k: (
            lerp(1 - p, p, mix)
            if p != 0 and not (last_three and k == 1 and k in last_three)
            else 0
        )
        for k, p in row.items()
    }
    row_total = sum(row_mixed.values())
    rand_val = generator.random() * row_total
    # print(f"{rand_val}/{row_total}")
    running_total = 0
    for k, v in row_mixed.items():
        # print(f"{k}: {running_total} < {rand_val} < {running_total + v}")
        if running_total < rand_val < running_total + v:
            return k
        else:
            running_total += v
    return list(row_mixed.keys())[-1]


def encode_data(data: list[float]):
    wip_data = data[::10]
    lowest = min(data)
    data_range = max(data) - lowest
    wip_data = [(d - lowest) / data_range for d in wip_data]
    chunked_data = [wip_data[i : i + 10] for i in range(0, len(wip_data), 10)]
    direction_data = [r[0] - r[-1] for r in chunked_data]
    largest_dir = max(map(abs, direction_data))
    scaled_direction = [(d / (largest_dir * 2)) + 5 for d in direction_data]
    print(scaled_direction)

    scale: musicpy.scale_class.scale = mp.scale("C", "major")

    chords_in_order: list[str] = [one]
    last_three: list[str | None] = [None, None, one]

    generator = random.Random(sum(wip_data))

    for i, sd in enumerate(scaled_direction + scaled_direction):
        chords_in_order.append(
            get_mixed_likely_chord(
                chords_in_order[-1], sd, last_three=last_three, generator=generator
            )
        )
        last_three.append(chords_in_order[-1])
        last_three.pop(0)
        print(chords_in_order[-1], end=", ")
        if i >= len(scaled_direction) and chords_in_order[-1] == one:
            break

    print()

    one_chord_notes: list[musicpy.primitives.note] = t.cast(
        musicpy.chord_class.chord, scale.tonic_chord()
    ).notes

    chords = scale.chord_progression(
        chords_in_order, durations=2, intervals=0, merge=False  # type: ignore
    )

    for chord in chords:
        for i, note in enumerate(chord.notes):
            if min(
                map(
                    lambda a: abs(
                        t.cast(musicpy.primitives.note, a.down(12)).degree - note.degree
                    ),
                    one_chord_notes,
                )
            ) > min(map(lambda a: abs(a.degree - note.degree), one_chord_notes)):
                chord[i] = note.down(12)
        chord.set(2, 0.2)

    # flat_chords = list(
    #     itertools.accumulate(
    #         [c.set(2, 0.1) for c in chords], lambda a, b: a | (b, 1 / 2)
    #     )
    # )[-1]
    staggered_chords = list(
        itertools.accumulate(
            [c.set(2, 0.1) for c in chords], lambda a, b: a | (b, 1 / 2)
        )
    )[-1]

    music: musicpy.piece_class.piece = mp.build(
        [staggered_chords, "Synth Bass 2"],
        [staggered_chords, 89],
        bpm=100,
    )
    music.add_volume(50, 1)

    song = mpd.daw(2)
    song.load(0, "./data/GeneralUser-GS.sf2")
    song.load(1, "./data/GeneralUser-GS.sf2")
    print(song.instruments(0).get_current_instrument())
    volume_db = 30
    return pydub.effects.normalize(song.export(music, action="get"))
