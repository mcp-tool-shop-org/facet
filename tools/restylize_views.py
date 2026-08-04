"""Make a mesh's OWN styled twins — contour-locked restylize of its renders.

Twins are not a reusable asset. A styled twin is a restylize of a render of ONE
mesh, so it carries that mesh's silhouette; projecting A0's twins through a
correctly-fitted W3 camera put A0's wider limb spread beside W3's narrower body
and collapsed styled coverage from 62% to 22.7% (E01). Whenever the mesh changes
— a fresh reconstruction, a decimation that moves the silhouette, a head graft —
the twins have to be made again from that mesh.

THE CONTROL IMAGE IS BUILT, NOT DISCOVERED. The first version of this file fed
the raw render to a Canny node and failed, measured: on `turn_render`'s Workbench
output — flat grey figure on flat grey background by design — Canny returned 6,482
edge pixels (0.84%) that were almost entirely INTERIOR creases, with no outer
contour. With nothing holding the silhouette, denoise 0.92 regenerated the
character: silhouette IoU against its own source render was 0.290 front / 0.266
back, bbox x/y came back 0.797 against the source's 0.458, and the BACK view
returned facing forward. The textured render was worse (0.68%, edge bbox 580 px
against an 847 px figure). The recipe had been developed against lit concept art,
which has a background gradient and a cast shadow and therefore real silhouette
contrast, and was carried to an image class that has none.

So the contour is constructed in two deterministic steps rather than hoped for:
composite the keyed figure onto a contrasting background so the boundary becomes a
hard edge Canny fires on, then OR the mask's morphological gradient into the edge
map so the contour is present whether or not a threshold found it. Keying is
`project_twins.py`'s — top-corner median, tol 0.06, eroded — so mask logic lives
in one place. The control image is written beside the output; look at it when a
twin comes back wrong.

The DIFFUSION latent still comes from the untouched render, so the composite
background never reaches the output.

  restylize_views.py --inputs w3clay_0.png w3clay_4.png --outdir DIR
                     [--denoise 0.92] [--lora-w 0.75] [--cn-strength 0.9]
                     [--seed 770700] [--prompt ...]
"""
import argparse
import json
import os
import time
import urllib.parse
import urllib.request
import uuid

import cv2
import numpy as np
from PIL import Image
from scipy.ndimage import minimum_filter

ap = argparse.ArgumentParser()
ap.add_argument("--inputs", nargs="+", required=True)
ap.add_argument("--outdir", required=True)
ap.add_argument("--prompts",
                help="versioned JSON of per-view prompts, keyed by INPUT STEM, with an "
                     "optional _negative. The twin pair this project treats as canon was "
                     "made with prompts that were never written down — E02-prompts.json "
                     "holds the eight brush strokes, not the two twin cameras — so the "
                     "character cannot be regenerated. A prompt that lives only in a shell "
                     "history is the same defect texpass_loop.ps1 was rewritten to remove.")
ap.add_argument("--masks", nargs="+", default=None,
                help="figure mask per input, parallel to --inputs. Supply the exact "
                     "mesh silhouette here; without it the mask is keyed off the "
                     "render, which E08 measured losing 24%% of the silhouette on a "
                     "grey-on-grey clay.")
ap.add_argument("--host", default="127.0.0.1:8188")
ap.add_argument("--seed", type=int, default=770700)
ap.add_argument("--steps", type=int, default=20)
ap.add_argument("--cfg", type=float, default=2.5)
ap.add_argument("--denoise", type=float, default=0.92,
                help="0.92 measured: high enough for the LoRA to land its full "
                     "palette on a grey clay render. It only holds pose if the "
                     "control image actually carries the contour — see module docstring.")
ap.add_argument("--lora-w", type=float, default=0.75)
ap.add_argument("--cn-strength", type=float, default=0.9)
ap.add_argument("--canny-low", type=float, default=0.4)
ap.add_argument("--canny-high", type=float, default=0.8)
ap.add_argument("--bg", default="0,0,0",
                help="composite background behind the keyed figure, for contrast")
ap.add_argument("--contour-width", type=int, default=3,
                help="kernel for the mask's morphological gradient, in pixels")
ap.add_argument("--tol", type=float, default=0.06, help="figure keying tolerance")
ap.add_argument("--erode", type=int, default=5, help="figure mask erode, project_twins' value")
ap.add_argument("--prompt", default=(
    "a burly bald warrior with a long red beard, dark green knitted sleeveless "
    "tunic, polished gold pauldrons, gold necklace, dark red layered cloth skirt "
    "with a leather belt, heavy dark boots, holding a massive greatsword, plain "
    "grey background, visible brushstrokes, painterly worked surface"))
ap.add_argument("--negative", default="watermark, text, logo, blurry, photo, deformed")
args = ap.parse_args()
BASE = f"http://{args.host}"
BG = np.array([float(v) for v in args.bg.split(",")], dtype=np.float32)
if BG.max() > 1.0:
    BG = BG / 255.0
os.makedirs(args.outdir, exist_ok=True)


def figure_mask(img, tol, erode):
    """project_twins.py's keying, unchanged — one place for mask logic."""
    c = np.concatenate([img[:8, :8].reshape(-1, 3), img[:8, -8:].reshape(-1, 3)])
    bg = np.median(c, axis=0)
    fm = (np.abs(img - bg).max(axis=-1) > tol).astype(np.float32)
    return minimum_filter(fm, size=erode)


def control_image(path, mask_path=None):
    """Composite for contrast, Canny, then OR in the mask's morphological gradient.

    The mask answers "where is the figure". Keying the render for it is what E01 fixed
    for the CANNY term (composite onto contrast first) and left in place here, and E08
    measured the cost on W3: the keyed clay mask held 111,602 px of a 146,356 px
    silhouette, IoU 0.76, losing a stripe down the whole blade. --masks supplies the
    exact mesh silhouette instead, which makes the CONTOUR term identical for any two
    renders of the same mesh from the same camera — the property this arm needs, and
    the last place figure_mask still governed anything.
    """
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    if mask_path:
        fm = (np.asarray(Image.open(mask_path).convert("L"), dtype=np.float32)
              / 255.0 > 0.5).astype(np.float32)
    else:
        fm = figure_mask(rgb, args.tol, args.erode)
    comp = rgb * fm[..., None] + BG * (1.0 - fm[..., None])
    grey = (comp.mean(axis=-1) * 255).astype(np.uint8)
    edges = cv2.Canny(grey, int(args.canny_low * 255), int(args.canny_high * 255))
    k = np.ones((args.contour_width, args.contour_width), np.uint8)
    contour = cv2.morphologyEx((fm > 0.5).astype(np.uint8) * 255,
                               cv2.MORPH_GRADIENT, k)
    ctrl = np.maximum(edges, contour)
    return (ctrl, fm, int((edges > 0).sum()), int((contour > 0).sum()),
            int((ctrl > 0).sum()))


def upload(path):
    name = os.path.basename(path)
    boundary = uuid.uuid4().hex
    with open(path, "rb") as fh:
        data = fh.read()
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; "
        f"filename=\"{name}\"\r\nContent-Type: image/png\r\n\r\n").encode() + data + (
        f"\r\n--{boundary}\r\nContent-Disposition: form-data; "
        f"name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n").encode()
    req = urllib.request.Request(
        f"{BASE}/upload/image", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    return json.load(urllib.request.urlopen(req, timeout=60))["name"]


def graph(render_name, ctrl_name, pos, neg):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "qwen_image_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image",
            "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "ControlNetLoader", "inputs": {
            "control_net_name": "Qwen-Image-InstantX-ControlNet-Union.safetensors"}},
        "5": {"class_type": "LoraLoaderModelOnly", "inputs": {
            "model": ["1", 0],
            "lora_name": "saltroad_style_v2_lowlr_000001500.safetensors",
            "strength_model": args.lora_w}},
        "6": {"class_type": "ModelSamplingAuraFlow", "inputs": {
            "model": ["5", 0], "shift": 3.1}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["2", 0], "text": pos}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["2", 0], "text": neg}},
        # latent comes from the UNTOUCHED render, so the composite bg never ships
        "9": {"class_type": "LoadImage", "inputs": {"image": render_name}},
        "10": {"class_type": "LoadImage", "inputs": {"image": ctrl_name}},
        "11": {"class_type": "ControlNetApplyAdvanced", "inputs": {
            "positive": ["7", 0], "negative": ["8", 0], "control_net": ["4", 0],
            "image": ["10", 0], "vae": ["3", 0], "strength": args.cn_strength,
            "start_percent": 0.0, "end_percent": 1.0}},
        "12": {"class_type": "VAEEncode", "inputs": {"pixels": ["9", 0], "vae": ["3", 0]}},
        "13": {"class_type": "KSampler", "inputs": {
            "model": ["6", 0], "seed": args.seed, "steps": args.steps, "cfg": args.cfg,
            "sampler_name": "euler", "scheduler": "simple", "positive": ["11", 0],
            "negative": ["11", 1], "latent_image": ["12", 0],
            "denoise": args.denoise}},
        "14": {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["3", 0]}},
        "15": {"class_type": "SaveImage", "inputs": {
            "images": ["14", 0], "filename_prefix": "restylize"}},
    }


if args.masks:
    assert len(args.masks) == len(args.inputs), (
        f"ANDON: {len(args.masks)} masks for {len(args.inputs)} inputs — --masks is "
        f"parallel to --inputs")
PROMPTS = json.load(open(args.prompts, encoding="utf-8")) if args.prompts else {}
for _i, path in enumerate(args.inputs):
    stem = os.path.splitext(os.path.basename(path))[0]
    pos = PROMPTS.get(stem, args.prompt)
    neg = PROMPTS.get("_negative", args.negative)
    if args.prompts and stem not in PROMPTS:
        print(f"[restyle] {stem}: NOT in {os.path.basename(args.prompts)} — falling back "
              f"to --prompt. A per-view prompt is how a rear camera is kept from being "
              f"told about a beard (E01).", flush=True)
    ctrl, fm, n_edge, n_contour, n_ctrl = control_image(
        path, args.masks[_i] if args.masks else None)
    ctrl_path = os.path.join(args.outdir, f"{stem}_control.png")
    Image.fromarray(ctrl).save(ctrl_path)
    # The exact figure mask, saved beside the twin. project_twins consumes this
    # rather than re-keying: it comes from the render the twin was made from, so
    # it is registered by construction. Heuristic re-keying on a painted twin with
    # a background gradient keyed a THIRD of the lower background as figure and
    # projected it onto the mesh (measured on A0's twins, E01).
    mask_path = os.path.join(args.outdir, f"{stem}_mask.png")
    Image.fromarray((fm > 0.5).astype(np.uint8) * 255).save(mask_path)
    print(f"[restyle] {stem}: control image {n_ctrl:,} px "
          f"(canny {n_edge:,} + contour {n_contour:,}); figure mask "
          f"{(fm > 0.5).mean() * 100:.1f}% -> {os.path.basename(mask_path)}",
          flush=True)
    if n_contour < 500:
        raise SystemExit(f"ANDON: figure mask produced almost no contour "
                         f"({n_contour} px) — keying failed on {stem}")

    req = urllib.request.Request(
        f"{BASE}/prompt",
        data=json.dumps({"prompt": graph(upload(path), upload(ctrl_path), pos, neg),
                         "client_id": "restylize"}).encode(),
        headers={"Content-Type": "application/json"})
    pid = json.load(urllib.request.urlopen(req, timeout=60))["prompt_id"]
    print(f"[restyle] {stem}: queued {pid}", flush=True)
    t0 = time.time()
    while True:
        time.sleep(3)
        h = json.load(urllib.request.urlopen(f"{BASE}/history/{pid}", timeout=30))
        if pid in h:
            status = h[pid].get("status", {})
            if status.get("status_str") == "error":
                msgs = [m for m in status.get("messages", [])
                        if m[0] == "execution_error"]
                raise SystemExit(f"ANDON: comfy execution error: {msgs}")
            outs = h[pid].get("outputs", {})
            if outs:
                img = outs["15"]["images"][0]
                q = urllib.parse.urlencode({
                    "filename": img["filename"], "subfolder": img.get("subfolder", ""),
                    "type": img["type"]})
                dst = os.path.join(args.outdir, f"{stem}.png")
                with open(dst, "wb") as fh:
                    fh.write(urllib.request.urlopen(f"{BASE}/view?{q}", timeout=120).read())
                print(f"[restyle] {stem} -> {dst}  ({time.time() - t0:.0f}s)", flush=True)
                # Provenance travels WITH the artifact. The pair this project treats as
                # canon has an unknown-parameters section in its manifest because no
                # sidecar existed when it was made, and it therefore cannot be
                # regenerated — measured, not feared (E08 director ruling).
                import hashlib
                side = {
                    "output": os.path.basename(dst),
                    "output_sha256": hashlib.sha256(open(dst, "rb").read()).hexdigest(),
                    "input": os.path.abspath(path),
                    "input_sha256": hashlib.sha256(open(path, "rb").read()).hexdigest(),
                    "mask": os.path.abspath(args.masks[_i]) if args.masks else None,
                    "mask_source": "file" if args.masks else "keyed from the render",
                    "prompt": pos, "negative": neg,
                    "prompts_file": os.path.abspath(args.prompts) if args.prompts else None,
                    "prompt_from_file": bool(args.prompts and stem in PROMPTS),
                    "seed": args.seed, "steps": args.steps, "cfg": args.cfg,
                    "denoise": args.denoise, "lora_w": args.lora_w,
                    "cn_strength": args.cn_strength,
                    "canny_low": args.canny_low, "canny_high": args.canny_high,
                    "bg": args.bg, "contour_width": args.contour_width,
                    "tol": args.tol, "erode": args.erode,
                    "control_px": {"total": n_ctrl, "canny": n_edge, "contour": n_contour},
                    "figure_mask_pct_of_frame": round(float((fm > 0.5).mean() * 100), 3),
                }
                with open(os.path.join(args.outdir, f"{stem}_gen.json"), "w",
                          encoding="utf-8") as fh:
                    json.dump(side, fh, indent=1)
                print(f"[restyle] {stem}: provenance -> {stem}_gen.json", flush=True)
                break
        if time.time() - t0 > 900:
            raise SystemExit(f"ANDON: restylize timed out on {stem} (900s)")
