"""MV-Adapter ig2mv, LICENSE-FREE path — the production runner.

Chain: SDXL (OpenRAIL++, commercial-ok) + MV-Adapter (open) + OUR geometry maps
(render_geomaps.py: open3d Apache-2.0 raycasting — proven equivalent to the
nvdiffrast maps at <1/255 MAE on all 6 views, 2026-08-03). nvdiffrast (NVIDIA
NON-commercial) is never imported: a tripwire stub occupies its module name and
RAISES if any code path touches it — the licence guard is structural, not attested.

  ig2mv_licensefree.py --ctrl geomaps/ctrl.npy --image twin.png --text "..."
                       --output out.png [--seed 770700] [--remove-bg]
"""
import argparse
import sys
import types


class _LicenceTripwire(types.ModuleType):
    """Occupies nvdiffrast's module name. Import bookkeeping (dunders, submodule
    binding) passes; any FUNCTIONAL attribute — the calls that would execute the
    non-commercial code — raises. Guard is structural, not attested."""

    def __getattr__(self, name):
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)          # normal module-introspection miss
        if name == "torch":
            return sys.modules["nvdiffrast.torch"]
        raise RuntimeError(
            f"LICENCE GUARD: nvdiffrast.{name} was invoked — the non-commercial "
            f"dependency must never execute in this pipeline. A code path changed; "
            f"halt and re-audit.")


for _name in ("nvdiffrast", "nvdiffrast.torch"):
    _m = _LicenceTripwire(_name)
    _m.__file__ = "<licence-stub>"
    _m.__path__ = []
    sys.modules[_name] = _m

import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from transformers import AutoModelForImageSegmentation

from diffusers import AutoencoderKL, DDPMScheduler, LCMScheduler, UNet2DConditionModel
from mvadapter.models.attention_processor import DecoupledMVRowColSelfAttnProcessor2_0
from mvadapter.pipelines.pipeline_mvadapter_i2mv_sdxl import MVAdapterI2MVSDXLPipeline
from mvadapter.schedulers.scheduling_shift_snr import ShiftSNRScheduler
from mvadapter.utils.saving import make_image_grid

ap = argparse.ArgumentParser()
ap.add_argument("--ctrl", required=True, help="ctrl.npy from render_geomaps.py")
ap.add_argument("--image", required=True, help="reference image (the styled twin)")
ap.add_argument("--text", default="high quality")
ap.add_argument("--output", required=True)
ap.add_argument("--base-model", default="stabilityai/stable-diffusion-xl-base-1.0")
ap.add_argument("--vae-model", default="madebyollin/sdxl-vae-fp16-fix")
ap.add_argument("--adapter-path", default="huanngzh/mv-adapter")
ap.add_argument("--num-inference-steps", type=int, default=50)
ap.add_argument("--guidance-scale", type=float, default=3.0)
ap.add_argument("--reference-conditioning-scale", type=float, default=1.0)
ap.add_argument("--seed", type=int, default=-1)
ap.add_argument("--remove-bg", action="store_true")
ap.add_argument("--device", default="cuda")
args = ap.parse_args()

device, dtype = args.device, torch.float16

ctrl = np.load(args.ctrl)                       # (N, H, W, 6) in [0,1]
num_views, height, width = ctrl.shape[0], ctrl.shape[1], ctrl.shape[2]
control_images = torch.from_numpy(ctrl).permute(0, 3, 1, 2).float().to(device)

pipe_kwargs = {}
if args.vae_model:
    pipe_kwargs["vae"] = AutoencoderKL.from_pretrained(args.vae_model)
pipe = MVAdapterI2MVSDXLPipeline.from_pretrained(args.base_model, **pipe_kwargs)
pipe.scheduler = ShiftSNRScheduler.from_scheduler(
    pipe.scheduler, shift_mode="interpolated", shift_scale=8.0, scheduler_class=None)
pipe.init_custom_adapter(
    num_views=num_views, self_attn_processor=DecoupledMVRowColSelfAttnProcessor2_0)
pipe.load_custom_adapter(args.adapter_path, weight_name="mvadapter_ig2mv_sdxl.safetensors")
pipe.to(device=device, dtype=dtype)
pipe.cond_encoder.to(device=device, dtype=dtype)
pipe.enable_vae_slicing()

reference_image = Image.open(args.image)


def preprocess_image(image, height, width):
    image = np.array(image)
    alpha = image[..., 3] > 0
    H, W = alpha.shape
    y, x = np.where(alpha)
    y0, y1 = max(y.min() - 1, 0), min(y.max() + 1, H)
    x0, x1 = max(x.min() - 1, 0), min(x.max() + 1, W)
    image_center = image[y0:y1, x0:x1]
    H, W, _ = image_center.shape
    if H > W:
        W = int(W * (height * 0.9) / H)
        H = int(height * 0.9)
    else:
        H = int(H * (width * 0.9) / W)
        W = int(width * 0.9)
    image_center = np.array(Image.fromarray(image_center).resize((W, H)))
    start_h = (height - H) // 2
    start_w = (width - W) // 2
    out = np.zeros((height, width, 4), dtype=np.uint8)
    out[start_h:start_h + H, start_w:start_w + W] = image_center
    out = out.astype(np.float32) / 255.0
    out = out[:, :, :3] * out[:, :, 3:4] + (1 - out[:, :, 3:4]) * 0.5
    return Image.fromarray((out * 255).clip(0, 255).astype(np.uint8))


if args.remove_bg:
    birefnet = AutoModelForImageSegmentation.from_pretrained(
        "ZhengPeng7/BiRefNet", trust_remote_code=True)
    birefnet.to(device)
    tfm = transforms.Compose([
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    img = reference_image.convert("RGB")
    with torch.no_grad():
        preds = birefnet(tfm(img).unsqueeze(0).to(device))[-1].sigmoid().cpu()
    mask = transforms.ToPILImage()(preds[0].squeeze()).resize(img.size)
    img.putalpha(mask)
    reference_image = preprocess_image(img, height, width)
elif reference_image.mode == "RGBA":
    reference_image = preprocess_image(reference_image, height, width)

gen = None
if args.seed != -1:
    gen = torch.Generator(device=device).manual_seed(args.seed)

images = pipe(
    args.text,
    height=height,
    width=width,
    num_inference_steps=args.num_inference_steps,
    guidance_scale=args.guidance_scale,
    num_images_per_prompt=num_views,
    control_image=control_images,
    control_conditioning_scale=1.0,
    reference_image=reference_image,
    reference_conditioning_scale=args.reference_conditioning_scale,
    negative_prompt="watermark, ugly, deformed, noisy, blurry, low contrast",
    generator=gen,
).images

make_image_grid(images, rows=1).save(args.output)
for i, im in enumerate(images):
    im.save(args.output.replace(".png", f"_v{i}.png"))
print(f"[ig2mv-free] wrote {args.output} ({num_views} views) — nvdiffrast never loaded",
      flush=True)
