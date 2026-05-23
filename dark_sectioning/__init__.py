"""Python port of the MATLAB_Code/Dark.m Dark-sectioning workflow."""

from .api import dark_section
from .config import DarkMConfig
from .io import read_tiff_stack, write_tiff_stack

__all__ = ["DarkMConfig", "dark_section", "read_tiff_stack", "write_tiff_stack"]

