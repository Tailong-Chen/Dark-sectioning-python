import numpy as np

from dark_sectioning import dark_section
from dark_sectioning.core.pipeline import _matlab_uint16


def test_matlab_uint16_rounds_and_clips_positive_values() -> None:
    values = np.array([-1.0, 0.49, 0.5, 1.49, 1.5, 65536.0])

    result = _matlab_uint16(values)

    np.testing.assert_array_equal(
        result,
        np.array([0, 0, 1, 1, 2, 65535], dtype=np.uint16),
    )


def test_dark_section_tiny_stack_completes() -> None:
    y, x = np.mgrid[:48, :48]
    base = np.exp(-((x - 24) ** 2 + (y - 24) ** 2) / 80.0)
    stack = np.stack([base * 1000, base * 800 + 20], axis=2).astype(np.float64)

    result = dark_section(stack)

    assert result.shape == stack.shape
    assert result.dtype == np.uint16
    assert result.max() > 0

