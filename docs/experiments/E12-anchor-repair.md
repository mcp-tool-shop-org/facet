# E12 Ruling 9a — the anchor's operand repair, and both subjects' digits

**Executor session, 2026-08-06.** `e04_frame_agree.py` conformed to `silhouette_masks`' own
arithmetic per Ruling 9a. **The bound did not move and no tolerance was introduced.** Every
run below is CPU raycast; watchdog alive throughout (heartbeat age 2.1 s at the start of the
leg), reported per the standing rule.

---

## 1. What was conformed, and what was deliberately not

Three incidental operands differed between the replica and the source it checks. All three
are now the source's:

| operand | `silhouette_masks.py` (the source) | `e04_frame_agree.py` before | now |
|---|---|---|---|
| vertex frame | `[x,-z,y] / max\|v\| * 0.5`, `vmax` taken on the **pre-remap** vertices | unnormalised | conformed, in the source's line order |
| up vector | `cross(rgt, look) / (norm + 1e-12)` → **0.999999999999** | hardcoded `(0,0,1)` | conformed, `+ 1e-12` reproduced rather than simplified |
| ray-back | `- look * 2.0` | `- look * radius` (2.9–3.0 depending on subject) | conformed to `2.0` |

**Not conformed, on purpose:** the framing derivation is still written in **`turn_render`'s**
form (`ortho_scale` on the fitted axis, `sensor_fit` VERTICAL/HORIZONTAL branch), because
that is the convention the anchor exists to test.

**The honest limit, written into the tool's docstring rather than left implicit.** Those two
derivations were always the *same formula on differently-named variables*, so once the frames
agree they are bit-identical arithmetic and **this tool can no longer catch a shared bug in
that formula.** What it still catches, and what it was built for:

- the two tools being **given different flags** — aspect, fit-axis, margin, step. This is the
  galleon's 4.68% failure in its current form: the derivations only move together because
  both take `--fit-axis`, and nothing else asserts a caller passed the same value to each.
- a **stale or foreign mask file** — wrong tag, wrong mesh, wrong frame. The replica
  re-derives from the GLB; the mask is read off disk.
- `turn_render`'s height/width → sensor_fit branch, encoded explicitly rather than inherited.

**The legacy construction is still computed and printed every run, ungated.** It keeps the
repair auditable and keeps the float-ordering class visible instead of absorbed. Gating on it
would be gating on a proxy for the question.

## 2. Both subjects' digits — and the ship's record moves

Run at each subject's **recorded anchor operands**, not at today's profile values, so the
numbers are comparable to what is on the record.

| subject | frame | fit-axis | view | E04 record | **legacy now** | **corrected now** |
|---|---|---|---|---|---|---|
| galleon 00006 | 1066 × 1024 | width | **1** | **1 px** | **1 px** | **0 px** |
| galleon 00006 | 1066 × 1024 | width | 7 | 0 px | 0 px | **0 px** |
| W3 (control) | 752 × 1024 | height | 0 | 0 px | 0 px | **0 px** |
| W3 (control) | 752 × 1024 | height | 4 | 0 px | 0 px | **0 px** |
| **beast 00003** | 1792 × 1024 | width | 1 | — | 0 px | **0 px** |
| **beast 00003** | 1792 × 1024 | width | **5** | — | **1 px** | **0 px** |

**Every recorded digit reproduces exactly under the legacy construction** — galleon view 1 at
hit 321,219 against mask 321,218, byte-matching `E04-step0-anchor1c.md`. That is what makes
this a confined operand repair rather than a change of unknown extent: the only rows that
moved are the two the repair was aimed at.

**The consumer-grep paid.** The ship's 1 px on view 1 **is the same float class** — advisor's
suspicion, now measured. E04 Ruling 11 adjudicated it a PASS under the pre-registered float
reading; under the corrected construction it is a **clean 0**, and the mechanism is identified
rather than adjudicated. The ship's record is the advisor's to annotate.

**The control still returns exactly 0 in both constructions**, on both views, at fit-axis
height. Two things follow: the repair did not break the height branch, and the instrument's
zero is still a zero rather than a tolerance — the property `E04-step0-anchor1c.md` called
"the control matters most".

## 3. Scale factors, recorded — they are subject-specific and none is 1.0

| subject | `max\|v\|` | scale `0.5 / max\|v\|` |
|---|---|---|
| beast | 0.500908494 | 0.998186307466 |
| galleon | 0.485136330 | **1.030638129839** |
| W3 | 0.501373470 | 0.997260585348 |

The galleon's is **3.06% off unity** — an order of magnitude further from 1.0 than the
beast's, and it still produced only one disagreeing pixel. The size of the scale error is not
what governs how many pixels flip; what governs it is how many rim rays happen to sit within
float32 rounding of a triangle edge. That is why this class is invisible until a subject with
a long, finely-scalloped rim arrives, and why it showed up on the dragon rather than on either
predecessor.

## 4. The pre-stated branch

Ruling 9a: *corrected gate returns 0 px on every checked view of the beast → proceed to
control construction; anything else → halt again.*

**Both beast views returned 0 px. Proceeding.**

## 5. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every run logged with its operands to `E12_pair/anchor_rerun.log`; each subject run at its own recorded anchor operands; the scale factor printed per run |
| ANDON_AUTHORITY | 3 | The bound stayed 0 and no tolerance was added; the branch was pre-stated by the advisor before the re-run and is quoted above; the legacy number is reported but cannot gate |
| NAMED_COMPENSATORS | 3 | One tool edited, additively (the legacy path is retained, not deleted); undo = `git revert`. No spend, nothing irreversible |
| DECOMPOSE_BY_SECRETS | 3 | The repair touches only the incidental numerics; the framing derivation — the thing that varies with the subject and is the anchor's subject — stays in `turn_render`'s form |
| UNCERTAINTY_GATED_HUMANS | 3 | The reduction in the instrument's independence is enumerated in its own docstring rather than left for a future session to discover; the ship's record change is handed up, not made here |
| EXTERNAL_VERIFIER | 2 | The legacy construction reproducing all four recorded digits is the verification that the change is confined. Marked 2, not 3, because the repair **cost** independence: the two derivations are now bit-identical arithmetic and a shared formula bug is no longer detectable here. Stated as a limit, not a score |
