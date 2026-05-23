"""PSF and block-size helpers ported from MATLAB_Code/helpfunctions."""

from __future__ import annotations

import numpy as np
from scipy import special

from dark_sectioning.config import DarkMConfig


def psf_generator(
    wavelength_nm: float, pixel_size_nm: float, na: float, width: int, factor: float
) -> np.ndarray:
    coords = np.linspace(0, width - 1, width, dtype=np.float64)
    x, y = np.meshgrid(coords, coords)
    scale = 2.0 * np.pi * na / wavelength_nm * pixel_size_nm
    scale *= factor
    radius = np.sqrt(np.minimum(x, np.abs(x - width)) ** 2 + np.minimum(y, np.abs(y - width)) ** 2)
    z = scale * radius + np.finfo(np.float64).eps
    psf = np.abs(2.0 * special.j1(z) / z) ** 2
    psf /= np.sum(psf)
    return np.fft.fftshift(psf)


def confirm_block(config: DarkMConfig, lp: np.ndarray) -> int:
    psf = psf_generator(
        config.emission_wavelength_nm,
        config.pixel_size_nm,
        config.na,
        lp.shape[0],
        config.factor,
    )
    psf_lo = np.abs(np.fft.ifft2(np.fft.fftshift(np.fft.fft2(psf)) * np.fft.fftshift(lp)))
    psf_lo = psf_lo / np.max(psf_lo)
    half = int(np.floor(lp.shape[0] / 2))
    count_x = half
    for idx in range(half - 1, lp.shape[0]):
        count_x = idx + 1
        if psf_lo[idx, half - 1] < 0.01:
            break
    return int(count_x - half)

