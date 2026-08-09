"""THE COLLAR-JUNCTION REPAIR - E14 Ruling 27c, run ONCE as handoff 8's step 0.

WHAT BROKE. The garnet re-projection rotated the drifted twins' stone paint by +34 to +55
degrees. The geometric stone mask's lower bound (z >= 0.4340) clips the bezel's lower arc
where the GOLD COLLAR's paint sits - the derivation's own section 6 rim finding, which read
twin 0's rim at hue 70.9 and named it the collar rather than lavender. Rotating gold by that
much lands it in the forbidden band 104-290, and it renders as a thin green line at the
collar junction in every view. The paint was CORRECT at stage 1b and its correct value is
KNOWN, so the repair is a restore, not a repaint.

THE PREDICATE IS GEOMETRY AND PROVENANCE, NEVER THE DEFECT'S OWN COLOUR. Selecting the
texels by "which ones are green now" would make the repair's success a tautology - the same
reasoning that made the demotion's mask an OWNERSHIP mask (Ruling 24f). Ruling 27c states the
predicate, and it is transcribed here BEFORE it was run, with one reading made explicit:

  territory                 the re-projection's own territory_mask.npy (67,904 texels)
  AND within 0.010 of       z <= Z_BOT + 0.010, Z_BOT re-derived by the demotion's own
  the stone mask's          landmark walk and asserted == 0.4340 (the same code, not a
  bottom edge               copied constant)
  AND stage-1b hue in       measured on state0/atlas.png, which IS the stage-1b atlas
  the gold band 42-104      (SHA asserted below)

THE READING MADE EXPLICIT: "hue in the gold band" carries the palette's chroma floor. The
route's own law is that below a chroma floor a hue is not a colour, and canon/E14-longsword-
palette.json defines its bands only above min_chroma 12.0 - so the gold band means the
palette's gold band, floor and all. The convention is palette_gate.py's exactly: C* > 12.0
strict, hue inclusive on both edges. This reading was fixed before the count was looked at;
the alternative (no floor) is not run and not compared, because choosing between them by
which one returns 1,086 would be tuning a mask against the number it is asserted to hit.

AMENDED 2026-08-08 at E14 RULING 28d, in place, with the reason. As first written this file
asserted 1,086 against the predicate above and HALTED at 1,431 - correctly: Ruling 27c had
attached an OUTCOME set's count to three DESCRIPTIVE legs, and a set's description is not its
generator. Read as a generator the legs admit 350 more (the shallow end of the same rotated
gold arc) and exclude 5 (sub-floor at stage 1b, so the gold leg cannot see them). Ruling 28d
rules the mask to be THE UNION of both clauses:

  clause P (the predicate)  territory AND z <= bottom+0.010 AND stage-1b gold above the floor
  clause O (the outcome)    territory AND forbidden AFTER the re-projection AND NOT before
  THE MASK = P OR O         1,431 + 5 disjoint = 1,436

Clause O is licensed as a LOCATED-DEFECT predicate on a known, deterministic prior state: the
tautology trap needs a selection tuned against results, and this set was fully determined by a
recorded operation before anyone looked at it. Its operand is the post-re-projection atlas,
supplied by --after; the tool additionally re-computes O on the LIVE atlas and asserts the two
agree, which proves in-tool - not in a report - that stroke 1 is orthogonal to this repair.

  ASSERT ALL THREE COUNTS: P = 1,431, O = 1,086, UNION = 1,436.
  Any other number is a HALT, not a tune (Ruling 28d; the assert stays absolute per 28b).

WHAT IT WRITES. Atlas colour only, restored from state0/. The holes and styled channels are
asserted BYTE-IDENTICAL after the write - this op is the demotion's mirror image, which
touched the state channels and asserted the atlas unchanged.

NAMED COMPENSATOR: the pre-repair RGB triplets and their flat indices are saved beside the
state as collar_repair_compensator.npz, and `--undo` restores them. It is exercised, not
declared - `--verify-undo` runs repair then undo on a scratch copy and asserts all three
state files come back byte-identical, before the real op is offered (the practice Ruling 24l
entered as the one to repeat).

  e14_repair_collar.py --state DIR --state0 DIR --prep DIR --territory MASK.npy --after ATLAS
                       [--undo] [--verify-undo] [--dry-run]

Standards compliance: PIN_PER_STEP - the mask is re-derived from named inputs, the landmark
is re-walked rather than pasted, state0's SHA is asserted against the works-perfectly gate's
recorded stage-1b hash, and both atlas SHAs are recorded. ANDON_AUTHORITY - the count assert
and every invariance raise before a byte is written, with no skip flag. NAMED_COMPENSATORS -
--undo, exercised by --verify-undo. EXTERNAL_VERIFIER - the band instruments
(e14_deep_share.py, palette_gate.py) read the result with code this file did not write.
"""
import argparse
import hashlib
import json
import os

import numpy as np
import trimesh
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
ap = argparse.ArgumentParser()
ap.add_argument("--state", required=True, help="the run state this op edits (the LIVE state)")
ap.add_argument("--state0", required=True, help="the pristine stage-1b state (the source of truth)")
ap.add_argument("--prep", required=True)
ap.add_argument("--territory", required=True, help="the re-projection's territory mask .npy")
ap.add_argument("--after", required=True,
                help="the POST-RE-PROJECTION atlas - clause O's 'forbidden after' operand. "
                     "Required rather than defaulted: the set is defined against a named "
                     "state, and letting it default would let a later state redefine it.")
ap.add_argument("--expect-p", type=int, default=1431, help="clause P's count (Ruling 28d)")
ap.add_argument("--expect-o", type=int, default=1086, help="clause O's count (Ruling 28d)")
ap.add_argument("--expect", type=int, default=1436, help="THE UNION's count (Ruling 28d)")
ap.add_argument("--stage1b-sha", default="69f61f32a3e2281aff653fb2",
                help="the works-perfectly gate's recorded stage-1b atlas SHA-256 prefix")
ap.add_argument("--undo", action="store_true", help="THE NAMED COMPENSATOR")
ap.add_argument("--verify-undo", action="store_true",
                help="exercise the compensator on a scratch copy before the real op")
ap.add_argument("--dry-run", action="store_true", help="derive and assert; write nothing")
args = ap.parse_args()
J = os.path.join

GOLD_LO, GOLD_HI = 42.0, 104.0          # canon/E14-longsword-palette.json, band "gold"
FORB_LO, FORB_HI = 104.0, 290.0         # the same file's forbidden span, clause O's band
CMIN = 12.0                             # the same file's min_chroma
Z_MARGIN = 0.010                        # Ruling 27c's "within 0.010 of the bottom edge"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def to_lab(rgb):
    """sRGB -> linear -> XYZ (D65) -> Lab. palette_gate.py's transform, unmodified."""
    c = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    e, k = 216 / 24389, 24389 / 27
    fx = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    return np.stack([116 * fx[..., 1] - 16,
                     500 * (fx[..., 0] - fx[..., 1]),
                     200 * (fx[..., 1] - fx[..., 2])], axis=-1)


# ---------------- the mask, re-derived: geometry AND stage-1b provenance ----------------
a0p = J(args.state0, "atlas.png")
sha_a0 = sha(a0p)
if not (sha_a0.startswith(args.stage1b_sha)):
    raise AssertionError(
        f"ANDON: --state0's atlas is {sha_a0[:24]}, not the recorded stage-1b atlas "
        f"{args.stage1b_sha}. The source of the restored values is not the paint the ruling "
        f"calls correct. HALT.")

meta = json.load(open(J(args.prep, "meta.json"), encoding="utf-8"))
mask2d = np.load(J(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask2d.reshape(-1)
vidx = np.where(valid)[0]
lo, hi = np.array(meta["lo"]), np.array(meta["hi"])
P = (np.load(J(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5

terr_v = np.load(args.territory)
if not (terr_v.shape == vidx.shape):
    raise AssertionError(f"ANDON: territory is {terr_v.shape}, valid is {vidx.shape}")

# the landmark, RE-WALKED by the demotion's own code rather than pasted as a constant
m = trimesh.load(J(args.prep, "prep_uv.glb"), force="mesh", process=False)
vv = np.asarray(m.vertices, dtype=np.float64)
vv = np.stack([vv[:, 0], -vv[:, 2], vv[:, 1]], axis=1) / np.abs(vv).max() * 0.5
ztop = vv[:, 2].max()
zs, exts, z = [], [], ztop
while z > ztop - 0.13:
    s = (vv[:, 2] <= z) & (vv[:, 2] > z - 0.004)
    zs.append(z - 0.002)
    exts.append(float(vv[s, 0].max() - vv[s, 0].min()) if s.sum() > 3 else 0.0)
    z -= 0.004
zs, exts = np.array(zs), np.array(exts)
pk = int(np.argmax(exts[:16])); i = pk + 1
while i + 1 < len(exts) and exts[i + 1] <= exts[i]:
    i += 1
Z_BOT = zs[i]
if not (abs(Z_BOT - 0.4340) < 1e-6):
    raise AssertionError(f"ANDON: the stone landmark reads {Z_BOT}, not 0.4340")

def lch_of(path):
    a = np.asarray(Image.open(path).convert("RGB"), dtype=np.float64) / 255.0
    lab = to_lab(a.reshape(-1, 3)[vidx])
    return (np.hypot(lab[:, 1], lab[:, 2]),
            np.degrees(np.arctan2(lab[:, 2], lab[:, 1])) % 360.0)


C0, H0 = lch_of(a0p)                      # stage 1b - clause P's provenance, clause O's BEFORE
C1, H1 = lch_of(args.after)               # post re-projection - clause O's AFTER
CL, HL = lch_of(J(args.state, "atlas.png"))   # the LIVE state, for the orthogonality check

leg_terr = terr_v
leg_edge = P[:, 2] <= Z_BOT + Z_MARGIN
leg_gold = (C0 > CMIN) & (H0 >= GOLD_LO) & (H0 <= GOLD_HI)


def forbidden(C, H):
    return (C > CMIN) & (H >= FORB_LO) & (H <= FORB_HI)


clause_p = leg_terr & leg_edge & leg_gold
clause_o = leg_terr & forbidden(C1, H1) & ~forbidden(C0, H0)
union = clause_p | clause_o
NP, NO, N = int(clause_p.sum()), int(clause_o.sum()), int(union.sum())
only_o = clause_o & ~clause_p
flat = vidx[union]

print(f"[repair] landmark re-walked: the stone's bottom edge z = {Z_BOT:.4f} (asserted)")
print(f"[repair] legs, each on the {len(vidx):,} valid texels:")
print(f"[repair]   territory                        {int(leg_terr.sum()):,}")
print(f"[repair]   z <= {Z_BOT:.4f} + {Z_MARGIN}                {int(leg_edge.sum()):,}")
print(f"[repair]   stage-1b gold {GOLD_LO:g}-{GOLD_HI:g} above C* {CMIN:g}     {int(leg_gold.sum()):,}")
print(f"[repair]   territory AND edge                {int((leg_terr & leg_edge).sum()):,}")
print(f"[repair] CLAUSE P  territory AND edge AND stage-1b gold      {NP:,}")
print(f"[repair] CLAUSE O  territory AND forbidden-after AND NOT before  {NO:,}")
print(f"[repair]   of clause O, outside clause P                     {int(only_o.sum()):,}")
print(f"[repair] THE RULED MASK  P OR O                              {N:,}")
for got, want, nm in ((NP, args.expect_p, "clause P"), (NO, args.expect_o, "clause O"),
                      (N, args.expect, "the union")):
    if not (got == want):
        raise AssertionError(
            f"ANDON: {nm} yields {got:,} texels, but Ruling 28d names {want:,}. The mask this op "
            f"would edit is not the mask the ruling adopted. A different count is a HALT, not a "
            f"tune. HALT.")
if not (N == NP + int(only_o.sum())):
    raise AssertionError("ANDON: the union is not P plus the O-only remainder")
print(f"[repair] ASSERTED against Ruling 28d: P {args.expect_p:,} / O {args.expect_o:,} / "
      f"union {args.expect:,}; the {int(only_o.sum())} O-only texels are disjoint from P")

# ORTHOGONALITY, asserted in the tool rather than claimed in a report: clause O re-computed
# on the LIVE atlas must give the SAME set. If a stroke had touched this territory the two
# would differ, and the repair would be editing paint that a commit had already banked.
clause_o_live = leg_terr & forbidden(CL, HL) & ~forbidden(C0, H0)
if not (np.array_equal(clause_o, clause_o_live)):
    raise AssertionError(
        "ANDON: clause O computed on the LIVE atlas differs from clause O on the "
        "post-re-projection atlas - a stroke has touched the repair territory. HALT.")
print(f"[repair] ASSERTED: clause O is identical on the LIVE atlas - no committed stroke "
      f"touches this repair's texels")
print(f"[repair] the union's stage-1b hue: median {np.median(H0[union]):.1f}  "
      f"C* median {np.median(C0[union]):.1f}   "
      f"z range {P[union, 2].min():.4f}-{P[union, 2].max():.4f}")


def apply_repair(state, tag="repair"):
    ap_, hp, sp = (J(state, "atlas.png"), J(state, "holes.png"), J(state, "styled_mask.npy"))
    sha_a_before, sha_h_before, sha_s_before = sha(ap_), sha(hp), sha(sp)
    atlas = np.array(Image.open(ap_).convert("RGB"))
    a_f = atlas.reshape(-1, 3)
    pre = a_f.copy()
    src = np.array(Image.open(a0p).convert("RGB")).reshape(-1, 3)
    # THE COMPENSATOR, saved BEFORE the write it inverts
    np.savez_compressed(J(state, "collar_repair_compensator.npz"),
                        flat=flat, rgb_pre=pre[flat])
    a_f[flat] = src[flat]
    # the op's own invariance: colour changed ONLY inside the mask
    ch = np.where((pre != a_f).any(axis=1))[0]
    if not (set(ch.tolist()).issubset(set(flat.tolist()))):
        raise AssertionError("ANDON: the atlas changed colour outside the ruled mask")
    outside = np.ones(len(a_f), dtype=bool)
    outside[flat] = False
    if not (np.array_equal(a_f[outside], pre[outside])):
        raise AssertionError("ANDON: a texel outside the ruled mask changed colour")
    Image.fromarray(atlas).save(ap_)
    sha_a_after, sha_h_after, sha_s_after = sha(ap_), sha(hp), sha(sp)
    # the mirror of the demotion's check: the STATE channels must not move
    if not (sha_h_before == sha_h_after):
        raise AssertionError("ANDON: holes.png changed during a colour-only op")
    if not (sha_s_before == sha_s_after):
        raise AssertionError("ANDON: styled_mask.npy changed during a colour-only op")
    dE = np.abs(pre[flat].astype(np.float64) - a_f[flat].astype(np.float64)).max(axis=1)
    print(f"[{tag}] restored {N:,} texels' atlas colour from {os.path.abspath(args.state0)}")
    print(f"[{tag}] of those, actually differing before the write: {len(ch):,} "
          f"(the rest were already at their stage-1b value)")
    print(f"[{tag}] |delta| per texel, 8-bit: median {np.median(dE):.0f}  max {dE.max():.0f}")
    print(f"[{tag}] ASSERTED: colour changed inside the ruled mask ONLY; "
          f"holes.png and styled_mask.npy BYTE-IDENTICAL (a colour-only operation)")
    print(f"[{tag}] atlas sha256  {sha_a_before[:24]}  ->  {sha_a_after[:24]}")
    return {"op": tag, "ruling": "E14 Ruling 28d", "mask_texels": N,
            "clause_P": NP, "clause_O": NO, "O_only": int(only_o.sum()),
            "predicate": {"territory": os.path.abspath(args.territory),
                          "z_bottom": float(Z_BOT), "z_margin": Z_MARGIN,
                          "gold_band": [GOLD_LO, GOLD_HI],
                          "forbidden_band": [FORB_LO, FORB_HI], "chroma_floor": CMIN,
                          "before_state": "state0/atlas.png (the stage-1b atlas)",
                          "after_state": os.path.abspath(args.after),
                          "clause_O_identical_on_live": True},
            "legs": {"territory": int(leg_terr.sum()), "edge": int(leg_edge.sum()),
                     "gold_at_1b": int(leg_gold.sum()),
                     "territory_and_edge": int((leg_terr & leg_edge).sum())},
            "texels_actually_changed": int(len(ch)),
            "delta_median_8bit": float(np.median(dE)), "delta_max_8bit": float(dE.max()),
            "state0_atlas_sha256": sha_a0,
            "atlas_sha256_before": sha_a_before, "atlas_sha256_after": sha_a_after,
            "holes_sha256": sha_h_before, "styled_sha256": sha_s_before,
            "holes_styled_byte_identical": True,
            "compensator": "e14_repair_collar.py --undo (restores the pre-repair RGB from "
                           "collar_repair_compensator.npz); deterministic inverse, "
                           "exercised by --verify-undo"}


def apply_undo(state):
    """THE NAMED COMPENSATOR. Restores the pre-repair colour saved by the op itself."""
    cj = J(state, "collar_repair_compensator.npz")
    if not (os.path.exists(cj)):
        raise AssertionError(f"ANDON: no compensator at {cj}; there is nothing to undo")
    z = np.load(cj)
    f0, rgb0 = z["flat"], z["rgb_pre"]
    if not (np.array_equal(np.sort(f0), np.sort(flat))):
        raise AssertionError(
            "ANDON: the saved compensator's texels are not the mask this run re-derived")
    ap_ = J(state, "atlas.png")
    atlas = np.array(Image.open(ap_).convert("RGB"))
    atlas.reshape(-1, 3)[f0] = rgb0
    Image.fromarray(atlas).save(ap_)
    print(f"[undo] restored {len(f0):,} texels' pre-repair colour from {os.path.basename(cj)}")
    return {"op": "undo", "mask_texels": int(len(f0)), "atlas_sha256_after": sha(ap_)}


if args.dry_run:
    print("[repair] --dry-run: the mask is derived and asserted; nothing written")
    raise SystemExit(0)

if args.verify_undo:
    import shutil
    scratch = args.state + "__repaircheck"
    os.makedirs(scratch, exist_ok=True)
    for f in ("atlas.png", "holes.png", "styled_mask.npy"):
        shutil.copy(J(args.state, f), J(scratch, f))
    h0 = {f: sha(J(scratch, f)) for f in ("atlas.png", "holes.png", "styled_mask.npy")}
    apply_repair(scratch, tag="repair-scratch")
    apply_undo(scratch)
    h1 = {f: sha(J(scratch, f)) for f in ("atlas.png", "holes.png", "styled_mask.npy")}
    bad = [f for f in h0 if h0[f] != h1[f]]
    if bad:
        raise AssertionError(f"ANDON: the compensator did not restore {bad} byte-identically")
    print("[verify-undo] PASS - repair then undo returns all three state files "
          "BYTE-IDENTICAL. The compensator is exercised, not merely declared.")
elif args.undo:
    rep = apply_undo(args.state)
    json.dump(rep, open(J(args.state, "collar_repair_undo.json"), "w"), indent=1)
else:
    rep = apply_repair(args.state)
    json.dump(rep, open(J(args.state, "collar_repair.json"), "w"), indent=1)
    print(f"[repair] wrote {J(args.state, 'collar_repair.json')}")
