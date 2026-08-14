# E35 arm slate — executor blind bands

**Registered 2026-08-14, after the spec was written and BEFORE any arm was emitted,
submitted, or measured.** Zero of the slate's jobs had fired when this file was pushed.

---

## Blindness limit, declared

**Not blind to:** the view-1 / seed-770700 baseline this slate is graded against — pale area
**278**, pale L\*-rise **4.97**, dark twin census **16** components / **157 px²**, register
C\* **23.77**, reg-IoU **0.9372**; the clay init's head at **L\* 76.43 / C\* 1.12**; R2-c's
measured direction (weakening cn *raises* pale, +235% and +339%); the 2b register continuum
(C\* 10.00 / 3.91 / 1.89) and the healthy cluster (22.40 / 23.77 / 24.29); the seed grading
from R2-a. All of it is my own prior work in this arc.

**Also not blind to the design** — I wrote the spec, including (d)'s selection rule. That is
not a defect here (the rule is pre-registered precisely so it cannot be chosen later), but it
is a disclosure: I am predicting the behaviour of a construction I authored, and an author
over-rates his own construction. Where that bites hardest is arm (c), and I say so below.

**Blind to:** every arm's outcome. No payload emitted, no depth map rendered, no job
submitted, nothing measured. Also blind to whether the Qwen union accepts a depth hint at
all — the enumeration that could settle it has not been run.

---

## What one counted thing IS, before any number

**A SPECK** = one connected component surviving `twin_despeckle.py --mode census` at its
defaults (`blob_max_px2 36`, `dark_dl 12.0`, `de_min 8.0`, `chroma_floor 8.0`, `window 15`)
inside the view's geometry mask. Dark-chromatic *relative to its own local register*, at or
below 36 px², not part of a larger same-colour structure. **Not** "a dark pixel," **not** "a
near-black pixel" — those are different populations with different magnitudes.

**A TWIN CENSUS** is that count on the generated 352×1024 twin. A **FLAT CENSUS** is the same
count on a Blender `--flat` render of the projected asset. Different objects, different
magnitudes (view-1 baseline: twin **16**, flat **102**). **Every band below is a TWIN
census.**

**PALE AREA** = summed area of components of head-region figure pixels sitting **L\* ≥ 6.0
above a 31 px local median**, each ≥ 25 px². It is a **local excursion**, not global
lightness — an image can get uniformly lighter and its pale area *fall*. **PALE L\*-RISE** =
how far above that local median those components sit.

**THE REGION** is the head, `HEAD = slice(60, 220)` of a 352×1024 frame. **One view. Not the
eight-view mean** — R2-a's 770700 row (734.5 / 11.67 / 170.4) is a different population and
is not a baseline for anything here.

---

## The bands

### Arm (a) — `euler_ancestral`

An ancestral sampler re-injects noise each step, so the trajectory carries more of its own
entropy and less of the init.

- **A1 — pale area FALLS, band 120–260.** By R2-c's mechanism: pale is init surviving where
  the sampler is least anchored, and injected noise is a second thing competing with the
  init for those regions. *Falsifier: ≥ 278, i.e. the init survives ancestral noise as well
  as it survives deterministic euler.*
- **A2 — dark census RISES slightly, band 14–28.** Extra high-frequency variance makes more
  discrete small blobs, and consult #1 ranked the sampler as something that "may sharpen what
  exists." I expect this arm to trade the classes the wrong way round.
- **A3 — register C\* holds, band 21.0–24.5.** Ancestral at 20 steps may under-converge a
  little; nothing here attacks chroma directly.

### Arm (b) — `soft studio light` → `flat even lighting`

- **B1 — dark census FALLS, band 6–14.** This is the arm's whole thesis: the dark class is
  testimony-ruled baked AO/shading painting, and this is the one lever aimed at shading
  rather than at the exposure axis.
- **B2 — pale area roughly UNCHANGED, band 200–400.** The pale class is init-driven, and this
  lever does not touch the init or the conditioning.
- **B3 — register C\* holds but moves more than any other arm, band 19.0–24.5.** It swaps one
  of the *three* R3 register terms; "studio" plausibly carried warmth that "flat even" does
  not.
- **⚠ B4 — CONFOUND, registered before measuring: if B1 and B2 both land, read B2 twice.**
  A flatter render has less local variation, and the pale measure is a *local* excursion —
  R2-c's PC3 already caught this shape on the denoise ladder. So a pale-area fall on this arm
  can mean "the wash went away" or "the instrument's local contrast went away," and the two
  are not distinguishable from the number alone. If pale falls below 200 here, the L\*-rise
  and the sheet decide, not the area.

### Arm (c) — depth hint

**The clauses, separately, then the join** — the join tracks the rarest clause, and here the
rarest one is the one I cannot measure without spending the job.

| clause | my odds | why |
|---|---|---|
| C-i — the Qwen InstantX union **accepts a depth hint at all** and returns a coherent figure | **~0.6** | the union is *described* as multi-modal and ComfyUI loads it with no type node, which is what auto-detection looks like — but that is testimony I have not resolved, and the enumeration is still pending |
| C-ii — given C-i, depth anchors the smooth regions canny leaves empty | ~0.85 | R2-c measured anchoring as the term that suppresses pale; depth's signal is exactly where canny's is not |
| C-iii — the register holds | ~0.9 | the prompt and denoise are untouched |
| **join** | **~0.46** | **this is the coin-flip arm, and its failure mode is at the front, not the back** |

- **C1 — pale area FALLS hardest of the three arms, band 60–220** *(conditional on C-i)*.
- **C2 — dark census falls, band 8–18** *(conditional on C-i)* — depth gives the sampler
  interior structure to paint instead of hallucinating speckle into a smooth field.
- **C3 — register C\* holds, band 22.0–25.0.**
- **C4 — if C-i fails, it fails LOUDLY, not subtly.** A union that cannot read the hint gives
  the sampler a control that constrains nothing, and this repo has that signature recorded:
  material and identity change, not a hue shift — gold plates gone, boots to fur. **If the
  twin comes back a different man, the diagnosis is C-i, not C-ii.**

### Arm (d) — the branch

Applying the pre-registered rule to my own bands' midpoints (a ≈ +0.07, b ≈ +0.33,
c ≈ +0.69):

- **D1 — branch 3 fires: |C| ≥ 2, and the pair is (c) + (b).** Registered as a call.
- **D2 — arm (a) is the marginal one.** Its score straddles zero because I expect it to trade
  the classes against each other, which is what the signed score is built to punish.
- **D3 — no arm is register-excluded.** I expect all three above C\* 19, nowhere near the
  10.00 bound.
- *Falsifiers, all live:* C-i fails and (c) scores negative, putting the pair at (b) + (a) —
  or, if (a) also scores negative, **branch 4 and (d) does not fire at all**, which the rule
  permits and which is a complete result.

---

## The one I most expect to be wrong about

**A2 and B4.** A2 predicts a lever makes a class *worse*, which is the least comfortable
prediction here and the easiest to have written softly; I have written it hard so it can
miss. B4 is not a band at all — it is a warning that one of my own numbers may not mean what
its name says, registered now so it cannot be reached for later as an explanation.

Nine consecutive arcs in this repo have missed on the unit/population family. The two places
this file could still be carrying that defect: the pale measure's *local* denominator (B4),
and C-i — **a property I predicted the behaviour of without checking it is defined for the
member in question.**
