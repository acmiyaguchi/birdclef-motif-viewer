import io
from typing import Tuple

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from simple import simple_fast


def load_audio_bytes(data: bytes, sr: int = None) -> Tuple[np.ndarray, int]:
    return librosa.load(io.BytesIO(data), sr=sr)


def plot_melspectogram(
    y: np.ndarray,
    sr: int = 32000,
    n_fft: int = 2048,
    hop_length: int = 80,
    n_mels: int = 16,
    mp_window: int = 80 * 5,
    log_scaled=True,
    offset: float = 0,
    length: float = -1,
) -> bytes:
    start = int(offset * sr)
    end = -1 if length < 0 else start + int(length * sr)
    S = librosa.feature.melspectrogram(
        y=y[start:end], sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels
    )
    if log_scaled:
        S = librosa.power_to_db(S, ref=np.max)
    mp, _ = simple_fast(S, S, mp_window)

    fig, ax = plt.subplots(
        nrows=2, ncols=1, sharex=False, sharey=False, figsize=(7.5, 5)
    )
    librosa.display.specshow(
        S,
        x_axis="time",
        y_axis="mel",
        sr=sr,
        hop_length=hop_length,
        ax=ax[0],
    )
    ax[0].set(title="Mel-frequency spectrogram")

    # plot the matrix profile mp on the second axis
    ax[1].plot(mp)
    ax[1].set(
        title="Similarity matrix profile (SiMPle)",
        ylabel="distance to nearest neighbor",
    )
    plt.tight_layout()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()
