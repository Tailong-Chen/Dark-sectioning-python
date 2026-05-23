This is the official code for the article "Dark-based Optical Sectioning assists Background Removal in Fluorescence Microscopy" in Nature Methods.
https://www.nature.com/articles/s41592-025-02667-6. If you find our method works, please cite our work~

Dark sectioning aims at remove the scattering background in fluorescence images based on dark channel priority and dual frequency seperation.
This code is finished by Ruijie Cao and Prof. Peng Xi in Peking University. We claim an Apache liscence for Dark sectioning.

If you have any questions, please contact caoruijie@stu.pku.edu.cn or xipeng@pku.edu.cn

Update in 2025.06.12: Someone reflects that in MATLAB 2024 or later, the nearset function is wrong. This is because the "nearest" function changed in 2024 version. We have changed it into "floor" function.

Update in 2025.04.04：The imagej version of Dark sectioning has been finished! You can download the Dark-0.1.0-SNAPSHOT(5).jar file and put it into the "plugin" file in Fiji, and it's easy to use!

Update in 2025.05.15：We make the guide video in figshare to guide the use of Fiji and Exe users: https://figshare.com/articles/dataset/Dark-sectioning/24607614

Update in 2025.05.15：We upload the simplified function of Dark sectioning for intergrate into your own algorithm!

Update in 2025.10.12：We correct the two bugs in the Fiji plugin, the new version can deal with rectangle-shaped image with high dynamic range rendering!

## Python library and CLI port

This repository now includes a Python port intended for research batch workflows.
The Python implementation targets `MATLAB_Code/Dark.m` only. It does not try to
match `MATLAB_Simplified_Fun`, the MATLAB App, or the Fiji/ImageJ plugin.

Install locally:

```bash
python -m pip install -e ".[test]"
```

Run the CLI:

```bash
dark-section MATLAB_Code/input/Mousekidney_561nm_1.49NA_65nm.tif --output /tmp/dark_python.tif
```

Use the API:

```python
from dark_sectioning import dark_section, read_tiff_stack, write_tiff_stack

stack = read_tiff_stack("MATLAB_Code/input/Mousekidney_561nm_1.49NA_65nm.tif")
result = dark_section(stack)
write_tiff_stack("/tmp/dark_python.tif", result)
```

The default Python constants are the constants hard-coded in `MATLAB_Code/Dark.m`:
`background=1`, `thres=70`, `pad_size=15`, `maxtime=2`, `NA=1.49`,
`emwavelength=610`, `pixelsize=65`, and `factor=2`.

The file `MATLAB_Code/output/Dark.tif` is retained as a historical upstream
artifact. Current parity testing treats live MATLAB execution of
`MATLAB_Code/Dark.m` as authoritative; in this checkout, the historical output
does not exactly match a fresh MATLAB Engine run of the current script.

See `NOTICE.md` for provenance and copyright notes.
