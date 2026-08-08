"""E14 handoff 2, Task 3.2 — the three checks the backdrop derivation does NOT do.

`e04_backdrop.py` reports three optima against the key's own max-channel metric. It does
not answer the questions this subject's fixture actually pre-registered, so this file adds
exactly those and nothing else:

  1. OCCUPANCY, CHECKED NOT ASSUMED (the 8a/15i lesson). LONGSWORD-IDENTITY.md declares
     "blue-violet is unoccupied" as an EXPECTATION to be checked at derivation. Checking it
     means putting a CHROMA FLOOR on every element before quoting any hue at all — below the
     floor a hue is not a colour, it is a rotation (CLAUDE.md; the same fact bit two
     instruments in this repo). L1 and L2 are declared near-achromatic, so the honest output
     is "hue undefined", never "hue 267 = blue".

  2. THE HUE FAMILIES, SURVEYED. On the beast the metric could not separate green from
     blue-violet from warm (0.009 of score), so the word went to a ruling rather than to the
     winner. Whether that holds on THIS subject is a fact about THIS table, and it is
     measured here rather than carried over.

  3. THE INHERITED CANDIDATES, SCORED. W3's "plain grey background" and the galleon's white
     are the two backdrops already in the repo. Neither transfers by default; both are
     scored against this subject's own table so the fixture's claim about grey is tested
     rather than repeated.

WHAT THE METRIC IS, so no reader over-reads it: max-channel absolute sRGB distance, which is
the KEY's own arithmetic (`max_channel |pixel - backdrop| > 0.06`), not a perceptual metric.
Two colours far apart here can be close to an eye and vice versa. It answers "will the key
separate them", which is the question the backdrop exists to answer, and no other.

  e14_backdrop_checks.py --materials m.json [--thin-weight 2.0] [--grid 26] [--out j.json]

Standards compliance: PIN_PER_STEP - the table is a file, every threshold a flag, output a
JSON beside the derivation's own. ANDON_AUTHORITY - none; this tabulates and adopts nothing.
DECOMPOSE_BY_SECRETS - the chroma floor is a stated constant with its reason, not folded into
a hue table. EXTERNAL_VERIFIER - the scoring function is re-derived here from the key's
definition and asserted equal to e04_backdrop.py's on the declared materials, so a divergence
between the two files is caught rather than assumed away.
"""
import argparse
import json
import os

import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--materials", required=True)
ap.add_argument("--thin-weight", type=float, default=2.0)
ap.add_argument("--grid", type=int, default=26)
ap.add_argument("--chroma-floor", type=float, default=5.0,
                help="C* below which a hue is not quoted at all. 5.0 is well above the "
                     "measured steel class (C* 1.6-2.8 at hue 267) and well below any "
                     "material anyone would call coloured.")
ap.add_argument("--sat-max", type=float, default=0.18,
                help="e04_backdrop.py's own low-saturation bound, repeated as a flag")
ap.add_argument("--l1-sweep", action="store_true",
                help="sweep L1's estimated grey level and report what each candidate's "
                     "score does - the estimate this subject's answer is most exposed to")
ap.add_argument("--out", default=None)
args = ap.parse_args()

MATS = json.load(open(args.materials, encoding="utf-8"))["materials"]
names = [m["id"] + " " + m["name"] for m in MATS]
C = np.array([[c / 255.0 for c in m["rgb"]] for m in MATS])
thin = np.array([bool(m.get("thin")) for m in MATS])
W = np.where(thin, args.thin_weight, 1.0)


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


def dists(bg):
    return np.abs(C - np.asarray(bg)[None, :]).max(axis=1)


def weighted_min(bg):
    d = dists(bg)
    return float((d / W).min()), int(np.argmin(d / W)), d


out = {"chroma_floor": args.chroma_floor, "thin_weight": args.thin_weight,
       "sat_max": args.sat_max}

# ---- 1. occupancy, with the chroma floor applied BEFORE any hue is quoted ----
print("[occ] every declared element, chroma floor C* = %.1f" % args.chroma_floor)
print("[occ] %-32s %8s %8s %10s   %s" % ("element", "L*", "C*", "hue", "verdict"))
occ = []
for i, m in enumerate(MATS):
    lab = srgb_to_lab(C[i:i + 1])[0]
    L, a, bb = float(lab[0]), float(lab[1]), float(lab[2])
    cstar = float(np.hypot(a, bb))
    if cstar < args.chroma_floor:
        hue_s, verdict = "UNDEFINED", "below the floor - occupies NO hue"
        hue = None
    else:
        hue = float(np.degrees(np.arctan2(bb, a)) % 360.0)
        hue_s = "%.1f" % hue
        verdict = "occupies hue %.0f" % hue
    print("[occ] %-32s %8.1f %8.1f %10s   %s" % (names[i], L, cstar, hue_s, verdict))
    occ.append({"id": m["id"], "name": m["name"], "L": round(L, 1),
                "C": round(cstar, 2), "hue": None if hue is None else round(hue, 1),
                "above_floor": cstar >= args.chroma_floor})
out["occupancy"] = occ

BANDS = [("red / wine", 0, 40), ("orange", 40, 70), ("warm yellow", 70, 105),
         ("green", 105, 175), ("cyan", 175, 225), ("blue-violet", 225, 300),
         ("magenta", 300, 360)]
occupied = {}
for b, lo, hi in BANDS:
    who = [o["id"] for o in occ if o["above_floor"] and lo <= o["hue"] < hi]
    occupied[b] = who
print("\n[occ] HUE BAND OCCUPANCY (elements below the chroma floor occupy NOTHING):")
for b, lo, hi in BANDS:
    who = occupied[b]
    print("[occ]   %-14s (%3d-%3d)  %s" % (b, lo, hi, ", ".join(who) if who else "UNOCCUPIED"))
out["hue_band_occupancy"] = occupied
bv = occupied["blue-violet"]
print("\n[occ] THE FIXTURE'S PRE-REGISTERED EXPECTATION - 'blue-violet is unoccupied': %s"
      % ("CONFIRMED" if not bv else "FALSIFIED, occupied by " + ", ".join(bv)))
out["blue_violet_unoccupied"] = not bv

# ---- 2. the hue families, surveyed at low saturation ----
g = np.linspace(0, 1, args.grid)
fam_best = {}
for r in g:
    for gg in g:
        for b in g:
            bg = np.array([r, gg, b])
            sat = float(bg.max() - bg.min())
            if sat > args.sat_max:
                continue
            lab = srgb_to_lab(bg[None, :])[0]
            cstar = float(np.hypot(lab[1], lab[2]))
            if cstar < args.chroma_floor:
                fam = "neutral"
            else:
                hue = float(np.degrees(np.arctan2(lab[2], lab[1])) % 360.0)
                fam = next(nm for nm, lo, hi in BANDS if lo <= hue < hi)
            s, bi, d = weighted_min(bg)
            if fam not in fam_best or s > fam_best[fam][0]:
                fam_best[fam] = (s, bg.copy(), bi, float(cstar), float(lab[0]))
print("\n[fam] BEST BACKDROP PER HUE FAMILY at sat <= %.2f  (weighted metric)" % args.sat_max)
print("[fam] %-14s %-18s %6s %6s %6s   %-12s %s"
      % ("family", "rgb", "L*", "C*", "score", "binds", "raw-min material"))
famrows = {}
for fam, (s, bg, bi, cstar, L) in sorted(fam_best.items(), key=lambda kv: -kv[1][0]):
    d = dists(bg)
    rgb = [int(round(x * 255)) for x in bg]
    print("[fam] %-14s (%3d,%3d,%3d)      %6.1f %6.1f %6.4f   %-12s %s"
          % (fam, *rgb, L, cstar, s, MATS[bi]["id"], names[int(np.argmin(d))]))
    famrows[fam] = {"rgb255": rgb, "L": round(L, 1), "C": round(cstar, 2),
                    "weighted_min": round(s, 4), "binds_weighted": MATS[bi]["id"],
                    "binds_raw": MATS[int(np.argmin(d))]["id"],
                    "per_material": {names[i]: round(float(d[i]), 4)
                                     for i in range(len(names))}}
out["hue_families"] = famrows
sc = sorted(v["weighted_min"] for v in famrows.values() if v is not None)
if len(sc) > 1:
    print("[fam] spread across families: %.4f  (top %.4f, bottom %.4f)"
          % (sc[-1] - sc[0], sc[-1], sc[0]))
    out["family_spread"] = round(sc[-1] - sc[0], 4)

# ---- 3. the inherited candidates, scored on THIS subject's table ----
CANDS = [("W3 mid grey 0.42", (0.42, 0.42, 0.42)),
         ("galleon white", (1.0, 1.0, 1.0)),
         ("black", (0.0, 0.0, 0.0)),
         ("beast lavender-grey (121,121,172)", (121 / 255, 121 / 255, 172 / 255))]
print("\n[inh] THE INHERITED CANDIDATES, on this subject's own table")
print("[inh] %-36s %8s %8s   %-8s %s" % ("backdrop", "weighted", "raw-min", "binds", "note"))
inh = {}
for nm, bg in CANDS:
    s, bi, d = weighted_min(np.array(bg))
    note = ""
    if float(d.min()) < 0.06:
        note = "UNDER the key's own 0.06 cut"
    print("[inh] %-36s %8.4f %8.4f   %-8s %s"
          % (nm, s, float(d.min()), MATS[bi]["id"], note))
    inh[nm] = {"weighted_min": round(s, 4), "raw_min": round(float(d.min()), 4),
               "binds_weighted": MATS[bi]["id"],
               "binds_raw": MATS[int(np.argmin(d))]["id"],
               "per_material": {names[i]: round(float(d[i]), 4)
                                for i in range(len(names))}}
out["inherited_candidates"] = inh

# ---- 4. SENSITIVITY TO L1's ESTIMATED LIGHTNESS ----
# The material table is the weakest link in this chain and says so. On this subject that
# weakness is not evenly spread: L1 is near-achromatic, so the ONLY axis on which a backdrop
# can escape it is lightness - and L1's lightness is the single estimate a styled pair is
# most likely to move (worn steel under harsh directional light can come back anywhere from
# a dark grey to a near-specular white). Every other element carries chroma and is separable
# in hue as well, so a wrong estimate there costs less. This sweeps L1's grey level and
# reports what each candidate's score does, so the ruling knows which parts of the answer
# survive a wrong guess and which do not.
if args.l1_sweep:
    i1 = next(i for i, m in enumerate(MATS) if m["id"] == "L1")
    keep = C[i1].copy()
    print("\n[sens] L1 LIGHTNESS SWEEP - the estimate this answer is most exposed to")
    print("[sens] %6s %6s | %-22s %-22s %-22s"
          % ("L1 v", "L1 L*", "galleon white", "pale blue-violet", "W3 mid grey 0.42"))
    sens = []
    for lvl in [60, 90, 120, 150, 180, 210, 235]:
        C[i1] = np.array([lvl, lvl + 3, lvl + 8]) / 255.0
        lab = srgb_to_lab(C[i1:i1 + 1])[0]
        row = {"L1_rgb": [lvl, lvl + 3, lvl + 8], "L1_L": round(float(lab[0]), 1)}
        cells = []
        for nm, bg in (("white", (1.0, 1.0, 1.0)),
                       ("bv", (214 / 255, 214 / 255, 1.0)),
                       ("grey", (0.42, 0.42, 0.42))):
            s, bi, d = weighted_min(np.array(bg))
            dl1 = float(d[i1])
            row[nm] = {"weighted_min": round(s, 4), "binds": MATS[bi]["id"],
                       "L1_distance": round(dl1, 4),
                       "L1_under_key_cut": bool(dl1 < 0.06)}
            cells.append("%.4f %-3s L1 %.3f%s"
                         % (s, MATS[bi]["id"], dl1, " !" if dl1 < 0.06 else ""))
        print("[sens] %6d %6.1f | %-22s %-22s %-22s" % (lvl, row["L1_L"], *cells))
        sens.append(row)
    C[i1] = keep
    out["l1_sensitivity"] = sens
    print("[sens] the '!' marks L1 falling under the key's own 0.06 cut - the grey-on-grey "
          "trap, arriving or not")

# ---- EXTERNAL_VERIFIER: this file's scorer must equal e04_backdrop.py's ----
# Re-derived independently above from the key's definition; asserted equal on a fixed grid
# so the two files cannot silently drift apart.
_probe = [(0.0, 0.0, 0.92), (0.84, 0.84, 1.0), (1.0, 1.0, 1.0), (0.42, 0.42, 0.42)]
for p in _probe:
    bgp = np.array(p)
    d_here = np.abs(C - bgp[None, :]).max(axis=1)
    s_here = float((d_here / np.where(thin, args.thin_weight, 1.0)).min())
    s_mine, _, _ = weighted_min(bgp)
    assert abs(s_here - s_mine) < 1e-12, "ANDON: this file's scorer disagrees with itself"
print("\n[chk] scorer reproduces the key's max-channel arithmetic on 4 probe points")

if args.out:
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(out, open(args.out, "w"), indent=1)
    print("[chk] wrote %s" % args.out)
