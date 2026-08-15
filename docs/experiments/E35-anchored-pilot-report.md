# E35 — anchored pilot sequence, executor report

**Run 2026-08-14** at the Director's word ([E35-ruling.md §7](E35-ruling.md)). Bands
registered blind in two stages and pushed before the jobs they cover: A1/A2 at `cdea731`,
A3 at `d206a96`.

**Five GPU jobs, exactly the ≤ 5 the sequence allowed. 38 → 43 of 60.** One additional
submission failed *validation* with no GPU execution and is accounted separately.

**The anchor worked and it paid for itself immediately.** A1 established the served template
produces images; A2 established a **working 2509 configuration on our subject**; A3 then
found that one specific change — feeding a natively-rendered frame instead of letting the
scaler resize ours — **corrupts the output, three times, three different signatures.**

---

## 1. The sequence, in order

| stage | what changed | GPU | result |
|---|---|---|---|
| **A1** | nothing — `run_template`, template defaults | 1 | **1024×1024, 216,691 colours.** The dalmatian its own prompt asks for |
| **A2** | +our clay via node 78, +the v-next prompt. Scaler KEPT | 1 (+1 validation fail) | **672×1568, 43,984 colours. A clean clay mannequin** |
| **A3a** | A2 + our clay rendered natively at 672×1568, +seed 770700 | 1 | **CORRUPTED** — register gone, horizontal chromatic streaks |
| **A3b** | A3a with turbo OFF (20 steps, cfg 4.0, no LoRA) | 1 | **CORRUPTED** — heavier streaking, whole frame |
| **A3c** | A3a **without** the seed override (mechanical repeat) | 1 | **CORRUPTED** — blocky red/blue/white patchwork |

Sheet: `facet_E35\diag\E35_anchored_sequence_sheet.png`, all five beside the reference.

## 2. What the sequence isolated

**A2 differs from A3 in exactly two things**, and the repeat separated them:

- the **input frame** — A2 fed the node our recorded 352×1024 clay and let it resize;
  A3 fed it a 672×1568 clay rendered natively at that frame
- a **seed override** (`433.image3 = 770700`) that A2 never carried

A3c removed the seed override and kept the native frame: **still corrupted.** So the seed is
exonerated and **the natively-rendered frame is the cause**, three runs to one.

⚠ **The mechanism is not established, only the trigger.** Both inputs are well-formed RGBA
with near-identical statistics (native 672: mean 159.1/159.4/161.7, 2,620 unique colours;
recorded 352: 160.2/160.6/162.8, 2,303) and both end at a 672×1568 latent. What differs is
that A2's image went *through* `FluxKontextImageScale`'s resample and A3's did not — the node
is a no-op on an already-legal shape. **Why a resampled input survives and a native one does
not is unanswered, and I have no authorised job left to ask.** Candidates I did not test:
the wider framing (our native render puts more background around the same figure, because
`h_ext` grows with the frame while the figure does not), and the higher spatial frequency of
a native render against a 1.909× lanczos upscale.

## 3. ⚠ A2 is NOT measured, and that was pre-registered

The A1/A2 bands say, before A2 ran: *"A2 is a mechanical stage; no class number is read from
it, and I say so before it runs rather than after."* The reason holds and got stronger:
replaying the scaler's transform exactly (352×1024 → ×1.909091 → 672×1955 → centre-crop
1568, top offset 193) produces a mask that registers to A2's figure at **IoU 0.9531** — but
the same transform maps the recorded head band (rows 60–220) to rows **−78…227**, i.e. **the
top of the head is outside A2's frame**. A class number read there is over a different region
than the recorded twin's.

Reaching for that number now — after A3 failed and with nothing else to show — is exactly
what the pre-registration existed to prevent. **The transform replay is recorded as a
finding** (it is how a successor arc would measure an A2-shaped result) **and no pale, dark
or register figure is read from A2.**

## 4. Bands, scored

**A1/A2 bands** (`cdea731`) — **6 of 6 HIT**:

| band | measured | verdict |
|---|---|---|
| A1-P1 non-degenerate, > 1000 colours | 216,691 | **HIT** |
| A1-P2 frame is a Kontext shape | 1024×1024 | **HIT** (weakly — square is the least discriminating member) |
| A2-P1 non-degenerate | 43,984 | **HIT** |
| A2-P2 frame is NOT 352×1024 | 672×1568 | **HIT** |
| A2-P3 frame is **672×1568** | 672×1568 | **HIT** |
| A2-P4 subject survives as a clay mannequin | it does | **HIT** |

**A3 bands** (`d206a96`) — **1 HIT, 1 MISS, 5 UNMEASURABLE**:

| band | predicted | measured | verdict |
|---|---|---|---|
| A3-P1 both produce non-degenerate images (0.9 / 0.7) | yes | all three ran, all corrupted | **MISS** — see below |
| A3-P6 A3a and A3b differ visibly | differ | mean \|Δ\| 27.43, 99.5% of px | **HIT**, and hollow — both are corrupt |
| A3-P2 pale falls, 60–300 | — | — | **UNMEASURABLE** |
| A3-P3 chroma split lands (ii) | — | — | **UNMEASURABLE** |
| A3-P4 dark census 4–16 | — | — | **UNMEASURABLE** |
| A3-P5 register C\* 15–30 | — | — | **UNMEASURABLE** |
| A3-P7 identity moves | — | — | **UNMEASURABLE** |

**A3-P1 is scored a MISS on purpose, and this is the band I got right in form.** After the
pilot's P2a — which predicted "the graph runs" and was hit by a graph that ran and returned
nothing — I wrote every band in this sequence as a property of the **returned pixels**. A3-P1
says *non-degenerate*, and these three are non-degenerate by colour count while being
unusable. So the band caught more than P2a would have, and still not enough: **"> 1000 unique
colours" does not separate a clay mannequin from a rainbow-streaked one.** The next version of
this band needs a term for *the register survived*, which is measurable — C\* on the keyed
figure — and which I did not put in it.

**A3-P6 is a hit I will not bank.** It predicted A3a and A3b would differ visibly and they do,
but both are corrupt, so what it measured is two corruptions differing — not the LoRA's
contribution, which is what the band was for. Same shape as the arm slate's A2.

## 5. My errors this stage

1. **I changed two things into A3, not one.** The dispatch's A3 named the frame; I added a
   seed override on my own initiative to make A3a and A3b comparable to each other, and
   thereby confounded them both against A2. The mechanical repeat that untangled it was spent
   on my own extra variable. *One lever, and a seed pin is a lever.*
2. **My A1/A2 registration check predicted a pure scale on both axes and fired.** The render
   was right; my model was wrong (the wider frame centres the figure, a computed +66.50 px
   offset). Caught before it mattered, recorded because the check firing is what it is for.
3. **The slot-address map cost a validation failure.** I inferred from node 433's own input
   *labels* that the slot names were authoritative; the platform's error proved the reported
   **defaults** are, and the positive prompt lives at `433.image`. No GPU ran, but the
   inference was stated confidently in the bands file and was wrong.

## 6. What this arc now has

- **A working 2509 configuration on our subject** — A2: served template, our clay through node
  78, the v-next prompt at `433.image`, scaler kept, turbo defaults. Reproducible.
- **The anchor discipline vindicated**: A1 cost one job and converted "2509 is broken" into
  "our construction was broken," which the two black frames could not distinguish.
- **A measured trigger for the corruption** — native-frame input — with the seed exonerated.
- **The scaler's transform recovered exactly**, IoU 0.9531, so an A2-shaped result is
  measurable by a successor arc that wants to.
- **The slot-address map for this template**, corrected by a platform error rather than
  assumed: `433.image`→positive prompt, `433.image2`→negative, `433.image3`→seed,
  `433.prompt`→unet_name, `433.seed_1`→turbo boolean.

**What it does not have:** any pale, dark or register number from 2509. Three stages in, the
class question is still open.

## 7. Artifacts

```
E:\AI\training\facet_E35\
  k672\armclay672_1.png            our clay at the derived frame (anchored: the 352 re-render
                                   matches the recorded armclay_1.png at 0 differing px)
  k672\armclay672mask_1.png        its raycast mask; registration verified to 0.22-0.75 px
  k672\a2mask_kontext_1.png        the scaler's transform replayed onto the recorded mask
  twins\anchor_A1_template_default.png  anchor_A2_clay_vnext.png
  twins\twin_A3a_turbo_v1.png  twin_A3b_noturbo_v1.png  twin_A3c_noseed_v1.png
  diag\E35_anchored_sequence_sheet.png
docs/experiments/E35-anchored-pilot-bands.md   two stages, each pushed before its jobs
```

| stage | prompt_id |
|---|---|
| A1 | `ecc59524-1c30-462f-aa80-938dd8ce243d` |
| A2 (validation fail, no GPU) | `be8068b2-aeec-48f1-b190-1e20038671df` |
| A2 | `e7725988-0de2-4f18-ad01-68a5368649fa` |
| A3a | `492b7733-1484-467c-9029-ab857c9b14da` |
| A3b | `081282d8-7a43-4abf-8ebc-f3ba21f542e4` |
| A3c | `b8513f18-2fec-42a2-be92-a1b3b877955c` |

## 8. HALT

**At the A3 sheet, as ordered.** 43 of 60. The eight-view rebuild fits the remaining
seventeen and **is not mine to launch on any outcome** — and on this outcome there is nothing
to rebuild from: A2 is the only clean 2509 result and it sits in a frame that crops the
subject.

A negative result is a full success, and this one is narrower and more useful than the
pilot's: **not "2509 does not work" but "2509 works, and our native-frame input is what
breaks it."** One job established that, which is what the anchor was for.
