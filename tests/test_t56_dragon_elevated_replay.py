"""T56 - the dragon's elevated replay: the recorded elevated.json payload
reproduces WHOLE, every float to its last digit.

E30's per-profile anchor gate for the beast's up-facing reach. The anchor is
the recorded artifact's own bytes-as-parsed - the recorded JSON is loaded and
compared as a whole object, so no number in this file is a literal someone
typed.

THE RECORDED GRID IS THE INVOCATION AND IT CAME FROM THE RECORD, not from a
sweep. E12-task2b-report.md quotes the invocation as
`e12_elevated.py --glb E12_prep/prep_uv.glb --fit-axis width` and then prints
the ray ladder that names the grid the reported number was taken at:

    896 x 512     39.286%
    1792 x 1024   48.106%   <- "the emit frame", and the value in elevated.json
    3584 x 2048   49.594%   <- and the value in elevated_4x.json

E16-7 later DERIVED the grid from rays-per-mean-face instead of inheriting it
from a generation frame, so the tool's default no longer reproduces a pre-E16
run - `--exact-grid` is the flag its own --help names for exactly this, and it
is why the invocation below carries `--aspect 1792,1024 --exact-grid`.

T9 anchors the sword's REPAIRED DEFAULT against a converged value inside a
noise bound, because the sword's recorded coarse run was wrong by 3.9x. This
anchor is the other kind and is stricter: the dragon's recorded run is pinned
exactly, as a reproduction of a recorded measurement rather than a claim that
the measurement converged. The ladder above is the record's own evidence that
48.106% is NOT converged, and nothing here says otherwise.

Read-only: --glb is the recorded mesh, --out is tmp_path. The mesh is re-hashed
afterward.
"""
import hashlib
import json

import pytest

from conftest import need, run_py

RECORDED_GRID = "1792,1024"      # E12-task2b-report.md's "the emit frame" row
FOURX_GRID = "3584,2048"         # its next rung, and elevated_4x.json


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _replay(tmp_path, glb, grid, name):
    out = tmp_path / name
    rc, txt, err = run_py(
        "diagnostics/e12_elevated.py",
        ["--glb", glb, "--aspect", grid, "--exact-grid", "--fit-axis", "width",
         "--out", out],
        timeout=3600)
    assert rc == 0, "e12_elevated exited %d\n%s\n%s" % (rc, txt, err)
    return json.loads(out.read_text(encoding="utf-8")), txt


@pytest.mark.artifacts
@pytest.mark.slow
def test_t56_dragon_elevated_reproduces_the_recorded_payload(assets, tmp_path):
    glb = need(assets, "facet_next/E12_prep/prep_uv.glb")
    rec = json.loads(
        need(assets, "facet_next/E12_prep/elevated.json")
        .read_text(encoding="utf-8"))

    before = _sha(glb)
    got, txt = _replay(tmp_path, glb, RECORDED_GRID, "elevated.json")

    # the whole payload, not a chosen field - including every `rounds` entry
    assert got == rec, (
        "the elevated payload differs from the recorded one.\n"
        "  recorded base_up_reached_pct %r\n  replay   base_up_reached_pct %r\n"
        "  differing top-level keys: %s"
        % (rec.get("base_up_reached_pct"), got.get("base_up_reached_pct"),
           sorted(k for k in set(rec) | set(got) if rec.get(k) != got.get(k))))

    # the grid is the invocation's load-bearing half; assert the tool used the
    # literal one rather than deriving its own
    assert "--exact-grid, literal --aspect" in txt, (
        "the run did not use the literal recorded grid:\n%s" % txt)

    assert _sha(glb) == before, "the recorded prep mesh changed during the replay"


@pytest.mark.artifacts
@pytest.mark.slow
def test_t56_dragon_elevated_4x_rung_reproduces(assets, tmp_path):
    """The ladder's next rung, recorded as its own artifact.

    It is what makes the anchor above a measurement rather than a fixed point:
    the two rungs differ (48.106 vs 49.594), so a replay that silently ignored
    --aspect would fail here even while passing there.
    """
    glb = need(assets, "facet_next/E12_prep/prep_uv.glb")
    rec = json.loads(
        need(assets, "facet_next/E12_prep/elevated_4x.json")
        .read_text(encoding="utf-8"))

    coarse = json.loads(
        need(assets, "facet_next/E12_prep/elevated.json")
        .read_text(encoding="utf-8"))
    # the can-fail proof, asserted on the RECORD rather than on the replay: the
    # two rungs must be different measurements, or neither test above could
    # detect a tool that ignored --aspect and answered the same thing twice
    assert rec["base_up_reached_pct"] != coarse["base_up_reached_pct"], (
        "the recorded 1x and 4x rungs carry the same reach - this pair can no "
        "longer tell a grid-sensitive tool from a grid-blind one")

    got, _ = _replay(tmp_path, glb, FOURX_GRID, "elevated_4x.json")
    assert got == rec, (
        "the 4x-grid payload differs from the recorded one.\n"
        "  recorded base_up_reached_pct %r\n  replay   base_up_reached_pct %r"
        % (rec.get("base_up_reached_pct"), got.get("base_up_reached_pct")))
