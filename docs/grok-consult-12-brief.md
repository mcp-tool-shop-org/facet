# Grok build #12 — the material boundary, which is where every defect he has named actually lives

**2026-08-17, facet advisor seat. BUILD round.** Queued behind brief 11.

**The advisor owes this channel a correction.** Brief 11 asked you to build an instrument
that decides whether a regeneration is worth its credits. That was the wrong ask: the
open work is repairing the asset, not measuring whether repairing it pays. The error is
the advisor's. Brief 11 runs to completion because it is already launched; this is the
brief that should have been sent.

*Everything below the line is the paste block.*

---

# Build the material-boundary repair. Every region the Director has circled is a material edge — and none of our fixes have addressed the edge itself.

## What he actually said, twice

**E48:** he judged the renders a clear step up and said the route could go further — and posted three crops
naming the residue: **the arm/sleeve (mangled, mostly the shirt sleeve)**, **the hand
(slightly)**, **the boot-tops/greaves**.

**E49:** he accepted the sheets and named one new defect class — flat angular
patches, green/yellow/orange on the tabard and skirt, gold on a boot.

Every one of those is a **material boundary**: sleeve-edge against flesh, flesh against
tunic-green at the fingers, gold plate against leather at the boot-top. The measurements
agree — defect texels sit at a median **0.439 px** from a material boundary.

**Note the ruling that constrains the sleeve region: the reference is SLEEVELESS.** The
Director ruled that the reference is sleeveless and expressed no preference beyond that. The armhole
smear is tunic paint crossing onto **bare arm**, not a garment rendering badly. Any repair
that "fixes the sleeve" by inventing one is wrong.

## The gap nobody has filled

The polygon class has a repair running now (E51: sample visible orphans with the eroded
sil, fill never-seen surface from its own material's statistics, refuse off-palette
fills). That addresses texels the fill passes invented.

**It does not address the mangled boundary itself.** Where the eight plates disagree
about *where a material ends*, the composite inherits a smeared edge — and no weighting
scheme over disagreeing sources produces a clean edge, because the sources disagree about
the edge's position. The boundary in the atlas is currently whatever the painted plates
voted for. **The mesh knows better than the paint does.**

## The build

`tools/` gets the boundary repair, `tests/` gets **t86**. An invocable CLI in this repo's
sense — `argparse`, real flags, a `__main__` guard.

The thesis to build and to attack: **derive material regions from the geometry and the
atlas topology rather than from the painted colour, then make the boundary agree with
them.** The pieces already exist and you have the tree:

- `tools/emit_view_aovs.py` emits **`surfid`** — the atlas texel index per view pixel,
  `row * 4096 + col` from the GLB's own UVs (lines 300-304). Atlas and view space are one
  lookup apart. Confirmed on disk for all 8 views.
- `tools/palette_gate.py` carries the LAB bands, the **chroma floor**, and two-threshold
  reporting. Reuse it; do not re-roll it.
- `tools/mask_geometry.py`, `tools/render_geomaps.py`, `tools/resample_atlas.py`,
  `tools/twin_fuse.py`, `tools/e13_harmonize.py` all exist. **Enumerate before you
  commission** — the advisor has lost three sessions in this repo to building something
  that was already a flag on an existing tool.

## Laws this build sits inside — each cost a session

- **A global constant must not govern a local feature.** Three instances. A fixed peel's
  cost runs inversely with local feature width: an erosion tuned on a wide figure ate a
  15 px blade alive. Derive per structure, or bound as a fraction of that structure's own
  width, and report per structure how much of its area you touched.
- **Below a chroma floor, hue is not a colour**, and a statistic of angles must be
  **circular**. An arithmetic median of hues once reported +49.1 degrees where the truth
  was -8.4 — on garnet, which straddles the wrap, and which this route paints constantly.
- **Test the property, not a geometric proxy for it.** "Is this pixel near a boundary" is
  not "is this pixel contaminated"; the proxy fails exactly where a structure is thin,
  because a 1-2 px structure is entirely boundary.
- **Gate on the direction your invariant does not bound.** If your repair makes edges
  crisper by construction, a gate on crispness fires on correct work. Ask what can still
  go wrong *after* the invariant, and watch that.
- Gates are `raise`, never bare `assert` — `python -O` deletes an assert and execution
  continues past a fired gate. A test that cannot fail is not a test: for every leg,
  construct the case that fails if the code is wrong in the way the leg exists to catch,
  and show it failing.

## Argue with all of it

**Rank these, kill what deserves killing, and name what we have not.**

1. Is geometry-derived material segmentation even available on this mesh? It is a
   TRELLIS.2 reconstruction with no authored material assignment — so "the mesh knows
   the boundary" may be false, and the honest source might be the atlas island topology,
   or the reference image, or nothing.
2. If the plates genuinely disagree about the edge's position, is snapping to *any*
   single answer an improvement, or does it trade a smear for a confidently-wrong edge?
3. Is the boundary repairable in atlas space at all, or does it have to happen in view
   space and be re-projected — and what does the re-projection cost at the edge?
4. Would a targeted repaint through the existing brush machinery beat a geometric repair
   outright, given the Director judges by eye and not by edge-gradient statistics?
5. Anything unnamed. Your brief-3 catch — that the brief tested unwrappers while calling
   the causal link unproven — turned an arc. Same standard.

## Constraints

Everything is on disk: **no GPU, no cloud generation, no credits.** Do not write anything
under `E:\AI\training\facet_E4*\` or `facet_E5*\` (recorded trees and two live seats).
Leave your change-set **uncommitted** for the advisor's fold. **T34 count surfaces are
yours again this round** — but brief 11's t85 change-set is still unfolded, so state
plainly which counts your change-set assumes, and do not silently reconcile someone
else's numbers. `--basetemp=<scratch>` for pytest on this rig. Absolute python
`E:\AI-Models\trellis2-env\Scripts\python.exe`. ASCII. `argparse` eats leading minus
signs.

Do not grade quality in any register. The Director's eye is the only acceptance gate, and
the deliverable that reaches him is an image.

## Calibration

Nominate **one checkable claim** — about the tree, a number, or a mechanism in a tool you
cite — that we verify by running before anything trusts the rest. Ten for ten, and a
round where your chip loses is still reported.
