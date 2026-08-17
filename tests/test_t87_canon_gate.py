"""T87 - the canon surface database and the gates that load it.

The instrument is tools/canon_gate.py plus canon/w3.surfaces.json.
SURFACE is the row. A hole is a null occupant.

A prompt that names five of nineteen phrases, a sleeve on a bare arm,
a second occupant on an occupied surface, a hand-set verification
field, or a bare assert fails at least one leg.

Hermetic tests do not open facet_E08. The artifacts leg re-reads the
ARMB workflow the older handoff cited.
"""
import ast
import hashlib
import json
import os
import sys

import numpy as np
import pytest
from PIL import Image

from conftest import REPO, need, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import canon_gate as C  # noqa: E402

W3 = os.path.join(str(REPO), "canon", "w3.surfaces.json")
SWORD = os.path.join(str(REPO), "canon", "longsword.surfaces.json")
IDENT = os.path.join(str(REPO), "canon", "W3-IDENTITY.md")


def test_t87_selftest_exits_zero():
    rc, out, err = run_py("canon_gate.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "profile-default hits 5 of 19" in out, out
    assert "fixture coverage 0.75" in out, out


def test_t87_profile_default_hits_five_of_nineteen():
    """MOVED ON PURPOSE 2026-08-17. Was `..._six_of_seventeen`, then
    `..._is_still_six_while_the_canon_grew` - whose assertion already said 5
    while its name still said six; E54 renamed it to what it asserts.

    The canon went 17 -> 19 NAMED rows when the hand and shin surfaces were
    drafted off the reference; the profile default did not change by a
    character, so completing the canon WIDENED the gap, 6/17 to 6/19. Then
    the kilt ruling (2da2e3e) renamed N8/N9 skirt -> kilt and the profile
    default's `skirt` stopped matching N8: 6/19 -> 5/19, still without the
    prompt moving a character. Which is why this leg pins the two numbers
    separately and never the ratio between them.
    """
    named = C.w3_named_phrases()
    assert len(named) == 19
    prompt = C.profile_default_prompt()
    hit, miss = C.phrase_hits_in_text(prompt, named)
    assert len(hit) == 5, (hit, miss)
    assert "N17" in miss


def test_t87_w3_coverage_is_full_and_every_row_is_RATIFIED():
    """MOVED ON PURPOSE 2026-08-17, in the commit that filled the holes.

    Was `..._holes_are_hands_and_greaves`, pinning holes == 4. The advisor
    walked canon/twin_front.png at 3x and drafted them: both hands are bare
    flesh (N18), and the greave row was a MIS-DECOMPOSITION rather than a hole
    - the gold knee plate runs knee to boot with leather and fleece behind it
    (N19). Coverage is therefore 1.0.

    MOVED AGAIN, SAME DAY: those four drafts were then wrong - the hands are
    gauntleted, not bare, and the Director caught it - and the corrected rows
    were RATIFIED by him on 2026-08-17. So the unratified set is now empty and
    the four carry a ratified stamp instead.

    The property this leg exists for is unchanged through both moves, and is why
    it did not simply become `holes == 0`: a surface-keyed canon shows you what
    an element list cannot. It shows holes, and then it shows drafts. Both
    assertions stay so that a future draft has to move this pin on purpose the
    way these two edits did.
    """
    doc = C.load_canon(W3)
    cov = C.coverage(doc)
    assert set(cov["hole_ids"]) == set(), cov["hole_ids"]
    assert cov["holes"] == 0
    assert cov["named"] + cov["holes"] == cov["prompt_surfaces"]
    assert cov["coverage"] == pytest.approx(
        cov["named"] / cov["prompt_surfaces"])
    assert cov["prompt_surfaces"] == 24
    assert cov["named"] == 24

    unratified = sorted(
        s["id"] for s in doc["surfaces"]
        if (s.get("occupant") or {}).get("ratify") is True)
    assert unratified == [], unratified
    ratified = sorted(
        s["id"] for s in doc["surfaces"]
        if (s.get("occupant") or {}).get("ratified"))
    assert ratified == ["greave_L", "greave_R", "hand_L", "hand_R"], ratified
    assert len(doc.get("ratification_queue", [])) == 5


def test_t87_w3_identity_pin():
    rc, out, err = run_py("canon_gate.py", [
        "pin-identity", "--canon", W3, "--identity", IDENT])
    assert rc == 0, "%s\n%s" % (out, err)
    doc = C.load_canon(W3)
    pin = C.pin_identity(doc, IDENT)
    # 17 -> 19 on purpose 2026-08-17: N18 bare hands and N19 the leather shin
    # guard were drafted into BOTH files in the same commit. This leg is the
    # two-files-one-truth gate and it FIRED when the JSON moved first, which is
    # exactly its job - the markdown carries the reasoning a row cannot.
    assert pin["named_rows"] == 19


def test_t87_recorded_thin_prompt_is_refused():
    """The six-element default must not pass the author-time gate."""
    prompt = C.profile_default_prompt()
    rc, out, err = run_py("canon_gate.py", [
        "check", "--canon", W3, "--prompt", prompt])
    assert rc == 2
    assert "ANDON" in err
    assert "leather-wrapped grip" in err


def test_t87_negation_does_not_count_as_coverage():
    doc = C.load_canon(W3)
    full = (
        "a bald head, a long red beard, a dark green knitted sleeveless "
        "tunic, polished gold pauldrons, gold scrollwork on the pauldrons, "
        "a gold belt medallion, a brown leather belt, a dark red layered "
        "cloth kilt, green cloth panels in the kilt, brown leather "
        "bracers, a gold plate on each outer forearm, gold knee plates, "
        "heavy dark boots, a massive greatsword, an ornate gold "
        "crossguard, a gold pommel, no a brown leather-wrapped grip")
    chk = C.check_prompt(doc, full)
    assert not chk["ok"]
    assert any("leather-wrapped grip" in m["phrase"] for m in chk["missing"])


def test_t87_sleeve_on_bare_arm_andon_sleeveless_does_not():
    doc = C.load_canon(W3)
    base = (
        "a bald head, a long red beard, a dark green knitted sleeveless "
        "tunic, polished gold pauldrons, gold scrollwork on the pauldrons, "
        "a gold belt medallion, a brown leather belt, a dark red layered "
        "cloth kilt, green cloth panels in the kilt, brown leather "
        "bracers, a gold plate on each outer forearm, gold knee plates, "
        "heavy dark boots, a massive greatsword, an ornate gold "
        "crossguard, a gold pommel, a brown leather-wrapped grip, brown "
        "leather gauntlets, a brown leather shin guard")
    ok = C.check_prompt(doc, base)
    assert ok["ok"], ok
    bad = C.check_prompt(doc, base + ", a shirt sleeve")
    assert not bad["ok"]
    assert bad["forbidden"]
    still = C.check_prompt(doc, base)  # sleeveless is inside N3
    assert still["ok"]


def test_t87_occupancy_records_blocked_additions():
    """Can-fail: installing N11 as a second forearm occupant would pass."""
    doc = C.load_canon(W3)
    occ = C.occupancy(doc)
    ids = {b["addition"] for b in occ["blocked"]}
    assert ids == {"N5", "N9", "N11"}
    # schema cannot express two occupants; a list would be the miss
    for s in doc["surfaces"]:
        occu = s.get("occupant")
        assert occu is None or isinstance(occu, dict)


def test_t87_surfaces_file_has_no_verification_field():
    """Verification is never hand-set in the canon file."""
    raw = json.loads(open(W3, encoding="utf-8").read())
    blob = json.dumps(raw)
    assert "verification" not in blob
    assert "median_dE" not in blob


def test_t87_longsword_schema_is_a_prop():
    doc = C.load_canon(SWORD)
    assert doc["kind"] == "prop"
    cov = C.coverage(doc)
    assert cov["holes"] == 0
    assert cov["coverage"] == 1.0
    assert any(j["id"] == "grip_pommel" for j in doc["joints"])


def test_t87_verify_writes_sidecar_not_canon(tmp_path):
    canon = tmp_path / "x.surfaces.json"
    canon.write_text(open(W3, encoding="utf-8").read(), encoding="utf-8")
    img_a = tmp_path / "a.png"
    img_b = tmp_path / "b.png"
    a = np.full((16, 16, 3), 30, dtype=np.uint8)
    b = a.copy()
    b[0:8, 0:8] = (220, 10, 10)
    Image.fromarray(a).save(img_a)
    Image.fromarray(b).save(img_b)
    regs = tmp_path / "r.json"
    regs.write_text(json.dumps([
        {"name": "same", "box": [8, 8, 16, 16]},
        {"name": "diff", "box": [0, 0, 8, 8]},
    ]), encoding="utf-8")
    rc, out, err = run_py("canon_gate.py", [
        "verify", "--canon", str(canon),
        "--twin", str(img_b), "--reference", str(img_a),
        "--regions", str(regs), "--write-sidecar",
    ])
    assert rc == 0, "%s\n%s" % (out, err)
    side = tmp_path / "x.verify.json"
    assert side.is_file()
    payload = json.loads(side.read_text(encoding="utf-8"))
    states = {r["name"]: r["state"] for r in payload["regions"]}
    assert states["same"] == "landed"
    assert states["diff"] == "missed"
    # canon file bytes unchanged
    assert json.loads(canon.read_text(encoding="utf-8")).get("verification") is None


def test_t87_duplicate_surface_id_andon(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({
        "subject": "X", "kind": "prop", "schema": 1,
        "surfaces": [
            {"id": "a", "occupant": None},
            {"id": "a", "occupant": None},
        ],
    }), encoding="utf-8")
    with pytest.raises(C.Andon, match="duplicate"):
        C.load_canon(str(p))


def test_t87_no_andon_is_a_bare_assert():
    src = open(os.path.join(str(REPO), "tools", "canon_gate.py"),
               encoding="utf-8").read()
    tree = ast.parse(src)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "bare assert at lines %s" % bares


@pytest.mark.artifacts
def test_t87_armb_workflow_is_fourteen_of_nineteen(assets):
    """MOVED ON PURPOSE 2026-08-17 (E54). Was `..._is_sixteen_of_seventeen`,
    "16/17, missing only the grip" - and the recorded string has not changed
    (sha256 pinned below; file mtime 2026-08-04, thirteen days before the
    canon work). The canon moved under it, twice in one day, measured by
    sweeping the NAMED list across canon/W3-IDENTITY.md revisions with this
    leg's own code path (E54 report, task 2):

      54bf90d  NAMED=17: hit 16, miss [N17]               (the recorded claim)
      2e73ba8  NAMED=19: hit 16, miss [N17,N18,N19]       (hand+shin drafted)
      2da2e3e  NAMED=19: hit 14, miss [N8,N9,N17,N18,N19]
               (the garment was ruled a kilt: N8/N9 renamed skirt -> kilt,
                and the recording says skirt twice, kilt never)

    A frozen recording can only lose hits as the canon is corrected, and
    each loss measures how far that recorded spend sits from today's canon -
    which is what this pin is for, and why it is re-stated rather than
    deleted."""
    wf = need(
        assets,
        "facet_E08/ARMB/out/stroke_1_y+090_e+00_workflow.json")
    raw = wf.read_bytes()
    # The recorded input is the contract here (E08 armB state is in the
    # byte-hash family, CLAUDE.md); a change in the recorded tree must
    # arrive as this notification, never as a silent hit-count move.
    assert hashlib.sha256(raw).hexdigest() == (
        "42547a4253f6b4d031b7e2d5c29ca6ada79751170e97009b7b77423982ddf576")
    doc = json.loads(raw.decode("utf-8"))
    text = doc["7"]["inputs"]["text"]
    named = C.w3_named_phrases()
    hit, miss = C.phrase_hits_in_text(text, named)
    assert len(hit) == 14, (hit, miss)
    assert miss == ["N8", "N9", "N17", "N18", "N19"], (hit, miss)
    low = text.lower()
    assert low.count("skirt") == 2  # the pre-rename garment, frozen in the record
    assert low.count("kilt") == 0
    assert low.count("grip") == 0
    assert low.count("gauntlet") == 0
    assert low.count("greave") == 0
    assert low.count("hand") == 0
