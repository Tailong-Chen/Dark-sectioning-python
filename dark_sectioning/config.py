"""Configuration values matching MATLAB_Code/Dark.m."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class DarkMConfig:
    """Constants for the MATLAB_Code/Dark.m compatibility target."""

    emission_wavelength_nm: float = 610.0
    na: float = 1.49
    pixel_size_nm: float = 65.0
    factor: float = 2.0
    background: int = 1
    pad: bool = True
    denoise: bool = False
    threshold: float = 70.0
    divide: float = 0.5
    pad_size_divisor: int = 15
    maxtime: int = 2
    deg_matrix: Tuple[float, ...] = (6.0, 3.0, 1.2)
    dep_matrix: Tuple[float, ...] = (3.0, 3.0, 2.0)
    hl_matrix: Tuple[float, ...] = (1.0, 1.0, 1.0)
    omega: float = 0.95
    guided_radius: int = 15
    guided_eps: float = 0.001
    min_transmission: float = 0.1

    def with_microscope(
        self,
        *,
        emission_wavelength_nm: float | None = None,
        na: float | None = None,
        pixel_size_nm: float | None = None,
        factor: float | None = None,
    ) -> "DarkMConfig":
        return DarkMConfig(
            emission_wavelength_nm=self.emission_wavelength_nm
            if emission_wavelength_nm is None
            else emission_wavelength_nm,
            na=self.na if na is None else na,
            pixel_size_nm=self.pixel_size_nm if pixel_size_nm is None else pixel_size_nm,
            factor=self.factor if factor is None else factor,
        )

