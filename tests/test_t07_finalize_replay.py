"""T7 - the finalize replay: atlas_final.png byte-identical on the sword's
recorded run/final inputs.

Source: E16-3's anchor (Ruling 31d.1). The anchor is the recorded artifact's
OWN BYTES - the replay's output is compared file-to-file, no sha literal in
test code. E16-3 replayed this twice today (tool before and after its print
change), both byte-identical to the record.

texpass_finalize reads --state and writes only --out/--json (E16-3 audited
every write before touching the recorded run), so the recorded tree is used
in place as the read-only state; the test re-hashes the three inputs
afterward to prove the citable tree did not move.
"""
import hashlib

import pytest

from conftest import need, run_py


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t07_finalize_reproduces_the_recorded_atlas(assets, tmp_path):
    prep = need(assets, "facet_next/E14_prep")
    final = need(assets, "facet_next/E14_strokes/run/final")
    recorded = need(assets, "facet_next/E14_strokes/run/final/atlas_final.png")

    inputs = {n: _sha(final / n)
              for n in ("atlas.png", "holes.png", "styled_mask.npy")}

    out_png = tmp_path / "atlas_final.png"
    out_json = tmp_path / "finalize.json"
    rc, out, err = run_py(
        "texpass_finalize.py",
        ["--state", final, "--prep", prep, "--surface-aware",
         "--out", out_png, "--json", out_json])
    assert rc == 0, "finalize exited %d\n%s\n%s" % (rc, out, err)

    assert out_png.read_bytes() == recorded.read_bytes(), (
        "atlas_final.png is not byte-identical to the recorded artifact "
        "(replay sha %s, recorded %s)" % (_sha(out_png), _sha(recorded)))

    # the citable tree was read, never written
    after = {n: _sha(final / n)
             for n in ("atlas.png", "holes.png", "styled_mask.npy")}
    assert after == inputs, "the recorded run/final inputs changed during the replay"

    # reported, not asserted: the sidecar json against the recorded one (the
    # dispatch anchors the atlas; the json's mean_fallback field is E16-3's
    # own flagged-not-fixed structural zero, queued for the advisor)
    rec_json = final / "finalize.json"
    same = out_json.read_bytes() == rec_json.read_bytes()
    print("T7 finalize.json vs recorded: %s" % ("byte-identical" if same else "DIFFERS"))
