# E12 handoff 15 — HALT at step 0's gate: the sweep returns 8 UNDECIDED, not 0

**Executor session, 2026-08-07.** Predictions registered blind in `1304b9f`
([E12-handoff15-predictions.md](E12-handoff15-predictions.md)), git blob `38775ea`, written
before the no-LoRA path was written and before anything ran.

**No stroke ran. No generation, no credit, nothing irreversible.** Task 0's capability half is
delivered and anchored; Task 0's gate fired and Tasks 1–3 did not start.

---

## The halt, in one line

`e04_registry_sweep.py --profile profiles/beast.json` returns **8 UNDECIDED, exit code 1**,
against the dispatch's expected 0. **Any UNDECIDED halts — that firing is the procedure**
(25g, and the dispatch says so in the same words). Certificate:
`E13_stroke/run/sweep.txt`.

```
[sweep] 83 SUBJECT-DATA flags on this route; decided 75
[sweep] 8 UNDECIDED - each of these runs this subject on the tool's own default,
[sweep] which on this route is the character's measurement:
[sweep]   project_twins.py   margin        tool default 1.204
[sweep]   texpass_brush.py   cfg           tool default 2.5
[sweep]   texpass_brush.py   cn-strength   tool default 1.0
[sweep]   texpass_brush.py   lora-w        tool default 0.75
[sweep]   texpass_brush.py   negative      tool default 'watermark, text, logo, ...'
[sweep]   texpass_brush.py   prompt        tool default 'a burly bald warrior with a long
[sweep]                                     red beard, ... holding a massive greatsword ...'
[sweep]   texpass_brush.py   seed          tool default 770700
[sweep]   texpass_brush.py   steps         tool default 20
```

### Why it fired: a block cleared in prose is not a block cleared in the registry

Ruling 25f states that `_NOT_CLEARED` clears "every key decided in this ruling" and lists the
values. The profile transcription replaced the marker string with a *narrative* one. Measured:

```
profiles/beast.json tools['texpass_brush.py'] keys:
  ['_CLEARED_BY_RULING_25', '_THE_RECIPE_NUMBERS_DO_NOT_REACH_THE_CLOUD_GRAPH']
  any {"value": ...} entries?  False
```

The block carries **no decided values at all**. Seven of the eight UNDECIDEDs are that. The
lifecycle's own words anticipated exactly this — *"Removing this marker without deciding the
keys reverts them to UNDECIDED and the coverage check fires — that firing is the procedure,
not a defect"* — and what happened is the near-miss version: the marker was removed and the
keys were decided **in prose**, which the registry cannot read.

**This is not a re-litigation of Ruling 25.** Its decisions are unambiguous and are quoted in
the block's own text: prompts = `docs/experiments/E13-brush-prompts.json` (present, four keys,
`E13-brush-1`), seed 770700, steps 20, cfg 2.5, cn_strength 1.0, lora NONE by register. What
is missing is the transcription into `{"value": …, "why": …, "from": …}` entries, and **this
dispatch forbids me to edit any fixture or profile**. It is a ruling's fold, not an executor's.

### The eighth is mine, and I own it

`project_twins.py margin` is UNDECIDED **because of my own handoff-13 change.** I exposed
`--margin` as a flag (it had been the literal `1.204` inside the frame derivation), which
created a registry slot that did not exist before. Ruling 24a then transcribed `fit-axis:
width` into the profile — and only that. So on the very consumer whose framing family was the
finding, the family is now **half-pinned**:

| consumer | aspect | fit-axis | margin |
|---|---|---|---|
| turn_render | ✓ 1792,1024 | ✓ width | ✓ 1.204 |
| silhouette_masks | ✓ 1792,1024 | ✓ width | ✓ 1.204 |
| texpass_iter | ✓ 1792,1024 | ✓ width | ✓ 1.204 |
| **project_twins** | ✓ 1792,1024 | ✓ width | **absent** |

Stage 1 ran at 1.204 because that is the flag's default and the default is right — nothing
that has run is wrong. But E04 Ruling 25's law is that the family moves together, and a value
arriving by silence is the thing the registry exists to prevent. Reported, not fixed.

### Two independent guards fire, which is the design working

The sweep is not the only one. `brush_cloud_step`'s own pre-flight halts on the same fact from
inside the tool that would perform the irreversible step (E08 A32), and **writes no file**:

```
ANDON: profiles/beast.json texpass_brush.py has no decided value for 'lora-w', so the
register is undeclared and the graph cannot be built either way. A ruling decides it;
this tool does not guess.
GUARD EXIT = 1        should_not_exist.json: not created
```

Evidence: `E13_stroke/run/guard_halt.txt`.

## What IS delivered: Task 0's capability, anchored (Ruling 25e)

The gate blocks the strokes. It does not block the capability the dispatch ordered *before*
it, and that is finished and proven, so the clearing ruling can dispatch the run without
another capability round.

**`brush_cloud_step.build_graph` gains the no-LoRA path.** The loader node is omitted when the
register is NONE and `ModelSamplingAuraFlow` reads the UNET directly — the twins' construction,
and Ruling 10b's ruled wording that 0.0 "is not a weight of zero on a loaded card, it is no
card". The weight now comes from **the subject's profile**, not from `DEFAULTS`, which converts
one of the five coincidences-of-value into agreement by construction — the class fix this
file's own docstring has been asking for since E04 Ruling 24.

The pre-flight is amended to match, and it is *stronger* than before:

- check (a) drops `lora-w` from the DEFAULTS comparison, **with the reason in the code**:
  `DEFAULTS['lora_w']` no longer reaches the graph, so comparing it would fire on a correct
  build — the exact class of error this repo keeps paying for;
- new check **(b2), the inverted scan** (the restylize class): when the register is NONE the
  claim is not "the weight is 0.0", it is that **no loader node and no card string exist
  anywhere in the graph**. Asserted by walking every node and every input, plus the link
  assertion that node 6 reads `["1", 0]`. In the positive-weight direction it asserts the
  mirror image — a decided weight with no loader would be silently inert, and that now halts
  too.

### The anchor: PASS, on all six recorded graphs

`E13_stroke/run/anchor.txt`. The accepted route's stroke graphs are rebuilt from their own
recorded inputs and compared **as parsed graphs** — node sets, class types, every input and
every link — because a JSON re-dump can differ in whitespace without a value moving.

| recorded graph | nodes | result |
|---|---|---|
| `stroke_1_y+300_e+00_workflow.json` | 17 → 17 | **IDENTICAL** |
| `stroke_2_y+030_e+00_workflow.json` | 17 → 17 | **IDENTICAL** |
| `stroke_3_y+150_e+00_workflow.json` | 17 → 17 | **IDENTICAL** |
| `stroke_4_y+240_e+00_workflow.json` | 17 → 17 | **IDENTICAL** |
| `stroke_5_y+000_e+40_workflow.json` | 17 → 17 | **IDENTICAL** |
| `stroke_6_y+180_e+40_workflow.json` | 17 → 17 | **IDENTICAL** |

**The card path did not move.** And the two branches were compared against each other rather
than each described on its own: the no-LoRA graph is **16 nodes**, loader nodes NONE, card
references NONE, node 6 reading `["1", 0]`, and the symmetric difference between the two
branches is **exactly `{"5"}`** — the loader node and its one link, nothing else.

## Predictions scored so far

| # | class | verdict |
|---|---|---|
| P1a anchor holds byte-identical | CODE-READ | **held** — 6 of 6, node for node |
| P1b sweep returns 0 UNDECIDED (80/20) | DERIVED | **FALSIFIED** — 8 UNDECIDED, exit 1. The 20% branch I named ("prose is not a registry") is what happened |
| P1c no-LoRA graph is 16 nodes | CODE-READ | **held** — 16, and the branches differ by exactly node 5 |
| P2–P6 | — | **not reached**; nothing ran past the gate |

P1b is the useful one. I gave the surprise 20% and wrote down what the surprise would be:
*"the sweep may find something else undecided that nobody was tracking — `texpass_brush`'s
block was cleared by a ruling written in prose, and prose is not a registry."* That is exactly
what it found, plus one more that is mine.

## What the clearing fold needs (stated as facts, not as a proposal)

1. `texpass_brush.py`'s block needs seven `{"value": …}` entries — `seed`, `steps`, `cfg`,
   `cn-strength`, `lora-w`, `prompt`, `negative`. Ruling 25f already decided the first five;
   `prompt`/`negative` are the protective-transcription class (E04 Ruling 22) because the tool
   defaults are **W3's identity string** — the named accident class, and the sweep printed it
   in full as the value this subject would otherwise inherit.
2. `lora-w` must be **0.0** for the new path to build the no-card graph; at any positive value
   it builds the 17-node card graph, and (b2) enforces the correspondence either way.
3. `project_twins.py` needs `margin`, to close the framing family on its fourth consumer.
4. Then the sweep re-runs and the strokes are unblocked. Nothing else in this dispatch is
   affected: the prompts fixture is present and correct, the stroke set and order are ratified,
   thin-extent 0.005 is live, and the capability is anchored.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the tool was touched, with the 20% surprise branch named in advance; the anchor pins the change to six recorded graphs from the other subject; the sweep certificate and both halt logs saved to disk |
| ANDON_AUTHORITY | **3** | The gate fired and the run stopped — no stroke, no spend, no improvisation past it; **two independent guards** (the registry sweep and the tool's own pre-flight) reach the same conclusion by different routes, and the in-tool one wrote no file; the anchor gated the change before the change was used |
| NAMED_COMPENSATORS | **3** | Nothing generated or spent; the only writes are one tool edit (additive, anchored) and three evidence files under a new `E13_stroke/run/` tree; A0's state untouched |
| DECOMPOSE_BY_SECRETS | **3** | The capability is separated from the run and anchored on the OTHER subject's recorded output; the register moves from a tool constant to the subject's profile, so subject data lives in the subject's file |
| UNCERTAINTY_GATED_HUMANS | **3** | The halt routes to the ruling with the exact list of what is missing and why, and explicitly does not edit the profile to unblock itself; my own contribution to the failure is named rather than buried |
| EXTERNAL_VERIFIER | **2** | The anchor tests new code against output the old code produced, on a different subject; the sweep is an independent instrument that does not share the pre-flight's code path. `skip:` per precedent |

---

**HALTED at Task 0's gate.** The no-LoRA capability is delivered and anchored at 6/6 identical;
the sweep certificate, both halt logs and the anchor log are staged. **To the advisor's eye.**
Tasks 1–3 (the four strokes, finalize/pack, the five-column sheet) did not start and are
unblocked by a profile fold this dispatch forbids me to make. Gate 1 waits.
