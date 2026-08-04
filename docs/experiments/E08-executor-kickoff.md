# E08 — executor kickoff

Paste this into a fresh executor session. Written by the advisor, 2026-08-04, because the
previous executor's context filled. That session's work is committed and its judgement was
consistently good — read its reports rather than re-deriving.

---

## You are the executor

```
cd E:\AI\facet && git pull
CLAUDE.md                              <- how to work here. Read first, follow exactly.
docs/experiments/E08-ruling-gate0.md   <- the ruling and its 16 amendments. The live document.
canon/W3-IDENTITY.md                   <- the test fixture you are running against
README.md                              <- measured state of every tool
```

**Your rules** (CLAUDE.md, §"Rules for an executor session"): never judge whether output is
good · state a prediction before you look and say whether it was blind · **stop at every gate,
never improvise past one** · do not write to the memory store · **a negative result is a full
success.**

The previous executor halted at four gates and refused three of its own instruments. That is
the behaviour, not an obstacle to it.

## Where this stands

The route: clay concept → mesh → render → **restylize to a "twin"** → project twins into the
UV atlas → brush the holes → dilation fill. W3 is a **test character**, not a shipping one
(Director, Amendment 14): its identity spec is a **fixture** so that "did the element land" has
a ground truth. **The product is the pipeline for future sprites.**

**Adopted and standing:**

- **A2** — projection surface comes from the **exact raycast silhouette**, never a keyed render.
  Reference coverage 28.4% → **39.1%** of valid, 53.8% → 74.2% of reachable.
- **Fitted-background keying** — a quadratic over a border ring, replacing corner-median, which
  has now failed three times. Reduces to the corner median on a flat field, so prior numbers
  stay comparable.
- **The bbox andon** — a keyed mask is checked against the geometry before any number is read
  from it.
- **Per-view prompts + provenance sidecars** in `restylize_views.py`.
- **`canon/twin_{front,back}.png`** — frozen, versioned, **demoted**: a specification source and
  visual target, **never a projection reference** (they under-fill the silhouette and show a
  body that is not the mesh's).

**Architecture, ruled:** *Twins belong to a mesh. Identity belongs to the prompt.* A twin has
one job — register to the mesh. A canon element not named in the prompt is arriving by accident
and will leave the same way.

**Withdrawn, with reasons in the ruling — do not revive without new evidence:** A2R (off-canon)
· A3's erosion invariant as a *fix* (kept as a component; shape-blind, cannot tell a blade from
a shadow tendril) · A4 colour thresholding (no bimodality exists) · the blue-background arm
(parked — it breaks the twin's own mask, which is the only remaining answer to *is the paint
trustworthy*).

**Measured, and the reason the specification premise is narrower than it looked:**

| element | form | result |
|---|---|---|
| gold knee plates | head noun, **replaces** the occupant | landed |
| brown leather bracers | head noun, **replaces** the occupant | landed |
| gold trim *on* the bracer | modifier, co-located | dropped |
| a gold plate *on* each forearm | head noun, co-located | dropped (**ΔE 1.07 — no response at all**) |

> **A specification determines what occupies each surface. It cannot add a second element to a
> surface already occupied.** Hypothesis, four data points. N11 failed because we were
> *patching*; a new sprite is *specified*, not patched.

## Your task, in priority order

### 1. THE CONTRADICTION TEST — highest priority, and it outranks everything below

The previous executor measured that **14–15 of the 16 NAMED elements already arrive
unprompted**. That makes a pass-rate gate near-vacuous, and it raises the question that
actually decides whether this is a pipeline or a dwarf generator:

**For a future sprite that is not this character, will the LoRA, mesh and control supply *this
dwarf's* attributes regardless of what the prompt says?**

Name elements that **conflict** with ones arriving unbidden — *silver pauldrons* where gold
arrive, a *black* skirt where wine-red arrives — and measure whether the prompt overrides the
supplied attribute. Control byte-matched; the contradicting terms the only variable.

- **Prompt wins** → identity is in the prompt, the architecture holds, the route generalises.
- **Supplied attribute wins** → identity lives in the LoRA and mesh for those elements, the
  specification is decorative for them, and **the pipeline produces this dwarf in different
  clothes.** That is the most important negative result available here and it is cheap.

Denominator equals however many elements you contradict — a real one, by construction.
**Predictions blind, before you look.**

**This is already pre-registered and committed** (`6d2853d`, deliberately landed *before* either
image exists — that ordering is the whole evidential value, so do not restate or re-tune it):

| file | what it fixes |
|---|---|
| `docs/experiments/E08-contradiction.json` | 8 contradicted elements **counted**; the 3 co-location cases substituted for prompt coherence and reported **outside** the denominator; 5 held elements as the internal control against a global repaint. Phrase count, order and structure identical to `E08-spec-prompt.json`, so the adjectives are the only variable. |
| `docs/experiments/E08-contradiction-regions.json` | boxes placed and then tightened against zooms, **all before either image existed**, recorded in the file rather than in a shell history |
| `tools/diagnostics/e08_contradiction.py` | every box **drawn and labelled** on the sheet, every row printing the base image's own median colour inside it — the direct answer to the forearm crop that caught the pauldron edge and inverted N11's reading. Plus a crop-free hue×chroma density panel, so the gold→silver question does not depend on a hand-placed box at all. |

Whole-figure ΔE is reported first and **against N11's 1.07**, so *the supplied attribute won* is
never confused with *the model did not read the phrase*.

### 2. Step 2 — the full-spec generation

Still worth running, and **its limits are already known: it is not the specification gate the
advisor claimed.** It tests two real things — regression across sixteen simultaneous elements,
and N11 under simultaneous specification. Report the honest unit alongside any pass rate: *of
the elements that were absent, how many arrived?*

**N5 is the discriminator.** Scrollwork on the pauldrons is an addition to an occupied surface.
If it **appears where it was absent, that falsifies co-location** rather than confirming it. Get
the sign right in your prediction.

**A spec tuned until it passes is not a spec.** Halt and report; do not reword.

### 3. Arm B — eight-camera twins. Waits on 1 and 2.

Forward arithmetic: eight cameras reach 74.10% of valid; at A2's acceptance that is ~55–60%
reference coverage against the rejected asset's 28.4%. Worth a loop run — **after** the
contradiction test, which answers for one view what Arm B would spend eight views assuming.

## The environment blocker — DIAGNOSED. Start at E3; do not re-run the dead hypotheses.

A previous executor worked the ordered protocol and **falsified all of it**, including both
advisor hypotheses. Full record in Amendment 17 and in
`E:\AI\training\facet_E08\CONTRA\ENV-PREDICTIONS.md`. Do not repeat these:

- **Settled instance — dead.** Registry fetch fully drained 167/167 before submit; died at 6/20
  anyway, the same point as three prior attempts.
- **`--disable-smart-memory` — dead.** Same place, same phase, same height. The log shows the
  text encoder is never released either way.

**The actual cause:** `--reserve-vram` reserves against the **card's total**, not against what is
left after the desktop. ComfyUI's working set sat on its reserve-derived budget (24,225 and
24,673 MiB against 24,415) in both runs, and the desktop's own 7.0–7.6 GB lives *inside* the
reserve. The breach happens at 47–54 W, **inside model load, before compute starts.** It is a
reserve problem, not a workload-size one.

**⚠ The machine was rebooted, and that is a confound working against you.** The desktop baseline
was 7,030–7,604 MiB when the failures were measured. **It is now ~1,150 MiB.** At that baseline
the *old, measured-not-to-work* setting would complete — and the pass would be meaningless,
credited to the wrong cause, and it would fail again the next time the desktop is warm.

**So, ruled in advance (Amendment 17), not open for tuning:**

1. **Launch at `--reserve-vram 10.0`** via `E:\AI\training\_comfyui_start.ps1 -ReserveVramGB 10.0`
   — the rig's own launcher, which does *not* pass `--disable-smart-memory`. Sized against the
   **worst observed baseline (7.6 GB)**, not today's lucky one: 22,367 + 7,600 = 29,967, still
   1.2 GB under the ceiling. E4 predicts it is slower because something streams from system RAM;
   that cost is accepted.
2. **Record `nvidia-smi` used-MiB at the moment of launch, in your report.** Every prior
   environment number here is un-attributable without it — that is how a 6.5 GB swing went
   unnoticed.

**The ceiling stays at 31,200 MiB. The watchdog stays untouched.** It was restarted 2026-08-04
02:30 via `_watchdog_start.ps1` and verified live; if its heartbeat is stale, restart it with
that script **before** any GPU job, never by weakening the bound.

**E2 is the halt condition and the advisor has already ruled on it.** The reproduction anchor
must return sha256 `d0220e244d5ad2015639153188c488e3f3d317933dbd54eb439724fe1f57f93d`. If it does
not, **halt and report — do not proceed to the measured arms.** Every prior number in this line
was taken on the old machine state; a non-reproducing anchor means SPEC and CONTRA are not
comparable to BRACER, ARMOUR or N11.

## Do not

Re-run N11 in any wording · re-open a withdrawn arm without new evidence · project from the
canon pair · tune a threshold after seeing the number it would have to clear · treat 15/16 as a
result · escalate canon questions about a test character to the Director — **the advisor authors
fixtures, the Director gates outcomes.**

## Calibration

The advisor has been wrong repeatedly this session and the corrections are in the ruling: the
gate/ownership reorder (a no-op), the stratum area-loss gate (fired on a correct build), the
bimodality that did not exist, the registration criterion (a better-registered twin was a
different man), the grammar hypothesis (co-location fits better), and a step-2 gate with a
denominator of one. **Every one was caught by an executor running the spec as written and
reporting the evidence.** Do that.
