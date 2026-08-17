"""T93 - the canon worksheet. Kind templates. Unable to fill an occupant.

Brief #19. The router (#18, t92) proved the schema. This file is the
authoring half: kind templates so a hole is a row, IDENTITY phrases
as inventory, spatial bind by surface id, element-count readout.

THE CHIP. emit(kind=humanoid, identity=W3-IDENTITY.md) produces a
worksheet whose every occupant phrase is empty, and all 19 NAMED
rows sit in inventory with assigned=null. Forward coverage of those
phrases is irrelevant -- the tool must be structurally incapable of
writing one onto a surface. The poison leg (inventory phrase +
assigned=torso) is the case that discriminates: a fill path would
put it on torso; this one does not.

T34 count surfaces assumed before this file: 1283 / 1229 / 54
(the brief's number, t92 already in the tree). This change-set
adds only these hermetic legs and moves the pins it moves.

Hermetic tests do not open facet_E*.
"""
import json
import os
import sys

import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import canon_gate as C  # noqa: E402
import canon_worksheet as W  # noqa: E402

W3 = os.path.join(str(REPO), "canon", "w3.surfaces.json")
IDENT = os.path.join(str(REPO), "canon", "W3-IDENTITY.md")
REGIONS = os.path.join(str(REPO), "tools", "s3_sheet_regions.json")
SWORD = os.path.join(str(REPO), "canon", "longsword.surfaces.json")


def test_t93_emit_w3_identity_cannot_fill_an_occupant():
    """THE CHIP. NAMED phrases stay in inventory. Occupants stay empty."""
    ws = W.emit("humanoid", subject="W3", identity_path=IDENT)
    assert W.occupant_phrases(ws) == []
    assert len(ws["inventory"]) == 19
    assert all(i.get("assigned") is None for i in ws["inventory"])
    ids = {i["id"] for i in ws["inventory"]}
    assert "N1" in ids and "N17" in ids and "N19" in ids
    phrases = {i["phrase"] for i in ws["inventory"]}
    assert "a bald head" in phrases
    assert "a brown leather-wrapped grip" in phrases
    assert "gold necklace" not in json.dumps(ws)


def test_t93_inventory_assigned_hint_does_not_fill():
    """Can-fail: a fill path would honour assigned=torso."""
    ws = W.emit("humanoid", subject="W3", identity_path=IDENT)
    poison = "POISON PHRASE GOLD NECKLACE"
    ws["inventory"].append(
        {"id": "X9", "phrase": poison, "assigned": "torso"})
    doc = W.to_surfaces(ws)
    assert poison not in json.dumps(doc)
    assert W.occupant_phrases(doc) == []
    torso = [s for s in doc["surfaces"] if s["id"] == "torso"][0]
    assert torso["occupant"] is None


def test_t93_prop_kind_emits_a_grip_row_without_identity():
    """The N17 lesson: a weapon template has a grip before anyone names it."""
    ws = W.emit("weapon")
    ids = [s["id"] for s in ws["surfaces"]]
    assert "grip" in ids
    assert ws["inventory"] == []
    assert W.occupant_phrases(ws) == []
    human = W.emit("humanoid")
    assert "grip" not in [s["id"] for s in human["surfaces"]]


def test_t93_to_surfaces_of_emit_is_all_holes_and_loadable(tmp_path):
    ws = W.emit("humanoid", subject="X")
    doc = W.to_surfaces(ws)
    assert "legal_clauses" not in doc
    assert doc["scopes"]["views"] == {}
    assert doc["schema"] == 2
    p = tmp_path / "x.surfaces.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    loaded = C.load_canon(str(p))
    cov = C.coverage(loaded)
    assert cov["named"] == 0
    assert cov["holes"] == cov["prompt_surfaces"]
    assert cov["prompt_surfaces"] == 20


def test_t93_round_trip_copies_w3_occupants_and_does_not_invent():
    src = C.load_canon(W3)
    ws = W.from_surfaces(src, identity_path=IDENT)
    assert ws["type"] == "worksheet"
    rt = W.to_surfaces(ws)
    got = {s["id"]: (s.get("occupant") or {}).get("phrase")
           for s in rt["surfaces"]}
    want = {s["id"]: (s.get("occupant") or {}).get("phrase")
            for s in src["surfaces"]}
    assert got == want
    assert rt["schema"] == 2
    assert "legal_clauses" in rt
    assert len(rt["legal_clauses"]) == len(src["legal_clauses"])


def test_t93_scope_slots_exist_and_empty_lists_do_not_write():
    ws = W.emit("humanoid")
    views = ws["scopes"]["views"]
    assert set(views) == set("01234567")
    assert all(v["surfaces"] == [] and v["status"] == "open"
               for v in views.values())
    doc = W.to_surfaces(ws)
    assert doc["scopes"]["views"] == {}
    ws["scopes"]["views"]["0"]["surfaces"] = ["torso", "beard"]
    filled = W.to_surfaces(ws)
    assert filled["scopes"]["views"] == {
        "0": {"surfaces": ["torso", "beard"]}}


def test_t93_bind_matches_surface_ids_and_leaves_skirt_unmatched():
    src = C.load_canon(W3)
    ws = W.from_surfaces(src)
    regs = json.loads(open(REGIONS, encoding="utf-8").read())
    before = W.occupant_phrases(ws)
    result = W.bind_regions(ws, regs)
    assert W.occupant_phrases(ws) == before
    names = {u["name"] for u in result["unmatched"]}
    assert "skirt" in names
    assert "tunic" in names
    assert "boot_tops" in names
    assert "grip" not in names
    assert "blade" not in names
    assert result["bound"] >= 2
    v0 = {r["surface"]: r for r in ws["regions"]["views"]["0"]}
    assert v0["grip"]["box"] is not None
    assert v0["grip"]["status"] == "proposal"
    assert v0["torso"]["box"] is None


def test_t93_w3_density_is_24_25_19_and_uses_the_tokenizer():
    """Three counts, not one. Injected tokenizer, never char/4."""
    doc = C.load_canon(W3)
    calls = []

    def fake(text):
        calls.append(text)
        return ["tok"] * 11

    d = W.density(doc, encode=fake, tokenizer_name="injected")
    assert d["prompt_surfaces"] == 24
    assert d["required_checks"] == 25
    assert d["unique_elements"] == 19
    assert d["tokens"] == 11
    assert d["tokenizer"] == "injected"
    assert calls, "tokenizer was not invoked"
    assert d["tokens"] != d["token_text_chars"] // 4
    assert "unmeasured" in d["notes"][1]


def test_t93_emit_density_is_demand_without_elements():
    ws = W.emit("humanoid", identity_path=IDENT)
    d = W.density(ws, encode=lambda t: [], tokenizer_name="injected")
    assert d["prompt_surfaces"] == 20
    assert d["unique_elements"] == 0
    assert d["required_checks"] == 0
    assert d["inventory"] == 19
    assert d["inventory_unassigned"] == 19
    assert d["holes"] == 20


def test_t93_joints_are_pairs_to_confirm_not_invent():
    ws = W.emit("humanoid")
    assert ws["joints"]
    for j in ws["joints"]:
        assert j.get("phrase") is None
        assert j["status"] == "confirm"
        assert j["a"] in {s["id"] for s in ws["surfaces"]}
        assert j["b"] in {s["id"] for s in ws["surfaces"]}


def test_t93_schema_1_longsword_round_trip_does_not_arm_reverse(tmp_path):
    src = C.load_canon(SWORD)
    assert src["schema"] == 1
    ws = W.from_surfaces(src)
    doc = W.to_surfaces(ws)
    assert "legal_clauses" not in doc
    p = tmp_path / "s.surfaces.json"
    p.write_text(json.dumps(doc), encoding="utf-8")
    loaded = C.load_canon(str(p))
    chk = C.check_prompt(loaded, C._profile_restylize_prompt("profiles/prop.json"))
    assert chk["unlicensed"] == []


def test_t93_selftest_and_cli_chip(tmp_path):
    rc, out, err = run_py("canon_worksheet.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "occupants empty" in out
    assert "inventory 19 unassigned" in out
    assert "24/25/19" in out
    outp = tmp_path / "w.json"
    rc, out, err = run_py("canon_worksheet.py", [
        "emit", "--kind", "humanoid", "--subject", "W3",
        "--identity", "canon/W3-IDENTITY.md", "--out", str(outp),
    ])
    assert rc == 0, err
    ws = json.loads(outp.read_text(encoding="utf-8"))
    assert W.occupant_phrases(ws) == []
    assert len(ws["inventory"]) == 19
    rc, out, err = run_py("canon_worksheet.py", [
        "readout", "--canon", W3,
    ])
    assert rc == 0, err
    assert "required_checks 25" in out
    assert "unique_elements 19" in out
    assert "prompt_surfaces 24" in out
