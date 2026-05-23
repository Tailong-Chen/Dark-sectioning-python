# Dark-sectioning Python

Python library and command-line interface for the Dark-sectioning workflow from
`MATLAB_Code/Dark.m` in the upstream Dark-sectioning project.

This repository is intentionally Python-only. The original MATLAB application,
MATLAB scripts, Fiji/ImageJ plugin artifacts, example TIFF stacks, and packaged
executables are not included here.

## Provenance

Dark-sectioning was introduced with the Nature Methods article "Dark-based
Optical Sectioning assists Background Removal in Fluorescence Microscopy":

<https://www.nature.com/articles/s41592-025-02667-6>

The upstream README names Ruijie Cao and Prof. Peng Xi at Peking University as
the original authors and states that the project uses an Apache license for
Dark-sectioning. See `NOTICE.md` for the preserved provenance notes.

This Python port targets only the behavior of upstream `MATLAB_Code/Dark.m`.
It does not implement compatibility modes for `MATLAB_Simplified_Fun`, the
MATLAB App, or the Fiji/ImageJ plugin.

## Install

```bash
python -m pip install -e ".[test]"
```

## CLI Usage

```bash
dark-section input.tif --output output_dark.tif
```

If `--output` is omitted, the CLI writes `<input_stem>_Dark.tif`.

## Python API

```python
from dark_sectioning import dark_section, read_tiff_stack, write_tiff_stack

stack = read_tiff_stack("input.tif")
result = dark_section(stack)
write_tiff_stack("output_dark.tif", result)
```

The default constants match upstream `MATLAB_Code/Dark.m`:

- `background=1`
- `thres=70`
- `pad_size=15`
- `maxtime=2`
- `NA=1.49`
- `emwavelength=610`
- `pixelsize=65`
- `factor=2`

## Tests

Run the default Python test suite:

```bash
python -m pytest -q
```

MATLAB Engine parity tests are optional. To run them, keep a separate checkout
of the upstream MATLAB repository and point the test suite at it:

```bash
export DARK_SECTIONING_MATLAB_ROOT=/path/to/upstream/Dark-sectioning
python -m pytest tests/test_matlab_engine_parity.py -q
```

The local development environment used for this port verified a full CLI output
against a live MATLAB Engine execution of upstream `MATLAB_Code/Dark.m` with:

- mean absolute error: `0.0`
- max absolute error: `0`
- correlation: `0.9999999999999998`

## Notes

The historical upstream file `MATLAB_Code/output/Dark.tif` was not used as the
final authority because it did not exactly match a fresh MATLAB Engine run of
the current upstream `MATLAB_Code/Dark.m`. Live MATLAB execution of that script
is the compatibility target.
