# Grok build #11 — the measurement that decides whether we spend credits

**2026-08-17, morning, facet advisor seat. BUILD round.** Prior: briefs 1–10, ten
nominated claims held, six builds landed. The Director's direction this session was to
put a track through this channel alongside the two seats already running.

*Everything below the line is the paste block.*

---

# Ten for ten. Build the instrument that decides whether the regeneration is worth the money — and argue with the inference it is supposed to support.

## Where the route stands

The Director accepted the E49 renders and named one new defect class: flat-coloured
angular patches. Strongest acceptance the route has had. A Sonnet
seat is testing the polygon class right now against the tagged provenance masks — that
is not your job and you should not touch `E:\AI\training\facet_E50\` or
`docs/experiments/E50-*`.

Your job is the decision *after* that one. The remaining plan is a canon build-out and
then regenerating all eight twins from the completed canon — and that costs Comfy Cloud
credits, which the Director approves personally. Nobody has measured whether it is the
right spend.

**The inference this instrument is meant to support, stated plainly so you can attack
it:** where the eight plates genuinely *disagree* about what a surface is, no compositor
can fix it and the source has to be regenerated. Where they agree and the render is
still wrong, the compositor is destroying information it was handed, and a compositor
pass is the cheaper fix. So: measure plate disagreement inside the regions the Director
circled, and the number tells us which branch to take.

**Argue with that.** It is the advisor's reasoning, not a ruling. If the inference does
not hold — if disagreement is high everywhere, or if "plates disagree" and "canon is
thin" are the same thing wearing two hats, or if the measurement cannot separate the
branches — say so, and say what would separate them. Your #3 catch in brief 3 turned an
arc by refusing the brief's framing. Same standard.

## What is on disk — MEASURED by the advisor this session, not inherited

```
E:\AI\training\facet_E46\
  s3_on\t00..t07\   disagreement.npy  (1024, 752) float32, range [0, 0.6265]
                    owner.npy         (1024, 752) int16, -1 = unowned, 0..7 = plate
                    coverage.png  dependent.png  independent.png  fallback.png
                    disagreement.png
  s3_off\t00..t07\  same shapes; disagreement range [0, 0.6390]
  flow\view_0..7\   flow.npy (1024,752,2) f32, confidence.npy (1024,752) f32,
                    confidence_xy.npy (1024,752,2) f32
  ab_table.json  ab_table.py  predictions.md  handoff.md  run_flow.py
  write_provenance.py
```

`t00..t07` index the eight flat-ring views. **There is no twin at elevation 55** — the
ring is 8 flat cameras and the el-55 pair are brush cameras. An earlier handoff said
"8+2 with two elevated"; that died on a measurement.

**The number that should shape your design.** In `s3_on/t00`, `owner` is -1 on 628,883
pixels, so the figure is **141,165** owned pixels of 770,048. `disagreement` is nonzero
on **122,439** — i.e. **86.7% of the figure carries nonzero disagreement.** A
share-of-nonzero statistic is therefore degenerate before you start. The question is
about the *magnitude distribution*, and choosing its summary is part of the build.

## The regions, and the gap in them

`tools/s3_sheet_regions.json` exists. It self-labels *"PROPOSALS. Not a ruling."* It
carries boxes for **views 0, 1 and 7 only** — `tunic`, `skirt`, `blade`, `grip` on 0 and
1, `boot_tops`, `blade`, `grip` on 7. Frame is 752x1024, boxes are half-open
`[x0,y0,x1,y1]`, crop is `src[y0:y1, x0:x1]`, exceeding the source is an ANDON.

The Director's named defect regions do not match that set. Across E48 and E49 he named:
**arm/sleeve** (mangled, mostly the shirt sleeve), **hand** (slightly),
**boot-tops/greaves**, then the E49 patches on **tabard and skirt** and a **boot**.
There is no `arm` box, no `hand` box, and five of eight views have no boxes at all.

Note also: the reference is **sleeveless** — the Director ruled it so, and expressed no
preference beyond that. The armhole smear is tunic paint crossing onto
unnamed flesh. Do not let a region called `sleeve` smuggle in a garment that does not
exist.

## Build order

Build **`tools/region_disagreement.py`** plus **`tests/test_t85_region_disagreement.py`**.
An invocable CLI in this repo's sense: `argparse`, real flags, a `__main__` guard. It
takes a tree, a mode, a region spec, and reports per-region plate disagreement with
honest denominators, its own base rate alongside every regional figure, and both a total
and a largest-connected-component per region (this repo's two-thresholds law: a total
alone must choose between missing the defect and firing on speckle).

Gates are `raise`, never bare `assert` — `python -O` deletes an assert and execution
continues past a fired gate; 87 of this repo's ANDONs were once removable by an
environment variable. Tests ride the commit that touches the code, and a test that
cannot fail is not a test: for every leg, construct the case that would fail if the code
were wrong in the specific way the leg exists to catch, and show it failing.

## Candidates — candidates, not rulings. Rank, kill, and add what we have not named.

1. **The summary statistic.** `nonzero` is dead on arrival (86.7%). Candidates: median
   and p90 magnitude within the region; share above a magnitude threshold you derive
   from something other than the regions you are testing; or **owner-flicker** — how
   often the `owner` label changes between 4-neighbours — as a proxy for *semantic*
   disagreement rather than *photometric* disagreement. Those are different questions
   and the second may be the one that matters. Which, and why?
2. **The denominator.** This repo has been bitten four times by a moving denominator,
   most recently by normalising a boundary quantity by area when it scales with
   perimeter — figure area swings 1.65x between a profile and a rear three-quarter on
   the same subject. Does disagreement live at material boundaries here? **Measure that
   before choosing**, and let the measurement pick the denominator.
3. **Which flow mode.** `s3_on` vs `s3_off`. Flow was directionally right 18/18 and a
   magnitude trim at 16–27% coverage. Report both, or is one the honest read?
4. **The region set.** Extend the JSON to the Director's named regions across all eight
   views, or stop hand-boxing and derive regions from material segmentation? Hand boxes
   are transcribed from one arc and carry its assumptions; a derived region is
   reproducible but may not be the thing he pointed at.
5. **Anything we have not enumerated.** Including: is this measurement answering the
   question at the top of this brief at all?

## Constraints that stand

Everything you need is on disk — **no GPU, no cloud generation, no credits.** Do not
edit any file under `E:\AI\training\facet_E4*\` (recorded trees; citable-only). Leave
your change-set **uncommitted** for the advisor's fold. **The test count surfaces are
reserved to you this round** — T34 pins stated counts against `pytest --collect-only`,
so move them in your own change-set; the advisor is concurrently editing only
`bin/facet.js`, `pyproject.toml`, `package.json`, `tools/record_mcp.py` and
`.github/workflows/ci.yml`, and the other seat writes only under `facet_E50\`. Run the
suite with `--basetemp=<scratch>` (Windows symlink PermissionError otherwise). Absolute
python: `E:\AI-Models\trellis2-env\Scripts\python.exe`. ASCII in tool output. `argparse`
eats leading minus signs — `--flag=-30`.

Do not grade quality in any register. The Director's eye is the only acceptance gate.

## Calibration

Nominate **one checkable claim** — about the tree, a number, or a mechanism in a tool
you cite — that we verify by running it before anything trusts the rest of your build.
Ten for ten; the streak is the authority, and a round where your chip loses is still
reported.
