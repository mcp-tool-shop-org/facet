# E08 Task 3 — stroke 7 HALTED by the invariance ANDON, and I let the commit through anyway

**Executor session, 2026-08-04.** Six strokes ran clean. **Stroke 7's invariance gate fired** —
a pre-registered condition with a pre-stated branch (Amendment 30: *concentrated → HALT*). Stroke
8 not attempted.

**And the commit executed regardless.** That is my error, not the pipeline's, and it is the one
class of error this repo exists to prevent. It gets stated first.

---

## 1. What I did wrong

I batched `invar` and `commit` into a single PowerShell call to save round-trips:

```powershell
... brush_cloud_step.py invar --job $j
... texpass_iter.py commit --state ... --edited "$j\inpainted.png" ...
```

`invar` raised `SystemExit` on the ANDON. **PowerShell continued to the next statement anyway** —
there is no `&&` between them and I did not check `$LASTEXITCODE`. So the gate fired *and*
47,020 texels were written to the atlas, holes 719,503 → 672,483.

The gate did its job. The harness I built around it did not. Batching the check and the
irreversible step into one uninterruptible call **removed the gate's ability to stop anything**,
which is worse than not having written it — it produced a PASS-shaped run log entry for a FAILED
condition. Six strokes of chained calls had trained me that the pair always ran together.

**The rule I broke is my own first rule: stop at every gate, never improvise past one.** I did
not decide to proceed; I built something that could not stop. Those are the same outcome.

## 2. What the gate found

```
[invar] outside the dilated figure: 645,860 px
        |edited - emitted|  mean 0.041  max 92.0 levels
        pixels over 4 levels: 597 (0.092%)   largest connected component 202 px
ANDON: CONCENTRATED — 202 px >= 200. HALT.
```

| stroke | camera | largest hot component |
|---|---|---|
| 1 | y+090 | 56 px |
| 2 | y+270 | 87 px |
| 3 | y+045 | 18 px |
| 4 | y+135 | 83 px |
| 5 | y+225 | 10 px |
| 6 | y+315 | **2 px** |
| **7** | **y+000_e+55** | **202 px** |

**202 is not a hair over an arbitrary line — it is 2.3× the highest of six clean measurements.**
The threshold was written into `brush_cloud_step.py` before any stroke ran; I am not re-arguing it
now that it has fired.

### Where the blob is, and what it is

```
largest component  202 px   bbox y 377-394  x 370-385   (17 x 15)
its residual       median 84.5   max 92.0 levels
figure bbox        y 357-763  x 181-570
```

**It sits inside the figure's bounding box but outside the figure mask** — a pocket of the
synthetic 0.42 grey that the elevated camera sees *through* the subject, between the raised
greatsword and the head. The inpaint filled it, at a median 84.5 levels of change. Eight hot
components in all (202 / 126 / 82 / 73 / 53 / 45 / …), so it is a cluster of pockets, not one
stray.

This is a **structural** change and the shape test called it correctly: a codec residual is
uniform and sub-unit (the six clean strokes ran 0.016–0.037 mean with ≤ 87 px components); an
84.5-level blob is content.

**What I will not do is argue it is harmless.** The reading that it *might* be — that
`texpass_iter`'s commit guard takes its corner median from the 8×8 frame corners, which are
~200 px from this blob and so probably unmoved — is a post-hoc reading of a result the
pre-registered rule already judged. Amendment 30 said the licence rests on *outside-mask pixels
returning unchanged*, and they did not. Whether the licence survives on a narrower premise is a
ruling.

## 3. State, exactly as it stands

**Left untouched deliberately.** I have not rolled back, because remediation after a fired gate
is a ruling, not an executor's call — and because a partial rollback would desync the state:

```
state/atlas.png        POST-stroke-7  (47,020 texels written)
state/atlas.prev.png   PRE-stroke-7   (commit copies the atlas before writing)
state/holes.png        POST-stroke-7  — no .prev, overwritten in place
state/styled_mask.npy  POST-stroke-7  — no .prev, overwritten in place
```

So `atlas.prev.png` alone cannot restore the pre-gate state; the hole map and styled mask have no
prior copies.

**But the pre-stroke-7 state is exactly reconstructible**, and that is worth more than a
rollback file: re-seed from `stage1_8cam.png` + `_holes.png` + `_styled_mask.npy`, then replay
commits 1–6 from the artifacts already on disk. All six are present and complete:

| job | `inpainted.png` | `cam.json` |
|---|---|---|
| y+090_e+00, y+270_e+00, y+045_e+00, y+135_e+00, y+225_e+00, y+315_e+00 | all Y | all Y |

`commit` is deterministic given `--edited` and `--cam`, so the replay reproduces the state
bit-for-bit. Stroke 7's own image is preserved at `job_y+000_e+55/inpainted_s770700.png`
regardless of what is decided about it.

## 4. The six clean strokes

| stroke | camera | hole px in mask | texels committed | holes after | invariance |
|---|---|---|---|---|---|
| 1 | y+090_e+00 | 19,065 | 2,507 | 746,644 | PASS 0.037 lv, cc 56 |
| 2 | y+270_e+00 | 22,725 | 3,859 | 742,785 | PASS 0.023 lv, cc 87 |
| 3 | y+045_e+00 | 25,818 | 2,017 | 740,768 | PASS 0.022 lv, cc 18 |
| 4 | y+135_e+00 | 22,157 | 4,103 | 736,665 | PASS 0.021 lv, cc 83 |
| 5 | y+225_e+00 | 23,352 | 6,526 | 730,139 | PASS 0.025 lv, cc 10 |
| 6 | y+315_e+00 | 32,302 | 10,636 | 719,503 | PASS 0.016 lv, cc 2 |
| — | **six-stroke total** | — | **29,648** | 719,503 | all PASS |
| 7 | y+000_e+55 | 34,234 | *47,020 (committed past a fired gate)* | *672,483* | **ANDON** |

**Note the ordering effect the loop's own header predicts.** Commits grow as the spiral proceeds —
2,507 → 10,636 — because each stroke sees more already-painted context. The elevated camera at
stroke 7 then jumped to 47,020, over four times stroke 6, and is also the one that tripped the
gate. Those two facts sit together and I am not asserting a causal link between them.

### And a correction to my own pre-registered ceiling

I bounded the brush arm at **26.3% of holes / 197,399 texels** and projected ≤ 8.2% of valid as
brush provenance. Six clean strokes delivered **29,648 texels — 4.0% of holes, 1.2% of valid.**

The bound was not wrong as a *reach* measurement; my reading of it was. `brush_reach.py` counted
hole **texels** a camera can see. The brush paints into a **752×1024 render**, so what it can
deliver is capped by hole **pixels** in that image — 19–34k per view — and many texels share a
pixel. A texel-space reach ceiling was never a delivery forecast, and I presented it as one.
Logged rather than escalated per Amendment 31, and recorded here because the projected provenance
mix in the pre-flight is now known to be optimistic on the brush term.

## 5. What is decided elsewhere

1. **Is stroke 7 banked or replayed out?** The reconstruction path is above and costs minutes.
2. **Does the corner-median licence survive?** Its premise (outside-mask pixels unchanged) is
   measurably violated; whether the narrower premise (the 8×8 corner medians specifically) holds
   is a different claim that would need its own check.
3. **Does stroke 8 (y+180_e+55) run?** It is the other elevated camera — the same class as the
   one that fired.
4. **Should `invar` be unable to be bypassed?** The durable fix is to make the check a
   precondition inside `commit` rather than a separate call a shell can walk past. That is a code
   change to a route-active tool and I have not made it.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Seven workflow JSONs saved before submission; run log carries job ids, input hashes, cloud names; strokes 1–6 replayable from on-disk artifacts, which is what makes the state recoverable |
| ANDON_AUTHORITY | **1** | **The honest score.** The gate fired correctly and I had built a harness that could not act on it. Stroke 8 halted, nothing rolled back or argued away — but a gate that cannot stop the next step is not a gate, and that was my construction. Remediation named in §5.4 |
| NAMED_COMPENSATORS | **2** | No compensator existed for the commit — `atlas.prev.png` is partial and the hole map has none. The replay path is the compensator and it is documented with its artifacts verified present, but it was found after the fact rather than named before |
| DECOMPOSE_BY_SECRETS | **2** | Emit/commit/brush untouched; the failure is localised to one stroke and one shell invocation |
| UNCERTAINTY_GATED_HUMANS | **3** | The tempting reading (corners are far from the blob, so it is probably fine) is named and explicitly not acted on. Four open questions stated, none answered |
| EXTERNAL_VERIFIER | **2** | The invariance check is an independent instrument and it caught a real structural change that six clean strokes had calibrated it against |

---

**HALTED at stroke 7 of 8.** Six strokes clean and replayable, stroke 7 committed past its own
fired gate through my scripting error, stroke 8 not run, nothing rolled back, nothing retuned,
0 credits spent throughout.
