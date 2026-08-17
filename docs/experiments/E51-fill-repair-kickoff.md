# E51 — repaint the fills so the polygons are never painted

**Written 2026-08-17** by the advisor seat, on the Director's ruling that the open work
is *editing the image*, not measuring whether editing it is worthwhile. One Sonnet
executor seat, background, working `E:\AI\training\facet_E51\`. **No GPU, no cloud, no
credits.**

## The defect and its mechanism, already located

The Director's E49 ruling: he accepted the sheets and named one new defect class —
flat-coloured angular patches, green/yellow/orange on the tabard and skirt, gold on a
boot.

`E:\AI\training\facet_E49\orphan_fill.py` states its own mechanism in its docstring: for
each texel of a zero-written island it samples the best-facing twin **with the UNERODED
sil**. Atlas islands at this fragmentation are frequently single mesh triangles. A
boundary-adjacent sample taken without the erosion reaches across a material edge,
imports the neighbouring material, and flat-fills a triangle-sized island with it. That
is a polygon of the wrong colour, by construction.

**This dispatch does not wait on E50's confirmation.** Both repairs below are correct
whether or not the overlay confirms the class, because both remove a way to paint a
texel a colour no view supports.

## The two arms — each changes one thing

**Arm A — visible orphans sample with the ERODED sil.** The uneroded sil is what lets a
sample cross a material boundary. Use this arc's own capped-eroded bundle for the sample,
keeping the selection rule unchanged (facing^6 argmax over views passing `sample_view`'s
depth-visibility test). A texel with no eroded-sil sample falls through to arm B.

**Arm B — never-seen surface gets a neutral per-material fill.** A texel that passes
visibility in NO view has no twin that can honestly speak for it (4.65–5.57% of valid
texels fail the depth gate in every flat-ring view — a standing open class). Sampling a
twin at a boundary for such a texel is inventing colour. Fill it from its **own
material's already-painted texels** instead. Deriving that colour is the one real design
decision here: it must be a statistic of pixels that genuinely belong to the material,
and this repo has a law about it — **below a chroma floor, hue is not a colour**, and a
statistic of hues must be **circular**. An arithmetic median of hues once reported +49.1
degrees where the truth was -8.4. Use the chroma floor to decide who votes and a
circular mean of unit chromatic vectors to decide where they point.

**The gate on both arms — a fill may not be off-palette.** `tools/palette_gate.py`
already carries the LAB bands, the chroma floor and the two-threshold reporting (total
plus largest connected component). Reuse it; do not re-roll it. A fill whose colour falls
outside the declared palette is **refused, not painted** — and refusals are counted and
reported per material, because a large refusal count is itself the finding.

## What must be reported, in this order

1. **The sheet, before any metric.** `reference | shipped | E49-complete | E51-complete`
   at native zoom for all 8 views, plus 2x crops on the tabard, the skirt and the boot
   where the Director named the patches. Defects first. An image is broken if any of it
   is. He judges; you do not.
2. Per-arm texel counts: how many texels arm A repainted, how many arm B filled, how many
   the palette gate refused, and what happened to the refused ones.
3. **What LEFT, not only what arrived.** This is a swap, not an addition. E49's fill
   painted these texels something; yours paints them something else. Characterise the
   difference by location and by class before reporting any net.
4. The sentinel count. Zero, or reported loudly.

## Gates — halt and report, never improvise past one

- **Gate A.** Arm A must not paint a texel the eroded sil says is invalid. This is the
  whole point of the arm; a violation means the bundle wiring is wrong.
- **Gate B.** Arm B must not run on a texel that any view can see. Never-seen is the
  precondition, and a texel visible somewhere belongs to arm A.
- **Gate C.** Every gate here is a `raise`, never a bare `assert` — `python -O` deletes
  an assert and execution continues past a fired gate, which is how 87 of this repo's
  ANDONs were once removable by an environment variable.
- **Gate D — put the andon where the invariant does not bound.** Arms A and B both make
  fills *more* conservative by construction, so over-painting is foreclosed and a gate
  aimed there fires on correct work. The live risk is the opposite: a texel left unpainted
  or filled flat-grey because both arms and the gate refused it. Watch that direction.

## Out of scope

Twin regeneration. Any generation spend. The canon build-out. Editing any repo tool —
work in `E:\AI\training\facet_E51\`, deriving from E49's scripts, and the only repo file
you write is `docs/experiments/E51-fill-repair-report.md`. Do not touch
`E:\AI\training\facet_E4*\` (recorded trees, citable-only) or `facet_E50\` (another seat).

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | Derives from named E49 scripts; manifest with sha256 per consumed artifact. |
| ANDON_AUTHORITY | 3 | Gates A–D halt, each a `raise`; Gate D watches the direction the invariant leaves open. |
| NAMED_COMPENSATORS | 3 | All writes under `facet_E51\` plus one report; compensator is delete-the-tree; owner the advisor. No irreversible call in scope. |
| DECOMPOSE_BY_SECRETS | 3 | Run-only seat; the durable form goes to the outside channel as a repo tool with tests (brief 12). |
| UNCERTAINTY_GATED_HUMANS | 3 | Terminus is the sheet for the Director's eye. |
| EXTERNAL_VERIFIER | 2 | Manifests make it replayable; the palette gate is an independent check on the fill, but no second seat re-measures. Owner advisor. |

## Rules for this seat

The standing executor set. No quality judgments in any register — not *better*, not
*fixed*, not *works*. Halt at every gate and report its evidence. A negative result — the
repair changes nothing visible, or refuses most fills — is a full success; say so and
stop rather than tuning toward a number. No commits. `handoff.md` first and kept current.
ASCII. Absolute python `E:\AI-Models\trellis2-env\Scripts\python.exe`. Blender via
PowerShell `-b -P` only. Scripts create their own output dirs. `argparse` eats leading
minus signs.

## Dispatch record

- 2026-08-17 — dispatched on the Director's correction that the open work is editing the
  image. The advisor's E50 (diagnosis) and Grok brief 11 (a decision instrument) both
  measure rather than repair; brief 11 was already launched and runs to completion, and
  E50's overlay still names which texels each arm should touch. This dispatch is the one
  that changes pixels.
