# E04 — the coverage pass. 41 keys inherit W3 by silence; here they are, classified.

**Executor session, 2026-08-04, after Ruling 21.** `e04_profile_check.py --coverage` is built
and run. **23 reference keys decided, 41 UNDECIDED.** No projection this leg; the sequence is
coverage → decisions → purity re-check → projection.

The checker now answers the second question. The old one compares values that are **present**
and is structurally blind to values that are **absent** — and an absent key is not neutral: the
tool falls back to its own default, which on this route is the character's measurement. Three
instances in this arc, the third one firing inside `project_twins` and stopping the projection.

Decided forms, per Ruling 21: **a value · a vacuous suspension · `_not_on_route`.** Silence
does not count. Conventions: `_not_on_route: {"key": "why"}` inside a tool block,
`_tools_not_on_route: {"tool": "why"}` at profile top level.

---

## The 41, classified — with the evidence for each bucket

### A. Whole tools the ship's own record already puts off-route — 13 keys

| tool | keys | the ship's existing record |
|---|---|---|
| `verify/head_render.py` | crop, crop-res, res, pad, views | `ship.json._gates.head_rect_metrics: false` — *"No face rect, so mesh_stats' density and curvature columns have no referent"* |
| `verify/mesh_stats.py` | crop, crop-res, curv-radius-frac | same gate; Gate 0 already recorded its front-view-rect warning as **the character instrument correctly noticing it is not looking at a character** |
| `smart_decimate.py` | target, crop-res, pad-frac, body-weight, factor | **the ship was never decimated.** `galleon_00006_raw.glb` is the raw TRELLIS output, and the bake reported *"native UVs: using the atlas the mesh arrived with, no re-unwrap"* |

These are the cheap ones: each already has a written reason elsewhere in the record, and
`_tools_not_on_route` would move that reason to where the checker can see it.

### B. On the route, currently running on W3's number — 21 keys

| tool | key | W3 value | status on this subject |
|---|---|---|---|
| `bake_hero_prep.py` | **res** | 4096 | **already used** — `meta.json` records `res: 4096`. The ship baked at the character's atlas resolution by silence |
| | crop-res | 1024 | used; the crop itself is explicit in the profile and inert at head-scale 1.0 |
| | unseen-strip | 24.0 | used |
| `cull_unseen.py` | min-seen | 0.3 | not yet run on the ship |
| | max-seen | 0.9 | not yet run |
| `project_twins.py` | **edge-min-struct** | 50 | **in the halted run** |
| | **power** | 6.0 | **in the halted run** — the facing-weight exponent |
| `texpass_iter.py` | facing-min | 0.25 | stage 2, not yet run |
| | edge-dist | 4.0 | stage 2 |
| | mask-dilate | 9 | stage 2 |
| `restylize_views.py` | seed / steps / cfg / denoise / lora-w / cn-strength / canny-low / canny-high / contour-width | 770700 / 20 / 2.5 / 0.92 / 0.75 / 0.9 / 0.4 / 0.8 / 3 | **these are the values the eight twins actually ran on.** Recording them is recording what happened, not choosing something new |
| | prompt, negative | W3's identity string | the ship passes `--prompts` from a file, so `--prompt` never reaches the output — but it is Ruling 2's named finding sitting in the default |

**The `restylize_views` row is the least alarming and the most worth writing down.** Those nine
values are already load-bearing: the pair used them, the twins inherited them, and
`E04-twin-prompts.json` records them as *"the recipe the pair used and the twins inherit unless
a ruling moves it."* `ship.json._still_suspended` lists the generation recipe as awaiting E04's
own anchor — **the anchor exists now.** Writing them into the profile turns a documented
inheritance into a decided one, and changes no behaviour.

**`bake_hero_prep.res 4096` deserves a separate line:** it is not pending, it is *spent*. The
ship's atlas was baked at the character's resolution and `meta.json` proves it. Whatever is
decided, the record should say the ship chose 4096 rather than that nobody asked.

### C. Already decided by a ruling the checker cannot see — 7 keys

`texpass_brush.py`'s seed, steps, cfg, lora-w, cn-strength, **prompt**, negative.

`ship.json` already carries, from Ruling 14:

```
"texpass_brush.py": { "_NOT_CLEARED": "FORBIDDEN on the ship until this block carries
ruled values - Ruling 14, standing law. The tool's --prompt defaults to the literal W3
identity string ..." }
```

That is **stronger** than `_not_on_route` — it forbids the tool outright rather than excusing a
key — but the checker as specified recognises three forms and this is a fourth. So these seven
rows are reported as undecided when they are in fact the most explicitly decided keys in the
file.

**I have not added `_NOT_CLEARED` to the accepted forms.** Widening what counts as a decision
is exactly the kind of change that should be ruled rather than assumed, and a checker that
accepts markers it was not specified to accept is how silence creeps back in. One line either
way.

## What the coverage pass says about its own three founding instances

All three now appear as **decided**, which is the check working:

| instance | how it reads now |
|---|---|
| `reg-iou-min`, `bbox-tol` | present with vacuous values (0.0, 9.99) — Ruling 14 |
| `bg-de`, `bg-max-pct` | present with 10.0 and vacuous 100.0 — Ruling 21 |
| `texpass_brush --prompt` | `_NOT_CLEARED` — Ruling 14, and the form question above |

## What was not done

No key decided, no profile edited, no projection. The classification above is evidence for a
ruling, not a ruling: bucket A's reasons already exist in the record and I have quoted them
rather than acted on them; bucket B contains values that are **already in effect** on artifacts
that exist, and saying so is not the same as endorsing them.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The checker reads the reference profile and the tools' own argparse; every row is machine-produced |
| ANDON_AUTHORITY | **3** | `--coverage` exits non-zero on any undecided key, so it can gate a run rather than inform one |
| NAMED_COMPENSATORS | **3** | One additive tool change; no profile, fixture or artifact touched |
| DECOMPOSE_BY_SECRETS | **3** | This is that standard's missing half: the boundary now has a test for *omission*, not only for *mistranscription* |
| UNCERTAINTY_GATED_HUMANS | **3** | 41 rows reduced to three buckets with the evidence for each, so the ruling is one pass; the fourth-form question is posed rather than resolved |
| EXTERNAL_VERIFIER | **2** | The checker compares two profiles against a third source neither controls — the tools' own defaults — and it immediately reported seven keys as undecided that a ruling had already decided, which is the instrument disagreeing with its author. `skip:` on a second model |
