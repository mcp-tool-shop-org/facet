"""E12 handoff 3 Task 4 — the styled target pair's cloud workflow, built and CHECKED on disk.

The galleon's pair was submitted from a hand-retyped payload. E04 Arm G7 is why that is not
done again: a hand-retyped workflow with a SELF-REFERENCING link (`VAEDecode.samples =
["14", 0]`, node 14 feeding itself) returned `status: validated` from `dry_run`. **A dry_run
PASS does not prove link sanity.** So link topology is checked HERE, in code, before the file
is written, and the file is written before anything is submitted.

Same shape as `brush_cloud_step.py graph`, for the same reasons (E08 Amendment 30: the recipe
for a generative step is the submitted workflow JSON, not the invocation that submits it) —
but this is the TWIN/restylize graph, not the brush's inpaint graph. Node for node it is
`restylize_views.py`'s `graph()`, with two substitutions that are the whole reason a separate
builder exists:

  lora_name   `saltroad_style_v2_lowlr_000001500.safetensors`  ->  the CLOUD card name
  images      local paths                                      ->  uploaded cloud names

⚠ THE LORA NAME IS AN IMPORT, AND AN API SURFACE IS NOT GROUND TRUTH FOR ONE (E08 A31,
banked): `search_models` and the node's own option list both return zero for "saltroad" while
the card sits in the account's library. "Absent from the node list" does not mean absent.
The recorded card name is used, and `dry_run` is the check that it resolves — a wrong name
was rejected there before, at `not in (list of length 144)`.

PRE-FLIGHT, before the JSON exists, the `brush_cloud_step` pattern applied to this block:

  * the six recipe values checked BY VALUE against the profile's restylize_views block
  * prompt and negative checked BY PROVENANCE - that `--prompts` IS the file the profile's
    `_fixtures.twin_prompts` names, and that the strings entering the graph are that file's,
    unmodified. Provenance rather than value equality, because the profile's copy DOCUMENTS
    the fixture; on this subject the per-view stems (Ruling 9d) deliberately differ from it
    on the reduced views, so a value check would be wrong by construction.
  * link topology - every reference resolves to a node that exists, no node references
    itself, and every declared output index is plausible.

  e12_pair_cloud_step.py --key dragonclay_1 --prompts P.json --profile profiles/beast.json
                         --render-name R.png --control-name C.png --out J.json [--seed N]

Standards compliance: PIN_PER_STEP - the saved JSON is the recipe; every value in it is
either the profile's or a recorded per-invocation argument printed loudly. ANDON_AUTHORITY -
pre-flight and topology both raise and leave NO file behind, so a failed check cannot be
submitted; there is no skip flag. NAMED_COMPENSATORS - writes one JSON; undo = delete it.
EXTERNAL_VERIFIER - the topology check tests the failure mode `dry_run` was measured missing.
"""
import argparse
import json
import os
import sys

# ⚠ The cloud's name for the imported LoRA, byte-identical to brush_cloud_step.py's CLOUD_LORA.
# Kept as its own constant rather than imported, and then ASSERTED equal below, because that
# file is a CLI with argparse at import time.
CLOUD_LORA = ("mcp-tool-shop__saltroad-style-lora__"
              "saltroad_style_v2_lowlr_000001500.safetensors")

ap = argparse.ArgumentParser()
ap.add_argument("--key", required=True, help="prompt key = the input stem, e.g. dragonclay_1")
ap.add_argument("--prompts", required=True)
ap.add_argument("--profile", required=True,
                help="REQUIRED and deliberately unskippable (E04 Ruling 24): the subject "
                     "profile whose restylize_views block the graph's values are checked "
                     "against. An optional guard is a skip flag with a different name.")
ap.add_argument("--render-name", required=True, help="uploaded cloud name of the CLAY render")
ap.add_argument("--control-name", required=True, help="uploaded cloud name of the CONTROL")
ap.add_argument("--seed", type=int, default=None,
                help="explicit per-invocation seed for the ONE allowed re-roll; printed as a "
                     "recorded deviation and does not silence the value check")
ap.add_argument("--prefix", default=None, help="SaveImage filename_prefix")
ap.add_argument("--out", required=True)
args = ap.parse_args()

prof = json.load(open(args.profile, encoding="utf-8"))
blk = prof.get("tools", {}).get("restylize_views.py")
if not isinstance(blk, dict):
    raise SystemExit("ANDON: %s has no tools['restylize_views.py'] block, so there is nothing "
                     "to check the graph against." % args.profile)


def pv(k):
    e = blk.get(k)
    if not (isinstance(e, dict) and "value" in e):
        raise SystemExit("ANDON: %s restylize_views.py has no decided value for %r"
                         % (args.profile, k))
    return e["value"]


P = json.load(open(args.prompts, encoding="utf-8"))
if args.key not in P:
    raise SystemExit("ANDON: no prompt for %s in %s" % (args.key, args.prompts))
pos, neg = P[args.key], P["_negative"]
seed = pv("seed") if args.seed is None else args.seed

graph = {
    "1": {"class_type": "UNETLoader", "inputs": {
        "unet_name": "qwen_image_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
    "2": {"class_type": "CLIPLoader", "inputs": {
        "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image",
        "device": "default"}},
    "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
    "4": {"class_type": "ControlNetLoader", "inputs": {
        "control_net_name": "Qwen-Image-InstantX-ControlNet-Union.safetensors"}},
    "5": {"class_type": "LoraLoaderModelOnly", "inputs": {
        "model": ["1", 0], "lora_name": CLOUD_LORA, "strength_model": pv("lora-w")}},
    "6": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["5", 0], "shift": 3.1}},
    "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": pos}},
    "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": neg}},
    # the latent comes from the UNTOUCHED render, so the composite bg never ships
    "9": {"class_type": "LoadImage", "inputs": {"image": args.render_name}},
    "10": {"class_type": "LoadImage", "inputs": {"image": args.control_name}},
    "11": {"class_type": "ControlNetApplyAdvanced", "inputs": {
        "positive": ["7", 0], "negative": ["8", 0], "control_net": ["4", 0],
        "image": ["10", 0], "vae": ["3", 0], "strength": pv("cn-strength"),
        "start_percent": 0.0, "end_percent": 1.0}},
    "12": {"class_type": "VAEEncode", "inputs": {"pixels": ["9", 0], "vae": ["3", 0]}},
    "13": {"class_type": "KSampler", "inputs": {
        "model": ["6", 0], "seed": seed, "steps": pv("steps"), "cfg": pv("cfg"),
        "sampler_name": "euler", "scheduler": "simple", "positive": ["11", 0],
        "negative": ["11", 1], "latent_image": ["12", 0], "denoise": pv("denoise")}},
    "14": {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["3", 0]}},
    "15": {"class_type": "SaveImage", "inputs": {
        "images": ["14", 0], "filename_prefix": args.prefix or ("dragon_target_" + args.key)}},
}

bad = []

# (a) the six recipe values, by value against the decided block
entering = {"lora-w": graph["5"]["inputs"]["strength_model"],
            "cn-strength": graph["11"]["inputs"]["strength"],
            "steps": graph["13"]["inputs"]["steps"], "cfg": graph["13"]["inputs"]["cfg"],
            "denoise": graph["13"]["inputs"]["denoise"], "seed": graph["13"]["inputs"]["seed"]}
for k, got in entering.items():
    if k == "seed" and args.seed is not None:
        if got != args.seed:
            bad.append("graph seed %r is neither the profile's nor the explicit --seed %r"
                       % (got, args.seed))
        if got != pv("seed"):
            print("[pre-flight] DEVIATION, EXPLICIT: seed %s against the profile's %s. "
                  "Recorded per-invocation argument (the one-re-roll precedent, E08 A23), "
                  "not an undeclared constant." % (got, pv("seed")), flush=True)
        continue
    if got != pv(k):
        bad.append("graph %s = %r but the profile decides %r" % (k, got, pv(k)))

# (b) prompt and negative by PROVENANCE through the profile's declared fixture
fx = (prof.get("_fixtures", {}).get("twin_prompts", {}) or {}).get("path")
if not fx:
    bad.append("%s names no _fixtures.twin_prompts.path, so the strings entering the graph "
               "have no declared source" % os.path.basename(args.profile))
else:
    root = os.path.dirname(os.path.dirname(os.path.abspath(args.profile)))
    want = os.path.realpath(os.path.join(root, fx))
    got = os.path.realpath(os.path.abspath(args.prompts))
    if want != got:
        bad.append("--prompts is %s but the profile's _fixtures.twin_prompts names %s"
                   % (got, want))
if graph["7"]["inputs"]["text"] != P.get(args.key):
    bad.append("the positive in the graph is not the fixture's string for " + args.key)
if graph["8"]["inputs"]["text"] != P.get("_negative"):
    bad.append("the negative in the graph is not the fixture's _negative")

# (c) LINK TOPOLOGY — the check a dry_run PASS was measured NOT to perform (E04 Arm G7)
for nid, node in graph.items():
    for pin, val in node["inputs"].items():
        if not (isinstance(val, list) and len(val) == 2 and isinstance(val[0], str)):
            continue
        tgt, idx = val
        if tgt == nid:
            bad.append("SELF-LINK: node %s pin %r references itself — this is exactly the "
                       "shape that returned status: validated in E04 Arm G7" % (nid, pin))
        if tgt not in graph:
            bad.append("DANGLING: node %s pin %r references node %r, which does not exist"
                       % (nid, pin, tgt))
        if not isinstance(idx, int) or idx < 0 or idx > 3:
            bad.append("BAD OUTPUT INDEX: node %s pin %r -> [%r, %r]" % (nid, pin, tgt, idx))
# every node must be reached from SaveImage
# ⚠ the walk SKIPS targets that are not in the graph. Found by testing this file against a
# dangling target: the walk ran before `bad` was raised and died on KeyError '99', so the
# tool halted with a traceback instead of the report it exists to produce. Safe either way -
# no JSON is written on either path - but a traceback is not a report, and the dangling entry
# is already recorded above.
reached, stack = set(), ["15"]
while stack:
    n = stack.pop()
    if n in reached or n not in graph:
        continue
    reached.add(n)
    for val in graph[n]["inputs"].values():
        if isinstance(val, list) and len(val) == 2 and isinstance(val[0], str):
            stack.append(val[0])
orphan = set(graph) - reached
if orphan:
    bad.append("ORPHANED nodes not reachable from SaveImage: %s" % sorted(orphan))

if bad:
    raise SystemExit("ANDON: pre-flight — the graph disagrees with %s or is malformed:\n  %s"
                     "\nNo workflow JSON was written; nothing can be submitted. This check has "
                     "no skip flag." % (os.path.basename(args.profile), "\n  ".join(bad)))

os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(graph, fh, indent=1, sort_keys=True)
    fh.write("\n")
print("[pre-flight] PASS against %s: six recipe values equal the decided block; --prompts IS "
      "_fixtures.twin_prompts and the graph's strings are that file's; %d links resolve, no "
      "self-link, no dangling target, no orphan."
      % (os.path.basename(args.profile),
         sum(1 for n in graph.values() for v in n["inputs"].values()
             if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str))), flush=True)
print("[graph] wrote %s" % args.out)
print("[graph]   key %s  seed %s  steps %s  cfg %s  denoise %s  lora_w %s  cn %s"
      % (args.key, seed, pv("steps"), pv("cfg"), pv("denoise"), pv("lora-w"),
         pv("cn-strength")))
print("[graph]   lora %s" % CLOUD_LORA)
print("[graph]   render=%s  control=%s" % (args.render_name, args.control_name))
print("[graph]   prompt %d chars, %d terms" % (len(pos), len(pos.split(","))))
sys.exit(0)
