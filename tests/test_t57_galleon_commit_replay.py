"""T57 - the galleon's write-head replay: the recorded selftest commit
reproduces all four state files byte-identically.

E30's per-profile anchor gate for the ship's commit, built to T11's shape. The
anchor is the recorded post-state's OWN BYTES; no sha256 literal appears here.

THE PRE/POST PAIR WAS ESTABLISHED BY ARITHMETIC, NOT BY THE FILENAMES, and not
by running the tool and seeing what matched:

  * bindcheck/     holes 1,963,858   styled 1,147,959   <- the pre-state
  * selftest_state holes 1,932,277   styled 1,179,540   <- the post-state
                        -31,581           +31,581

  Holes lost equals styled gained, exactly, and 31,581 is the number
  E04-stroke-frame-halt.md records for that selftest ("31,581 committed"). The
  conservation identity holds from bindcheck's counts to selftest_state's and
  would not hold from any other state in the tree. selftest_state/atlas.prev.png
  is byte-identical to bindcheck/atlas.png, which is the commit's own record of
  what it was handed.

  The tree also carries selftest2/, a SECOND commit from the same pre-atlas
  landing 31,418 texels. It is a different run under a condition this session
  did not identify, so it is named here and NOT anchored - an anchor whose
  invocation is unknown is not an anchor.

WHAT THE EDITED IMAGE IS. `texpass_iter selftest` emits, fake-inpaints by local
blur, then commits, all in one process; the fake_inpaint.png it produced is on
disk in the recorded job directory, so this test replays the COMMIT half alone
against that recorded input. That keeps the anchor to T11's shape - a recorded
edited image and a recorded cam against a recorded post-state - instead of
re-running a mode that would re-emit and overwrite state.

The recorded state is COPIED to tmp_path before the commit runs (commit is a
write-head; it mutates its --state), and bindcheck's three files plus the job's
two are re-hashed afterward.
"""
import hashlib

import pytest

from conftest import copy_state, need, run_py

STATE_FILES = ("atlas.png", "holes.png", "styled_mask.npy")
COMMIT_LINES = [
    "[commit] trust mask AND geometry: 234,653 -> 234,653 px (-0 keyed on no surface)",
    "[commit] wrote 31,581 texels; holes 1,963,858 -> 1,932,277",
]
POST_FILES = ("atlas.png", "holes.png", "styled_mask.npy", "atlas.prev.png")


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.mark.artifacts
@pytest.mark.slow
def test_t57_galleon_selftest_commit_reproduces(assets, tmp_path):
    pre = need(assets, "facet_next/E04_stroke/bindcheck")
    post = need(assets, "facet_next/E04_stroke/selftest_state")
    job = need(assets, "facet_next/E04_stroke/selftest_state/selftest_y+300_e+00")
    prep = need(assets, "facet_next/E04_shipprep")
    edited = need(assets,
                  "facet_next/E04_stroke/selftest_state/selftest_y+300_e+00/"
                  "fake_inpaint.png")

    pre_in = {n: _sha(pre / n) for n in STATE_FILES}
    job_in = {n: _sha(job / n) for n in ("fake_inpaint.png", "cam.json")}

    # the pairing's own premise, kept runnable: the commit that produced the
    # post-state was handed the pre-state's atlas
    assert (post / "atlas.prev.png").read_bytes() == (pre / "atlas.png").read_bytes(), (
        "selftest_state/atlas.prev.png is no longer bindcheck/atlas.png - the "
        "recorded pre/post pair this anchor rests on has moved")

    state = copy_state(pre, tmp_path / "state")
    rc, out, err = run_py(
        "texpass_iter.py",
        ["commit", "--profile", "profiles/ship.json", "--state", state,
         "--prep", prep, "--edited", edited, "--cam", job / "cam.json"],
        timeout=1800)
    assert rc == 0, "commit exited %d\n%s\n%s" % (rc, out, err)

    for line in COMMIT_LINES:
        assert line in out, (
            "recorded commit line missing:\n want %r\n got:\n%s" % (line, out))

    mismatched = ["%s (replay %s, recorded %s)"
                  % (n, _sha(state / n)[:16], _sha(post / n)[:16])
                  for n in POST_FILES
                  if (state / n).read_bytes() != (post / n).read_bytes()]
    assert not mismatched, (
        "outputs differ from the recorded selftest_state:\n  "
        + "\n  ".join(mismatched))

    assert {n: _sha(pre / n) for n in STATE_FILES} == pre_in, (
        "the recorded bindcheck pre-state changed during the replay")
    assert {n: _sha(job / n) for n in ("fake_inpaint.png", "cam.json")} == job_in, (
        "the recorded selftest job inputs changed during the replay")


@pytest.mark.artifacts
def test_t57_the_pre_state_is_fixed_by_conservation(assets):
    """Why bindcheck is the pre-state, as a check rather than as a paragraph.

    Holes lost must equal styled gained, from bindcheck's counts to
    selftest_state's. If a future edit repoints this anchor at a different
    directory, this fires before the replay does.
    """
    import numpy as np
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None

    pre = need(assets, "facet_next/E04_stroke/bindcheck")
    post = need(assets, "facet_next/E04_stroke/selftest_state")

    def holes(d):
        return int((np.asarray(Image.open(d / "holes.png").convert("L")) > 0).sum())

    def styled(d):
        return int(np.load(str(d / "styled_mask.npy")).sum())

    dh = holes(pre) - holes(post)
    ds = styled(post) - styled(pre)
    assert dh == ds == 31581, (
        "the recorded ladder no longer reads bindcheck -> selftest_state: "
        "holes fell %d, styled rose %d, E04-stroke-frame-halt.md records 31,581"
        % (dh, ds))
