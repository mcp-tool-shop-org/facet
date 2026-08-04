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

**Step 0 below the tasks comes first.** Nothing here runs on the local rig — read it before you
touch a GPU.

### 1. THE CONTRADICTION TEST — highest priority once step 0 clears

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

## STEP 0 — Move to Comfy Cloud. This comes before everything above.

**The local rig cannot run this job, and the reserve protocol is retired.** E3 settled it
(Amendment 18): the staged set is 7,910 + 19,483 + 3,372 + 241 = **31,006 MiB** against a
**31,200 MiB** ceiling on a **32,607 MiB** card, and run 3's working set reached **30,809** —
everything resident, nothing left for activations. **No reserve value fixes that.**

The reserve lever is also **not binding**: peak was 31.7–32.0 GB across all three runs,
independent of reserve *and* baseline. Runs 1 and 2 only looked bounded because the desktop held
~7 GB. ComfyUI stages to fill what it sees — the reboot freed 6.5 GB and the working set grew
6.1 GB. **The earlier passes succeeded because *less* VRAM was free.** Do not walk the reserve
upward; that hypothesis is dead and each attempt costs a watchdog kill.

**Retired, do not re-run:** settled instance · `--disable-smart-memory` · `--reserve-vram` at any
value · the reboot-confound protocol. All falsified, record in Amendment 17 and E3's report.

**Comfy Cloud is the studio's standing default** — the `comfy-local` skill states local is the
*fallback* and Cloud (RTX 6000 Pro, **96 GB**) is the default for image generation. Invoke the
`comfy-mcp` skill. Ninety-six gigabytes against a 31 GB working set is not a tuning margin.

### 0a. LoRA delivery — check this first, it is a hard blocker

`saltroad_style_v2_lowlr_000001500.safetensors` is a local file. Memory records the cloud
bridge's LoRA delivery as **HF-URL-only**, though the plugin now exposes `upload_file`. **If the
LoRA cannot reach the cloud, nothing below runs there.** One call to establish. Report it before
spending anything else.

### 0b. The anchor, and it is the halt

**The first cloud run reproduces N11's twin — not the contradiction test.** Every number in this
line rests on byte-matched controls; that is what makes A2 / N11 / BG2 comparable at all. Cloud
is recorded as seed-identical to the local 5090, **validated 2026-06-26** — ~40 days old, which
the freshness rule makes *advisory until re-measured*. N11's sidecar carries every parameter and
its control is byte-matched at 20,973 px, so this is a clean reproduction.

Pre-registered, so it cannot be argued after the fact:

| outcome | reading |
|---|---|
| sha256 == `d0220e244d5ad2015639153188c488e3f3d317933dbd54eb439724fe1f57f93d` | **clean pass.** The anchor holds, every prior arm stays comparable, proceed to task 1 on cloud. |
| sha differs, whole-figure median **ΔE ≤ 1.07** | **accept with the boundary recorded.** 1.07 is N11's own measured no-response floor — this pipeline's noise level, not a number invented here. Every later report states that arms span a hardware boundary. |
| whole-figure median **ΔE > 1.07** | **HALT.** Cross-boundary comparisons are void. Report and stop. |

**If it halts, the fallback is sound and not a dead end:** re-run the *anchors* on cloud —
N11, BRACER, ARMOUR — so within-cloud comparisons are valid even though cross-boundary ones are
not. That costs three generations and buys back the whole line. Do not attempt it without
reporting the halt first.

### 0c. If cloud is unavailable for a reason not listed above

Report and stop. **Do not fall back to local for a measured arm.** The ceiling stays at 31,200
MiB, the watchdog stays untouched, and a local run that happens to pass because the desktop is
cold is a number credited to the wrong cause — which is exactly the confound that cost the
previous session its E3.

## Do not

Re-run N11 in any wording · re-open a withdrawn arm without new evidence · project from the
canon pair · tune a threshold after seeing the number it would have to clear · treat 15/16 as a
result · escalate canon questions about a test character to the Director — **the advisor authors
fixtures, the Director gates outcomes** · walk `--reserve-vram` upward · run a measured arm
locally · raise the watchdog ceiling.

## Calibration

The advisor has been wrong repeatedly this session and the corrections are in the ruling: the
gate/ownership reorder (a no-op), the stratum area-loss gate (fired on a correct build), the
bimodality that did not exist, the registration criterion (a better-registered twin was a
different man), the grammar hypothesis (co-location fits better), and a step-2 gate with a
denominator of one. **Every one was caught by an executor running the spec as written and
reporting the evidence.** Do that.
