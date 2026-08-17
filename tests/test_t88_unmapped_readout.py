"""T88 - rendered-pixel readout of the unmapped class.

The instrument is tools/unmapped_readout.py. Every number below is
known by construction except the artifacts replay, which re-reads
E50's view-0 accounting (1154 / 146356).

A share-of-atlas quoted as appearance, a magenta pixel classified as
written, an interior control that carries the class, or a bare assert
fails at least one leg.

Hermetic tests do not open facet_E49 / E06. The artifacts legs do,
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
import unmapped_readout as U  # noqa: E402


def test_t88_selftest_exits_zero():
    rc, out, err = run_py("unmapped_readout.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "unmapped == 1" in out, out
    assert "interior control 0" in out, out


def test_t88_fixture_exact_magenta_is_unmapped():
    """Can-fail: lumping unmapped into written hides the sentinel."""
    surfid, valid, im, owner, filled, orphan, nvv = U.fixture_calibration()
    rec, cls = U.readout_view(surfid, valid, im, owner, filled, orphan, nvv)
    assert rec["n_unmapped"] == 1
    assert rec["exact_magenta"] == 1
    assert rec["exact_by_class"]["unmapped"] == 1
    assert rec["exact_by_class"]["written"] == 0
    assert rec["enrichment_at_exact_magenta"]["share"] == 1.0
    assert rec["enrichment_at_interior_control"]["unmapped"] == 0
    assert rec["space"] == "rendered figure pixels"


def test_t88_written_interior_is_not_unmapped():
    surfid, valid, im, owner, filled, orphan, nvv = U.fixture_calibration()
    rec, cls = U.readout_view(surfid, valid, im, owner, filled, orphan, nvv)
    assert not bool(cls["unmapped"][12, 12])
    assert cls["written"][12, 12]


def test_t88_shape_mismatch_andon():
    surfid, valid, im, owner, filled, orphan, nvv = U.fixture_calibration()
    bad = np.zeros((8, 8, 3), dtype=np.uint8)
    with pytest.raises(U.Andon, match="render"):
        U.readout_view(surfid, valid, bad, owner, filled, orphan, nvv)


def test_t88_loose_does_not_equal_exact():
    """Can-fail: a bilinear neighbour is not the sentinel."""
    im = np.zeros((4, 4, 3), dtype=np.uint8)
    im[1, 1] = (255, 0, 255)
    im[1, 2] = (220, 40, 220)
    assert int(U.exact_magenta(im).sum()) == 1
    assert int(U.loose_magenta(im).sum()) == 2


def test_t88_lcc_separates_blob_from_speckle():
    m = np.zeros((16, 16), dtype=bool)
    m[2:6, 2:6] = True
    m[10, 10] = True
    m[14, 1] = True
    tot, big = U.lcc(m)
    assert tot == 16 + 2
    assert big == 16
    assert tot != big


def test_t88_cli_missing_exits_2(tmp_path):
    rc, out, err = run_py("unmapped_readout.py", [
        "--aov-dir", str(tmp_path / "nope"),
        "--mask", str(tmp_path / "no.npy"),
        "--render-dir", str(tmp_path),
    ])
    assert rc == 2
    assert "ANDON" in err


def test_t88_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "unmapped_readout.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares


@pytest.mark.artifacts
def test_t88_e50_view0_unmapped_is_1154(assets):
    """E50's shaping number, re-measured. Do not write the tree."""
    aov = need(assets, "facet_E49/aov_eroded/view_0")
    prep = need(assets, "facet_E06/C1/prep")
    surfid = np.load(str(aov / "surfid.npy"))
    valid = U.load_valid(str(prep / "mask.npy"))
    cls = U.classes_for_view(surfid, valid)
    assert int(cls["sil"].sum()) == U.CALIBRATION_FIG
    assert int(cls["unmapped"].sum()) == U.CALIBRATION_UNMAPPED


@pytest.mark.artifacts
def test_t88_e49_exact_magenta_is_unmapped_not_written(assets):
    """The advisor hypothesis on view 0, owner, exact sentinel."""
    aov = need(assets, "facet_E49/aov_eroded/view_0")
    prep = need(assets, "facet_E06/C1/prep")
    rend = need(assets, "facet_E49/renders_owner_complete")
    atlas = need(assets, "facet_E49/atlas_owner_eroded")
    surfid = np.load(str(aov / "surfid.npy"))
    valid = U.load_valid(str(prep / "mask.npy"))
    im = np.asarray(Image.open(str(rend / "owner_complete_0.png")).convert("RGB"))
    owner = np.load(str(atlas / "owner.npy"))
    filled = np.load(str(atlas / "filled_mask.npy"))
    orphan = np.load(str(atlas / "orphan_fill_mask.npy"))
    nvv = np.load(str(atlas / "no_view_visible_mask.npy"))
    rec, _ = U.readout_view(surfid, valid, im, owner, filled, orphan, nvv)
    assert rec["exact_by_class"]["written"] == 0
    assert rec["exact_by_class"]["unmapped"] >= rec["exact_magenta"] - 10
    assert rec["exact_by_class"]["unmapped"] > rec["exact_by_class"]["no_view_visible"]
    # interior control is not the 11.58x population
    ic = rec["enrichment_at_interior_control"]
    ex = rec["enrichment_at_exact_magenta"]
    assert ic["share"] is not None and ex["share"] is not None
    assert ex["share"] > 0.9
    assert ic["share"] < 0.05
    assert rec["atlas"]["dist_to_valid_min"] >= 16.0
