# E08 Task 3 — the run completed. The sheet is built. Gate 1 is the Director's.

**Executor session, 2026-08-04.** Eight strokes committed, finalize, pack, renders, and the
sheet — *reference | asset | provenance | error*, views 4–6, at 2× zoom on blade and torso.
Built before the metrics, per CLAUDE.md. **No judgement of the asset appears in this document.**

---

## 1. The asset

```
stage 1 (8 cameras)   1,653,659 texels   68.8% of 2,402,810 valid
8 brush strokes         101,527           4.2%
dilation fill           647,624          27.0%
                      ---------          -----
non-dilated total     1,755,186          73.0%      atlas variance 0.04329
                                                    565 texels took the mean fallback
```

**Against E07's rejected asset — 28.4% reference / 37.7% invention / 33.9% interpolation:**

| provenance | E07 rejected | this asset | ratio |
|---|---|---|---|
| reference (the twins) | 28.4% | **68.8%** | **×2.42** |
| diffusion invention (brush) | 37.7% | **4.2%** | **×0.11** |
| interpolation (dilation) | 33.9% | **27.0%** | ×0.80 |

The pre-registered ceiling (Amendment 33: ~68.8 / ~1–2 / ~29–30) held on reference exactly and
the brush came in above its six-stroke projection — the two elevated cameras delivered 72,116 of
the 101,527, 71% of the brush total, because they see the most hole area.

## 2. Per-stroke, all eight

| stroke | camera | mask hole px | texels | holes after | in-tool corner assert | intersection removed |
|---|---|---|---|---|---|---|
| 1 | y+090_e+00 | 19,065 | 2,352 | 746,799 | pass | −32 px |
| 2 | y+270_e+00 | 22,725 | 3,781 | 743,018 | pass | −41 px |
| 3 | y+045_e+00 | 25,818 | 2,013 | 741,005 | pass | −2 px |
| 4 | y+135_e+00 | 22,157 | 4,103 | 736,902 | pass | −0 px |
| 5 | y+225_e+00 | 23,352 | 6,526 | 730,376 | pass | −3 px |
| 6 | y+315_e+00 | 32,302 | 10,636 | 719,740 | pass | −0 px |
| 7 | y+000_e+55 | 34,234 | **46,941** | 672,799 | pass | −11 px |
| 8 | y+180_e+55 | 26,289 | **25,175** | **647,624** | pass | −6 px |
| | | | **101,527** | | 8/8 | |

Stroke 7 re-committed from its existing generation at **46,941 against the voided 47,020** — a
delta of **79 texels**, which is the whole cost of the geometry intersection on that view. Its
re-emitted `render.png` and `mask.png` came back **byte-identical** to the brush's actual inputs,
so the generation is paired with exactly what produced it despite the 237-texel baseline change.

## 3. ⚠ Amendment 32's diagnosis of the stroke-7 pocket is FALSIFIED

**This is the one finding in this report that contradicts the banked record, and it is mine to
have caused.** A32 diagnosed the 202 px pocket as *"Amendment 26's cast shadow at the brush
site — repainted backdrop keyed as figure."* Measured, after the fix was in place:

| the pocket, y 377–394 × 370–385 | measurement |
|---|---|
| geometry hit (`hit.png`) | **288 of 288 px — 100%** |
| inside the job mask the brush was told to paint | **288 of 288 px — 100%** |
| emitted colour | mean rgb (107.0, 107.0, 107.0) |

`107/255 = 0.42` is `project_twins --hole-grey` **and** emit's background fill — the same value
by construction. **So an unpainted hole on real surface renders at exactly the background colour
and is indistinguishable from background by colour.** The pocket is not off-surface paint; it is
a hole the brush was instructed to fill, and it filled it.

**The ANDON that fired on stroke 7 was a false positive**, and the fix confirms it independently:
the geometry intersection removed 11 px on that stroke at bbox y 380–667, x 241–324 — **zero
overlap** with the pocket at y 377–394, x 370–385.

**The fault is my invariance check's operand.** I defined "outside the figure" as
`|render − 0.42| < 1.5/255` — **colour as a proxy for absence of surface** — when the property
itself was available exactly as the raycast `hit` mask that emit computes. On stroke 7, 8,331 px
the check called "outside the figure" are geometry hits, 7,832 of them inside the job mask.
*Test the property, not a geometric proxy for it* — this repo's own rule, and the same rule A26
and A27 turned on. Corrected in place: the diagnostic now reads `hit`, and stroke 8's
outside-figure residual came back **0 px over 4 levels** where the colour version would have
reported hundreds.

**What this does and does not change.** It does **not** excuse the breach — the commit ran past a
fired gate through my shell chaining, and that error stands. It does **not** invalidate the A32
fix, which is correct on its own terms and removed 32/41/2/0/3/11/6 px of genuine rim spill
across the run. It does mean the 47,020 was voided on a false alarm — and the void cost 79 texels,
which is now measured rather than assumed.

## 4. The sheet

`out/GATE1_sheet_ZOOM.png` (2×, blade and torso) and `out/GATE1_sheet_full.png`.
Columns: **reference** (the ARMB twin) | **asset** (`--flat`, never STUDIO) | **provenance** |
**error** (ΔE heat, dark = agrees). Rows: views 4, 5, 6.
Provenance: **green** = reference/stage 1 · **blue** = brush · **orange** = dilation.

### ΔE, asset against its own reference twin, inside the exact silhouette

| view | figure px | median | mean | p90 | > 10 | > 23 |
|---|---|---|---|---|---|---|
| 4 (yaw 180) | 146,356 | 11.02 | 15.75 | 33.85 | 54.8% | 18.0% |
| 5 (yaw 225) | 149,780 | 11.27 | 16.99 | 40.31 | 56.0% | 22.7% |
| 6 (yaw 270) | 90,553 | 12.82 | 18.94 | 43.29 | 64.0% | 27.0% |

**These are not a pass/fail number and no threshold is attached to them.** A stage-1 texel carries
the reference's own colour, so ΔE against the reference is partly a rendering comparison (Blender
`--flat` against a diffusion image) rather than a texture-fidelity one. Reported because the heat
panel is read from them.

### The blade's provenance, called out explicitly

Required by Amendments 28/29. Measured in **atlas space**, not from the provenance render —
Blender tone-maps under `--flat`, so colour-matching the render gave classes summing to 3.5% and
was discarded as invalid before being reported:

| view | §9a band | candidate texels | reference | brush | **dilation** |
|---|---|---|---|---|---|
| 4 | 7,328 px | 31,699 | 46.5% | 6.1% | **47.4%** |
| 5 | 6,082 px | 30,548 | 38.2% | 5.2% | **56.6%** |
| 6 | 4,110 px | 14,136 | 30.0% | 8.7% | **61.3%** |
| — | whole asset | 2,402,810 | 68.8% | 4.2% | 27.0% |

**The blade band runs 47–61% dilation against the asset's 27%, and 30–47% reference against
68.8%.** It is the worst-served structure on the asset by both measures, which is what §9a
predicted from the key excluding it — and it is visible as the orange stripe on every provenance
panel. E07 Gate 0 recorded the blade as carrying *no* reference at all; here it carries 30–47%.
Whether that is enough is Gate 1's.

## 5. Faults of mine in this run, all logged

1. **Chained `invar; commit`** in one PowerShell call with no exit-code check, so a fired ANDON
   did not stop an irreversible write. §3 above shows the ANDON was itself a false positive,
   which changes nothing about the breach.
2. **`∧` in a `print`** — fourth non-ASCII crash of the session, and this one killed `commit`
   mid-replay on all six strokes. Comments in three other files did not prevent it.
3. **`tr -d '>-,'`** parses as a character range; a `/e/AI/...` path in a heredoc is unresolvable
   by Windows Python.
4. **Retyped the 0b anchor prompt** instead of reading it, making a two-variable test; caught,
   cancelled, resubmitted verbatim.
5. **Presented a texel-space reach ceiling as a delivery forecast** (26.3% / ≤8.2%).
6. **Colour-matched a tone-mapped render** to measure provenance classes; caught by the classes
   not summing to 100% and redone in atlas space.

## 6. Artifacts

```
out/W3_final.glb                    the asset            out/atlas_final.png
out/renders_flat/final_{0..7}.png   textures, --flat     out/renders_clay/clay_{0,4,6}.png
out/GATE1_sheet_ZOOM.png            2x, blade+torso      out/GATE1_sheet_full.png
out/provenance_atlas.png + W3_prov.glb + renders_prov/
out/stroke_{1..8}_*_workflow.json   the eight recipes    out/run_log.jsonl  (11 entries)
out/TARGET_pre_stroke7_atlas.png  ·  out/VOID_post_stroke7_atlas.png
state/job_*/inpainted_s770700.png   every cloud output preserved
out/gate1_dE.json
```

Cloud: 9 jobs (8 strokes + the weight-identity anchor), 1 cancelled, **0 credits** — no paid API
nodes at any point. No local generation.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Eight workflow JSONs saved before submission; 11-entry ordered run log with job ids, input hashes and cloud names; the weight-identity anchor reproduced ΔE 0.84/1.06/6.8%/0.2% and was pixel-identical to the prior cloud output; stroke 7's re-emit byte-identical |
| ANDON_AUTHORITY | **2** | The in-tool corner assert passed 8/8 and cannot be bypassed by a shell — the breach's structural remedy is in place and exercised. Scored 2 not 3 because the breach happened in this run, and because the gate that fired was one I had mis-specified |
| NAMED_COMPENSATORS | **3** | Void executed and verified; three named atlas states preserved; every cloud output and every pre-replay emit output on disk; no regeneration was needed at any point |
| DECOMPOSE_BY_SECRETS | **2** | Fix localised to one operand in one tool; emit gained one output; prompts in their own versioned file; E07-era and A4 instruments untouched |
| UNCERTAINTY_GATED_HUMANS | **3** | The sheet is the checkpoint and it carries the artifact, not an argument. ΔE is reported with its confound stated and no threshold attached. The falsified A32 diagnosis is surfaced rather than buried |
| EXTERNAL_VERIFIER | **2** | The cloud validator, the in-tool assert and the replay gate each caught something my own reading had passed; the blade measurement was invalidated by its own arithmetic before it reached this report |

---

**Task 3 complete. The sheet is in front of the Director.** Eight strokes, 0 credits, every
recipe saved, every fault logged. **Gate 1 is his, and nothing in this document anticipates it.**
