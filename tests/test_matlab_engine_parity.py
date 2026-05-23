import shutil
import subprocess
import os
from pathlib import Path

import numpy as np
import pytest
from scipy.io import loadmat

from dark_sectioning.config import DarkMConfig
from dark_sectioning.core.dehaze import dehaze_fast2
from dark_sectioning.core.frequency import separate_hi_lo
from dark_sectioning.core.pipeline import (
    _crop_spatial_padding,
    _normalize_to_255,
    _pad_planes,
    _pad_to_square,
)
from dark_sectioning.core.psf import confirm_block
from dark_sectioning.io import read_tiff_stack


ROOT = Path(__file__).resolve().parents[1]


def _matlab_root() -> Path:
    return Path(os.environ.get("DARK_SECTIONING_MATLAB_ROOT", ROOT))


@pytest.mark.matlab
def test_first_plane_first_pass_matches_matlab_engine(tmp_path: Path) -> None:
    if shutil.which("conda") is None:
        pytest.skip("conda is required to run the matlab_py36 MATLAB Engine environment")

    matlab_root = _matlab_root()
    input_path = matlab_root / "MATLAB_Code" / "input" / "Mousekidney_561nm_1.49NA_65nm.tif"
    if not input_path.exists():
        pytest.skip("upstream MATLAB checkout is not present")

    mat_path = tmp_path / "first_plane.mat"
    script = ROOT / "tests" / "export_matlab_first_plane.py"
    command = [
        "conda",
        "run",
        "-n",
        "matlab_py36",
        "python",
        str(script),
        str(matlab_root),
        str(mat_path),
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    if completed.returncode != 0:
        pytest.skip(
            "MATLAB Engine reference export failed:\n"
            + completed.stdout[-2000:]
            + completed.stderr[-2000:]
        )

    mat = loadmat(mat_path)
    matlab_result = np.asarray(mat["result_crop"], dtype=np.float64)
    matlab_block = int(np.asarray(mat["block_size"]).ravel()[0])

    cfg = DarkMConfig()
    image0 = _normalize_to_255(read_tiff_stack(input_path))
    image0, _, _ = _pad_to_square(image0)
    nx, ny, _ = image0.shape
    image = _pad_planes(image0, nx, ny, cfg.pad_size_divisor, cfg.pad)
    hi, lo, lp, el = separate_hi_lo(image[:, :, 0], cfg, 6.0, cfg.divide)
    block = confirm_block(cfg, lp)
    lo_process = dehaze_fast2(
        lo,
        cfg.omega,
        block,
        el,
        3.0,
        cfg.threshold,
        guided_radius=cfg.guided_radius,
        guided_eps=cfg.guided_eps,
        min_transmission=cfg.min_transmission,
    )
    python_result = _crop_spatial_padding(lo_process + hi, nx, ny, cfg.pad_size_divisor)

    assert block == matlab_block
    np.testing.assert_allclose(python_result, matlab_result, rtol=0, atol=1e-8)
