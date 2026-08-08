"""E08 Amendment 30 — the hand-driven cloud stroke, in three auditable pieces.

`texpass_brush.py` posts to a LOCAL ComfyUI and generation must run on Comfy Cloud, so the
transport is driven by the session through the MCP. Amendment 30's ruling: the recipe for a
generative step is **the submitted workflow JSON**, not the invocation that submits it — so this
tool writes that JSON to disk BEFORE anything is submitted, byte-matched to `texpass_brush.py`'s
own graph and defaults, with the prompt from the versioned prompt file as the only per-stroke
variable. The eight saved JSONs are the recipe, and they are the regression fixtures for the
cloud transport that will later live inside `texpass_brush.py`.

Three subcommands, so each step is separately replayable and separately logged:

  graph   — build + save stroke k's workflow JSON from the emitted job. Submits nothing.
  invar   — the first-stroke invariance ANDON: is the returned image unchanged OUTSIDE the
            figure? Reads the residual's SHAPE, per Amendment 30 — uniform sub-unit is the
            codec boundary and proceeds; CONCENTRATED is a repainted backdrop and halts.
            That distinction is Amendment 21's: a structural difference concentrates, two
            float kernels do not.
  log     — append an ordered line to the run log.

  brush_cloud_step.py graph --job DIR --key y+090_e+00 --prompts P.json --out J.json
  brush_cloud_step.py invar --job DIR [--tol 1.0] [--conc-tol 4.0]
  brush_cloud_step.py log --run-log L.jsonl --entry '{"...":...}'
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy.ndimage import label, maximum_filter

Image.MAX_IMAGE_PIXELS = None

# ⚠ BYTE-MATCHED to texpass_brush.py's defaults. Any divergence here is a silent second
# variable in a run that is only supposed to carry one (the prompts).
DEFAULTS = {"seed": 770700, "steps": 20, "cfg": 2.5, "lora_w": 0.75, "cn_strength": 1.0}
# ⚠ CORRECTED (E08 Amendment 31). The cloud's name for the imported LoRA, enumerated in the
# Model Library UI by the advisor. The previous value —
# `mikeyfrilot__saltroad-lora__...` — is the REDUNDANT import that has since vanished; it is
# the one 0b ran on, and stroke 1 was rejected with it at `not in (list of length 144)`.
# The copy below is the ORIGINAL, imported 8/1/26, the one Amendment 21 found already present
# before the mikeyfrilot delivery path was built on top of it.
#
# THE TRAP, banked: `search_models` and this node's own option list do NOT see account
# imports — both return zero for "saltroad" while the card sits in the library. So "absent
# from the node list" does NOT mean "absent from the library", and an API surface is not the
# ground truth for an import. Enumerate imports in the browser.
CLOUD_LORA = ("mcp-tool-shop__saltroad-style-lora__"
              "saltroad_style_v2_lowlr_000001500.safetensors")


def build_graph(render_name, mask_name, prompt, negative, seed=None, lora_w=None):
    """texpass_brush.py's graph, node for node, with cloud model names.

    ⚠ THE NO-LoRA PATH (E12 Ruling 25e, handoff 15 step 0). This function used to insert node
    5 — `LoraLoaderModelOnly` with the hardcoded saltroad card — UNCONDITIONALLY, with node 6
    reading `["5", 0]`. On a subject whose register is NO CARD that is not expressible at any
    weight: E12 Ruling 10b's ruled wording is that 0.0 "is not a weight of zero on a loaded
    card, it is no card, and the graph is built without the loader", which is how
    `e12_pair_cloud_step` builds the twins. The gap was three layers deep and was found by
    BUILDING the graph, not by reading it (handoff 14 §5).

    `lora_w` now comes from the SUBJECT'S PROFILE rather than from DEFAULTS — the caller reads
    the decided `texpass_brush.lora-w` and passes it. That converts one of the five
    coincidences-of-value into agreement by construction, which is the class fix this file's
    own docstring has been asking for; the pre-flight below is amended to match, and it gains
    a STRUCTURAL assertion the value check cannot make: the loader node exists if and only if
    the decided weight is positive.

    At a positive weight the graph is byte-for-byte what it always was — 17 nodes, node 5 at
    that weight, node 6 reading ["5", 0]. That identity is not asserted by argument: it is the
    handoff-15 anchor, which rebuilds the ship's recorded stroke graph and compares.
    """
    d = dict(DEFAULTS)
    if seed is not None:
        d["seed"] = seed
    if lora_w is not None:
        d["lora_w"] = lora_w
    if d["lora_w"] == 0.0:
        g = _graph_common(render_name, mask_name, prompt, negative, d)
        # no loader: ModelSamplingAuraFlow reads the UNET directly, exactly as the twins' path
        g["6"]["inputs"]["model"] = ["1", 0]
        return g
    g = _graph_common(render_name, mask_name, prompt, negative, d)
    g["5"] = {"class_type": "LoraLoaderModelOnly", "inputs": {
        "model": ["1", 0], "lora_name": CLOUD_LORA, "strength_model": d["lora_w"]}}
    g["6"]["inputs"]["model"] = ["5", 0]
    return g


def _graph_common(render_name, mask_name, prompt, negative, d):
    """Every node except the loader and the one link that depends on it."""
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "qwen_image_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image",
            "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "ControlNetLoader", "inputs": {
            "control_net_name": "Qwen-Image-InstantX-ControlNet-Inpainting.safetensors"}},
        "6": {"class_type": "ModelSamplingAuraFlow", "inputs": {
            "model": None, "shift": 3.1}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": negative}},
        "9": {"class_type": "LoadImage", "inputs": {"image": render_name}},
        "10": {"class_type": "LoadImage", "inputs": {"image": mask_name}},
        "11": {"class_type": "ImageToMask", "inputs": {"image": ["10", 0], "channel": "red"}},
        "12": {"class_type": "ControlNetInpaintingAliMamaApply", "inputs": {
            "positive": ["7", 0], "negative": ["8", 0], "control_net": ["4", 0],
            "vae": ["3", 0], "image": ["9", 0], "mask": ["11", 0],
            "strength": d["cn_strength"], "start_percent": 0.0, "end_percent": 1.0}},
        "13": {"class_type": "VAEEncode", "inputs": {"pixels": ["9", 0], "vae": ["3", 0]}},
        "14": {"class_type": "SetLatentNoiseMask", "inputs": {
            "samples": ["13", 0], "mask": ["11", 0]}},
        "15": {"class_type": "KSampler", "inputs": {
            "model": ["6", 0], "seed": d["seed"], "steps": d["steps"], "cfg": d["cfg"],
            "sampler_name": "euler", "scheduler": "simple", "positive": ["12", 0],
            "negative": ["12", 1], "latent_image": ["14", 0], "denoise": 1.0}},
        "16": {"class_type": "VAEDecode", "inputs": {"samples": ["15", 0], "vae": ["3", 0]}},
        "17": {"class_type": "SaveImage", "inputs": {
            "images": ["16", 0], "filename_prefix": "texpass"}},
    }


ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)

g = sub.add_parser("graph")
g.add_argument("--job", required=True)
g.add_argument("--key", required=True)
g.add_argument("--prompts", required=True)
# E10 Ruling 6: the profile's vocabulary is two-lane. One subject can own two content
# lanes - the base atlas and an environment-contact layer - and each declares its own
# prompt fixture. The mapping lives HERE, fixed, so a lane cannot name an arbitrary key;
# the check fires against the mapped key in BOTH lanes, with no skip flag in either.
# Default `base` means the character and E04 paths are unchanged BY CONSTRUCTION: no
# existing invocation passes --lane.
g.add_argument("--lane", choices=["base", "layer"], default="base",
               help="content lane. Selects the profile fixture key (base -> "
                    "_fixtures.brush_prompts, layer -> _fixtures.layer_prompts) and is "
                    "CORROBORATED against the job's state identity: a guard that infers "
                    "its own jurisdiction can be steered, so the lane is a declared input "
                    "cross-checked against data already in hand.")
g.add_argument("--out", required=True)
g.add_argument("--render-name", default=None, help="cloud input name; defaults to local")
g.add_argument("--mask-name", default=None)
g.add_argument("--seed", type=int, default=None)
g.add_argument("--profile", required=True,
               help="REQUIRED, and there is deliberately no way to skip it (E04 Ruling 24). "
                    "The subject profile whose texpass_brush.py block the values entering "
                    "the graph are checked against. Required rather than optional because "
                    "an optional guard is a skip flag with a different name.")

v = sub.add_parser("invar")
v.add_argument("--job", required=True)
v.add_argument("--tol", type=float, default=1.0,
               help="ANDON: max mean |edited-emitted| in 8-bit levels outside the dilated "
                    "figure. Sub-unit is a codec boundary.")
v.add_argument("--conc-tol", type=float, default=4.0,
               help="ANDON: a CONCENTRATED residual halts even if the mean is small. This "
                    "is the level above which a pixel counts as materially changed.")
v.add_argument("--dilate", type=int, default=9,
               help="dilate the figure by this before calling anything 'outside', so the "
                    "inpaint's own antialiased boundary is not read as a repaint")

lg = sub.add_parser("log")
lg.add_argument("--run-log", required=True)
lg.add_argument("--entry", required=True)

args = ap.parse_args()

def preflight(gr, P, key):
    """E04 Ruling 24 — the coincidence becomes a CHECKED EQUALITY, inside the tool that acts.

    DEFAULTS above hardcodes five recipe values and this tool binds no profile, so on any
    subject whose profile decides those five keys they agree BY COINCIDENCE OF VALUE, not by
    construction. A future ruling that moves a subject's brush recipe would edit a profile
    this tool never reads. Until the class fix lands (brush_cloud_step binding the profile
    properly - shared-code bundle, Step-0-class, character anchors), this asserts the
    coincidence every time a graph is built, and HALTS rather than warning.

    Two different questions, checked two different ways, because they have different
    failure modes:

      the five recipe numbers - checked by VALUE against the profile block. This is the
        coincidence the ruling names.
      prompt and negative    - checked by PROVENANCE: that --prompts IS the file the
        profile's _fixtures.brush_prompts names, and that the strings entering the graph
        are that file's, unmodified. Value equality would be the wrong check here: a
        profile's prompt/negative copies DOCUMENT the fixture (ship.json says so in the
        row itself) and on the character they deliberately differ from it - character.json
        carries texpass_brush's stale default, which E08's fixture exists to supersede.
        Asserting provenance is stronger than asserting equality anyway: it guarantees the
        strings came from this subject's decided file rather than merely matching a copy.

    Runs BEFORE the workflow JSON is written, so a failed pre-flight leaves no file that
    could be submitted.
    """
    prof = json.load(open(args.profile, encoding="utf-8"))
    blk = prof.get("tools", {}).get("texpass_brush.py")
    if not (isinstance(blk, dict)):
        raise AssertionError(
            f"ANDON: {args.profile} has no tools['texpass_brush.py'] block, so there is nothing "
            f"to check the graph against. A subject whose brush block is absent is running this "
            f"tool's constants by silence, which is the failure this check exists to catch.")
    if not ("_NOT_CLEARED" not in blk):
        raise AssertionError(
            f"ANDON: {args.profile}'s texpass_brush.py block carries _NOT_CLEARED - the tool is "
            f"FORBIDDEN on this subject until a ruling clears the block and decides its keys.")

    def pv(k):
        e = blk.get(k)
        if not (isinstance(e, dict) and "value" in e):
            raise AssertionError(
                f"ANDON: {args.profile} texpass_brush.py has no decided value for '{k}'")
        return e["value"]

    bad = []
    # (a) the hardcoded constants against the decided block - unconditional, and
    #     independent of any per-invocation override, because THIS is the coincidence.
    #
    # ⚠ lora-w LEFT THIS LIST at Ruling 25e, and the reason is that it is no longer a
    # coincidence. build_graph now takes the weight FROM THIS PROFILE (below) rather than
    # from DEFAULTS, so comparing DEFAULTS['lora_w'] against the decided value would be
    # comparing a number that no longer reaches the graph - the check would fire on a
    # correct build, which is the class of error this repo keeps paying for. What replaces
    # it is stronger than a value comparison and appears as (b2): the loader NODE exists if
    # and only if the decided weight is positive, asserted structurally over every node.
    for pk, dk in (("seed", "seed"), ("steps", "steps"), ("cfg", "cfg"),
                   ("cn-strength", "cn_strength")):
        if DEFAULTS[dk] != pv(pk):
            bad.append(f"DEFAULTS[{dk!r}] = {DEFAULTS[dk]!r} but the profile decides "
                       f"{pk} = {pv(pk)!r}")
    # (b) what actually landed in the graph nodes
    entering = {"seed": gr["15"]["inputs"]["seed"], "steps": gr["15"]["inputs"]["steps"],
                "cfg": gr["15"]["inputs"]["cfg"],
                "cn-strength": gr["12"]["inputs"]["strength"]}
    if "5" in gr:
        entering["lora-w"] = gr["5"]["inputs"]["strength_model"]

    # (b2) THE INVERTED SCAN, the restylize class (E12 Ruling 10b / 25e). When the register
    # says NO CARD, "lora-w is 0.0" is not the claim being made - the claim is that no loader
    # node and no card string exist ANYWHERE in the graph. Asserted by walking every node,
    # because a weight check reads one field and a smuggled loader is a different field.
    _lw = pv("lora-w")
    _loaders = [k for k, n in gr.items() if "lora" in str(n.get("class_type", "")).lower()]
    _cards = [k for k, n in gr.items()
              if any("lora" in str(v).lower() or "saltroad" in str(v).lower()
                     for v in n.get("inputs", {}).values())]
    if _lw == 0.0:
        if _loaders or _cards:
            bad.append(f"the register is NONE (lora-w 0.0) but the graph carries loader "
                       f"node(s) {_loaders} and card reference(s) {_cards} - 0.0 is not a "
                       f"weight of zero on a loaded card, it is NO CARD (Ruling 10b)")
        if gr["6"]["inputs"]["model"] != ["1", 0]:
            bad.append(f"the register is NONE but ModelSamplingAuraFlow reads "
                       f"{gr['6']['inputs']['model']!r} instead of the UNET ['1', 0]")
    else:
        if not _loaders:
            bad.append(f"the profile decides lora-w {_lw!r} but the graph carries NO loader "
                       f"node - the weight would be silently inert")
        if gr["6"]["inputs"]["model"] != ["5", 0]:
            bad.append(f"lora-w {_lw!r} is positive but ModelSamplingAuraFlow reads "
                       f"{gr['6']['inputs']['model']!r} instead of the loader ['5', 0]")
    print(f"[pre-flight] register scan: decided lora-w {_lw!r}; loader nodes {_loaders or 'NONE'}; "
          f"card references {_cards or 'NONE'}; {len(gr)} nodes", flush=True)
    for k, got in entering.items():
        if k == "seed" and args.seed is not None:
            # an explicit --seed is a recorded per-invocation argument (the one-re-roll
            # precedent, E08 A23), not an undeclared constant. It must land in the graph
            # exactly as given, and the deviation from the decided value is printed loudly
            # rather than hidden - but it does not silence check (a) above.
            if got != args.seed:
                bad.append(f"graph seed {got!r} is neither the profile's nor the explicit "
                           f"--seed {args.seed!r}")
            if got != pv("seed"):
                print(f"[pre-flight] DEVIATION, EXPLICIT: seed {got} against the profile's "
                      f"{pv('seed')}. Recorded per-invocation argument, not a constant.",
                      flush=True)
            continue
        if got != pv(k):
            bad.append(f"graph {k} = {got!r} but the profile decides {pv(k)!r}")
    # (c) prompt and negative by PROVENANCE, through the lane's declared fixture
    # E10 Ruling 6. The mapping is fixed here so a lane cannot name an arbitrary key.
    LANE_FIXTURE = {"base": "brush_prompts", "layer": "layer_prompts"}
    lane = getattr(args, "lane", "base")
    fxkey = LANE_FIXTURE[lane]

    # CORROBORATION: the declared lane is cross-checked against the job's state identity.
    # A layer state is seeded with layer_state.json beside it (e10_layer_seed.py); a base
    # state has none. The lane is DECLARED rather than inferred - a guard that works out
    # its own jurisdiction from the data can be steered by that data - and then the
    # declaration is required to agree with what is already on disk.
    jobdir = os.path.abspath(args.job)
    state = os.path.dirname(jobdir)
    marker = any(os.path.exists(os.path.join(d, "layer_state.json"))
                 for d in (state, os.path.dirname(state)))
    if lane == "layer" and not marker:
        bad.append(f"--lane layer, but no layer_state.json beside the job's state "
                   f"({state}). A layer stroke must run against a seeded layer state.")
    if lane == "base" and marker:
        bad.append(f"--lane base (the default), but the job's state ({state}) IS a seeded "
                   f"layer state. A base stroke committed here would paint the layer's "
                   f"atlas while claiming the base lane's fixture.")

    fx = (prof.get("_fixtures", {}).get(fxkey, {}) or {}).get("path")
    if not (fx):
        raise AssertionError(f"ANDON: {args.profile} names no _fixtures.{fxkey}.path, so the strings "
                    f"entering the graph have no declared source for lane {lane!r}")
    root = os.path.dirname(os.path.dirname(os.path.abspath(args.profile)))
    want_fx = os.path.realpath(os.path.join(root, fx))
    got_fx = os.path.realpath(os.path.abspath(args.prompts))
    if want_fx != got_fx:
        bad.append(f"--prompts is {got_fx} but lane {lane!r} maps to the profile's "
                   f"_fixtures.{fxkey}, which names {want_fx}")
    if gr["7"]["inputs"]["text"] != P.get(key):
        bad.append("the positive prompt in the graph is not the fixture's string for "
                   + str(key))
    if gr["8"]["inputs"]["text"] != P.get("_negative"):
        bad.append("the negative in the graph is not the fixture's _negative")
    if bad:
        raise SystemExit(
            "ANDON: pre-flight - the values entering this graph disagree with "
            + os.path.basename(args.profile) + "'s decided texpass_brush block:\n  "
            + "\n  ".join(bad)
            + "\nNo workflow JSON was written. This check has no skip flag: it exists "
              "because brush_cloud_step.py binds no profile, so agreement between its "
              "constants and a subject's decided values is a coincidence until something "
              "asserts it. HALT.")
    same_p = blk.get("prompt", {}).get("value") == P.get(key)
    same_n = blk.get("negative", {}).get("value") == P.get("_negative")
    print(f"[pre-flight] PASS against {os.path.basename(args.profile)}: five recipe values "
          f"equal the decided block; lane {lane!r} -> --prompts IS _fixtures.{fxkey} "
          f"(corroborated against the job's state identity); the graph's strings are that "
          f"file's.", flush=True)
    print(f"[pre-flight]   the profile's documentation copies of prompt/negative "
          f"{'both match' if same_p and same_n else 'do NOT both match'} the fixture "
          f"(prompt {same_p}, negative {same_n}) - reported, not gated: the graph never "
          f"reads them.", flush=True)


if args.cmd == "graph":
    P = json.load(open(args.prompts, encoding="utf-8"))
    if not (args.key in P):
        raise AssertionError(f"ANDON: no prompt for {args.key} in {args.prompts}")
    rn = args.render_name or "render.png"
    mn = args.mask_name or "mask.png"
    # THE REGISTER COMES FROM THE PROFILE, not from DEFAULTS (Ruling 25e). This is the one
    # key that stops being a coincidence-of-value and becomes agreement by construction; the
    # pre-flight's (a) drops it and its (b2) asserts the structure instead. A profile with no
    # decided lora-w raises there, which is the lifecycle working.
    _prof = json.load(open(args.profile, encoding="utf-8"))
    _blk = _prof.get("tools", {}).get("texpass_brush.py", {})
    _lwe = _blk.get("lora-w") if isinstance(_blk, dict) else None
    if not (isinstance(_lwe, dict) and "value" in _lwe):
        raise AssertionError(
            f"ANDON: {args.profile} texpass_brush.py has no decided value for 'lora-w', so the "
            f"register is undeclared and the graph cannot be built either way. A ruling decides "
            f"it; this tool does not guess.")
    gr = build_graph(rn, mn, P[args.key], P["_negative"], args.seed, lora_w=_lwe["value"])
    preflight(gr, P, args.key)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    # sorted keys + fixed separators so a byte-comparison of two saved JSONs is meaningful
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(gr, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(f"[graph] wrote {args.out}")
    _reg = (f"lora_w {gr['5']['inputs']['strength_model']}" if "5" in gr
            else "lora NONE - no loader node in the graph (Ruling 10b/25e); "
                 "ModelSamplingAuraFlow reads the UNET directly")
    print(f"[graph]   key {args.key}  seed {gr['15']['inputs']['seed']}  "
          f"steps {gr['15']['inputs']['steps']}  cfg {gr['15']['inputs']['cfg']}  "
          f"{_reg}  cn {gr['12']['inputs']['strength']}")
    print(f"[graph]   inputs render={rn}  mask={mn}")
    print(f"[graph]   prompt chars {len(P[args.key])}")

elif args.cmd == "invar":
    em = np.asarray(Image.open(os.path.join(args.job, "render.png")).convert("RGB"),
                    dtype=np.float32)
    ed = np.asarray(Image.open(os.path.join(args.job, "inpainted.png")).convert("RGB"),
                    dtype=np.float32)
    if not (em.shape == ed.shape):
        raise AssertionError(
            f"ANDON: the returned image is {ed.shape}, emitted was {em.shape} — the cloud "
            f"re-sized it, so nothing downstream is comparable")
    # ⚠ THE OPERAND IS GEOMETRY, NOT COLOUR (E04 Ruling 26). This is E08 Amendment 32's fix
    # at its SECOND CONSUMER, and it took a fired gate on E04's first stroke to find it.
    #
    # HISTORICAL TEXT, kept because corrections happen in place: "the figure: emit composites
    # the subject onto a synthetic flat 0.42 grey (=107/255), so 'outside the figure' is
    # where the emitted render is still that grey."  ->  bg = |em - 107| < 1.5.
    #
    # That is colour as a proxy for absence of surface, and 0.42 is ALSO project_twins'
    # --hole-grey, so an unpainted HOLE ON REAL SURFACE renders at exactly the background
    # value and is indistinguishable from background BY COLOUR, BY CONSTRUCTION. A32
    # corrected this operand inside texpass_iter's commit and nobody grepped for the other
    # consumer; this one only executes when a stroke flies, so it sat unfixed until the next
    # stroke flew. Measured on E04 stroke 1: the check's "outside" set was 803,683 px of
    # which 0.26% was real surface, but its HOT pixels were 89.1% ON GEOMETRY, and the
    # 1,515 px component that halted the run was 93% on geometry and 93% inside the job mask
    # - the brush painting the hull's foot, which is what it was dispatched to do. Same
    # residual, same bounds, geometry operand: mean 0.216 -> 0.020 lv, largest component
    # 1,515 -> 40 px, HALT -> PASS.
    #
    # THE BOUNDS DO NOT MOVE. They were never the problem, and the same-bounds comparison
    # above is what proves it. Test the property, not a proxy for it.
    hp = os.path.join(args.job, "hit.png")
    if not os.path.exists(hp):
        raise SystemExit(
            f"ANDON: no hit.png in {args.job}. This check asks whether anything changed "
            f"WHERE THERE IS NO SURFACE, and emit's geometry mask is the only thing that "
            f"answers it - the colour it replaced cannot, because an unpainted hole renders "
            f"at the background value by construction. An invariance check with no geometry "
            f"cannot test, so it halts rather than falling back to the operand that was "
            f"withdrawn. Re-emit the job with a post-A32 texpass_iter. HALT.")
    hit = np.asarray(Image.open(hp).convert("L"), dtype=np.float32) > 127
    if not (hit.shape == em.shape[:2]):
        raise AssertionError(
            f"ANDON: hit.png is {hit.shape} but the render is {em.shape[:2]} - the geometry mask "
            f"does not belong to this job")
    outside = maximum_filter(hit.astype(np.float32), size=args.dilate) < 0.5
    n_out = int(outside.sum())
    if not (n_out > 1000):
        raise AssertionError(f"ANDON: only {n_out} px outside the dilated figure — cannot test")
    resid = np.abs(ed - em).max(axis=-1)
    ro = resid[outside]
    mean_r, max_r = float(ro.mean()), float(ro.max())
    hot = resid > args.conc_tol
    hot_out = hot & outside
    n_hot = int(hot_out.sum())
    lab, nl = label(hot_out)
    cc = int(np.bincount(lab.ravel())[1:].max()) if nl else 0
    print(f"[invar] outside the dilated figure: {n_out:,} px")
    print(f"[invar]   |edited - emitted|  mean {mean_r:.3f}  max {max_r:.1f}  "
          f"levels (8-bit)")
    print(f"[invar]   pixels over {args.conc_tol:.0f} levels: {n_hot:,} "
          f"({n_hot/n_out*100:.3f}%)  largest connected component {cc:,} px")
    # SHAPE, not just size (Amendment 30, refining Amendment 21). Uniform sub-unit = codec.
    # Concentrated = a repainted backdrop, which is structural and clusters.
    uniform = mean_r <= args.tol
    concentrated = cc >= 200
    if concentrated:
        raise SystemExit(
            f"ANDON: the residual outside the figure is CONCENTRATED — largest component "
            f"{cc:,} px over {args.conc_tol:.0f} levels. A structural change clusters; two "
            f"float kernels do not. The inpaint is repainting the backdrop, which voids "
            f"texpass_iter's corner-median licence (its operand is no longer flat). HALT.")
    if not uniform:
        raise SystemExit(
            f"ANDON: mean residual {mean_r:.3f} levels outside the figure exceeds "
            f"{args.tol:.1f} without being concentrated — diffuse but not sub-unit. Not a "
            f"codec boundary and not a repaint; report it rather than proceeding.")
    print(f"[invar] PASS — uniform and sub-unit ({mean_r:.3f} <= {args.tol:.1f} levels, "
          f"largest hot component {cc} < 200 px). Consistent with a codec boundary, and "
          f"the median of a near-flat field is unmoved, so the corner-median licence holds.")

elif args.cmd == "log":
    os.makedirs(os.path.dirname(os.path.abspath(args.run_log)), exist_ok=True)
    e = json.loads(args.entry)
    with open(args.run_log, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(e, sort_keys=True) + "\n")
    print(f"[log] appended to {args.run_log}: {list(e.keys())}")
