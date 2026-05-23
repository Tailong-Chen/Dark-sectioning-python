"""TIFF stack I/O helpers."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import tifffile


def read_tiff_stack(path: str | Path) -> np.ndarray:
    """Read a TIFF as a MATLAB-style stack with shape ``(rows, cols, planes)``."""

    data = tifffile.imread(str(path))
    arr = np.asarray(data)
    if arr.ndim == 2:
        return arr[:, :, np.newaxis]
    if arr.ndim != 3:
        raise ValueError(f"Expected 2D or 3D TIFF stack, got shape {arr.shape!r}")

    # tifffile usually returns multi-page grayscale TIFFs as (planes, rows, cols).
    # MATLAB uses (rows, cols, planes), so move the shortest page axis to the end.
    if arr.shape[0] <= arr.shape[1] and arr.shape[0] <= arr.shape[2]:
        return np.moveaxis(arr, 0, -1)
    return arr


def write_tiff_stack(path: str | Path, stack: np.ndarray) -> None:
    """Write a MATLAB-style ``(rows, cols, planes)`` stack as a multi-page TIFF."""

    arr = np.asarray(stack)
    if arr.ndim == 2:
        out = arr[np.newaxis, :, :]
    elif arr.ndim == 3:
        out = np.moveaxis(arr, -1, 0)
    else:
        raise ValueError(f"Expected 2D or 3D stack, got shape {arr.shape!r}")

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tifffile.imwrite(str(path), out, photometric="minisblack")

