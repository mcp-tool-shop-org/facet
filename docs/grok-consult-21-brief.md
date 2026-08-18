# Grok build #21 — the prompt is not an artifact yet, and the sidecar shows exactly which fields are missing

**2026-08-17, facet advisor seat.** Twenty briefs, twenty chips held. #20's chip was verified
by running all three discriminating cases: neither flag → typed `canon_gate.Andon` with
`--outdir` never created; `--no-canon --subject W3` → **refused** ("W3 has surfaces");
`--no-canon --subject GALLEON` → proceeds and announces. The escape cannot be worn by a
subject that has canon, which is the checkbox trap closed by construction.

*Everything below the line is the paste block.*

---

# Twenty for twenty. The gate is fail-closed. Now: a generation that cannot be replayed is not a recipe, and ours records twenty fields while missing every one that says WHICH model made it.

## What landed since #20, and one number that bears on the studio

An Opus seat ran the density question against the plates already paid for. **The answer is no,
and it is structural**: zero elements in the corpus hold their phrase constant while the count
around them varies *and* are capable of being absent. No re-read fixes that.

What it did get is a one-sided bound, from five prompts at one camera with **byte-identical
control, mask and seed 770700** — so the prompt is genuinely the only variable. Ladder:
**ARMOUR 10 → BRACER 11 → N11 12 → SPEC/CONTRA 17** unique elements, against a canon target
of **19 the corpus never reaches.** Calibration interval [0.84, 17.09], both endpoints
measured in the same run.

- widest count change, **+7 elements** → ΔE 4.26, **21%** of the interval
- an **identity flip at Δcount zero** → ΔE 17.09, **100%** of it
- **not one** of the nine always-named elements drops across a 70% count rise

**Firmly closed:** count over 10→17 removed nothing that was present at 10. **Not closed:**
"count has no effect" — above 17 is unmeasured, and the canon target is 19. The readout you
built is what keeps that honest, and it now has a number to sit beside: **the studio can tell
an author when a prompt has left measured territory.**

It also corrected the record twice: **the headroom element is N10, not N11** (N11 is
constant-absent at every count and carries no variance), and it nearly overturned the N9
confound before catching itself on the sheet — naming changed the panel's *treatment*, not its
presence. It logged reading a response measure as a presence measure as its own miss.

## The finding this round exists for

`restylize_views.py:296` already writes a provenance sidecar per view. **It is good, and I
enumerated it before writing this brief rather than commissioning something that exists.** It
records twenty fields:

> `output` + `output_sha256` · `input` + `input_sha256` · `mask` · `mask_source` · `prompt` ·
> `negative` · `prompts_file` · `prompt_from_file` · `seed` · `steps` · `cfg` · `denoise` ·
> `lora_w` · `cn_strength` · `canny_low` · `canny_high` · `bg` · `contour_width` · `tol` ·
> `erode` · `control_px` · `figure_mask_pct_of_frame`

**Now read what is NOT in that list.** Not one field says *which model produced this image*:

| missing | why it matters |
|---|---|
| **checkpoint identity** | no name, no hash. Two runs of the same recipe against different weights are indistinguishable in the record. |
| **LoRA identity** | `lora_w` is a *strength*. Nothing records **which** LoRA — and the whole route's identity thesis rests on a style LoRA. |
| **sampler / scheduler** | not recorded at all. |
| **library + driver + hardware** | the hardware boundary is *already known to matter here* — this project measured a cross-boundary residual at ΔE 0.84 against a 1.07 no-response floor, and E55 just used that same 0.84 as its calibration floor. |
| **the canon it was gated against** | the gate now refuses uncovered prompts. Nothing records *which canon version* let this one through. |
| **an identity for the prompt itself** | no immutable id, no alias. A prompt is a string in a field. |

And the standard is **not enforced**: E53 measured that `facet_E08\SPEC\` carries **no**
`w3clay_0_gen.json` at all, where `BRACER/`, `N11/` and `ARMOUR/` each do. The one arm whose
prompt mattered most to two later rulings is the one with no sidecar, and the gap was found
only because a seat went looking.

## The evidence, with its gate status stated

From #19's research grounding. ⚠ **Most of these returned `not_addressed` from the citation
oracle**, which reads title+abstract only — existence-verified, groundedness unverified.
Motivation, not proof; read the source before making any of it load-bearing.

- **A seed does not replay a generation.** HF's own reproducibility docs: results "may not be
  reproducible between CPU and GPU executions, even when using identical seeds," and complex
  pipelines should not expect similar results across GPU hardware or PyTorch versions.
  *(Primary doc, directly quoted — the firmest item here.)*
- **Three independent vendors converged on IMMUTABLE VERSION + MOVABLE ALIAS.** MLflow's
  registered prompt is immutable with mutable aliases; LangSmith gives each push a content
  hash independent of environment tags; Weave's `weave.publish` creates an immutable ref.
  **Convergence across competitors is the load-bearing signal, not one vendor's opinion.**
- **DSPy's own docs state its save captures only "learned state"** and does **not** preserve
  dataset version, seeds, model/provider or package versions — those "must be recorded
  separately." The framework closest to this problem names the gap.
- **Hash the weight tensor, not the file.** Civitai's LoRA hash covered the whole safetensors
  file including mutable metadata, so identical weights could hash differently
  (civitai/civitai#742).

## What to build

Your call on scope, as always. The shape I would defend:

1. **A generation record with an identity** — immutable content id for the recipe, separate
   from any movable pointer. The sidecar is 90% of the fields already; this is mostly adding
   the ones that name the *producer*, and giving the whole thing an id.
2. **Extend, do not replace.** Twenty fields are correct and in use; a new format that orphans
   the recorded sidecars would break the replay of arms this repo still cites.
3. **Make the standard enforceable.** A generation that writes an image and no sidecar is the
   `SPEC/` hole. Where the sidecar is skippable, it will be skipped.
4. **Record the canon version at the gate.** The router now refuses; what it *allowed* should
   be as recorded as what it refused.

## Argue

1. **What is honestly pinnable from here, and what is not?** We generate on **Comfy Cloud**
   through an MCP transport — checkpoint hashes and driver versions may simply not be visible
   to us. **A field we cannot fill must not exist as a field that reads as filled.** Say what
   is reachable, and design the unreachable ones as explicitly-absent rather than omitted.
2. **Does a CLI repo have any business with quick / advanced / assist modes?** #19's grounding
   says structured fields beat a free-text box (SSIM 0.648 vs 0.479) and that real expert
   practice is 3–5 term edits on one long prompt — but every one of those studies measured a
   **GUI**. We have flags and JSON files. **If tiered modes are a UI answer to a UI question
   and do not belong here, say so** — that is a more useful answer than a mode flag nobody
   uses, and #19 already recorded that no three-tier prompt UI has ever been evaluated.
3. **Where does the immutable id come from?** Content hash of the recipe, a registry, or a
   commit? Note the repo's own precedent: `dispatch.lock.json` shapes exist elsewhere in this
   studio, and the index's own determinism leg is **byte-identity with a pre-registered
   fallback reported as the weaker claim it is**. Whatever you pick, normalise text (CRLF→LF,
   NFC) before hashing — a line-ending drift already broke a lock in this studio once.
4. **Is the LoRA reachable at all?** If we cannot hash the weights we use, the honest record
   says so rather than hashing a filename and calling it provenance.
5. **Anything unnamed.** Nine rounds running you have cut a brief down and been right.

## Constraints

No GPU, no cloud generation, **no credits**. Read `E:\AI\training\facet_E*\`; write to none of
them. Change-set uncommitted for the advisor's fold. Gates `raise`, never a bare `assert`.
Tests ride the commit. **Next free test file is `t96`.**

⚠ **PUBLIC SURFACES ARE LEAD-AUTHORED AND ARE NOT YOURS THIS ROUND.** `README.md`,
`README.*.md`, `CHANGELOG.md`, `SHIP_GATE.md`, `site/**`, and repo metadata are written by the
advisor under a studio law earned the hard way. **This is a change from earlier rounds** —
#18's change-set touched `CHANGELOG.md` and that was mine to catch, not yours. If your build
implies a change to any of them, **say so in your report and I will write it.**

⚠ **An Opus seat is live** under `E:\AI\training\facet_E56\`, asking whether an honest
automated check can separate an asset the Director rejected from one he accepted on the
wrong-material class. It is fenced **off** `tools/canon_gate.py` and `tools/canon_worksheet.py`
— those are yours — and off every public surface. It has `t97` and writes
`docs/experiments/E56-wrong-material-check-report.md`.

**Count surfaces are at 1319 / 1265 / 54.** State what your change-set assumes; the advisor
reconciles after both land. Note the reconciler's own two traps, now in the law book: a bare
digit replace corrupts the CI run id containing `1266`, and `README.fr.md` writes its counts
with a non-breaking space, so a plain replace silently half-updates it.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Twenty for twenty, and a round where the chip loses is still reported.
