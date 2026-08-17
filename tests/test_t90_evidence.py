"""T90 - the diagnostic layer (library plus thin verbs).

The instrument is tools/evidence.py. Brief #16 assigned t89; that
number is already taken by flat_trace. This file is t90. The brief's
t89 is a collision, not a second T89.

A monolith that hardcodes a subject, a 5-way that treats ~valid as
unmapped, a new crop, a third surfid decode, or a bare assert fails
at least one leg.

Hermetic tests do not open facet_E49 / E06. The artifacts leg does,
read-only.
"""
import ast
import os
import sys

import numpy as np
import pytest
from PIL import Image

from conftest import REPO, need, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import evidence as E  # noqa: E402
import s3_sheet as SH  # noqa: E402
import unmapped_readout as U  # noqa: E402


def test_t90_selftest_exits_zero():
    rc, out, err = run_py("evidence.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "128/64/32/32" in out, out
    assert "overlap ANDON" in out, out
    assert "crop[0,0] == 200" in out, out


def test_t90_atlas_four_way_is_disjoint_and_exhaustive():
    owner, filled, orphan, nvv, valid = E.fixture_atlas()
    cls = E.classify_atlas(owner, filled, orphan, nvv, valid)
    nums = E.numbers_atlas(cls)
    assert nums["classes"]["written"]["n"] == E.FIX_WRITTEN
    assert nums["classes"]["filled"]["n"] == E.FIX_FILLED
    assert nums["classes"]["orphan_fill"]["n"] == E.FIX_ORPHAN
    assert nums["classes"]["no_view_visible"]["n"] == E.FIX_NVV
    assert nums["denominator"] == E.FIX_VALID
    assert nums["space"] == E.ATLAS_SPACE
    s = sum(nums["classes"][k]["n"] for k in E.FOUR)
    assert s == nums["denominator"]


def test_t90_overlap_andon():
    """Can-fail: silently OR-ing classes would hide the fifth one."""
    with pytest.raises(E.Andon, match="overlap"):
        E.classify_atlas(*E.fixture_overlap())


def test_t90_unmapped_atlas_is_not_the_gutter():
    """Can-fail: ~valid is the gutter, not the class E50 found."""
    owner, filled, orphan, nvv, valid = E.fixture_atlas()
    gutter = int((~valid).sum())
    assert gutter > 0
    empty = np.full(valid.shape, -1, dtype=np.int64)
    um = E.atlas_unmapped_from_surfid(empty, valid)
    assert um["n"] == 0
    assert um["space"] == E.UNMAPPED_ATLAS_SPACE
    # one figure pixel whose surfid lands outside valid
    surfid = np.full(valid.shape, -1, dtype=np.int64)
    surfid[4, 4] = 1 * valid.shape[0] + 1
    um2 = E.atlas_unmapped_from_surfid(surfid, valid)
    assert um2["n"] == 1
    assert um2["n"] != gutter


def test_t90_rendered_five_way_uses_unmapped_readout():
    surfid, valid, im, owner, filled, orphan, nvv = U.fixture_calibration()
    rec, cls = U.readout_view(
        surfid, valid, im, owner, filled, orphan, nvv)
    rend = E.numbers_rendered(rec)
    assert rend["classes"]["unmapped"]["n"] == 1
    assert rend["space"] == E.RENDER_SPACE
    assert rend["classes"]["unmapped"]["space"] == E.RENDER_SPACE
    assert rend["classes"]["written"]["denominator"] == rec["n_fig_px"]


def test_t90_every_share_names_its_space():
    owner, filled, orphan, nvv, valid = E.fixture_atlas()
    nums = E.numbers_atlas(E.classify_atlas(owner, filled, orphan, nvv, valid))
    for name in E.FOUR:
        c = nums["classes"][name]
        assert c["space"] == E.ATLAS_SPACE, name
        assert c["denominator"] == E.FIX_VALID
        assert c["denominator_name"]


def test_t90_sheet_crop_is_s3_sheet_crop():
    """Can-fail: a new crop that clamps would not land 200 at [0,0]."""
    src = SH.fixture_calibration_canvas(32)
    columns = [{"role": "reference", "rgb": src, "path": "fixture.png"}]
    rgb, consumed, hw = E.build_column_sheet(
        columns,
        [{"name": "pin", "box": list(SH.CALIBRATION_BOX)}],
        0, zoom=SH.CALIBRATION_ZOOM)
    crop = SH.crop_nn(
        src, SH.CALIBRATION_BOX, SH.CALIBRATION_ZOOM,
        name="pin", source="fixture")
    assert int(crop[0, 0, 0]) == SH.CALIBRATION_VALUE
    assert rgb.shape[0] > crop.shape[0]
    assert consumed[0]["path"] == "fixture.png"


def test_t90_sheet_missing_column_is_missing_panel(tmp_path):
    src = SH.fixture_calibration_canvas(32)
    src_p = str(tmp_path / "ref.png")
    SH.write_png(src_p, src)
    spec = {
        "views": {
            "0": [{"name": "pin", "box": list(SH.CALIBRATION_BOX)}],
        }
    }
    regions = tmp_path / "regions.json"
    regions.write_text(
        __import__("json").dumps(spec), encoding="utf-8")
    out = tmp_path / "sheet"
    rc, out_s, err = run_py("evidence.py", [
        "sheet",
        "--col", "reference=%s" % src_p,
        "--col", "shipped=%s" % str(tmp_path / "nope.png"),
        "--regions", str(regions),
        "--views", "0",
        "--out", str(out),
    ])
    assert rc == 0, "%s\n%s" % (out_s, err)
    png = Image.open(str(out / "sheet_v00.png"))
    arr = np.asarray(png)
    # MISSING fill is s3_sheet's (180, 0, 140)
    assert (arr == np.array(SH.MISSING_RGB, dtype=np.uint8)).all(axis=-1).any()


def test_t90_flats_delegates_to_flat_trace():
    rc, out, err = run_py("evidence.py", ["flats", "--selftest"])
    assert rc == 0, "flats --selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "owner-twin" in out, out
    assert "same-xy is not" in out, out


def test_t90_cli_missing_exits_2(tmp_path):
    rc, out, err = run_py("evidence.py", [
        "classify",
        "--atlas-dir", str(tmp_path / "nope"),
        "--mask", str(tmp_path / "no.npy"),
        "--out", str(tmp_path / "out"),
    ])
    assert rc == 2
    assert "ANDON" in err


def test_t90_does_not_reroll_surfid_or_crop():
    """The layer imports the instruments. A third decode is the waste."""
    src = open(os.path.join(str(REPO), "tools", "evidence.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    names = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    assert "decode_surfid" not in names
    assert "crop_array" not in names
    assert "crop_nn" not in names
    assert "import s3_sheet as SH" in src
    assert "import unmapped_readout as U" in src


def test_t90_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "evidence.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares


@pytest.mark.artifacts
def test_t90_e50_gate_a_owner_four_way(assets):
    """E50 Gate A, re-measured. Do not write the tree."""
    atlas = need(assets, "facet_E49/atlas_owner_eroded")
    prep = need(assets, "facet_E06/C1/prep")
    payload = E.classify_paths(str(atlas), str(prep / "mask.npy"))
    a = payload["atlas"]["classes"]
    assert a["written"]["n"] == E.CALIBRATION_ATLAS_WRITTEN
    assert a["filled"]["n"] == E.CALIBRATION_ATLAS_FILLED
    assert a["orphan_fill"]["n"] == E.CALIBRATION_ATLAS_ORPHAN
    assert a["no_view_visible"]["n"] == E.CALIBRATION_ATLAS_NVV
    assert payload["atlas"]["denominator"] == E.CALIBRATION_ATLAS_VALID
    assert payload["atlas"]["space"] == E.ATLAS_SPACE
    assert "unmapped" not in a
