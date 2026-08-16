# Grok consult #4 — a build, not a consult

**2026-08-16, facet advisor seat.** First build delegation to this channel.

*Everything below the line is the paste block.*

---

# Build us the Callieri border mask. You are the one who found we never had it.

## Status since #3

**S0 is run and your chip lost.** We rendered the asset FLAT + Standard transform — no Studio
multiply, no AgX — beside the canonical twin. A and B differ by **6.1/255 mean**; both are equally
wrong against the twin. The blade carries orange, blue and dark patches over what should be clean
steel; the right bracer is a smear of pink, gold and green; gold flecks sit across tunic and skirt.
**Colour management is dead as an explanation. The asset is genuinely degraded and the week's
rejections were reading something real.**

Your S0 was still the right first step — it was cheap and it removed a whole branch in ten minutes.

Repo is clean and pushed: instrument flags with a non-perturbation proof, count surfaces reconciled
at 1087/1042, four arc documents and all consults filed, served index recertified after 30 commits
stale (VERIFY PASSED, four legs, byte-identity).

Next is your S1 (soup vs welded clay, normals from welded connectivity). That one is ours — it is a
Blender-side render we have the rig for.

## What we want you to build

**The Callieri border mask and the mixed-depth reject, as one standalone Python module.** You
corrected us at primary source: the border is distance to **image borders and depth-map
discontinuities (silhouette borders)**, Sobel on the **non-normalised** depth — not the material-ΔE
quantity we measured and then wrongly closed the lever on. We have never built the real thing. You
should build it, because you are the one who read the paper and we are the ones who got it wrong.

It feeds S3 (the Blender existence proof) and S4 (the same weight on the current projector), so it
is on the critical path either way.

### Inputs we will hand it, exactly

Per camera, eight cameras, all `752 × 1024`:

- `depth` — **float32 numpy array**, non-normalised camera Z in world units. Background is `+inf`
  (we can emit NaN or a sentinel instead if you prefer — say which and why).
- `silhouette` — bool array, True on figure.
- Optionally `normal` — float32 `(H, W, 3)`, camera-space unit normals, if your facing term wants it.

Figure scale for reference: the mesh's largest bbox axis is `0.9969` in the same world units as
depth. Camera is **orthographic**. Typical figure occupies ~151,705 of 770,048 pixels.

### What we need out

1. `border_weight(depth, silhouette) -> float32 (H, W)` in `[0, 1]` — Callieri's border mask:
   zeros at image borders **and** at depth discontinuities, weight rising with image-space distance
   from those zeros. **A true Euclidean distance transform** (`scipy.ndimage.distance_transform_edt`),
   not an iterated dilation or a Gaussian — we have been burned by an approximation standing in for
   a quantity before.
2. `depth_edge_mask(depth) -> bool (H, W)` — the discontinuity set itself, exposed separately so we
   can look at it.
3. `mixed_depth_reject(depth, ...) -> bool (H, W)` — True where a 2×2 bilinear footprint would
   straddle a depth jump, i.e. where sampling the twin at that location mixes two surfaces. This is
   your own item 3 from consult #1 and it is **not** the same thing as the border weight; keep them
   separate.
4. `facing_weight(normal, exponent) -> float32 (H, W)` — with the exponent as a parameter, not a
   constant. We currently ship `facing^6.0` and want to try 2 and 4 once normals are welded-smooth.

### The hard requirements, which are this repo's own laws

- **A check that cannot fail is not a check.** Ship a self-test with synthetic fixtures whose
  correct answers are known by construction — a flat plane (no discontinuities, so the only zeros
  are the image border), a step edge at a known column, a thin bar a few pixels wide. For each,
  state what the function **must** return, and make the assertion fail if the implementation is
  replaced by something trivial.
- **State the instrument's yes/no interval.** For each output, what does it read when the answer is
  unambiguously yes, and unambiguously no? We have predicted outside an instrument's own range
  before and it cost an arc.
- **No global constant governing a local feature.** Three instances in this repo, each cost a
  session. If your depth-discontinuity threshold is absolute, a thin structure gets treated the same
  as a torso. Derive it from local scale, or expose it and say in the docstring what it is relative
  to. **Our sword blade is roughly 15 px wide in these frames** — that is the structure that breaks
  fixed constants here.
- **Say what it does at the figure's own silhouette**, where depth jumps to background. That edge is
  a real discontinuity and Callieri zeroes it. Confirm that is what you intend, because it means the
  entire outline of the figure gets zero weight and something has to be said about how wide that
  band is.

### Constraints

- **numpy + scipy only.** No Blender API, no torch, no OpenCV, no pymeshlab (GPL). PIL is fine for
  the self-test writing debug PNGs.
- **Python 3.13**, and it must run headless.
- **MIT or public-domain header** — this is a commercial project.
- Pure functions, no I/O in the mask functions themselves. The self-test may write PNGs.
- No hidden mutable state, no reliance on call order.

### What we do NOT want

- A Blender node graph — we will wire it ourselves.
- Anything that reads our filesystem or assumes our paths.
- An approximation of the distance transform.
- A "probably fine" threshold with no stated basis.

## Two things worth your attention while you write it

**We think you should tell us if the mixed-depth reject subsumes the border weight**, or vice
versa. They are related and we do not want two levers that are secretly one — that is a mistake we
have already made this week with a material-boundary quantity standing in for a depth one.

**And say what this cannot fix.** If the twin's paint is wrong at a location where depth is perfectly
smooth, no border weight helps. We would rather have that limit stated in the module's own docstring
than discover it after wiring.

## Calibration

Same standard. Nominate one checkable claim about your own implementation — a specific value your
self-test must produce on a specific synthetic input — that we verify by running it before trusting
the rest. Yours have held four times.
