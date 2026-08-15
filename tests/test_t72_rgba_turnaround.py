"""T72 - rgba_turnaround.py: alpha is the geometry silhouette, exactly.

WHAT THIS PINS. E37 requirement 4 says the turnarounds carry REAL alpha, sourced from the
raycast silhouettes rather than keyed from pixels. The property is exactness, not closeness,
so the test asserts identity against the mask and constructs the discriminating cases for
every ANDON the tool carries.

ASK OF EVERY FIXTURE: what would this look like if the code were wrong in the specific way
this check exists to catch? The flat-255 defect is the named failure (E36 task 0 measured
this route's turn renders at alpha 255 across the whole frame), so `test_flat_255_is_caught`
builds a fully-opaque mask and requires the tool to REFUSE - a check that cannot fail is not
a check.

Hermetic: synthetic arrays only, no recorded tree, no Blender, no GPU.
"""
import os
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

TOOL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "tools", "rgba_turnaround.py")
sys.path.insert(0, os.path.dirname(TOOL))
import rgba_turnaround  # noqa: E402


def _write(tmp, name, arr, mode):
    p = os.path.join(tmp, name)
    Image.fromarray(arr, mode=mode).save(p)
    return p


def _rgb(h=16, w=8):
    return (np.arange(h * w * 3, dtype=np.uint8).reshape(h, w, 3) % 251)


def _mask(h=16, w=8, on=None):
    m = np.zeros((h, w), dtype=np.uint8)
    m[on if on is not None else slice(4, 12), 2:6] = 255
    return m


def test_alpha_is_the_mask_exactly(tmp_path):
    """The whole contract: the alpha channel IS the silhouette, value for value."""
    t = str(tmp_path)
    rgb, m = _rgb(), _mask()
    out, st = rgba_turnaround.compose(_write(t, "r.png", rgb, "RGB"),
                                      _write(t, "m.png", m, "L"))
    assert np.array_equal(out[..., 3], m), "alpha must equal the mask exactly, not approximately"
    assert np.array_equal(out[..., :3], rgb), "RGB must be untouched"
    assert st["opaque_px"] == int((m > 0).sum())
    assert st["transparent_px"] == m.size - st["opaque_px"]


def test_flat_255_is_caught(tmp_path):
    """The named defect. A fully-opaque mask means the frame is not RGBA-true, and the
    tool's end-of-run check must refuse it. Run through the CLI, because that is where
    the check lives."""
    t = str(tmp_path)
    os.makedirs(os.path.join(t, "r"), exist_ok=True)
    os.makedirs(os.path.join(t, "m"), exist_ok=True)
    _write(os.path.join(t, "r"), "v_0.png", _rgb(), "RGB")
    _write(os.path.join(t, "m"), "s_0.png", np.full((16, 8), 255, np.uint8), "L")
    p = subprocess.run([sys.executable, TOOL, "--renders", os.path.join(t, "r"),
                        "--render-tag", "v", "--masks", os.path.join(t, "m"),
                        "--mask-tag", "s", "--out", os.path.join(t, "o"),
                        "--out-tag", "x", "--views", "0"],
                       capture_output=True, text=True, timeout=60)
    assert p.returncode != 0, "a flat-255 alpha must be refused, not written"
    assert "flat-255" in (p.stdout + p.stderr)


def test_size_mismatch_raises(tmp_path):
    t = str(tmp_path)
    with pytest.raises(SystemExit) as e:
        rgba_turnaround.compose(_write(t, "r.png", _rgb(16, 8), "RGB"),
                                _write(t, "m.png", _mask(20, 8), "L"))
    assert "one frame" in str(e.value)


def test_soft_mask_raises(tmp_path):
    """A soft mask would smuggle a keyed edge back in - the thing geometry-sourced alpha
    exists to avoid."""
    t = str(tmp_path)
    m = _mask()
    m[5, 3] = 128
    with pytest.raises(SystemExit) as e:
        rgba_turnaround.compose(_write(t, "r.png", _rgb(), "RGB"),
                                _write(t, "m.png", m, "L"))
    assert "not binary" in str(e.value)


def test_empty_mask_raises(tmp_path):
    t = str(tmp_path)
    with pytest.raises(SystemExit) as e:
        rgba_turnaround.compose(_write(t, "r.png", _rgb(), "RGB"),
                                _write(t, "m.png", np.zeros((16, 8), np.uint8), "L"))
    assert "empty" in str(e.value)


def test_andons_survive_optimize(tmp_path):
    """Every gate above must `raise`, not `assert` - E21 Ruling 2. Measured, not asserted
    about: the soft-mask refusal is re-run under -O and PYTHONOPTIMIZE=1."""
    t = str(tmp_path)
    m = _mask()
    m[5, 3] = 128
    rp, mp = _write(t, "r.png", _rgb(), "RGB"), _write(t, "m.png", m, "L")
    prog = ("import sys; sys.path.insert(0, %r); import rgba_turnaround as R\n"
            "try:\n    R.compose(%r, %r)\n    print('SILENT')\n"
            "except SystemExit:\n    print('FIRED')\n" % (os.path.dirname(TOOL), rp, mp))
    for env_extra, flags in (({}, ["-O"]), ({"PYTHONOPTIMIZE": "1"}, []), ({"PYTHONOPTIMIZE": "1"}, ["-O"])):
        env = dict(os.environ)
        env.update(env_extra)
        r = subprocess.run([sys.executable] + flags + ["-c", prog],
                           capture_output=True, text=True, env=env, timeout=60)
        assert "FIRED" in r.stdout, "ANDON went silent under %s %s" % (flags, env_extra)
