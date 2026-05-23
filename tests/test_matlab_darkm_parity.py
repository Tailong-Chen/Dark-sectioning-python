from pathlib import Path
import os

import numpy as np
import pytest

from dark_sectioning.io import read_tiff_stack


ROOT = Path(__file__).resolve().parents[1]


def _matlab_root() -> Path:
    return Path(os.environ.get("DARK_SECTIONING_MATLAB_ROOT", ROOT))


def test_bundled_input_and_historical_output_shapes() -> None:
    matlab_root = _matlab_root()
    input_path = matlab_root / "MATLAB_Code" / "input" / "Mousekidney_561nm_1.49NA_65nm.tif"
    historical_path = matlab_root / "MATLAB_Code" / "output" / "Dark.tif"
    if not input_path.exists() or not historical_path.exists():
        pytest.skip("upstream MATLAB fixtures are not present")

    source = read_tiff_stack(input_path)
    historical = read_tiff_stack(historical_path)

    assert source.shape == (512, 512, 31)
    assert source.dtype == np.uint8
    assert historical.shape == (512, 512, 31)
    assert historical.dtype == np.uint16
