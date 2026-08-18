"""T96 - the generation record. Recipe id. Explicitly absent producer.

Brief #21. The sidecar already recorded the run and named no producer.
This file is the identity half: immutable recipe_id, movable alias,
canon the gate allowed, producer fields that cannot be filled are
absent with a why. The twenty (actually the existing) fields stay
at the top level.

THE CHIP. Two recipes that differ only by CRLF vs LF in the prompt
share a recipe_id. A record that fills checkpoint_hash with a hex
string is refused. That is the case that separates an honest record
from a filename hash wearing provenance's clothes.

T34 count surfaces assumed before this file: 1319 / 1265 / 54
(the brief's number). This change-set adds only these hermetic
legs. Public surfaces are the advisor's this round; the implied
T34 move is stated in the report, not written here.

E56 / t97 / docs/experiments/E56-* are the other seat.

Hermetic tests do not open facet_E*.
"""
import json
import os
import sys

import pytest

from conftest import REPO, run_py

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import gen_record as G  # noqa: E402


def _legacy(prompt="a bald head"):
    return {
        "output": "x.png",
        "output_sha256": "00" * 32,
        "input": "/i.png",
        "input_sha256": "11" * 32,
        "mask": None,
        "mask_source": "keyed from the render",
        "prompt": prompt,
        "negative": "watermark",
        "prompts_file": None,
        "prompt_from_file": False,
        "seed": 770700,
        "steps": 20,
        "cfg": 2.5,
        "denoise": 0.92,
        "lora_w": 0.75,
        "cn_strength": 0.9,
        "canny_low": 0.4,
        "canny_high": 0.8,
        "bg": "0,0,0",
        "contour_width": 3,
        "tol": 0.06,
        "erode": 5,
        "control_px": {"total": 1, "canny": 1, "contour": 1},
        "figure_mask_pct_of_frame": 1.0,
    }


def test_t96_crlf_and_lf_share_a_recipe_id():
    """THE CHIP. Line-ending drift is not a new recipe."""
    a = G.build_record(_legacy("a bald head\r\nnext"))
    b = G.build_record(_legacy("a bald head\nnext"))
    assert a["recipe_id"] == b["recipe_id"]
    assert a["prompt_id"] == b["prompt_id"]
    assert a["alias"] is None
    for k in G.LEGACY:
        assert k in a


def test_t96_filled_checkpoint_hash_is_refused():
    """Can-fail: hashing a filename would pass if we accepted a string."""
    rec = G.build_record(_legacy())
    rec["producer"]["checkpoint_hash"] = "deadbeef" * 8
    with pytest.raises(G.Andon, match="cannot be filled"):
        G.validate(rec)


def test_t96_lora_weight_hash_cannot_wear_a_filename():
    rec = G.build_record(_legacy())
    rec["producer"]["lora_weight_hash"] = {
        "state": "declared", "value": rec["producer"]["lora_name"]["value"]}
    with pytest.raises(G.Andon, match="cannot be filled"):
        G.validate(rec)
    assert rec["producer"]["lora_name"]["state"] == "declared"


def test_t96_legacy_sidecar_still_loads_without_schema(tmp_path):
    p = tmp_path / "old_gen.json"
    p.write_text(json.dumps(_legacy()), encoding="utf-8")
    rec = G.load_record(str(p))
    assert rec.get("schema") is None
    assert rec["prompt"] == "a bald head"


def test_t96_write_generation_writes_both_or_the_image_is_not_left(tmp_path):
    rec = G.build_record(_legacy())
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8
    G.write_generation(str(tmp_path), "stem", png, rec)
    assert (tmp_path / "stem.png").is_file()
    assert (tmp_path / "stem_gen.json").is_file()
    G.require_sidecar(str(tmp_path / "stem.png"))
    loaded = G.load_record(str(tmp_path / "stem_gen.json"))
    assert loaded["schema"] == 1
    assert loaded["prompt"] == "a bald head"
    assert loaded["output_sha256"]


def test_t96_orphan_png_in_scratch_andon(tmp_path):
    p = tmp_path / "w3clay_0.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n")
    with pytest.raises(G.Andon, match="has no sidecar"):
        G.require_sidecar(str(p))
    rc, out, err = run_py("gen_record.py", ["check", str(p)])
    assert rc == 2
    assert "ANDON" in (out + err)


def test_t96_canon_verdict_is_recorded():
    rec = G.build_record(_legacy(), canon_verdict={
        "gated": True,
        "subject": "W3",
        "path": os.path.join(str(REPO), "canon", "w3.surfaces.json"),
        "note": None,
    })
    assert rec["canon"]["gated"] is True
    assert rec["canon"]["subject"] == "W3"
    assert rec["canon"]["schema"] == 2
    ung = G.build_record(_legacy(), canon_verdict={
        "gated": False, "subject": "GALLEON", "path": None,
        "note": "GALLEON identity exists, surfaces missing",
    })
    assert ung["canon"]["gated"] is False
    assert "GALLEON" in ung["canon"]["note"]


def test_t96_alias_is_not_in_the_recipe_id():
    a = G.build_record(_legacy(), alias=None)
    b = G.build_record(_legacy(), alias="w3-current")
    assert a["recipe_id"] == b["recipe_id"]
    assert b["alias"] == "w3-current"


def test_t96_selftest():
    rc, out, err = run_py("gen_record.py", ["--selftest"])
    assert rc == 0, "selftest exited %d\n%s\n%s" % (rc, out, err)
    assert "CRLF=LF" in out
    assert "filled hash refused" in out
    assert "orphan sidecar ANDON" in out
