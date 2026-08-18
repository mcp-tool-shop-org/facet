"""T91 - the canon gate is in the generation path.

Brief #17. canon_gate.py existed and nothing called it. A gate
that is not in the path is a document again.

restylize_views.py checks --canon BEFORE mkdir. T31's
DIR_AHEAD_OF_GATE pin for the masks ANDON is a different site
and moved 197 -> 215 on purpose in the same change-set.

Ratification is not occupancy. Unratified rows are named, not
required. The six-phrase profile default is the specimen: the
gate refuses it. The prompt text is not repaired.

A test that cannot fail is not a test. Hermetic tests do not
open facet_E*.
"""
import ast
import json
import os
import sys

import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import canon_gate as C  # noqa: E402

W3 = os.path.join(str(REPO), "canon", "w3.surfaces.json")
SWORD = os.path.join(str(REPO), "canon", "longsword.surfaces.json")

# Every RATIFIED phrase. N18 and N19 joined the set on 2026-08-17 when the
# Director ratified all four drafted rows, so a prompt that omitted them stopped
# being a covering prompt on that day - which is the gate doing its job on the
# fixture rather than on a subject.
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


def test_t91_census_exits_zero():
    rc, out, err = run_py("canon_gate.py", ["census"])
    assert rc == 0, "census exited %d\n%s\n%s" % (rc, out, err)
    assert "W3" in out and "24/24" in out, out
    # 6 -> 5 on purpose 2026-08-17: the Director ruled the garment is a KILT and
    # the live default still says skirt, so the canon rename cost a hit without
    # the prompt changing. Every canon repair today widened this gap.
    assert "5/19" in out, out
    assert "NONE" in out, out


def test_t91_w3_ratified_is_24_of_24():
    """MOVED ON PURPOSE 2026-08-17: the Director ratified all four drafted rows.

    Was `..._is_20_of_24`. The distinction the leg exists for - occupancy is not
    ratification - is unchanged and is why the two numbers are still asserted
    separately rather than collapsed into one. They happen to be equal today.
    """
    doc = C.load_canon(W3)
    cov = C.coverage(doc)
    assert cov["named"] == 24
    assert cov["prompt_surfaces"] == 24
    assert cov["coverage"] == 1.0
    assert cov["ratified"] == 24
    assert cov["unratified"] == 0
    assert cov["unratified_ids"] == []
    assert cov["ratified_coverage"] == pytest.approx(1.0)
    stamped = sorted(s["id"] for s in doc["surfaces"]
                     if (s.get("occupant") or {}).get("ratified"))
    assert stamped == ["greave_L", "greave_R", "hand_L", "hand_R"], stamped


def test_t91_unratified_phrases_are_not_required():
    """Can-fail: requiring a drafted phrase would treat a draft as ratified.

    REBUILT 2026-08-17, not repointed. W3 has no unratified rows any more, so
    reading this property off W3 would have made the leg unable to fail - the
    exact trap this repo names. It now builds its own drafted row on a copy, so
    the property is tested independently of whatever W3's ratification state
    happens to be on any given day.
    """
    doc = json.loads(open(W3, encoding="utf-8").read())
    for s in doc["surfaces"]:
        if s["id"] == "hand_L":
            s["occupant"].pop("ratified", None)
            s["occupant"]["ratify"] = True
            s["occupant"]["phrase"] = "a synthetic drafted phrase"
    chk = C.check_prompt(doc, RATIFIED_PROMPT)
    assert chk["ok"], chk
    missing_ids = {m["surface"] for m in chk["unratified_missing"]}
    assert "hand_L" in missing_ids
    assert not any(m["surface"] == "grip" for m in chk["unratified_missing"])
    assert not any(m["surface"] == "hand_L" for m in chk["missing"])


def test_t91_missing_ratified_phrase_still_refuses():
    doc = C.load_canon(W3)
    thin = RATIFIED_PROMPT.replace("a brown leather-wrapped grip", "")
    chk = C.check_prompt(doc, thin)
    assert not chk["ok"]
    assert any("leather-wrapped grip" in m["phrase"] for m in chk["missing"])


def test_t91_profile_default_is_refused_and_leaves_no_outdir(tmp_path):
    """THE CHIP. Default prompt + --canon must halt before mkdir."""
    out = tmp_path / "o"
    rc, out_s, err = run_py("restylize_views.py", [
        "--inputs", str(tmp_path / "nope.png"),
        "--outdir", str(out),
        "--canon", W3,
    ])
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "canon does not cover" in both
    assert "unratified named not required" in both
    assert not out.exists(), "refused generation created --outdir"


def test_t91_character_profile_attaches_the_canon(tmp_path):
    """First contact with --profile character.json is the specimen."""
    out = tmp_path / "o"
    rc, out_s, err = run_py("restylize_views.py", [
        "--profile", os.path.join(str(REPO), "profiles", "character.json"),
        "--inputs", str(tmp_path / "nope.png"),
        "--outdir", str(out),
    ], cwd=str(REPO))
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "canon does not cover" in both
    assert not out.exists()


def test_t91_no_canon_flag_is_fail_closed(tmp_path):
    """MOVED ON PURPOSE 2026-08-17 (t94). Was 'does not invent a check'.

    Silence is the defect #20 exists for. A restylize with neither
    --canon nor --no-canon now ANDON's before mkdir.
    """
    out = tmp_path / "o"
    png = tmp_path / "a.png"
    from PIL import Image
    import numpy as np
    Image.fromarray(np.zeros((8, 8, 3), dtype=np.uint8)).save(png)
    rc, out_s, err = run_py("restylize_views.py", [
        "--inputs", str(png),
        "--outdir", str(out),
        "--emit-only",
    ])
    both = out_s + err
    assert rc != 0
    assert "ANDON" in both
    assert "no canon:" in both
    assert not out.exists(), "ungated restylize created --outdir"


def test_t91_longsword_profile_covers_its_canon():
    """The prop profile was written against IDENTITY. The gate holds."""
    doc = C.load_canon(SWORD)
    prompt = C._profile_restylize_prompt("profiles/prop.json")
    chk = C.check_prompt(doc, prompt)
    assert chk["ok"], chk
    assert chk["required"] == 5


def test_t91_census_does_not_invent_surfaces():
    # E57, 2026-08-17: A1 joined CENSUS_ROWS. Not parametrized on purpose - this
    # test iterates census() internally, so widening its assertions here does not
    # add a new collected item and does not move T34's front-door counts (verified:
    # `pytest --collect-only` reports 1338 both before and after this edit).
    rows = {r["subject"]: r for r in C.census()}
    assert set(rows) == {
        "W3", "GALLEON", "DRAGON", "LONGSWORD", "E10-LAYER", "LOGO", "A1"}
    assert rows["GALLEON"]["surfaces"] is None
    assert rows["DRAGON"]["surfaces"] is None
    assert rows["W3"]["ratified"] == "24/24"
    assert rows["LONGSWORD"]["occupancy"] == "5/5"
    # A1's own row: 19 surfaces total, 16 with a "prompt"-provenance occupant (the
    # NAMED ones canon_gate counts toward occupancy - silhouette/proportions/
    # brushwork are mesh- or style-provenance and are not prompt surfaces), and
    # RATIFIED 2026-08-17 as drafted (canon_gate reads ratification as the ABSENCE
    # of "ratify": true - a1.surfaces.json carries no draft flags, so occupancy
    # and ratified read equal, same shape as W3's post-ratification row above).
    assert rows["A1"]["surfaces"] == "canon/a1.surfaces.json"
    assert rows["A1"]["identity"] == "canon/A1-IDENTITY.md"
    assert rows["A1"]["identity_named"] == 10
    assert rows["A1"]["occupancy"] == rows["A1"]["ratified"]


def test_t91_clause_class_staging_accepted_unknown_still_andons(tmp_path):
    # E57 fold, 2026-08-17: "staging" joined CLAUSE_CLASSES after census FIRED
    # on A1's ratified canon (four staging-class shot clauses). Two legs, both
    # can fail: the first fails if the widening is reverted, the second fails
    # if the membership check is deleted outright.
    def doc(cls):
        p = tmp_path / (cls + ".surfaces.json")
        p.write_text(json.dumps({
            "subject": "X", "kind": "prop", "schema": 2,
            "surfaces": [{"id": "s", "occupant": {
                "id": "P1", "phrase": "a thing", "provenance": "prompt"}}],
            "legal_clauses": [
                {"id": "c1", "phrase": "on a stand", "class": cls}],
        }), encoding="utf-8")
        return str(p)

    assert C.load_canon(doc("staging"))["legal_clauses"][0]["class"] == "staging"
    with pytest.raises(C.Andon) as e:
        C.load_canon(doc("lighting"))
    assert "lighting" in str(e.value)


def test_t91_restylize_has_one_andon_raise():
    """MOVED ON PURPOSE 2026-08-17 (t94). Was two: the canon wrap plus
    the masks ANDON. The wrap is gone; Andon keeps its type inside
    require_canon. The masks AssertionError is the one raise left.
    """
    src = open(os.path.join(str(REPO), "tools", "restylize_views.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    n = 0
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Raise) and isinstance(node.exc, ast.Call)):
            continue
        if not (isinstance(node.exc.func, ast.Name)
                and node.exc.func.id == "AssertionError"):
            continue
        arg = ast.get_source_segment(src, node.exc.args[0]) or ""
        if "ANDON" in arg or "str(e)" in arg:
            n += 1
    assert n == 1, "restylize ANDON raises: %d" % n


def test_t91_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "canon_gate.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares
