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


def control_image(path):
    """Composite for contrast, Canny, then OR in the mask's morphological gradient."""
    rgb = np.asarray(Image.open(path).convert("RGB"), dtype=np.float32) / 255.0
    fm = figure_mask(rgb, args.tol, args.erode)
    comp = rgb * fm[..., None] + BG * (1.0 - fm[..., None])
    grey = (comp.mean(axis=-1) * 255).astype(np.uint8)
    edges = cv2.Canny(grey, int(args.canny_low * 255), int(args.canny_high * 255))
    k = np.ones((args.contour_width, args.contour_width), np.uint8)
    contour = cv2.morphologyEx((fm > 0.5).astype(np.uint8) * 255,
                               cv2.MORPH_GRADIENT, k)
    ctrl = np.maximum(edges, contour)
    return ctrl, int((edges > 0).sum()), int((contour > 0).sum()), int((ctrl > 0).sum())


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


def graph(render_name, ctrl_name):
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
            "clip": ["2", 0], "text": args.prompt}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["2", 0], "text": args.negative}},
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


for path in args.inputs:
    stem = os.path.splitext(os.path.basename(path))[0]
    ctrl, n_edge, n_contour, n_ctrl = control_image(path)
    ctrl_path = os.path.join(args.outdir, f"{stem}_control.png")
    Image.fromarray(ctrl).save(ctrl_path)
    print(f"[restyle] {stem}: control image {n_ctrl:,} px "
          f"(canny {n_edge:,} + contour {n_contour:,})", flush=True)
    if n_contour < 500:
        raise SystemExit(f"ANDON: figure mask produced almost no contour "
                         f"({n_contour} px) — keying failed on {stem}")

    req = urllib.request.Request(
        f"{BASE}/prompt",
        data=json.dumps({"prompt": graph(upload(path), upload(ctrl_path)),
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
                break
        if time.time() - t0 > 900:
            raise SystemExit(f"ANDON: restylize timed out on {stem} (900s)")
