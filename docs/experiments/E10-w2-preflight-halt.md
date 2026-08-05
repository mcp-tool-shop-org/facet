# E10 Arm W2 — HALT at the pre-flight: the layer has no declared prompt binding

**Executor session, 2026-08-05.** Run under [E10 Ruling 5](E10-ruling.md)'s sequence.
Written after the work. **Nothing was submitted; 0 credits spent.** The gate fired before
the workflow JSON was written, which is where it was built to fire.

---

## The halt

```
brush_cloud_step.py graph --job <layer job> --key y+000_e+00
    --prompts docs/experiments/E10-layer-prompts.json --profile profiles/ship.json

ANDON: pre-flight - the values entering this graph disagree with ship.json's decided
texpass_brush block:
  --prompts is E:\AI\facet\docs\experiments\E10-layer-prompts.json
  but the profile's _fixtures.brush_prompts names
     E:\AI\facet\docs\experiments\E04-brush-prompts.json
No workflow JSON was written. This check has no skip flag: it exists because
brush_cloud_step.py binds no profile, so agreement between its constants and a
subject's decided values is a coincidence until something asserts it. HALT.
```

The guard is right and it is not in the way of anything. `_fixtures.brush_prompts` is a
**decided** value — Ruling 23 ruled it, on the twin file's own measured argument — and the
pre-flight exists precisely so a generative step cannot fly on a prompt file the subject
never decided.

## What the halt actually found

**E10's spec scored DECOMPOSE_BY_SECRETS a 3** on this claim: *"contact geometry in the
profile (`waterline_z`), mechanism in tools, water identity in the prompt and layer fixture
— a change required outside those is a primary finding."*

Every part of that held. `waterline_z` went into the profile. The mechanism went into the
tools. The layer's identity went into `canon/E10-LAYER-IDENTITY.md`,
`canon/E10-layer-palette.json` and `docs/experiments/E10-layer-prompts.json`.

**The thing that did not hold is one level up: the profile has exactly one brush-prompts
slot per subject, and E10 introduces a second content lane over the same subject.** The
galleon now has two prompt fixtures that are both legitimately its own — the hull's twelve
elements (E04, ruled) and the layer's L1 (E10, ruled) — and the profile's vocabulary can
name only one of them. The gate then does its job and refuses the second.

This is the spec's own test firing as designed. It is a finding, not an obstacle.

## What is NOT done, deliberately

I did not add `_fixtures.layer_prompts` to `profiles/ship.json`, and I did not teach the
pre-flight a second legal binding. Both are **decided values and a no-skip gate's
definition of legal** — the advisor's, not the executor's. Editing either while holding a
run I want to fly is the precise shape of improvising past a gate.

## What the ruling faces

Stated without a recommendation:

1. **Where the layer's prompt fixture is declared.** `_fixtures.layer_prompts` in
   `ship.json` is the obvious slot and matches where `waterline_z` already went; whether a
   layer is *subject* data on the same profile or its own profile is the question under it.
2. **How the pre-flight learns the lane.** It compares one path against one decided value.
   A second lane needs the check to know which lane a run is in — a flag, or the state
   directory's own declaration. Whichever it is, it must stay unskippable.

## Everything else in the chain is staged and green

| step | state |
|---|---|
| layer state seeded | done — re-seed byte-identical, base sha unchanged |
| `canon/E10-LAYER-IDENTITY.md` (L1 verbatim from Ruling 5) | landed as authored |
| `canon/E10-layer-palette.json` (warm-pale, bounds null, report-only) | landed as authored |
| `docs/experiments/E10-layer-prompts.json` | written — L1 prepended to E04's ruled string, one variable |
| layer job emitted at the beam | done — 293,865 figure px, **25,213 hole px** in the band |
| workflow JSON | **not written** — the gate fired first |
| submission / credits | **none** |

The emit is worth one line on its own: the layer state renders as *the ship* (its atlas is
a copy of the accepted base, so the brush has context and registration), and the only
paintable region is the geometric band. W2's job mask is geometry's answer, not a prompt's.

## Standards compliance (this step)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | the prompt file transcribes E04's ruled string byte-for-byte and prepends L1, so the run carries one variable; defaults byte-matched to `texpass_brush.py` |
| ANDON_AUTHORITY | 3 | the pre-flight fired before the workflow was written and was not edited afterward |
| NAMED_COMPENSATORS | 3 | no irreversible action reached: nothing submitted, no credits, undo is deleting `e10_layer/` |
| DECOMPOSE_BY_SECRETS | 3 | the boundary test the spec pre-registered fired and produced its first primary finding |
| UNCERTAINTY_GATED_HUMANS | 3 | halted with both questions stated and neither answered |
| EXTERNAL_VERIFIER | 2 | the gate is a different tool than the one that built the values it checks. Not 3: no generation has been graded yet |
