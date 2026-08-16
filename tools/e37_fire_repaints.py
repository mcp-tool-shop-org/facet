"""E37 Phase 2 firing pass -- union mask, held-pixel re-check, payload build, composite, dE proof.

Ruling 25 fires the repaints; Ruling 26 corrects seven jobs to six (v4's two ear masks
are two masks on ONE view and ride one repaint as a union mask) and adopts the
repaint-proof requirement: after each composite, measure dE inside the mask against the
original -- a same-seed repaint that reproduces its own defect must read as NO CHANGE,
never as a repair.

Receipts are append-only (Ruling 23): this writes only under phase2fire/, never over
phase2/masks_v2/.

Subcommands:
  prep       build the firing masks: v4 union + closed-rect held hardening, shrink-only
  payload    emit one repaint payload from a byte-pinned set-A base
  composite  composite a downloaded repaint through its feathered mask + dE proof
  lift       composite the v0 lift at a given rung

Mask-count conventions, stated once because three legitimate counts exist on one mask:
  poly_px   the hand-placed polygon's fill (minus any held island) -- this is what
            masks_v2.json records as `core_px`; reproduces exactly on all eight
  half_px   alpha > 0.5 -- the ladder's "8,908 texels" for the lift region
  supp_px   alpha > 0   -- the feathered support
"""
import argparse
import json
import os

import numpy as np
from PIL import Image

PHASE1 = r"E:/AI/training/facet_E37/phase1"
PHASE2 = r"E:/AI/training/facet_E37/phase2"
FIRE = r"E:/AI/training/facet_E37/phase2fire"

HELD_RECTS = {"v6nose": [196, 112, 224, 142], "v7band": [214, 116, 236, 134]}


# ---------------------------------------------------------------- colour

def srgb_to_linear(a):
    a = a.astype(np.float64) / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(a):
    a = np.clip(a, 0.0, 1.0)
    return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)


_M = np.array([[0.4124564, 0.3575761, 0.1804375],
               [0.2126729, 0.7151522, 0.0721750],
               [0.0193339, 0.1191920, 0.9503041]])
_WP = np.array([0.95047, 1.00000, 1.08883])


def rgb_to_lab(rgb8):
    lin = srgb_to_linear(rgb8)
    xyz = lin @ _M.T / _WP

    def f(t):
        d = 6.0 / 29.0
        return np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4.0 / 29.0)

    fx, fy, fz = f(xyz[..., 0]), f(xyz[..., 1]), f(xyz[..., 2])
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], axis=-1)


def delta_e76(a, b):
    return np.sqrt(((a - b) ** 2).sum(axis=-1))


# ---------------------------------------------------------------- union

def counts(m):
    return {"poly_or_full_px": int((m == 1.0).sum()), "half_px": int((m > 0.5).sum()),
            "supp_px": int((m > 0).sum())}


def harden_held(m, name):
    """Zero the mask over the CLOSED held rect.

    The ratified masks were cut against a HALF-OPEN held rect: on v7band the guarantee
    reads exactly 0.0000 over [116:134, 214:236] -- reproducing the recorded value -- while
    the CLOSED rect [116:135, 214:237] carries one pixel at (236,134) = 8/255. That single
    corner pixel is the whole disagreement, and it is resolved the way Ruling 21 already
    ruled this conflict's general form: the mask is cut, the hold does not yield. The
    alternative -- reading the checker on the half-open rect so the gate goes green -- is
    narrowing a test to make a red gate pass, and is rejected in writing here.

    The edit is shrink-only by construction and asserted so below.
    """
    x0, y0, x1, y1 = HELD_RECTS[name]
    out = m.copy()
    out[y0:y1 + 1, x0:x1 + 1] = 0.0
    return out


def cmd_prep(args):
    """Build the firing masks: v4 union, closed-rect held hardening, shrink-only.

    ANDON: every check here raises rather than asserts (E21 Ruling 2 -- a gate that decides
    whether an irreversible step proceeds must raise; `assert` is deletable by -O).
    """
    dst = os.path.join(FIRE, "masks_fire")
    os.makedirs(dst, exist_ok=True)
    src = os.path.join(PHASE2, "masks_v2")
    rec = json.load(open(os.path.join(src, "masks_v2.json")))

    def load(fn):
        return np.asarray(Image.open(os.path.join(src, fn)).convert("L")).astype(np.float64) / 255.0

    # ---- v4's two ear masks ride ONE repaint as a union (Ruling 26).
    L, R = load("mask_v4_v4earL.png"), load("mask_v4_v4earR.png")
    overlap = int(((L > 0) & (R > 0)).sum())
    U = np.maximum(L, R)
    cl, cr, cu = counts(L), counts(R), counts(U)
    # ANDON: a union that is not the disjoint sum of its parts has merged two feathers
    # and is no longer the pair of ratified masks.
    if overlap != 0 or any(cu[k] != cl[k] + cr[k] for k in cu):
        raise SystemExit(
            f"ANDON: v4 union is not disjoint -- overlap {overlap} px; union {cu} against "
            f"L {cl} + R {cr}. The two ratified masks would not survive the union.")

    jobs = {
        "v1chest": ("mask_v1_v1chest.png", 1, load("mask_v1_v1chest.png")),
        "v3ear": ("mask_v3_v3ear.png", 3, load("mask_v3_v3ear.png")),
        "v4earUNION": ("mask_v4_v4earUNION.png", 4, U),
        "v5ear": ("mask_v5_v5ear.png", 5, load("mask_v5_v5ear.png")),
        "v6nose": ("mask_v6_v6nose.png", 6, load("mask_v6_v6nose.png")),
        "v7band": ("mask_v7_v7band.png", 7, load("mask_v7_v7band.png")),
        "v0lift": ("mask_v0_v0lift.png", 0, load("mask_v0_v0lift.png")),
    }

    out_rec = {
        "ruling": "25 fires; 26 makes v4 one job; the held rect is hardened to CLOSED here",
        "union": {"overlap_px": overlap, "counts": cu, "L": cl, "R": cr},
        "held": {}, "masks": {},
    }

    for tag, (fn, view, m) in jobs.items():
        before = counts(m)
        if tag in HELD_RECTS:
            closed_max_before = float(m[HELD_RECTS[tag][1]:HELD_RECTS[tag][3] + 1,
                                        HELD_RECTS[tag][0]:HELD_RECTS[tag][2] + 1].max())
            m2 = harden_held(m, tag)
            x0, y0, x1, y1 = HELD_RECTS[tag]
            closed_max_after = float(m2[y0:y1 + 1, x0:x1 + 1].max())
            # ANDON: identity-adjacent paint moves only at the Director's word (Ruling 21).
            if closed_max_after != 0.0:
                raise SystemExit(f"ANDON: held-pixel guarantee BROKEN on {tag} -- closed-rect max "
                                 f"{closed_max_after:.6f}, must be exactly 0.0")
            out_rec["held"][tag] = {
                "held_rect_closed": [x0, y0, x1, y1],
                "closed_max_before_hardening": closed_max_before,
                "closed_max_after_hardening": closed_max_after,
                "half_open_max": float(m[y0:y1, x0:x1].max()),
                "px_zeroed": int(((m > 0) & (m2 == 0)).sum()),
            }
            m = m2
        after = counts(m)
        # ANDON: the only legal edit here is a shrink. Growing a mask admits paint nobody walked.
        if any(after[k] > before[k] for k in after):
            raise SystemExit(f"ANDON: {tag} GREW under hardening -- before {before}, after {after}")
        Image.fromarray((m * 255.0 + 0.5).astype(np.uint8), mode="L").save(os.path.join(dst, fn))
        out_rec["masks"][tag] = {"file": fn, "view": view, "before": before, "after": after,
                                 "recorded_core_px": rec["masks"].get(tag, {}).get("core_px")}
        print(f"[prep] {tag:11s} v{view}  poly {after['poly_or_full_px']:6d}  half {after['half_px']:6d}  "
              f"supp {after['supp_px']:6d}" + ("  (held rect hardened to CLOSED)" if tag in HELD_RECTS else ""))

    json.dump(out_rec, open(os.path.join(dst, "masks_fire.json"), "w"), indent=1)
    for k, v in out_rec["held"].items():
        print(f"[held] {k}: closed-rect max {v['closed_max_before_hardening']:.6f} -> "
              f"{v['closed_max_after_hardening']:.6f}  ({v['px_zeroed']} px zeroed); "
              f"half-open rect was {v['half_open_max']:.6f}")
    print(f"[write] {dst}")


# ---------------------------------------------------------------- payload

def cmd_payload(args):
    """Emit one repaint payload: base + SetLatentNoiseMask + ColorMatchV2(mkl, ref=original twin)."""
    base = json.load(open(os.path.join(PHASE1, "payloads", f"set2026081511_v{args.view}.json")))
    before = json.dumps(base, sort_keys=True)

    for nid in ("12", "13", "14", "15"):
        if nid not in base:
            raise SystemExit(f"ANDON: base payload for v{args.view} lacks node {nid}")
    if base["13"]["inputs"]["latent_image"] != ["12", 0]:
        raise SystemExit(f"ANDON: KSampler latent_image is {base['13']['inputs']['latent_image']}, expected ['12',0]")
    if base["15"]["inputs"]["images"] != ["14", 0]:
        raise SystemExit(f"ANDON: SaveImage images is {base['15']['inputs']['images']}, expected ['14',0]")

    base["20"] = {"class_type": "LoadImage", "inputs": {"image": args.mask_name}}
    base["21"] = {"class_type": "ImageToMask", "inputs": {"image": ["20", 0], "channel": "red"}}
    base["22"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["12", 0], "mask": ["21", 0]}}
    base["13"]["inputs"]["latent_image"] = ["22", 0]

    base["23"] = {"class_type": "LoadImage", "inputs": {"image": args.ref_name}}
    base["24"] = {"class_type": "ColorMatchV2", "inputs": {
        "image_target": ["14", 0], "image_ref": ["23", 0],
        "method": "mkl", "strength": 1.0, "multithread": True}}
    base["15"]["inputs"]["images"] = ["24", 0]
    base["15"]["inputs"]["filename_prefix"] = args.prefix

    # A payload that did not change cannot be the repaint payload (a check that can fail).
    if json.dumps(base, sort_keys=True) == before:
        raise SystemExit("ANDON: payload unchanged after edit")
    if base["13"]["inputs"]["seed"] != 2026081511:
        raise SystemExit(f"ANDON: seed moved to {base['13']['inputs']['seed']}; the repaint is same-seed by ruling")

    ids = set(base)
    for nid, node in base.items():
        for k, v in node["inputs"].items():
            if isinstance(v, list) and len(v) == 2 and isinstance(v[0], str):
                if v[0] not in ids:
                    raise SystemExit(f"ANDON: node {nid}.{k} links to missing node {v[0]}")
                if v[0] == nid:
                    raise SystemExit(f"ANDON: node {nid}.{k} self-links")

    os.makedirs(os.path.join(FIRE, "payloads"), exist_ok=True)
    out = os.path.join(FIRE, "payloads", f"repaint_{args.tag}.json")
    json.dump(base, open(out, "w"), indent=1)
    print(f"[payload] {out}  seed {base['13']['inputs']['seed']}  mask {args.mask_name}  ref {args.ref_name}")


# ---------------------------------------------------------------- composite

def cmd_composite(args):
    """Composite a repaint through its feathered mask; then the Ruling-26 dE proof."""
    orig = np.asarray(Image.open(args.orig).convert("RGB")).astype(np.uint8)
    rep = np.asarray(Image.open(args.repaint).convert("RGB")).astype(np.uint8)
    m = np.asarray(Image.open(args.mask).convert("L")).astype(np.float64) / 255.0

    if orig.shape != rep.shape:
        raise SystemExit(f"ANDON: shape mismatch orig {orig.shape} vs repaint {rep.shape}")
    if m.shape != orig.shape[:2]:
        raise SystemExit(f"ANDON: mask shape {m.shape} vs image {orig.shape[:2]}")

    a = m[..., None]
    comp_lin = srgb_to_linear(orig) * (1 - a) + srgb_to_linear(rep) * a
    comp = (linear_to_srgb(comp_lin) * 255.0 + 0.5).astype(np.uint8)

    # Outside the mask, nothing may move: the composite is the original there, exactly.
    outside = m <= 0.0
    moved = int((comp[outside] != orig[outside]).any(axis=-1).sum())
    if moved:
        raise SystemExit(f"ANDON: {moved} px outside the mask moved in the composite")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    Image.fromarray(comp).save(args.out)

    # ---- Ruling 26 proof: dE inside the mask, composite against the original.
    lab_o = rgb_to_lab(orig)
    lab_c = rgb_to_lab(comp)
    lab_r = rgb_to_lab(rep)
    de_comp = delta_e76(lab_o, lab_c)
    de_raw = delta_e76(lab_o, lab_r)

    core = m >= 0.999
    supp = m > 0.0
    proof = {
        "mask": os.path.basename(args.mask),
        "core_px": int(core.sum()),
        "support_px": int(supp.sum()),
        "dE_core": {
            "mean": float(de_comp[core].mean()), "median": float(np.median(de_comp[core])),
            "p90": float(np.percentile(de_comp[core], 90)), "max": float(de_comp[core].max()),
            "pct_over_1": float((de_comp[core] > 1.0).mean() * 100),
            "pct_over_2": float((de_comp[core] > 2.0).mean() * 100),
        },
        "dE_raw_core_before_compositing": {
            "mean": float(de_raw[core].mean()), "median": float(np.median(de_raw[core])),
        },
        "dE_whole_frame_raw": {
            "mean": float(de_raw.mean()), "median": float(np.median(de_raw)),
        },
    }
    json.dump(proof, open(args.out.replace(".png", "_proof.json"), "w"), indent=1)
    c = proof["dE_core"]
    print(f"[composite] {os.path.basename(args.out)}  core {proof['core_px']} px  "
          f"dE mean {c['mean']:.2f} median {c['median']:.2f} p90 {c['p90']:.2f} max {c['max']:.2f}  "
          f">1: {c['pct_over_1']:.1f}%  >2: {c['pct_over_2']:.1f}%")


# ---------------------------------------------------------------- locality

def cmd_locality(args):
    """Did the repaint land where this view's mask is?

    The upload names are server-assigned and are NOT a content digest of the file (checked:
    md5/sha1/sha256/sha384/sha512/blake2b/blake2s/sha3_256 all miss), so the mask->view
    pairing cannot be verified from the name. It CAN be verified from the result:
    SetLatentNoiseMask preserves the latent outside the mask, so a correctly paired job
    moves paint inside the mask and leaves the rest at the VAE round-trip plus the
    whole-frame ColorMatchV2 residual.

    A check that can fail: if the wrong view's mask flew, the moved region would not
    coincide with this view's mask and the ratio below would collapse toward 1.
    """
    orig = np.asarray(Image.open(args.orig).convert("RGB")).astype(np.uint8)
    rep = np.asarray(Image.open(args.repaint).convert("RGB")).astype(np.uint8)
    m = np.asarray(Image.open(args.mask).convert("L")).astype(np.float64) / 255.0

    de = delta_e76(rgb_to_lab(orig), rgb_to_lab(rep))
    inside, outside = m > 0.0, m <= 0.0

    ins_mean, out_mean = float(de[inside].mean()), float(de[outside].mean())
    ratio = ins_mean / out_mean if out_mean > 0 else float("inf")

    # Where the frame actually moved most, against where the mask is.
    thr = float(np.percentile(de, 99.5))
    hot = de >= thr
    hot_in = float((hot & inside).sum() / max(hot.sum(), 1) * 100)
    ys, xs = np.nonzero(m > 0)
    mys, mxs = np.nonzero(hot)
    rec = {
        "mask": os.path.basename(args.mask),
        "dE_inside_mean": ins_mean, "dE_outside_mean": out_mean, "ratio_inside_over_outside": ratio,
        "dE_inside_p90": float(np.percentile(de[inside], 90)),
        "dE_outside_p99": float(np.percentile(de[outside], 99)),
        "mask_bbox_xyxy": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
        "hot_bbox_xyxy": [int(mxs.min()), int(mys.min()), int(mxs.max()), int(mys.max())],
        "pct_of_hottest_0p5pct_inside_mask": hot_in,
    }
    if args.out:
        json.dump(rec, open(args.out, "w"), indent=1)
    print(f"[locality] {rec['mask']}  dE in {ins_mean:.3f} / out {out_mean:.3f} = {ratio:.1f}x  "
          f"| hottest 0.5% inside mask: {hot_in:.1f}%  "
          f"| mask bbox {rec['mask_bbox_xyxy']}  hot bbox {rec['hot_bbox_xyxy']}")


# ---------------------------------------------------------------- lift

def cmd_lift(args):
    """The v0 face tone lift: multiplicative gain in linear light, target L* = L*0 + dL*mask."""
    orig = np.asarray(Image.open(args.src).convert("RGB")).astype(np.uint8)
    m = np.asarray(Image.open(args.mask).convert("L")).astype(np.float64) / 255.0
    if m.shape != orig.shape[:2]:
        raise SystemExit(f"ANDON: mask shape {m.shape} vs image {orig.shape[:2]}")

    lab0 = rgb_to_lab(orig)
    L0 = lab0[..., 0]
    Lt = L0 + args.dL * m

    def L_to_Y(L):
        fy = (L + 16.0) / 116.0
        d = 6.0 / 29.0
        return np.where(fy > d, fy ** 3, 3 * d * d * (fy - 4.0 / 29.0))

    y0, yt = L_to_Y(L0), L_to_Y(Lt)
    gain = np.where(y0 > 1e-8, yt / np.maximum(y0, 1e-8), 1.0)
    out = linear_to_srgb(srgb_to_linear(orig) * gain[..., None])
    out8 = (out * 255.0 + 0.5).astype(np.uint8)

    outside = m <= 0.0
    moved = int((out8[outside] != orig[outside]).any(axis=-1).sum())
    if moved:
        raise SystemExit(f"ANDON: {moved} px outside the lift mask moved")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    Image.fromarray(out8).save(args.out)

    core = m >= 0.999
    Lm = rgb_to_lab(out8)[..., 0]
    rec = {
        "dL_target": args.dL,
        "core_px": int(core.sum()),
        "L_median_before": float(np.median(L0[core])),
        "L_median_after": float(np.median(Lm[core])),
        "measured_delta": float(np.median(Lm[core]) - np.median(L0[core])),
        "p10_before": float(np.percentile(L0[core], 10)),
        "p90_before": float(np.percentile(L0[core], 90)),
    }
    json.dump(rec, open(args.out.replace(".png", "_lift.json"), "w"), indent=1)
    print(f"[lift] +{args.dL} L*  core {rec['core_px']} px  "
          f"L* median {rec['L_median_before']:.2f} -> {rec['L_median_after']:.2f} "
          f"(measured {rec['measured_delta']:+.2f})")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("prep").set_defaults(func=cmd_prep)

    q = sub.add_parser("payload")
    q.add_argument("--view", type=int, required=True)
    q.add_argument("--mask-name", required=True)
    q.add_argument("--ref-name", required=True)
    q.add_argument("--prefix", required=True)
    q.add_argument("--tag", required=True)
    q.set_defaults(func=cmd_payload)

    q = sub.add_parser("composite")
    q.add_argument("--orig", required=True)
    q.add_argument("--repaint", required=True)
    q.add_argument("--mask", required=True)
    q.add_argument("--out", required=True)
    q.set_defaults(func=cmd_composite)

    q = sub.add_parser("locality")
    q.add_argument("--orig", required=True)
    q.add_argument("--repaint", required=True)
    q.add_argument("--mask", required=True)
    q.add_argument("--out", default=None)
    q.set_defaults(func=cmd_locality)

    q = sub.add_parser("lift")
    q.add_argument("--src", required=True)
    q.add_argument("--mask", required=True)
    q.add_argument("--dL", type=float, required=True)
    q.add_argument("--out", required=True)
    q.set_defaults(func=cmd_lift)

    a = p.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
