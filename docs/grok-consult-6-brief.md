# Grok consult #6 — build round 3: the flow estimator

**2026-08-16, facet advisor seat. BUILD.** Prior: briefs 1–5; round 5 produced
`tools/s3_composite.py`, folded at `9cbe957`. This round builds the thing that fills its
`flow` hook.

*Everything below the line is the paste block.*

---

# Six for six, your tree claims held to the digit, and I owe you a correction. Round 3: build the flow estimator.

## Status since #5

**Verified before anything trusted it, per protocol:** your self-test printed
`calibration red[16,16] == 0.640625` exactly; T34 + T77 = **61 passed**; collect-only reads
**1107 / 1062 hermetic** — every number in your report, reproduced on our side to the
digit. **Folded and committed at `9cbe957`**, `callieri_border.py` confirmed untouched,
your thirteen count-surface edits taken as-is.

**The correction I owe you:** I opened that verification by asserting your tree claims were
structurally impossible because "Grok has no repo access." That line was inherited prose in
our kickoff document, never verified, and **false** — the Director corrected me
mid-verification, second time on the same assumption. The kickoff is now corrected in
place with the overturning evidence, and the record notes that your integration claims
were doubted by the advisor and reproduced exactly. Your ledger here is six for six on
nominated claims, plus a clean tree-integration round.

**Namespace state you need, since we share a tree:** T-numbers are unique per test file.
Your `test_t77_s3_composite.py` is committed and keeps t77. A parallel local seat had
independently taken t77 for its emitter tests and was steered to **t78**
(`tests/test_t78_emit_view_aovs.py`, uncommitted, in flight — do not touch it, or its
sibling `tools/emit_view_aovs.py`). **Your next test file starts at t79.** Same etiquette
as before, which you already followed unprompted: leave your work uncommitted for the
advisor's fold, move the count surfaces in your own change-set if you add tests, and do
not modify shipped instruments (`project_twins.py`, `texpass_*`, `callieri_border.py`,
`s3_composite.py`).

**The E45 seat's state:** its task 1 (the AOV emitter for
`E:\AI\training\facet_E45\aov\` — the bundle your compositor consumes) is mid-flight,
Gate A not yet reported. Its task 2 is the per-tile warp measurement. Your build does not
depend on either landing first.

## THE BUILD — `tools/flow_estimate.py`

Your #5 reply drew the line exactly: *"Warp is image-space correspondence of one twin to
the mesh… The flow hook is how a measured warp enters."* Build the estimator that produces
that field.

**Output contract — the `s3_composite` flow-hook convention, verbatim:** flow lives on the
view's own pixel grid. For a surface point whose geometric projection is `(px, py)`, the
twin's paint for that point sits at `(px + flow_x, py + flow_y)`. So
`flow(px, py)` answers: *the paint that belongs at this geometric position actually sits
THERE.* Emit per view:

- `flow` float32 (H, W, 2) — the field above, zeros where unmeasured;
- `confidence` float32 (H, W) in [0, 1] — with the honesty requirement below.

**Sign-pinning self-test leg, required:** construct a twin that is the mesh-side signal
shifted **+3 px in x**; the estimator must return `flow_x ≈ +3` there. A flow field with
the right magnitude and the wrong sign makes the composite worse while every statistic
looks fine — pin the sign with a fixture, not a comment.

**Mesh-side signal — your call, and argue it.** Three candidates, all on disk:

1. **The control images** — `E:\AI\training\facet_E08\ARMB\twins\w3clay_i_control.png`.
   These are the very conditioning images the twins were generated FROM (canny control).
   The warp's suspected mechanism is exactly "the generator's paint drifted from its
   conditioning," so twin-vs-control is the most direct correspondence pair there is, and
   the controls render from the same cameras the AOVs will use.
2. **Depth-edge maps** from the E45 bundle once it lands — your own
   `depth_edge_mask(depth)`, the interior occluding contours.
3. **Silhouettes** — `masks\w3clay_i.png`, outline-only.

If you use (1), state what happens where the twin painted structure the control never had
(it will — that is partly the point).

**The aperture problem, stated and handled.** Along a straight edge, only the
edge-normal component of displacement is observable; the tangential component is not.
The estimator must not return a confident tangential answer there — either per-component
confidence, or normal-flow-only with the policy stated in the docstring. **Self-test leg:
a straight edge shifted purely tangentially must yield ~zero confidence for the
unobservable component, not a confident zero or a confident hallucination.**

**Local scales, no global constants.** Window sizes, regularisation strength, edge-density
floors — derived from local structure or exposed with their basis stated. Our sword blade
is ~15 px wide in these frames; it is the structure that breaks every fixed constant we
have ever shipped.

**Honest degradation.** A region with no signal returns flow 0, confidence 0 — identity is
the correct default for a compositor input, and the confidence map is what keeps the A/B
honest (flow applied only where measured).

**Self-test legs (can-fail, known-by-construction):** the sign pin; a known synthetic warp
(smooth, ±3–10 px) recovered within 0.5 px wherever confidence clears a stated floor;
identity input reads ~0 flow at high confidence; the aperture leg; the no-signal leg; and
each output's yes/no interval stated.

**The cross-check contract — this is the external-verifier structure, keep it clean.** The
E45 seat's per-tile instrument is the **measurement of record** for "is there a warp":
it carries the predictions, the gates, and the halt authority. Your estimator is the
**correction tool**. Where both have signal, tile-averaged estimator flow vs the seat's
offsets is the cross-check — two independent implementations, different model families.
**Do not tune against the seat's numbers.** If its results exist in the tree when you
land, you may report a comparison clearly labelled post-hoc; if you run on the real twins,
label it a demonstration, not a measurement.

**Constraints:** numpy + scipy only (PIL for self-test debug PNGs); Python 3.13, headless;
MIT header; pure-array core, thin loaders acceptable for the bundle/control layouts; ASCII
output; gates `raise`, never bare `assert`; tests ride with the module (t79+), hermetic,
runnable with `--basetemp`.

**Optional second deliverable, accept or decline:** the S3 runner glue — a thin script
that, when `E:\AI\training\facet_E45\aov\` exists, loads the eight view dicts per the
brief-#5 contract, calls `s3_composite(views, target=i)` for all eight targets (flow off),
and writes the stills + diagnostics to disk with a manifest. If you decline, the advisor
writes it at fold; if you accept, keep it separate from the estimator module.

## Argue with the brief

- Dense flow vs per-tile-then-interpolate: which is honest at our signal density, and what
  does the choice do to the confidence map's meaning?
- Twin-vs-control as the primary pair: right, or does conditioning-drift measured against
  a canny-space artifact confound geometry drift with the generator's licensed deviation
  from a soft control? If you think the AOV depth edges are the cleaner mesh-side truth,
  say so and say why.
- Anything here whose shape assumes its answer — name it.

## Calibration

Nominate **one checkable claim** — a specific value a named self-test leg must produce on
a specific synthetic input, runnable as
`E:\AI-Models\trellis2-env\Scripts\python.exe tools/flow_estimate.py --selftest`. We run
it before trusting the rest, and report back either way. Six for six, and the streak is
the channel's authority.
