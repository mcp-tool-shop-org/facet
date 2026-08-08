"""T9 - e12_elevated at the repaired default reproduces the sword's converged
up-facing reach.

Source: E16-7's anchor (Ruling 10a). The recorded coarse run took its grid
from the generation frame and was wrong by 3.9x (13.851% against 53.920%);
the repair derives the grid from rays-per-mean-face (default 10) and the
repaired default measured 53.967% - +0.047 points against the recorded
converged 53.920%, inside ray-sampling noise.

The bound is the dispatched one - within ray-sampling noise, +-0.5 points,
E16-7's own pre-registered width. The invocation carries E16-7's correction:
the recorded framing is --fit-axis height (the prop's pinned value), not the
tool's default width - at width the same frame reads 15.013%, which is how
the record's own invocation-as-quoted failed to reproduce.

E16-7 also measured that 53.920% is NOT converged (54.849% at 40 rays/face,
still climbing) - this test pins the repaired DEFAULT's behaviour, not a
convergence claim.
"""
import json

import pytest

from conftest import need, run_py

RECORDED_CONVERGED = 53.920
NOISE_BOUND = 0.5


@pytest.mark.artifacts
@pytest.mark.slow
def test_t09_repaired_default_reaches_the_recorded_value(assets, tmp_path):
    glb = need(assets, "facet_next/E14_prep/prep_uv.glb")
    out_json = tmp_path / "elevated.json"
    rc, out, err = run_py(
        "diagnostics/e12_elevated.py",
        ["--glb", glb, "--aspect", "240,1024", "--fit-axis", "height",
         "--out", out_json],
        timeout=3600)
    assert rc == 0, "e12_elevated exited %d\n%s\n%s" % (rc, out, err)

    j = json.loads(out_json.read_text(encoding="utf-8"))
    got = j["base_up_reached_pct"]
    assert abs(got - RECORDED_CONVERGED) <= NOISE_BOUND, (
        "up-facing reach %.3f%% is outside +-%.1f of the recorded %.3f%%"
        % (got, NOISE_BOUND, RECORDED_CONVERGED))
    print("T9 up-facing reach at the repaired default: %.3f%% "
          "(recorded converged 53.920%%, E16-7 measured 53.967%%)" % got)
