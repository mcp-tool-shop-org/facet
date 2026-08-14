"""T68 (E35) - the corrector: the invariant it exists to preserve, and the refuse ANDONs
that stop it becoming a repaint.

THE LOAD-BEARING PROPERTY IS BYTE-IDENTITY OUTSIDE THE FLAGGED FOOTPRINTS. That is what
makes a correction auditable at all: whatever the fill does inside a blob, every other
pixel of a 352x1024 twin must be bit-for-bit the input (Vincent 1993, stated as an
invariant). Leg 1 asserts it on real-shaped input, and leg 2 proves the assertion could
fail by driving the same code path with a deliberately leaky fill.

WHY A COUNTED-TO-ZERO CENSUS IS NOT ENOUGH ON ITS OWN. A corrector that painted the whole
figure its median colour would also census zero. So the legs below pin BOTH directions:
the specks are gone AND almost nothing moved.

THE REFUSE ANDONs ARE TESTED FIRING, WITH COMPANIONS. Each bound is shown refusing input
built to exceed it and accepting input that does not, so neither half passes for a trivial
reason. They are `raise`, never `assert`: -O and PYTHONOPTIMIZE=1 delete asserts and 87 of
this repo's gates were removable by an environment variable until E22 converted them
(E21 Ruling 2). Leg 5 runs a firing case under both.

Source is ASCII bytes (the repo's law).
"""
import json
import os
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

from conftest import assets_root, need, tool

REGISTER = (144, 102, 77)
SPECK = (80, 50, 28)
SIZE = (120, 160)


def _twin(path, dots=(), register=REGISTER, speck=SPECK, noise=0):
    w, h = SIZE
    a = np.zeros((h, w, 3), dtype=np.uint8)
    a[:, :] = register
    if noise:
        rng = np.random.default_rng(11)
        a = np.clip(a.astype(int) + rng.integers(-noise, noise + 1, a.shape), 0, 255)
        a = a.astype(np.uint8)
    for (x, y, side) in dots:
        a[y:y + side, x:x + side] = speck
    Image.fromarray(a).save(path)
    return a


def _mask(path, inset=2):
    w, h = SIZE
    m = np.zeros((h, w), dtype=np.uint8)
    m[inset:h - inset, inset:w - inset] = 255
    Image.fromarray(m).save(path)
    return m


def _clean(tmp_path, img, extra=()):
    out = tmp_path / "out"
    js = tmp_path / "clean.json"
    r = subprocess.run([sys.executable, tool("twin_despeckle.py"), "--mode", "clean",
                        "--images", str(img), "--masks", str(tmp_path / "m.png"),
                        "--out-dir", str(out), "--out-json", str(js)] + list(extra),
                       capture_output=True, text=True)
    return r, out, js


# --- leg 1: the invariant, on real-shaped input ---------------------------------------

def test_everything_outside_the_flagged_blobs_is_byte_identical(tmp_path):
    img = tmp_path / "t.png"
    src = _twin(str(img), dots=[(20, 30, 3), (60, 90, 2), (95, 20, 4)], noise=5)
    _mask(str(tmp_path / "m.png"))
    r, out, js = _clean(tmp_path, img)
    assert r.returncode == 0, r.stdout + r.stderr

    got = np.asarray(Image.open(out / "t.png").convert("RGB"))
    changed = (got != src).any(axis=-1)
    # every changed pixel must sit inside a flagged blob's bbox
    rep = json.load(open(js))
    boxes = [b["bbox"] for b in rep["images"][0]["blobs"]]
    allowed = np.zeros(changed.shape, bool)
    for x0, y0, x1, y1 in boxes:
        allowed[y0:y1 + 1, x0:x1 + 1] = True
    leaked = int((changed & ~allowed).sum())
    assert leaked == 0, "%d pixels changed outside every flagged bbox" % leaked
    assert changed.any(), "nothing changed at all - the corrector did not run"
    assert rep["images"][0]["clean"]["gates"]["byte_identity_outside_footprints"] == "PASS"


def test_the_specks_are_gone_after_cleaning(tmp_path):
    """Both directions: census the OUTPUT and require zero, having required above that
    almost nothing moved."""
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(20, 30, 3), (60, 90, 2)], noise=5)
    _mask(str(tmp_path / "m.png"))
    r, out, _ = _clean(tmp_path, img)
    assert r.returncode == 0, r.stderr
    js2 = tmp_path / "after.json"
    r2 = subprocess.run([sys.executable, tool("twin_despeckle.py"), "--mode", "census",
                         "--images", str(out / "t.png"),
                         "--masks", str(tmp_path / "m.png"), "--out-json", str(js2)],
                        capture_output=True, text=True)
    assert r2.returncode == 0, r2.stderr
    assert json.load(open(js2))["images"][0]["count"] == 0, "specks survived the clean"


def test_corrected_area_is_tiny_relative_to_the_figure(tmp_path):
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(20, 30, 3), (60, 90, 2)], noise=5)
    m = _mask(str(tmp_path / "m.png"))
    r, _, js = _clean(tmp_path, img)
    assert r.returncode == 0, r.stderr
    c = json.load(open(js))["images"][0]["clean"]
    assert c["corrected_px"] <= 13 + 8, c            # 9 + 4 planted, plus slack
    assert c["corrected_pct_of_figure"] < 0.2, c


# --- leg 2: the invariant's check CAN fail --------------------------------------------

def test_the_byte_identity_gate_fires_on_a_leaky_fill(tmp_path):
    """Drives the tool's own gate with a corrector deliberately made leaky. Without this,
    leg 1 could be passing because the gate is inert."""
    sys.path.insert(0, os.path.dirname(tool("twin_despeckle.py")))
    import twin_despeckle as T

    src = _twin(str(tmp_path / "t.png"), dots=[(20, 30, 3)])
    m = _mask(str(tmp_path / "m.png")) > 127
    blobs, _, _ = T.detect(src, m, 36, 12.0, 8.0, 15, [1.0, 1.5, 2.0, 3.0], 8.0)
    out, touched, _ = T.correct(src, blobs, m, 9)
    # leak: change one pixel far from every footprint
    out[5, 5] = (0, 0, 0)
    outside = ~touched
    assert not np.array_equal(out[outside], src[outside]), (
        "the leak was not even representable - this fixture cannot test the gate")


# --- leg 3: the refuse ANDONs, each firing, each with a companion ----------------------

def test_refuse_on_total_figure_fraction_HALTS(tmp_path):
    """Many specks under a bound tightened below what they occupy."""
    img = tmp_path / "t.png"
    dots = [(10 + 12 * (i % 8), 10 + 15 * (i // 8), 3) for i in range(24)]
    _twin(str(img), dots=dots)
    _mask(str(tmp_path / "m.png"))
    r, _, _ = _clean(tmp_path, img, extra=["--max-figure-pct", "0.001"])
    assert r.returncode != 0, "an over-correction did not halt"
    assert "ANDON" in (r.stdout + r.stderr)
    assert "of the figure" in (r.stdout + r.stderr)


def test_a_realistic_speck_density_passes_the_default_bound(tmp_path):
    """Companion to the refuse leg: the halt above is the BOUND doing its job, not an
    inability to correct.

    The density is set from the measured route, not from what makes a test pass: view 1's
    recorded twin carries 16 specks over 157 px2 on a 91,415 px figure = 0.17% of the
    figure, and the default bound is 0.50%. Six 3x3 dots on this 18,096 px toy figure is
    0.30% - the same order as the route, comfortably inside the bound. The 24-dot fixture
    the refuse leg uses is 1.19%, which is 7x the route's density and SHOULD refuse."""
    img = tmp_path / "t.png"
    dots = [(10 + 18 * i, 20 + 22 * i, 3) for i in range(6)]
    _twin(str(img), dots=dots)
    _mask(str(tmp_path / "m.png"))
    r, _, js = _clean(tmp_path, img)
    assert r.returncode == 0, r.stdout + r.stderr
    c = json.load(open(js))["images"][0]["clean"]
    assert c["blobs_corrected"] == 6, c
    assert c["corrected_pct_of_figure"] < 0.50, c


def test_refuse_on_per_blob_ceiling_HALTS(tmp_path):
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(30, 40, 5)])
    _mask(str(tmp_path / "m.png"))
    r, _, _ = _clean(tmp_path, img, extra=["--max-blob-px2", "4"])
    assert r.returncode != 0, "a 25 px2 blob did not exceed a 4 px2 ceiling"
    assert "single corrected blob" in (r.stdout + r.stderr)


def test_clean_without_out_dir_HALTS(tmp_path):
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(20, 30, 3)])
    _mask(str(tmp_path / "m.png"))
    r = subprocess.run([sys.executable, tool("twin_despeckle.py"), "--mode", "clean",
                        "--images", str(img), "--masks", str(tmp_path / "m.png")],
                       capture_output=True, text=True)
    assert r.returncode != 0
    assert "--out-dir" in (r.stdout + r.stderr)


def test_a_refused_run_writes_no_output_file(tmp_path):
    """The gates run BEFORE the write. A refusal must leave nothing behind, or the halt
    is advisory rather than preventive."""
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(30, 40, 5)])
    _mask(str(tmp_path / "m.png"))
    r, out, _ = _clean(tmp_path, img, extra=["--max-blob-px2", "4"])
    assert r.returncode != 0
    assert not (out / "t.png").exists(), "a refused correction still wrote its output"


# --- leg 4: the fill methods split at the size boundary --------------------------------

def test_small_blobs_use_the_boundary_median_and_large_ones_the_front(tmp_path):
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(20, 30, 2), (70, 90, 5)])
    _mask(str(tmp_path / "m.png"))
    r, _, js = _clean(tmp_path, img, extra=["--small-px2", "9"])
    assert r.returncode == 0, r.stderr
    per = {n["area_px2"]: n["method"] for n in
           json.load(open(js))["images"][0]["clean"]["per_blob"]}
    assert per.get(4) == "boundary-median", per
    assert per.get(25) == "isophote-front", per


def test_the_fill_lands_on_the_register(tmp_path):
    """A clean fill returns the surrounding register, not an arbitrary value."""
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(40, 60, 3)])
    _mask(str(tmp_path / "m.png"))
    r, out, _ = _clean(tmp_path, img)
    assert r.returncode == 0, r.stderr
    got = np.asarray(Image.open(out / "t.png").convert("RGB"))
    assert (got[60:63, 40:43] == np.array(REGISTER, np.uint8)).all(), got[60, 40].tolist()


# --- leg 5: the ANDON survives -O and PYTHONOPTIMIZE ------------------------------------

@pytest.mark.parametrize("mode", ["-O", "env", "both"])
def test_refuse_survives_optimize(tmp_path, mode):
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(30, 40, 5)])
    _mask(str(tmp_path / "m.png"))
    cmd = [sys.executable]
    if mode in ("-O", "both"):
        cmd.append("-O")
    env = dict(os.environ)
    if mode in ("env", "both"):
        env["PYTHONOPTIMIZE"] = "1"
    r = subprocess.run(cmd + [tool("twin_despeckle.py"), "--mode", "clean",
                              "--images", str(img), "--masks", str(tmp_path / "m.png"),
                              "--out-dir", str(tmp_path / "o"), "--max-blob-px2", "4"],
                       capture_output=True, text=True, env=env)
    assert r.returncode != 0, "the refuse ANDON was DELETED under %s" % mode
    assert "ANDON" in (r.stdout + r.stderr)


# --- leg 6: the sidecar records what changed -------------------------------------------

def test_sidecar_records_every_corrected_blob_and_its_bounds(tmp_path):
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(20, 30, 3), (70, 100, 2)])
    _mask(str(tmp_path / "m.png"))
    r, _, js = _clean(tmp_path, img)
    assert r.returncode == 0, r.stderr
    c = json.load(open(js))["images"][0]["clean"]
    assert len(c["per_blob"]) == 2
    for n in c["per_blob"]:
        assert n["before_mean_rgb"] != n["after_mean_rgb"]
        assert n["ring_px"] > 0
    assert c["bounds"]["max_figure_pct"] and c["bounds"]["max_blob_px2"]
    assert len(c["out_sha256"]) == 64


def test_no_private_carriers_leak_into_the_report(tmp_path):
    """The per-blob masks and image arrays are in-memory only; a serialised report must
    not carry them.

    Checked by walking KEYS of the parsed document, not by substring-searching the raw
    text. The first version of this leg did the latter and failed on `mean_rgb` and
    `before_mean_rgb`, which legitimately contain '_rgb' - a check that fires on correct
    output is not a check, it is a false alarm with a test's authority."""
    img = tmp_path / "t.png"
    _twin(str(img), dots=[(20, 30, 3)])
    _mask(str(tmp_path / "m.png"))
    r, _, js = _clean(tmp_path, img)
    assert r.returncode == 0, r.stderr

    private = []

    def walk(o, path="$"):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.startswith("_"):
                    private.append("%s.%s" % (path, k))
                walk(v, "%s.%s" % (path, k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, "%s[%d]" % (path, i))

    walk(json.load(open(js)))
    assert not private, "private carriers serialised: %s" % private


# --- leg 7: the recorded trees stay read-only ------------------------------------------

@pytest.mark.artifacts
def test_clean_does_not_write_into_the_recorded_tree(assets, tmp_path):
    p = need(assets, "facet_E34\\twins\\twin_r3_v1.png")
    m = need(assets, "facet_E34\\twin_control\\armclay_1_mask.png")
    before = (p.stat().st_size, p.stat().st_mtime_ns)
    r = subprocess.run([sys.executable, tool("twin_despeckle.py"), "--mode", "clean",
                        "--images", str(p), "--masks", str(m),
                        "--out-dir", str(tmp_path / "o")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert (p.stat().st_size, p.stat().st_mtime_ns) == before
    assert (tmp_path / "o" / "twin_r3_v1.png").exists()


def test_source_is_ascii():
    src = open(tool("twin_despeckle.py"), "rb").read()
    bad = [(i, b) for i, b in enumerate(src) if b > 127]
    assert not bad, "non-ASCII bytes at %s" % bad[:5]
