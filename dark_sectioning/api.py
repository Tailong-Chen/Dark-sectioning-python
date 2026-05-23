"""Public API for the Dark.m-compatible pipeline."""

from __future__ import annotations

import numpy as np

from .config import DarkMConfig
from .core.pipeline import dark_section_darkm


def dark_section(
    stack: np.ndarray,
    *,
    emission_wavelength_nm: float = 610.0,
    na: float = 1.49,
    pixel_size_nm: float = 65.0,
    factor: float = 2.0,
) -> np.ndarray:
    """Run the Python port of ``MATLAB_Code/Dark.m`` on a 3D image stack."""

    config = DarkMConfig().with_microscope(
        emission_wavelength_nm=emission_wavelength_nm,
        na=na,
        pixel_size_nm=pixel_size_nm,
        factor=factor,
    )
    return dark_section_darkm(stack, config=config)

