"""Dehaze helpers ported from MATLAB_Code/helpfunctions."""

from __future__ import annotations

import numpy as np

from .dark_channel import dark_channel
from .guided_filter import guided_filter


def get_atmosphere(image: np.ndarray, dark: np.ndarray) -> float:
    arr = np.asarray(image, dtype=np.float64)
    dark_vec = np.reshape(dark, (-1,), order="F")
    image_vec = np.reshape(arr, (-1,), order="F")
    n_search_pixels = int(np.floor(arr.shape[0] * arr.shape[1] * 0.01))
    n_search_pixels = max(n_search_pixels, 1)
    indices = np.argsort(-dark_vec, kind="stable")[:n_search_pixels]
    return float(np.sum(image_vec[indices]) / n_search_pixels)


def get_transmission_estimate(
    rep_atmosphere: np.ndarray, image: np.ndarray, omega: float, win_size: int
) -> np.ndarray:
    return 1.0 - omega * dark_channel(image / rep_atmosphere, win_size)


def get_radiance(
    rep_atmosphere: np.ndarray, image: np.ndarray, transmission: np.ndarray, min_transmission: float
) -> np.ndarray:
    max_transmission = np.maximum(transmission, min_transmission)
    return ((image - rep_atmosphere) / max_transmission) + rep_atmosphere


def dehaze_fast2(
    image: np.ndarray,
    omega: float,
    win_size: int,
    el: np.ndarray,
    dep: float,
    threshold: float,
    *,
    guided_radius: int = 15,
    guided_eps: float = 0.001,
    min_transmission: float = 0.1,
) -> np.ndarray:
    arr = np.asarray(image, dtype=np.float64)
    mask = np.zeros(arr.shape, dtype=np.float64)
    mask[arr < threshold] = 1.0

    masked = arr * mask
    min_atmosphere = get_atmosphere(masked, dark_channel(masked, win_size))
    max_atmosphere = get_atmosphere(arr, dark_channel(arr, win_size))

    el_norm = el - np.min(el)
    el_max = np.max(el_norm)
    if el_max == 0:
        rep_atmosphere_process = np.full(arr.shape, min_atmosphere, dtype=np.float64)
    else:
        rep_atmosphere_process = el_norm / el_max * (max_atmosphere - min_atmosphere) + min_atmosphere
    rep_atmosphere_process = dep * rep_atmosphere_process

    trans_est = get_transmission_estimate(rep_atmosphere_process, arr, omega, win_size)
    transmission = guided_filter(arr, trans_est, guided_radius, guided_eps)
    return get_radiance(rep_atmosphere_process, arr, transmission, min_transmission)

