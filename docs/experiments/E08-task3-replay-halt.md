# E08 Task 3 — the A32 replay gate FIRED: the fix is not a no-op on clean input

**Executor session, 2026-08-04.** Amendment 32's fix is implemented, the void is done, and the
replay's pre-registered gate **fired**. The premise the gate encoded — *the backdrop was flat on
all six, so the intersection must be a no-op where the premise held* — is measurably false, and
the reason is specific and small. Stroke 7 not re-committed. Stroke 8 not run.

```
                       expected      replayed    delta   intersection removed
stroke 1  y+090_e+00      2,507         2,352     -155   76,421 -> 76,389  (-32 px)
stroke 2  y+270_e+00      3,859         3,781      -78   76,506 -> 76,465  (-41 px)
stroke 3  y+045_e+00      2,017         2,013       -4  128,982 -> 128,980  (-2 px)
stroke 4  y+135_e+00      4,103         4,103        0                      (-0 px)
stroke 5  y+225_e+00      6,526         6,526        0                      (-3 px)
stroke 6  y+315_e+00     10,636        10,636        0                      (-0 px)
                                                  ----
holes    719,503 expected   719,740 replayed      -237
atlas    237 differing texels, max |d| 107
```

**155 + 78 + 4 = 237 = the differing texel count exactly.** The arithmetic closes with no
residue, so the divergence is entirely accounted for by three strokes' commit losses and nothing
else moved.

---

## 1. Two script faults of mine came first, and neither is this finding

The first replay attempt failed for reasons that were purely my own and are recorded so they are
not confused with the result:

- **I put `∧` (U+2227) in a `print`.** Not in cp1252, so `commit` raised
  `UnicodeEncodeError` **after** printing its diagnostic and **before** writing anything — on all
  six strokes. Nothing committed; strokes 3–6's renders then differed only because the state
  never advanced. **Fourth non-ASCII-in-print fault this session**, and I had already written a
  warning comment about it in three other files — a comment in another file did not help, so it
  is now in this one too.
- `tr -d '>-,'` parses `>-,` as a character range and errors; and a `/e/AI/...` path inside a
  heredoc is unresolvable by Windows Python.

After fixing those, **all six emits reproduced `render.png` and `mask.png` byte-identically**,
which is what proves the state advanced correctly and that each saved `inpainted.png` still
corresponds to its own input. The replay is valid. The gate's failure is about the fix.

## 2. Why the fix is not a no-op: flatness was the wrong premise

The intersection removes **32 / 41 / 2 / 0 / 3 / 0** pixels from the six trust masks. Measured,
every one of them sits **1 px outside the geometry** — median 1.0, max 1 — in 7 / 5 / 2 tiny
components (largest 11, 34, 1 px).

**That is rim spill, not a repainted backdrop.** The brush output's keyed figure is
`|edited − bg| > 0.06` followed by `minimum_filter(size=5)`; nothing in that construction aligns
it to the raycast hit mask, so at an antialiased figure edge the key extends about a pixel past
the geometry **regardless of how flat the backdrop is.** The amendment's inference —
flat backdrop ⇒ no off-surface keyed pixels ⇒ no-op — skipped that step. Flatness governs whether
the *estimator* is right; it does not govern whether a *threshold plus erosion* lands on the same
boundary as a raycast.

**And the amount is small but the cost is not proportional to it.** 32 removed pixels cost 155
texels; 41 cost 78; 2 cost 4. That is Amendment 26's mechanism exactly — deleting a few boundary
pixels shrinks `dist_e` locally, and the `edge_dist >= 4.0` test then rejects samples several
pixels inboard. It is the same shape as R1, where 6,619 removed pixels cost 5,399 texels, and the
**direction is the same too: intersecting tightens.** Third instance of that pattern in this
experiment, and the second time a "this will be a no-op" prediction about it has been wrong.

## 3. What the fixed tool does, and what it caught

Implemented per Amendment 32, atomically inside `texpass_iter`:

| part | status |
|---|---|
| `emit` writes `hit.png`, the geometry mask it rendered | done |
| `commit` intersects `fm_e ∧ hit` before `dist_e` | done — the six removals above |
| **in-tool assert**: the 8×8 corners the bg estimator reads must match the emitted render (≤1 level) | done — **passed on all six**, cannot be walked past by a shell |
| whole-image outside-figure residual demoted to a logged diagnostic | done — printed per stroke, never halts |

The diagnostic's per-stroke means reproduce the six clean readings (0.037 / 0.023 / 0.022 / 0.021
/ 0.025 / 0.016 lv), so demoting it lost no information.

**The corner assert is the part that matters structurally**: it lives inside the tool that
performs the irreversible write, so the failure mode that produced the breach — a shell walking
past a separate checker — is now impossible rather than merely discouraged.

## 4. State — all three atlases preserved, nothing lost

```
state/atlas.png                        the REPLAYED atlas   (719,740 holes)
out/TARGET_pre_stroke7_atlas.png       the pre-stroke-7 target (719,503 holes)
out/VOID_post_stroke7_atlas.png        the voided post-stroke-7 atlas (672,483 holes)
state/job_*/render.orig.png, mask.orig.png   the pre-replay emit outputs, for all 7 jobs
state/job_*/inpainted.png, inpainted_s770700.png   every cloud output, untouched
```

**Stroke 7's commit is void and stays void** — the replay achieved that much. What it did not
achieve is byte-equality with the target, so the current state is *neither* the old sequence nor
a verified reconstruction of it. That is the halt.

## 5. What is decided elsewhere

The gate's pre-stated branch is HALT, and I have taken it rather than adopting the new numbers.
Three readings are available and I am not choosing between them:

1. **The replayed atlas is the correct one and the target was wrong.** The 237 texels were
   trusted only because a rim-spill pixel inflated `dist_e`; by Amendment 26's own logic they were
   never legitimately trusted, and 719,740 is the honest baseline. This makes the gate's premise
   the error and the fix correct.
2. **The gate means what it says** — any digit differs, halt — and the fix needs its own
   regression before adoption, exactly as the A26 intersection got one (R0/R1) rather than being
   folded into a run.
3. **The `edge_dist = 4.0` constant is the real subject.** A 1 px change in the mask boundary
   costing 155 texels is a global constant governing a local feature, fifth instance; A3's local
   half-width cap is already the named alternative and is already queued post-Gate-1.

Also open: whether stroke 7 re-commits from its existing `inpainted.png` under whichever atlas is
ruled correct, and whether stroke 8 runs before or after that ruling.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Six emits byte-identical, proving state advance and input correspondence; three atlases and all pre-replay emit outputs preserved; the replay is a committed script, re-runnable |
| ANDON_AUTHORITY | **3** | The pre-registered gate fired and the session stopped at it — no adoption of the new counts, no argument that 237 texels is negligible, no re-run without the fix. The new in-tool assert is now unbypassable by construction, which is the breach's structural remedy |
| NAMED_COMPENSATORS | **3** | The void is complete and the compensator is exact and verified: three named atlas states on disk, every cloud output preserved, no regeneration needed for any path forward |
| DECOMPOSE_BY_SECRETS | **2** | The fix is localised to one operand in one tool; emit gained one output; the demoted diagnostic kept its numbers |
| UNCERTAINTY_GATED_HUMANS | **3** | Three readings stated with the measurement that supports each, including the one that says the gate's own premise was the error. None chosen |
| EXTERNAL_VERIFIER | **2** | The gate is an external check on my implementation and it caught that the fix is not what the ruling predicted; the rim-spill measurement is independent of the count comparison and agrees with it |

---

**HALTED at the replay gate.** Stroke 7 void, six strokes replayed through the fixed tool,
237 texels of divergence fully accounted for and diagnosed to 1 px of rim spill, stroke 8 not
run, 0 credits spent since the last ruling.
