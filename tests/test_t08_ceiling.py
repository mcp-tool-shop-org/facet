"""T8 - the e08_ceiling re-derivation: N6 and N8 exact.

Source: E16-6's anchor - WITH ITS DISPATCH CORRECTION. The E17 kickoff
repeats the E16 kickoff's conflation: "51.005%" is NOT an e08_ceiling output
(it is the 0/45/135/180/225/315 camera SET, computed by e14_atlas_anatomy
and a session script; this tool's yaws(n) can only express evenly spaced
sets). The numbers this tool actually produces, thrice-matched on the sword:

    N6 (evenly spaced six)  reachable = 1,871,948  (51.12%, handoff 2)
    N8                      reachable = 1,879,807  (51.3342%, handoff 9,
                                                    E16-6)

THE INVOCATION CARRIES ITS OWN E16-6 LESSON, learned again by this port's
first run: the recorded run's floors were BOTH 0.45 (--head-facing-min 0.45;
prop has no head exception), while the recorded ceiling.json's three
identical blocks sit under PRE-REPAIR captions reading "head 0.18" - captions
E16-6 proved false ("the output can no longer imply three measurements where
there is one"). This port first inferred its invocation from that caption and
ran the tool's defaults (0.45/0.18), which floor the 1,894,691-texel head
band at 0.18 and lift N6 to 1,946,557. Data is not a literal; the three
identical blocks ARE the floors-equal signature. At the true floors the
repaired tool collapses the settings to one block and prints the NOTE, which
this test asserts.
"""
import json

import pytest

from conftest import need, run_py

N6_REACHABLE = 1_871_948
N8_REACHABLE = 1_879_807
VALID_TEXELS = 3_661_903  # the denominator, from the recorded ceiling.json
HEAD_BAND = 1_894_691     # geometry (meta crop box), from the same record


@pytest.mark.artifacts
@pytest.mark.slow
def test_t08_n6_n8_exact(assets, tmp_path):
    prep = need(assets, "facet_next/E14_prep")
    out_json = tmp_path / "ceiling.json"
    rc, out, err = run_py(
        "diagnostics/e08_ceiling.py",
        ["--prep", prep, "--sets", "6,8", "--head-facing-min", "0.45",
         "--out-json", out_json],
        timeout=3600)
    assert rc == 0, "e08_ceiling exited %d\n%s\n%s" % (rc, out, err)

    j = json.loads(out_json.read_text(encoding="utf-8"))
    assert j["valid_texels"] == VALID_TEXELS, (
        "valid texel count moved: %d (recorded %d)"
        % (j["valid_texels"], VALID_TEXELS))
    assert j["head_band"] == HEAD_BAND, (
        "head band moved: %d (recorded %d)" % (j["head_band"], HEAD_BAND))

    # equal floors collapse the three settings to ONE measurement, said out
    # loud (E16-6's repair); select the configuration by its PROPERTY via
    # settings_index, never by caption - the tool's own lesson
    assert "the three threshold settings collapse to 1" in out, (
        "collapse NOTE missing - the floors were not equal:\n%s" % out)
    idx = j["settings_index"]
    assert len(idx) == 1 and idx[0]["facing_min"] == 0.45 \
        and idx[0]["head_facing_min"] == 0.45, (
        "settings_index is not the single 0.45/0.45 configuration: %r" % idx)

    blocks = j["settings"]
    assert len(blocks) == 1, "expected one collapsed settings block: %r" % list(blocks)
    for name, blk in blocks.items():
        assert blk["N6"]["reachable"] == N6_REACHABLE, (
            "settings %r: N6 %d != recorded %d"
            % (name, blk["N6"]["reachable"], N6_REACHABLE))
        assert blk["N8"]["reachable"] == N8_REACHABLE, (
            "settings %r: N8 %d != recorded %d"
            % (name, blk["N8"]["reachable"], N8_REACHABLE))
    print("T8 settings block checked: %s" % ", ".join(sorted(blocks)))
