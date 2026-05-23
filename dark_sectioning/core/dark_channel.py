"""Dark-channel minimum filter."""

from __future__ import annotations

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def dark_channel(image: np.ndarray, win_size: int) -> np.ndarray:
    arr = np.asarray(image, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError(f"dark_channel expects a 2D image, got shape {arr.shape!r}")
    if win_size < 1:
        raise ValueError("win_size must be positive")

    rows, cols = arr.shape
    pad_size = int(np.floor(win_size / 2))
    padded = np.pad(
        arr,
        ((pad_size, pad_size), (pad_size, pad_size)),
        mode="constant",
        constant_values=np.inf,
    )
    windows = sliding_window_view(padded, (win_size, win_size))
    return windows[:rows, :cols].min(axis=(-2, -1))

