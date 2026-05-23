import numpy as np

from dark_sectioning.config import DarkMConfig
from dark_sectioning.core.dark_channel import dark_channel
from dark_sectioning.core.frequency import hpgauss, lpgauss, separate_hi_lo
from dark_sectioning.core.guided_filter import guided_filter, window_sum_filter
from dark_sectioning.core.psf import confirm_block, psf_generator


def test_dark_channel_matches_inf_padded_window_minimum() -> None:
    image = np.array(
        [
            [5.0, 4.0, 3.0],
            [6.0, 1.0, 2.0],
            [7.0, 8.0, 9.0],
        ]
    )

    result = dark_channel(image, 3)

    expected = np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0],
        ]
    )
    np.testing.assert_array_equal(result, expected)


def test_window_sum_filter_matches_hand_computed_center_value() -> None:
    image = np.arange(1, 26, dtype=np.float64).reshape(5, 5)

    result = window_sum_filter(image, 1)

    assert result[2, 2] == np.sum(image[1:4, 1:4])
    assert result[0, 0] == np.sum(image[0:2, 0:2])


def test_guided_filter_shape_and_finite_values() -> None:
    image = np.arange(100, dtype=np.float64).reshape(10, 10)
    target = image / 100.0

    result = guided_filter(image, target, radius=1, eps=0.001)

    assert result.shape == image.shape
    assert np.isfinite(result).all()


def test_frequency_filters_have_expected_range() -> None:
    lp = lpgauss(8, 8, 2.0)
    hp = hpgauss(8, 8, 2.0)

    assert lp.shape == (8, 8)
    assert hp.shape == (8, 8)
    np.testing.assert_allclose(lp + hp, 1.0)
    assert np.max(lp) <= 1.0
    assert np.min(lp) >= 0.0


def test_separate_hi_lo_returns_matching_shapes() -> None:
    image = np.arange(64, dtype=np.float64).reshape(8, 8)

    hi, lo, lp, el = separate_hi_lo(image, DarkMConfig(), deg=6.0, divide=0.5)

    assert hi.shape == image.shape
    assert lo.shape == image.shape
    assert lp.shape == image.shape
    assert el.shape == image.shape


def test_psf_generator_is_normalized() -> None:
    psf = psf_generator(610.0, 65.0, 1.49, 32, 2.0)

    assert psf.shape == (32, 32)
    np.testing.assert_allclose(np.sum(psf), 1.0)


def test_confirm_block_returns_positive_integer() -> None:
    cfg = DarkMConfig()
    lp = lpgauss(64, 64, 4.0)

    block = confirm_block(cfg, lp)

    assert isinstance(block, int)
    assert block > 0

