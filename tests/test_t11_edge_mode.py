"""T11 - the edge-mode default is byte-identical: stroke 1's recorded commit
reproduced at `global`; `--edge-mode local` parses and runs.

Source: E16-10's anchor (Ruling 24c, the A3 port as an OPT-IN flag). The
default `global` must remain byte-identical to every commit this route has
made; `local` is adopted nowhere and its delta is REPORTED, never asserted.

THE OPERANDS, identified the hard way by this port's first run (check what
the operands are - the repo's own law):

  * the pre-stroke state is run/state's three files (the stage1b projection
    + demotion + garnet reprojection; run/state/atlas.png is byte-identical
    to s1b/atlas.prev.png, which is the record's own copy of the pre-commit
    atlas);
  * the job is s1b's OWN job_y+000_e+00 (emitted 2026-08-08 02:58 from the
    post-garnet state). The job under run/state (emitted 02:02, post-
    demotion pre-garnet) is stroke 1-A's, abandoned - committing its
    inpaint writes 5,416 texels, not the recorded 4,344;
  * s1b/atlas.png as recorded is POST-collar-repair (E14 Ruling 28d rewrote
    it; collar_repair.json pins both shas), so the raw commit's atlas is
    asserted against the sidecar's own `atlas_sha256_before` rather than
    the file. holes/styled_mask/atlas.prev are untouched by the repair and
    compare byte-for-byte.

This asserts strictly more of the record than E16-10's own anchor did (its
"all four byte-identical" was replay-vs-replay across the tool edit; the
log lines were its record anchor).
"""
import hashlib
import json
import re

import pytest

from conftest import copy_state, need, run_py

COMMIT_LINES = [
    "[commit] trust mask AND geometry: 32,040 -> 32,040 px (-0 keyed on no surface)",
    "[commit] wrote 4,344 texels; holes 2,005,056 -> 2,000,712",
]
BYTE_OUTPUTS = ["holes.png", "styled_mask.npy", "atlas.prev.png"]


def _commit(assets, state_dir, extra=()):
    prep = need(assets, "facet_next/E14_prep")
    job = need(assets, "facet_next/E14_strokes/run/s1b/job_y+000_e+00")
    return run_py(
        "texpass_iter.py",
        ["commit", "--profile", "profiles/prop.json",
         "--state", state_dir, "--prep", prep,
         "--edited", job / "inpainted.png", "--cam", job / "cam.json",
         *extra],
        timeout=1800)


@pytest.mark.artifacts
def test_t11_default_reproduces_stroke1(assets, tmp_path):
    state_src = need(assets, "facet_next/E14_strokes/run/state")
    s1b = need(assets, "facet_next/E14_strokes/run/s1b")
    repair = json.loads(
        need(assets, "facet_next/E14_strokes/run/s1b/collar_repair.json")
        .read_text(encoding="utf-8"))
    state = copy_state(state_src, tmp_path / "state")

    rc, out, err = _commit(assets, state)
    assert rc == 0, "commit exited %d\n%s\n%s" % (rc, out, err)
    for line in COMMIT_LINES:
        assert line in out, "recorded commit line missing:\n want %r\n got:\n%s" % (line, out)

    mismatched = [n for n in BYTE_OUTPUTS
                  if (state / n).read_bytes() != (s1b / n).read_bytes()]
    assert not mismatched, (
        "outputs differ from the recorded s1b: %s" % ", ".join(mismatched))

    got_atlas = hashlib.sha256((state / "atlas.png").read_bytes()).hexdigest()
    assert got_atlas == repair["atlas_sha256_before"], (
        "raw commit atlas %s != the collar repair's recorded pre-repair sha %s"
        % (got_atlas, repair["atlas_sha256_before"]))


@pytest.mark.artifacts
def test_t11_local_mode_parses_and_runs(assets, tmp_path):
    state = copy_state(need(assets, "facet_next/E14_strokes/run/state"),
                       tmp_path / "state_local")
    rc, out, err = _commit(assets, state, extra=["--edge-mode", "local"])
    assert rc == 0, "--edge-mode local did not run (rc %d)\n%s\n%s" % (rc, out, err)
    m = re.search(r"wrote ([\d,]+) texels", out)
    assert m, "no commit line in local-mode output:\n%s" % out
    # REPORTED, not asserted (the mode is adopted nowhere; E16-10 measured
    # +30.6% on this stroke, concentrated in the thinnest strata)
    print("T11 --edge-mode local wrote %s texels (default wrote 4,344)" % m.group(1))
