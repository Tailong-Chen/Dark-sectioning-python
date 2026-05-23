"""Full pipeline matching MATLAB_Code/Dark.m."""

from __future__ import annotations

import numpy as np

from dark_sectioning.config import DarkMConfig

from .dehaze import dehaze_fast2
from .frequency import separate_hi_lo
from .psf import confirm_block


def _normalize_to_255(stack: np.ndarray) -> np.ndarray:
    arr = np.asarray(stack, dtype=np.float64)
    min_val = np.min(arr)
    max_val = np.max(arr)
    if max_val == min_val:
        return np.zeros(arr.shape, dtype=np.float64)
    return 255.0 * (arr - min_val) / (max_val - min_val)


def _ensure_stack(stack: np.ndarray) -> np.ndarray:
    arr = np.asarray(stack)
    if arr.ndim == 2:
        arr = arr[:, :, np.newaxis]
    if arr.ndim != 3:
        raise ValueError(f"Expected 2D or 3D image stack, got shape {arr.shape!r}")
    return arr


def _pad_to_square(image0: np.ndarray) -> tuple[np.ndarray, int, int]:
    nx0, ny0, _ = image0.shape
    nx, ny = nx0, ny0
    if ny > nx:
        pad_rows = ny - nx
        image0 = np.pad(image0, ((0, pad_rows), (0, 0), (0, 0)), mode="constant")
    elif ny < nx:
        pad_cols = nx - ny
        image0 = np.pad(image0, ((0, 0), (0, pad_cols), (0, 0)), mode="constant")
    return image0, nx0, ny0


def _pad_planes(image0: np.ndarray, nx: int, ny: int, divisor: int, symmetric: bool) -> np.ndarray:
    pad_x = int(np.floor(nx / divisor) + 1)
    pad_y = int(np.floor(ny / divisor) + 1)
    mode = "symmetric" if symmetric else "constant"
    padded = [
        np.pad(image0[:, :, plane], ((pad_x, pad_x), (pad_y, pad_y)), mode=mode)
        for plane in range(image0.shape[2])
    ]
    return np.stack(padded, axis=2)


def _crop_spatial_padding(image: np.ndarray, nx: int, ny: int, divisor: int) -> np.ndarray:
    pad_x = int(np.floor(nx / divisor) + 1)
    pad_y = int(np.floor(ny / divisor) + 1)
    return image[pad_x : pad_x + nx, pad_y : pad_y + ny]


def _matlab_uint16(values: np.ndarray) -> np.ndarray:
    rounded = np.floor(values + 0.5)
    return np.clip(rounded, 0, np.iinfo(np.uint16).max).astype(np.uint16)


def dark_section_darkm(stack: np.ndarray, *, config: DarkMConfig | None = None) -> np.ndarray:
    """Run the MATLAB_Code/Dark.m-compatible two-pass severe-background pipeline."""

    cfg = DarkMConfig() if config is None else config
    image0 = _normalize_to_255(_ensure_stack(stack))
    image0, nx0, ny0 = _pad_to_square(image0)
    nx, ny, nz = image0.shape

    result_stack = np.zeros((nx, ny, nz), dtype=np.float64)
    image = _pad_planes(image0, nx, ny, cfg.pad_size_divisor, cfg.pad)

    for time_idx in range(cfg.maxtime):
        deg = cfg.deg_matrix[time_idx]
        dep = cfg.dep_matrix[time_idx]
        hl = cfg.hl_matrix[cfg.maxtime - 1]
        for z_idx in range(nz):
            plane = np.squeeze(image[:, :, z_idx])
            hi, lo, lp, el = separate_hi_lo(plane, cfg, deg, cfg.divide)
            block_size = confirm_block(cfg, lp)
            lo_process = dehaze_fast2(
                lo,
                cfg.omega,
                block_size,
                el,
                dep,
                cfg.threshold,
                guided_radius=cfg.guided_radius,
                guided_eps=cfg.guided_eps,
                min_transmission=cfg.min_transmission,
            )
            result = lo_process / hl + hi
            result_stack[:, :, z_idx] = _crop_spatial_padding(
                result, nx, ny, cfg.pad_size_divisor
            )

        image0 = result_stack
        image = _pad_planes(image0, nx, ny, cfg.pad_size_divisor, cfg.pad)

    result_final = np.zeros((nx, ny, nz), dtype=np.float64)
    for z_idx in range(nz):
        temp = np.pad(
            result_stack[:, :, z_idx],
            (
                (int(np.floor(nx / cfg.pad_size_divisor) + 1),) * 2,
                (int(np.floor(ny / cfg.pad_size_divisor) + 1),) * 2,
            ),
            mode="symmetric" if cfg.pad else "constant",
        )
        result_final[:, :, z_idx] = _crop_spatial_padding(temp, nx, ny, cfg.pad_size_divisor)

    # Preserve MATLAB_Code/Dark.m's crop behavior, including its rectangular-image
    # column-crop condition, because Dark.m is the sole v1 compatibility target.
    if nx0 != nx or ny0 != ny:
        if nx > nx0:
            result_final = result_final[:nx0, :, :]
        if ny0 > ny:
            result_final = result_final[:, :ny0, :]

    max_val = np.max(result_final)
    if max_val == 0:
        return np.zeros(result_final.shape, dtype=np.uint16)
    return _matlab_uint16(65535.0 * result_final / max_val)

