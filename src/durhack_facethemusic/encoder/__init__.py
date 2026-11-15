import pydub
import typing as t

from . import encode, dummy_encoder, stupid_encoder, markov_chain_encoder, decoding

all_encoders: dict[str, t.Callable[[list[float]], pydub.AudioSegment]] = {
    "harry": encode.encode_data,
    "dummy": dummy_encoder.encode_data,
    "stupid": stupid_encoder.encode_data,
    "markov": markov_chain_encoder.encode_data,
    "decoding": decoding.encode_data,
}
