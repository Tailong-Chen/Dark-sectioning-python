"""Command-line interface for Python Dark-sectioning."""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from .api import dark_section
from .io import read_tiff_stack, write_tiff_stack


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dark-section",
        description="Run the MATLAB_Code/Dark.m-compatible Dark-sectioning pipeline.",
    )
    parser.add_argument("input", type=Path, help="Input TIFF stack.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output TIFF stack. Defaults to <input_stem>_Dark.tif.",
    )
    parser.add_argument("--emission-wavelength", type=float, default=610.0)
    parser.add_argument("--na", type=float, default=1.49)
    parser.add_argument("--pixel-size", type=float, default=65.0)
    parser.add_argument("--factor", type=float, default=2.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    output = args.output
    if output is None:
        output = args.input.with_name(f"{args.input.stem}_Dark.tif")

    start = time.perf_counter()
    stack = read_tiff_stack(args.input)
    result = dark_section(
        stack,
        emission_wavelength_nm=args.emission_wavelength,
        na=args.na,
        pixel_size_nm=args.pixel_size,
        factor=args.factor,
    )
    write_tiff_stack(output, result)
    elapsed = time.perf_counter() - start

    print(f"input={args.input}")
    print(f"output={output}")
    print(f"input_shape={stack.shape}")
    print(f"output_shape={result.shape}")
    print(f"output_dtype={result.dtype}")
    print(f"elapsed_seconds={elapsed:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

