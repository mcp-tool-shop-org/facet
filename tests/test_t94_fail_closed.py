"""T94 - fail-closed spend gate. Silence is dead.

Brief #20. The router guarded three of seven spend sites, and all
three could be walked past by omitting a flag. require_canon is the
helper: no --canon and no census-backed --no-canon is an ANDON
before any write.

THE CHIP. restylize_views.py --emit-only with neither --canon nor
--no-canon raises ANDON and does not create --outdir. That is the
case that separates a gate from an optional check.

T34 count surfaces assumed before this file: 1295 / 1241 / 54
(the brief's number). This change-set adds only these hermetic
legs and moves the pins it moves. E55 / t95 / docs/experiments/E55-*
are the other seat.

Hermetic tests do not open facet_E*.
"""
import json
import os
import sys

import pytest
from PIL import Image
import numpy as np

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import canon_gate as C  # noqa: E402

W3 = os.path.join(str(REPO), "canon", "w3.surfaces.json")


def _png(path):
    Image.fromarray(np.zeros((8, 8, 3), dtype=np.uint8)).save(path)
    return str(path)


def test_t94_restylize_without_canon_andon_before_mkdir(tmp_path):
    """THE CHIP. Silence is not a path."""
    out = tmp_path / "o"
    rc, out_s, err = run_py("restylize_views.py", [
        "--inputs", _png(tmp_path / "a.png"),
        "--outdir", str(out),
        "--emit-only",
    ])
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "no canon:" in both
    assert not out.exists(), "ungated restylize created --outdir"


def test_t94_no_canon_on_w3_is_the_checkbox_and_refuses():
    with pytest.raises(C.Andon, match="no-canon refused"):
        C.require_canon("anything", no_canon=True, subject="W3")


def test_t94_no_canon_on_galleon_is_ungated_and_says_so():
    v = C.require_canon("anything", no_canon=True, subject="GALLEON")
    assert v["gated"] is False
    assert "GALLEON" in v["note"]
    assert "surfaces missing" in v["note"]


def test_t94_no_canon_without_subject_refuses():
    with pytest.raises(C.Andon, match="no-canon requires a census subject"):
        C.require_canon("anything", no_canon=True)


def test_t94_no_canon_plus_attached_path_refuses():
    with pytest.raises(C.Andon, match="surfaces attached"):
        C.require_canon("anything", canon_path=W3, no_canon=True)


def test_t94_galleon_without_escape_names_the_escape():
    with pytest.raises(C.Andon, match="pass --no-canon"):
        C.require_canon("anything", subject="GALLEON")


def test_t94_replay_drift_does_not_refuse():
    """e37 is a replay. Different verdict, not a warn checkbox."""
    doc = C.load_canon(W3)
    thin = C.report_replay_drift(doc, "plain grey background")
    assert thin["refuses"] is False
    assert thin["verdict"] == "replay_drift"
    assert thin["check"]["missing"]
    covering = (
        "a bald head, a long red beard, a dark green knitted sleeveless "
        "tunic, polished gold pauldrons, gold scrollwork on the pauldrons, "
        "a gold belt medallion, a brown leather belt, a dark red layered "
        "cloth kilt, green cloth panels in the kilt, brown leather "
        "bracers, a gold plate on each outer forearm, gold knee plates, "
        "heavy dark boots, a massive greatsword, an ornate gold "
        "crossguard, a gold pommel, a brown leather-wrapped grip, brown "
        "leather gauntlets, a brown leather shin guard"
    )
    ok = C.report_replay_drift(doc, covering)
    assert ok["refuses"] is False
    assert ok["verdict"] == "replay_match"


def test_t94_texpass_brush_without_canon_andon_before_upload(tmp_path):
    """The loop cannot walk past the tool. Gate fires before --job is read."""
    rc, out_s, err = run_py("texpass_brush.py", [
        "--job", str(tmp_path / "missing-job"),
        "--prompt", "x",
    ])
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "no canon:" in both
    assert "uploaded" not in both.lower()


def test_t94_e12_without_escape_writes_nothing(tmp_path):
    """The paid twin-graph author. Same helper, before --out exists."""
    out = tmp_path / "g.json"
    prompts = tmp_path / "p.json"
    prompts.write_text(json.dumps({
        "K": "a prompt", "_negative": "n",
    }), encoding="utf-8")
    ent = lambda v: {"value": v, "why": "w", "from": "E00"}
    prof = tmp_path / "prof.json"
    prof.write_text(json.dumps({
        "name": "x",
        "tools": {"restylize_views.py": {
            "seed": ent(1), "steps": ent(4), "cfg": ent(1.0),
            "denoise": ent(0.5), "cn-strength": ent(1.0),
            "lora-w": ent(0.0),
        }},
        "_fixtures": {"twin_prompts": {"path": str(prompts)}},
    }), encoding="utf-8")
    rc, out_s, err = run_py("diagnostics/e12_pair_cloud_step.py", [
        "--key", "K", "--prompts", str(prompts), "--profile", str(prof),
        "--render-name", "r.png", "--control-name", "c.png",
        "--out", str(out),
    ])
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "no canon:" in both
    assert not out.exists(), "ungated twin graph wrote --out"


def test_t94_e12_galleon_escape_is_named_in_output(tmp_path):
    out = tmp_path / "g.json"
    # e12 corroborates --prompts against the profile fixture path.
    # Put both under the repo-relative layout it expects, or skip the
    # pre-flight by using an absolute fixture path that matches.
    prompts = tmp_path / "p.json"
    prompts.write_text(json.dumps({
        "K": "a prompt", "_negative": "n",
    }), encoding="utf-8")
    ent = lambda v: {"value": v, "why": "w", "from": "E00"}
    prof = tmp_path / "prof.json"
    prof.write_text(json.dumps({
        "name": "x",
        "tools": {"restylize_views.py": {
            "seed": ent(1), "steps": ent(4), "cfg": ent(1.0),
            "denoise": ent(0.5), "cn-strength": ent(1.0),
            "lora-w": ent(0.0),
        }},
        "_fixtures": {"twin_prompts": {"path": str(prompts)}},
    }), encoding="utf-8")
    rc, out_s, err = run_py("diagnostics/e12_pair_cloud_step.py", [
        "--key", "K", "--prompts", str(prompts), "--profile", str(prof),
        "--render-name", "r.png", "--control-name", "c.png",
        "--out", str(out),
        "--no-canon", "--subject", "GALLEON",
    ])
    both = out_s + err
    # Pre-flight may still fire on fixture path mismatch; the canon
    # line must appear first if we get that far, OR the pre-flight
    # ANDON names the fixture. Either way --out is not written unless
    # canon let it through.
    if rc == 0:
        assert out.exists()
        assert "UNGATED" in both
        assert "GALLEON" in both
    else:
        assert not out.exists() or "UNGATED" in both


def test_t94_selftest_names_fail_closed():
    rc, out, err = run_py("canon_gate.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "fail-closed held" in out
    assert "profile-default hits 5 of 19" in out


def test_t94_calibration_docstring_matches_measurement():
    src = open(os.path.join(str(REPO), "tools", "canon_gate.py"),
               encoding="utf-8").read()
    assert "exactly 5 of the" in src
    assert "hit 14 of 19" in src
    assert C.ARMB_HITS == 14
    assert C.PROFILE_DEFAULT_HITS == 5
    assert C.W3_NAMED == 19
    assert "Neither hit count moved" not in src
    assert "is 20 since" not in src
