from pathlib import Path

import numpy as np
import pytest

from dark_sectioning import dark_section
from dark_sectioning.io import read_tiff_stack


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "MATLAB_Code" / "input" / "Mousekidney_561nm_1.49NA_65nm.tif"
EXPECTED = ROOT / "MATLAB_Code" / "output" / "Dark.tif"


def _pearson(a: np.ndarray, b: np.ndarray) -> float:
    af = a.astype(np.float64).ravel()
    bf = b.astype(np.float64).ravel()
    return float(np.corrcoef(af, bf)[0, 1])


@pytest.mark.slow
def test_bundled_darkm_output_shape_and_metrics() -> None:
    source = read_tiff_stack(INPUT)
    expected = read_tiff_stack(EXPECTED)

    result = dark_section(source)
    diff = result.astype(np.int64) - expected.astype(np.int64)

    assert result.shape == expected.shape
    assert result.dtype == np.uint16
    assert expected.shape == (512, 512, 31)
    assert _pearson(result, expected) >= 0.999
    assert float(np.mean(np.abs(diff))) <= 200.0

