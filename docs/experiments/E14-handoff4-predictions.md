# E14 handoff 4 — blind predictions, committed BEFORE any submission

**Executor session, 2026-08-07.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 18b/18f;
dispatched at [E14-executor-kickoff.md](E14-executor-kickoff.md) "Session handoff 4".

**Blind.** Nothing at seed 770701 exists on views 1, 3, 5 or 7 — no image, no measurement, no
partial. Everything below is reasoned from artifacts already in the record: the Task 2 twin set
(all eight at 770700), the accepted pair (view 0 at 770700, view 1 at 770701), and the pair's
rejected view-1 roll at 770700. The four graphs are not built yet.

Written and committed first so it can be scored rather than rationalised.

---

## 0. What I checked before predicting anything (the inherited-claim rule)

The dispatch asserts "stems, controls, recipe all unchanged" and makes the canny anchor row a
HALT. Both were verified against source before any prediction was written, because a prediction
built on a drifted input is not a prediction about the seed.

| claim | check | result |
|---|---|---|
| the eight profile renders are the Task-2 renders | SHA-256 + byte length | **unchanged** — view 0 is 243,196 B / `3E173A21D8A7AC02`, the digits the Task 2 report recorded |
| the controls are the Task-2 controls | re-derived all eight from the renders through `restylize_views.py --profile prop.json --emit-only` into a scratch dir, then compared **bytes and pixels** against the copies whose uploads are being reused | **all sixteen artifacts (8 controls + 8 masks) byte-identical AND pixel-identical** |
| the canny anchor row | the re-derivation's own printed counts against the recorded row | **exact on all eight**: 8,695 / 8,230 / 5,580 / 8,400 / 9,509 / 8,508 / 5,230 / 7,870 |

No drift. No HALT. The bytes-are-not-pixels law is honoured in the direction it points: bytes
agreed *and* pixels agreed, so neither reading rests on the other.

## 0b. A confound in the ruling's own seed evidence, named before it can be used as an excuse

Ruling 18b rests on "770701 clears view 1" — the accepted pair's re-roll. **That artifact was
generated from twin-prompts v1** (five-element stems, ten terms, *no* `gold collar rings`);
Ruling 13b says so explicitly and the v2 fixture repeats it. **This dispatch generates view 1
at 770701 from v2** (eleven terms, rings included). So against the pair's accepted artifact the
run moves **two** things, not one: the seed relative to the twin set, and the rings term
relative to the pair.

It is not a reason to change anything — v2 is the ruled fixture and the dispatch pins it — and
Ruling 13a's measurement is the mitigation: at 770700 the rings term changed the view-1 outcome
**not at all** (v1 sprawled, v2 sprawled at 95.5%). But *inert at a seed that sprawls* does not
prove *inert at a seed that does not*, and the rings term is a second gold noun-phrase, which is
the 12e family-pressure direction. **This is the specific way P1 can fail on view 1**, and it is
stated here rather than after the result.

Views 3, 5 and 7 have never been generated at 770701 in any stem version. They are the genuinely
new draws.

---

## 1. P1 — per-diagonal sprawl outcome at 770701

**Prediction: all four land iron. 0 of 4 sprawl.**

Per view, in the gold watch's own verdict vocabulary (`goldwatch`: FIRES > 20%, trace 3–20%,
clean <= 3%):

| view | yaw | predicted verdict | predicted gold % |
|---|---|---|---|
| 1 | 45 | clean | <= 3% |
| 3 | 135 | clean | <= 3% |
| 5 | 225 | clean | <= 3% |
| 7 | 315 | clean | <= 3% |

with the allowance that **one** of the four may land "trace" (3–20%); I will score a trace as a
partial miss, not as a held prediction.

Supporting numbers, so this is falsifiable on more than a verdict word: I predict the
`above C* 12` arm count falls to the **150–700** band the clean face-ons occupy (304 / 340 at
770700), not the 2,339–2,392 band the sprawled diagonals occupied, and gold px **under 150**.

**Why.** Within view 1 there is a matched comparison already in the record: same control, same
render (byte-identical, verified this session), 770700 sprawls and 770701 lands iron and was
accepted. Geometry is fixed inside a view, so the sprawl cannot be *purely* geometric — the seed
flipped it once. And the four diagonals move together: at 770700 they landed 95.5 / 96.0 / 93.5 /
93.3 %, a 2.7-point spread across four separate views, with IoUs inside 0.010 of each other. The
initial noise tensor is identical across views at a fixed seed; the diagonals present the same
foreshortened crossguard mass; so they are four highly correlated draws, not four independent
ones.

**Therefore the outcome I expect is all-four-alike.** The second most likely single outcome is
**all four sprawl** (the correlated-draw model with a high base rate, and the reading that
Ruling 18b generalised from n = 1). A split — 2/2 or 3/1 — I consider the *least* likely shape,
under 20%, precisely because of the 2.7-point agreement at 770700.

**The reading rule, pre-stated so the branch is not decided after seeing the number.** A FIRES
verdict on any diagonal is a sprawl and halts the dispatch. A trace verdict is ambiguous by
construction and will be reported as ambiguous, with the 4x crop, and resolved by the eye against
the pre-registered occupancy rule — gold occupying L2's quillon arms is a sprawl at any
percentage; scattered warm speckle at a material boundary is not. The eye clause is the
authority (Ruling 17d); the number is its evidence.

## 2. P2 — the IoU range the re-rolls land in

**Prediction: all four in 0.92–0.96 at tolerance 0.06; within-set spread <= 0.02; every bbox
check `ok` with ratios in 0.98–1.05; mirror deltas (v1 vs v5, v3 vs v7) <= 0.010.**

Baseline: the same four views at 770700 measured 0.9359 / 0.9453 / 0.9451 / 0.9461, bbox 1.00x,
mirror deltas 0.0092 and 0.0007. The control holds form, and nothing about a seed change touches
pose on a view whose control is strong — the pose failures were views 2 and 6, on 5,580 /
5,230-px controls, and neither is in this dispatch.

**And the prediction that matters more than the range: IoU is blind to what this dispatch tests.**
The 770700 sprawl painted gold *on* the crossguard, inside the silhouette — an occupancy failure,
not a registration one — and view 1 scored 0.9359 while 95.5% gold. So a sprawled re-roll and an
iron one will both land in this band. **If the IoU numbers are read as evidence for the branch
either way, that is the error.** No bound is derived here regardless (Ruling 18d).

## 3. P3 — deep-share behaviour

**Prediction: 0 of 4 flag. All four stay in the recorded baseline class.**

Per view: deep share between **0.02% and 0.40%**, largest connected component **under 40 px**,
row span reaching **0.85 or lower on the bottom edge**.

Baseline class (the accepted pair): 144 px = 0.160%, unconcentrated, rows 0.13–0.91. The same
four views at 770700: 0.292% / 0.027% / 0.155% / 0.045%, CCs 14 / 4 / 22 / 7, all reaching 0.91.
The diagnostic's two flags at Task 2 were views 2 and 6 — both pose failures, both outside this
dispatch. A seed change with an identical control has no mechanism I can name for driving an
interior backdrop-family arrival, so I predict the diagnostic stays quiet.

**What would falsify it usefully:** a deep AND concentrated population on a view whose pose is
fine would mean the 17c reading condition fires on something that is not a phantom crossguard —
new information about the diagnostic, not just about the twin.

## 4. P4 — the gem (L5)

**Prediction: at least one of the four re-rolls shows the gem reading magenta-purple rather than
garnet, and view 1 is the most likely one.** Stated numerically: the above-floor body hue median
of the pommel gem sits **above 290 deg** on at least 1 of the 4.

**This is a deliberate stake against the Task 2 outcome, and here is why.** Task 2 measured 0 of
8 drifts at 770700 and Ruling 17e recorded the spread as *narrowed*. But the one artifact this
route has ever produced at **770701 on a diagonal** — the accepted pair's view-1 re-roll — is
exactly the artifact whose gem read magenta-purple, median hue 303.9, 37% magenta, and that
instability is what forced the wine band to a 60-degree span. Moving four diagonals onto that
seed is the first chance to see whether the drift travels with the seed or was a stem-v1
accident.

Confidence: **low-to-moderate, near even.** The alternative I expect if I am wrong is the clean
one — 0 of 4, reproducing Task 2's narrowing — which would say the drift belonged to the v1 stem
or to that single draw, not to 770701.

L5 is below any area floor by construction (the D8 lesson) so **no gate is armed on this** either
way; it is reported at the 4x hilt crop with the hue measured beside it.

## 5. P5 — cost

**Prediction: `estimate_credits` returns 0 credits — "no paid API nodes" — on all four
submissions**, as it did on all ten at Task 2 and all three at Task 4. Quoted per submission
either way.

## 6. P6 — which exit

**Prediction: the first exit.** All four land iron, the set completes at seven accepted twins
(0, 1, 3, 4, 5, 6, 7) with view 2 excluded per Ruling 18c, and the dispatch halts with the set
staged for the advisor's eye and then the Director's.

If the second exit fires instead, that is Ruling 18b falsified on its own pre-registered branch,
and per the dispatch's calibration paragraph it is the measurement working rather than a failed
run. No third roll on anything.

---

## Amendment 1 (2026-08-07, before any submission) — reading the halt clause

The dispatch says the task is four submissions, and its second exit says *"HALT IMMEDIATELY —
no further submissions on any view, not 770702, nothing."* Read in sequence those two could
conflict: if view 1 sprawled, does the halt forbid submitting 3, 5 and 7?

**Decided now, before any output exists, because deciding it after would make the design
outcome-dependent: all four are submitted.** Grounds, in order:

1. Ruling 18b authorises exactly one re-roll per diagonal — four, and the dispatch's task
   section names them as the unit of work. All four are pre-registered and pre-authorised.
2. The halt sentence *enumerates escalation*: "not 770702, nothing." It bans a third roll and
   any view outside the four, which is the thing Ruling 18b bounds.
3. The exit's own instruction is *"Report what landed and what sprawled with the quantified
   watch"* — a mixed outcome is anticipated and reportable, which requires all four measured.
4. Stopping early would make the number of measurements a function of the result. The ruling
   needs the diagonal class characterised at this seed either way; a truncated set answers a
   smaller question than the one that was asked.

What the halt does forbid, and is honoured absolutely: **no third roll on any view, no 770702,
no other seed, no other view, and no disposition made here.** The four graphs and their
measurements go to the ruling exactly as they land.

---

## Standards compliance (this predictions file)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Every prediction is numeric with its instrument and threshold named (the gold watch's own 3% / 20% verdicts, IoU at tolerance 0.06, deep > 2 px, gem hue above the 12.0 floor); the pre-flight table records the exact check that produced each "unchanged" |
| ANDON_AUTHORITY | **3** | The branch reading rule is stated **before** the numbers exist, including the ambiguous case (trace), so the halt cannot be tuned after the fact |
| NAMED_COMPENSATORS | **3** | This file creates nothing irreversible; it is committed before spend so the record cannot be reordered |
| DECOMPOSE_BY_SECRETS | **2** | The one variable is the seed — verified by re-deriving the controls rather than asserting them. Not 3: section 0b records that against the *pair's* accepted artifact a second thing moves (the rings term). That is the fixture's decided state and not mine to change, but it is a second difference and it is named |
| UNCERTAINTY_GATED_HUMANS | **3** | P1 and P4 both carry the alternative outcome and the reasoning that would make it right; P2 states in advance that the metric a reader will reach for cannot answer the question |
| EXTERNAL_VERIFIER | **2** | The pre-flight checked the controls by re-derivation through the tool rather than by trusting its log, and by pixels as well as bytes. `skip:` on a second model, per precedent |
