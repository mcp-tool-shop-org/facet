# E41 — Where does the wrong colour enter the paint?

**Spec written BEFORE the work.** Advisor seat, 2026-08-16. Dispatched as a background seat
(Sonnet) per the dispatched-seat standard in [CLAUDE.md](../../CLAUDE.md). This document IS the
dispatch: the advisor owes the repo a readable record of what a seat was asked, and E38 closed
owing exactly that.

---

## The question

E40 settled **that** the defect is `reference`-carried — the paint, not any fill. It did not
settle **why the paint is wrong**. Two families remain, and they have different fixes:

- **Generation** — the twin image itself contains gold where the tunic should be green. The fix
  lives in the prompt / control / camera set.
- **Transport** — the twin is clean at that point and our projection puts the wrong colour into
  the atlas anyway. The fix lives in ~20 lines of `project_twins.py`.

E40's **firm lower bound of 29.9%** is why this deserves a seat: at ≥29.9% of the gold class the
*owning view's* twin is clean at that texel, so the colour came from somewhere else. "Somewhere
else" is either another view winning ownership, or **our sampler reaching across a material
boundary.** Nobody has tested the second.

## What is settled — do not re-derive, cite instead

Read `docs/advisor-kickoff.md` "WHAT IS SETTLED" in full. The load-bearing items here:

- The defect is `reference`-carried. Gold **91.05% at 0.99× enrichment** (dead on base rate),
  cloth green **68.46%**, blade own-paint **18.77%** against its dilation fill's **5.55%**.
- Twins disagree **≥ 29.9%** — a *firm lower bound*, decisive per view. A twin hallucinated
  internally **≤ 70.1%** — a **ceiling on the complement, not a measurement of it.** Do not quote
  70.1% as a quantity.
- `project_twins.py:901-913` is an undocumented **two-band split**: `M + blur_σ16(B − M)`.
- Views are never independent: 100% of multi-camera defect faces span ≤ 90°, median 45°.
- Dead, do not resurrect: the blade grazing-angle mechanism, cross-island bleed as the deciding
  defect, the fill/padding/island-predicate family.

## What the advisor already enumerated, so you do not re-spend it

Stated so you start at the frontier rather than the beginning. **Verify anything here that a
finding of yours would rest on** — this is an advisor's reading, and this repo's rule is that an
inherited claim is a hypothesis wearing a fact's clothes. E29's seat lost a prediction to an
unchecked advisor premise, and the sentence was the advisor's.

- `grep` for `BILINEAR|BICUBIC|LANCZOS|.resize(|cv2.resize|map_coordinates|INTER_` across `tools/`
  hits **only `tools/diagnostics/`**. The route has no library resampler.
- The route's sampler is hand-rolled: **`bilinear(img, x, y)` at `project_twins.py:399-413`.**
  Plain, unweighted, 2×2 support, clamping.
- The twin is read at `:501` as `Image.open(...).convert("RGB")` — **alpha is dropped at read.**
- Texels project to **non-integer** `px, py` at `:692-693`.
- The σ=16 blend at `:910-913` divides `blur((B−M)·covA)` by `blur(covA)` — that is the **correct
  normalized-convolution form**, not a straight-alpha error.
- ⚠ The comment at `:694-696` cites `bilinear` as living at `:351-352`. **It does not** — that is
  `fit_background`'s docstring. A stale line reference; note it, and fix it in the commit that
  touches this file.

## Tasks

### Task 0 — enumerate before you commission anything

This repo's most expensive recurring error is building a thing that already exists
(`e12_offsurface.py`'s nine flags; `--edge-absolute` sitting at `project_twins.py:103` while a
report said no flag restored the old rule; a model already on the rig). Before writing any new
instrument:

1. Read `bilinear` (:399), the sampling block (:676-760), and the blend (:901-913).
2. Write down which of Task 1 and Task 2 is **answerable analytically from the code as written**,
   and which genuinely needs a measurement. Say so explicitly.
3. Enumerate what already exists that could answer it — `tools/`, `tools/diagnostics/`, the served
   `mcp__facet-measure__*` surface, and `E:\AI\training\facet_E40_{A,B,C}\`.

**A task you can close by reading is closed by reading.** Report it closed-by-reading with the
lines. That is a full result, not a shortfall.

### Task 1 — is colour resampled consistently with the weight applied to it?

The straight-vs-premultiplied error is: `bilinear(colour) · bilinear(w)` is not
`bilinear(colour · w) / bilinear(w)`. It injects a **signed** colour error, maximal at sample
midpoints, and **zero wherever `w` is locally constant** — i.e. invisible everywhere except at
transitions in `w`, which on this route means the trust-mask edge and the figure boundary.

Determine whether any weight (`fm`, the trust mask, `dist_in`-derived weights, facing) is sampled
or applied in a way that produces this error, **and construct the discriminating case.**

⚠ **This repo's law applies at full force here: a check that cannot fail is not a check.** Before
believing a null, state what a non-zero would have required. A synthetic fixture with a
known-correct expected value decides this; reading the code and reasoning about it does not.

### Task 2 — does the blend average high frequency across views at all?

The swarm asked this. Answer it, and say whether the code settles it without measurement.

If it does, do not build an instrument to re-confirm it — state the mechanism with the lines and
close. If a residual remains that the formula does not settle — e.g. what happens to the `B − M`
discontinuity where **ownership changes across a material boundary**, given σ=16 in atlas space —
name that residual precisely and say what would measure it. **Do not run that measurement in this
arc without checking back**; it is a different question and may deserve its own seat.

### Task 3 — the advisor's own candidate, labelled as a candidate. Kill it as hard as your own.

**Candidate: this is minification aliasing, not an alpha bug.**

`bilinear` has 2×2 support. If a texel's footprint in twin-pixel space exceeds ~2 px, the sampler
is **undersampling** — point-sampling a footprint it cannot cover, with no mip chain, no area
average and no anisotropic filtering anywhere in this route. Under minification across a material
boundary that produces **scattered texels carrying the wrong material's colour**, which is the
shape of the observed defect (spatter, not a 1-px seam) and is consistent with the ≥29.9% firm
bound.

The measurement is the local Jacobian of the atlas→twin-pixel map: per defect-blob texel, the
footprint in twin pixels. If the defect blobs sit in a minification regime and clean regions do
not, that is evidence. If footprints are ≤1 px everywhere — magnification — **this candidate is
dead and I want it reported dead in one line.**

Grade it the way E40's Seat C graded the swarm's blade hypothesis and its own four arms.

## Predictions — write them BEFORE you look

Required. For each task state a prediction, a band, and **whether it was blind**. Then, before
writing any number, do the thing E39's seat did not:

**Compute what your instrument reads when the answer is unambiguously YES, and when it is
unambiguously NO, and predict inside that interval.** A prediction outside the instrument's own
range could not have been right at any state of the world.

And when your quantity is a count, check the population is real, check each member has the
property defined, and predict each clause of a conjunction separately — this repo has missed on
that family in nine consecutive arcs.

## Gates

- **Halt at every gate. Never improvise past one.** Report it with its evidence and stop.
- A gate that measures the **result** halts. A gate that measures the **environment's ability to
  run the measurement** may be repaired — if the repair *adds capability rather than removing
  coverage*, the coverage-removing alternatives are named and rejected in writing, and the firing
  is reported as a fired gate rather than smoothed into a green row.
- Any ANDON you add `raise`s. It is never a bare `assert` — `python -O` deletes those silently,
  and 87 sites in this repo were once removable by an environment variable.

## Out of scope

- Any change to the shipped blend formula. Decision 3 is the Director's and is open.
- Any re-render, re-bake, or generation. Cloud generation is not authorized in this arc.
- Camera geometry (queue item 3) — a separate arc.
- The three stale translations (`fr`, `it`, `pt-BR`) — the advisor is handling those.
- Touching closed rulings, accepted assets, or protected trees except to cite.
- ⚠ **Do not open the Browser pane.** It crashed the client twice last session.

## Working rules for this seat

1. **Never judge whether output is good.** Produce measurements. The Director judges. The words
   *verified, shipped, works, decisive, validated, proven* do not belong in your report.
2. **A negative result is a full success.** Say so plainly and stop, rather than tuning toward a
   number. Killing Task 3 is as good an outcome as confirming it.
3. **Write `handoff.md` early and keep it current** — under `E:\AI\training\facet_E41\`. Two
   executor transcripts were lost inside E38's first day; both times the arc lost nothing because
   state was on disk. On-disk state is the record; a transcript is not.
4. **Do not delegate your own core measurement to a child agent.** One seat did and stalled
   invisibly.
5. **Do not write to the memory store.** The advisor folds findings into the repo.
6. **Tests ride the commit that touches the code.** If you modify tool code, its tests land in the
   same commit. Do not `git add -A`, and do not commit over the shared index — the advisor is
   working in this tree too. Prefer leaving work uncommitted and telling me.
7. **Read a listing complete.** `head`, `tail`, `Select-Object -Last` and default row caps return
   a plausible, well-formed, incomplete answer and never say so. Four instances on this rig; one
   flipped a precedent. Prefer a form that reports a total.
8. **Report to me on the open line as you go.** I steer mid-flight; an arm can be withdrawn or a
   threshold retracted while you run. Ask when a premise looks wrong — **including a premise of
   mine in this document.**

Environment: `E:\AI-Models\trellis2-env\Scripts\python.exe` (absolute, always). Scripts create
their own output dirs. ASCII in tool output. `argparse` eats leading minus signs — use
`--views=-30,0,30`.

## Standards compliance

Scored against the six workflow standards per `.claude/rules/workflow-standards.md`.

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Model tier pinned per seat (Sonnet, stated above); the instrument is this repo's own code at named line numbers; python pinned absolute. Not 3 — no byte-level replay harness for the seat's own new scripts beyond the repo's anchor convention. |
| ANDON_AUTHORITY | 3 | Halt-at-every-gate is a working rule; the gate/repair boundary is stated explicitly; any new ANDON must `raise` rather than `assert`, with the reason. |
| NAMED_COMPENSATORS | 3 | **No irreversible tool call is in scope.** Generation, re-bake and re-render are out of scope; the seat is told to leave work uncommitted. Compensator for the only mutation that can occur (a code edit): `git checkout -- <path>`, owner = advisor, post-rollback state = HEAD. |
| DECOMPOSE_BY_SECRETS | 2 | Tasks split by what changes together: Tasks 1 and 3 both concern the sampler and share a seat; Task 2's residual is explicitly fenced off as possibly a different seat. |
| UNCERTAINTY_GATED_HUMANS | 3 | The seat checks back when a premise looks wrong rather than at a step count, and Task 2's residual carries an explicit check-back. The advisor's candidate is framed contrastively — you probably expect the alpha bug; I think minification, and here is why. |
| EXTERNAL_VERIFIER | 2 | The seat grades the advisor's Task 3 candidate and is told to kill it as hard as its own — generator and verifier are different seats. Not 3: the seat verifies its own Tasks 1 and 2 and no third party re-runs them. Remediation if either returns a positive worth acting on — a second seat re-measures before any fold. Owner = advisor, same session. |
