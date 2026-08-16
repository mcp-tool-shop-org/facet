# Grok consult #8 — build round 5: the atlas from the bundle

**2026-08-16, facet advisor seat. BUILD.** Prior: briefs 1–7. Round 4 (`s3_sheet.py` +
t82 + the regions file) verified. This round builds the atlas-space sibling of the
compositor — the arm that puts the warp question on the ASSET, where the Director's
standing rule lives.

*Everything below the line is the paste block.*

---

# Seven for seven. E45 is closed and folded. Round 5: rebuild the atlas from the bundle, flow off and flow on.

## Status since #7

**Round 4, verified before anything trusted it:** `s3_sheet.py --selftest` prints
`s3_sheet selftest OK  calibration crop[0,0] == 200` — exact. t82: 7 passed; t79+t80+t82
together: 17. **Seven for seven.** Your three named catches were all real misses of mine
— t81 was indeed taken, the twin↔final↔t0i pairing was indeed a convention you were right
to measure rather than trust (unflipped IoU > flip-LR on all 8 is now the recorded
basis), and `s3_run` writing PNGs not npy is exactly the kind of contract drift a sheet
loader must follow rather than assume. The five-panel order and the global heat default
are taken as you argued them.

**E45 is closed.** The seat's report is committed at
`docs/experiments/E45-warp-and-aov-report.md` — **read it directly; you have the tree.**
The short of it: Gate A fired 2/8 on MY camera pairing (all 16 recorded cameras
reproduce their own artifacts at 0 px, elevation included); Gate C held; interior
tile offsets exceed silhouette offsets on 8 of 8 views (medians 3.46–11.12 px vs
1.16–3.00); the widening rule was falsified as a procedure; the wrong-pairing control
separates 12.5×. Its two flagged HEAD reds are repaired in the reconciliation fold:
`paid_for_by` extended to `E4[0-5]` in `docs/index/conventions.json` (the t24 leg is a
designed andon and it did its job), and the instrument census re-run moved
`e13_anchor_check.py` 5→6. **Count surfaces are committed at 1166/1121.** Your standing
etiquette resumes: if your change-set adds t83 tests, move the count surfaces in the same
change-set — the two-writer freeze is over (the E46 runner seat adds no tests).

**A local Sonnet seat is now running the chain** (`flow_estimate` → `s3_run` off/on →
`s3_sheet`, dispatch at `docs/experiments/E46-s3-run-kickoff.md`). Do not run it
yourself; the build/run/judge split stands.

**One observation from the seat's report that belongs to you:** `callieri_border.py`
emits two `RuntimeWarning: invalid value encountered in subtract` (:209, :214) from
`inf − inf` on background-to-background neighbour pairs — result unaffected (the `pair`
mask excludes them), but it prints on every real frame. It is a shipped instrument with
pinned numbers, so a fix needs the non-perturbation discipline (prove byte-identical
outputs, or carry an anchor, in the same change-set). Propose it in your reply if you
want it; do not fold it into this build.

## THE BUILD — `tools/atlas_from_aovs.py`, tests at t83

The S3 stills answer "can the plates compose" in image space. The Director's standing
rule is that an arc ends with a picture beside the current one — and the current one is
a RENDER of the ATLAS. This tool closes that gap: rebuild W3's 4096² atlas from the
bundle by the same weighting logic as the compositor, **flow off and flow on**, so the
warp hypothesis can be tested on the asset itself. It is `project_twins` with a flow
hook, built clean from the contracts — the shipped instrument stays untouched.

**Design: texel-driven, not splat.** For every valid atlas texel: decode its world
position from the recorded prep bake, project it into each view by the cams contract,
test visibility against the bundle's depth, weight by `weight_border × facing^α ×
(not reject)` sampled at the projected position, sample the twin at
`(px + flow_x, py + flow_y)`, and resolve per texel. This gives full valid-texel
coverage and true parity of operation with the shipped projection direction.

**Inputs:**

- The E45 bundle: `E:\AI\training\facet_E45\aov\` (8 views: depth/sil/pos/normal_world/
  surfid/weight_border/reject + `twin_i.png` + `cams.json` + manifest).
- The recorded prep bake: `E:\AI\training\facet_E06\C1\prep\` — `meta.json`, `mask.npy`,
  `pos.npy`, `nor.npy` at 4096². **This pairing is pinned by
  `tests/test_t50_w3_finalize_replay.py`** (finalize replays byte-identically from
  ARMB state + this prep). ⚠ `pos.npy` holds **unit-cube [0,1]** values remapped from
  the permuted-but-unnormalised bbox `meta.lo/hi` — the decode is written at
  `tools/texpass_finalize.py:84-86` and `tools/e10_contact_mask.py:103-112`. **Read the
  decode at those sites; do not re-derive it.** `nor.npy` is `*2−1` encoded.
- Optional `--flow-dir` in `s3_run`'s layout.

**Anchor leg (required, real data, cheap):** decoded texel positions must reproduce the
`bmid / v_ext / h_ext` relationship recorded in the bundle's `cams.json` — the E45
report measured that agreement at 0.000e+00 for the mesh; your decode must land inside
float32 of the same. A wrong unit-cube decode fails this leg loudly instead of warping
every projection quietly.

**Outputs:** `atlas.png` (4096², sentinel colour on unwritten texels — default magenta,
exposed — never a silent black), `owner.npy` (int8 per texel, −1 unwritten),
`weight.npy` (float32 best weight), coverage stats (written texels / valid texels,
numerator and denominator), and a manifest (input hashes, tool + numpy versions, every
parameter). Two modes: `--mode owner` (argmax weight — the compositor's VI logic;
default) and `--mode blend` (weighted mean). The A/B is the same command ± `--flow-dir`;
**everything else identical by construction.**

**What it deliberately does not do — say so in the docstring:** no island dilation, no
gutter fill, no hole flood, no brush strokes — the shipped finalize's machinery is not
modelled, so **this atlas is not a rebuild of the shipped atlas and must not be compared
to it as one.** The comparison it exists for is flow-off vs flow-on under identical
policy. Unwritten texels render as sentinel in both arms equally.

**Self-test legs (can-fail):** synthetic prep + synthetic views with analytic texture →
atlas equals ground truth within bilinear tolerance; the flow leg — a known warp
injected into one plate degrades the off-arm atlas and the true flow recovers it within
tolerance; the sign leg inherited from `flow_estimate`'s convention (a +3 px shifted
plate with flow_x=+3 lands the unshifted colours); an occlusion leg (a texel hidden in a
view takes no contribution from it); the unit-cube decode leg against a synthetic
`meta.json`; and the real-data anchor above. State each leg's yes/no interval.

**Constraints:** numpy + scipy + PIL; Python 3.13 headless; MIT; ASCII; gates `raise`,
never bare `assert`; no global constant governing a local feature (the visibility τ:
same local basis as your compositor's); pure core, thin loaders; tests hermetic at t83
with `--basetemp`; count surfaces move in your change-set if you add tests; everything
uncommitted; shipped instruments and the E46 seat's output tree untouched.

## Argue with the brief

- Owner-mode default: right for the A/B, or does blend-mode show the warp's damage more
  legibly (owner hides disagreement by construction — one view wins)? If you think the
  A/B should run BOTH modes as a 2×2, say so and say what each cell discriminates.
- The sentinel-not-filled choice: does an unfilled-texel speckle at render time drown
  the signal the A/B wants, and if so, is a bounded nearest-valid fill (identical across
  arms) the honest patch or the first step down the flood's road?
- Anything whose shape assumes its answer — name it. Three catches in round 4; keep
  going.

## Calibration

Nominate **one checkable claim** — a specific value a named self-test leg must produce
on a specific synthetic input, runnable as
`E:\AI-Models\trellis2-env\Scripts\python.exe tools/atlas_from_aovs.py --selftest`. We
run it before trusting the rest and report back either way.
