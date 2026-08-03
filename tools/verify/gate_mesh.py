"""HARD MESH GATE -- may the pipeline spend money downstream of this mesh? Exit 0 = yes.

THE MESH IS THE PIPELINE. TRELLIS yawed a head ~30 deg on 3/3 plates of one subject
(2026-08-02) and every downstream stage inherited the defect; five downstream repairs all
merely relocated the artifact. This gate is the ANDON step for the character pipeline:
ANY non-zero exit halts the run before the first credit is spent.

  gate_mesh.py --glb <mesh.glb> [--concept <plate.png>] [--workdir DIR] [--blender EXE]

Exit codes:
  0  PASS   head provably square to the body: THREE independent signal families agree
            (aligned mirror statistics + vertex-PCA geometry + frontal-face detection).
  3  HUMAN  cannot decide automatically -- LOOK at the printed x6 crop sheet (with the
            concept's head beside it when --concept is given), then proceed or reject
            by eye. This is a CORRECT verdict, not an error.
  2  FAIL   reserved -- see "why there is no automatic FAIL" below. Never emitted today.
  1  tool error (render failed, no figure, missing input).

Why there is no automatic FAIL (measured 2026-08-02, do not "fix" this back in):
  Every FAIL rule tested also false-fired on a KNOWN-GOOD mesh. The Tripo mesh of the
  same subject -- the one that projected cleanly downstream (head IoU 0.958, cheek
  coverage 100%) -- reads WORSE than the broken TRELLIS mesh on every automatic signal:
  aligned pair_delta 21.7 vs 18.4, vertex-PCA yaw -45 vs -46 (its nape bun is a larger,
  more offset lobe, and its head is legitimately turned ~15 deg because THE CONCEPT'S
  head is turned ~15 deg). Head-yaw magnitude is NOT comparable across generators, and
  "square to the body" is not even the right question -- "matches the concept's head
  pose" is. Until a concept-registration signal is calibrated (candidate: head-band
  silhouette IoU against the concept, the quantity that actually separated the two
  meshes at 0.795 vs 0.958 in project_texture), a non-PASS is a HUMAN LOOK, never a
  confident number. An honest "I don't know, look at this crop" beats a wrong FAIL that
  blocks a good mesh -- and beats a wrong PASS that burns a day downstream.

Method (calibrated on 7 render control sets + 5 known meshes, 2026-08-02):

  pass 1  8 clay views via turn_render.py --clay. BODY axis = k=2 Fourier phase of the
          shoulder-band silhouette WIDTH vs angle (max width = shoulders square-on).
          Correct within ~10 deg on 7/7 controls incl. off-grid orientations (raw Tripo
          fronts measured 65-100 deg, NOT the nominal 90). Modulation on controls
          0.238-0.314; floor 0.12, below which the body axis is unlocatable -> HUMAN.
  pass 2  re-render 8 views with --yaw-offset = body axis, so view 0 looks straight
          down the body's own front-back axis. The mesh is NEVER mutated (the camera
          rotates; mesh rotation via to_mesh() destroys authored vertex normals).
  A       aligned head-band mirror-asymmetry series s[0..7], re-indexed to the FACE
          side of the axis (the width phase is 180-ambiguous; the face scan picks the
          side):
            pair_delta   = mean_j |s[j]-s[-j]|  (square head => views +j/-j are mirror
                           images)
            front_excess = s[0]-min(s)          (the on-axis view of a square head is
                           the most self-symmetric view)
          ⚠ UNITS: these levels depend on render exposure (measured: the same square
          head reads pair 0.47 on a blown-out render set and ~10 on the gate's own
          properly-exposed renders). Bands are valid ONLY for the gate's own renders:
          straight ~10/3.5 (n=1 -- thin!), yawed 18.4-21.7 / 26.6-35.9, decorated
          square heads in between. Hence PASS needs the OTHER two families to agree.
  B       vertex-PCA: MAJOR axis of uniform surface samples in the head band vs MINOR
          axis of the shoulder band, horizontal plane. Read-only geometry. On known
          meshes: straight subjects +1..+3 deg, TRELLIS yaw -46. Elongation ratio is
          the confidence: below 1.20 the band is hat/hair-dominated (tricorne star,
          beret) and PCA ABSTAINS rather than votes.
  C       Haar frontal-face scan of the aligned views (contrast-stretched head crops).
          On 7/7 controls the peak view was in the true facing quadrant, never
          confidently wrong. A face found far off-axis vetoes PASS (a 180-deg-backward
          head is mirror-symmetric -- this is the check that catches it). NO face found
          anywhere also vetoes PASS: an unformed face (the mesh_character.py
          ptype-512 eyeless class) must not be waved through.

Known limits (measured; the reason HUMAN exists):
  - decorated heads (side-hung hair, feathered/asymmetric hats, offset buns) confound
    every automatic signal -- mirror stats, PCA, and detection alike. HUMAN.
  - a concept-faithful head TURN (the concept itself painted ~15 deg) is
    indistinguishable from a generator-added yaw without the concept. HUMAN + sheet.
  - roll/pitch are not measured, only yaw. The crop sheet shows them to the eye.
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

TOOLS = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BLENDER = "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"

# --- calibrated constants (2026-08-02; see module docstring for provenance) ---
# ⚠ UNITS TRAP (measured): mirror-asym LEVELS depend on render exposure/lighting. The
# original turn_clay control set was rendered near-blown-out (its straight head read
# pair 0.47); the gate's own renders are properly exposed and the SAME square head
# class reads pair ~10. All bands below are in the gate's OWN render units, calibrated
# by running THIS gate on known meshes. Never import thresholds from foreign renders.
BODY_MOD_FLOOR = 0.12          # shoulder-width modulation; controls 0.238-0.314
PASS_PAIR = 12.0               # straight lady 9.9-10.2 (n=1!); yawed 18.4-21.7
PASS_EXCESS = 8.0              # straight lady 3.3-3.6; everything else >= 17.3
PCA_ELONG_FLOOR = 1.20         # below: hat/hair-dominated band, PCA abstains
PCA_PASS_DEG = 10.0            # straight meshes measured +1.3..+2.7
HEAD_FRAC_MESH = 0.16          # vertex head band (no pad; render band uses 0.19)
BG_TOL, PAD_UP, HEAD_FRAC = 18.0, 0.02, 0.19
SH_LO, SH_HI = 0.19, 0.34


def die(msg):
    print(f"[gate] TOOL ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


# ---------- rendering ----------

def render(blender, glb, outdir, yaw=0.0):
    os.makedirs(outdir, exist_ok=True)
    cmd = [blender, "-b", "-P", os.path.join(TOOLS, "turn_render.py"), "--",
           "--glb", glb, "--out", outdir, "--tag", "clay", "--clay",
           "--yaw-offset", str(yaw)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    missing = [i for i in range(8)
               if not os.path.exists(os.path.join(outdir, f"clay_{i}.png"))]
    if missing:
        sys.stderr.write(r.stdout[-2000:] + r.stderr[-2000:])
        die(f"render produced no views {missing} in {outdir}")
    return [os.path.join(outdir, f"clay_{i}.png") for i in range(8)]


# ---------- image signals ----------

def load_fig(path):
    a = np.asarray(Image.open(path).convert("L")).astype(np.float32)
    fig = np.abs(a - a[:12, :12].mean()) > BG_TOL
    r = np.where(fig.any(axis=1))[0]
    if len(r) < 8:
        die(f"no figure found in {path} (bg-tol {BG_TOL})")
    return a, fig, r[0], r[-1]


def shoulder_width(path):
    _, fig, top, bot = load_fig(path)
    fh = bot - top
    band = fig[int(top + SH_LO * fh):int(top + SH_HI * fh)]
    return float(band.sum(axis=1).max()) / fh


def body_axis_deg(widths):
    y = np.array(widths, dtype=np.float64)
    n = len(y)
    t = np.radians(np.arange(n) * 360.0 / n)
    C = float(np.sum(y * np.cos(2 * t))) * 2 / n
    S = float(np.sum(y * np.sin(2 * t))) * 2 / n
    ax = np.degrees(np.arctan2(S, C) / 2.0) % 180.0
    mod = float(np.hypot(C, S)) / max(float(np.mean(y)), 1e-6)
    return ax, mod


def head_mirror_asym(path):
    a, fig, top, bot = load_fig(path)
    fh = bot - top
    y0 = max(0, int(top - PAD_UP * fh))
    y1 = int(top + HEAD_FRAC * fh)
    band = fig[y0:y1]
    c = np.where(band.any(axis=0))[0]
    if len(c) < 4:
        return None
    img, m = a[y0:y1, c[0]:c[-1] + 1], fig[y0:y1, c[0]:c[-1] + 1]
    if img.shape[1] % 2:
        img, m = img[:, :-1], m[:, :-1]
    both = m & m[:, ::-1]
    if not both.sum():
        return None
    return float(np.abs(img - img[:, ::-1])[both].mean())


def face_scan(paths):
    import cv2
    casc = cv2.CascadeClassifier(cv2.data.haarcascades
                                 + "haarcascade_frontalface_alt2.xml")
    scores = []
    for p in paths:
        a, fig, top, bot = load_fig(p)
        fh = bot - top
        y0 = max(0, int(top - PAD_UP * fh))
        y1 = int(top + HEAD_FRAC * fh)
        band = fig[y0:y1]
        c = np.where(band.any(axis=0))[0]
        if len(c) < 4:
            scores.append(0.0)
            continue
        crop = a[y0:y1, c[0]:c[-1] + 1]
        lo, hi = np.percentile(crop, 2), np.percentile(crop, 98)
        crop8 = np.clip((crop - lo) / max(hi - lo, 1e-6) * 255, 0, 255).astype(np.uint8)
        s = max(1.0, 160.0 / max(crop8.shape[0], 1))
        big = cv2.resize(crop8, None, fx=s, fy=s, interpolation=cv2.INTER_LANCZOS4)
        big = cv2.equalizeHist(big)
        det = casc.detectMultiScale(big, scaleFactor=1.05, minNeighbors=3)
        scores.append(float(sum(w * h for (_, _, w, h) in det))
                      / (big.shape[0] * big.shape[1]))
    return scores


# ---------- geometry signal (read-only; never writes or concatenates a mesh) ----------

def pca_head_yaw(glb, n=200_000):
    import trimesh
    sc = trimesh.load(glb, process=False)
    geoms = []
    if isinstance(sc, trimesh.Scene):
        for node in sc.graph.nodes_geometry:
            T, gname = sc.graph[node]
            g = sc.geometry[gname]
            if hasattr(g, "faces"):
                geoms.append((g, np.asarray(T)))
    else:
        geoms.append((sc, np.eye(4)))
    total = sum(float(g.area) for g, _ in geoms)
    pts = []
    for g, T in geoms:
        k = max(1, int(n * float(g.area) / total))
        p, _ = trimesh.sample.sample_surface(g, k)
        p4 = np.c_[p, np.ones(len(p))] @ T.T
        pts.append(p4[:, :3])
    v = np.vstack(pts)
    ext = v.max(axis=0) - v.min(axis=0)
    up = int(np.argmax(ext))
    horiz = [i for i in range(3) if i != up]
    h = v[:, up]
    top, bot = h.max(), h.min()
    fh = top - bot

    def axes(sel):
        q = sel - sel.mean(axis=0)
        w, e = np.linalg.eigh(np.cov(q.T))
        elong = float(np.sqrt(w[1] / max(w[0], 1e-12)))
        return e[:, 1], e[:, 0], elong   # major, minor, elongation

    head = v[h >= top - HEAD_FRAC_MESH * fh][:, horiz]
    shld = v[(h <= top - SH_LO * fh) & (h >= top - SH_HI * fh)][:, horiz]
    hmaj, _, helong = axes(head)
    _, smin, selong = axes(shld)

    def ang(vec):
        return float(np.degrees(np.arctan2(vec[1], vec[0]))) % 180.0

    d = (ang(hmaj) - ang(smin)) % 180.0
    yaw = d - 180.0 if d > 90.0 else d
    return yaw, helong, selong


# ---------- crop sheet ----------

def crop_sheet(paths, out, concept=None, front=0):
    imgs = ([concept] if concept else []) + [paths[front], paths[(front + 1) % 8],
                                             paths[(front - 1) % 8], paths[(front + 4) % 8]]
    labs = (["CONCEPT"] if concept else []) + ["on-axis", "+45", "-45", "back"]
    cmd = [sys.executable, os.path.join(TOOLS, "head_crop.py"),
           "--images", *imgs, "--labels", *labs, "--scale", "6", "--out", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[gate] warning: crop sheet failed:\n{r.stderr[-800:]}", file=sys.stderr)
        return None
    return out


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glb", required=True)
    ap.add_argument("--concept", default=None,
                    help="the concept plate; its head is placed FIRST on the crop sheet "
                         "so the human question ('does the mesh match the concept's "
                         "head pose?') is one glance")
    ap.add_argument("--workdir", default=None,
                    help="default: <glb dir>/gate_<glb stem>/")
    ap.add_argument("--blender", default=os.environ.get("BLENDER", DEFAULT_BLENDER))
    args = ap.parse_args()

    glb = os.path.abspath(args.glb)
    if not os.path.exists(glb):
        die(f"no such GLB: {glb}")
    if args.concept and not os.path.exists(args.concept):
        die(f"no such concept: {args.concept}")
    stem = os.path.splitext(os.path.basename(glb))[0]
    work = os.path.abspath(args.workdir
                           or os.path.join(os.path.dirname(glb), f"gate_{stem}"))
    os.makedirs(work, exist_ok=True)
    print(f"[gate] mesh: {glb}")
    print(f"[gate] workdir: {work}")

    report = {"glb": glb}
    notes = []

    # pass 1: body axis
    p1 = render(args.blender, glb, os.path.join(work, "pass1"))
    widths = [shoulder_width(p) for p in p1]
    axis, mod = body_axis_deg(widths)
    report.update({"body_axis_deg": round(axis, 1), "body_modulation": round(mod, 3)})
    print(f"[gate] body axis {axis:.1f} deg  modulation {mod:.3f} "
          f"(floor {BODY_MOD_FLOOR}; controls 0.24-0.31)")

    front = 0
    if mod < BODY_MOD_FLOOR:
        aligned = p1
        verdict = "HUMAN"
        notes.append(f"body axis unlocatable (modulation {mod:.3f} < {BODY_MOD_FLOOR})"
                     " -- 'square to the body' is undefined without a body axis")
    else:
        # pass 2: body-aligned renders
        aligned = render(args.blender, glb, os.path.join(work, "aligned"), yaw=axis)

        # signal C first: frontal face -- also disambiguates the width phase's
        # front/back 180-deg ambiguity (the axis can land on the occiput side)
        fs = face_scan(aligned)
        fmax = max(fs)
        fview = int(np.argmax(fs)) if fmax > 0 else None
        flip = fview in (3, 4, 5)
        front = 4 if flip else 0
        if flip:
            print(f"[gate] C face: peak at view {fview} -> the body axis landed on the "
                  f"BACK side; statistics re-indexed about view 4")

        # signal A: aligned mirror statistics, about the FACE side of the axis
        s_raw = [head_mirror_asym(p) for p in aligned]
        if any(x is None for x in s_raw):
            die("head band not locatable in aligned views")
        s = [s_raw[(i + front) % 8] for i in range(8)]
        pair = float(np.mean([abs(s[j] - s[-j]) for j in (1, 2, 3)]))
        excess = float(s[0] - min(s))
        a_square = pair <= PASS_PAIR and excess <= PASS_EXCESS
        print(f"[gate] A mirror: series {[round(v, 1) for v in s]} (front = raw view {front})")
        print(f"[gate] A mirror: pair_delta {pair:.2f} (straight ~10 | yawed >=18.4)  "
              f"front_excess {excess:.2f} (straight ~3.5 | others >=17.3)  "
              f"-> {'square' if a_square else 'NOT provably square'}")

        # signal B: vertex PCA
        yaw, helong, selong = pca_head_yaw(glb)
        b_conf = helong >= PCA_ELONG_FLOOR
        b_square = abs(yaw) <= PCA_PASS_DEG
        print(f"[gate] B pca: head yaw {yaw:+.1f} deg  head elong {helong:.2f} "
              f"(floor {PCA_ELONG_FLOOR}; abstains below)  shoulder elong {selong:.2f}  "
              f"-> {'square' if b_square else 'off-axis'}"
              f"{'' if b_conf else ' [ABSTAIN: hat/hair-dominated band]'}")

        # signal C verdict component: face position relative to the (flipped) front
        fview_eff = None if fview is None else (fview - front) % 8
        c_onaxis = fview_eff in (0, 1, 7)
        print(f"[gate] C face: scores {[round(v, 2) for v in fs]}  peak raw view {fview}"
              f" (= {fview_eff} about the front)  -> "
              f"{'on-axis' if c_onaxis else ('NONE FOUND' if fview is None else 'off-axis')}")

        report.update({"head_asym_series": [round(v, 2) for v in s],
                       "front_raw_view": front,
                       "pair_delta": round(pair, 2), "front_excess": round(excess, 2),
                       "pca_yaw_deg": round(yaw, 1), "pca_head_elong": round(helong, 2),
                       "face_scores": [round(v, 3) for v in fs], "face_view": fview})

        # verdict: PASS only when ALL THREE families positively say square.
        # (PCA abstention blocks PASS: with an n=1 straight control the mirror bands
        # are too thin to carry PASS with only two votes.)
        if a_square and c_onaxis and b_conf and b_square:
            verdict = "PASS"
            notes.append("head square to the body: mirror statistics in the straight "
                         "band, PCA confirms, frontal face on-axis")
        else:
            verdict = "HUMAN"
            if not a_square:
                lean = ("signals LEAN YAWED" if pair >= 18 and excess >= 17
                        else "signals are between bands")
                notes.append(f"{lean} -- but yaw magnitude is NOT comparable across "
                             "generators (a known-good mesh reads worse than a "
                             "known-bad one), so no automatic FAIL is issued")
            elif not (b_conf and b_square):
                notes.append("mirror statistics are in the straight band, but PCA "
                             + ("abstained (hat/hair-dominated head band)" if not b_conf
                                else f"reads {yaw:+.1f} deg")
                             + " -- PASS needs all three families")
            if fview is None:
                notes.append("NO frontal face detected in any view -- check the face "
                             "is formed (the ptype-512 eyeless class fails here)")
            elif not c_onaxis:
                notes.append(f"frontal face peaks at view {fview} ({fview * 45} deg "
                             "off the body axis)")
            if b_conf and not b_square:
                notes.append(f"PCA reads the head band {yaw:+.1f} deg off the body "
                             "axis (may be decoration: an offset bun drags this)")
            notes.append("LOOK at the crop sheet"
                         + (" -- the concept's head is panel 1; judge whether the mesh "
                            "matches ITS pose" if args.concept else
                            " (pass --concept next time to get the concept beside it)"))

    sheet = crop_sheet(aligned, os.path.join(work, "HEAD_CROP.png"),
                       concept=args.concept, front=front)
    report.update({"verdict": verdict, "notes": notes, "crop_sheet": sheet})
    with open(os.path.join(work, "gate_report.json"), "w") as f:
        json.dump(report, f, indent=1)

    code = {"PASS": 0, "FAIL": 2, "HUMAN": 3}[verdict]
    print()
    print(f"[gate] ================ VERDICT: {verdict} (exit {code}) ================")
    for nt in notes:
        print(f"[gate]   {nt}")
    if sheet:
        print(f"[gate]   x6 head crops: {sheet}")
    print(f"[gate]   report: {os.path.join(work, 'gate_report.json')}")
    sys.exit(code)


if __name__ == "__main__":
    main()
