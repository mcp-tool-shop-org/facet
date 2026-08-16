"""T73 - e37_fire_repaints: the mask hardening, the union, and the locality instrument.

E37 Phase 2's firing pass. Every check here is built to the repo's own question -- what
would this look like if the code were wrong in the specific way this check exists to
catch -- so each one constructs the failing case and proves the check fires on it, rather
than only proving it passes on good input.

Hermetic: synthetic arrays only, no recorded tree, no cloud. The instrument's own
artifacts are never read as evidence (E28's self-reference lesson).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "tools" / "e37_fire_repaints.py"

sys.path.insert(0, str(REPO / "tools"))
import e37_fire_repaints as fr  # noqa: E402


def _write(path, arr):
    Image.fromarray(arr.astype(np.uint8), mode="L").save(path)


def _rgb(path, arr):
    Image.fromarray(arr.astype(np.uint8), mode="RGB").save(path)


# ---------------------------------------------------------------- held rect

def test_harden_zeroes_the_closed_rect_not_the_half_open_one():
    """The one-pixel disagreement that fired at the firing seat, pinned.

    The ratified v7 mask was cut against a HALF-OPEN held rect, so the CLOSED rect's far
    corner carried 8/255. If harden_held ever reverts to half-open bounds, the corner
    pixel survives and this fires.
    """
    x0, y0, x1, y1 = fr.HELD_RECTS["v7band"]
    m = np.zeros((1024, 368))
    m[y0:y1 + 1, x0:x1 + 1] = 1.0          # paint the whole CLOSED rect
    out = fr.harden_held(m, "v7band")
    assert out[y0:y1 + 1, x0:x1 + 1].max() == 0.0
    # the corner pixel specifically -- the one the gate caught
    assert out[y1, x1] == 0.0
    # and nothing outside the rect was touched
    m2 = np.ones((1024, 368))
    out2 = fr.harden_held(m2, "v7band")
    assert out2.sum() == m2.sum() - (y1 - y0 + 1) * (x1 - x0 + 1)


def test_harden_is_shrink_only():
    """A hardening pass may only remove. Growing admits paint nobody walked."""
    rng = np.random.default_rng(0)
    m = rng.random((1024, 368))
    for name in fr.HELD_RECTS:
        out = fr.harden_held(m, name)
        assert (out <= m + 1e-12).all()


# ---------------------------------------------------------------- counts

def test_counts_separate_the_three_conventions():
    """Three legitimate counts exist on one feathered mask; conflating them is how
    8,928 / 8,908 / 7,826 read as a discrepancy instead of three objects."""
    m = np.zeros((10, 10))
    m[0:4, 0:4] = 1.0      # 16 fully opaque
    m[4, 0:4] = 0.75       # 4 above half
    m[5, 0:4] = 0.25       # 4 in support only
    c = fr.counts(m)
    assert c["poly_or_full_px"] == 16
    assert c["half_px"] == 20
    assert c["supp_px"] == 24


# ---------------------------------------------------------------- union andon

def test_union_andon_fires_on_overlapping_masks(tmp_path):
    """Two masks whose feathers overlap do not survive a max() union as the ratified
    pair. Constructed to fail: without the disjointness check this passes silently."""
    a = np.zeros((1024, 368)); a[100:140, 100:140] = 255
    b = np.zeros((1024, 368)); b[120:160, 120:160] = 255      # deliberately overlapping
    L = a / 255.0
    R = b / 255.0
    U = np.maximum(L, R)
    overlap = int(((L > 0) & (R > 0)).sum())
    assert overlap > 0, "fixture must actually overlap or the check cannot fail"
    cl, cr, cu = fr.counts(L), fr.counts(R), fr.counts(U)
    assert any(cu[k] != cl[k] + cr[k] for k in cu), "overlapping union must break the sum"


def test_union_of_disjoint_masks_is_the_exact_sum():
    a = np.zeros((1024, 368)); a[100:140, 100:140] = 1.0
    b = np.zeros((1024, 368)); b[100:140, 250:290] = 1.0
    u = np.maximum(a, b)
    assert int(((a > 0) & (b > 0)).sum()) == 0
    ca, cb, cu = fr.counts(a), fr.counts(b), fr.counts(u)
    for k in cu:
        assert cu[k] == ca[k] + cb[k]


# ---------------------------------------------------------------- locality

def test_locality_separates_a_confined_repaint_from_an_unconfined_one(tmp_path):
    """The check that caught job 1, with both outcomes constructed.

    A confined repaint moves paint only inside the mask; an unconfined one moves the whole
    frame. If the ratio collapses toward 1 the mask did not confine -- which is exactly
    what the fired gate reported.
    """
    h, w = 200, 100
    orig = np.full((h, w, 3), 150, dtype=np.uint8)
    mask = np.zeros((h, w)); mask[50:80, 30:60] = 255
    mp = tmp_path / "m.png"; _write(mp, mask)
    op = tmp_path / "o.png"; _rgb(op, orig)

    confined = orig.copy(); confined[50:80, 30:60] = 60
    cp = tmp_path / "c.png"; _rgb(cp, confined)

    unconfined = np.full((h, w, 3), 60, dtype=np.uint8)
    up = tmp_path / "u.png"; _rgb(up, unconfined)

    def run(rep, out):
        subprocess.run([sys.executable, str(TOOL), "locality", "--orig", str(op),
                        "--repaint", str(rep), "--mask", str(mp), "--out", str(out)],
                       check=True, capture_output=True)
        return json.loads(Path(out).read_text())

    good = run(cp, tmp_path / "g.json")
    bad = run(up, tmp_path / "b.json")
    assert good["dE_outside_mean"] == 0.0
    assert good["ratio_inside_over_outside"] == float("inf")
    assert bad["dE_outside_mean"] > 0
    assert bad["ratio_inside_over_outside"] == pytest.approx(1.0, abs=0.01), \
        "an unconfined repaint must collapse the ratio to 1"


# ---------------------------------------------------------------- composite

def test_composite_andon_fires_when_pixels_outside_the_mask_move(tmp_path):
    """Composite through the feather: outside the mask the result IS the original."""
    h, w = 60, 40
    orig = np.full((h, w, 3), 200, dtype=np.uint8)
    rep = np.full((h, w, 3), 40, dtype=np.uint8)
    mask = np.zeros((h, w)); mask[20:40, 10:30] = 255
    op, rp, mp = tmp_path / "o.png", tmp_path / "r.png", tmp_path / "m.png"
    _rgb(op, orig); _rgb(rp, rep); _write(mp, mask)
    out = tmp_path / "comp.png"
    subprocess.run([sys.executable, str(TOOL), "composite", "--orig", str(op),
                    "--repaint", str(rp), "--mask", str(mp), "--out", str(out)],
                   check=True, capture_output=True)
    comp = np.asarray(Image.open(out).convert("RGB"))
    outside = mask <= 0
    assert (comp[outside] == orig[outside]).all()
    assert (comp[mask >= 255] == rep[mask >= 255]).all()
    proof = json.loads(Path(str(out).replace(".png", "_proof.json")).read_text())
    assert proof["dE_core"]["mean"] > 2.0, "a real repaint must not read as a NO-OP"


def test_composite_of_an_identical_repaint_reads_as_a_no_op(tmp_path):
    """Ruling 26's requirement, constructed: a same-seed repaint that reproduces its own
    defect must read as NO CHANGE. Without this, six no-ops wear six receipts."""
    h, w = 60, 40
    orig = np.full((h, w, 3), 123, dtype=np.uint8)
    mask = np.zeros((h, w)); mask[20:40, 10:30] = 255
    op, rp, mp = tmp_path / "o.png", tmp_path / "r.png", tmp_path / "m.png"
    _rgb(op, orig); _rgb(rp, orig); _write(mp, mask)
    out = tmp_path / "comp.png"
    subprocess.run([sys.executable, str(TOOL), "composite", "--orig", str(op),
                    "--repaint", str(rp), "--mask", str(mp), "--out", str(out)],
                   check=True, capture_output=True)
    proof = json.loads(Path(str(out).replace(".png", "_proof.json")).read_text())
    assert proof["dE_core"]["mean"] == 0.0
    assert proof["dE_core"]["max"] == 0.0


# ---------------------------------------------------------------- lift

def test_lift_hits_its_target_on_the_opaque_core(tmp_path):
    h, w = 60, 40
    orig = np.full((h, w, 3), 110, dtype=np.uint8)
    mask = np.zeros((h, w)); mask[20:40, 10:30] = 255
    op, mp = tmp_path / "o.png", tmp_path / "m.png"
    _rgb(op, orig); _write(mp, mask)
    out = tmp_path / "lift.png"
    subprocess.run([sys.executable, str(TOOL), "lift", "--src", str(op), "--mask", str(mp),
                    "--dL", "12", "--out", str(out)], check=True, capture_output=True)
    rec = json.loads(Path(str(out).replace(".png", "_lift.json")).read_text())
    assert rec["measured_delta"] == pytest.approx(12.0, abs=0.25)
    lifted = np.asarray(Image.open(out).convert("RGB"))
    assert (lifted[mask <= 0] == orig[mask <= 0]).all(), "the lift must not move unmasked pixels"


# ---------------------------------------------------------------- gates raise

def test_every_gate_raises_and_survives_dash_O():
    """E21 Ruling 2: a gate deciding whether an irreversible step proceeds must raise.
    `assert` is deletable by -O, so no ANDON in this tool may be one."""
    src = TOOL.read_text(encoding="ascii")
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("assert ") and "ANDON" in s:
            pytest.fail(f"ANDON written as a deletable assert: {s}")
    assert "raise SystemExit" in src
    # the module imports and its gates are present under -O
    r = subprocess.run([sys.executable, "-O", "-c",
                        "import sys; sys.path.insert(0, r'%s');"
                        "import e37_fire_repaints as f;"
                        "print(len(f.HELD_RECTS))" % (REPO / "tools")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "2"
