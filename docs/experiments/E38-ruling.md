# E38 — ruling

**The arc is RUNNING, and this document does not close it.** It rules on the evidence that
has landed, because A10 sat unruled through a seat change and an unruled arm is a shelf.
Written 2026-08-16 by the incoming advisor, at its own seat, against
[the spec](E38-material-route-kickoff.md) and `E:\AI\training\facet_E38\phase2\phase2-report.md`.

The route question this arc opened is answered. **The question the Director's eye is on has
moved**, and it moved to [E39](E39-w3-polish-kickoff.md) — see Ruling 6.

---

## 0. What this seat verified before ruling

Rulings on numbers this seat did not measure are worth less than the numbers. Three checks
ran first:

- **The index ritual**, on a scratch DB: build then verify, **19/19, all four legs**,
  determinism leg byte-identity, declaration leg 0 findings.
- **The tool-edit anchor** re-run independently — see Ruling 5, which corrects it.
- **The `texpass_finalize.py` predicate**, read at the file rather than quoted from the
  handoff: `fill = ~grown & (cnt > 0)` at line 155, with `valid` used at 146 and 158 to decide
  *when to stop*, never *where to write*. The docstring at lines 12–18 already says so.

## 1. A10 — a clean negative. Adopt nothing from it. RULED.

Both padding values land at **3.3–3.4× A11's own Population B** (546 and 569 against 165).
The lever this arm existed to isolate produced no reduction — direction reversed, magnitude
+4.2% / +2.0%.

**What makes this a finding rather than a null:** the lever demonstrably moved real atlas
geometry. Valid-texel coverage fell **81.39% → 64.05%**, 17.34 points of the 4096² canvas
shifted from chart interior into gutter, exactly as padding is supposed to act. The gutter
widened and Population B did not care. A lever that does nothing and a lever that does its
job while the target ignores it are different results, and only the coverage measurement
separates them.

**The transferable fact is the one the arm did not set out to measure.** Run on the identical
148,062 visible faces, with the same union-find, `arm_geom.py` reports **xatlas 12,979 charts
against Blender-native 8,601 — 50.9% more islands.** That is a same-instrument,
same-population comparison, which is what makes it citable at all; this repo has been bitten
three times by island counts compared across different objects, including inside this very
report (see Ruling 4). The arm's own setup had explicitly downgraded chart segmentation as
"not this arm's lever." **The measurement weighs against that premise**, and the executor said
so plainly rather than burying it.

**RULED: A11 alone remains the best configuration for Population B. A10 does not change that
ranking, and no padding value is adopted.** The executor's refusal to try a third padding
value after two misses is the correct call and is noted as such.

## 2. The sweep's finding, and nobody picks a winner. RULED.

Two standing results, neither displacing the other:

| | Population A | Population B |
|---|---|---|
| A0, Blender 5.2 stock | 766 | 556 |
| A1+A7+A6', Blender 5.2 | **4** (−99.48%) | 279 |
| A11 — Blender 5.3 alpha, **stock** | **0** (−100%) | **165** (−70.3%) |
| A11 + the same three levers | 0 | **257 — worse** |

**On 5.2, which is the route today, the three packing levers are right. On 5.3, change
nothing** — they were compensating for a Blender bug ([PR #161752](https://projects.blender.org/blender/blender/pulls/161752),
merged: *"if a triangle does not overlap texel center, it will be empty"*), and once it is
gone they turn net-negative on Population B. Tight packing carries an independent cost on B,
present with or without 5.3.

**RULED: 5.2 remains the route. Blender 5.3 alpha is an INSTRUMENT and does not enter the
pipeline.** No lever is adopted into the route's defaults in this ruling; the shipping
configuration is a Director decision and it now has numbers under it rather than a preference.

## 3. Both populations closed by intervention, and B is independent. RULED, and this is the
   arc's methodological high point.

Population A: a magenta refill of every texel outside `valid_mask` left **0.00% of A dark on
either build**, median ΔE 114. Population B: **100% shifted**, median ΔE 66–67, while nothing
at B's own nearest texel changed — only a render-time read past the nearest valid texel can
produce that.

**What earns the word "closed" is the shape of the test, not the size of the number.** The
first attempt at B's independence was geometric, returned zero, and **the executor withdrew
its own "settled by construction" reading in place** because the test could not have returned
anything else given the already-known 7–8 texel distance, and could not see mip-radius bleed.
That is *a check that cannot fail is not a check*, applied by a seat to its own result. The
replacement — re-running the magenta intervention on A11's own atlas — is mechanism- and
radius-agnostic by construction, returned **0.0% movement at A11 and 100% at A0**, and so is
a test that could have failed and did not.

**RULED: Population B is independent of Population A. Neither is a hypothesis any longer.**

## 4. The executor's own correction stands, and it makes the class BIGGER. RULED.

The report's "20,600 islands, 47% more fragmented than W3" was withdrawn by the seat that
wrote it, caught because a fresh run printed a number that did not match a recorded one. The
two figures were **different measurement methods on different pipeline stages**, not two
meshes on one footing. Apples to apples the comparison is **13,722 (E38) against 14,010 (W3)
— 2.05%, very slightly LESS fragmented.**

**The correction is what makes the finding serious.** If this route's fragmentation is
*route-normal*, then E05's named class — *"at 8 faces an island is small enough to be entirely
unpainted, and 54.6% of them were"* — is a property of the **route**, not of this mesh, and is
present in every native-UV asset since. The seat then refused to quantify it on assets it had
not measured, which was right, and the back-catalogue survey measured it afterwards:
longsword **0.808%** > W3 **0.578%** > dragon **0.065%** > galleon **0.000000%** of pooled
figure pixels. Whether it renders black does not generalise at all — W3 **0%** on every view,
longsword **39.70–51.40%**. **The galleon's zero is unseen, not absent**: 23,260 black
background texels these eight cameras never sample.

**RULED: the object/methodology ledger the executor added to that report is adopted as the
form.** A count in this repo carries its object and its pipeline stage, or it is not a
citation. This is the ninth arc in a row to lose a number to the unit/population family and
the first to ship a ledger against it.

## 5. ⚠ The anchor holds — but it is PIXEL identity, not byte identity. The report's wording is
   corrected here.

`tests/test_t74_bake_hero_prep_pack_levers.py`'s docstring and the phase-2 report both state
the reconstructed A0 command reproduced *"all 8 renders byte-identical."* **Measured at this
seat, that is wrong.** All eight PNG file hashes **differ**:

```
view 0   bb89fbffefcf0e79   vs   86d9b2b0e458a0c3     ... and so for all eight
```

and all eight are **pixel-identical**: `0` differing pixels, `maxabs 0`, over (1024, 368, 4).
The two atlases *are* byte-identical (`f8c379f382126b4e`, `1c39b85b484cb94a`).

**This is the third live firing of this repo's own law** — *a PNG hash mismatch is not
evidence a render changed; file bytes are not pixel values.* Had anyone re-run the anchor as
a byte check it would have produced a false halt on a correct result.

**RULED: the anchor HOLDS and the tool edit is admitted.** Its force is undiminished — pixel
identity is the stronger claim for this purpose, since it is a statement about the render
rather than about the encoder. Only the wording was wrong. The correction is folded into T74's
docstring in the commit that lands it, per *correct in place, with the measurement that
overturned the claim*.

## 6. ⚖ The framing correction, and it is the ADVISOR'S. RULED and adopted.

**The Director, 2026-08-16:** *"let's not over focus on the black artifacts. W3 is far from
perfect and needs a serious polish."*

He is right. The class this arc solved measures **0.578% of W3's figure pixels and renders
zero black there**, while what is actually wrong with W3 — gold across the tunic, skirt, boots
and blade; green on the grip; brown-green on the hands — sits measured in this repo's own
`docs/known-defects.md` and was treated as a footnote for a whole arc.

**The error is not that E38 was run.** Its route question is answered and the answers in
Rulings 1–4 are real. The error is *which question was allowed to be the priority*, and that
is an advisor's choice, made by the outgoing seat and inherited by this one. It is the same
shape as the eight instances already in that seat's record: **a countable proxy standing in
for the thing the Director's eye actually judges.**

**RULED: E38's route question is answered; E38's class is not W3's defect and never was.**
The polish question opens as **[E39](E39-w3-polish-kickoff.md)**, dispatched at this seat.
E38 stays RUNNING — A5/A9 and the shipping-configuration decision are unfinished — but it is
no longer the priority arc.

## 7. Three CI reds were inherited, unnamed by the handoff, and are repaired in the same
   commit as this ruling.

Verified directly against `HEAD` (`git show HEAD:<path>`), not inferred:

| red | evidence at HEAD | cause |
|---|---|---|
| T34 experiment pins | `README.md` says *"Thirty-seven experiments are in"*; the status table holds **38** | E38's status row landed; the four surfaces that quote the count did not |
| T34 kickoff pins ×3 | `docs/advisor-kickoff.md` matches **0** of its three pinned anchors | the kickoff was rewritten and its pinned sentences were not re-pinned — T34's own message says *"a rewritten sentence must be re-pinned in the commit that rewrites it"* |
| T24 arc span | `conventions.json:237` declares `E3[0-7]`; the record holds E38 | the span was never bumped, so `laws.paid_for_by` could not read the arc's own laws — visible in `facet_index verify`'s vocabulary leg as *"law paid_for_by … not recognised: E38"* |

**Never leave CI red** is a standing studio rule, and *"the pre-tag re-count gate has fired at
every release seat and caught a stale number every time"* is `SHIP_GATE.md`'s own line about
exactly this. **The lesson is the one SHIP_GATE already states and the handoff re-proved: a
hand-written list of surfaces is itself a live-moving quantity.** The outgoing handoff
enumerated the tree's uncommitted state precisely and named none of these three.

**A fourth, smaller instance, and it is this seat's own:** adding E39's status row bumped the
experiment count to **39**, so the same four surfaces moved again inside this session. That is
not a defect — it is T34 working — and it is why all of it is one commit.

**RULED:** counts reconciled off the collector at **1072 total / 1027 hermetic**, experiment
surfaces at **39**, span bumped to `E3[0-9]`, and the three kickoff anchors written back into
`docs/advisor-kickoff.md` as sentences that carry their information rather than as regex bait.

## 8. What this ruling does NOT settle

- **A5 and A9 never ran.** A5 (combination) is the one arm the sweep's own evidence most
  recommends, since A1 and A4 fix Population A by two non-overlapping mechanisms — but on 5.3
  Population A is already 0, which is most of A5's stated case. **Not commissioned here.**
- **The shipping configuration.** Ruling 2 gives the numbers and picks no winner. His call.
- **The back-catalogue re-bake**, greenlit conditionally on the fix eliminating the class. It
  does — but W3's STATE cannot be regenerated (⚠ CORRECTED 2026-08-16, E40 Seat B: the four files DO survive at E:\AI\training\facet_E06\C1\prep\; the three prior checks searched facet_E08 only. Only STATE regeneration is impossible — finalize replays byte-identically on frozen state, so fill-stage arms run on W3 itself.) (the original wording read: "no `prep_uv.glb`/`mask.npy`/`pos.npy`/`meta.json`
  survives; verified a third time at this seat), and the longsword is the only accepted asset
  carrying visible black. **He gets numbers, not a plan.**
- **The zero-UV-area triangles.** 1,035 faces (0.345%) carry real 3D area and no UV footprint;
  `smart_decimate.py:220-225` guards UV collapse by *whole-mesh variance*, which 0.345% cannot
  move. **No guard in this pipeline checks UV area per face.** Named with its mechanism and
  file location by the executor, routed here, and **not fixed** — it is a genuine unguarded
  decimation artifact and it wants its own arm.
- **Whether Population B and W3's cross-island bleed are one class at two sites** — B is a
  render-time *read*, E07's 74.9% is a bake-time *write*. Still unconfirmed. E39 measures the
  W3 side of it first.

## 9. The executor seats' record on this arc

Stated because calibration is the point of keeping one. Across E38 the dispatched seats
**caught five of the advisor's seven wrong mechanism calls**, withdrew two of their own
readings in place before either could contaminate a downstream arm, found two instrument bugs
(the parked-face area double-count, the lossy raycast round-trip) before they reached more
than one report, and ran a reproduction check *because a number surprised them* — which is the
one habit that separated "citation mismatch" from "reproducibility failure" and is now the
report's own stated rule.

They also missed most of their numeric bands. Both facts belong in the same paragraph: **the
predictions were mostly wrong and the work was mostly right**, because every miss was
pre-registered, scored against the bar set before looking, and reported without retuning.
That is the arrangement working exactly as designed.
