"""T67 (E35) - median-of-K twin fusion: the property it exists for, and the ANDON that
stops it turning into ghosting.

WHY MEDIAN IS TESTED AGAINST MEAN AND NOT ONLY AGAINST ITSELF. The whole reason for a
median is that ONE seed's invented dot must not survive at 1/K strength. A fixture plants a
dot in exactly one of three otherwise-identical twins and asserts the fused pixel is the
clean register EXACTLY - a mean would leave a third of the dot behind, so this leg
discriminates against the obvious implementation rather than merely agreeing with the
chosen one.

WHY THE STRUCTURAL ANDON IS TESTED ON A REGION AND THE SPECK CASE ON DOTS. Speckle
disagreement is many tiny components; a moved fold line or material boundary is ONE large
one. Bounding the largest component is what tells them apart, so one fixture plants
scattered dots (must pass) and another plants a single large moved region (must halt), and
they are built from the same generator so the difference is the SHAPE of the disagreement,
not its amount.

THE ANDONs ARE `raise`, NEVER `assert`: -O and PYTHONOPTIMIZE=1 delete asserts silently and
87 of this repo's gates were removable by an environment variable until E22 converted them
(E21 Ruling 2). Leg 6 runs the firing case under both.

Source is ASCII bytes (the repo's law).
"""
import json
import os
import subprocess
import sys

import numpy as np
import pytest
from PIL import Image

from conftest import tool

REGISTER = (144, 102, 77)
SPECK = (80, 50, 28)
SIZE = (120, 160)          # w, h


def _twin(path, dots=(), register=REGISTER, speck=SPECK, region=None):
    w, h = SIZE
    a = np.zeros((h, w, 3), dtype=np.uint8)
    a[:, :] = register
    for (x, y, side) in dots:
        a[y:y + side, x:x + side] = speck
    if region is not None:
        x, y, rw, rh, col = region
        a[y:y + rh, x:x + rw] = col
    Image.fromarray(a).save(path)
    return a


def _mask(path, inset=2):
    w, h = SIZE
    m = np.zeros((h, w), dtype=np.uint8)
    m[inset:h - inset, inset:w - inset] = 255
    Image.fromarray(m).save(path)
    return m


def _run(args):
    return subprocess.run([sys.executable, tool("twin_fuse.py")] + args,
                          capture_output=True, text=True)


def _fuse(tmp_path, images, extra=()):
    out = tmp_path / "fused.png"
    js = tmp_path / "fused.json"
    r = _run(["--images"] + [str(p) for p in images]
             + ["--mask", str(tmp_path / "m.png"), "--out", str(out),
                "--out-json", str(js)] + list(extra))
    return r, out, js


# --- leg 1: the property median exists for -------------------------------------------

def test_a_dot_in_one_of_three_is_removed_exactly(tmp_path):
    """The load-bearing leg. A mean would leave (144-80)/3 = 21 counts of the dot behind;
    the median must return the register EXACTLY."""
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"; c = tmp_path / "c.png"
    _twin(str(a), dots=[(40, 60, 3)])
    _twin(str(b))
    _twin(str(c))
    r, out, _ = _fuse(tmp_path, [a, b, c])
    assert r.returncode == 0, r.stderr
    fused = np.asarray(Image.open(out).convert("RGB"))
    patch = fused[60:63, 40:43]
    assert (patch == np.array(REGISTER, dtype=np.uint8)).all(), (
        "the lone seed's dot survived fusion: got %s, expected %s (a MEAN would land near "
        "%s)" % (patch[0, 0].tolist(), list(REGISTER),
                 [int(round((2 * REGISTER[i] + SPECK[i]) / 3)) for i in range(3)]))


def test_a_dot_in_two_of_three_survives(tmp_path):
    """The companion. Median is not a speck eraser - it is a majority vote. If two seeds
    agree a pixel is dark, the fused pixel is dark. Without this leg, leg 1 would also pass
    for an implementation that simply returned the cleanest input."""
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"; c = tmp_path / "c.png"
    _twin(str(a), dots=[(40, 60, 3)])
    _twin(str(b), dots=[(40, 60, 3)])
    _twin(str(c))
    r, out, _ = _fuse(tmp_path, [a, b, c])
    assert r.returncode == 0, r.stderr
    fused = np.asarray(Image.open(out).convert("RGB"))
    assert (fused[60:63, 40:43] == np.array(SPECK, dtype=np.uint8)).all()


def test_identical_inputs_fuse_to_themselves(tmp_path):
    """A can-fail floor: with nothing to disagree about, fusion must be the identity and
    the disagreement map must be empty. If this ever reports disagreement, every
    disagreement number above is noise."""
    _mask(str(tmp_path / "m.png"))
    ps = []
    for n in "abc":
        p = tmp_path / ("%s.png" % n)
        _twin(str(p), dots=[(20, 30, 3), (70, 100, 2)])
        ps.append(p)
    r, out, js = _fuse(tmp_path, ps)
    assert r.returncode == 0, r.stderr
    src = np.asarray(Image.open(ps[0]).convert("RGB"))
    assert (np.asarray(Image.open(out).convert("RGB")) == src).all()
    m = json.load(open(js))["metrics"]
    assert m["disagreement_px"] == 0, m
    assert m["largest_disagreement_px2"] == 0


# --- leg 2: the disagreement map is real ---------------------------------------------

def test_scattered_speck_disagreement_is_reported_and_passes(tmp_path):
    """Speck-scale disagreement: many tiny components, none large. Must NOT halt."""
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"; c = tmp_path / "c.png"
    _twin(str(a), dots=[(20, 30, 3), (60, 40, 2)])
    _twin(str(b), dots=[(30, 70, 3), (90, 50, 2)])
    _twin(str(c), dots=[(45, 110, 3)])
    r, out, js = _fuse(tmp_path, [a, b, c])
    assert r.returncode == 0, r.stdout + r.stderr
    m = json.load(open(js))["metrics"]
    assert m["disagreement_px"] > 0, "five planted disagreements read as zero"
    assert m["disagreement_components"] >= 3, m
    assert m["largest_disagreement_px2"] <= 200, m


def test_structural_disagreement_HALTS(tmp_path):
    """One large moved region - a fold line or material boundary. Fusing across it is
    ghosting, and the tool must refuse."""
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"; c = tmp_path / "c.png"
    _twin(str(a), region=(20, 40, 40, 40, (60, 60, 140)))
    _twin(str(b), region=(20, 40, 40, 40, (60, 60, 140)))
    _twin(str(c))
    r, _, _ = _fuse(tmp_path, [a, b, c])
    assert r.returncode != 0, "a 1600 px2 structural disagreement did not halt"
    assert "ANDON" in (r.stdout + r.stderr)
    assert "STRUCTURALLY" in (r.stdout + r.stderr)


def test_report_only_downgrades_the_structural_halt(tmp_path):
    """Companion: the same input measures the same way without halting, so the ANDON is a
    decision and not an inability to compute."""
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"; c = tmp_path / "c.png"
    _twin(str(a), region=(20, 40, 40, 40, (60, 60, 140)))
    _twin(str(b), region=(20, 40, 40, 40, (60, 60, 140)))
    _twin(str(c))
    r, _, js = _fuse(tmp_path, [a, b, c], extra=["--report-only"])
    assert r.returncode == 0, r.stderr
    assert "REPORT-ONLY, would have halted" in r.stdout
    assert json.load(open(js))["metrics"]["largest_disagreement_px2"] > 200


# --- leg 3: input guards -------------------------------------------------------------

def test_single_image_halts(tmp_path):
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"
    _twin(str(a))
    r, _, _ = _fuse(tmp_path, [a])
    assert r.returncode != 0
    assert "at least 2" in (r.stdout + r.stderr)


def test_shape_mismatch_halts(tmp_path):
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"
    _twin(str(a))
    Image.fromarray(np.zeros((40, 40, 3), np.uint8)).save(str(b))
    r, _, _ = _fuse(tmp_path, [a, b])
    assert r.returncode != 0
    assert "ANDON" in (r.stdout + r.stderr)


def test_full_frame_mask_halts(tmp_path):
    w, h = SIZE
    Image.fromarray(np.full((h, w), 255, np.uint8)).save(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"
    _twin(str(a)); _twin(str(b))
    r, _, _ = _fuse(tmp_path, [a, b])
    assert r.returncode != 0
    assert "spans the whole frame" in (r.stdout + r.stderr)


# --- leg 4: the report replays -------------------------------------------------------

def test_report_pins_inputs_and_params(tmp_path):
    _mask(str(tmp_path / "m.png"))
    ps = []
    for n in "abc":
        p = tmp_path / ("%s.png" % n)
        _twin(str(p), dots=[(20, 30, 2)])
        ps.append(p)
    r, _, js = _fuse(tmp_path, ps)
    assert r.returncode == 0
    rep = json.load(open(js))
    assert len(rep["inputs"]) == 3
    assert all(len(i["sha256"]) == 64 for i in rep["inputs"])
    assert rep["mask"]["sha256"] and len(rep["tool_sha256"]) == 64
    assert rep["params"]["dev_thresh"] and rep["params"]["disagreement_max_px2"]
    assert rep["metrics"]["inter_seed_iou_min"] is not None


# --- leg 5: structural agreement is measured, not assumed (R-b) -----------------------

def test_inter_seed_iou_falls_when_a_seed_paints_a_different_figure(tmp_path):
    """R-b's precondition has to be able to FAIL. Two seeds painting the same figure and a
    third painting a smaller one must drop the reported minimum IoU below 1."""
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"; c = tmp_path / "c.png"
    _twin(str(a)); _twin(str(b))
    # a seed that leaves a large neutral (chroma-free) area = a different painted figure
    _twin(str(c), region=(10, 10, 60, 80, (150, 150, 150)))
    r, _, js = _fuse(tmp_path, [a, b, c], extra=["--report-only"])
    assert r.returncode == 0, r.stderr
    m = json.load(open(js))["metrics"]
    assert m["inter_seed_iou_min"] < 0.95, m
    assert m["inter_seed_iou_mean"] < 1.0


# --- leg 6: the ANDON survives -O and PYTHONOPTIMIZE ----------------------------------

@pytest.mark.parametrize("mode", ["-O", "env", "both"])
def test_andon_survives_optimize(tmp_path, mode):
    _mask(str(tmp_path / "m.png"))
    a = tmp_path / "a.png"; b = tmp_path / "b.png"; c = tmp_path / "c.png"
    _twin(str(a), region=(20, 40, 40, 40, (60, 60, 140)))
    _twin(str(b), region=(20, 40, 40, 40, (60, 60, 140)))
    _twin(str(c))
    cmd = [sys.executable]
    if mode in ("-O", "both"):
        cmd.append("-O")
    env = dict(os.environ)
    if mode in ("env", "both"):
        env["PYTHONOPTIMIZE"] = "1"
    r = subprocess.run(cmd + [tool("twin_fuse.py"), "--images", str(a), str(b), str(c),
                              "--mask", str(tmp_path / "m.png"),
                              "--out", str(tmp_path / "f.png")],
                       capture_output=True, text=True, env=env)
    assert r.returncode != 0, "the ANDON was DELETED under %s - it is not a gate" % mode
    assert "ANDON" in (r.stdout + r.stderr)


def test_source_is_ascii():
    src = open(tool("twin_fuse.py"), "rb").read()
    bad = [(i, b) for i, b in enumerate(src) if b > 127]
    assert not bad, "non-ASCII bytes at %s" % bad[:5]
