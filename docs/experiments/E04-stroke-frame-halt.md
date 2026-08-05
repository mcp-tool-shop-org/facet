# E04 stage 2 — HALT before stroke 1: `texpass_iter emit` renders the ship in the CHARACTER's frame

**Executor session, 2026-08-05, after Ruling 24 cleared the strokes to fly.** Ruling 24's
guard landed first and is complete. Setting up the run, the tool's own `selftest` — which
`texpass_iter.py`'s header says to run before any real brush — **emitted at 752×1024
fit-axis height**, the character's convention, not the 1072×1024 width-fit frame the twins,
the atlas and the whole stroke derivation were built in.

**Four of the six ruled stroke cameras clip the ship at that frame.** No stroke has flown.
Nothing generated, nothing submitted, no credits. The state directory is byte-identical to
the stage-1 seed and no job directory was written into it.

---

## How it surfaced

The selftest is a passing test — write-head lossless on styled texels, holes strictly
shrink, 31,581 committed. It passed. What did not match was the *frame*:

```
[emit] E04_stroke/selftest_state/selftest_y+300_e+00: 267,720 figure px
cam.json      W,H = 752 1024    h_ext 0.84860   v_ext 1.15554
the derivation      1072 1024    h_ext 1.20238   v_ext 1.14854
```

`e04_stroke_cameras.py` modelled 271,165 figure px at that camera against emit's 267,720 —
1.29% apart, which is what sent me to the frame rather than past it. A model that agrees to
1% is easy to call agreement; it was the *direction* that mattered, because a pure raycast
of the same geometry through the same grid should agree exactly.

## The cause, and it is a profile omission with a live consumer

`ship.json`'s `texpass_iter.py` block carries four keys — `thin-extent`, `facing-min`,
`edge-dist`, `mask-dilate` — and **neither `aspect` nor `fit-axis`**. So `emit` fell back to
its own defaults, which are the character's `752,1024` and `height`.

| profile | tool | `aspect` | `fit-axis` |
|---|---|---|---|
| ship.json | `verify/turn_render.py` | (w/h) | **width** |
| ship.json | `silhouette_masks.py` | **1072,1024** | **width** |
| ship.json | `project_twins.py` | **1072,1024** | *tool has no such flag* |
| **ship.json** | **`texpass_iter.py`** | **ABSENT** | **ABSENT** |

`texpass_iter.py`'s own header names this exact invariant:

> ⚠ `--fit-axis` travels with it: emit derives v_ext/h_ext the way turn_render and
> silhouette_masks do, and **all three must agree** or the job frame and the mask disagree
> (Ruling 6, measured at 4.68% on a landscape frame).

Two of the three agree. The third was never written.

## The consequence, measured at every ruled camera

`emit` run at both frames on the ruled six, counting figure pixels touching each frame edge:

| stroke | frame the profile produces (752×1024, height) | the twins' frame (1072×1024, width) |
|---|---|---|
| `y+300_e+00` | 267,720 px, no clipping | 271,165 px, none |
| `y+030_e+00` | 337,677 px, **clipped L 49 / R 262** | 345,796 px, none |
| `y+150_e+00` | 336,879 px, **clipped L 219 / R 55** | 344,956 px, none |
| `y+240_e+00` | 269,472 px, no clipping | 272,997 px, none |
| `y+000_e+40` | 275,107 px, **clipped L 175 / R 320** | 295,595 px, none |
| `y+180_e+40` | 271,767 px, **clipped L 323 / R 189** | 292,066 px, none |

**Four of six clip. Zero clip at the correct frame.** Area running off the ends, measured
in the correct frame as the figure lying outside the horizontal window the character frame
covers:

| stroke | figure off-frame | share |
|---|---|---|
| `y+300_e+00` / `y+240_e+00` | 0 | 0.00% |
| `y+030_e+00` | 3,808 px | 1.10% |
| `y+150_e+00` | 3,848 px | 1.12% |
| **`y+000_e+40`** | **17,338 px** | **5.87%** |
| **`y+180_e+40`** | **17,234 px** | **5.90%** |

Nothing is lost vertically — the character frame is 0.6% *taller* in world units. **The
entire loss is off the bow and the stern**, because the frame is 29% narrower and this
subject is landscape.

**That is the worst possible place to lose 6%.** The ends are the identity-dense ends: the
fixture's **G1** gilded lion figurehead is at the bow, and **G5** gilded scrollwork on the
stern castle, **G6** the gilded spire on the stern turret and **G12** the gilded
stern-gallery railings are at the stern. Task 4c chose a bow three-quarter and a stern
three-quarter for the styled target pair *for exactly that reason*. And the two worst-hit
strokes are the deck pair, which carries 200,660 of the ruled set's texels — the largest
contribution in the whole stage.

Two consequences, and the second is worse than the first: the clipped region gets **no
paint** from that stroke, and the brush composes at denoise 1.0 against a render in which
**the ship runs off both edges of the image**. What it would compose there is not knowable
from here, and it is a different picture from the one the twins established.

## What is NOT affected

- **Everything already run stands.** `turn_render` and `silhouette_masks` carry both keys;
  `project_twins` **has no `--fit-axis` flag at all** (`grep` returns 0) and its `aspect` is
  set, so stage 1's frame was never in question. The twins, the atlas, the owner and blend
  sidecars, the hole map and the derivation are untouched.
- **The stroke derivation is unaffected** — `e04_stroke_cameras.py` takes its frame from
  `--aspect`/`--fit-axis` arguments defaulting to `1072,1024` and `width`, so every number
  in [E04-stroke-derivation.md](E04-stroke-derivation.md) and every number Ruling 24 rests
  on was computed in the correct frame. **The derivation is right and the pipeline was
  wrong**, not the other way round.
- **Ruling 24's guard is landed and complete** (`8ca1c0c`): required `--profile`, fires
  three ways with exit 1 and writes no file, character anchor byte-identical.

## THE SECOND FINDING, which is why this is a halt and not a fix

**`--coverage` is structurally blind to this, and returning 0 UNDECIDED did not mean what it
looked like it meant.**

The coverage check diffs a subject profile against **`character.json`'s per-tool keys**. And
`character.json`'s `texpass_iter.py` block carries the same four keys and **also lacks
`aspect` and `fit-axis`** — because on the character those values *are* the tool defaults, so
nobody ever wrote them down. An absent key in the reference cannot be reported as absent in
the subject.

Ruling 24 named this mechanism one level coarser: *"the coverage reference is
`character.json`'s tool blocks, and a tool with no block there inherits the character's blind
spots into the registry itself."* This is the same sentence with *tool* replaced by *key*, and
it is live rather than latent: **it let a landscape subject reach the stroke stage carrying a
portrait frame, one leg after the profile was ratified at 64 decided / 0 undecided.**

So the honest reading of that line, banked here: **`0 UNDECIDED` means every flag the
character bothered to write down is decided. It does not mean every flag that matters is.**
The registry inherits the reference subject's silences, and a value that is a *default* on the
reference subject is exactly the kind that never gets written.

## Why I did not simply add the two keys

The values are not in doubt — `1072,1024` and `width`, already decided twice in the same
profile for the other two consumers of the same convention, and mandated by the tool's own
header. It is a two-key edit.

I am halting anyway, on precedent and on scope. The previous session's **halt #3** was this
defect exactly — *"profile missing `fit-axis`; would have rendered in the un-adjudicated
mode"* — and it halted rather than self-corrected. `ship.json` is a ratified artifact that
Ruling 22 closed at 64/0 and Ruling 24 cleared to fly one message ago; editing it silently
under a "cleared to fly" would be the executor deciding that a ruled artifact was wrong,
which is not mine. And the second finding above is a statement about a **guard the advisor
owns**, which should be ruled rather than absorbed into a commit message.

## What is ready the moment it is ruled

State seeded and pristine · fixture regenerated with the ruled six-stroke `_order`
(`y+300 · y+030 · y+150 · y+240 · y+000@40 · y+180@40`) · anchoring for that exact sequence
re-simulated: **80.8 / 76.7 / 76.3 / 83.8 / 71.7 / 76.1, min 71.72%, mean 77.57%** · the
pre-flight guard passing on the ship and on the character anchor · `selftest` PASS (write-head
lossless, holes 1,963,858 → 1,932,277 on the throwaway state) · watchdog ALIVE, 1,612/32,607
MiB, 29,588 below the ceiling.

**One line either way.** If the two keys land, everything above re-runs at the correct frame
and the first stroke flies.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Both frames run through the same tool with the same geometry and the same seeded state; the comparison is emit's own `hit.png` and `cam.json`, not a model of them |
| ANDON_AUTHORITY | **3** | Halted before the first irreversible step with the evidence, rather than making a two-key edit to a ratified artifact under a clearance; the tool's own selftest was run before any brush exactly as its header instructs |
| NAMED_COMPENSATORS | **3** | Nothing to undo: the selftest and the frame comparison ran on throwaway state copies, the real state is byte-identical to the stage-1 seed and carries no job directory, no cloud call was made |
| DECOMPOSE_BY_SECRETS | **3** | The finding *is* this standard failing at its own boundary — a subject value absent from the profile, invisible to the checker built to find exactly that, because the reference is another subject's silence |
| UNCERTAINTY_GATED_HUMANS | **3** | The fix is named and costed in one line; the reason for not applying it is stated as scope and precedent rather than doubt; the second finding is posed to the advisor because it concerns a guard the advisor owns |
| EXTERNAL_VERIFIER | **2** | The discrepancy was found by an instrument disagreeing with the tool it models — 271,165 against 267,720 — which is the derivation checking the pipeline rather than either checking itself. `skip:` on a second model |
