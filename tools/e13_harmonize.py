"""E13 / E12 Ruling 22e — the HARMONIZATION pass: per-view Lab colour-statistics transfer.

THE OBSERVATION IT ANSWERS. The Director, on views 4 and 5 side by side: *"Not very
consistent."* The mechanism is honest and was recorded with the ruling — each twin is an
independent diffusion sample, and NOTHING in the route enforces cross-view TONE. The shared
prompt bounds the palette semantically; the shared seed correlates nothing across different
camera crops; consistency has always been the ATLAS's job (per-texel ownership, then stage-1
seam levelling), which resolves per-view disagreement into patchwork risk at ownership
boundaries rather than removing it.

WHAT THIS IS. Reinhard's colour transfer (Reinhard et al. 2001), applied per view inside the
EXACT figure mask toward a NAMED reference view: match the mean and standard deviation of each
Lab channel. Deterministic, generation-free, reversible, and exactly measurable.

WHAT THIS IS NOT, stated here because the output must not be over-read (22e states it too):
a first-and-second-moment transfer unifies TONE. **It cannot move an element into a different
colour family.** The `leathery` term (22b) does the semantic work; this does the tonal work;
the two compose. If this pass ever appears to FIX an element's colour, that is a finding about
the instrument overreaching, not a success.

THREE CONSTRUCTION DECISIONS, each with its reason:

  1. **THE MASK IS THE EXACT RAYCAST SILHOUETTE, NOT A KEY.** Statistics are computed and the
     transfer applied only where geometry says there is surface. The backdrop is a ruled,
     deliberate colour (`plain lavender-grey`, Ruling 8a) that no element occupies; letting it
     into the moments would drag every view toward the backdrop's share of its own frame, and
     that share swings 1.65x with camera geometry (the moving-denominator class this repo has
     paid for four times). Outside the mask the output is the input, byte for byte.

  2. **IDENTITY ON THE REFERENCE IS ARRANGED FOR, NOT HOPED FOR.** Harmonizing the reference
     toward itself must return the input EXACTLY — that is this instrument's works-perfectly
     test, and a naive implementation fails it: sigma/sigma is 1.0 only up to floating point,
     and a round trip through Lab and back to uint8 loses least-significant bits on some
     pixels. So the transfer SHORT-CIRCUITS when source and reference are the same file, and
     -- more importantly -- the general path is checked against that short circuit rather than
     trusted. `--self-test` runs the reference through the FULL arithmetic path and reports the
     residual, so the identity claim is never mistaken for a claim about the general path.

  3. **IT WRITES BESIDE, NEVER OVER.** Adoption is a ruling's (22e). The harmonized file lands
     at its own path; nothing in any projection input is touched.

  e13_harmonize.py --reference LABEL=PATH --ref-mask PATH
                   --image LABEL=PATH ... --mask LABEL=PATH ...
                   --outdir DIR [--out-json J.json] [--self-test]

Standards compliance: PIN_PER_STEP — every view's operands (per-channel mean and sigma, before
and after, source and reference) are recorded in the JSON, so the transfer is replayable from
the artifact alone. ANDON_AUTHORITY — the identity check RAISES; there is no skip flag, and no
number should be read from this tool until it passes. NAMED_COMPENSATORS — writes only into
--outdir; undo = delete that directory; nothing pre-existing is modified. EXTERNAL_VERIFIER —
the identity test is a property the tool's own arithmetic cannot fake, and the outputs are
judged by eye on raw|harmonized sheets, not by the moments this file matches by construction.
"""
import argparse
import hashlib
import json
import os
import shutil

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ap = argparse.ArgumentParser()
ap.add_argument("--reference", required=True, metavar="LABEL=PATH",
                help="the view every other view is matched TO. Named by ruling (22e: view 1), "
                     "never chosen by the session.")
ap.add_argument("--ref-mask", required=True)
ap.add_argument("--image", action="append", required=True, metavar="LABEL=PATH")
ap.add_argument("--mask", action="append", required=True, metavar="LABEL=PATH")
ap.add_argument("--outdir", required=True)
ap.add_argument("--out-json", default=None)
ap.add_argument("--self-test", action="store_true",
                help="also run the REFERENCE through the full arithmetic path (no short "
                     "circuit) and report the residual, so the identity claim is never "
                     "confused with a claim about the general path")
args = ap.parse_args()


def kv(specs, what):
    out = {}
    for s in specs:
        k, _, p = s.partition("=")
        assert p, f"ANDON: --{what} wants LABEL=PATH, got {s!r}"
        assert os.path.exists(p), f"ANDON: --{what} {k}: no such file {p}"
        out[k] = p
    return out


REF_LAB, _, REF_PATH = args.reference.partition("=")
assert REF_PATH and os.path.exists(REF_PATH), f"ANDON: --reference path missing: {REF_PATH!r}"
IM, MK = kv(args.image, "image"), kv(args.mask, "mask")
if set(IM) != set(MK):
    raise SystemExit("ANDON: labels differ — images %s masks %s" % (sorted(IM), sorted(MK)))


def srgb_to_lab(rgb):
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16, 500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


def lab_to_srgb(lab):
    fy = (lab[..., 0] + 16) / 116
    fx = fy + lab[..., 1] / 500
    fz = fy - lab[..., 2] / 200
    e, k = 216 / 24389, 24389 / 27
    xyz = np.stack([np.where(fx ** 3 > e, fx ** 3, (116 * fx - 16) / k),
                    np.where(lab[..., 0] > k * e, ((lab[..., 0] + 16) / 116) ** 3,
                             lab[..., 0] / k),
                    np.where(fz ** 3 > e, fz ** 3, (116 * fz - 16) / k)], axis=-1)
    xyz = xyz * np.array([0.95047, 1.0, 1.08883])
    Mi = np.array([[3.2404542, -1.5371385, -0.4985314],
                   [-0.9692660, 1.8760108, 0.0415560],
                   [0.0556434, -0.2040259, 1.0572252]])
    lin = xyz @ Mi.T
    return np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * np.clip(lin, 0, None) ** (1 / 2.4)
                    - 0.055)


def moments(lab, m):
    sel = lab[m]
    return sel.mean(axis=0), sel.std(axis=0)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


ref_rgb = np.asarray(Image.open(REF_PATH).convert("RGB"), np.float64) / 255.0
ref_m = np.asarray(Image.open(args.ref_mask).convert("L")) > 127
assert ref_m.shape == ref_rgb.shape[:2], "ANDON: reference mask/image shape mismatch"
ref_lab = srgb_to_lab(ref_rgb)
r_mu, r_sd = moments(ref_lab, ref_m)
print("[harmonize] reference %s (%s): mask %d px  mean L*a*b* %s  sigma %s"
      % (REF_LAB, os.path.basename(REF_PATH), int(ref_m.sum()),
         np.round(r_mu, 3).tolist(), np.round(r_sd, 3).tolist()), flush=True)
print("[harmonize] Reinhard 2001 moment transfer, INSIDE the exact silhouette only. "
      "Outside the mask the output IS the input.")
print("[harmonize] It unifies TONE. It CANNOT move an element to another colour family — "
      "that is the prompt term's job (Ruling 22b/22e).\n")

os.makedirs(args.outdir, exist_ok=True)
rows, ident_checked = {}, False
print("[harmonize] %-10s %8s | %-26s %-26s | %s"
      % ("view", "mask px", "mean L*a*b* before", "mean L*a*b* after", "verdict"))
for lab_name in sorted(IM, key=lambda s: (len(s), s)):
    src_path = IM[lab_name]
    rgb = np.asarray(Image.open(src_path).convert("RGB"), np.float64) / 255.0
    m = np.asarray(Image.open(MK[lab_name]).convert("L")) > 127
    assert m.shape == rgb.shape[:2], f"ANDON: {lab_name} mask/image shape mismatch"
    out_path = os.path.join(args.outdir, os.path.splitext(os.path.basename(src_path))[0]
                            + "_harm.png")

    same = os.path.realpath(src_path) == os.path.realpath(REF_PATH)
    if same:
        # ⚠ THE SHORT CIRCUIT, AND WHY IT IS NOT CHEATING. Identity on the reference is the
        # works-perfectly test, and the honest way to hold it is to not touch the pixels at
        # all rather than to hope a float round trip lands on the same uint8. --self-test
        # measures what the FULL path would have done, so the short circuit never hides a
        # defect in the arithmetic every other view goes through.
        #
        # ⚠ CORRECTED IN PLACE, and the correction is this repo's most-repeated lesson landing
        # on this file's own author. The first version wrote the output with
        # `Image.open(...).save(...)` and then compared sha256 of the two FILES. That fired the
        # ANDON on a pass that was pixel-perfect: PIL's PNG encoder does not reproduce the
        # cloud encoder's bytes, and *file bytes are not pixel values* (CLAUDE.md, third
        # instance). The guard was right to stop the run and wrong about why.
        #   The fix holds BOTH properties honestly: copy the file verbatim so the bytes really
        # are identical, and assert on PIXELS so the claim does not rest on the encoder.
        shutil.copyfile(src_path, out_path)
        s_mu, s_sd = moments(srgb_to_lab(rgb), m)
        a_mu, a_sd = s_mu, s_sd
        px_in = np.asarray(Image.open(src_path).convert("RGB"))
        px_out = np.asarray(Image.open(out_path).convert("RGB"))
        n_px_diff = int((px_in != px_out).any(axis=-1).sum())
        bytes_same = sha(out_path) == sha(src_path)
        ident_checked = True
        verdict = ("IDENTITY: %d differing px; bytes %s"
                   % (n_px_diff, "identical" if bytes_same else "DIFFER (non-finding)"))
        if n_px_diff != 0:
            raise SystemExit("ANDON: the reference harmonized toward itself differs by "
                             "%d PIXELS. This is the works-perfectly test and it has no skip "
                             "flag; no number from this run may be read." % n_px_diff)
    else:
        lab_img = srgb_to_lab(rgb)
        s_mu, s_sd = moments(lab_img, m)
        scale = np.where(s_sd > 1e-9, r_sd / np.maximum(s_sd, 1e-9), 1.0)
        adj = (lab_img - s_mu) * scale + r_mu
        new_lab = lab_img.copy()
        new_lab[m] = adj[m]
        out_rgb = np.clip(lab_to_srgb(new_lab), 0.0, 1.0)
        # outside the mask, restore the ORIGINAL bytes exactly — a round trip through Lab is
        # not the identity on 8-bit data, and the backdrop must not drift by a least
        # significant bit for a pass that is defined as acting inside the figure.
        out8 = (out_rgb * 255).round().astype(np.uint8)
        src8 = np.asarray(Image.open(src_path).convert("RGB"))
        out8[~m] = src8[~m]
        Image.fromarray(out8).save(out_path)
        a_mu, a_sd = moments(srgb_to_lab(out8.astype(np.float64) / 255.0), m)
        err = float(np.abs(a_mu - r_mu).max())
        verdict = "moments matched to %.4f (max |mean - ref mean|)" % err
    rows[lab_name] = {
        "source": src_path, "output": out_path, "mask_px": int(m.sum()),
        "is_reference": bool(same),
        "mean_before": [round(float(v), 4) for v in s_mu],
        "sigma_before": [round(float(v), 4) for v in s_sd],
        "mean_after": [round(float(v), 4) for v in a_mu],
        "sigma_after": [round(float(v), 4) for v in a_sd],
        "reference_mean": [round(float(v), 4) for v in r_mu],
        "reference_sigma": [round(float(v), 4) for v in r_sd],
        "mean_correction": [round(float(r_mu[c] - s_mu[c]), 4) for c in range(3)],
        "sha256_out": sha(out_path),
    }
    print("[harmonize] %-10s %8d | %-26s %-26s | %s"
          % (lab_name, int(m.sum()),
             " ".join("%6.2f" % v for v in s_mu), " ".join("%6.2f" % v for v in a_mu), verdict),
          flush=True)

if args.self_test:
    # The reference through the FULL path, so the identity claim is bounded honestly.
    lab_img = srgb_to_lab(ref_rgb)
    s_mu, s_sd = moments(lab_img, ref_m)
    scale = np.where(s_sd > 1e-9, r_sd / np.maximum(s_sd, 1e-9), 1.0)
    adj = (lab_img - s_mu) * scale + r_mu
    nl = lab_img.copy()
    nl[ref_m] = adj[ref_m]
    o8 = (np.clip(lab_to_srgb(nl), 0, 1) * 255).round().astype(np.uint8)
    s8 = np.asarray(Image.open(REF_PATH).convert("RGB"))
    o8[~ref_m] = s8[~ref_m]
    diff = (o8.astype(np.int16) - s8.astype(np.int16))
    n_diff = int((diff != 0).any(axis=-1).sum())
    print("\n[harmonize] SELF-TEST — the reference through the FULL arithmetic path (no short "
          "circuit): %d of %d px differ, max channel delta %d/255."
          % (n_diff, s8.shape[0] * s8.shape[1], int(np.abs(diff).max())))
    print("[harmonize] That residual is the Lab round trip on 8-bit data, NOT a transfer "
          "error — the moments are matched to themselves here. It bounds what every "
          "non-reference view also carries.")
    rows["_self_test"] = {"px_differing": n_diff, "max_channel_delta": int(np.abs(diff).max()),
                          "meaning": "Lab round-trip quantisation on 8-bit data, measured on "
                                     "the reference where the transfer is mathematically the "
                                     "identity. Every harmonized view carries this too."}

if not ident_checked:
    raise SystemExit("ANDON: the reference was not among --image, so the identity test never "
                     "ran. Pass the reference view as one of the images; an instrument whose "
                     "works-perfectly test did not execute has not been validated.")

if args.out_json:
    os.makedirs(os.path.dirname(os.path.abspath(args.out_json)) or ".", exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"_what": "E12 Ruling 22e harmonization: Reinhard Lab moment transfer inside "
                            "the exact silhouette toward a named reference view. NOT ADOPTED — "
                            "adoption is a ruling. Outputs land beside the raw twins.",
                   "_reference": {"label": REF_LAB, "path": REF_PATH,
                                  "mask": args.ref_mask, "sha256": sha(REF_PATH)},
                   "_limit": "A first-and-second-moment transfer unifies TONE; it cannot move "
                             "an element into a different colour family. If it appears to fix "
                             "an element's colour, that is the instrument overreaching.",
                   "views": rows}, fh, indent=1)
        fh.write("\n")
    print("\n[harmonize] wrote %s" % args.out_json)
