from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from dark_sectioning.io import read_tiff_stack


def compare(expected_path: Path, actual_path: Path) -> dict[str, object]:
    expected = read_tiff_stack(expected_path)
    actual = read_tiff_stack(actual_path)
    if expected.shape != actual.shape:
        raise ValueError(f"shape mismatch: expected {expected.shape}, actual {actual.shape}")

    diff = actual.astype(np.int64) - expected.astype(np.int64)
    expected_f = expected.astype(np.float64).ravel()
    actual_f = actual.astype(np.float64).ravel()
    pearson = float(np.corrcoef(expected_f, actual_f)[0, 1])
    return {
        "expected": str(expected_path),
        "actual": str(actual_path),
        "shape": actual.shape,
        "dtype": str(actual.dtype),
        "pearson": pearson,
        "mean_abs_error": float(np.mean(np.abs(diff))),
        "max_abs_error": int(np.max(np.abs(diff))),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    args = parser.parse_args()
    print(json.dumps(compare(args.expected, args.actual), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

