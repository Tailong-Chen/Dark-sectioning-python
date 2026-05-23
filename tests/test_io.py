from pathlib import Path

import numpy as np

from dark_sectioning.io import read_tiff_stack, write_tiff_stack


def test_tiff_round_trip_preserves_matlab_stack_shape(tmp_path: Path) -> None:
    stack = np.arange(4 * 5 * 3, dtype=np.uint16).reshape(4, 5, 3)
    path = tmp_path / "stack.tif"

    write_tiff_stack(path, stack)
    loaded = read_tiff_stack(path)

    assert loaded.shape == stack.shape
    assert loaded.dtype == stack.dtype
    np.testing.assert_array_equal(loaded, stack)

