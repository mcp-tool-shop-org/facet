# E30 report — per-profile anchor gates for W3, the galleon and the dragon

**Executor session, 2026-08-09.** Predictions committed at `b18c050` before the first
replay; anchors at `f556d44`. **Gate 5 FIRED on the projection lane and the arc halted
there.** No polish work ran; no accepted asset changed; no tool code was written.

Eight anchors were built and all eight reproduce. One replay does not reproduce, and that
is this arc's most valuable output. Two further replays in the same lane were **not run**,
because the gate says halt.

---

## What is on the screen

| # | subject | stage | verdict | tier that decided |
|---|---|---|---|---|
| T50 | W3 | finalize | reproduces, byte-identical | byte |
| T51 | galleon | finalize | reproduces, byte-identical (atlas **and** sidecar) | byte |
| T52 | dragon | finalize | reproduces, byte-identical (atlas **and** sidecar) | byte |
| T53 | W3 | ceiling | reproduces — 15 reachable counts across three distinct settings | value |
| T54 | galleon | ceiling | reproduces — 5 counts, collapsed setting | value |
| T55 | dragon | ceiling | reproduces — 5 counts, collapsed setting | value |
| T56 | dragon | elevated | reproduces — the **whole recorded payload**, both ladder rungs | value |
| T57 | galleon | commit | reproduces — four state files byte-identical, 31,581 texels | byte |
| — | **W3** | **projection** | **DOES NOT REPRODUCE — gate 5, halted** | byte flagged, **pixel confirmed** |
| — | galleon | projection | **NOT RUN** (halted) | — |
| — | dragon | projection | **NOT RUN** (halted) | — |
| — | W3 | elevated | **not anchorable** — no recorded output exists | — |
| — | galleon | elevated | **not anchorable** — no recorded output exists | — |
| — | W3 | commit | **not anchorable** — no recorded pre-state exists | — |
| — | dragon | commit | **not anchorable** — no recorded pre-state exists | — |

11 test functions in 8 files, all `artifacts` + `slow`. **`11 passed in 250.66s`.**

---

## 1. The halt — W3's projection does not reproduce

**Replayed:** `project_twins.py --profile profiles/character.json --prep facet_E06/C1/prep
--view 0..7=facet_E08/ARMB/twins/twin_N.png`, against the recorded
`facet_E08/ARMB/stage1_8cam.png`.

```
                       recorded (E08-eightcam.md)      replay
styled texels               1,653,659                1,718,750     +65,091
holes                         749,151                  684,060     -65,091
atlas variance                0.03687                  0.03713
reachable                   1,780,546                1,780,546     unchanged
```

Holes lost equals styled gained exactly, so the write-head accounting is intact; the
difference is entirely in **which texels were accepted**.

### Which tier decided, and it was not the byte tier alone

The dispatch's warning was checked before this was believed. `tools/verify/anchor_compare.py`:

```
byte_identical   False
pixel_identical  False | differing 330,481 (1.969820%)
largest component 15,767 px (0.0477 of differing) | |d| p50 1.0  p95 61.0  max 195
```

**The pixel tier confirms it.** 330,481 genuinely differing pixels is not encoder metadata,
so this is not the two-false-halts class. The **shape** matters as much as the magnitude and
the grid carries it: the largest connected component is **4.77% of the differing set**, so
the difference is **distributed, not concentrated**, and the magnitude is bimodal — half the
differing pixels differ by a single level (p50 = 1.0) with a tail to 195. That is the
signature of an **acceptance-rule change**: newly-admitted texels arrive at full magnitude,
and their arrival re-weights the blend by a level almost everywhere else.

### The mechanism, read out of the tool rather than run for

[`tools/project_twins.py:720`](../../tools/project_twins.py:720) carries its own history:

> `⚠ REBUILT (E08 A3). This erosion used to be an ABSOLUTE distance, scaled by the` …

and [line 764](../../tools/project_twins.py:764) prints what it does now:

```
edge-dist = min({ed_body}px, {edge_frac} x local half-width); median local cap …
```

Two pieces of evidence tie that to the number above, and neither required another run:

1. **The global term still matches the record.** E08-eightcam's per-view table records
   `ed_body` 3.85 / 4.17 / 2.75 / 3.03 / 3.86 / 4.13 / 2.74 / 3.03. The replay's view 7
   printed `min(3.0px, 0.333 x local half-width)` — 3.0 is the recorded 3.03 at one decimal.
   So A3 did not change `ed_body`; it **adds a per-texel cap on top of it**.
2. **The direction is forced.** A cap can only make erosion *smaller*, so fewer samples are
   rejected and more texels are admitted. Measured: **+65,091**. E16-10 measured the same
   family in `texpass_iter` at +30.6%, "concentrated in the thinnest strata".

**There is no flag that restores the pre-A3 rule.** `project_twins --help` has no
`--edge-mode`; the rebuild *replaced* the rule rather than adding a mode, which is the
opposite of how `texpass_iter` took the same port (T11: `--edge-mode local`, opt-in, default
`global`, byte-identical).

### The two readings, stated rather than resolved

This is the advisor's to rule, and both readings fit the evidence:

- **A failing anchor.** The recorded invocation was replayed and did not reproduce.
- **A stage that is not anchorable at HEAD.** The recorded 8-camera invocation is *not fully
  quoted anywhere I found* — E08-eightcam quotes flag fragments for its four *other* anchors,
  not for the adopted 8-cam run — so the invocation used here was **reconstructed from
  `profiles/character.json`, not recovered from the record**. Under that reading the anchor
  was never built, and what failed was the reconstruction.

**I did not sweep for an invocation that matches**, and the repo's own law is why: a match
cannot be verified as *the* recipe. Nothing was adjusted, nothing re-run with a changed
parameter.

⚠ **What this does NOT say.** The accepted asset is unmoved: W3's `atlas_final.png`
reproduced **byte-identically** in T50, from the recorded post-stroke state. What cannot be
re-derived at HEAD is the stage-1 **intermediate** that state was built from.

### Why the other two projections were not run

Gate 5 says a failing anchor halts the arc. The galleon's and the dragon's projections sit
in the same lane behind the same rebuilt rule, and running them after the gate fired would
be improvising past it. They are named as the arc's first carry, with a prediction already
on the record (E30-predictions P3: "expect 0 to 2 of 3").

---

## 2. What is not anchorable, per subject, per stage — and why

**4 of 15, exactly as predicted, and for exactly the predicted reasons.**

| subject | stage | reason |
|---|---|---|
| W3 | elevated | **No recorded output exists.** `find` over `facet_E06` and `facet_E08` returns no `elevated*.json`. W3's arc is E06/E08; `e12_elevated` is an E12-era instrument. |
| galleon | elevated | Same, one arc earlier — E04. |
| W3 | commit | **No recorded pre-state exists.** `state/atlas.prev.png` is *one* of the three files a commit needs; `holes.png` and `styled_mask.npy` in that directory are post-commit, overwritten in place by the commit that produced them. |
| dragon | commit | Same. `run/state/atlas.prev.png` alone; `state_holeclass/` is a different state (1,809,823 holes against 1,710,180) and not the predecessor. |

**The galleon is the one subject with a commit anchor**, and only because its E04 arc left a
`bindcheck/` state beside its own job — which is T11's shape and is why T57 exists.

**A negative result reported plainly:** the dragon yields three anchors and W3 yields two.
Neither was padded toward six.

---

## 3. How the invocations were recovered — three cases worth the ruling's eye

None was chosen by running variants until one matched.

**W3's finalize mode**, from a report rather than a sidecar. W3 has no `finalize.json`.
`E08-task3-report.md` records *"565 texels took the mean fallback"*, and in surface-aware
mode that count is **structurally zero** — the tool says so itself (`grown = valid.copy()`
before the loop, E14 Ruling 31d). A non-zero fallback can only come from the default flood.
The replay then reproduced 647,624 / 565 / 0.04329 — the whole of that report's row.

**The ceiling floors, from the profiles, corroborated by the record's own structure.**
`profiles/character.json` pins 0.45/**0.18**; ship, beast and prop pin 0.45/0.45. E16-6's
repair collapses the tool's three specs to one block exactly when the floors are equal. So
the profile **predicts** each recorded payload's shape before any replay: W3's three blocks
should differ and the other three subjects' should be identical. Measured — W3's N2 reads
1,265,391 / 1,039,711 / 1,362,043; the galleon's, the dragon's and the sword's are identical
across all three blocks. Profile and record corroborate each other; neither looks at a result.

**The galleon's commit pre-state, by conservation.** Holes lost must equal styled gained:

```
bindcheck        holes 1,963,858   styled 1,147,959
selftest_state   holes 1,932,277   styled 1,179,540
                      -31,581           +31,581
```

and 31,581 is the number `E04-stroke-frame-halt.md` records for that selftest.
`selftest_state/atlas.prev.png` is byte-identical to `bindcheck/atlas.png` — the commit's own
record of what it was handed. The identity holds from that directory and from no other in the
tree. **`selftest2/` is named and NOT anchored**: a second commit from the same pre-atlas
landing 31,418 texels under a condition this session did not identify. An anchor whose
invocation is unknown is not an anchor.

Both premises are kept **runnable** rather than written down: T57's second test asserts the
conservation ladder, and T52's asserts that `run/state_final` is the post-finalize copy — so
a future session that repoints either anchor fails on the premise before it fails on the
replay.

---

## 4. The prediction scorecard

| # | predicted | measured | verdict |
|---|---|---|---|
| **P1** total buildable of 15 | **11**, band 8–13 | **8 built and reproducing**; 3 projections not buildable at HEAD | **MISSED HIGH by 3**, and all 3 are the lane I flagged |
| **P2** W3 / galleon / dragon | **3 / 4 / 4** | **2 / 3 / 3** | missed by exactly one each — the same projection |
| **P3** reproduce first run | **7 of 11**, band 4–10 | **8 of 9 replays run** | the *count* landed inside the band; see below |
| **P4** not anchorable, + reason | **4**, "missing recorded output or missing pre-state" | **4** — 2 elevated (no output), 2 commit (no pre-state) | **HIT, on the count and on the reason** |
| **P5** any anchor need the pixel tier | **NO — 0 of them** | **0.** All 8 decided on the byte or value tier | **HIT** |

**P3 carries an internal inconsistency that is mine and worth owning.** I wrote a point
estimate of 7 and then, in the same section, a composition that summed to 8 before the
projections were counted at all (finalize 3 + ceiling 3 + elevated 1 + commit 1). The
composition was exactly right; the headline number contradicted my own working two paragraphs
below it. A point estimate that disagrees with its own decomposition is not a prediction, it
is a typo wearing one.

**The P1 miss is the seventh consecutive arc on the unit/population family, and it is a NEW
shape.** E27 Ruling 5's law asks whether the property is *defined* for every member — I
applied it, and it caught the two elevated stages (P4 hit). But I checked existence:
*does this stage have a recorded input, a recorded output?* All three projections have every
artifact on disk. What none of them has is **an instrument that can still express the rule
the recorded run used.** Candidate law, for the advisor:

> **A member can hold every artifact the property names and still fail it, because the
> instrument lost the option the recorded run was made with.** Existence of the operands is
> not replayability. Before counting a stage as anchorable, ask not only *is the output
> recorded* but *can the tool at HEAD still be put in the state that produced it* — and a
> tool that REPLACED a rule rather than adding it as a mode cannot.

The contrast is in the repo already: `texpass_iter` took the same A3 port as an **opt-in
flag** with `global` still the default (T11), and `project_twins` took it as a **replacement**.
One subject's anchors survive that; three subjects' do not.

**And the mechanism I named was wrong while the lane was right.** I predicted the projection
misses and attributed them to E16-8's fitted border ring and E16-10's `local_thickness`
extraction — both *later* changes. The actual cause is **E08 A3's erosion rebuild**, earlier
than either, and it was sitting in the tool's own comment the whole time.

*One wording slip, noted rather than edited:* `E30-predictions.md` line 113 reads "T10 **works**
because E16-8 **proved** byte-identity" — two words the dispatch forbids in any doc. **The
predictions file is left byte-frozen anyway**, because editing a pre-registered prediction
after seeing the results is the move the freeze exists to prevent, and that holds for wording
as much as for numbers. The correction lives here, where post-hoc text belongs.

---

## 5. Gates

| gate | evidence | verdict |
|---|---|---|
| **1. tree manifest** | 7,312 files / 17,072,807,610 bytes before the first replay; at the close `RECHECK before=7312 after=7312  added 0  removed 0  changed 0`. E23's count reproduces exactly | **PASS** |
| **2. every replay to scratch** | every `--out`/`--json`/`--state` pointed at the session scratchpad; the one write-head replay ran on a `copy_state` copy | **PASS** |
| **3. no sha256 literal in test code** | `grep -nE "[0-9a-f]{16,}"` over all eight files returns nothing | **PASS** |
| **4. every anchor carries the input re-hash leg** | all 8; T55's leg additionally covers the recorded `ceiling.json` it reads its own anchor from, because `E12_prep` is the one prep tree that holds outputs beside inputs | **PASS** |
| **5. a failing anchor halts the arc** | **FIRED** on W3's projection. Halted. Nothing adjusted, nothing re-run with a changed parameter, the other two projections not run | **FIRED — reported, not repaired** |
| **6. `git diff --name-status -- tools/` empty** | reads **two entries** — `tools/diagnostics/texel_provenance.py`, `tools/measure_mcp.py`. Both are named in this dispatch's own coordination section as **E28 task 3's**. **E30 wrote no tool code**; its entire commit is `tests/` and `docs/experiments/` | **PASS for E30**, non-empty for the working copy |
| **7. CI green** | **NOT GREEN, and knowingly so — see §6.** No run id is written here because none has run on this commit | **NOT YET RUN / expected red on T34** |

---

## 6. Finding — the front-door count is a shared scalar and two live seats both move it

**This is a coordination defect the dispatch's separation did not cover**, and it was measured
rather than inferred. The dispatch made the *tool surface* disjoint (gate 6) and allocated
T-numbers, but **T34 pins a single test count across eight READMEs plus `SHIP_GATE.md`,
`docs/advisor-kickoff.md` and `site/src/site-config.ts`** — and both seats add tests.

Measured, in the exact trees:

| tree | total | hermetic | T34 |
|---|---|---|---|
| HEAD (`731df45`) | 790 | 761 | green |
| **E30's commit** (HEAD + the 8 anchor files) | **801** | **761** | **20 failed / 30 passed** |
| shared working copy (both seats) | 808 | 768 | 20 failed / 30 passed |
| what the sibling's uncommitted README edit states | 797 | 768 | — |

T34's doctrine is that the stated count must equal `pytest --collect-only` **of that tree**.
E30's commit is self-consistent only at **801/761**; the combined tree is only consistent at
**808/768**. **No single number is correct for both**, so two seats adding tests to one repo
cannot both be green independently — whichever lands second must re-measure and edit.

The surfaces that carry the count are, right now, **modified in the working copy by the
sibling seat**. Staging any of them would commit their uncommitted work, which E28 Ruling 16
and this dispatch's coordination section both forbid. **Put to the Director, who ruled:
report it, touch nothing.** So nothing was touched.

**The remedy, and whose it is:** once E28 task 3 lands, one edit sets every count-bearing
surface to the then-true pair (808/768 if neither seat adds another test) and T34 goes green
for both arcs at once. Until then E30's commit is **local and unpushed** — pushing it would
put a knowingly-red T34 on the remote and, with `cancel-in-progress: true`, collide with the
sibling's run.

*The verification pattern that produced this section is worth keeping: `git archive HEAD |
tar -x` into scratch, plus this arc's own files, reproduces the exact tree CI will see
without touching a shared working copy or `.git`.*

---

## 7. What this session does not settle

- **The projection lane.** Two subjects unmeasured; W3's measured and halted. Whether the
  right remedy is a `--edge-mode global` opt-in in `project_twins` mirroring `texpass_iter`'s
  (which would make all three projections anchorable at once), or whether stage-1
  intermediates are simply not anchorable across the A3 boundary and the record should say so,
  is a ruling. **Gate 6 forbade me to touch the tool, and the finding is filed rather than
  fixed.**
- **`selftest2`** — a recorded commit from a known pre-state whose distinguishing condition
  I did not identify. A ninth anchor is sitting there for whoever finds it.
- **The wider diagnostic-sidecar population** enumerated in the predictions — `blade_band`,
  `brush_reach`, `keyed_outside`, `silhouette_agree`, `palette_gate`, `offsurface`,
  `thin_curve`, `contact_mask`, `w1_coverage`, `layer_export`. Named, not scored.
- **Whether eight anchors is enough to open a polish lane.** E14 Ruling 35's clause says
  every lane opens with its subject's anchor gate; three subjects now have finalize and
  ceiling gates, the dragon has elevated, the galleon has commit. Whether the projection gap
  blocks the lane is the Director's.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | every anchor pins a recorded invocation to a recorded output under the absolute pinned interpreter; predictions SHA-committed at `b18c050` before the first replay; three invocations recovered from the record with the derivation written into each docstring |
| ANDON_AUTHORITY | **3** | gate 5 fired and the arc halted; two further replays in the same lane deliberately not run; the fired gate is reported as fired rather than smoothed into a green row, and so is gate 7 |
| NAMED_COMPENSATORS | **3** | tests and docs only — `git revert` restores everything. The recorded trees were read in place with scratch outputs and manifested before and after: 7,312 / 0 / 0 / 0 |
| DECOMPOSE_BY_SECRETS | **3** | one anchor per subject per stage, in its own file; every subject-specific fact lives in that subject's own docstring; nothing shared across the three lanes |
| UNCERTAINTY_GATED_HUMANS | **3** | the halt is routed to the Director's judgment with both readings stated and neither resolved; the shared-count collision was put to him as a question rather than decided unilaterally, and his ruling is recorded here |
| EXTERNAL_VERIFIER | **3** | the anchor pattern is the external verifier — recorded bytes produced before this session existed, with no literal in test code to fit to. Every count is loaded from the recorded JSON rather than transcribed, which is stricter than T8 |

---

**HALT at the report, per gate 5 and the dispatch.** Eight anchors are in the repo at
`f556d44`; the ninth measurement is the halt and is the reason to read this document.
