"""Per-stroke claim replay, faithful to texpass_iter.commit AS SHIPPED (with E08
Amendment 32's hit-intersect) — because texel_provenance.py's replay predates A32.

Measured trigger for this file's existence (2026-08-05, the Ruling 4 dispatch):
texel_provenance's replay over-claims the ship's six strokes by +6/+118/+148/+25/+5/+56
(total +358) against out/provenance.json — exactly the signature of a missing
`fm_e & hit` intersect, since every extra texel it claims is one commit refused as
"keyed on no surface". This replica adds that one step, byte-faithful to
texpass_iter.py lines 363-390: corner-median key -> minimum_filter(5) -> AND hit.png
-> distance transform -> edge >= edge-dist, after facing/visibility/job-mask, in
stroke order over the saved job directories.

The anchor decides whether this replica is believed: all six per-stroke counts must
equal provenance.json's exactly. Anything else is reported, not tuned.

Writes claim.npy into --out-dir (never into the shipped state).

  e10_claim_replay.py --out-dir DIR
"""
import argparse
import json
import os

import numpy as np
import open3d as o3d
import trimesh
from PIL import Image
from scipy.ndimage import distance_transform_edt, minimum_filter

Image.MAX_IMAGE_PIXELS = None
PREP = r"E:\AI\training\facet_next\E04_shipprep"
STROKE = r"E:\AI\training\facet_next\E04_stroke"
STAGE1 = r"E:\AI\training\facet_next\E04_armT72\stage1"
ORDER = ["y+300_e+00", "y+030_e+00", "y+150_e+00", "y+240_e+00",
         "y+000_e+40", "y+180_e+40"]
RECORDED = {"y+300_e+00": 26531, "y+030_e+00": 22766, "y+150_e+00": 17904,
            "y+240_e+00": 24486, "y+000_e+40": 63288, "y+180_e+40": 58877}
FACING_MIN, EDGE_DIST, BIAS, NOFFS = 0.25, 4.0, 3e-3, 1.5e-3  # ship.json texpass_iter


def basis(yaw_d, el_d):
    th, el = np.radians(yaw_d), np.radians(el_d)
    cd = np.array([np.sin(th) * np.cos(el), -np.cos(th) * np.cos(el), np.sin(el)])
    look = -cd / np.linalg.norm(cd)
    right = np.cross(look, [0.0, 0.0, 1.0])
    right /= np.linalg.norm(right) + 1e-12
    up = np.cross(right, look)
    return look, right, up / (np.linalg.norm(up) + 1e-12)


def bilin(img, x, y):
    Hh, Ww = img.shape[:2]
    x = np.clip(x, 0.0, Ww - 1.001)
    y = np.clip(y, 0.0, Hh - 1.001)
    x0, y0 = x.astype(np.int64), y.astype(np.int64)
    fx, fy = x - x0, y - y0
    if img.ndim == 3:
        fx, fy = fx[:, None], fy[:, None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    J = os.path.join

    meta = json.load(open(J(PREP, "meta.json"), encoding="utf-8"))
    RES = meta["res"]
    valid = np.load(J(PREP, "mask.npy"))[..., 0] > 0.5
    holes = np.asarray(Image.open(J(STAGE1, "stage1_8cam_holes.png")).convert("L"),
                       dtype=np.float32) / 255 > 0.5
    styled0 = np.load(J(STAGE1, "stage1_8cam_styled_mask.npy"))
    pos_e = np.load(J(PREP, "pos.npy"), mmap_mode="r")
    nor_e = np.load(J(PREP, "nor.npy"), mmap_mode="r")
    lo = np.array(meta["lo"])
    hi = np.array(meta["hi"])

    m = trimesh.load(J(PREP, "prep_uv.glb"), force="mesh", process=False)
    v = np.asarray(m.vertices, dtype=np.float64)
    f = np.asarray(m.faces, dtype=np.int64)
    v = np.stack([v[:, 0], -v[:, 2], v[:, 1]], axis=1) / np.abs(v).max() * 0.5
    rs = o3d.t.geometry.RaycastingScene()
    rs.add_triangles(o3d.core.Tensor(v.astype(np.float32)),
                     o3d.core.Tensor(f.astype(np.uint32)))

    claim = np.full(RES * RES, 255, dtype=np.uint8)
    claim[np.where(styled0.reshape(-1))[0]] = 0
    h = holes.reshape(-1).copy()
    vf = valid.reshape(-1)
    print(f"[replay2] {len(ORDER)} commits from stage-1 holes {int((h & vf).sum()):,}, "
          f"WITH the A32 hit-intersect", flush=True)

    all_ok = True
    for si, keyname in enumerate(ORDER, start=1):
        Jd = J(STROKE, "state", "job_" + keyname)
        cam = json.load(open(J(Jd, "cam.json")))
        edited = np.asarray(Image.open(J(Jd, "inpainted.png")).convert("RGB"),
                            dtype=np.float32) / 255
        jobmask = np.asarray(Image.open(J(Jd, "mask.png")).convert("L"),
                             dtype=np.float32) / 255
        hitm = (np.asarray(Image.open(J(Jd, "hit.png")).convert("L"),
                           dtype=np.float32) / 255.0) > 0.5

        hidx = np.where(h & vf)[0]
        P = (np.asarray(pos_e.reshape(-1, 3)[hidx], dtype=np.float64)
             * (hi - lo) + lo) / meta["maxabs"] * 0.5
        N = np.asarray(nor_e.reshape(-1, 3)[hidx], dtype=np.float64) * 2.0 - 1.0
        N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
        look, right, up = basis(cam["yaw"], cam["el"])
        dtc = -look
        keep = (N @ dtc) > FACING_MIN
        hidx, P, N = hidx[keep], P[keep], N[keep]
        org = (P + N * NOFFS + dtc[None, :] * BIAS).astype(np.float32)
        t = rs.cast_rays(o3d.core.Tensor(np.concatenate(
            [org, np.broadcast_to(dtc.astype(np.float32), org.shape)],
            axis=1)))["t_hit"].numpy()
        vis = ~np.isfinite(t)
        hidx, P = hidx[vis], P[vis]
        bmid = np.array(cam["bmid"])
        px = ((P - bmid) @ right / cam["h_ext"] + 0.5) * cam["W"] - 0.5
        py = (0.5 - (P - bmid) @ up / cam["v_ext"]) * cam["H"] - 0.5
        inj = bilin(jobmask, px, py) > 0.5
        hidx, px, py = hidx[inj], px[inj], py[inj]

        c8 = np.concatenate([edited[:8, :8].reshape(-1, 3), edited[:8, -8:].reshape(-1, 3)])
        bg = np.median(c8, axis=0)
        fm_e = minimum_filter(
            (np.abs(edited - bg).max(axis=-1) > 0.06).astype(np.float32), size=5)
        fm_e = ((fm_e > 0.5) & hitm).astype(np.float32)     # THE A32 STEP
        dist_e = distance_transform_edt(fm_e > 0.5).astype(np.float32)
        ok = bilin(dist_e, px, py) >= EDGE_DIST
        hidx = hidx[ok]
        claim[hidx] = si
        h[hidx] = False
        rec = RECORDED[keyname]
        mark = "OK" if len(hidx) == rec else f"MISMATCH ({len(hidx)-rec:+,})"
        all_ok &= (len(hidx) == rec)
        print(f"[replay2] stroke {si} {keyname}: claimed {len(hidx):,}  "
              f"(recorded {rec:,})  {mark}", flush=True)

    os.makedirs(args.out_dir, exist_ok=True)
    out = J(args.out_dir, "claim.npy")
    np.save(out, claim.reshape(RES, RES))
    print(f"[replay2] wrote {out}")
    print(f"[replay2] ANCHOR: {'ALL SIX EXACT' if all_ok else 'NOT ANCHORED'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
