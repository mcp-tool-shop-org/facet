# E38 — one material, not eight paintings

**Status: RUNNING.** Opened 2026-08-15 at the Director's directive after E37's halt. This
document is the spec. It was written *after* the arc began — the dispatches were issued as
background-agent prompts and existed only in an advisor transcript until 2026-08-16, which is
the debt named in [CLAUDE.md](../../CLAUDE.md)'s dispatched-seat standard. Recorded here with
that provenance stated rather than backdated.

---

## The question

E37 halted because no configuration of the per-view generation route made the generator paint
eight consistent, defect-free views of one subject. The Director's directive, 2026-08-15:
*"Let's try a completely different route, making sure that it's commercial-safe, so that we can
publish in the future."* Then, 2026-08-16, widening it: *"The point of these experiments is to
gain control over our art, so that is what you should be aiming for."*

**Can the performer be built as ONE material authored directly in UV space — identity carried
by geometry plus a front-projected decal — rather than by N independently-sampled painted
views?**

## Why this shape

The subject is a jointed wooden artist's mannequin with a drawn-on face: one turned-wood
material plus a small decal, not eight paintings that must agree. Authoring the material in UV
space removes the failure classes by construction rather than fighting them —

- no independent samples → no cross-view incoherence
- no projection, no view owners → no seams
- no generator in the base material → no invented flecks, no baked lighting
- no model weights in the chain → **commercially clean by construction**, which is the
  Director's publishing gate
- procedural and deterministic → tone, grain, scale and wear become *dials*, which is the
  stated aim

**The consult channel independently confirmed there is no served alternative**: `output_type=
MATERIAL` returns zero nodes and MATERIAL is not a registered socket type, so no served path
emits material maps without regenerating geometry. Authoring is the only route to
register-by-construction. See [consult #10](comfy-consult-10.md) when folded.

## The dispatches

Three seats, all Sonnet background agents spawned and steered by the advisor. Two transcripts
were lost; every artifact survived under `E:\AI\training\facet_E38\`.

| seat | asked for | landed |
|---|---|---|
| 1 | Phase 0 attribution (are the defects generation-side or ours?) + Phase 1 the material baseline | `phase0-report.md`, `phase1-report.md` |
| 2 | Phase 1.5 the bisect — are the marks in the atlas or in the render? | `phase1_5-report.md` |
| 3 | Phase 2 — aimed lever sweep | `phase2-report.md` (running) |

Every dispatch carried: predictions written blind before measuring, halt at every gate, no git
writes, no cloud, ASCII output, commercial-safety as a gate, and the standing instruction to
kill the advisor's candidates as hard as its own.

## What has been measured

**Phase 0.** The advisor's parked-face hypothesis is **FALSIFIED**: 151,914 parked faces at
100.000% agreement with `seen_faces_300k.npy`, patch colour RGB(67,38,20) not black, **0 parked
faces visible on all 8 cameras**, raycaster self-validated at IoU 0.99999+ before the zero was
trusted. The skull seam **is** an owner boundary — zero-pixel separation from an owner
transition, replicated on the flat render's own peak, with 30–48% surviving flat light (so it
is baked into albedo as well as lit).

**Phase 1.** The procedural material removes two classes by construction, confirmed at the
Director's eye and the advisor's walk: eight views read as one material where v4's read as four
woods; the skull seam is gone (7–15× fall at v4's own fixed pixels). **The dark marks
survived** — 847 → 425 — with **69.2% within 3px of a v4 mark** across two unrelated colouring
processes. The class is in the shared atlas substrate, not the generator.

**Phase 1.5 — the bisect split the class in two.**

| population | share | signature |
|---|---|---|
| **A** | 57.94% / 60.34% | UV lands outside any triangle's footprint; **100.00%** read atlas RGB exactly (0,0,0). Null **0.00%** |
| **B** | 42.06% / 39.66% | atlas clean at the exact texel; boundary-distance median **1.414** against the null's **2.828** |

Atlas-wide precondition: 13,722 islands, ~21.9 faces each, **median valid texel 1.0 texel from
a boundary**.

**Phase 2 Step 1.** Population A's hit triangles run a median 1.28 texels² against B's and the
null's 11.7–14.3, max 2.4486. Against a pre-registered bar the advisor invented, this is
**PARTIAL** and stays PARTIAL. Fully degenerate zero-UV-area triangles appear **only** in
Population A — categorical, needing no threshold, but ~4% of it.

**Margin reach.** Population A sits a median **18.0 texels** from the nearest valid texel,
**0/766 within either candidate margin**. Isolation in atlas space is the mechanism; margin
application is not.

**Phase 2 Step 2 — both mechanisms confirmed by INTERVENTION.** With the atlas fill set to
magenta: Population A 0% stayed dark; Population B **100% shifted, median ΔE 66–67, while
nothing at their own nearest texel changed.**

**Phase 2 A4 (res 4096 → 8192).** Population A collapses **92.7% / 93.6%** (766→56, 776→50);
census total down 66.8–80.7%; the live quality gate does not fire; utilisation unchanged. The
residual is ~half the same 12 zero-area triangles, immune to resolution (0 × 4 = 0).

## The continuity that matters

`bake_hero_prep.py`'s own `--reunwrap` help text records E05's finding: *"at 8 faces an island
is small enough to be entirely unpainted, and 54.6% of them were."* **That is Population A.**
E05 identified the mechanism, adopting native xatlas reduced it, and the record treated it as
closed. It was reduced, not closed — and apples-to-apples our layout (13,722 / 21.9) is
*normal* for this route against W3's 14,010 / 20.5. **The class is therefore a property of
every asset this route has produced, including the four accepted ones — measured here,
UNMEASURED there.**

## Arms

One variable each, all local, all free. A0 is the Phase 1 build.

| arm | change | aimed at |
|---|---|---|
| A1 | `margin_method='ADD'` | B |
| A2 | `margin` 0.001 → 0.005 | B |
| A3 | `shape_method='AABB'` | B |
| A4 | `--res` 4096 → 8192 | A — **done, decisive** |
| A5 | combination of whatever moved | — after singles only |
| A10 | direct xatlas re-unwrap, `PackOptions.padding` > 0 | the residual + B |
| A9 | atlas fill = mid-wood | **mitigation, measured NOT adopted** |

**Withdrawn:** A6 (bake margin — reach is 0%), A7 (`ADJACENT_FACES` — already the default),
A8 (`--reunwrap` — the advisor's error; it means smart_project, measured worse).

## Gates

- Any arm that reduces the census but visibly degrades the material at native resolution
  **halts**. Cheaper marks bought with a worse asset is the Director's call, not the seat's.
- No colour transform anywhere in this arc — third time on this subject a colour operation's
  own metric improved while it ate the face. A non-uniform result is reported, never corrected.
- Editing `bake_hero_prep.py` requires the A0 byte-identity anchor re-run in the same breath.
- Commercial-safety: procedural or our own authored art only.

## Out of scope

The face decal (Phase 3, unstarted, deliberately separate so each phase stays attributable) ·
the full PBR set (named, not built) · any cloud job · any route change to accepted assets ·
measuring this class on W3, the galleon, the dragon or the longsword.

## The advisor's errors in this arc, for calibration

Five asserted mechanisms, all wrong: the parked faces · an invented 1.0-texel² threshold · the
bake margin read as 16/EXTEND when the call site sets 8/ADJACENT_FACES · the `--reunwrap` arm,
built on a truncated grep line · the island-count comparison, which set a post-export-split
number beside a single-session one. **Dispatched seats caught three; a measurement killed one;
one returned PARTIAL.** What held was structure — the route decision, the bisect design, the
order that put margin-reach before the magenta test, and the gates.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every arm one variable, commands reconstructed and A0 reproduced byte-identical (atlas, render, census 425/1322/22) |
| ANDON_AUTHORITY | 3 | halts fired and were honoured at Step 1, the mask overlays, and the A0 anchor; the atlas-edit pivot carried a raising check that did not fire |
| NAMED_COMPENSATORS | 2 | no irreversible act in this arc — no cloud, no git writes from seats, all outputs to a fresh tree; compensator table owed if any arm ships |
| DECOMPOSE_BY_SECRETS | 3 | phases split so each contribution stays attributable; AO isolated as its own variable |
| UNCERTAINTY_GATED_HUMANS | 3 | the Director gates on artifacts, not step count; sheets walked at the advisor's seat first |
| EXTERNAL_VERIFIER | 3 | the executor grades the advisor's candidates and killed four of them |
