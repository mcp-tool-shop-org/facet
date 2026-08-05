# E04 stage 1 — the galleon is painted. Report and HALT.

**Executor session, 2026-08-04, after Ruling 22.** All 41 coverage decisions landed, **coverage
0 undecided**, purity clean of NO-SUCH-FLAG rows, and **the projection flew**. Eight twins,
profile-driven, owner and blend sidecars native. The atlas exists.

---

## The landing, and the two checks

**41 decisions in one commit**, per Ruling 22's two rules and no bespoke arguments: 13 keys as
three whole-tool `_tools_not_on_route` entries, 21 keys as **SPENT** (the value that ran, with
the run as provenance) or **LIVE** (code default as explicit first-run operating point), and 7
keys decided by `_NOT_CLEARED`, now the ruled fourth form and implemented with its lifecycle —
lifting the block reverts its keys to undecided and coverage fires again.

```
[cov] coverage against character.json: 64 reference keys decided, 0 UNDECIDED
[cov] every reference key has an explicit decision in this profile.
[chk] ship.json: 49 values checked against 8 tools — 0 NO-SUCH-FLAG rows
```

**One row where neither bucket-B rule applied verbatim, flagged rather than forced:**
`restylize_views --prompt`. It never ran (every ship invocation passes `--prompts`), so SPENT
does not apply; and LIVE cannot apply, because the code default **is the literal W3 identity
string** — writing it would make another subject's identity a ship *decision*. It carries the
ship's own identity string, transcribed verbatim from the ratified `E04-twin-prompts.json`, so
an invocation that forgets `--prompts` asks for this galleon instead of that warrior. Documents
**and** protects, where `_not_on_route` would only document.

## THE HEADLINE, in H4's units — both, always together

> **styled / valid = 1,147,959 / 3,111,817 = 36.89%**
> **styled / reachable = 1,147,959 / 1,329,359 = 86.4%** of the pre-registered ceiling

The tool's own reachable/valid prints **42.7%** — the pre-registered 42.72%, reproduced from
the inside by the projection itself. The ceiling held.

**Read against the character, with the ceiling difference in the same breath (Ruling 5):**

| | character | ship |
|---|---|---|
| reference share of valid | 68.8% | **36.89%** |
| that subject's reach ceiling | 74.1% | **42.72%** |
| **share of what is reachable** | **92.8%** | **86.4%** |

**H4 is confirmed and its cause is geometry.** The ship's stage-1 share is 31.9 points below the
character's on valid — and 6.4 points below on the only ratio that compares like with like.
Roughly half this subject's surface cannot be reached from any exterior eye-level camera; that
was measured before the twins existed and it is not a pipeline regression.

## Per-view acceptance diagnostics — the operating points, exercised

| view | IoU (tool, vs dilated sidecar) | centroid \|d\| | keyed outside silhouette | largest cmp | bg probe: newly admitted | median ΔE | within ΔE 10 | already-trusted |
|---|---|---|---|---|---|---|---|---|
| y+000 | 0.8287 | 7.7 px | 24,151 (8.48%) | 1,357 | 114,949 | 31.5 | 19.06% | 0.01% |
| y+045 | 0.9068 | 10.0 px | 12,799 (4.06%) | 1,076 | 58,140 | 25.3 | 25.22% | 0.01% |
| y+090 | 0.9423 | 6.3 px | 2,565 (1.34%) | 199 | 18,119 | 15.1 | 39.75% | 0.00% |
| y+135 | 0.9051 | 8.5 px | 11,175 (3.61%) | 2,790 | 58,268 | 19.3 | 34.85% | 0.00% |
| y+180 | 0.8317 | 11.2 px | 22,611 (7.99%) | 2,631 | 108,010 | 28.0 | 21.86% | 0.00% |
| y+225 | 0.9220 | 6.4 px | 11,228 (3.54%) | 1,202 | 54,388 | 25.7 | 24.25% | 0.01% |
| y+270 | 0.9448 | 6.0 px | 2,334 (1.22%) | 199 | 18,226 | 14.7 | 37.71% | 0.01% |
| y+315 | 0.9228 | 5.5 px | 11,150 (3.53%) | 1,814 | 58,791 | 20.8 | 33.85% | 0.00% |

**The suspended `bg-max-pct` was the right call and the full set shows why.** The within-ΔE-10
fraction runs **19.06% – 39.75%** across the eight — every view would have halted at 2.0%, and
the *highest* fractions are on views 2 and 6, the two **end-on** views with the **smallest**
admitted sets (18,119 and 18,226 texels). A ratio whose denominator collapses is not a
contamination measure; it is a perimeter statistic in disguise. **The already-trusted column is
0.00–0.01% on every view** — the trusted core is clean everywhere, and the entire disagreement
is the admitted rim.

The tool's own IoU (0.8287–0.9448) is measured against its **dilated sidecar**, which it says
itself; my exact-silhouette numbers were 0.8442–0.9565. Both orderings agree: the broadsides
are worst, the end-on views best.

## THE PALE-DECK ANSWER, which the ruling asked for specifically

**Upward-facing surface (normal_z > 0.5): 653,140 texels, 20.99% of valid.**

| | styled by stage 1 | hole |
|---|---|---|
| **deck / upward-facing** | **24.99%** | **75.01%** |
| everything else | 40.05% | 59.95% |

**Stage 1 covered a quarter of the deck, and the deck is covered at 62% of the rate the rest of
the ship is.** This is the pale-deck question answered in the only terms that matter: **the
pale deck is not badly *painted*, it is largely not painted at all** — the eye-level cameras
cannot see it. `ship.json` predicted this before any twin existed: eight eye-level yaws reach
30.17% of upward-facing area, and half of it sits under sails, yards and tops.

So Ruling 8's watch item resolves in an unexpected direction: the pale cluster's tight key
margin was never going to decide the deck's fate, because **the deck's dominant failure mode is
absence of coverage, not mis-keyed coverage.** Whatever fixes the deck is a camera or a stroke,
not a backdrop.

## Waterline rim — edge diagnostics where the rejected twin painted water

**Hull-foot texels (lowest 7% of the mesh): 117,682, 3.78% of valid. Styled 19.44%, against
36.89% whole-mesh** — the hull's foot is covered at **53%** of the ship's average rate.

Recorded for E10 with the ruling's framing: the region where the model spontaneously painted
implied water is also **the region stage 1 covers least**. A waterline layer would be painting
where the base coat is thinnest — which is an argument for the layer, and a caution that its
underlying base needs the stroke pass first.

## Owner partition — the ship is the first subject born with the sidecar

| camera | texels owned | share of styled |
|---|---|---|
| y+315 | 172,216 | **15.00%** |
| y+000 | 160,693 | 14.00% |
| y+180 | 158,619 | 13.82% |
| y+045 | 150,558 | 13.12% |
| y+135 | 150,053 | 13.07% |
| y+225 | 142,489 | 12.41% |
| y+270 | 114,589 | 9.98% |
| y+090 | 98,742 | 8.60% |

**No camera dominates** — 8.60% to 15.00%, a 1.74× spread. The two end-on views own least,
consistent with their smaller silhouettes. H3's named likely site (view 7 = y+315 boundaries)
is the **largest** owner, so its seams have the most neighbours to disagree with; the sheet's
owner column will show it.

## The hole map, which seeds the stroke-camera derivation

**Holes: 1,963,858 = 63.11% of valid.** Decomposed against the ceiling:

| | texels |
|---|---|
| reachable but unpainted | **181,400** |
| beyond the eye-level ceiling entirely | **1,782,458** |

**91% of the holes are geometry, not misses.** By surface class:

| class | share of valid | holes | % of that class |
|---|---|---|---|
| upward-facing (deck, tops) | 20.99% | 489,889 | **75.01%** |
| downward-facing (hull bottom) | 22.11% | 515,329 | **74.91%** |
| side-facing | 56.90% | 958,640 | 54.14% |

The two extreme-normal classes are ~75% unpainted and the side-facing class ~54%. **The stroke
derivation's target is not a scatter — it is two coherent surfaces, the decks above and the
hull bottom below**, and the profile's measured elevated pair (0/180 @ 40°, +19.41 points of
deck coverage) addresses exactly one of them. Nothing below the waterline is reachable from any
elevation.

## Artifacts

`E04_armT72/stage1/stage1_8cam.png` · `_holes.png` · `_styled_mask.npy` · `_owner.npy` ·
`_blend.png` · `hole_class.npy`. Atlas variance 0.01589.

## What was not done

No strokes, no finalize, no pack, no Gate 1 sheet. No threshold moved. The suspended bounds
stayed suspended and are reported per view above.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | One profile-driven invocation; 49 profile values and 64 coverage decisions in the file; every diagnostic is the tool's own stdout |
| ANDON_AUTHORITY | **3** | The bound that halted the previous run is suspended *mechanically* and its diagnostic printed on all eight views — the evidence for a real bound now exists where before there was a halt |
| NAMED_COMPENSATORS | **3** | Additive writes only; the profile edit is one commit with git as undo; no spend |
| DECOMPOSE_BY_SECRETS | **3** | Coverage 0 undecided is this standard mechanised: the profile boundary now has a test for omission as well as for mistranscription |
| UNCERTAINTY_GATED_HUMANS | **3** | Both H4 ratios reported together as the spec requires; the pale-deck answer given in the terms asked for, including that it resolves against the expected mechanism |
| EXTERNAL_VERIFIER | **2** | The projection reproduced the pre-registered 42.72% ceiling from the inside, having been computed by a different tool on a different day. `skip:` on a second model |
