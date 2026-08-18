"""T97 - the binding. A surface is a face set, or it is only a word.

Brief #22. The router knows the material for torso. Nothing knows
which pixels are torso. scopes.views is empty. Per-asset labels
collapse because the accepted asset and the defective asset are
the same file.

THE CHIP. emit(w3.surfaces) has one row per surface, every
faces=[], bound 0, figure 0.00%. seed_boxes copies grip and blade
as proposals and leaves skirt unmatched. Faces stay empty. That
is the case that separates a binding from a rename table.

T34 count surfaces assumed before this file: 1328 / 1274 / 54
(the brief's number). This change-set adds only these hermetic
legs. Public surfaces are the advisor's; the implied T34 move
is stated in the report, not written here.

E56 report is on disk; t97 was free. Do not touch E56-*.

Hermetic tests do not open facet_E*.
"""
import json
import os
import sys

import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import canon_gate as C  # noqa: E402
import canon_bind as B  # noqa: E402

W3 = os.path.join(str(REPO), "canon", "w3.surfaces.json")
BIND = os.path.join(str(REPO), "canon", "w3.binding.json")
REGIONS = os.path.join(str(REPO), "tools", "s3_sheet_regions.json")
SWORD = os.path.join(str(REPO), "canon", "longsword.surfaces.json")


def test_t97_emit_w3_is_all_holes_and_zero_figure():
    """THE CHIP. A word list is not a binding."""
    surf = C.load_canon(W3)
    doc = B.emit(surf, source_rel="canon/w3.surfaces.json")
    assert len(doc["surfaces"]) == len(surf["surfaces"])
    assert doc["unit"] == "face"
    assert all(s["faces"] == [] for s in doc["surfaces"])
    assert all(s["ratified"] is False for s in doc["surfaces"])
    cov = B.coverage(doc)
    assert cov["bound"] == 0
    assert cov["figure_fraction"] == 0.0
    assert cov["surfaces"] == 27


def test_t97_seed_boxes_proposes_grip_and_leaves_skirt():
    surf = C.load_canon(W3)
    doc = B.emit(surf)
    regs = json.loads(open(REGIONS, encoding="utf-8").read())
    result = B.seed_boxes(doc, regs)
    names = {u["name"] for u in result["unmatched"]}
    assert "skirt" in names
    assert "tunic" in names
    assert "boot_tops" in names
    assert "grip" not in names
    assert "blade" not in names
    by_id = {s["id"]: s for s in doc["surfaces"]}
    assert by_id["grip"]["status"] == "proposal"
    assert by_id["grip"]["faces"] == []
    assert by_id["grip"]["ratified"] is False
    assert by_id["blade"]["status"] == "proposal"
    assert by_id["torso"]["status"] == "open"
    assert by_id["kilt"]["status"] == "open"


def test_t97_unknown_id_and_omitted_row_andon():
    surf = C.load_canon(W3)
    doc = B.emit(surf)
    extra = dict(doc)
    extra["surfaces"] = list(doc["surfaces"]) + [{
        "id": "skirt", "faces": [], "status": "open",
        "seeds": [], "ratified": False,
    }]
    with pytest.raises(B.Andon, match="extra"):
        B.validate(extra, surf)
    missing = dict(doc)
    missing["surfaces"] = [s for s in doc["surfaces"] if s["id"] != "torso"]
    with pytest.raises(B.Andon, match="missing"):
        B.validate(missing, surf)


def test_t97_two_surfaces_cannot_own_one_face():
    surf = C.load_canon(W3)
    doc = B.emit(surf)
    doc["surfaces"][0]["faces"] = [7]
    doc["surfaces"][1]["faces"] = [7]
    with pytest.raises(B.Andon, match="owned by"):
        B.validate(doc, surf)


def test_t97_ratified_empty_faces_andon():
    surf = C.load_canon(W3)
    doc = B.emit(surf)
    doc["surfaces"][0]["ratified"] = True
    with pytest.raises(B.Andon, match="ratified with no faces"):
        B.validate(doc, surf)


def test_t97_recorded_w3_binding_is_zero_figure():
    """The file in canon/ is the 0.00% the census should quote."""
    surf = C.load_canon(W3)
    doc = B.load_binding(BIND, surf)
    cov = B.coverage(doc)
    assert cov["bound"] == 0
    assert cov["proposed"] == 2
    assert cov["open"] == 25
    assert cov["figure_fraction"] == 0.0
    assert cov["surfaces"] == 27


def test_t97_propose_scopes_does_not_fill_lists():
    surf = C.load_canon(W3)
    doc = B.emit(surf)
    scopes = B.propose_scopes(doc)
    assert set(scopes["views"]) == set("01234567")
    assert all(v["surfaces"] == [] and v["status"] == "open"
               for v in scopes["views"].values())
    live = C.load_canon(W3)
    assert live["scopes"]["views"] == {}


def test_t97_margin_gate_fails_when_distributions_overlap():
    """The seat's Gate C: pauldron-as-control at 39.90% overlaps named."""
    bad = B.margin_holds([0.3990, 0.0756, 0.4026], [0.3990, 0.0096], 0.10)
    assert bad["ok"] is False
    good = B.margin_holds([0.80, 0.70], [0.10, 0.05], 0.40)
    assert good["ok"] is True


def test_t97_longsword_emit_has_no_grip_faces_either():
    surf = C.load_canon(SWORD)
    doc = B.emit(surf)
    assert "grip" in {s["id"] for s in doc["surfaces"]}
    assert B.coverage(doc)["bound"] == 0


def test_t97_selftest_and_census_names_zero():
    rc, out, err = run_py("canon_bind.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "faces empty" in out
    assert "skirt unmatched" in out
    assert "grip proposed" in out
    rc, out, err = run_py("canon_gate.py", ["census"])
    assert rc == 0, err
    assert "0/27 faces, 2 proposed" in out
    assert "LONGSWORD" in out and "NONE" in out
