from pathlib import Path

import numpy as np

from dark_sectioning.io import read_tiff_stack


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "MATLAB_Code" / "input" / "Mousekidney_561nm_1.49NA_65nm.tif"
HISTORICAL_OUTPUT = ROOT / "MATLAB_Code" / "output" / "Dark.tif"


def test_bundled_input_and_historical_output_shapes() -> None:
    source = read_tiff_stack(INPUT)
    historical = read_tiff_stack(HISTORICAL_OUTPUT)

    assert source.shape == (512, 512, 31)
    assert source.dtype == np.uint8
    assert historical.shape == (512, 512, 31)
    assert historical.dtype == np.uint16
