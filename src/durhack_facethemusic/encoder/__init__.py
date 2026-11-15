import pydub
import typing as t

from . import encode, dummy_encoder, elle_encoder

all_encoders: dict[str, t.Callable[[list[float]], pydub.AudioSegment]] = {
    "harry": encode.encode_data,
    "dummy": dummy_encoder.encode_data,
    "elle": elle_encoder.encode_data,
}
