# E37 Phase 2 firing pass — HALT after job 1: the masked repaint did not confine, and the mechanism is the init image

**Seat:** executor · **Written:** 2026-08-15 · **Spend: 51 → 52 of 80.** One of six
pre-authorized repaints fired. **Five NOT fired.** The v0 lift is DELIVERED at the ruled
+12 rung.

---

## 1. Ritual

| leg | result |
|---|---|
| E15 scratch `--db` | **PASS** — all four legs, exit **0**; seeded set **19 / 19**; determinism leg byte-identical; **37 experiments** |
| VRAM watchdog | **ADVANCING** on two reads — heartbeat `18:57:01.597` → `18:57:54.090`, CSV **430,551 → 431,677** bytes. State `ok`, VRAM **7,339 of 32,607 MiB — 23,861 below the 31,200 ceiling** |
| manifest gates | **HELD** — E33 116/116 · E34 84/84 · E35 335/335 · gate C **7,312 files, delta +0 files / +0 bytes** across all eight subtrees |
| receipts | `facet_E37\phase2fire\` — outside every protected tree; append-only, nothing written over `phase2\masks_v2\` |

*(`_watchdog_TRIPPED` on disk is stale — `2026-08-15 16:46:34`, a RAM kill from a prior
session. State reads `ok` on both live reads.)*

---

## 2. ⚑ A gate FIRED before any job: the held-pixel guarantee, one pixel

The firing seat re-ran the held-pixel check on the masks about to fly. It fired on v7band.

| operand | reading |
|---|---|
| held rect **half-open** `[116:134, 214:236]` — the convention the ratified mask was cut against | **0.000000** over 396 px — reproduces [Ruling 22](E37-ruling.md)'s recorded value exactly |
| held rect **closed** `[116:135, 214:237]` — this checker's convention | **0.031373** (8/255) at exactly one pixel, `(x=236, y=134)`, the rect's far corner |
| v6nose, both conventions | **0.000000** |

**The ratified artifact is exactly what it was recorded to be.** The disagreement is a
boundary convention on one corner pixel, and nobody ever stated which convention the held
rect carries.

**Resolved by cutting, not by re-reading.** [Ruling 21](E37-ruling.md) already ruled this
conflict's general form — *the mask is cut, the hold does not yield* — so the pixel is
zeroed in a fresh append-only mask and the guarantee now holds under **both** conventions.
**The rejected alternative, named in writing:** reading the checker on the half-open rect
so the gate goes green is narrowing a test to make a red gate pass. The edit is
**shrink-only** and asserted so by a raising check — v7band support 7,678 → 7,677, one
pixel, everything else unmoved, nothing grew.

### 2a. Three legitimate mask counts, reconciled

`masks_v2.json`'s `core_px` reproduces **exactly on all eight** as the hand-placed
polygon's fill (v7band = 7,395 fill − 814 held island = **6,581**). The ladder's
*"8,908 texels"* is the **α > 0.5** count of the same mask. `α = 1.0` gives 7,826. Three
objects, three numbers, all reproducing — recorded here so they are never read as a
discrepancy again.

---

## 3. The mask/view pairing could not be verified from the upload name

The server assigns upload names by its own scheme. Checked against the local file:
**md5, sha1, sha256, sha384, sha512, blake2b, blake2s, sha3_256 — none match**, and
phase-1's payload names are not sha256s of any PNG in the tree either. **My first check
assumed the name was a content digest and returned 12/12 mismatch** — which is the
signature of a wrong premise, not of twelve mis-paired uploads. Owned, and the check
replaced with one that can actually fail: the end-to-end locality test in §4.

`upload_manifest.json` records the local sha256 of all twelve uploaded files against the
server name they received.

---

## 4. ⛔ THE HALT: job 1 did not confine, and its falsifier is what proves it

**Why one job and not six.** [Ruling 24](E37-ruling.md) pre-authorizes the repaints to fire
behind the cleared walk with no further round-trip, and firing them as a batch was
available. They were sequenced instead — one job, verified end-to-end, then the rest —
because §3 had just established that the mask/view pairing **cannot be verified before
submission**, only from a result. That ordering is what kept the failure to one job
instead of six. It is a sequencing choice inside the authorization, not a narrowing of it.

Job 1 = **v6nose** — the phase-1 report's strongest single defect — prompt id
`b8c7c111-f655-47f9-9320-5ab54042e2bf`, completed, no warnings. Payload diff against the byte-pinned base is **exactly** 5 added nodes +
3 rerouted fields; seed 2026081511, denoise 0.92, `cn_strength` 1.0, init and control all
byte-preserved. Dry run validated with zero warnings.

**The locality check and its falsifier:**

| mask compared against the v6 repaint | dE inside / outside | ratio | hottest 0.5% inside mask |
|---|---|---|---|
| **v6nose — the CORRECT mask** | 24.54 / **13.37** | **1.8×** | **0.1%** |
| v3ear — wrong view's mask | 45.57 / 13.20 | 3.5× | 0.4% |
| v5ear — wrong view's mask | 38.79 / 13.23 | 2.9× | 1.7% |
| v7band — wrong view's mask | 42.69 / 12.82 | 3.3× | 3.4% |

**The correct mask scores worst.** dE outside the mask is 13.37 and the hot region spans
rows 122–936 — the whole figure. A confined repaint cannot do that.

**What kind of change it is, measured before deciding what caused it:**

- **Structural, not a colour transform** — outside the mask, per-channel sd (15.01 / 6.75 / 12.11) dwarfs the means (−0.70 / −0.08 / −0.19).
- **Not a global colour map** — the background collapsed from spatially varying (corners 186 / 182 / 204 / 190) to essentially constant (175.6,167.8,162.3 · 175.6,167.8,162.8 · 175.0,167.8,163.1). **A linear map cannot flatten a gradient**, so `ColorMatchV2` cannot be the sole cause.
- **The mask targeting is correct** — the overlay puts the green mask squarely on the nose wedge.
- **The geometry held** — same silhouette, ear and nose placement; the ControlNet still constrained.
- **The register is destroyed** — warm wood → pale near-neutral with red rim accents.

### 4a. The mechanism: the unmasked region reverts to the INIT, and the init is CLAY

`comfy/samplers.py:637-641` blends
`out = out * denoise_mask + self.latent_image * (1 - denoise_mask)` — outside the mask the
result is restored to **the init latent**. On this route the byte-pinned phase-1 payload is
an **img2img from the clay render** (`node 9` = `stageB/clay8/armwoodclay_6.png`), *not*
from the twin being repaired.

**My first version of this prediction was not confirmed and I say so**: raw dE to clay
9.31 against 13.37 to the twin, medians near-identical (7.78 / 7.34) — closer to clay but
not close to it. The reading only lands once the colour transform is fitted out:

| source, fitted to the repaint over the **unmasked figure** (52,731 px) | raw dE | **after one global affine map** |
|---|---|---|
| **the init CLAY render** | 19.32 | **7.13** (median 6.27) |
| the phase-1 wood TWIN | 47.86 | **17.99** (median 12.46) |

**The unmasked region is the clay render, recoloured** — 2.5× better explained by clay
than by the twin, and the sheet shows it at native: panel 2's figure is clay-white like
panel 4, not wood like panel 1. The chain is: outside the mask the sampler restored the
**clay**, then `ColorMatchV2(mkl, ref = wood twin)` dragged the whole frame warm — which is
why the backdrop moved 155 → 176 and why the result is neither clay nor wood.

### 4b. What this means for the recipe, and why it is not mine to change

[Ruling 26](E37-ruling.md)'s firing recipe — *"the byte-pinned set-A payload +
SetLatentNoiseMask between VAEEncode and KSampler"* — **byte-pinning the payload pins the
clay as init.** Both nodes were schema-verified live and both behave exactly as their
schemas say; **schema verification is not behavioural verification**, and neither seat
could have seen this from the contract.

The apparent repair is one field — node 9's `LoadImage` becomes the original set-A twin,
the control unchanged — but that **edits the byte-pinned payload the ruling specified**, so
it is a ruling, not an executor's call. Reported here rather than tried.

**And the two levers went in together.** `SetLatentNoiseMask` and `ColorMatchV2` were
introduced in the same job, so their contributions cannot be apportioned from this
result — the repo's own law, arriving again: *"one variable" is a property of the
dependency graph, not of the parameter you edited.*

---

## 5. Item 1a — the v0 face tone lift, DELIVERED at the ruled +12 rung

Local, deterministic, zero cloud, append-only in `phase2fire/v0lift_p12/`. Unaffected by
§4 — it touches no job.

| region convention | original | **+12 rung** | measured Δ |
|---|---|---|---|
| α = 1.0 core (7,826 px) | 42.70 | **54.70** | **+12.00** |
| α > 0.5 (8,908 px — the ladder's region) | 43.18 | **54.97** | +11.80 |

**It reproduces the ratified ladder rung**: same medians on both conventions, **max pixel
difference 1**, **19 px differing of 376,832**. The recipe reproduces its output, and the
43.18/42.70 and 54.96/54.70 pairs are the two region conventions of §2a, not a
disagreement. No pixel outside the lift mask moved (raising check).

### 5a. ⚑ What the walk found that no metric reported: the lift brightens the backdrop

Walked at 3× on the head sheet, the lift's **rectangular boundary is visible on the
background** — pale strips beside the skull and a pale band below the chin. Measured
against the view's raycast figure mask:

| | |
|---|---|
| lift mask **support** (α > 0) | 10,034 px |
| **on** the figure | 9,391 px (93.6%) |
| **off** the figure — backdrop raised by the lift | **643 px (6.4%)** |
| how far the backdrop moved | mean **+6.01 L\***, median +4.73, **max +12.15**; 306 px above +6 |
| the step at the mask edge | backdrop **77.10 L\*** just inside against **74.79** just outside — a visible **+2.30 L\*** rectangle |

**This is a property of the ratified mask, not of this seat's compositing**: the same
measurement on the prior seat's ladder `v0_lift_p12L.png` returns **643 px, +6.01 mean,
+12.15 max** — identical. The Director ruled the rung from that ladder.

**Why the receipts did not show it**: `masks_v2.json` records `core_off_figure_pct: 1.0`
for v0lift — that is the **core** (polygon fill). The thing that shows on screen is the
**support**, which is 6.4% off-figure. §2a's count-convention family again, this time
deciding whether an artifact is visible.

[Ruling 22](E37-ruling.md)'s criterion — *every mask boundary lands on plain wood* — was
about not crossing drawn features, and it holds. It does not bound a lift that raises
**everything inside the mask, including backdrop**, and a rectangle over a round skull
necessarily contains backdrop at its corners.

**Not repaired here.** The known move is to intersect the lift mask with the raycast
silhouette — the **E08 A27** precedent, *one mask cannot answer two questions* (cited bare,
as CLAUDE.md cites it; the pattern is discussed at
[E08-ruling-gate0.md:2152](E08-ruling-gate0.md)) — but that edits a ratified mask, so it is
a ruling. Reported with its numbers and left standing.

---

## 6. Sheets, at native resolution, walked at this seat

| sheet | size | walked |
|---|---|---|
| `sheet_v6_repaint_native.png` — original \| repaint \| mask overlay \| init clay render | 1512 × 1054 | **1:1, yes** |
| `sheet_v0_lift_p12_native.png` — original \| +12 \| lift mask | 1136 × 1054 | **1:1, yes** |
| `sheet_v0_lift_p12_head3x.png` — head band at 3× | 1382 × 390 | **yes** |
| `diag_v6_locality.png` / `diag_v6_head3x.png` — dE map + head crops | — | yes |

All are under the display cap and were read at 1:1 — no downscaled read decided anything
here. **To the advisor's walk first, then the Director's eye.**

---

## 7. Tests ride the commit

`tests/test_t73_fire_repaints.py` — **10 tests, all passing**. Each constructs the failing
case rather than only the passing one:

- the closed-vs-half-open held rect, with the corner pixel pinned by name
- hardening is shrink-only over a random mask
- the three count conventions separate (16 / 20 / 24 on a built fixture)
- the union ANDON **fires on a deliberately overlapping pair** — the fixture asserts the overlap is real first, or the check could not fail
- an unconfined repaint **collapses the locality ratio to 1.0** — the constructed twin of what job 1 actually did
- a repaint identical to its original reads dE **exactly 0.0** — [Ruling 26](E37-ruling.md)'s NO-OP requirement, so six no-ops cannot wear six receipts
- no ANDON in the tool is a deletable `assert`, and the module's gates survive `-O`

The `-O` test **caught a real defect in my own tool** — a non-ASCII character against the
repo's ASCII law — which was fixed rather than waived.

Count surfaces moved in this commit per the T34 law: **1053 → 1063 total, 1008 → 1018
hermetic**, 45 artifacts unchanged, across `SHIP_GATE.md`, `docs/advisor-kickoff.md`,
`site-config.ts`, both handbook pages and all eight READMEs (two digit sites each). T34
passes 50/50.

### 7a. An inherited red gate, repaired by conforming to the record

**T06 (`no CRLF in tracked text files`) was already failing at `93f3d1b`** on
`docs/experiments/E37-ruling.md` — a file this seat never edited. Measured: the **committed
blob is clean (0 CRLF, 892 LF)**; only the **worktree copy** carried 9 CRLF, left behind by
the Ruling 26 / addendum writes. `.gitattributes` pins `*.md text eol=lf` on both sides, so
LF is the mandated form.

Normalized, and the claim checked rather than asserted: the worktree file with `\r`
removed is **byte-identical to `git show HEAD:`** (55,851 → 55,842, the 9 CR bytes), and
after the fix `git diff` exits **0** with nothing staged. **No committed byte of the ruling
moved** — the working copy was conformed to the record and to the repo's own pinned policy,
which is the opposite of revising a ruling. Reported here because a red gate this seat
inherited and silently fixed would be a gate nobody knew fired.

### 7b. My own truncated read, caught by the law that exists for it

The first full-suite run was captured through `| tail -8`, so its file held **7 FAILED
lines against a summary of 26** — I could not have known what the other 19 were. Re-run
complete to a file with no pipe. The repo's own law, committed by the seat quoting it.

---

## 8. State

- **Spend 51 → 52 of 80.** Five pre-authorized repaints **NOT fired**.
- Set A is **untouched**. `phase2/masks_v2/` is **untouched**. No protected tree was written to; manifest gates HELD at open.
- The v0 lift at +12 is delivered and reproduces the ratified ladder.
- Nothing was tuned, no threshold moved, no gate re-read to make it pass.
- The masks, payloads, upload manifest, job output, diagnostics and sheets are all on disk under `phase2fire\`.

**What the next ruling decides:** whether the repaint's init becomes the set-A twin (a
one-field departure from Ruling 26's byte-pinned payload), and whether the two levers are
separated before the remaining five fly.
