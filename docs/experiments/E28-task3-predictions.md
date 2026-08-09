# E28 task 3 — predictions, frozen before the first measurement

**Executor, 2026-08-09, the third seat of the arc.** Task 3 is the named carry
([E28 Ruling 17](E28-ruling.md)); its contract is
[E27 Ruling 7](E27-ruling.md) and [the kickoff's Task 3](E28-instrument-census-kickoff.md).

**This file is committed before `texel_provenance.py` is edited and before any measurement
of it is taken.** What I had already done when writing it: read the instrument, the wrapper's
handler, T38, the fixture builder, `instrument_census.py`'s exclusion logic and
`record_markdown()`. **Reading source is not measuring**, but it is not blindness either, and
every row below discloses which it is. Nothing has been *run*.

Two laws from this arc bind these numbers and are applied per row rather than cited:

- **A composite definition is governed by its rarest clause** (Ruling 8) — P17 is a
  four-clause conjunction and is predicted clause by clause, then the join.
- **An instrument inside its own population must be checked against itself on every axis,
  each time** (Ruling 7) — P22 and P23 are that check for this seat, and they are predicted
  rather than assumed, because *one clean check is not clearance*.

---

## The registered design, so no part of it can be chosen after seeing a result

The pure-move discipline has a shape, and I am fixing it here rather than after the numbers
land.

**In the instrument** (`tools/diagnostics/texel_provenance.py`):

1. A largest-connected-component block **printed after the whole-atlas census loop and
   before the `--render` early exit**, so it rides the write-free census path — which is the
   path the server wraps.
2. One line per class already in the census (TWINS, each BRUSH stroke, DILATION), carrying
   **the component's texel count, the class total beside it, and the percentage of the
   class** — the two-thresholds law wants the pair, so the pair is printed on one line and
   the denominator is named in the text.
3. **4-connectivity, atlas space, over `class AND valid`** — the same mask the census totals
   use, or the two numbers would not describe the same set. No toroidal wrap.
4. **The caveat rides the output, not a comment**: atlas adjacency is not surface adjacency
   (the instrument's own docstring says so), so a surface-contiguous region split by UV seams
   appears as several atlas components. The atlas LCC is therefore a **lower bound** on the
   largest surface-contiguous run of that class. That direction is stated in the print block,
   in the docstring body, and in the served payload's notes.
5. **Docstring line 1 is not touched** (axis C reads it).
6. **No new flag** (axis A counts `add_argument`).

**In the wrapper** (`tools/measure_mcp.py`): the new lines are parsed at pinned print sites,
exactly as the census lines already are, into `census.twins_largest_component`,
`census.dilation_largest_component`, and `largest_component` inside each stroke row. The
`measure.notes` gap-text is **deleted in this same commit** and replaced by the
atlas-adjacency caveat. `ratios` gains the new pair with its denominator named. No arithmetic
is added to the server (gate 3).

**What "pure-move" means here, stated before it is tested.** The task adds an output, so
whole-stream byte identity is *impossible by construction* and would be the wrong condition —
naming it as the bar would be a pass condition the experiment is designed to break. The
registered condition is the honest form of the arc's standard:

> **INSERT-ONLY on stdout** — every line the pre-change instrument printed appears in the
> post-change stdout, byte-identical, in the same relative order, with the new block as the
> only addition; **and BYTE-IDENTICAL on `--out-json`**, which gains nothing at all.

The JSON is the stronger half and is deliberate: `--out-json` carries the head-render
region report, not the atlas census, so the census's new number belongs beside the census's
existing numbers and nowhere else.

---

## The predictions

| # | quantity | unit / denominator | point | band | blind? |
|---|---|---|---:|---|---|
| **P17** | recorded texel_provenance subjects available for the proof | one **(prep, state, stage1) triple**, not one invocation | **2** | 1-5 | **BLIND** |
| **P18** | the pure-move condition above holds on every subject run | boolean | **HOLDS** | - | code-read |
| **P19a** | fixture LCC(TWINS) | texels, 4-conn | **512** | exact | derived |
| **P19b** | fixture LCC(DILATION) | texels, 4-conn | **160** | 120-160 | derived |
| **P19c** | fixture LCC(BRUSH s1) | texels, 4-conn | **352** | 300-352 | derived |
| **P20** | the stripe variant's separation at equal TWINS total | ratio LCC(blob) / LCC(scatter) | **16x** | >=8x | derived |
| **P21** | tests T47 adds | **collected pytest cases** (parametrization expanded) | **6** | 4-10 | half-blind |
| **P22** | census rows whose headline `cited_count` moves on re-emit | rows, of 107 | **0** | 0 | code-read |
| **P23** | census rows whose axis-E `anchored` moves on re-emit | rows, of 107 | **0** | 0 | code-read |
| **P24** | LCC(DILATION) / DILATION total on the largest recorded subject | fraction **of that class**, not of valid texels | **<5%** | 0.5-20% | **BLIND** |

### P17 — clause by clause, because the join tracks the rarest

A subject needs all four. I predict each, then the join, per Ruling 8.

| clause | what it needs | predicted |
|---|---|---:|
| a - a complete prep | `meta.json`, `mask.npy`, `pos.npy`, `nor.npy`, `prep_uv.glb` | 6 |
| b - a stage-1 atlas with **both** siblings | `X_holes.png` **and** `X_styled_mask.npy` | 2 |
| c - a state with >=1 complete job | `job_<key>/{cam.json,inpainted.png,mask.png}` | 2 |
| d - a recorded stroke order | the order is citable from the record, not invented | 2 |
| **join** | all four on the same triple | **2** |

**The rarest clause I am naming in advance is (b)**: `_styled_mask.npy` is written by the
stage-1 projection, and only an arc that ran stage 1 *and then brushed* leaves one beside an
atlas. Preps are plentiful across arcs; brush states are not. If I am wrong I expect to be
wrong on (a), which I am guessing at hardest.

**What would falsify the unit itself**: if the same state carries several *recorded* stroke
orders, "subject" would have been the wrong unit and the count is invocations, not triples.
Named now so it cannot be discovered as a convenience later.

### P18 — the falsifier, stated

Any pre-change stdout line absent, reordered, or differing by a byte in the post-change run;
or any byte of `--out-json` differing. Mechanism for the prediction: the change reads `claim`
and `valid` and prints; it computes nothing that feeds an existing quantity.

**The known trap, from the seat before me**: 2a's harness produced a false `DIFFERS` because
the tool prints its own `--out-json` argument back. Both runs therefore get the **same**
`--state` and the **same** `--out-json` path, and the JSON is moved aside between them. A
differing byte the harness injected is not a differing behaviour.

**Three legitimate changes I am declaring in advance, so they are not scored as violations**:
the payload's `instrument_sha256` (the file changed - that is the identity envelope working),
its `config_hash`, and `MEASURE_VERSION`, which I expect to bump because the served payload
gains fields and two surfaces must not share a version number.

### P19 — derived from the fixture builder, not measured

The fixture styles `u < 0.5` of a 32x32 atlas: a solid 32x16 block, one 4-connected
component, so **512 exactly**. DILATION is the 160 holes the edge-distance guard refused;
the complement of a distance-guarded interior against a convex painted region is a rim, and a
rim is connected, so I predict **all 160 in one component** - with a band down to 120 because
a rim that pinches to nothing at a corner would split. BRUSH is the guarded interior, which
should be a single solid region: **352**.

**These three are the ones I am most entitled to and least informed by** - they are geometry
I read out of the fixture builder. Scoring them as hits proves the arithmetic runs, not that
the measurement is interesting.

### P20 — the can-fail leg, specified before it is built

A scratch variant of the committed fixture whose stage-1 styled mask is **16 alternating
full-height columns** (512 texels, same total) with the hole map rewritten as its exact
complement, so TWINS stays 512 and nothing overlaps. Sixteen separate 32-texel components
against one 512-texel block: **LCC 32 against 512, a 16x separation at an identical total.**
That is the two-thresholds law exercised in one pair, and it is the leg that can fail - a
count-only census cannot tell those two atlases apart at all.

### P21 — the unit is collected cases, because that is what has bitten

E26's P8 predicted what it would *write* and the instrument counted parametrized cases (8 to
34). I am predicting **collected cases** and intend no parametrization, so I expect the two
to coincide; if I parametrize, the prediction is against the expanded count. Planned legs:
the fixture's three LCC values, the invariant that LCC <= class total for every class, the
stripe-variant separation at equal total, the served payload carrying the new keys, the gap
note being gone, and the caveat being present.

### P22 / P23 — the self-population check, predicted rather than assumed

This seat writes two `docs/experiments/E28-*.md` files into the corpus and one
`tests/test_t47_*.py` into the axis-E set. Ruling 7's exclusion is prefix-based and
permanent, so I predict the **headline** axis-D count does not move on any of 107 rows; and
`texel_provenance` is already anchored by T38, so I predict axis E does not move either.

**What I expect to move, named so a moved number is not read as a defect**:
`corpus_files_before_self_exclusion` (+2, my two documents), `self_documents_excluded`
(+2), and `cited_count_raw` for whichever instruments my documents name - `cited_raw` excludes
only `SELF_OUTPUTS`, not this arc's papers, by design. Those are the contamination staying
visible, which is what that field is for.

**The check is only meaningful if it can fail**, so it is run as a diff of the committed JSON
against a fresh emission, not as a re-reading of the same file.

### P24 — the one number this task exists to produce

DILATION is grown in from neighbours where no camera painted. In the atlas it should be
dominated by rims along island boundaries - thousands of small components - which puts the
largest one at a small fraction of the class. **Under 5%, band 0.5-20%.**

The falsifier is interesting either way, and that is why it is worth predicting: **above 20%
means one dominant unpainted region**, an occlusion pocket rather than seam noise, and that
is precisely the "one wrong garment" the two-thresholds law exists to separate from speckle.
A high number is a finding, not a failure.

---

## What I am not predicting, and why

- **Whether any of this is good.** Not the executor's call.
- **The DILATION LCC's location on the mesh.** The instrument reports atlas components; where
  they sit on the surface is a picture for the Director's eye, and the atlas-to-surface step
  is exactly the caveat above rather than a number I can quietly supply.
- **Whether the atlas LCC should have been a surface-connected LCC instead.** It is a
  different, more expensive measurement (adjacency over the mesh graph, not the atlas), it is
  not what E27 Ruling 7 commissioned, and inventing it here would be the forcing Ruling 10
  ruled against. Named as a limitation in the report, not built.
