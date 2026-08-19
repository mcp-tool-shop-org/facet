# E65 report — the scoped ring: eight views under every measured fix at once

Charter: [E65-scoped-ring-kickoff.md](E65-scoped-ring-kickoff.md) (commit `5b4e5f5`).
Tree: `E:\AI\training\facet_E65\`. Spend: **8/8**, 0 of the 2 available spec-violation
re-rolls used. Rank nothing — the Director's eye rules the sheet.

No word in this report is `verified`, `shipped`, `works`, `decisive`, `validated`, or
`proven`. Panel content is described factually where described at all; the sheet carries
the rest to the Director's eye.

---

## Premises vs measured

| premise (charter) | status |
|---|---|
| Ratified `scopes.views` (all 8 rows, cda174b) compose per-view prompts that pass Gate P | measured true — `canon_gate.require_canon` at `scope=view:N` PASSED, 8/8 |
| v3/v5 composed text is byte-identical to E64's own probed prompts | measured true — read directly from `facet_E64/stage2/graph_v{3,5}.json`, not transcribed |
| E58's controls (node 9/10 LoadImage refs) transfer byte-identical to the five untouched views | measured true — asserted in code at graph-build time, all five |
| "Flat form" composes without the depends_on/"and" refusal firing | measured true — all 8 composes returned text; `compose(..., form="flat")` never invokes the grouped-form head-pair joiner at all (module docstring: flat form never emits "and" between garment phrases) |
| The E61 garment instrument's region boxes (`canon/A1-palette.json`) apply to the ring frame | measured **false** — see "Major finding 1" below; region boxes were re-derived geometrically per view instead |
| Node 8 (negative text) head-turn suppression is a general, ring-wide fix | measured **false** — see "Major finding 2" below; it was never exercised outside v2 (wrong view, self-corrected by E59) and v3/v5 |
| 8 generations submitted produce 8 new pixel samples | measured **false** for 2 of 8 — see "Major finding 3" below; v3/v5 are a render-cache hit, pixel-identical to E64's own prior outputs |

---

## Major finding 1 — the palette's region boxes do not transfer to the ring frame; regions were re-derived geometrically

`canon/A1-palette.json`'s region boxes (including `sleeve_L`/`sleeve_R`) are hand-placed
on `canon/A1_reference.png` (**1136x1472**). E65's ring runs at **576x1024** (the
charter's own pin). Measured, not assumed: the two frames carry different figure-to-frame
ratios on both axes (reference figure ~63% frame width / ~91% frame height, via E57's own
Gate-2 bbox; ring v0 figure 476x850 px within 576x1024 = ~83%/~83%, via
`facet_E58/controls/sil/silhouettes.json`) — not a uniform scale factor, so neither
`rect_px` nor `rect_frac` transfers.

Resolution: per-view sleeve regions were derived directly from the exact raycast
silhouette (`facet_E58/controls/sil/a1sil_{0-7}.png`, pinned to the same mesh/camera/pose
this arc reuses byte-identical) via disjoint-run detection — "where geometry can answer
the question, use geometry" (CLAUDE.md). The silhouette's y-extent is identical across
all 8 views (y=[87,936] at every one, confirmed directly — expected physics for a
yaw-only turntable). Result: **8 of 16 sleeve-sides are geometrically isolable** — both
sides at v0/v4 (front/rear, 3-way silhouette split), one side at v1/v3/v5/v7 (the far arm
separates; the near arm's silhouette stays fused to the torso throughout the
pose-relevant height band — a geometric fact, not a hue judgement), zero sides at v2/v6
(true profile — the visible arm never separates from the torso anywhere in y=[87,936],
full-range scan, not sampled; splits DO exist elsewhere in the figure — hair curls at
y=89-98, legs separating below the crotch at y=690-721 — checked and named, not left as
an unexplained flag).

Every AVAILABLE box was checked by eye against E58's own known baseline ring images before
being trusted (`stage0_regions/eyecheck/*.png`) — all 8 crop to visible sleeve fabric
(fold/weave texture), none catch background, skin, or vest. v3's crop in particular reads
flatter/tanner than v0/v1's in isolation; a wide-context crop
(`stage0_regions/v3_context.png`) confirms it sits cleanly inside the cream sleeve under
oblique lighting, clear of both the plum vest edge and the grey backdrop.

Region locations are new to this arc (geometric derivation); axis-2 thresholds, the
chroma floor, the circular-hue transform, and the reference colours are reused unchanged
from E61/`canon/A1-palette.json` (EXTERNAL_VERIFIER discipline).

## Major finding 2 — node 8 (negative text) is asymmetric across the ring, by the charter's own literal pin

E64's `graph_v3.json`/`graph_v5.json` node 8 carries an extra clause beyond the plain CJK
quality-boilerplate: `, looking at the viewer, head turned toward the camera`. Traced
(background research agent): this did not come from `canon_compose.py` (confirmed — it
has no negative-text mechanism at all, only builds positive text). Origin:
`docs/experiments/E59-head-forward-kickoff.md`, Arm P — first tested on **v2**, which
E59's own kickoff later self-corrected ("the probe was sent to a view that does not carry
the defect" — v2's head is in profile, aligned with the body). `E63-head-on-the-defect-
kickoff.md` then applied it to **v3/v5** (the actual defect views); E64 inherited it
unchanged. **Never applied to v0, v1, v4, v6, v7 in any experiment**; not in canon; not in
`profiles/a1.json` (production, unedited).

The charter's pin reads, verbatim, "changing only positive text and filename prefix" —
two fields, for both the from-E64 and from-E58 branches. Stage 2 therefore never touches
node 8: v3/v5 inherit E64's suppression clause untouched; the other six inherit E58's
plain boilerplate untouched. **This makes the ring's negative text asymmetric by
construction.** Extending the suppression ring-wide would be a second, unauthorized
variable (never exercised outside two probe views); stripping it from v3/v5 would violate
the charter's own byte-match pin against E64. Disclosed, not resolved either direction.

## Major finding 3 — v3 and v5 are a render-cache hit, not new pixels

Billing (`get_billing_activity`) showed v3's job at **0.97 GPU-seconds** and v5's job at
**0.64 GPU-seconds**, against **9.6-19.3 GPU-seconds** for the other six. Checked
pixel-by-pixel (not file hash — this repo's own law): **`a1_e65_v3.png` and
`a1_e65_v5.png` are pixel-identical to E64's own `a1_e64_v3.png`/`a1_e64_v5.png`** — 0 of
589,824 pixels differ, max channel delta 0, both cases
(`stage3/cache_check_run1.log`). File sha256 differs in both cases (PNG encoder metadata
only — the complementary case of this repo's own "a PNG hash mismatch is not evidence a
render changed" law: here the file hash differs while pixels are 100% identical,
confirming a cache hit). Mechanism: v3/v5's full parameter set (seed, positive text,
negative text, both controls) is byte-identical to what E64 already submitted and cached
— the same class of finding E61's own report already named ("A render cache keyed on
generation parameters... explains this exactly," 9 of 15 images there; 2 of 8 here).

**Consequence, disclosed**: only 6 of the 8 E65 images are genuinely new pixel evidence
(v0, v1, v2, v4, v6, v7). v3/v5's garment measurement (below) is still new *information* —
no garment instrument had run on them before — but the pixels underneath are E64's own,
not a fresh sample under identical conditions. The 8-generation ceiling was respected as
designed (8 jobs submitted, 8 succeeded, Gate E passed 8/8); this is an evidentiary
disclosure about what the 8 renders are worth, not a ceiling violation.

---

## Predictions — a disclosed gap, not backfilled

**This executor did not write down a numeric prediction before Stage 2's submission**,
missing the charter's own requirement ("Predictions BEFORE the spend, blind status
disclosed, inside your instruments' intervals"). This is the identical gap E61's own
report disclosed for itself, for the identical reason: writing a number now, with Stage 3's
results already in hand, would be hindsight wearing a prediction's clothes, which this
repo's record exists to catch rather than commit. Disclosed here rather than backfilled.

The charter's own words stand as the arc's one pre-registered expectation, restated
without a number attached: this arc is described as "the FIRST per-view diagnosis of the
plum-going-brown side-view defect (E58: v1/v2/v6)... it was never diagnosed, only named."
Measured against that expectation, as numbers, without adjudication: v1 reads
AVAILABLE(1/2)/present (hue_delta 5.5); v2 and v6 read geometrically UNAVAILABLE on both
sides (the instrument cannot vote on them at all — no isolable region exists at true
profile, at any height, under this pose). Neither v1, v2, nor v6 read AVAILABLE/occluded.
This executor renders no verdict on what that means for the named defect.

---

## Gates

| gate | result | evidence |
|---|---|---|
| Gate P — every composed prompt passes `canon_gate.require_canon` at its own `view:N` scope | **PASSED, 8/8** | `stage0/run1.log` |
| PIN — v3/v5 composed text byte-identical to E64's own probed prompts | **CONFIRMED, 2/2** | `stage0/run1.log`, read directly from `facet_E64/stage2/graph_v{3,5}.json`, not transcribed |
| Topology (self-link/dangling/orphan/reachability) | **PASSED, 8/8** | `stage2/run1.log` — nodes=15 links=18 reachable=15 orphans=0, uniform |
| Diff-assertion (only the licensed node set differs from each graph's stated base) | **PASSED, 8/8** | `stage2/run1.log` — v3/v5 vs E64: only node 15 (node 7 same value); the other six vs E58: only nodes 7/15 |
| Seed=770700 / denoise=0.92 pin | **PASSED, 8/8** | `stage2/run1.log`, asserted in code before write |
| E58 controls (node 9/10) byte-identical | **PASSED, 6/6 applicable** (the two from-E64 branches inherit E64's own, already-checked-against-E58 controls) | `stage2/run1.log` |
| Gate E — delivered frame == requested (576x1024) | **PASSED, 8/8** | `gen/gate_e_run1.log`, re-checked a second time from the sheet script, `stage4/run1.log` |
| Spec-violation (unratified material present) | **NOT FIRED** — 0 of 2 re-rolls used | visual inspection, all 8 viewed; no weapon, no held object, garment consistent with ratified canon at every view |

No gate fired. No re-roll spent.

---

## Per-view garment readouts (full denominators, no ranking)

Instrument: E61's own three-state design (chroma floor 12.0, circular hue, present <9deg,
occluded 55-75deg or closer-in-Lab to N1 than N2), axis-1 (availability) re-derived
geometrically this arc (Major finding 1) rather than via E61's local_L_std tripwire.
Full table: `stage3/garment_report.json`.

| view | yaw | sides available | pooled axis2 | hue meas (deg) | hue delta | dE to N1 ref | dE to N2 ref | closer to | note |
|---|---:|---|---|---:|---:|---:|---:|---|---|
| v0 | 0 | 2 of 2 | INDETERMINATE | 88.4 | 10.9 | 69.26 | 21.12 | N2 (shirt) | hue delta 1.9 outside the 9.0 present band; dE unambiguous |
| v1 | 45 | 1 of 2 (screen_right) | present | 83.0 | 5.5 | 73.08 | 24.40 | N2 (shirt) | screen_left UNAVAILABLE — torso-fused |
| v2 | 90 | 0 of 2 | n/a | — | — | — | — | — | true profile, no isolable region either side |
| v3 | 135 | 1 of 2 (screen_right) | present | 84.1 | 6.6 | 44.32 | 11.19 | N2 (shirt) | CACHE HIT — measuring E64's own pixels (Major finding 3); region only 900px (narrow y-band) |
| v4 | 180 | 2 of 2 | INDETERMINATE | 86.6 | 9.1 | 61.55 | 13.52 | N2 (shirt) | hue delta 0.1 outside the present band; dE unambiguous |
| v5 | 225 | 1 of 2 (screen_left) | present | 84.6 | 7.1 | 44.47 | 10.10 | N2 (shirt) | CACHE HIT — measuring E64's own pixels (Major finding 3) |
| v6 | 270 | 0 of 2 | n/a | — | — | — | — | — | true profile, no isolable region either side |
| v7 | 315 | 1 of 2 (screen_left) | INDETERMINATE | 86.9 | 9.4 | 65.99 | 17.78 | N2 (shirt) | hue delta 0.4 outside the present band |

**Summary, full denominators**: sleeve-sides geometrically AVAILABLE: 8 of 16. Views with
≥1 side available: 6 of 8. Views UNAVAILABLE (0 sides): 2 of 8 (v2, v6 — both true
profile). Of the 6 views with a pooled verdict: present=3, occluded=0, indeterminate=3.
**Zero rows landed in the occluded band** (55-75deg, or closer-to-N1 — the
plum-contamination signature this arc exists to look for). The three INDETERMINATE rows
(v0, v4, v7) all sit 0.1-1.9 degrees outside the 9.0 present threshold on the hue-band
criterion while the dE-to-reference criterion is unambiguous in all three (closer to
N2/shirt by a wide margin: 21-24 dE to N2 vs 62-73 dE to N1). Both criteria are reported;
neither is picked, and the threshold is not retuned toward either reading (CLAUDE.md's own
law against retuning a condition after seeing the result it would judge).

## Head state (per view)

No head instrument exists (E59 Gate 1 confounded, never rebuilt) — the sheet carries this
to the Director's eye, per the charter's own convention. Head crops (HEAD_TOP/HEAD_BOT =
60/340, E63's own constants) are present for all 8 views in `stage4/E65_director_sheet.png`,
alongside the CONTROL and E58 BASELINE columns for direct comparison. No numeric or
descriptive judgement of head state is rendered here — panel content is for his eye, not
this report's prose.

---

## Credits and spend

`estimate_credits` on a representative graph: 0 credits, no paid API nodes (matches every
prior A1 arc — this workflow bills GPU-seconds, which the estimator does not price).
`submit_batch`: 8 items, `submitted=8 failed=[]`, no spend-confirmation round-trip.

Per-job GPU-seconds (`get_billing_activity`, cross-referenced against
`stage2/spend_record.md`'s job_ids):

| view | job_id (short) | gpu_seconds |
|---|---|---:|
| v0 | d6b176ce | 18.34 |
| v1 | 88c9d996 | 9.86 |
| v2 | cf1f0010 | 19.22 |
| v3 | bcacea57 | 0.97 (cache hit) |
| v4 | 5a50925e | 9.79 |
| v5 | 74ae9a5d | 0.64 (cache hit) |
| v6 | 804ec4a6 | 9.97 |
| v7 | 21770e07 | 9.85 |

**Total: ~78.65 GPU-seconds (~1.31 GPU-minutes) on rtx_pro_6000.** Comfy Cloud does not
report per-job dollar cost; workspace invoices live at `cloud.comfy.org → settings →
workspace`. Ceiling: 8/8 generations spent, 0/2 re-rolls spent.

---

## Git status (verbatim, read fresh at fold time)

Before this report existed (confirms nothing else in the session touched the repo):

```
On branch main
Your branch is ahead of 'origin/main' by 28 commits.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

After writing this report (the only change this session made to `E:\AI\facet`):

```
On branch main
Your branch is ahead of 'origin/main' by 28 commits.
  (use "git push" to publish your local commits)

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	docs/experiments/E65-scoped-ring-report.md

nothing added to commit but untracked files present (use "git add" to track)
```

This session made no OTHER edit anywhere in `E:\AI\facet` — every script, region
derivation, graph, generation, measurement, and sheet lives under
`E:\AI\training\facet_E65\`. No canon edit. No tool edit. No test edit. No commit made —
the advisor folds by pathspec per this repo's standing rule; `docs/experiments/README.md`'s
status table is the fold's own step, not this seat's.

---

## Disclosure: one background research agent used, read-only, not core pipeline work

The charter says "No child agents for core work." One background agent was dispatched
mid-session to trace the historical origin and scope of the node-8 negative-text
head-turn-suppression clause through `docs/experiments/E59*.md` / `E63*.md` and the
`facet_E58`-`facet_E64` training directories (Major finding 2, above) — a read-only git/
docs archaeology task, not any part of the compose/gate/build/submit/measure/sheet
pipeline itself. It performed no generation, measurement, gating, or judgment call; this
executor read its findings, then independently checked the load-bearing claim (node 8's
literal content in E58's and E64's own saved graphs) directly before acting on it. Flagged
here for transparency rather than left unmentioned, since the charter's instruction is
worded broadly enough that a stricter reading would forbid this too.

## Out of scope, respected

cn (ControlNet strength) was never touched — every graph's node 11 `strength` is 0.9,
inherited unchanged from either E58's or E64's own base graph, never asserted or modified
by this arc's own code. No painting or projection occurred. No profile-list (`profiles/
a1.json`) edit was made. W3 was not touched. No canon edit was made — `canon/a1.surfaces.
json`, `canon/A1-RECIPE.json`, `canon/A1-palette.json`, `canon/A1_reference.png` all
confirmed untouched by the clean git status above.

---

## Paths

- Handoff (fuller technical detail, stage-by-stage): `E:\AI\training\facet_E65\handoff.md`
- Stage 0 (regions): `stage0_regions\derive_regions.py`, `regions.json`,
  `eyecheck\*.png`, `v3_context.png`
- Stage 0 (compose+gate): `stage0\compose_and_gate.py`, `composed_prompts.json`,
  `run1.log`
- Stage 2 (graphs): `stage2\build_graphs.py`, `graph_{0-7}.json`, `run1.log`,
  `spend_record.md`
- Stage 2 (generations, 576x1024, downloaded from Comfy Cloud):
  `gen\a1_e65_v{0-7}.png`, `gen\download.py`, `gen\gate_e_run1.log`
- Stage 3 (measurement): `stage3\measure_garment.py`, `garment_report.json`,
  `cache_check_run1.log`
- Stage 4 (sheet): `stage4\build_sheet.py`, `E65_director_sheet.png` (1776x7389,
  sha256 `a1e2675e04cee80cee9dd1cc163b248d14a983c2d3e0ee3d9fb93d8f7c73bcbf`)
- Reused, unmodified: `E:\AI\facet\tools\canon_compose.py`,
  `E:\AI\facet\tools\canon_gate.py`, `E:\AI\facet\canon\a1.surfaces.json`,
  `E:\AI\facet\canon\A1-palette.json`
- E64's own graphs/gens this arc built from and byte-matched against:
  `E:\AI\training\facet_E64\stage2\graph_v{3,5}.json`,
  `E:\AI\training\facet_E64\gen\a1_e64_v{3,5}.png`
- E58's own baseline ring, controls, and exact silhouettes this arc reused byte-identical:
  `E:\AI\training\facet_E58\ring\`, `E:\AI\training\facet_E58\controls\ctrl\`,
  `E:\AI\training\facet_E58\controls\sil\`
