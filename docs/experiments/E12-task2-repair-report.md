# E12 handoff 4, Task 2 — the re-pair under the ruled register

**Executor session, 2026-08-06.** Task 1's derivation is `de0440c`
([E12-task1-canny-report.md](E12-task1-canny-report.md)); its predictions were registered
blind in `d347744` before any Canny ran. **This report ranks nothing and judges nothing.**
The register question — *does it read ultra-realistic and scary* — is the Director's, and the
observations below are offered as data with no verdict attached.

**0 credits. 0 re-rolls of the 1 allowed. Both jobs `succeeded` with zero warnings.**

**Look at `E12_repair/PAIR_SHEET.png` before the numbers** — clay | control | styled, both
views, full size. Then the three zoom crops at 3×.

---

## 1. What ran

| leg | result |
|---|---|
| watchdog | **alive** before every leg and reported either way — heartbeat ages 0.1–2.2 s, pid 22324, VRAM 2,134→2,250 MiB against the 31,200 ceiling. No `_watchdog_DEAD` |
| silhouettes | fresh directory, views 1/2/4/5; views 1 and 5 **anchored 0 differing px, IoU 1.000000** against `E12_pair/masks/` by the tool's own `--anchor` |
| clay | **reused read-only.** Both cloud uploads returned the **same content-hash names handoff 3 uploaded**, which is a free byte-identity proof |
| **anchor** | `e04_frame_agree` ANCHOR 1c — **0 px on both views**, run before the controls and before any upload. Legacy unconformed construction printed beside it (1 px view 5), ungated |
| prompts | `E12-twin-prompts.json` v**E12-pair-3**, rebuilt by a new committed builder; 17-term entry, view 1 full, view 5 at 11 terms; 5 full-string views asserted byte-equal |
| controls | canny **0.05/0.10** — view 1 **108,887 px** (canny 94,269 + contour 25,256), view 5 **88,717 px** (74,131 + 25,256) |
| graphs | 14 nodes each, **zero LoRA nodes**; pre-flight PASS on both; 17 links resolve, no self-link, no dangling target, no orphan |
| cloud | `estimate_credits` **0 credits**; `dry_run` **validated, zero warnings**; two submissions, both `succeeded`, outputs 1792 × 1024 |

## 2. Three guards were self-tested before being trusted

The house rule is that a check which cannot fail is not a check. Each of these was proven to
fire before it was relied on:

1. **The prompts builder** — three defect classes: a `--drop` term that is not a comma-term of
   the profile entry, a `--drop` naming a view outside `--views`, and a missing profile block.
   All three raise, exit 1, and **write no file**.
2. **The no-LoRA assertion** — a `LoraLoaderModelOnly` at `strength_model: 0.0` was injected
   into a copy of the builder after graph construction. It fired on **both** the class family
   and the card-name string, exit 1, no file written.
3. **The canny replica's anchor** — it fired for real on first use, on a genuine defect (§3).

## 3. Task 1's ANDON, carried forward because it is the session's methodological finding

The canny replica's anchor **fired**: 35,992 against `restylize_views`' recorded 36,011
(view 1) and 22,658 against 22,642 (view 5). Nothing was swept. The mechanism was isolated
before anything changed — the replica held the figure mask as **bool**, so `1.0 - fm`
promoted the composite to **float64** and ~19 px per view crossed the `uint8` truncation and
then a Canny threshold. `control_image` writes `.astype(np.float32)`; conforming to it
reproduced both digits exactly.

**Second instance of this class in two sessions** (Ruling 9a was a normalisation that cancels
mathematically and not in float32). The rule caught it both times and is quoted at the site:
*an anchor is computed with the source's own arithmetic, not with arithmetic equivalent to it.*

It was then confirmed a third way, for free: **the real tool, run at 0.05/0.10, printed
canny 94,269 and 74,131 — the replica's sweep values to the digit.**

## 4. What the pair shows — observations, no verdict

### Both views

- **Backdrop** reads lavender-grey, the Ruling 8a word. No numeric measurement is offered
  here: the bands are Task 3 and Task 3 runs only if the pair is accepted.
- **Scale relief is legible as surface**, not as brushwork — individual plates on the flank,
  tail, neck and limbs. That is the field that reached the control as **nothing** at 0.4/0.8
  (`CROP_5_backspines.png` from Task 1 shows the profile's pair catching only the two spine
  silhouettes beside an untouched scale field).
- **The ivory family (D4 horns, D5 crown/cheek spikes, D6 dorsal and tail spines, D7 claws,
  D10 fangs)** all read bone-ivory and are individually separated.

### View 1 (full 17-term string)

- **D8 ember-orange eyes: present, large, with a vertical slit pupil, seated in the brow
  recess.** This is the checkpoint E12 Ruling 2 named and Ruling 10g read as
  passed-as-mechanism on the rejected artifact (153–282 px, one blob). It is substantially
  more legible here. **The verdict remains the Director's**; Ruling 10g's final closure is
  "re-confirm on the accepted pair," which is Task 3.
- **D11 mouth interior reads WINE-RED, not slate** — the same observation the rejected pair
  produced, on a different register and a different control. Two declared elements (D9 tongue,
  D11 interior) share one cavity and the warmer one appears to take it. Recorded as data; the
  cavity is largely the interior geometry `cull_unseen` removes by construction (Ruling 10f).
- **D2 ventral plates** band the throat, chest and belly in bone-tan.

### View 5 (rear stem, 11 terms) — two observations that belong in front of the Director

- **The membranes read closer to BONE-IVORY than to D3's storm-grey.** At 3×
  (`MEMBRANE_view5_3x.png`) the sheet is pale bone with a fine directional fibre texture and a
  faint blue-grey wash near the struts. D3 is the element the backdrop derivation was bound by
  (Ruling 8b: D3 bound every optimum), so where D3 lands matters beyond this view.
- **The hide's green does not cover the same regions it does on view 1.** Haunch, shoulder and
  much of the near hindquarter read pale tan; the green concentrates on the back, tail and one
  foreleg. **This is the defect class E07 established decides acceptance** — a large region of
  the wrong material — and it is the class no 5×5 statistic can see, which is why it is
  reported at full size and at 3× rather than scored.
- **No grafted head anatomy on the hindquarters**, as before — and, as before, that outcome
  does **not** isolate the stem from the occlusion (§ sidecar).

## 5. What this does not settle

- **Whether the register landed.** That is the Director's question and this seat does not
  answer it.
- **Whether a denser control over-constrains.** Not measurable from a clay render; it needed a
  generation, and this is the generation — but reading it requires the eye, not a number
  (Ruling 10d: no structure metric is armed as a gate, and edge-density retention measured
  87.6%/102% on a pair the eye rejected).
- **The bands.** Task 3 runs **only if the pair is accepted** — the suspended Task-5 bands
  died with the rejected pair and re-derive from the fixture against the new one.
  Non-circularity holds.
- **Nothing about whether the route works on a beast.** No twin, no atlas, no projection.

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | The submitted workflow JSONs are on disk with the uploaded cloud names in them, so the saved file *is* the submitted graph; `uploads.json` maps every input; the prompts file records the entry it derived from, the drop map and per-view term counts; the canny override printed as an explicit recorded deviation, never arriving by silence |
| ANDON_AUTHORITY | **3** | The Task-1 anchor **fired** and halted the sweep before a row was written; the frame-agreement gate ran before the controls and before any upload; three guards proven to fire before use, each writing no file on failure; no skip flag anywhere; re-roll bounded at one and unused |
| NAMED_COMPENSATORS | **3** | New files only, all under `E12_repair/` and three new docs; `E12_pair/` never opened for writing; two tools edited additively (the cloud step keeps its LoRA path for subjects that have one); 0 credits, so no spend to compensate |
| DECOMPOSE_BY_SECRETS | **3** | The style register is now subject data expressed mechanically (`lora-w 0.0` → no node) rather than inherited; the prompts file derives from the profile entry by deletion rather than transcription, so a register change cannot desynchronise a stem; the canny pair is per-subject and the profile write stays the advisor's |
| UNCERTAINTY_GATED_HUMANS | **3** | Task 1 halted at the ruling gate rather than spending credits on an unruled threshold, and the question went up split into a derived half and a judgement half with the trade table attached; the negative-prompt tension was surfaced blind, before any measurement, and its resolution was the Director's |
| EXTERNAL_VERIFIER | **2** | The replica was checked against digits the tool it replicates printed in a previous session, and caught a real defect on first use; the no-LoRA claim is corroborated independently by the cloud's own warning disappearing. Marked 2 because the replica is now bit-identical arithmetic to its source and can no longer catch a bug the two share; `skip:` on a second model, per precedent |

---

**Task 2 complete. HALT.** The pair, the sheet, the three crops and this report go to the
**advisor's eye first, then the Director's.** His question is the register: **does it read
ultra-realistic and scary.** Task 3 (re-derive the bands, re-confirm D8) runs **only on
acceptance**.
