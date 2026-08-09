"""T46 - anchor_compare + the served anchor_check (E28 2c, the eighth tool).

Commissioned at E28 Ruling 10, the Director's word: at least 8 tools IF it can
be done honestly, and a forced tool is worse than no tool. The honesty
decomposition is the tool's whole design - THE TOOL COMPARES, THE CALLER
REPLAYS - and these tests pin both what it measures and what it refuses to
invent.

THE OWED FIXTURE rides in this commit: a pixel-identical, byte-different PNG
pair (tests/fixtures/measure_min/anchor/), pinning the false-halt class that
has cost this repo two halts - a byte-hash mismatch on pixel-identical
renders. The pair is SELF-VALIDATING: its own leg re-checks both properties
before any test uses it, so a regenerated fixture that lost the property
fails loudly instead of making the class untestable.
"""
import io
import json
import os
import shutil

import numpy as np
import pytest

from conftest import REPO
from measure_support import FIXTURE, call, payload, refusal

ANCHOR = os.path.join(FIXTURE, "anchor")
PAIR_A = os.path.join(ANCHOR, "pair_a.png")
PAIR_B = os.path.join(ANCHOR, "pair_b.png")


# ---------------------------------------------------------------------------
# the owed fixture, self-validating
# ---------------------------------------------------------------------------

def test_t46_the_fixture_pair_is_pixel_identical_and_byte_different():
    """The pair's own properties, re-checked before anything trusts them. A
    fixture that silently lost either half would make the false-halt class
    untestable while every downstream leg kept passing."""
    from PIL import Image
    with io.open(PAIR_A, "rb") as fh:
        a = fh.read()
    with io.open(PAIR_B, "rb") as fh:
        b = fh.read()
    assert a != b, "the pair's bytes are equal - the fixture lost its point"
    A = np.asarray(Image.open(PAIR_A).convert("RGBA"))
    B = np.asarray(Image.open(PAIR_B).convert("RGBA"))
    assert A.shape == B.shape and np.array_equal(A, B), (
        "the pair's pixels differ - it no longer isolates the encoder-"
        "metadata class")


def test_t46_the_false_halt_class_separates_at_the_served_surface():
    """The reason the tool exists: byte tier DIFFERENT, pixel tier SAME, on
    one payload - which two live halts in this repo's history could not
    tell apart."""
    doc = payload(call("anchor_check", {"a": PAIR_A, "b": PAIR_B}))
    assert doc["byte"]["byte_identical"] is False
    assert doc["pixel"]["pixel_identical"] is True
    assert doc["pixel"]["differing_pixels"] == 0
    assert "bytes are the contract" in doc["byte"]["gate_eligibility"], (
        "the byte tier's gate-eligibility caveat must travel IN the payload")


def test_t46_an_identical_pair_reads_same_on_both_tiers(tmp_path):
    dup = os.path.join(str(tmp_path), "dup.png")
    shutil.copyfile(PAIR_A, dup)
    doc = payload(call("anchor_check", {"a": PAIR_A, "b": dup}))
    assert doc["byte"]["byte_identical"] is True
    assert doc["pixel"]["pixel_identical"] is True


# ---------------------------------------------------------------------------
# the two-thresholds law: total AND largest component, plus the carried grid
# ---------------------------------------------------------------------------

def _png(path, arr):
    from PIL import Image
    Image.fromarray(arr).save(path)


def test_t46_the_grid_and_component_separate_blob_from_speckle(tmp_path):
    """Equal totals, opposite shapes: one 400-px blob against 400 scattered
    pixels. Total alone cannot tell one wrong garment from ordinary speckle -
    the record's own law - and this leg is the tool proving it can."""
    rng = np.random.default_rng(9)
    base = rng.integers(0, 200, (128, 128, 3), dtype=np.uint8)
    blob = base.copy()
    blob[40:60, 40:60] += 40
    scat = base.copy()
    flat = rng.choice(128 * 128, 400, replace=False)
    scat.reshape(-1, 3)[flat] += 40
    p0 = os.path.join(str(tmp_path), "base.png")
    pb = os.path.join(str(tmp_path), "blob.png")
    ps = os.path.join(str(tmp_path), "scat.png")
    _png(p0, base), _png(pb, blob), _png(ps, scat)

    db = payload(call("anchor_check", {"a": p0, "b": pb}))["pixel"]
    ds = payload(call("anchor_check", {"a": p0, "b": ps}))["pixel"]
    assert db["differing_pixels"] == ds["differing_pixels"] == 400, (
        "the fixture's totals must be equal or the separation proves nothing")
    assert db["largest_component_px"] >= 3 * ds["largest_component_px"], (
        "blob LCC %d vs scatter LCC %d - the component statistic no longer "
        "separates the shapes the two-thresholds law names"
        % (db["largest_component_px"], ds["largest_component_px"]))
    gb = np.array(db["shape_grid"])
    gs = np.array(ds["shape_grid"])
    assert gb.shape == gs.shape == (8, 8)
    assert gb.max() > gs.max(), (
        "the carried grid must peak higher under a concentrated difference")
    # and the grid is CARRIED, not reduced: no numeric FIELD reduces it to a
    # score. The first draft of this leg grepped the payload for the word
    # "uniformity" and fired on the note EXPLAINING why no such score exists
    # - a check written against the token rather than the specification, this
    # repo's own law. The specification is about KEYS, so keys are what is
    # scanned.
    def keys_of(o):
        if isinstance(o, dict):
            for k, v in o.items():
                yield k
                yield from keys_of(v)
        elif isinstance(o, list):
            for v in o:
                yield from keys_of(v)
    bad = [k for k in keys_of(db)
           if "uniform" in k.lower() or "score" in k.lower()]
    assert not bad, (
        "the payload grew a reduced-shape field, which is where forcing "
        "begins (Ruling 10): %s" % bad)


# ---------------------------------------------------------------------------
# refusals and the boundary
# ---------------------------------------------------------------------------

def test_t46_dimension_mismatch_names_both_sizes(tmp_path):
    rng = np.random.default_rng(1)
    p1 = os.path.join(str(tmp_path), "s64.png")
    p2 = os.path.join(str(tmp_path), "s32.png")
    _png(p1, rng.integers(0, 255, (64, 64, 3), dtype=np.uint8))
    _png(p2, rng.integers(0, 255, (32, 32, 3), dtype=np.uint8))
    err = refusal(call("anchor_check", {"a": p1, "b": p2}))
    text = err["message"] + " " + err["hint"]
    assert "64x64" in text and "32x32" in text, (
        "a dimension mismatch must name BOTH frames: %s" % text[:300])


def test_t46_a_non_image_gets_the_byte_tier_and_says_why(tmp_path):
    p = os.path.join(str(tmp_path), "notes.txt")
    with io.open(p, "w", encoding="utf-8") as fh:
        fh.write("not an image\n")
    doc = payload(call("anchor_check", {"a": p, "b": p}))
    assert doc["byte"]["byte_identical"] is True
    assert doc["pixel"]["attempted"] is False
    assert "byte tier" in doc["pixel"]["not_attempted_because"]


def test_t46_missing_input_refuses_naming_it():
    err = refusal(call("anchor_check", {"a": "no-such.png", "b": PAIR_A}))
    assert err["code"] == "PRECONDITION_MISSING"
    assert "no-such.png" in err["message"]


# ---------------------------------------------------------------------------
# the envelope and the carried boundaries
# ---------------------------------------------------------------------------

def test_t46_envelope_carries_the_replay_boundary_and_the_collision():
    doc = payload(call("anchor_check", {"a": PAIR_A, "b": PAIR_B}))
    env = doc["measure"]
    assert env["tool"] == "anchor_check"
    assert env["instrument"]["path"] == "tools/verify/anchor_compare.py"
    assert len(env["instrument"]["sha256"]) == 64
    assert doc["replay"] == "caller-supplied", (
        "the tool compares, the caller replays - the boundary must read as "
        "designed rather than forgotten (Ruling 10)")
    assert any("e13_anchor_check" in n for n in env["notes"]), (
        "the name collision migrated from the refusal into the served notes "
        "(E27 Ruling 4) and must stay carried")
    assert "pixel.differing_fraction" in env["ratios"]
    assert "pixel.largest_component_fraction_of_differing" in env["ratios"]
