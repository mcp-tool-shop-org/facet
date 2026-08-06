# E12 handoff 2, Task 3 — the backdrop derivation

**Executor session, 2026-08-05.** Prediction pre-registered in `c7f23f1` before the
derivation ran ([E12-task3-predictions.md](E12-task3-predictions.md)). Input:
`canon/dragon-materials-estimated.json`, eleven sRGB estimates read off the fixture's words —
the weakest link in the chain, and superseded by the styled pair under the fixture's own
non-circularity rule.

```
e04_backdrop.py --materials canon/dragon-materials-estimated.json --out E12_backdrop
```

---

## 1. The three optima

| | rgb | L* | sat | weighted-min | **bound by** |
|---|---|---|---|---|---|
| metric optimum | (255, 0, 245) | 59.7 | **1.000** | 0.3980 | **D3** storm-grey membranes |
| best low-saturation | (122, 163, 133) | 63.4 | 0.160 | **0.1922** | **D3** storm-grey membranes |
| best neutral | (153, 153, 153) | 63.2 | 0.000 | 0.1353 | D4 ivory (raw min D3) |

**The metric optimum is a full-saturation magenta and is disqualified** by the standing rule
that a saturated backdrop bleeds into a diffusion image. It is reported, as the tool's own
docstring requires, because the metric does not know that rule.

**D3 binds every optimum.** The storm-grey membranes are the minimum at the metric optimum,
at the low-saturation optimum, and the raw minimum at the neutral. **The dispatch's concern
about D3 is expressed by the derivation itself and needs no weight** — which is why the
materials file deliberately did not flag it thin under a flag whose name describes a
different mechanism.

## 2. The inherited candidates, scored — neither transfers

| backdrop | weighted-min | bound by | |
|---|---|---|---|
| **W3's mid grey (0.42)** | **0.0506** | D3 | **below the key's own 0.06 threshold** |
| galleon's white | 0.0961 | D10 ivory | |
| black | 0.1216 | D11 slate | |
| derived neutral (153) | 0.1353 | D4 ivory | |
| **derived low-saturation (122,163,133)** | **0.1922** | D3 | |

**W3's inherited "plain grey background" scores 0.0506 on this subject — under the key's own
0.06 cut.** That is the same shape as the failure that killed the blade: a mid grey puts a
large near-neutral material *on* the threshold. Here the material is not a sword band, it is
**the wing membranes**, which is most of what this subject is for. The galleon's white is
better but still worse than any derived option, bound by the ivory family sitting within 0.19
of white before the thin weight. **Neither inherited backdrop transfers, and the fixture was
right to list both as candidates rather than inherit either.**

## 3. What the metric does NOT decide, and it matters

The tool reports one low-saturation winner. Surveying the low-saturation space (sat ≤ 0.20)
by hue family shows the winner is not meaningfully ahead of its alternatives:

| family | rgb | sat | weighted-min | bound by |
|---|---|---|---|---|
| green | (114, 165, 133) | 0.200 | **0.2029** | D3 |
| **blue-violet** | (121, 121, 172) | 0.200 | **0.1978** | D4 |
| warm | (159, 108, 140) | 0.200 | **0.1936** | D3 |
| neutral | (146, 153, 146) | 0.025 | 0.1478 | D4 |

**Green, blue and warm span 0.009 of score.** The metric does not separate them. So the hue
choice is *not* decided by this derivation, and reporting the green winner as though it were
the answer would be reading precision the measurement does not carry.

**One observation for the eye, offered as data:** the top-scoring low-saturation option is a
desaturated **green**, and this subject's dominant declared material is **deep moss-green
hide** (D1, second-lowest distance at the low-sat optimum, 0.2949). A green backdrop behind a
green animal is the kind of thing a metric is content with and an eye may not be. The
**blue-violet** at (121,121,172) costs 0.005 of score, is the one hue family **no declared
material occupies**, and carries no such adjacency. Both are on the table; **the choice is
the ruling's, not this session's.**

## 4. Predictions scored — 6 of 6

| # | prediction | outcome | measured |
|---|---|---|---|
| R1 | unconstrained optimum saturated (>0.30) and disqualified | **held** | sat **1.000**, rgb(255,0,245) |
| R2 | best neutral in 0.50–0.65 | **held** | 153/255 = **0.600** |
| R3 | D3 or the ivory family binds the neutral optimum | **held** | **D3 binds all three optima**; D4 binds the neutral on the weighted metric |
| R4 | neutral optimum's score below 0.20 | **held** | weighted 0.1353, raw 0.1686 |
| R5 | recommendation is a low-saturation non-neutral, not a pure grey | **held** | low-sat 0.1922 against neutral 0.1353 — **42% better** |
| R6 | the galleon's white does not transfer | **held** | **0.0961**, worse than every derived option |

**Six of six.** Worth stating plainly against this session's record — Gate 0 was 13/21 and
Task 2 was 11/18 — that the difference is not improved judgement. R1–R6 are predictions about
**arithmetic on a table I had just authored**, where the operands were in hand. Gate 0's and
Task 2's were predictions about **a subject nobody had measured**. The scoreboard is the same
number in both cases and does not mean the same thing, and this arc's real calibration lesson
stands unchanged: this subject class has no working prior, and every value it needs must be
measured on it.

## 5. What has NOT run

- **The chosen word is not chosen.** The derivation proposes rgb values; a prompt takes a
  *name*, and naming is where an estimate becomes a term the generator acts on. The twin-
  prompts file is written when the hue is ruled.
- **Tasks 4 and 5.** No generation has run. **No credits have been spent.**

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Material table is a versioned file, not a literal; every optimum, its saturation, its binding material and the inherited candidates' scores are recorded with operands |
| ANDON_AUTHORITY | 2 | No halt in scope. The saturated optimum is surfaced and disqualified by the standing rule rather than silently dropped |
| NAMED_COMPENSATORS | 3 | Two new canon/doc files and one output dir; nothing pre-existing modified; no spend |
| DECOMPOSE_BY_SECRETS | 3 | The D3 weighting question was answered by *not* overloading a flag whose name describes a different mechanism, and handed to the ruling as a named decision instead |
| UNCERTAINTY_GATED_HUMANS | 3 | The hue is explicitly **not** chosen, with the reason measured: green, blue and warm span 0.009 of score, so the metric does not separate them. The green-on-green adjacency is offered to the eye as data |
| EXTERNAL_VERIFIER | 3 | The derivation's input is a declared table, and both inherited backdrops were scored against it — which is what showed W3's grey landing under the key's own 0.06 threshold on this subject |
