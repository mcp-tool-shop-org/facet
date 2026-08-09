"""T52 - the dragon's finalize replay: dragon_final.png byte-identical on the
recorded E13_stroke run/state.

E30's per-profile anchor gate for the beast exemplar, to T7's shape. The anchor
is the recorded artifact's OWN BYTES; no sha256 literal appears here.

THE MODE IS IN THE RECORD: run/finalize.json opens `"mode": "surface_aware"`,
so --surface-aware is part of the recorded invocation. Its hole_texels
1,710,180 is exactly the hole count of run/state/holes.png, which is what fixes
run/state as the input.

WHICH DIRECTORY IS THE INPUT MATTERS HERE AND WAS MEASURED, not inherited. The
tree also carries run/state_final/, whose holes.png and styled_mask.npy are
byte-identical to run/state's but whose atlas.png is byte-identical to
dragon_final.png - it is the POST-finalize state, so finalize's output was
written into it and the pre-finalize atlas there is gone. Anchoring against
state_final's atlas would have compared the recorded output to itself. run/state
is the one directory that still holds the input atlas.

The sidecar is compared byte-for-byte beside the atlas (bytes are the contract
for a json.dump of eleven numbers), and the atlas is pixel-identical as well -
measured, 0 differing pixels of 16,777,216.

The tool reads --state/--prep and writes only --out/--json, both in tmp_path;
the recorded state's three files are re-hashed afterward.
"""
import hashlib

import pytest

from conftest import need, run_py

STATE_FILES = ("atlas.png", "holes.png", "styled_mask.npy")


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t52_dragon_finalize_reproduces_the_recorded_atlas(assets, tmp_path):
    state = need(assets, "facet_next/E13_stroke/run/state")
    prep = need(assets, "facet_next/E12_prep")
    recorded = need(assets, "facet_next/E13_stroke/run/dragon_final.png")
    rec_json = need(assets, "facet_next/E13_stroke/run/finalize.json")

    inputs = {n: _sha(state / n) for n in STATE_FILES}

    out_png = tmp_path / "dragon_final.png"
    out_json = tmp_path / "finalize.json"
    rc, out, err = run_py(
        "texpass_finalize.py",
        ["--state", state, "--prep", prep, "--surface-aware",
         "--out", out_png, "--json", out_json])
    assert rc == 0, "finalize exited %d\n%s\n%s" % (rc, out, err)

    assert "surface-aware" in out, (
        "the replay did not run the mode the recorded sidecar declares "
        "(mode: surface_aware):\n%s" % out)

    assert out_png.read_bytes() == recorded.read_bytes(), (
        "the dragon's final atlas is not byte-identical to the recorded "
        "artifact (replay sha %s, recorded %s)"
        % (_sha(out_png), _sha(recorded)))
    assert out_json.read_bytes() == rec_json.read_bytes(), (
        "the finalize sidecar differs from the recorded one:\n replay %s\n "
        "recorded %s" % (out_json.read_text(encoding="utf-8"),
                         rec_json.read_text(encoding="utf-8")))

    after = {n: _sha(state / n) for n in STATE_FILES}
    assert after == inputs, "the recorded run/state changed during the replay"


@pytest.mark.artifacts
def test_t52_state_final_is_the_post_finalize_copy(assets):
    """The premise the anchor above rests on, kept runnable rather than stated.

    If a future session points a dragon replay at run/state_final, this fires
    and names why: that directory's atlas IS the recorded output.
    """
    state = need(assets, "facet_next/E13_stroke/run/state")
    final_state = need(assets, "facet_next/E13_stroke/run/state_final")
    recorded = need(assets, "facet_next/E13_stroke/run/dragon_final.png")

    for n in ("holes.png", "styled_mask.npy"):
        assert (state / n).read_bytes() == (final_state / n).read_bytes(), (
            "run/state and run/state_final disagree on %s - state_final is no "
            "longer a copy of the finalize input" % n)
    assert (final_state / "atlas.png").read_bytes() == recorded.read_bytes(), (
        "run/state_final/atlas.png is no longer the recorded dragon_final.png")
    assert (state / "atlas.png").read_bytes() != recorded.read_bytes(), (
        "run/state/atlas.png has become the finalized atlas - the pre-finalize "
        "input is gone and T52's anchor has no operand")
