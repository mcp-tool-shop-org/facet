"""T82 - the S3 acceptance sheet (layout only).

The instrument is tools/s3_sheet.py. Brief #7 assigned t81; that number is
already taken by the E45 warp instrument. This file is t82.

Every number below is known by construction. An auto-clamped crop, a
bilinear zoom, a silent skip of a missing input, or a hash the sheet
echoed without reading the file fails at least one leg.

Tests are hermetic. They do not open the E45 bundle or the ARMB twins.
"""
import ast
import os
import sys

import numpy as np
import pytest
from PIL import Image

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import s3_sheet as S  # noqa: E402


def test_t82_selftest_exits_zero():
    rc, out, err = run_py("s3_sheet.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "calibration crop[0,0] == 200" in out, out


def test_t82_calibration_crop_origin():
    src = S.fixture_calibration_canvas(32)
    crop = S.crop_nn(src, S.CALIBRATION_BOX, S.CALIBRATION_ZOOM,
                     name="pin", source="fixture")
    got = int(crop[0, 0, 0])
    assert got == S.CALIBRATION_VALUE, (
        "CALIBRATION: crop[0,0] is %r, not %d "
        "(swapped x/y, origin slip, clamp, or resample)"
        % (got, S.CALIBRATION_VALUE))
    assert crop.shape[0] == 16 and crop.shape[1] == 16, crop.shape
    assert int(crop[1, 1, 0]) == S.CALIBRATION_VALUE
    assert int(crop[2, 0, 0]) == 0


def test_t82_oversized_box_andon():
    src = S.fixture_calibration_canvas(32)
    with pytest.raises(S.Andon, match="exceeds source"):
        S.crop_array(src, [0, 0, 40, 40], "big", "fixture")


def test_t82_mismatched_row_andon():
    a = np.zeros((32, 32, 3), dtype=np.uint8)
    b = np.zeros((16, 16, 3), dtype=np.uint8)
    with pytest.raises(S.Andon, match="mismatched panel size"):
        S.compose_row(
            [a, b],
            [{"role": "a", "path": "a"}, {"role": "b", "path": "b"}],
            "mismatch")


def test_t82_missing_panel_is_detectable(tmp_path):
    ref = S.fixture_calibration_canvas(32)
    ref_dir = tmp_path / "ref"
    ship_dir = tmp_path / "ship"
    s3 = tmp_path / "s3" / "t00"
    ref_dir.mkdir()
    ship_dir.mkdir()
    s3.mkdir(parents=True)
    S.write_png(str(ref_dir / "twin_0.png"), ref)
    S.write_png(str(s3 / "dependent.png"), ref)
    S.write_png(str(s3 / "independent.png"), ref)
    np.save(str(s3 / "disagreement.npy"),
            np.full((32, 32), 0.25, dtype=np.float64))
    Image.fromarray(np.full((32, 32), 255, dtype=np.uint8)).save(
        str(s3 / "coverage.png"))
    Image.fromarray(np.zeros((32, 32), dtype=np.uint8)).save(
        str(s3 / "fallback.png"))
    np.save(str(s3 / "owner.npy"), np.zeros((32, 32), dtype=np.int32))
    maps, paths, _consumed = S.load_target_inputs(
        str(tmp_path / "s3"), str(ref_dir), str(ship_dir), 0)
    assert maps["shipped"] is None
    panel, ok = S.panel_for(None, (32, 32), paths["shipped"], 1)
    assert ok is False
    assert S.is_missing_panel(panel)
    assert not S.is_missing_panel(maps["reference"])
    assert int(panel[0, 0, 0]) != int(maps["reference"][S.CALIBRATION_Y,
                                                         S.CALIBRATION_X, 0])


def test_t82_provenance_hashes_match_files(tmp_path):
    S.selftest(scratch=str(tmp_path / "st"))
    ref = tmp_path / "st" / "ref" / "twin_0.png"
    expect = S.sha256_file(str(ref))
    import json
    man = json.loads((tmp_path / "st" / "out" / "manifest.json").read_text(
        encoding="utf-8"))
    found = None
    for e in man["results"][0]["consumed"]:
        if e.get("sha256") and os.path.basename(e["path"]) == "twin_0.png":
            found = e["sha256"]
    assert found == expect, "manifest %s != reread %s" % (found, expect)
    assert found == S.sha256_file(str(ref))


def test_t82_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "s3_sheet.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares
