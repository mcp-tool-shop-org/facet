# E14 handoff 7, Task 2 — the demotion ran; the lane is GATED before stroke 1

**Executor session, 2026-08-08.** Authorised by [E14-ruling.md](E14-ruling.md) Ruling 24
(`8f84ce2`), TASK 2 IS GO.

**Nothing generated. Zero credits. No workflow JSON was submitted or written to the run
tree.** The pre-flight halted before stroke 1's graph existed, which is the guard working —
and the beast's own fixture note predicted this exact halt in these exact words.

---

## 1. What ran, in order

| # | step | result |
|---|---|---|
| 1 | provenance correction to the handoff-7 report | the predictions hash was `c04a629` in my tree; the relief fold rebased mine to `a75d5cf`, which is what Ruling 24's evidence line cites. Corrected in place with the reason, not silently |
| 2 | **stroke stems v3** built (Ruling 24g) | `docs/experiments/E14-brush-prompts.json`, 8 keys |
| 3 | run state built from stage 1b | `E14_strokes/run/state/` — a copy; `state0/` and the banked A0 untouched |
| 4 | **the compensator EXERCISED first** (24f) | demote → undo → **all three state files byte-identical**. PASS |
| 5 | **the garnet demotion** (24f), once | 67,904 texels, atlas byte-identical, own invariance asserted |
| 6 | stroke 1 emitted (yaw 0, the ruled first camera) | 49,775 figure px, **10,162 hole px** |
| 7 | stroke 1 graph build | **⚠ ANDON — halted at pre-flight. No file written.** |

## 2. The stems, v3 (Ruling 24g)

Built by `tools/diagnostics/e14_make_brush_prompts.py`, which inherits the twin builder's
deletion construction whole and adds the one bound the ruling's term change needs:

```
[stems] entry terms 11; ONE substitution, asserted:
[stems]   - 'a dark garnet gem pommel'
[stems]   + 'a deep red garnet gem pommel'
```

**A substitution is a retype, which is exactly what the deletion construction exists to
forbid**, so it is bounded by assertion rather than by care: the v3 entry must differ from
the twin entry in exactly one comma-term, the term count must not move, and the result must
equal the twin entry with only that term replaced. Three assertions, no skip flag, a failure
writes no file. Then the drop map, unchanged from v2 (Ruling 15a):

| key | terms | |
|---|---|---|
| `y+000_e+00` `y+180_e+00` `y+045_e+00` `y+225_e+00` `y+315_e+00` `y+135_e+00` | 11 | FULL |
| `y+090_e+00` `y+270_e+00` | 10 | boss term dropped |

Keys are the job keys `texpass_iter emit` writes, so `brush_cloud_step --key` addresses them
directly. Order recorded in the file as Ruling 24e's: `0,180,45,225,315,135,90,270`.

## 3. The demotion (Ruling 24f) — and its compensator, exercised before it ran

`tools/diagnostics/e14_demote_garnet.py`. The mask is **re-derived from stage 1b's owner
array and the stone's geometric landmark**, never from colour, and its count is asserted
against the ruling before a byte is written:

```
[demote] mask re-derived from OWNERSHIP (drifted views 1/3/5/7) and the stone's landmark
         z >= 0.4340: 67,904 texels, asserted against Ruling 24f
[demote] styled 1,656,847 -> 1,588,943   holes 2,005,056 -> 2,072,960
[demote] changed: styled channel 67,904 texels, holes channel 67,904 texels
         - both subsets of the ruled mask, asserted
[demote] atlas.png BYTE-IDENTICAL before/after (69f61f32a3e2...) - the colour stays as the
         brush's shape context, by design (Ruling 24f)
```

**The named compensator was exercised before the real operation, not merely declared:**

```
[verify-undo] PASS - demote then undo returns all three state files BYTE-IDENTICAL.
```

`--verify-undo` copies the state to a scratch directory, demotes it, restores it from
`state0/`, and asserts the SHA-256 of all three files is unchanged. Only then was the real
demotion offered. It is standing ready and unused.

**The commit ANDON is untouched.** `texpass_iter`'s `assert not protected[hidx].any()` is
byte-unchanged; the demotion makes the target ordinary holes rather than weakening the guard
that protects styled ones.

### 3b. The demotion landed where the ruling aimed it

Stroke 1's job mask, before and after:

| | px |
|---|---|
| job mask at yaw 0, pre-demotion | 8,742 |
| job mask at yaw 0, post-demotion | **10,162** |
| newly masked | **+1,420** |
| of those, inside the gem watch band (rows 87–158) | **1,420 = 100.0%** |
| newly-masked bbox | rows 97–139, cols 95–144 |

**Every newly-masked pixel is the stone.** Nothing leaked into the collar, the wrap or the
blade — the ownership-derived mask is as tight in the frame as it is in the atlas.

## 4. ⚠ THE GATE — and it is the guard working

```
[pre-flight] register scan: decided lora-w 0.0; loader nodes NONE; card references NONE; 16 nodes
AssertionError: ANDON: ../profiles/prop.json names no _fixtures.brush_prompts.path, so the
strings entering the graph have no declared source for lane 'base'
```

`profiles/prop.json` decides `texpass_brush.prompts = "stroke stems v3"` but carries **no
`_fixtures.brush_prompts` pointer**, so `brush_cloud_step`'s E10-Ruling-6 provenance check
has nothing to check the graph's strings against and halts. **No workflow JSON was written**
— the pre-flight runs before the write, by construction.

**This halt was predicted verbatim by the route's own record.** `profiles/beast.json`'s
`_fixtures.brush_prompts` note says: *"the pointer must exist here or that guard halts,
which is the guard working."* The ship and the beast both carry the pointer; the prop's fold
decided the value and did not add the fixture row.

**I have not added it.** The standing rule is that HALT 1's ruling makes the profile edits —
the advisor's fold, not mine — and this is a fixture row, the load-bearing kind.

### 4b. It is the ONLY gap, and that is measured rather than assumed

A read-only probe ran the same pre-flight against a **scratch copy** of the profile in the
session scratchpad carrying only that one added row. Nothing from it is submittable and it
is labelled so in the file:

```
[pre-flight] register scan: decided lora-w 0.0; loader nodes NONE; card references NONE; 16 nodes
[pre-flight] PASS: five recipe values equal the decided block; lane 'base' -> --prompts IS
             _fixtures.brush_prompts (corroborated against the job's state identity);
             the graph's strings are that file's.
[graph]   key y+000_e+00  seed 770700  steps 20  cfg 2.5
          lora NONE - no loader node in the graph (Ruling 10b/25e);
          ModelSamplingAuraFlow reads the UNET directly    cn 1.0
```

Every other leg passes: the five recipe values against the cleared block, the **inverted
no-LoRA scan** (16 nodes, no loader node, no card reference, `ModelSamplingAuraFlow` reading
the UNET directly — the register expressed structurally, not as a weight), the lane
corroboration (no `layer_state.json` beside the state), and the prompt/negative provenance.
**One line in one file is the whole gap.**

One reported-not-gated line to carry into the fold: the pre-flight notes the profile's
*documentation* copies of prompt/negative do not match the fixture (`prompt False, negative
False`). That is expected and correct here — `texpass_brush`'s block carries
`prompts: "stroke stems v3"` as a pointer-by-name rather than a copied string, and the graph
never reads those fields.

## 5. What has NOT been done

- **No generation, no submission, zero credits.** `estimate_credits` has nothing to quote:
  no graph reached the cloud, and none was written into the run tree.
- **No stroke committed.** The run state holds the demotion and stroke 1's emitted job only.
- **No profile, fixture or palette edit.** The scratch profile used for §4b lives in the
  session scratchpad, is marked `_PROBE_WARNING`, and its graph is named `PROBE_ONLY_*`.
- **The banked A0 is untouched** — `stage1b_atlas*` all retain their original timestamps.
  `state0/` is pristine and is the compensator's source.
- **The demotion is left applied**, staged, with the compensator standing ready. It is a
  ruled operation that ran correctly into a *new* state; re-running it after the pointer
  lands would be redundant. The A0's dip to 1,588,943 is by construction (24f) and is in a
  state no accepted artifact depends on.
- No memory-store write. No gate armed. No finalize, no pack.

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The stems built from the live profile entry rather than transcribed, with the ruling recorded per key; the demotion re-derives its mask from named inputs and asserts the ruling's count; every step's log kept beside the state |
| ANDON_AUTHORITY | **3** | The pre-flight halted and **nothing improvised past it**; the demotion's own invariance asserted before any write (exactly the ruled mask, in state channels only, atlas byte-identical); the stems builder's three assertions write no file on failure; `texpass_iter`'s commit ANDON untouched |
| NAMED_COMPENSATORS | **3** | The compensator was **exercised before the operation it protects** — demote → undo → byte-identical SHA-256 on all three files — and is standing ready. Zero irreversible steps taken; zero spend |
| DECOMPOSE_BY_SECRETS | **3** | The term change belongs to the stroke lane and the fixture's L5 is unchanged; the mask comes from ownership and never from colour; the stems file is the lane's, the profile block is the recipe's, and neither reaches into the other |
| UNCERTAINTY_GATED_HUMANS | **3** | The halt goes up with the gap characterised to one line rather than as a bare failure; the demotion's effect on stroke 1's frame is measured and shown before any generation could depend on it |
| EXTERNAL_VERIFIER | **2** | `brush_cloud_step`'s pre-flight checks the stems file by provenance — a tool that did not write it; the demotion's effect is confirmed from the *frame* side (the job mask) as well as the atlas side. `skip:` on a second model per precedent |

---

## HALT — before stroke 1, at a fired pre-flight

`E:\AI\training\facet_next\E14_strokes\run\`:

```
state/atlas.png · holes.png · styled_mask.npy    the demoted run state
state/demotion.json                              the op's invariance record + compensator name
state/job_y+000_e+00/                            stroke 1's emitted job (render, mask, hit, cam)
demotion.log · emit_s1.log
HALT2a_demotion_and_gate.png                     fixture word | context | job mask, at 6x
```
`docs/experiments/E14-brush-prompts.json` — the v3 stems, in the repo, unreferenced by any
profile until the fold.

**One thing wants the ruling, and it is one line:**

**`profiles/prop.json` needs its `_fixtures.brush_prompts` row** pointing at
`docs/experiments/E14-brush-prompts.json`, the way `ship.json` and `beast.json` carry theirs.
Ruling 24 cleared `texpass_brush` with per-key provenance and decided
`prompts: "stroke stems v3"`, but the fixture pointer that makes that name resolvable was
not added, so the provenance guard has nothing to resolve against. Everything else in the
pre-flight passes (§4b). **The lane runs the moment that row lands** — demotion done, stems
built, stroke 1 emitted, compensator standing.

**Two things to carry into that fold, both measured here:** the demotion's effect on stroke
1's frame is entirely inside the gem band (§3b), so the stone is the only thing stroke 1
repaints beyond its ordinary holes; and stroke 1 is Ruling 24i's live test of the term, so
the sheet the advisor walks after it will be the generation at 6× against the fixture panel,
not the 11.2% the commit banks.
