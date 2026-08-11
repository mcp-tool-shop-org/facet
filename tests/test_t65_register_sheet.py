"""T65 (E33) - the register sheet's ANDONs, each shown FIRING on input built to fire it.

WHY THE LEGS ARE SHAPED AS FAILURES. This repo has caught two checks that could not fail - a
silhouette IoU returning 1.00000 on a holed mesh, and a dilation comparison returning 0.00%
by construction - so a leg that only agrees with the happy path is not evidence. Every ANDON
leg below constructs the specific wrong input the guard exists to catch, and a companion leg
proves the same code path SUCCEEDS on the corresponding right input, so neither half can be
passing for a trivial reason.

THREE PROPERTIES, with the wrong-implementation each discriminates against:

  1. A TWIN OFF ITS CONTROL'S SIZE HALTS. `build` must refuse a candidate whose pixel size
     differs from the clay render of its own view - the E04 Ruling 15 failure, where a width
     not divisible by 8 decoded 1066 -> 1064 and put every twin 2 px off its control.
     Discriminates against: the obvious implementation, which LANCZOS-resizes every panel to
     the column width and would therefore make a mismatched twin look tidy. The off-by-TWO
     case is the fixture, not an obviously broken 2x, because two pixels is what the real
     defect looked like.
  2. A MISSING CANDIDATE HALTS. A (register, view) pair with no file raises rather than
     drawing a short row. Discriminates against: `candidates.get(...)` falling through to a
     blank tile, which reads as "this register produced nothing" - the opposite of the truth,
     which is that nobody passed it.
  3. THE COLUMN ORDER IS THE CALLER'S, NOT SORTED. `--register` order sets column order, so
     a register list given R3, R1, R2 lays out R3, R1, R2. Discriminates against: sorting the
     dict, which would silently re-order a comparison sheet a human is about to rule from.

The ANDONs are `raise SystemExit`, never `assert`: `python -O` and PYTHONOPTIMIZE=1 delete
asserts silently and 87 of this repo's gates were removable by an environment variable until
E22 converted them (E21 Ruling 2). Leg 4 runs the firing case under `-O` and asserts it still
halts, which is the property that conversion bought.

Source is ASCII bytes (the repo's law).
"""
import os
import subprocess
import sys

import pytest
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "diagnostics", "e33_register_sheet.py")
sys.path.insert(0, os.path.join(ROOT, "tools", "diagnostics"))


def _mod():
    import importlib.util
    spec = importlib.util.spec_from_file_location("e33_register_sheet", TOOL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _png(path, w, h, colour=(128, 128, 128)):
    Image.new("RGB", (w, h), colour).save(path)
    return path


@pytest.fixture()
def scene(tmp_path):
    """A minimal, correct scene: one view, two registers, everything the right size."""
    clay = tmp_path / "clay"
    ctrl = tmp_path / "ctrl"
    cand = tmp_path / "cand"
    for p in (clay, ctrl, cand):
        p.mkdir()
    _png(str(clay / "t_0.png"), 32, 96)
    _png(str(ctrl / "t_0_control.png"), 32, 96, (0, 0, 0))
    _png(str(cand / "r1_0.png"), 32, 96, (200, 100, 60))
    _png(str(cand / "r2_0.png"), 32, 96, (60, 100, 200))
    _png(str(tmp_path / "concept.png"), 64, 64, (250, 250, 250))
    return {"root": tmp_path, "clay": str(clay), "ctrl": str(ctrl), "cand": str(cand),
            "concept": str(tmp_path / "concept.png")}


def test_t65_correct_scene_builds(scene):
    """The companion leg: the same code path SUCCEEDS on the right input.

    Without this, legs 1 and 2 could be passing because `build` raises on everything.
    """
    m = _mod()
    sheet, cols = m.build(scene["concept"], scene["clay"], scene["ctrl"], "t", ["0"],
                          {("R1", "0"): os.path.join(scene["cand"], "r1_0.png"),
                           ("R2", "0"): os.path.join(scene["cand"], "r2_0.png")},
                          [("R1", "clause one"), ("R2", "clause two")], 100)
    assert sheet.width > 0 and sheet.height > 0
    assert [c.split("  ")[0] for c in cols] == ["clay", "control", "R1", "R2"]


def test_t65_candidate_two_px_off_its_control_halts(scene):
    """E04 Ruling 15's exact magnitude: two pixels, not an obvious 2x."""
    m = _mod()
    bad = os.path.join(scene["cand"], "r1_off.png")
    _png(bad, 32, 94, (200, 100, 60))          # 96 -> 94: the VAE-truncation shape
    with pytest.raises(SystemExit) as e:
        m.build(scene["concept"], scene["clay"], scene["ctrl"], "t", ["0"],
                {("R1", "0"): bad,
                 ("R2", "0"): os.path.join(scene["cand"], "r2_0.png")},
                [("R1", "clause one"), ("R2", "clause two")], 100)
    msg = str(e.value)
    assert "ANDON" in msg and "32x94" in msg and "32x96" in msg
    assert "No file written" in msg


def test_t65_missing_candidate_halts(scene):
    m = _mod()
    with pytest.raises(SystemExit) as e:
        m.build(scene["concept"], scene["clay"], scene["ctrl"], "t", ["0"],
                {("R1", "0"): os.path.join(scene["cand"], "r1_0.png")},
                [("R1", "clause one"), ("R2", "clause two")], 100)
    msg = str(e.value)
    assert "ANDON" in msg and "R2" in msg and "No file written" in msg


def test_t65_column_order_is_the_callers_not_sorted(scene):
    """Given R2 before R1, the sheet lays out R2 before R1."""
    m = _mod()
    _, cols = m.build(scene["concept"], scene["clay"], scene["ctrl"], "t", ["0"],
                      {("R1", "0"): os.path.join(scene["cand"], "r1_0.png"),
                       ("R2", "0"): os.path.join(scene["cand"], "r2_0.png")},
                      [("R2", "clause two"), ("R1", "clause one")], 100)
    assert [c.split("  ")[0] for c in cols] == ["clay", "control", "R2", "R1"]


def test_t65_andon_survives_dash_O(scene, tmp_path):
    """The property E22's conversion bought: a gate that `assert` would lose under -O.

    Runs the CLI in a child interpreter with -O and PYTHONOPTIMIZE=1 and requires a non-zero
    exit with the ANDON text. An `assert`-based guard exits 0 here and writes the sheet.
    """
    bad = os.path.join(scene["cand"], "r1_off.png")
    _png(bad, 32, 94, (200, 100, 60))
    out = str(tmp_path / "sheet.png")
    env = dict(os.environ, PYTHONOPTIMIZE="1")
    p = subprocess.run(
        [sys.executable, "-O", TOOL,
         "--concept", scene["concept"], "--clay", scene["clay"], "--control", scene["ctrl"],
         "--tag", "t", "--views", "0",
         "--candidate", "R1:0=" + bad,
         "--candidate", "R2:0=" + os.path.join(scene["cand"], "r2_0.png"),
         "--register", "R1=clause one", "--register", "R2=clause two",
         "--out", out],
        capture_output=True, text=True, env=env)
    assert p.returncode != 0, p.stdout + p.stderr
    assert "ANDON" in (p.stdout + p.stderr)
    assert not os.path.exists(out), "the sheet was written after a fired gate"


def test_t65_source_is_ascii():
    with open(TOOL, "rb") as fh:
        raw = fh.read()
    raw.decode("ascii")
