# SPDX-License-Identifier: MIT
# Copyright (c) 2026 mcp-tool-shop
"""Generation record. Extend the sidecar; do not replace it.

WHY THIS EXISTS. Consult #21 / build #21. restylize_views already writes
twenty fields beside a twin. None of them name the producer. A seed is
not a replay (HF reproducibility docs). Three vendors converged on
immutable version + movable alias. Hashing a LoRA filename is not
provenance (civitai#742: metadata mutates the file hash).

EXTEND, DO NOT REPLACE. The twenty fields stay at the top level so
recorded sidecars and E55's as-generated reader keep working. Schema 1
adds recipe_id, alias, producer, canon, prompt_id.

EXPLICITLY ABSENT. A field we cannot fill must not look filled.
checkpoint_hash, lora_weight_hash, driver, hardware, library are
{state: absent, why: ...}. Declared names (unet, LoRA card, sampler)
are reachable because we author the graph. Weight tensors on Comfy
Cloud are not.

ENFORCE. write_generation writes the sidecar then the image. An image
without a sibling _gen.json is the SPEC/ hole. require_sidecar ANDON's
on that shape. Historical trees are not rewritten.

NO TIERED MODES. quick/advanced/assist are a GUI answer to a GUI
question. This repo has flags and JSON. #19 recorded that no
three-tier prompt UI has ever been evaluated.

CALIBRATION CLAIM (run --selftest; T96 pins the same numbers).
  Two recipes that differ only by CRLF vs LF in the prompt share a
  recipe_id. A record that fills checkpoint_hash with a hex string
  is refused. write_generation leaves no image if the sidecar is
  missing.

  python tools/gen_record.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import unicodedata

TOOL_VERSION = "1.0.0"
RECORD_SCHEMA = 1
RECORD_TYPE = "generation_record"

# The twenty fields restylize already writes. Do not rename. Do not drop.
LEGACY = (
    "output", "output_sha256", "input", "input_sha256",
    "mask", "mask_source", "prompt", "negative",
    "prompts_file", "prompt_from_file",
    "seed", "steps", "cfg", "denoise", "lora_w", "cn_strength",
    "canny_low", "canny_high", "bg", "contour_width", "tol", "erode",
    "control_px", "figure_mask_pct_of_frame",
)

# Declared names from the graph this repo authors. Names, not hashes.
RESTYLIZE_DECLARED = {
    "unet_name": "qwen_image_fp8_e4m3fn.safetensors",
    "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
    "vae_name": "qwen_image_vae.safetensors",
    "controlnet_name": "Qwen-Image-InstantX-ControlNet-Union.safetensors",
    "lora_name": "saltroad_style_v2_lowlr_000001500.safetensors",
    "sampler": "euler",
    "scheduler": "simple",
}

ABSENT_PRODUCER = (
    ("checkpoint_hash",
     "Comfy Cloud MCP does not return weight hashes to this repo"),
    ("lora_weight_hash",
     "cloud card tensors are not readable here; a filename hash is "
     "not provenance (civitai/civitai#742)"),
    ("driver",
     "Comfy Cloud worker / driver version is not returned"),
    ("hardware",
     "cloud GPU identity is not returned; cross-boundary residual "
     "was measured at dE 0.84"),
    ("library",
     "cloud torch / comfy / python versions are not returned"),
)

ABSENT_KEYS = tuple(k for k, _ in ABSENT_PRODUCER)


class Andon(ValueError):
    pass


def _andon(msg):
    raise Andon("ANDON: " + msg)


def normalize_text(text):
    """CRLF/CR -> LF, then NFC. Line-ending drift already broke a lock here."""
    if text is None:
        return ""
    s = str(text).replace("\r\n", "\n").replace("\r", "\n")
    return unicodedata.normalize("NFC", s)


def _sha256_text(text):
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def _sha256_json(obj):
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)
    return hashlib.sha256(normalize_text(blob).encode("utf-8")).hexdigest()


def absent(why):
    if not why or not str(why).strip():
        _andon("absent field needs a why")
    return {"state": "absent", "why": str(why).strip()}


def declared(value):
    return {"state": "declared", "value": value}


def _producer(declared_names):
    names = dict(RESTYLIZE_DECLARED)
    if declared_names:
        names.update(declared_names)
    out = {}
    for key in ("unet_name", "clip_name", "vae_name", "controlnet_name",
                "lora_name", "sampler", "scheduler"):
        out[key] = declared(names.get(key))
    for key, why in ABSENT_PRODUCER:
        out[key] = absent(why)
    return out


def _canon_block(verdict):
    if not verdict:
        return {
            "gated": None,
            "subject": None,
            "path": None,
            "schema": None,
            "note": "no require_canon verdict",
        }
    path = verdict.get("path")
    schema = None
    if path and os.path.isfile(path):
        try:
            schema = json.load(open(path, encoding="utf-8")).get("schema")
        except (OSError, ValueError, TypeError):
            schema = None
    return {
        "gated": bool(verdict.get("gated")),
        "subject": verdict.get("subject"),
        "path": path,
        "schema": schema,
        "note": verdict.get("note"),
    }


def _recipe_payload(legacy, producer, canon, prompt_id):
    """What the immutable id covers. Not the artifact, not the alias."""
    return {
        "prompt": normalize_text(legacy.get("prompt")),
        "negative": normalize_text(legacy.get("negative")),
        "seed": legacy.get("seed"),
        "steps": legacy.get("steps"),
        "cfg": legacy.get("cfg"),
        "denoise": legacy.get("denoise"),
        "lora_w": legacy.get("lora_w"),
        "cn_strength": legacy.get("cn_strength"),
        "canny_low": legacy.get("canny_low"),
        "canny_high": legacy.get("canny_high"),
        "bg": legacy.get("bg"),
        "contour_width": legacy.get("contour_width"),
        "tol": legacy.get("tol"),
        "erode": legacy.get("erode"),
        "unet_name": (producer.get("unet_name") or {}).get("value"),
        "lora_name": (producer.get("lora_name") or {}).get("value"),
        "sampler": (producer.get("sampler") or {}).get("value"),
        "scheduler": (producer.get("scheduler") or {}).get("value"),
        "canon_path": canon.get("path"),
        "canon_schema": canon.get("schema"),
        "canon_gated": canon.get("gated"),
        "prompt_id": prompt_id,
    }


def build_record(legacy, canon_verdict=None, declared_names=None, alias=None):
    """Assemble a schema-1 record. legacy must carry the twenty fields."""
    if not isinstance(legacy, dict):
        _andon("legacy sidecar must be an object")
    missing = [k for k in LEGACY if k not in legacy]
    if missing:
        _andon("legacy sidecar missing fields: %s" % ",".join(missing))
    producer = _producer(declared_names)
    canon = _canon_block(canon_verdict)
    prompt_id = _sha256_text(
        normalize_text(legacy.get("prompt")) + "\n"
        + normalize_text(legacy.get("negative")))
    recipe_id = _sha256_json(
        _recipe_payload(legacy, producer, canon, prompt_id))
    rec = {
        "type": RECORD_TYPE,
        "schema": RECORD_SCHEMA,
        "tool": "gen_record.py",
        "tool_version": TOOL_VERSION,
        "recipe_id": recipe_id,
        "alias": alias,
        "prompt_id": prompt_id,
        "producer": producer,
        "canon": canon,
    }
    for k in LEGACY:
        rec[k] = legacy[k]
    validate(rec)
    return rec


def validate(rec):
    """Refuse a record that looks filled where we cannot know."""
    if not isinstance(rec, dict):
        _andon("record must be an object")
    ver = rec.get("schema")
    if ver is None:
        # legacy twenty-field sidecar. Incomplete, loadable, not writable
        # as schema 1 without going through build_record.
        miss = [k for k in LEGACY if k not in rec]
        if miss:
            _andon("legacy sidecar missing fields: %s" % ",".join(miss))
        return rec
    try:
        ver = int(ver)
    except (TypeError, ValueError):
        _andon("record schema %r is not an int" % rec.get("schema"))
    if ver > RECORD_SCHEMA:
        _andon("stale consumer: record schema %d > %d" % (ver, RECORD_SCHEMA))
    if rec.get("type") != RECORD_TYPE:
        _andon("record type %r is not %s" % (rec.get("type"), RECORD_TYPE))
    if not rec.get("recipe_id"):
        _andon("schema-1 record needs recipe_id")
    miss = [k for k in LEGACY if k not in rec]
    if miss:
        _andon("record missing legacy fields: %s" % ",".join(miss))
    prod = rec.get("producer")
    if not isinstance(prod, dict):
        _andon("schema-1 record needs producer")
    for key in ABSENT_KEYS:
        slot = prod.get(key)
        if not isinstance(slot, dict) or slot.get("state") != "absent":
            _andon(
                "%s cannot be filled from this seat; it must be "
                "explicitly absent, not %r" % (key, slot))
        if not slot.get("why"):
            _andon("%s absent slot has no why" % key)
        if "value" in slot:
            _andon("%s absent slot must not carry a value" % key)
    return rec


def load_record(path):
    if not os.path.isfile(path):
        _andon("no record %s" % path)
    rec = json.load(open(path, encoding="utf-8"))
    return validate(rec)


def sidecar_path(image_path):
    stem, ext = os.path.splitext(image_path)
    if ext.lower() != ".png":
        _andon("generation image must be a .png, got %s" % image_path)
    return stem + "_gen.json"


def require_sidecar(image_path):
    """ANDON if an image has no sibling _gen.json. The SPEC/ hole."""
    side = sidecar_path(image_path)
    if not os.path.isfile(side):
        _andon("generation image %s has no sidecar %s"
               % (os.path.basename(image_path), os.path.basename(side)))
    return side


def write_generation(outdir, stem, image_bytes, record):
    """Write sidecar then image. No image is left if the sidecar is missing."""
    if not stem or "/" in stem or "\\" in stem:
        _andon("stem must be a bare name")
    if not isinstance(image_bytes, (bytes, bytearray)):
        _andon("image_bytes must be bytes")
    rec = dict(record)
    rec["output"] = stem + ".png"
    rec["output_sha256"] = hashlib.sha256(image_bytes).hexdigest()
    # recipe_id does not include output hash; rebuild to keep validate happy
    # but do not re-hash recipe from mutated output.
    validate(rec)
    if not os.path.isdir(outdir):
        _andon("no directory %s" % outdir)
    side = os.path.join(outdir, stem + "_gen.json")
    img = os.path.join(outdir, stem + ".png")
    payload = json.dumps(rec, indent=1, ensure_ascii=True) + "\n"
    with open(side, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    if not os.path.isfile(side):
        _andon("sidecar write vanished")
    try:
        with open(img, "wb") as fh:
            fh.write(image_bytes)
    except Exception:
        if os.path.isfile(side):
            os.remove(side)
        raise
    if not os.path.isfile(side):
        if os.path.isfile(img):
            os.remove(img)
        _andon("sidecar missing after image write")
    require_sidecar(img)
    return rec


def dump_legacy_compatible(rec):
    """The twenty fields, for a reader that does not know schema 1."""
    return {k: rec[k] for k in LEGACY}


def _selftest(scratch):
    base = {
        "output": "x.png",
        "output_sha256": "00" * 32,
        "input": "/i.png",
        "input_sha256": "11" * 32,
        "mask": None,
        "mask_source": "keyed from the render",
        "prompt": "a bald head\r\nnext",
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
    crlf = dict(base)
    lf = dict(base)
    lf["prompt"] = "a bald head\nnext"
    a = build_record(crlf)
    b = build_record(lf)
    if a["recipe_id"] != b["recipe_id"]:
        _andon("CRLF and LF prompts hashed differently")
    if a["prompt_id"] != b["prompt_id"]:
        _andon("prompt_id moved with line endings")
    if a["alias"] is not None:
        _andon("alias must default to null")
    for k in LEGACY:
        if k not in a:
            _andon("legacy field %s dropped" % k)
    filled = dict(a)
    filled["producer"] = dict(a["producer"])
    filled["producer"]["checkpoint_hash"] = "deadbeef"
    try:
        validate(filled)
        _andon("filled checkpoint_hash was accepted")
    except Andon as e:
        if "cannot be filled" not in str(e):
            _andon("filled hash refused for the wrong reason: %s" % e)
    png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 16
    rec = write_generation(scratch, "stem", png, a)
    img = os.path.join(scratch, "stem.png")
    side = os.path.join(scratch, "stem_gen.json")
    if not os.path.isfile(img) or not os.path.isfile(side):
        _andon("write_generation did not write both")
    require_sidecar(img)
    lone = os.path.join(scratch, "orphan.png")
    with open(lone, "wb") as fh:
        fh.write(png)
    try:
        require_sidecar(lone)
        _andon("orphan image did not refuse")
    except Andon as e:
        if "has no sidecar" not in str(e):
            _andon("orphan refused for the wrong reason: %s" % e)
    loaded = load_record(side)
    if loaded["recipe_id"] != rec["recipe_id"]:
        _andon("round-trip moved recipe_id")
    return a["recipe_id"]


def selftest(scratch=None):
    if scratch is None:
        scratch = tempfile.mkdtemp(prefix="gen_record_")
    return _selftest(scratch)


def build_parser():
    p = argparse.ArgumentParser(
        description="Generation record: recipe id, explicit-absent producer.")
    p.add_argument("--selftest", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    c = sub.add_parser("check", help="ANDON if a png has no sibling _gen.json")
    c.add_argument("image")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.selftest:
            rid = selftest()
            sys.stdout.write(
                "calibration CRLF=LF recipe_id %s  "
                "filled hash refused  orphan sidecar ANDON\n" % rid[:12])
            return 0
        if args.cmd == "check":
            require_sidecar(args.image)
            sys.stdout.write("sidecar present %s\n" % sidecar_path(args.image))
            return 0
        _andon("need a subcommand or --selftest")
    except Andon as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
