"""Guided-filter helpers ported from MATLAB_Code/helpfunctions."""

from __future__ import annotations

import numpy as np


def window_sum_filter(image: np.ndarray, radius: int) -> np.ndarray:
    arr = np.asarray(image, dtype=np.float64)
    h, w = arr.shape
    r = int(radius)
    if r < 0:
        raise ValueError("radius must be nonnegative")
    if r == 0:
        return arr.copy()
    if h <= 2 * r + 1 or w <= 2 * r + 1:
        raise ValueError("image is too small for the MATLAB window_sum_filter radius")

    sum_img = np.zeros_like(arr, dtype=np.float64)
    im_cum = np.cumsum(arr, axis=0)
    sum_img[: r + 1, :] = im_cum[r : 2 * r + 1, :]
    sum_img[r + 1 : h - r, :] = im_cum[2 * r + 1 : h, :] - im_cum[: h - 2 * r - 1, :]
    sum_img[h - r : h, :] = im_cum[h - 1, :][np.newaxis, :] - im_cum[
        h - 2 * r - 1 : h - r - 1, :
    ]

    im_cum = np.cumsum(sum_img, axis=1)
    sum_img[:, : r + 1] = im_cum[:, r : 2 * r + 1]
    sum_img[:, r + 1 : w - r] = im_cum[:, 2 * r + 1 : w] - im_cum[:, : w - 2 * r - 1]
    sum_img[:, w - r : w] = im_cum[:, w - 1][:, np.newaxis] - im_cum[
        :, w - 2 * r - 1 : w - r - 1
    ]
    return sum_img


def guided_filter(guide: np.ndarray, target: np.ndarray, radius: int, eps: float) -> np.ndarray:
    g = np.asarray(guide, dtype=np.float64)
    t = np.asarray(target, dtype=np.float64)
    if g.shape != t.shape:
        raise ValueError(f"guide and target must have same shape, got {g.shape!r} and {t.shape!r}")

    avg_denom = window_sum_filter(np.ones(g.shape, dtype=np.float64), radius)
    mean_g = window_sum_filter(g, radius) / avg_denom
    mean_t = window_sum_filter(t, radius) / avg_denom
    corr_gg = window_sum_filter(g * g, radius) / avg_denom
    corr_gt = window_sum_filter(g * t, radius) / avg_denom

    var_g = corr_gg - mean_g * mean_g
    cov_gt = corr_gt - mean_g * mean_t
    a = cov_gt / (var_g + eps)
    b = mean_t - a * mean_g

    mean_a = window_sum_filter(a, radius) / avg_denom
    mean_b = window_sum_filter(b, radius) / avg_denom
    return mean_a * g + mean_b

