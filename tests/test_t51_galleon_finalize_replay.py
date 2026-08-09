"""T51 - the galleon's finalize replay: galleon_final.png byte-identical on the
recorded E04_stroke state.

E30's per-profile anchor gate for the ship exemplar, to T7's shape. The anchor
is the recorded artifact's OWN BYTES; no sha256 literal appears here.

THE MODE IS IN THE RECORD, in the ship's own sidecar rather than in a report:
out/finalize.json opens `"mode": "atlas_flood"`, so the recorded run is the
DEFAULT flood and --surface-aware is absent. The same sidecar carries
hole_texels 1,750,006, which is exactly the hole count of state/holes.png - the
identity that fixes WHICH state directory was the input, without inheriting it
from a sentence.

The whole sidecar is compared too, and it is compared BYTE-FOR-BYTE against the
recorded one rather than field-by-field: this artifact's bytes are the contract
(five integers and a float written by json.dump in the same tool), which is the
class anchor_compare's byte tier names as gate-eligible. The atlas beside it is
also byte-compared, and it is pixel-identical as well - measured, 0 differing
pixels of 16,777,216.

texpass_finalize reads --state/--prep and writes only --out/--json, both in
tmp_path; the recorded state's three files are re-hashed afterward.
"""
import hashlib

import pytest

from conftest import need, run_py

STATE_FILES = ("atlas.png", "holes.png", "styled_mask.npy")


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t51_galleon_finalize_reproduces_the_recorded_atlas(assets, tmp_path):
    state = need(assets, "facet_next/E04_stroke/state")
    prep = need(assets, "facet_next/E04_shipprep")
    recorded = need(assets, "facet_next/E04_stroke/out/galleon_final.png")
    rec_json = need(assets, "facet_next/E04_stroke/out/finalize.json")

    inputs = {n: _sha(state / n) for n in STATE_FILES}

    out_png = tmp_path / "galleon_final.png"
    out_json = tmp_path / "finalize.json"
    rc, out, err = run_py(
        "texpass_finalize.py",
        ["--state", state, "--prep", prep, "--out", out_png, "--json", out_json])
    assert rc == 0, "finalize exited %d\n%s\n%s" % (rc, out, err)

    assert "atlas-space flood" in out, (
        "the replay did not run the mode the recorded sidecar declares "
        "(mode: atlas_flood):\n%s" % out)

    assert out_png.read_bytes() == recorded.read_bytes(), (
        "the galleon's final atlas is not byte-identical to the recorded "
        "artifact (replay sha %s, recorded %s)"
        % (_sha(out_png), _sha(recorded)))
    assert out_json.read_bytes() == rec_json.read_bytes(), (
        "the finalize sidecar differs from the recorded one:\n replay %s\n "
        "recorded %s" % (out_json.read_text(encoding="utf-8"),
                         rec_json.read_text(encoding="utf-8")))

    after = {n: _sha(state / n) for n in STATE_FILES}
    assert after == inputs, "the recorded E04_stroke state changed during the replay"
