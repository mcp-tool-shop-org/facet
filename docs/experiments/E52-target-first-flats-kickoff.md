# E52 — does the target-first compositor carry the flat class?

**Dispatched 2026-08-17 by the advisor seat. Sonnet executor, background, open line.**
This document is the spec. Mid-flight rulings are appended here with dates.

---

## Why this arc exists, and what the kickoff got wrong

The advisor kickoff at `docs/advisor-kickoff.md:69` ranks *"the target-view-preferring
compositor"* as the first free item and states **"Nothing built."**

**That premise is false, and it was checkable in one grep.** `tools/s3_composite.py` takes
`primary_mode` and its own docstring (lines 18–27) argues target-first against the brief's
"highest-facing leads". `tools/s3_run.py:117` and `:169` default it to `"target"`.
`docs/grok-session-handoff.md:89` already records *"S3-A primary is target-first
(`primary_mode='facing'` exists)."* E46 ran it on **all 8 targets, both flow arms**, and
the stills are on disk.

Fourth instance in this repo of **enumerate the resource before commissioning one**
(`e12_offsurface.py`'s nine flags; a model already on the rig; `--edge-absolute` already at
`project_twins.py:103`; open3d's cp313 wheel). This one was caught before the commission
rather than after.

**What is genuinely not built** is target preference *in the atlas* — and it cannot be: one
texture serves eight views, so a per-target owner has nowhere to live in a single atlas.
`tools/atlas_from_aovs.py` offers `owner` (global argmax weight) and `blend`, and that is
the complete set the asset path can hold.

So the item as written commissions a tool that exists. **The open question underneath it is
a measurement nobody has taken**, and every artifact it needs is already on disk.

## The question

E50 and `tools/flat_trace.py` established that the flat olive patch is an **ownership**
artifact: at `owner_complete_0` [490:540, 280:360], 115 olive-classified pixels split
owner 6 = 97, owner 0 = 9, owner -1 = 8, owner 7 = 1. View 0's own twin is clean there.
View 6 won at facing 0.68 against 0.60.

The target-first policy is precisely the rule that would give those pixels back to view 0.
**Nobody has read the flat classifier against a target-first still.**

## Arms — all on disk, no GPU, no cloud, no generation

| arm | artifact | policy |
|---|---|---|
| **A** anchor | `E:\AI\training\facet_E48\renders_owner_complete\owner_complete_0.png` | atlas render, global argmax. Where the class was measured and where the Director saw it. |
| **B** | `E:\AI\training\facet_E46\s3_off\tNN\independent.png` | view-independent still, global argmax |
| **C** | `E:\AI\training\facet_E46\s3_off\tNN\dependent.png` | **target-first** still, same run |

**B vs C is the one-variable comparison.** Same bundle, same code path, same target, same
flow arm; only the primary policy differs.

**A is NOT one variable against either** and must never be reported as if it were. A went
through atlas packing, island dilation, orphan fill and a Blender render; B and C are
direct image-space composites. A's role is to establish that the classifier fires where the
Director saw the defect, and to carry the population's provenance. Report it in its own row
with that caveat written next to it.

`s3_on/` (flow applied) exists too. **Out of scope** — adding it makes a 2x2 and this arc
asks one question. Name it in the report as available and untouched.

## Gates — halt and report, never improvise past one

- **Gate A — frame correspondence.** A, B and C must share frame dimensions, and the
  recorded region must land on the same body structure in each. Verify by measurement; do
  not assume it because the cams contract is shared. If the region does not correspond,
  **halt** and report what it lands on in each.
- **Gate B — the instrument reproduces its own pinned claim.** T89 pins `n == 115` and
  `owner == 6 on 97` for arm A's region. Run `flat_trace.py --selftest` and the pinned
  region count. If either fails, the instrument is not reproducing and every number after
  it is void — **halt**.
- **Gate C — B and C are one run.** Confirm from `facet_E46\s3_off\manifest.json` and
  `provenance.json` that both stills came from the same invocation with the same bundle. If
  not, **halt**.
- **Gate D — no write outside your own tree.** `E:\AI\training\facet_E52\` is yours.
  `facet_E4*` and `facet_E5*` are **read-only**; hash-check anything you read twice.

## Calibration — required before any count is reported

This repo has missed on the same family for eleven consecutive arcs, and the two newest
members are about the *instrument's own range*:

> *Compute what your instrument reads when the thing is definitely true, and when it is
> definitely false, and predict inside that interval.*

> *A threshold placed where the instrument cannot discriminate is not a threshold.*

So, before the arms:

1. **Definitely-yes population.** The classifier's own anchor region on arm A.
2. **Definitely-no population.** A region of the same still that is unambiguously not
   olive — pick one and say why you picked it. The red kilt and the blade are candidates;
   check the chroma floor law before trusting any hue-shaped reasoning.
3. State what the olive rule returns on each. **A count reported without this interval is
   not a measurement.**

Note the trap this classifier carries: **the tunic is legitimately dark green (N3)**, so a
full-frame olive count is mostly correct paint, not defect. The rule is region-scoped for a
reason. If you widen the population beyond the anchor region, say what you did to keep
correct tunic out of it, and show that you did not simply admit more of N3.

## Predictions — pre-register before you look, and disclose blindness

Write `predictions.md` in your own tree **before running the arms**, covering at minimum:

- **P1** — olive count in C at the anchor region, as an interval, against B's count.
- **P2** — what C puts *in place of* the removed pixels. A count going to zero is not the
  result; the result is whether the target's own paint is the surrounding tunic or a
  different flat. Predict the colour relationship, then measure it.
- **P3** — how many of the 8 targets show the same direction as target 0. State plainly
  which side of this your evidence can close: *this target's stills disagree* is decisive
  about that target; *they agree* does not poll the region's cause.

Each prediction states its band **and** what would falsify it. A hypothesis with no
prediction cannot be wrong.

## Terminus — the sheet, not the number

The cheapest diagnostic in this repo is the comparison sheet, and it decides this arc.
Build, at the **Director's zoom, defects first**:

- per target, the anchor region as **B | C** side by side, native pixels, no downscale
- the reference twin for that view beside them where one exists
  (`E:\AI\training\facet_E08\ARMB\twins`)
- arm A's same region on the target-0 sheet only, labelled as the not-one-variable row

Reuse `tools/evidence.py` and `tools/s3_sheet_regions.json` rather than writing an eighth
sheet builder — that is what the diagnostic layer was built for last session. If neither
fits, say what did not fit before you write a new one.

## Rules that bind this seat

1. **Never judge whether output is good.** No *verified, shipped, works, decisive,
   validated, proven*. Measurements and sheets; the Director judges.
2. **State a prediction before you look**, and disclose whether it was blind.
3. **Stop at every gate.** Do not change a parameter and re-run.
4. **Do not write to the memory store.** Do not commit; leave the change-set uncommitted
   for the advisor's fold.
5. **A negative result is a full success.** If target-first carries the flat class
   unchanged, say so plainly and stop.
6. **`handoff.md` first, kept current.** Two executor transcripts were lost inside E38's
   first day; on-disk state is the record.
7. **Do not delegate your own core measurement to a child agent.**
8. Gates `raise`; never a bare `assert`. Tests ride the commit — if you add or change tool
   code, its tests land in the same change-set. Next free test file is **t92**.
9. **Read every listing complete.** No `head`, `tail`, `Select-Object -Last` on anything
   that decides a number.
10. Absolute python: `E:\AI-Models\trellis2-env\Scripts\python.exe`. `pytest` needs
    `--basetemp=<scratch>` on this rig. `argparse` eats leading minus signs — use
    `--flag=-30`. Scripts create their own output directories.

## Out of scope

Twin regeneration. Any cloud or GPU generation — **this arc spends nothing**. The `s3_on/`
flow arm. The atlas path and `atlas_from_aovs.py`. The canon build-out. The
compound-occupant question (that is the advisor's, and it needs the Director's word on a
spend). Repairing anything — this arc measures.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every input is named by absolute path and both arms come from one recorded E46 invocation; the seat must cite `manifest.json`/`provenance.json` for the arms and `flat_trace.py`'s selftest for the instrument. Scored 2 not 3 because this dispatch does not pin the executor's own model/prompt hash into the arc's manifest. |
| ANDON_AUTHORITY | 3 | Four gates, each with a halt condition and a report obligation; Gate B halts on the instrument failing its own pinned claim, which is the direction that voids every downstream number. |
| NAMED_COMPENSATORS | 3 | The only writes are under `E:\AI\training\facet_E52\` plus this repo's report file. Compensator is delete-the-tree; owner is the advisor. No irreversible call exists in this arc — no publish, no push, no generation. |
| DECOMPOSE_BY_SECRETS | 2 | Classifier, arm runner, calibration populations and sheet builder are separable and the seat is told to reuse `evidence.py` rather than fuse them. Scored 2 because this spec does not name the module boundary; the seat chooses it. |
| UNCERTAINTY_GATED_HUMANS | 3 | The terminus is a sheet for the Director's eye, not a pass condition — deliberately, per the *suspend rather than invent one* precedent. The one decision escalated (the generation spend) is escalated because it is his money, not because the seat is unsure. |
| EXTERNAL_VERIFIER | 2 | The instrument (`flat_trace.py`) was written by a different seat than this dispatch, is pinned by T89, and is invoked unmodified. Scored 2 not 3 because no second, differently-sourced computation over the same pixels is required here; if the seat has budget, an independent re-derivation of the olive rule is the upgrade. |

**No pass condition, by design.** No calibrated threshold exists for "how much of the flat
class must disappear", and inventing one while looking at the arms is retuning however
principled the reasoning. Precedent: `project_twins`' suspended `seen.mean() > 0.30`.
Report numerator and denominator separately and let the Director's eye rule.
