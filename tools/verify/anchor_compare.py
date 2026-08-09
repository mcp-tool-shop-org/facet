"""Is this re-production the recorded output - and if not, what is the difference's shape?

COMPARE-ONLY, BY RULING. E28 Ruling 10 commissioned this tool at the Director's word ("at
least 8 tools, if it could be done honestly... a tool that is forced is worse than no tool
at all") with the decomposition as the honesty condition: THE TOOL COMPARES, THE CALLER
REPLAYS. A recipe-runner would be a shell with the safety surface the census's axis F
refused at instrument scale - 88 of 99 diagnostics execute at import, and a tool that runs
recipes inherits every one of those bodies. So the replay is the caller's act, this file
never executes anything, and the payload states `replay: caller-supplied` so the boundary
reads as designed rather than forgotten.

TWO TIERS, AND THE SPLIT IS THE PRODUCT. This repo has halted twice on a byte-hash
mismatch between pixel-identical renders (encoder metadata moves run to run), and CLAUDE.md
carries the law: FILE BYTES ARE NOT PIXEL VALUES. So:

  byte tier   always: sha256 of both files, `byte_identical`. Gate-eligible ONLY for
              artifacts whose bytes are the contract (the E08-armB state / E04-step-0
              class), and the payload carries that caveat next to the number - a caller
              who gates a render on the byte tier is repeating the recorded mistake.
  pixel tier  when both inputs are images of equal WxH: `pixel_identical`, differing-pixel
              count and fraction, the LARGEST CONNECTED COMPONENT of differing pixels (the
              two-thresholds law: total alone cannot tell one wrong garment from ordinary
              speckle), |delta| percentiles and Lab dE beside them as diagnostics, and the
              SHAPE as an N x N grid of per-cell differing fractions. The grid is CARRIED,
              never reduced to a uniformity score: a structural difference concentrates, a
              kernel difference spreads (the E04 hardware-anchor reading), and collapsing
              that to one invented number is where forcing would begin (Ruling 10's bound).

WHAT IT DOES NOT DO. No recipe execution, no verdict, no threshold. Read-only on both
inputs. If a payload field would need a statistic the record has not earned, the field is
refused rather than filled - that refusal is the specification working.

  anchor_compare.py --a recorded.png --b candidate.png [--grid 8] [--out j.json]

Standards compliance: PIN_PER_STEP - the grid size is a flag and is echoed; both inputs'
hashes ride the payload. ANDON_AUTHORITY - structured refusals (dimension mismatch naming
both, pixel tier of a non-image naming the byte tier as what exists); raises, no skip
flag. NAMED_COMPENSATORS - reads two files, writes one JSON; undo = delete it.
DECOMPOSE_BY_SECRETS - no subject constant anywhere; both subjects arrive as flags.
EXTERNAL_VERIFIER - emits comparisons; adopts nothing; the caller's eye rules.
"""
import argparse
import hashlib
import json
import os
import sys


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Compare a recorded artifact against a caller-supplied "
                    "re-production: byte tier always, pixel tier for images.")
    ap.add_argument("--a", required=True, help="the recorded artifact")
    ap.add_argument("--b", required=True, help="the candidate re-production")
    ap.add_argument("--grid", type=int, default=8,
                    help="N for the N x N difference-shape grid")
    ap.add_argument("--out", default=None, help="write the payload JSON here")
    args = ap.parse_args(argv)

    for tag, p in (("--a", args.a), ("--b", args.b)):
        if not os.path.isfile(p):
            raise RuntimeError("ANDON: %s names no file: %s" % (tag, p))
    if args.grid < 1:
        raise RuntimeError("ANDON: --grid must be >= 1, got %d" % args.grid)

    rec = {
        "a": os.path.abspath(args.a), "b": os.path.abspath(args.b),
        "replay": "caller-supplied",
        "replay_note": ("this tool COMPARES; the replay that produced --b is "
                        "the caller's act, by E28 Ruling 10's decomposition - "
                        "a recipe-runner would execute arbitrary module "
                        "bodies, the exact surface the census refused"),
        "byte": {
            "a_sha256": sha256_file(args.a),
            "b_sha256": sha256_file(args.b),
            "a_bytes": os.path.getsize(args.a),
            "b_bytes": os.path.getsize(args.b),
        },
    }
    rec["byte"]["byte_identical"] = (
        rec["byte"]["a_sha256"] == rec["byte"]["b_sha256"])
    rec["byte"]["gate_eligibility"] = (
        "byte_identical is gate-eligible ONLY for artifacts whose bytes are "
        "the contract (the E08-armB state / E04-step-0 class). On renders, "
        "encoder metadata moves the bytes of pixel-identical images - this "
        "repo has false-halted on that twice - so a byte mismatch there is "
        "NOT evidence the render changed. Read the pixel tier.")

    # ---- pixel tier: only when both inputs decode as images ----------------
    pix = {"attempted": False}
    imgs = []
    for p in (args.a, args.b):
        try:
            from PIL import Image
            with Image.open(p) as im:
                imgs.append(im.convert("RGBA"))
        except Exception as exc:
            imgs.append(exc)
    a_img, b_img = imgs
    both_images = not isinstance(a_img, Exception) and \
        not isinstance(b_img, Exception)

    if both_images and a_img.size != b_img.size:
        raise RuntimeError(
            "ANDON: dimension mismatch - %s is %dx%d, %s is %dx%d. A pixel "
            "comparison of different frames would measure the framing, not "
            "the difference; re-produce at the recorded frame or compare "
            "bytes only." % (args.a, a_img.size[0], a_img.size[1],
                             args.b, b_img.size[0], b_img.size[1]))

    if both_images:
        import numpy as np
        A = np.asarray(a_img, dtype=np.int16)
        B = np.asarray(b_img, dtype=np.int16)
        H, W = A.shape[0], A.shape[1]
        d = np.abs(A - B)
        differing = np.any(d > 0, axis=-1)
        n_diff = int(differing.sum())
        pix = {
            "attempted": True, "width": W, "height": H,
            "pixel_identical": n_diff == 0,
            "differing_pixels": n_diff,
            "differing_fraction": n_diff / float(H * W),
        }
        if n_diff:
            # largest connected component, 8-connectivity: a blob painted the
            # wrong colour is one component however it wiggles; scattered
            # speckle stays scattered. scipy is in the pinned environment.
            from scipy import ndimage
            lab, n_comp = ndimage.label(
                differing, structure=np.ones((3, 3), dtype=np.int8))
            sizes = ndimage.sum_labels(
                np.ones_like(lab), lab, index=range(1, n_comp + 1))
            pix["components"] = int(n_comp)
            pix["largest_component_px"] = int(sizes.max())
            pix["largest_component_fraction_of_differing"] = (
                float(sizes.max()) / n_diff)
            # magnitude diagnostics: max-channel |delta| percentiles, and Lab
            # dE beside them. Diagnostics, not gates.
            mx = d.max(axis=-1)[differing].astype(np.float64)
            pix["abs_delta_maxchannel"] = {
                "p50": float(np.percentile(mx, 50)),
                "p95": float(np.percentile(mx, 95)),
                "max": float(mx.max())}

            def to_lab(rgb_u8):
                rgb = rgb_u8.astype(np.float64) / 255.0
                lin = np.where(rgb > 0.04045,
                               ((rgb + 0.055) / 1.055) ** 2.4, rgb / 12.92)
                M = np.array([[0.4124564, 0.3575761, 0.1804375],
                              [0.2126729, 0.7151522, 0.0721750],
                              [0.0193339, 0.1191920, 0.9503041]])
                xyz = lin @ M.T
                wn = np.array([0.95047, 1.0, 1.08883])
                t = xyz / wn
                f = np.where(t > (6 / 29) ** 3, np.cbrt(t),
                             t / (3 * (6 / 29) ** 2) + 4 / 29)
                L = 116 * f[:, 1] - 16
                a_ = 500 * (f[:, 0] - f[:, 1])
                b_ = 200 * (f[:, 1] - f[:, 2])
                return np.stack([L, a_, b_], axis=1)

            la = to_lab(A[differing][:, :3].astype(np.uint8))
            lb = to_lab(B[differing][:, :3].astype(np.uint8))
            de = np.sqrt(((la - lb) ** 2).sum(axis=1))
            pix["dE_lab"] = {"mean": float(de.mean()),
                             "p95": float(np.percentile(de, 95))}
        # the SHAPE, carried as a grid and never reduced: per-cell differing
        # fraction over an N x N partition. A structural difference
        # concentrates; a kernel difference spreads. The reader reads it.
        N = args.grid
        grid = []
        ys = np.linspace(0, H, N + 1).astype(int)
        xs = np.linspace(0, W, N + 1).astype(int)
        for i in range(N):
            row = []
            for j in range(N):
                cell = differing[ys[i]:ys[i + 1], xs[j]:xs[j + 1]]
                row.append(round(float(cell.mean()) if cell.size else 0.0, 6))
            grid.append(row)
        pix["shape_grid"] = grid
        pix["shape_grid_note"] = (
            "per-cell differing fractions, %d x %d - CARRIED, not reduced: "
            "a uniformity score would be an invented statistic (Ruling 10's "
            "bound), and the concentrated-vs-spread reading belongs to the "
            "reader" % (N, N))
    else:
        pix["not_attempted_because"] = (
            "one or both inputs do not decode as images; the byte tier is "
            "what exists for them")
    rec["pixel"] = pix

    print("[anchor] a %s  %s" % (rec["byte"]["a_sha256"][:16], args.a))
    print("[anchor] b %s  %s" % (rec["byte"]["b_sha256"][:16], args.b))
    print("[anchor] byte_identical %s" % rec["byte"]["byte_identical"])
    if pix.get("attempted"):
        print("[anchor] pixel_identical %s | differing %d (%.6f%%)"
              % (pix["pixel_identical"], pix["differing_pixels"],
                 100 * pix["differing_fraction"]))
        if pix.get("differing_pixels"):
            print("[anchor] largest component %d px (%.4f of differing) | "
                  "|d| p50 %.1f p95 %.1f max %.0f"
                  % (pix["largest_component_px"],
                     pix["largest_component_fraction_of_differing"],
                     pix["abs_delta_maxchannel"]["p50"],
                     pix["abs_delta_maxchannel"]["p95"],
                     pix["abs_delta_maxchannel"]["max"]))
    else:
        print("[anchor] pixel tier not attempted: %s"
              % pix["not_attempted_because"])

    if args.out:
        d0 = os.path.dirname(os.path.abspath(args.out))
        if d0 and not os.path.isdir(d0):
            os.makedirs(d0)
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1)
        print("[anchor] wrote %s" % os.path.abspath(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
