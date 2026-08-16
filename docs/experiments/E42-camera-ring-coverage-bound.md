# E42 — Bound the camera-ring lever before spending generation on it

**Spec written BEFORE the work.** Advisor seat, 2026-08-16, under the Director's standing
authority to run experiments testing the levers. Dispatched as a background seat (Sonnet).
This document IS the dispatch.

---

## Why this exists, and why it is cheap

E40 measured **74.28% of the blade never hit by any camera**. Research since (E42-adjacent
swarm, five agents, 2026-08-16) returned one measured, primary-source-verified camera finding:

**MVPaint arXiv:2411.02336 Table S2** — at N=8 with a flat equatorial ring, FID **23.45**; at N=8
with **interleaved ±30° elevation**, FID **20.89**; at N=16 flat, **25.71**. Same view count,
11% better from breaking the ring; *more* views is *worse*. Verified at the primary source by a
research agent, and the two other rig claims this repo carried were checked at the same time —
**TEXTure's "back-low view at −60°" is FALSIFIED** (it is 8 equatorial + 2 top/bottom, the same
shape as ours), and Hunyuan3D-2's −90° camera is real but weighted **0.05** against the front
view's 1.0 (`hy3dgen/texgen/pipelines.py`).

**Our rig is the flat-ring configuration that measured worse.** Changing it needs new
generation, which is cloud-only and costs credits. This repo's law is to **bound an expensive
arm before spending it** — one executor priced a six-stroke experiment at +1.7 points and
skipped it. This arc is that bound, and it is **pure geometry: no generation, no credits, no
GPU.**

## ⚠ The trap this arc must not fall into, stated before the tasks

**The instrument measures REACHABILITY. MVPaint measured FID. Those are different units.**

A camera set that reaches more surface is not thereby a set that *paints it better* — reachable
texels can be reached badly, at grazing angles, at poor footprint. This repo has missed on the
unit/population family in **ten consecutive arcs**, and the newest member is exactly this shape:
*a share measured in one space is not a claim about another*.

So: this arc answers **"how much surface does a ±30° ring reach that ours does not"** and
**nothing about appearance**. If the coverage gain is large, that licenses a generation spend to
test appearance. If it is small, the lever is bounded and we do not spend. **Do not, anywhere in
your report, translate a coverage number into an expected quality number.**

## Enumerate first — the instrument already exists

Confirmed by the advisor before writing this, so you do not re-spend it. **Verify it; do not
trust it.**

- **`tools/diagnostics/e08_ceiling.py`** already computes the reachable-texel ceiling over camera
  ladders, using the projection route's own acceptance construction (facing floors, ray bias,
  normal offset — `project_twins`' defaults). Its own docstring says it exists to run "BEFORE an
  expensive arm is spent."
- It takes **`--elev "yaw:el,yaw:el"`** — arbitrary yaw/elevation pairs. **The elevation lever is
  already a flag.** Do not build a new instrument.
- Flags, complete: `--prep` (required), `--sets` (default `2,4,6,8,12`), `--facing-min` (0.45),
  `--head-facing-min` (0.18), `--bias` (3e-3), `--noffs` (1.5e-3), `--elev` (default ""),
  `--out-json`.
- It is also served as **`mcp__facet-measure__reach_ceiling`**, which wraps the same script and
  attaches an identity envelope (server version, instrument sha256, config hash). **Prefer the
  served tool** where it can express the arm, so the numbers carry provenance; drop to the script
  only where a flag is unreachable through the wrapper, and say which you used per arm.
- **W3's prep is at `E:\AI\training\facet_E06\C1\prep`** — verified present with all five members
  and all six required `meta.json` keys (`res` 4096, `crop_res` 1024). *The record said for months
  that W3 could not be re-baked; that was false and it was the advisor's — the prep lives in
  `facet_E06`, and three searches of `facet_E08` is one scope error repeated.*

**Before anything else, enumerate what else already exists** that bears on this: a blade mask or
blade face-set from E40 Seat C, any recorded coverage numbers, and whatever `--sets` ladder has
already been run on this prep. A task you can close by reading is closed by reading.

## Task 0 — establish the shipped rig's ACTUAL geometry

Do not assume it. Read the route and report, with file and line, the actual yaw and elevation of
every camera the shipped W3 run used. The advisor's belief — **8 at elevation 0 plus 2 elevated
at +55°, nothing looking down** — is a belief, and it is the premise the whole arc rests on.
E29's seat lost a prediction to an unchecked advisor premise, and the sentence was the
advisor's. **If it is wrong, stop and tell me before running an arm.**

## Task 1 — the coverage ladder

Run the reachability measurement over these camera sets on W3's prep. All are geometry-only.

| arm | set | what it isolates |
|---|---|---|
| **R0** | the shipped rig exactly, as Task 0 establishes it | the baseline; must reproduce whatever is on record |
| **R1** | 8 flat @ elev 0, no elevated pair | what the 2 elevated views buy |
| **R2** | 8 interleaved ±30° (0:+30, 45:−30, 90:+30, 135:−30, 180:+30, 225:−30, 270:+30, 315:−30) | **MVPaint's measured best, at equal view count to R1** |
| **R3** | R2 plus the shipped elevated pair | whether the elevated pair still adds after ring-breaking |
| **R4** | R0 plus one downward camera (report the yaw/elevation you chose and why) | the held-blade underside specifically |

Report, per arm: total reachable fraction, and the **change against R0 and against R1**.

## Task 2 — the blade, which is the whole reason this matters

The 74.28% never-hit was measured **on the blade**, not on the figure. A whole-figure coverage
number will be dominated by the torso and will hide the lever's actual target.

Report every arm's reachability **restricted to the blade**. Enumerate first whether a blade mask
or face-set already exists (E40 Seat C had one) — reuse it and cite where it came from. If none
exists, say so and tell me before building one; a blade mask defined by this seat, for this
measurement, would be a criterion chosen while looking at the thing it selects.

⚠ **A global constant must not govern a local feature** — three instances in this repo, each cost
a session. If anything in your measurement is scaled by a global figure width, say so.

## Predictions — write them BEFORE you look

For each of R1–R4, and separately for the blade restriction, state a prediction with a band, and
whether it was blind.

**First compute the instrument's own interval**: what reachable fraction does it return for a
camera set that unambiguously sees everything, and for one that unambiguously sees almost
nothing? **Predict inside that interval.** E39's seat predicted 75% for a rate whose instrument
ceiling was 63.66% — a number that could not have been right at any state of the world.

And check the population: *reachable* is defined per texel, and a texel no camera can see is
still a texel. Say what your denominator is made of before the first result depends on it.

## Gates

- **Halt at every gate. Never improvise past one.** Report it with its evidence and stop.
- If R0 does not reproduce the coverage already on record for the shipped rig, **that is a halt**,
  not a thing to explain away. It means either the record or the reconstruction of the rig is
  wrong, and which one matters more than this arc does.
- A gate measuring the **result** halts. A gate measuring the **environment's ability to run the
  measurement** may be repaired, if the repair adds capability rather than removing coverage, the
  coverage-removing alternatives are named and rejected in writing, and the firing is reported as
  a fired gate rather than smoothed into a green row.
- Any ANDON you add `raise`s — never a bare `assert`; `python -O` deletes those silently.

## Out of scope

- **Any generation, re-render, or re-bake. This arc spends zero credits. That is the point of it.**
- Changing the shipped rig, or any route default.
- The blend formula, the sampler, and the footprint term — E41 owns the sampler question and is
  running now. **Do not touch `tools/project_twins.py`**; another seat is reading it.
- Translating any coverage number into an expected appearance/quality number.
- ⚠ **Do not open the Browser pane.** It crashed the client twice last session.

## Working rules for this seat

1. **Never judge whether output is good.** Produce measurements. The Director judges. The words
   *verified, shipped, works, decisive, validated, proven* do not belong in your report.
2. **A negative result is a full success.** If ±30° recovers almost nothing, say so plainly and
   stop — that is the arc succeeding, because it saves a generation spend.
3. **Write `handoff.md` early and keep it current**, under `E:\AI\training\facet_E42\`. Transcripts
   get lost here; on-disk state is the record.
4. **Do not delegate your own core measurement to a child agent.**
5. **Do not write to the memory store.** Do not `git add -A`. Do not commit over the shared index —
   the advisor and two other seats are in this tree. Leave work uncommitted and tell me.
6. **Tests ride the commit that touches the code.** If you modify tool code, its tests land with it.
7. **Read listings COMPLETE.** `head`, `tail`, `Select-Object -Last` return plausible,
   well-formed, incomplete answers and never say so. Four instances on this rig; one flipped a
   precedent.
8. **Report to me on the open line** — after Task 0 at minimum, and immediately if a premise of
   mine looks wrong. I steer mid-flight and would rather withdraw an arm than have you work
   around it.

Environment: `E:\AI-Models\trellis2-env\Scripts\python.exe`, absolute, always. Scripts create their
own output dirs. ASCII in tool output. **`argparse` eats leading minus signs — use
`--elev=45:-30,135:-30` with an equals sign**, which matters in this arc more than most since half
your elevations are negative.

---

## ⚠ FINDING, recorded mid-arc — the identity envelope's guarantee is narrower than it reads

Found by the E42 seat 2026-08-16 while running R0, and verified by the advisor at
`tools/measure_mcp.py:284-291`.

**A served MCP instrument can silently drop parameters it does not know about, while its payload
still carries a correct-looking instrument hash.**

The envelope computes `sha256: _sha256_file(tool_path(instrument_rel))` — the instrument file
**on disk at call time** — and its comment states the hash "must hash the file that actually RAN."
For a subprocess-invoked instrument that is true: the subprocess reads from disk at spawn, so the
hash and the executed code agree.

**But the wrapper is not the instrument.** `measure_mcp.py` is a long-lived module loaded at
server start. When its source is edited mid-session, the running process keeps the old signature
and the old registered tool schema, so new parameters are dropped before they ever reach the
subprocess. The result is a payload that:

- certifies the **new** instrument sha256 — truthfully, the new file did run;
- reports the server version unchanged, because `MEASURE_VERSION` is a constant in the stale module;
- and was produced **without the new parameters being honoured at all**.

`measure_report`'s refusal-on-mismatch cannot see this, because nothing mismatches. **The envelope
certifies which instrument file executed. It does not certify that the wrapper honoured your
arguments, and it cannot.**

**What caught it was the echo.** The advisor required `--cams`/`--elev` to print their parsed lists
unconditionally into the payload, for an unrelated reason — guarding against a silent *misparse*.
The first R0 call returned `parsed_cams: []` with no custom row, and the staleness was visible
immediately. Without it, the call would have returned a plain equatorial-ring number labelled R2,
with a valid envelope, and nothing downstream would have objected.

**The generalisable rule: a payload should report what the run actually DID, not only what it
IS.** An identity block describes configuration; an echo describes behaviour; only the second
catches a caller that silently discarded half the configuration.

**Remediation, owner = advisor, not this arc:** a caller-side comparison of requested parameters
against the envelope's own `params` block would catch this class outright, since a dropped
parameter is absent from the echo. Not built here — E42 is fenced to camera geometry, and the seat
correctly fell back to invoking the script directly with the instrument sha256 pinned
(`3816c043…c134a1fd`) rather than shipping a half-verified wrapper path.

---

## ⚖ RULING — the halt is RESOLVED. E40's 74.28% is not a coverage figure. (Advisor, 2026-08-16)

**The seat's falsification was correct about its own bound and I mis-specified that bound.** I asked
for a *global* ray count when the mechanism is *local*: 64,438 rays are not reserved for the 17,955
texels, they are competed for by **all 150,470** blade texels, since each pixel resolves to the
nearest texel among all of them. Against that denominator the bound is 64,438 / 150,470 = **at most
42.8% hittable, so ≥ 57.2% never-hit forced by pigeonhole**, before geometry enters. Comparing
against the subset was the wrong denominator, and the spec I wrote invited it. *This repo's own law —
ask what the denominator is made of — failed in the check written to test it.*

**But the decisive evidence is simpler and does not depend on that argument.** The same
`c1_result.json` reports the **torso** dilation population: n = 4,472, `never_hit_pct` =
**97.987%**.

The torso is the best-covered surface on this figure. E42 measured whole-figure reachability at
74–78% and the torso sits at the top of that range. **A claim that 98% of torso texels are seen by
no camera is not credible, so `never_hit` is not measuring visibility.** And read as coverage the
two figures invert the truth: they would say the blade (74.28%) is *better covered* than the torso
(97.99%), the opposite of what the number has been used to assert for three arcs.

**What it does measure:** whether any pixel ray *resolved to* that texel — a **sampling-resolution**
statistic over a rasterized nearest-texel assignment, not a geometric visibility test. Its
population is dilation-sourced texels, i.e. texels the projection did not paint, which sit in chart
gutters and edges that geometry does not cover at pixel resolution. Such texels lose the
nearest-texel competition by construction. **The measurement is therefore close to tautological
with its own population selection**, and the torso's 97.99% is what near-tautology looks like.

**Disposition.** **E40's 74.28% is WITHDRAWN as a coverage claim.** It is not withdrawn as a
measurement — it reproduces, and it is a valid statement about rasterized sampling. It may not be
cited as evidence that cameras cannot reach the blade, which is how it has been used in
`docs/advisor-kickoff.md`'s queue, in the project's state memory, and in the motivation for this
very dispatch. E42's **96.35% blade reachable against a 99.75% ceiling** is the coverage figure.

**Confidence, stated separately by claim.** The torso reductio is solid and is the load-bearing
evidence. The precise mechanism — gutter texels losing the nearest-texel competition versus a
near-tautological population selection — is **my reading, arrived at after both seats closed, and
it is checkable**: run c1's own hit test over the *full* 150,470 blade population rather than the
dilation subset. If it returns ≥ 57.2% never-hit, the pigeonhole bound is confirmed too.

**The seat behaved correctly throughout** and reported a falsification against its own hypothesis
when the rule I gave it said to. The error in the check was mine.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Every arm is a named camera set against one frozen prep; the served `reach_ceiling` attaches server version, instrument sha256 and config hash per payload, so each arm's numbers carry their own provenance. Model tier pinned (Sonnet). |
| ANDON_AUTHORITY | 3 | Halt-at-every-gate is a working rule; R0's failure to reproduce is pre-registered as a halt rather than a puzzle; the gate/repair boundary is stated; new ANDONs must `raise`. |
| NAMED_COMPENSATORS | 3 | **No irreversible call is in scope** — generation is explicitly excluded and the arc is read-only geometry. Compensator for the only possible mutation (a code edit): `git checkout -- <path>`, owner = advisor, post-rollback state = HEAD. |
| DECOMPOSE_BY_SECRETS | 3 | The arc is fenced off `project_twins.py` entirely because E41 owns it concurrently; camera geometry and sampler are separate secrets held by separate seats. |
| UNCERTAINTY_GATED_HUMANS | 3 | Check-back is gated on a premise looking wrong, not on step count; Task 0 explicitly halts on the advisor's own rig belief; the blade-mask question halts rather than defaulting. |
| EXTERNAL_VERIFIER | 2 | The seat checks the advisor's rig premise and the MVPaint-derived motivation; but it verifies its own coverage numbers and no third party re-runs them. Remediation if a large coverage gain is returned and a generation spend is proposed on it: a second seat re-measures R2 independently before any credits are spent. Owner = advisor, before the spend. |
