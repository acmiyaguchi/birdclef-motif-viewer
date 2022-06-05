import librosa
import numpy as np
import pytest
import soundfile as sf

from api.spectrogram import load_audio_bytes


@pytest.fixture
def sr():
    return 32000


@pytest.fixture
def chirp(tmp_path, sr):
    chirp = librosa.chirp(sr=sr, fmin=110, fmax=110 * 64, duration=10)
    path = tmp_path / "chirp.ogg"
    sf.write(path.as_posix(), chirp, sr, format="ogg", subtype="vorbis")
    yield path


def test_load_audio_bytes(sr, chirp):
    data = chirp.read_bytes()
    y, sr = load_audio_bytes(data, sr)
    assert sr == sr
    assert y.shape == (10 * sr,)
