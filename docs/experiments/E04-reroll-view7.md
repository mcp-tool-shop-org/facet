# E04 — A23 re-roll of view 7: the waterline is gone, and the row changed. HALT for the ruling.

**Executor session, 2026-08-04, after Rulings 18 and 19.** One re-roll, as written. **The
waterline band is decisively eliminated. The replacement row is not the same class — and it is
not in family either.** Nothing projected.

**Seed 770701** — the deterministic increment from 770700, stated so it reads as arithmetic
rather than a choice. Every other field byte-matched; the diff against the rejected run is
exactly two entries, `KSampler.seed` and `SaveImage.filename_prefix`, and both uploads are the
same content-addressed objects. Workflow saved before submission and link-checked.
**0 credits. Re-roll 1 of the 1 allowed — spent.**

**The rejected artifact is preserved** at `twins/twin_7_REJECTED_seed770700.png`
(sha `77D02993…`), per A23 and now also as E10's founding exemplar per Ruling 19.

---

## The A23 question is answered: NO

| view 7 | off-palette | % | largest CC | CC red | IoU | key margin | red < 40° | **waterline test** |
|---|---|---|---|---|---|---|---|---|
| **REJECTED** 770700 | 5,613 | 1.74% | 2,002 | 0.0% | 0.92990 | 1.118% | 1,807 | **2,272 px** |
| **RE-ROLL** 770701 | 13,796 | 4.28% | **10,866** | 25.8% | 0.93017 | 1.498% | 3,106 | **0 px** |

**Waterline test** — chroma-bearing pixels in the lower 7% of the figure at hue 240–273, the
band the rejected twin painted: **2,272 px → 0 px.** The blue-grey band across the hull's foot
is not present at any scale. Registration is unchanged (0.92990 → 0.93017).

**And the replacement component is a declared material.** Its median is rgb(47,22,13),
**h 43.1, C\* 15.5, L\* 10.7** — the dark-tarred-wood signature, sitting just outside the warm
band's 50° lower edge. Compare the rejected component: rgb(56,77,97), h 262.6, C\* 14.4, a
blue-grey at the waterline that matched nothing declared.

Decomposed against the whole set, using the tar signature (C\* 12–20, L\* < 20, hue 40–50):

| view | tar-signature off-palette px | share of that view's largest CC |
|---|---|---|
| 0 | 574 | 0.7% |
| 1 | 274 | 0.0% |
| 2 | 124 | 1.6% |
| 3 | 537 | 0.0% |
| 4 | 356 | 62.1% |
| 5 | 163 | 7.8% |
| 6 | 2,575 | 89.2% |
| **7 re-roll** | **9,289** | **69.5%** |
| 7 rejected | 1,040 | **0.0%** — its component was the waterline, not tar |

**So the re-roll traded a 2,002 px unnamed blue-grey band for a 9,289 px expansion of a
declared one.** It is the same class as views 4 and 6 — Ruling 18's *"two declared tar at the
band's 50° edge"* — at 3.6× view 6's amount.

## Why I am not taking the "projection proceeds" branch myself

Ruling 18 pre-stated: *a clean row in family with the other seven → projection proceeds
directly; the same class again → that's the result.*

**It is not the same class** — that much is measured and unambiguous. But **it is not a clean
row in family either**, on the two axes that carry the comparison:

- largest CC **10,866 px** against a previous maximum of 4,562 (view 0) — **2.4×**
- tar-signature off-palette **9,289 px** against a previous maximum of 2,575 (view 6) — **3.6×**

And the decisive point: **Ruling 17 accepted *the eight as measured*.** View 7's measured row
has changed — off-palette 1.74% → 4.28%, largest CC 2,002 → 10,866. The set that was accepted
is not the set that would be projected. Whether the replacement row is close enough to "in
family" to spend that acceptance is an outcome judgment, and outcome judgments are not mine.

**This needs one line, not an investigation.** The A23 answer is NO; the class question is
answered; only the magnitude is open.

## Two things worth having beside the ruling

**The re-roll is the cheapest evidence yet that the waterline was a roll, not a tendency.** Same
prompt, same control, same init latent, same recipe, one seed apart — 2,272 px of water became
0. That is the per-view-roll signature again (E08's blue sleeve, G7's port-vs-starboard red),
now on an *environment* element, and it is the fact E10's spec most needs: **the model paints
implied water sometimes, not reliably** — which is precisely why a deliberate layer beats
hoping the base coat produces one.

**The rejected artifact is now doubly load-bearing** — A23's evidentiary record and, per Ruling
19, the first measured exemplar of spontaneous environment contact: 2,002 px, h 262.6,
C\* 14.4, L\* 31.7, bbox x 398–686 / y 896–939 against a figure ending at 939, i.e. hugging the
hull's foot across 288 px of its length. Fully characterised, on disk, reproducible from a
recorded seed.

## What was not done

No projection, no atlas, no second re-roll, no threshold moved, no fixture or profile edit.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Seed stated as an increment before the run; the two-field diff enumerated in code; same content-addressed uploads; workflow saved before submission |
| ANDON_AUTHORITY | **3** | The re-roll allowance is spent and recorded as spent; no second roll considered; the branch that would let me proceed is declined because its condition is not met on the measurement |
| NAMED_COMPENSATORS | **3** | 0 credits; rejected artifact preserved under an explicit name with its sha; all writes new files |
| DECOMPOSE_BY_SECRETS | **3** | The tar-signature decomposition is built from the fixture's declared materials, not from the defect |
| UNCERTAINTY_GATED_HUMANS | **3** | The A23 question is answered plainly so the remaining ruling is one line; the magnitude question is posed without a recommendation |
| EXTERNAL_VERIFIER | **2** | The waterline test and the tar-signature decomposition are two independent questions that could each have gone the other way; both were built before the re-roll's numbers were read. `skip:` on a second model |
