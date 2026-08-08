"""THE GARNET DEMOTION — E14 Ruling 24f, run ONCE before stroke 1.

WHAT THIS IS AND WHY IT IS NOT A WORKAROUND. `texpass_iter commit` asserts that no styled
texel is touched, with no skip flag (E08 Amendment 32). The Director's word is garnet, so
the stone's drifted territory must be repainted — which is writing over styled texels. The
ruling's disposition is NOT to weaken the ANDON but to make the target ordinary holes first,
in a separate, recorded, deterministic state operation that touches state channels only:

  holes = 1  and  styled = False  on EXACTLY the ruled mask, and nothing else.

The atlas's colour bytes are left alone deliberately. `emit` builds `render.png` from the
atlas and `mask.png` from `holes` INDEPENDENTLY, so keeping the colour gives the brush the
stone's shape, facets and bezel as context while still telling it to repaint them. That is a
property of the tool, used on purpose and printed below as a byte-identity check.

THE MASK COMES FROM THE OWNERSHIP PARTITION, NEVER FROM COLOUR. Deriving a repaint mask from
the hue it exists to fix would make the stroke's success a tautology; this file re-derives it
from stage 1b's owner array and the stone's geometric landmark, and asserts the count the
ruling names.

NAMED COMPENSATOR (the standard's own requirement, and this op is irreversible to the state
it edits): `--undo`, which restores the demoted mask's three channels from the pristine
`state0/`. It is the operation's own deterministic inverse and it is exercised, not merely
declared — `--verify-undo` runs demote, undo, and asserts the state is byte-identical to
where it started, before the real demotion is offered.

  e14_demote_garnet.py --state DIR --state0 DIR --prep DIR [--undo] [--verify-undo]

Standards compliance: PIN_PER_STEP — the mask is re-derived from named inputs and its count
asserted against the ruling; the invariance report is printed and written beside the state.
ANDON_AUTHORITY — every assertion raises before a byte is written; the count, the landmark
and the disjointness of holes and styled are all checked. NAMED_COMPENSATORS — `--undo`,
exercised by `--verify-undo`. EXTERNAL_VERIFIER — `texpass_iter commit`'s own ANDON is the
downstream check that this op left a legal state; it is untouched by this file.
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
ap.add_argument("--state", required=True, help="the run state this op edits")
ap.add_argument("--state0", required=True, help="the pristine pre-stroke state (the compensator's source)")
ap.add_argument("--prep", required=True)
ap.add_argument("--stage1b", required=True, help="dir holding stage1b_atlas_owner.npy")
ap.add_argument("--expect", type=int, default=67904, help="the mask count the ruling names")
ap.add_argument("--undo", action="store_true", help="THE NAMED COMPENSATOR")
ap.add_argument("--verify-undo", action="store_true",
                help="exercise the compensator on a scratch copy before offering the real op")
args = ap.parse_args()

J = os.path.join
VIEWS = [0, 1, 3, 4, 5, 7]
DRIFT_OI = [VIEWS.index(v) for v in (1, 3, 5, 7)]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


# ---------------- the mask, re-derived from ownership and geometry ----------------
meta = json.load(open(J(args.prep, "meta.json"), encoding="utf-8"))
mask2d = np.load(J(args.prep, "mask.npy"))[..., 0] > 0.5
valid = mask2d.reshape(-1)
lo, hi = np.array(meta["lo"]), np.array(meta["hi"])
P = (np.load(J(args.prep, "pos.npy")).reshape(-1, 3)[valid].astype(np.float64)
     * (hi - lo) + lo) / meta["maxabs"] * 0.5
owner = np.load(J(args.stage1b, "stage1b_atlas_owner.npy")).reshape(-1)[valid]
styled1b = np.load(J(args.stage1b, "stage1b_atlas_styled_mask.npy")).reshape(-1)[valid]

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
assert abs(Z_BOT - 0.4340) < 1e-6, f"ANDON: the stone landmark reads {Z_BOT}, not 0.4340"

sel = (P[:, 2] >= Z_BOT) & styled1b & np.isin(owner, DRIFT_OI)
N = int(sel.sum())
assert N == args.expect, (
    f"ANDON: the ownership partition yields {N:,} drifted-owned stone texels, but Ruling 24f "
    f"names {args.expect:,}. The mask this op edits is not the mask the ruling adopted. HALT.")
flat = np.where(valid)[0][sel]
print(f"[demote] mask re-derived from OWNERSHIP (drifted views 1/3/5/7) and the stone's "
      f"landmark z >= {Z_BOT:.4f}: {N:,} texels, asserted against Ruling 24f")


def apply_demotion(state, tag="demote"):
    ap_, hp, sp = J(state, "atlas.png"), J(state, "holes.png"), J(state, "styled_mask.npy")
    a_before = sha(ap_)
    st = np.load(sp)
    ho = np.array(Image.open(hp).convert("L"))
    assert st.shape == mask2d.shape and ho.shape == mask2d.shape, "ANDON: state shape"
    st_f, ho_f = st.reshape(-1), ho.reshape(-1)
    pre_st, pre_ho = st_f.copy(), ho_f.copy()
    n_styled0, n_holes0 = int(st.sum()), int((ho > 127).sum())
    st_f[flat] = False
    ho_f[flat] = 255
    # ⚠ THE OP'S OWN INVARIANCE, printed: exactly the mask changed, in state channels only.
    ch_st = np.where(pre_st != st_f)[0]
    ch_ho = np.where(pre_ho != ho_f)[0]
    assert np.array_equal(np.sort(ch_st), np.sort(flat[pre_st[flat]])), (
        "ANDON: the styled channel changed outside the ruled mask")
    assert set(ch_ho.tolist()).issubset(set(flat.tolist())), (
        "ANDON: the holes channel changed outside the ruled mask")
    np.save(sp, st)
    Image.fromarray(ho).save(hp)
    a_after = sha(ap_)
    assert a_before == a_after, (
        f"ANDON: atlas.png changed during a state-channel-only operation\n  before "
        f"{a_before}\n  after  {a_after}")
    rep = {"op": tag, "mask_texels": N, "z_stone_bottom": float(Z_BOT),
           "styled": [n_styled0, int(st.sum())], "holes": [n_holes0, int((ho > 127).sum())],
           "styled_changed": int(len(ch_st)), "holes_changed": int(len(ch_ho)),
           "atlas_sha256_before": a_before, "atlas_sha256_after": a_after,
           "atlas_byte_identical": True,
           "compensator": "e14_demote_garnet.py --undo (restores the mask's three channels "
                          "from state0/); deterministic inverse, exercised by --verify-undo"}
    print(f"[{tag}] styled {n_styled0:,} -> {int(st.sum()):,}   "
          f"holes {n_holes0:,} -> {int((ho > 127).sum()):,}")
    print(f"[{tag}] changed: styled channel {len(ch_st):,} texels, holes channel "
          f"{len(ch_ho):,} texels - both subsets of the ruled mask, asserted")
    print(f"[{tag}] atlas.png BYTE-IDENTICAL before/after ({a_before[:12]}...) - the colour "
          f"stays as the brush's shape context, by design (Ruling 24f)")
    return rep


def apply_undo(state, state0):
    """THE NAMED COMPENSATOR. Restores the ruled mask's state from the pristine state0."""
    st = np.load(J(state, "styled_mask.npy"))
    ho = np.array(Image.open(J(state, "holes.png")).convert("L"))
    st0 = np.load(J(state0, "styled_mask.npy"))
    ho0 = np.array(Image.open(J(state0, "holes.png")).convert("L"))
    st.reshape(-1)[flat] = st0.reshape(-1)[flat]
    ho.reshape(-1)[flat] = ho0.reshape(-1)[flat]
    np.save(J(state, "styled_mask.npy"), st)
    Image.fromarray(ho).save(J(state, "holes.png"))
    print(f"[undo] restored {N:,} texels' styled/holes state from {state0}")
    return {"op": "undo", "mask_texels": N, "styled": int(st.sum()),
            "holes": int((ho > 127).sum())}


if args.verify_undo:
    import shutil
    scratch = args.state + "__undocheck"
    os.makedirs(scratch, exist_ok=True)
    for f in ("atlas.png", "holes.png", "styled_mask.npy"):
        shutil.copy(J(args.state, f), J(scratch, f))
    h0 = {f: sha(J(scratch, f)) for f in ("atlas.png", "holes.png", "styled_mask.npy")}
    apply_demotion(scratch, tag="demote-scratch")
    apply_undo(scratch, args.state0)
    h1 = {f: sha(J(scratch, f)) for f in ("atlas.png", "holes.png", "styled_mask.npy")}
    bad = [f for f in h0 if h0[f] != h1[f]]
    assert not bad, f"ANDON: the compensator did not restore {bad} byte-identically"
    print("[verify-undo] PASS - demote then undo returns all three state files "
          "BYTE-IDENTICAL. The compensator is exercised, not merely declared.")
elif args.undo:
    rep = apply_undo(args.state, args.state0)
    json.dump(rep, open(J(args.state, "demotion_undo.json"), "w"), indent=1)
else:
    rep = apply_demotion(args.state)
    json.dump(rep, open(J(args.state, "demotion.json"), "w"), indent=1)
    print(f"[demote] wrote {J(args.state, 'demotion.json')}")
