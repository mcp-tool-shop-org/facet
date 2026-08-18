"""TEXTURE-SPACE PASS — the BRUSH. Runs one emitted job through local ComfyUI:
Qwen fp8 + saltroad LoRA + InstantX Inpainting-ControlNet, latent-masked so only
the hole region synthesizes. Output lands in the job dir as inpainted.png; the
write-head's commit step then filters by mask again (belt + braces — pixels
outside the job mask never reach the atlas even if the model drifts them).

  texpass_brush.py --job DIR [--seed 770700] [--steps 20] [--cfg 2.5]
                   [--lora-w 0.75] [--prompt ...] [--host 127.0.0.1:8188]
"""
import argparse
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import subject_profile
import canon_gate
import json
import os
import time
import urllib.parse
import urllib.request
import uuid

ap = argparse.ArgumentParser()
ap.add_argument("--job", required=True)
ap.add_argument("--host", default="127.0.0.1:8188")
ap.add_argument("--seed", type=int, default=770700)
ap.add_argument("--steps", type=int, default=20)
ap.add_argument("--cfg", type=float, default=2.5)
ap.add_argument("--lora-w", type=float, default=0.75)
ap.add_argument("--cn-strength", type=float, default=1.0)
ap.add_argument("--prompt", default=(
    "a burly bald warrior with a long red beard, dark green knitted sleeveless "
    "tunic, polished gold pauldrons, gold necklace, dark red layered cloth skirt "
    "with a leather belt, heavy dark boots, holding a massive greatsword, plain "
    "grey background, visible brushstrokes, painterly worked surface"))
ap.add_argument("--negative", default="watermark, text, logo, blurry, photo, deformed")
ap.add_argument("--canon", default=None,
                help="surfaces JSON. The fallback --prompt is refused if it "
                     "does not cover the ratified rows. Per-job stems from "
                     "a prompts file are not this check.")
ap.add_argument("--subject", default=None,
                help="census subject id. Names the identity-only escape.")
ap.add_argument("--no-canon", action="store_true",
                help="explicit ungated escape for an identity-only subject.")
args = ap.parse_args(subject_profile.bind(ap, "texpass_brush.py", None))
BASE = f"http://{args.host}"
# Fail-closed BEFORE any upload. texpass_loop.ps1 is a transport; this
# is the irreversible step. Andon keeps its type.
_canon = canon_gate.require_canon(
    args.prompt, canon_path=args.canon, subject=args.subject,
    no_canon=args.no_canon, profile_path=getattr(args, "profile", None))
if not _canon["gated"]:
    print("[canon] UNGATED: %s" % _canon["note"], flush=True)
elif (_canon.get("coverage") or {}).get("unratified_ids"):
    print("[canon] unratified (named, not required): %s"
          % ",".join(_canon["coverage"]["unratified_ids"]), flush=True)


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
    r = json.load(urllib.request.urlopen(req, timeout=60))
    return r["name"]


rname = upload(os.path.join(args.job, "render.png"))
mname = upload(os.path.join(args.job, "mask.png"))
print(f"[brush] uploaded {rname}, {mname}", flush=True)

g = {
    "1": {"class_type": "UNETLoader", "inputs": {
        "unet_name": "qwen_image_fp8_e4m3fn.safetensors", "weight_dtype": "default"}},
    "2": {"class_type": "CLIPLoader", "inputs": {
        "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors", "type": "qwen_image",
        "device": "default"}},
    "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
    "4": {"class_type": "ControlNetLoader", "inputs": {
        "control_net_name": "Qwen-Image-InstantX-ControlNet-Inpainting.safetensors"}},
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
    "9": {"class_type": "LoadImage", "inputs": {"image": rname}},
    "10": {"class_type": "LoadImage", "inputs": {"image": mname}},
    "11": {"class_type": "ImageToMask", "inputs": {
        "image": ["10", 0], "channel": "red"}},
    "12": {"class_type": "ControlNetInpaintingAliMamaApply", "inputs": {
        "positive": ["7", 0], "negative": ["8", 0], "control_net": ["4", 0],
        "vae": ["3", 0], "image": ["9", 0], "mask": ["11", 0],
        "strength": args.cn_strength, "start_percent": 0.0, "end_percent": 1.0}},
    "13": {"class_type": "VAEEncode", "inputs": {"pixels": ["9", 0], "vae": ["3", 0]}},
    "14": {"class_type": "SetLatentNoiseMask", "inputs": {
        "samples": ["13", 0], "mask": ["11", 0]}},
    "15": {"class_type": "KSampler", "inputs": {
        "model": ["6", 0], "seed": args.seed, "steps": args.steps, "cfg": args.cfg,
        "sampler_name": "euler", "scheduler": "simple", "positive": ["12", 0],
        "negative": ["12", 1], "latent_image": ["14", 0], "denoise": 1.0}},
    "16": {"class_type": "VAEDecode", "inputs": {"samples": ["15", 0], "vae": ["3", 0]}},
    "17": {"class_type": "SaveImage", "inputs": {
        "images": ["16", 0], "filename_prefix": "texpass"}},
}

req = urllib.request.Request(
    f"{BASE}/prompt",
    data=json.dumps({"prompt": g, "client_id": "texpass"}).encode(),
    headers={"Content-Type": "application/json"})
resp = json.load(urllib.request.urlopen(req, timeout=60))
pid = resp["prompt_id"]
print(f"[brush] queued {pid}", flush=True)

t0 = time.time()
while True:
    time.sleep(3)
    h = json.load(urllib.request.urlopen(f"{BASE}/history/{pid}", timeout=30))
    if pid in h:
        entry = h[pid]
        status = entry.get("status", {})
        if status.get("status_str") == "error":
            msgs = [m for m in status.get("messages", []) if m[0] == "execution_error"]
            raise SystemExit(f"ANDON: comfy execution error: {msgs}")
        outs = entry.get("outputs", {})
        if outs:
            img = outs["17"]["images"][0]
            q = urllib.parse.urlencode({
                "filename": img["filename"],
                "subfolder": img.get("subfolder", ""), "type": img["type"]})
            data = urllib.request.urlopen(f"{BASE}/view?{q}", timeout=60).read()
            dst = os.path.join(args.job, "inpainted.png")
            with open(dst, "wb") as fh:
                fh.write(data)
            # seed-stamped copy: a re-roll must never destroy the prior stroke
            with open(os.path.join(args.job, f"inpainted_s{args.seed}.png"), "wb") as fh:
                fh.write(data)
            print(f"[brush] {dst}  ({time.time()-t0:.0f}s)", flush=True)
            break
    if time.time() - t0 > 900:
        raise SystemExit("ANDON: brush timed out (900s)")
