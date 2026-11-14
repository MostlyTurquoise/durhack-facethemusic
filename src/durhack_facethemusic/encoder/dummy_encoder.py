import musicpy as mp
import pydub


def encode_data(_: list[float]) -> pydub.AudioSegment:
    return pydub.AudioSegment.from_wav("./dummy.wav")
