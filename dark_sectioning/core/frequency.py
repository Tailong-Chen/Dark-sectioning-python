"""Frequency-domain helpers ported from MATLAB_Code/helpfunctions/separateHiLo.m."""

from __future__ import annotations

import numpy as np

from dark_sectioning.config import DarkMConfig


def lpgauss(height: int, width: int, sigma: float) -> np.ndarray:
    h = float(height)
    w = float(width)
    kcx = sigma
    kcy = (h / w) * sigma
    x = np.arange(-np.floor(w / 2), np.floor((w - 1) / 2) + 1, dtype=np.float64)
    y = np.arange(-np.floor(h / 2), np.floor((h - 1) / 2) + 1, dtype=np.float64)
    xx, yy = np.meshgrid(x, y)
    temp = -((xx**2) / (kcx**2) + (yy**2) / (kcy**2))
    return np.fft.ifftshift(np.exp(temp))


def hpgauss(height: int, width: int, sigma: float) -> np.ndarray:
    return 1.0 - lpgauss(height, width, sigma)


def separate_hi_lo(
    image: np.ndarray, config: DarkMConfig, deg: float, divide: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    nx, ny = image.shape
    resolution = 0.5 * config.emission_wavelength_nm / config.na / config.factor
    k_m = ny / (resolution / config.pixel_size_nm)
    kc = np.floor(k_m * 0.2)
    sigma_lp = kc * 2.0 / 2.355

    lp = lpgauss(nx, ny, sigma_lp * 2.0 * divide)
    hp = hpgauss(nx, ny, sigma_lp * 2.0 * divide)
    elp = lpgauss(nx, ny, sigma_lp / deg)

    fft_image = np.fft.fftshift(np.fft.fft2(image))
    hi = np.real(np.fft.ifft2(np.fft.ifftshift(fft_image * np.fft.fftshift(hp))))
    lo = np.real(np.fft.ifft2(np.fft.ifftshift(fft_image * np.fft.fftshift(lp))))
    el = np.real(np.fft.ifft2(np.fft.fft2(image) * elp))
    return hi, lo, lp, el

