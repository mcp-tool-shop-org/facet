# E12 Gate 0 — predictions, written blind

**Executor session, 2026-08-05, ~20:45 local.** Committed **before any dragon mesh exists**:
no TRELLIS run has been started, `E:\AI\training\facet_next\E12_gate0\` does not exist, and
`mesh_stats.py` has not been pointed at anything. The status is **blind** in the strict
sense — the only dragon information in hand is the three staged clay PNGs, which I have
looked at at full size, and the E01 / E04 precedent numbers.

A wrong prediction is a full success. This file exists so the beast profile inherits a
calibration rather than a set of after-the-fact rationalisations.

---

## What the priors are, and where each comes from

| prior | value | source, checked this session |
|---|---|---|
| character reconstruction shells (welded) | 40–191, 92–98% of faces in the largest | [E01 ruling](E01-ruling-gate1.md) §"Shell soup" — **verified against source** |
| ship reconstruction shells (welded) | 237 / 274 / 512, largest 88.0 / 92.3 / 92.9% | [E04 Gate 0](E04-gate0-report.md) §3 — **verified against source** |
| ship reconstruction cost | 116–141 s, peak 4.4–5.6 GB | `E04_gate0/recon.log` `[GLB] … OVERALL PEAK` lines — **verified against source** |
| thin sheets at sash scale | opposing faces of a sheet closer than one triangle edge (0.77) | E07, quoted in the dispatch |
| the ship's extra shells | free-floating standing rigging returns as its own island per filament | E04 Gate 0 §3 |

**The dispatch's bet, restated so it can be scored:** a dragon's thin structure is mostly
*attached* — membranes to arms and flank, horns to skull, spikes to tail — where the ship's
was free-floating. I am betting **with** that prior on shell count and **against** an
assumption of uniformity on density.

## What I saw in the three clays, checked against the dispatch's own descriptions

Viewed at full size before writing this. All three are 1344 × 1024 RGB, staged
2026-08-06T00:11:56−04:00 by mtime — which is **~3 h 34 min in the future** against a
20:37 local session start, i.e. a UTC instant written into a local-time field. The
dispatch's reading (a UTC stamp from the staging extraction, ~20:11 local) is consistent
with that offset to the minute; these are the files it describes.

| clay | dispatch says | what I see | verdict |
|---|---|---|---|
| 00001 | quadruped forward lean, near-profile head framed by raised wings, largest head relative to frame | quadruped, all four limbs planted, body leaning image-left; head in near-profile facing image-left, both wings raised behind and around it; head visually the largest of the three | **matches** |
| 00002 | most upright stance, broadest wingspread, biggest paired horns, smallest head relative to frame | upright — hind legs bearing, forelimbs raised clear of the ground; wings spread nearly edge-to-edge of the 1344 px frame; large swept paired horns; head visually the smallest of the three | **matches** |
| 00003 | mid-stride walking pose, asymmetric swept wings | forelimb lifted mid-stride; image-left wing folded and short, image-right wing spread wide and high — plainly asymmetric | **matches** |

Common to all three, as the dispatch states and I confirm: open jaws with teeth and a
visible tongue, membrane wings with vein ridges, scale relief over neck, chest, flank and
tail, horn / spike / claw filaments, a studio-grey gradient backdrop with a cast ground
shadow, and a subject wider than tall in a landscape frame.

One thing the dispatch does not mention, recorded now so it cannot be read as hindsight:
**on 00002 both wingtips come within ~15 px of the frame edge.** On 00001 and 00003 the
subject clears its frame comfortably.

---

## The predictions

Each is stated so it can be falsified by a number this session will produce. "All three"
means the prediction fails if **any** of the three misses.

### Topology

| # | prediction | falsified by |
|---|---|---|
| **P1** | Welded shell count lands in **60–200** on all three | any mesh below 60 or above 200 |
| **P2** | All three come in **below the ship's 237 floor** — the attached-thin-structure bet | any mesh ≥ 237 |
| **P3** | Largest-shell fraction ≥ **0.95** on all three — above both the character band's floor (0.92) and every ship (0.880 / 0.923 / 0.929) | any mesh below 0.95 |
| **P4** | Ordering by shell count: **00002 ≥ 00001 ≥ 00003**, because 00002 carries the longest run of individually-modelled tail spikes and the widest membrane area | any other ordering |
| **P5** | `watertight` is **False** on all three | any True |

P3 and P1 are not the same bet and can both hold: teeth and spike tips can multiply the
shell *count* while contributing almost nothing to the face *share*.

### Form of the thin structure — the reason this subject is the new primary

| # | prediction | falsified by |
|---|---|---|
| **P6** | Wing membranes come back as **closed slabs** — a double-sided surface joined around its rim, with small but non-zero thickness — not as open single-sided sheets | a membrane with a free boundary, or one that reconstructs as a genuine zero-thickness sheet |
| **P7** | Membrane thickness is **visible on the `--clay` renders** at a grazing view (1/3/5/7) as a distinct edge rather than a hairline | membranes invisible edge-on at every view |
| **P8** | **No through-holes** in the main membrane field of any of the three | any hole punched through membrane interior |
| **P9** | The membranes' **scalloped trailing edges tear or blunt** on at least one mesh — the thinnest part of the thinnest structure | all three trailing edges clean and complete |
| **P10** | Horns and the tail ridge **survive attached** — no detached filament islands from either — while **spike or claw tips blunt** on at least one mesh | a detached horn/spike island, a missing horn, or all tips perfectly sharp |
| **P11** | The mouth cavity reconstructs **open** on all three, with teeth present as relief on the jaw rather than as separate shells | any fused-shut jaw, or teeth returning as free-standing islands |
| **P12** | Scale relief reconstructs as **geometry** — legible on a `--clay` render with no texture at all | flat clay body surface where the concept has scales |

### Proportion and framing

| # | prediction | falsified by |
|---|---|---|
| **P13** | Widest-horizontal / height > **1.0** on all three (wider than tall, as staged) | any ≤ 1.0 |
| **P14** | That ratio lands in **1.15–1.60** — above every galleon (1.114 / 1.088 / 1.041), because a wingspread is a wider thing than a hull is long | any outside the band |
| **P15** | The derived render frames are **wider than the galleon's 1072–1152**, and all three are landscape | any frame at or below 1152 wide |

### The head — the live allocation question

| # | prediction | falsified by |
|---|---|---|
| **P16** | Head-box face share lands in **8–22%** of total faces on all three | any outside the band |
| **P17** | Share is ordered **00001 > 00003 > 00002**, following the heads' apparent size in their clays | any other ordering |
| **P18** | Median face area **inside** the head box is **smaller** than outside on all three, with an outside/inside ratio between **1.0 and 2.5** | inside ≥ outside on any mesh, or a ratio above 2.5 |

P18 is the one I hold least confidently, and it is the one that bears on the profile
decision. The case for a ratio near 1.0: `mesh_character.py` runs with `remesh=True`, and a
remesh tends toward uniformity — which would mean the reconstructor grants a head **no**
density privilege from a full-figure frame. The case for a ratio above 1.0: E01 measured
3.1–4.5× more polygons on a head from a bust crop, which cannot be true of a perfectly
uniform remesh in any framing. I predict a **mild** contrast, real but far short of the
crop's factor; a 1.0 and a 3× outcome are informative in opposite directions.

### Cost

| # | prediction | falsified by |
|---|---|---|
| **P19** | Wall time **110–170 s** per mesh | any outside |
| **P20** | Peak VRAM (torch `OVERALL PEAK`) **4.0–7.0 GB** per mesh, nowhere near the 31,200 MiB ceiling | any outside, or any watchdog ABORT during the leg |
| **P21** | The loaded attention backend is reported as **`flash_attn`** despite `ATTN_BACKEND=sdpa`, exactly as E04 recorded | anything else loading |

---

## What I am not predicting, and why

- **Which dragon is better.** Not mine to say, and not measurable here.
- **Face and vertex counts.** The galleon's 939k–969k faces sit just under the 1,000,000
  `--decimation` target, so the number is at least as likely to be reporting the flag as the
  subject; predicting it would be scoring the argument, not the beast.
- **Any threshold value for `beast.json`.** No profile exists, and deriving one from three
  candidates that may all be rejected is the improvisation this dispatch forbids.
