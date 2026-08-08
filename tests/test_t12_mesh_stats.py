"""T12 - mesh_stats warns on the honest condition and on nothing else.

Source: E16 Ruling 2 (the E16-5 halt, ruled). The dispatch's original anchor
contradicted itself on the measured data - the sword starts warning AND
galleon/beast stop - and the executor halted rather than tune. The ruling
resolved it at the honest condition ALONE: `rect_frac_of_figure > 1` (a face
rect larger than the figure's own silhouette cannot be a face readout); the
`up_axis_dominant` proxy leg goes (a tip-standing prop passes it, a ship and
a dragon fail it for being the shape they are); the subject-class question
lives in the profiles.

ANCHOR, pre-stated by the ruling from the measured table (every value
unchanged; warning states):

    W3        rect_frac 0.680787   silent
    galleon   rect_frac 0.327707   silent   (the proxy used to fire here)
    beast     rect_frac 0.568773   silent   (and here)
    longsword rect_frac 1.902512   WARNS

The galleon/beast rows are this test's can-fail proof in both directions: a
reintroduced proxy leg fires on them (silence asserted), and a deleted
warning goes silent on the sword (firing asserted).
"""
import json

import pytest

from conftest import need, run_py

# label -> (mesh path under FACET_ASSETS, ruled rect_frac, warns)
SUBJECTS = {
    "W3": ("facet_E06/C1/prep/prep_uv.glb", 0.680787, False),
    "galleon": ("facet_next/E04_shipprep/prep_uv.glb", 0.327707, False),
    "beast": ("facet_next/E12_prep/prep_uv.glb", 0.568773, False),
    "longsword": ("facet_next/E14_prep/prep_uv.glb", 1.902512, True),
}


@pytest.mark.artifacts
@pytest.mark.slow
def test_t12_honest_warning_condition(assets, tmp_path):
    labels = list(SUBJECTS)
    glbs = [need(assets, SUBJECTS[l][0]) for l in labels]
    out_json = tmp_path / "mesh_stats.json"
    rc, out, err = run_py(
        "verify/mesh_stats.py",
        ["--glb", *glbs, "--label", *labels, "--out", out_json],
        timeout=3600)
    assert rc == 0, "mesh_stats exited %d\n%s\n%s" % (rc, out, err)

    # the proxy leg is gone - its message must not appear for ANY subject
    assert "vertical extent is not the largest" not in out, (
        "the up-axis proxy warning fired - the proxy leg is back:\n%s" % out)

    rows = {r["label"]: r
            for r in json.loads(out_json.read_text(encoding="utf-8"))["meshes"]}
    for label, (rel, ruled_frac, warns) in SUBJECTS.items():
        r = rows[label]
        assert abs(r["rect_frac_of_figure"] - ruled_frac) < 5e-6, (
            "%s rect_frac %f != ruled %f" % (label, r["rect_frac_of_figure"], ruled_frac))
        fired = ("WARNING %s: the front-view face rect covers" % label) in out
        assert fired == warns, (
            "%s: warning %s, ruled anchor says %s\n%s"
            % (label, "fired" if fired else "silent",
               "WARNS" if warns else "silent", out))
    # the field the proxy read stays in the JSON, value untouched (the repair
    # moved the warning leg, not the measurement)
    assert all("up_axis_dominant" in r for r in rows.values())
