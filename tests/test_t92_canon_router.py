"""T92 - the canon router. Schema 2. Both directions. Every spend site.

Brief #18. canon_gate.py was a checker with a CLI. The router is the
component every consumer asks: for THIS subject, at THIS scope, is
this prompt covered? It refuses when the answer is not covered, and
it refuses when there is no answer at all.

THE CHIP. A prompt that covers every ratified W3 phrase and also
contains `gold necklace` is refused as unlicensed. E08 named the
class (docs/experiments/E08-ruling-gate0.md:940-945): the prompt
says gold necklace; the canon has a gold belt medallion. Forward
coverage is blind to it. Reverse is not.

The worksheet is t93 (tools/canon_worksheet.py). This file is the
router. Kind templates, occupant filling, and spatial binding
landed in that change-set.

T34 count surfaces are contested (a second seat holds t93 / E53).
This change-set assumes the pre-t92 collect 1266 / 1212 / 54 and
does not reconcile those pins.

Hermetic tests do not open facet_E*.
"""
import json
import os
import sys

import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import canon_gate as C  # noqa: E402

W3 = os.path.join(str(REPO), "canon", "w3.surfaces.json")
SWORD = os.path.join(str(REPO), "canon", "longsword.surfaces.json")
CHAR = os.path.join(str(REPO), "profiles", "character.json")

RATIFIED_PROMPT = (
    "a bald head, a long red beard, a dark green knitted sleeveless "
    "tunic, polished gold pauldrons, gold scrollwork on the pauldrons, "
    "a gold belt medallion, a brown leather belt, a dark red layered "
    "cloth kilt, green cloth panels in the kilt, brown leather "
    "bracers, a gold plate on each outer forearm, gold knee plates, "
    "heavy dark boots, a massive greatsword, an ornate gold "
    "crossguard, a gold pommel, a brown leather-wrapped grip, brown "
    "leather gauntlets, a brown leather shin guard"
)


def test_t92_gold_necklace_on_covering_w3_is_unlicensed():
    """THE CHIP. Covering + gold necklace refuses on the reverse, not the forward."""
    doc = C.load_canon(W3)
    assert doc["schema"] == 2
    covering = C.check_prompt(doc, RATIFIED_PROMPT)
    assert covering["ok"], covering
    assert covering["unlicensed"] == []
    chk = C.check_prompt(doc, RATIFIED_PROMPT + ", gold necklace")
    assert not chk["ok"], chk
    assert chk["missing"] == []
    assert chk["forbidden"] == []
    assert any("gold necklace" in u["span"] for u in chk["unlicensed"]), chk


def test_t92_skirt_on_covering_w3_is_unlicensed():
    """The other live default lie: skirt after the garment was ruled a kilt."""
    doc = C.load_canon(W3)
    chk = C.check_prompt(doc, RATIFIED_PROMPT + ", skirt")
    assert not chk["ok"]
    assert any("skirt" in u["span"] for u in chk["unlicensed"]), chk


def test_t92_style_clauses_on_covering_w3_are_licensed():
    styled = (RATIFIED_PROMPT
              + ", plain grey background, visible brushstrokes, "
                "painterly worked surface, a burly bald warrior, holding")
    chk = C.check_prompt(C.load_canon(W3), styled)
    assert chk["ok"], chk


def test_t92_schema_1_does_not_arm_reverse():
    """Can-fail: if reverse ran on schema 1, longsword style words would refuse."""
    doc = C.load_canon(SWORD)
    assert doc["schema"] == 1
    assert "legal_clauses" not in doc
    chk = C.check_prompt(doc, C._profile_restylize_prompt("profiles/prop.json"))
    assert chk["ok"], chk
    assert chk["unlicensed"] == []


def test_t92_stale_consumer_refuses_schema_3(tmp_path):
    p = tmp_path / "x.surfaces.json"
    p.write_text(json.dumps({
        "subject": "X", "kind": "prop", "schema": 3,
        "surfaces": [{"id": "blade", "occupant": None}],
    }), encoding="utf-8")
    with pytest.raises(C.Andon) as ei:
        C.load_canon(str(p))
    assert "stale consumer" in str(ei.value)


def test_t92_resolve_w3_and_galleon():
    path = C.resolve_subject("W3")
    assert os.path.normcase(path) == os.path.normcase(W3)
    with pytest.raises(C.Andon) as ei:
        C.resolve_subject("GALLEON")
    assert "identity exists, surfaces missing" in str(ei.value)
    with pytest.raises(C.Andon) as ei:
        C.resolve_subject("no-such-subject")
    assert "unknown subject" in str(ei.value)


def test_t92_undeclared_view_is_no_answer():
    """W3 scopes.views is empty. Asking for a view is a named refusal."""
    doc = C.load_canon(W3)
    with pytest.raises(C.Andon) as ei:
        C.check_prompt(doc, RATIFIED_PROMPT, scope="view:0")
    assert "no view scope 0" in str(ei.value)


def test_t92_declared_view_does_not_require_out_of_scope(tmp_path):
    """Also E59 Stage 0's pytest-level home, extended in place rather than as
    a new function: T34 pins the collected-item count across 8 READMEs +
    SHIP_GATE.md + site-config.ts + handbook pages, and a new collected test
    would force a translation regeneration, which is out of a Sonnet
    session's authority (the studio's translation rule). Same reasoning E58
    used to extend test_t91_census_does_not_invent_surfaces in place instead
    of adding a function. The can-fail assertions for the new behaviour also
    live in tools/canon_gate.py's own `_selftest_router`, exercised by
    test_t92_selftest_still_holds below — this is the second, pytest-idiom
    layer, not the only one.
    """
    p = tmp_path / "x.surfaces.json"
    p.write_text(json.dumps({
        "subject": "X", "kind": "prop", "schema": 2,
        "legal_clauses": [
            {"id": "bg", "phrase": "plain grey background", "class": "style"},
            {"id": "pose", "phrase": "head facing straight ahead",
             "class": "staging", "required": True},
        ],
        "scopes": {"views": {"0": {"surfaces": ["blade"]}}, "strokes": {}},
        "surfaces": [
            {"id": "blade", "occupant": {
                "id": "P1", "phrase": "a steel blade", "provenance": "prompt"}},
            {"id": "grip", "occupant": {
                "id": "P2", "phrase": "a leather grip", "provenance": "prompt"}},
        ],
    }), encoding="utf-8")
    doc = C.load_canon(str(p))
    chk = C.check_prompt(doc, "a steel blade, plain grey background, "
                              "head facing straight ahead",
                         scope="view:0")
    assert chk["ok"], chk
    thin = C.check_prompt(doc, "plain grey background, head facing straight ahead",
                          scope="view:0")
    assert not thin["ok"]
    assert any("steel blade" in m["phrase"] for m in thin["missing"])

    # (a) the required clause ("pose"), stripped -> refuses naming it, even
    # at a NARROW view:0 scope that already excludes "grip" -- a legal_clause
    # names no surface id, so scope-narrowing (which narrows by surface id)
    # cannot honestly exempt it. This is the missing-required-clause half.
    no_pose = C.check_prompt(doc, "a steel blade, plain grey background",
                             scope="view:0")
    assert not no_pose["ok"], no_pose
    assert any(m["phrase"] == "head facing straight ahead"
               for m in no_pose["missing"]), no_pose

    # (b) the UNMARKED clause ("bg"), stripped -> still ok. Without this half
    # a change that made every legal_clause mandatory by accident would pass
    # (a) and go unnoticed here and on W3's five unmarked clauses alike.
    no_bg = C.check_prompt(doc, "a steel blade, head facing straight ahead",
                           scope="view:0")
    assert no_bg["ok"], no_bg


def test_t92_w3_occupants_were_not_edited():
    """Schema 2 added keys. Ratified occupant phrases did not move."""
    doc = json.loads(open(W3, encoding="utf-8").read())
    by_id = {s["id"]: (s.get("occupant") or {}).get("phrase")
             for s in doc["surfaces"]}
    assert by_id["scalp"] == "a bald head"
    assert by_id["kilt"] == "a dark red layered cloth kilt"
    assert by_id["belt_front"] == "a gold belt medallion"
    assert by_id["grip"] == "a brown leather-wrapped grip"
    assert "necklace" not in json.dumps(by_id)
    assert doc["schema"] == 2
    assert "legal_clauses" in doc
    assert doc["scopes"]["views"] == {}
    assert doc["scopes"]["strokes"] == {}


def test_t92_cli_resolve_and_check():
    rc, out, err = run_py("canon_gate.py", ["resolve", "--subject", "W3"])
    assert rc == 0, err
    assert os.path.normcase(out.strip()) == os.path.normcase(W3)
    rc, out, err = run_py("canon_gate.py", [
        "check", "--subject", "W3",
        "--prompt", RATIFIED_PROMPT + ", gold necklace",
    ])
    assert rc == 2
    both = out + err
    assert "ANDON" in both
    assert "unlicensed" in both
    assert "gold necklace" in both


def test_t92_brush_cloud_step_writes_nothing_on_necklace(tmp_path):
    """The paid spend site. Router fires before --out exists."""
    out = tmp_path / "g.json"
    prompts = tmp_path / "prompts.json"
    prompts.write_text(json.dumps({
        "K": RATIFIED_PROMPT + ", gold necklace",
        "_negative": "n",
    }), encoding="utf-8")
    prof = tmp_path / "p.json"
    ent = lambda v: {"value": v, "why": "w", "from": "E00"}
    prof.write_text(json.dumps({
        "name": "x",
        "tools": {"texpass_brush.py": {
            "seed": ent(770700), "steps": ent(20), "cfg": ent(2.5),
            "cn-strength": ent(1.0), "lora-w": ent(0.75),
            "prompt": ent("x"), "negative": ent("n"),
        }},
        "_fixtures": {
            "canon": {"path": W3},
            "brush_prompts": {"path": str(prompts)},
        },
    }), encoding="utf-8")
    job = tmp_path / "job"
    job.mkdir()
    rc, out_s, err = run_py("brush_cloud_step.py", [
        "graph", "--job", str(job), "--key", "K",
        "--prompts", str(prompts), "--out", str(out),
        "--profile", str(prof),
    ], cwd=str(REPO))
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "canon does not cover" in both
    assert "gold necklace" in both
    assert not out.exists(), "refused graph wrote --out"


def test_t92_no_canon_on_cloud_step_is_fail_closed(tmp_path):
    """MOVED ON PURPOSE 2026-08-17 (t94). A profile without a canon
    fixture used to write the graph. Silence is dead: it now ANDON's
    and --out is not written. The named escape is --no-canon plus a
    census identity-only subject.
    """
    out = tmp_path / "g.json"
    prompts = tmp_path / "prompts.json"
    prompts.write_text(json.dumps({
        "K": "anything", "_negative": "n",
    }), encoding="utf-8")
    ent = lambda v: {"value": v, "why": "w", "from": "E00"}
    prof = tmp_path / "p.json"
    prof.write_text(json.dumps({
        "name": "x",
        "tools": {"texpass_brush.py": {
            "seed": ent(770700), "steps": ent(20), "cfg": ent(2.5),
            "cn-strength": ent(1.0), "lora-w": ent(0.75),
            "prompt": ent("x"), "negative": ent("n"),
        }},
        "_fixtures": {"brush_prompts": {"path": str(prompts)}},
    }), encoding="utf-8")
    job = tmp_path / "job"
    job.mkdir()
    rc, out_s, err = run_py("brush_cloud_step.py", [
        "graph", "--job", str(job), "--key", "K",
        "--prompts", str(prompts), "--out", str(out),
        "--profile", str(prof),
    ], cwd=str(REPO))
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "no canon:" in both
    assert not out.exists(), "ungated graph wrote --out"


def test_t92_selftest_still_holds():
    rc, out, err = run_py("canon_gate.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "profile-default hits 5 of 19" in out, out
    assert "router reverse held" in out, out
    # E59 Stage 0: _selftest_router's own required-clause fixture ran and
    # held (both halves - required refuses, unmarked stays optional). This
    # is the pytest-visible seam onto the in-tool can-fail checks.
    assert "required clause held" in out, out


def test_t92_worksheet_landed_in_t93():
    """#18 fenced the generator so the router could prove the schema first.
    #19 commissioned it. The pin moves on purpose; t93 owns the legs."""
    assert os.path.isfile(
        os.path.join(str(REPO), "tools", "canon_worksheet.py"))
