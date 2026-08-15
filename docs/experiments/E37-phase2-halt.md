# E37 Phase 2 — HALT before spend: the repair regions cannot be located by measurement, and my eyeballed rects failed their own walk

**Seat:** executor · **Written:** 2026-08-15 · **Spend: 51 of 80 — UNMOVED. No job fired.**

Phase 2 stops before the first masked repaint. Two things are established and one is not: the
mechanics are verified, the fleck census is measured and it changes item 2 — and **the repair
regions themselves are not yet locatable to mask precision.**

---

## 1. Mechanics — the ritual and the two nodes

E15 ritual **PASS**, all four legs, exit 0. Manifest gates **HELD** — E33 116/116 · E34 84/84
· E35 335/335 · C 7,312 files delta +0/+0. Watchdog read at open. Receipts in
`facet_E37\phase2\`, outside every protected tree.

**Amendment 3's two nodes are verified live, not inherited:**

| node | pack | contract |
|---|---|---|
| `SetLatentNoiseMask` | **core**, `model/latent` | `samples` LATENT + `mask` MASK → LATENT |
| `ColorMatchV2` | ComfyUI-KJNodes, `KJNodes/image` | `image_target`, `image_ref`, `method`, `strength` (0–10), `multithread` → IMAGE |

`ColorMatchV2`'s methods are `mkl` (default) · `hm` · `reinhard` · `mvgd` · `hm-mvgd-hm` ·
`hm-mkl-hm` · `reinhard_lab_gpu`. The deprecated original is absent from the catalog, as
Amendment 3 said. **The masked-repaint path exists and its schema is what the amendment
claims.**

---

## 2. ⚑ The fleck census: its largest components are the man's face

Dispatch item 2 asks the 162 fleck sites to ride the repair pass *"where components are big
enough to matter."* Measured, the components big enough to matter are largely **not flecks**.

Of the **15 components ≥ 15 px²**:

| what | count | where |
|---|---|---|
| **drawn face features** | **4** | v6 brow **32 px²** (206.8, 134.4) · v6 eye/brow **27** (213.1, 120.8) · v7 brow **21** (225.2, 125.0) · v6 mouth/chin **19** (213.4, 183.1) |
| **the ear knob** | 2 | v4 **18** (248.9, 171.6) · v1 **16** (238.1, 171.1) — already repair 1c |
| body strays | 9 | rows 486–909 — limbs, ankles, feet |

Across all 162 sites: **68 (42.0%) and 334 px² (41.3%) sit inside the measured head band**
(rows 80–232).

**Two consequences, neither of them mine to rule:**

1. **[Ruling 19](E37-ruling.md) item 5 holds v6's brows as identity-adjacent. The census says
   they are also the two largest components in the whole set** — so a fleck pass that took the
   biggest components first would erase them. The same reasoning extends to **v7's brow
   (21 px², the third-largest head-band component)**, which no ruling has held yet.
2. The **9 body components** at rows 486–909 are genuine strays, and most sit on views with no
   named repair — so "rides the same pass" reaches fewer of them than the phrase implies.

This is reported, not acted on. The instrument is a **dark-speck** census and the drawn face
is dark paint on pale wood; the two are the same colour class by construction.

---

## 3. ⛔ The halt: the repair regions are not locatable to mask precision

### 3a. Measured derivation FAILED

Two derivations were tried, on the reasoning that a paint artifact sitting where the clay is
flat should separate:

**Paint outside the geometry silhouette, band-limited to the head rows.** Returns 266–602 px
per view, largest component 60–123 px, bboxes clustering at **x 126–156, y 173–212** — the
**jaw/neck rim**, on every view including ones with no ear defect. Unbanded it returns the
**ground shadow** (v6: largest component 17,761 px at rows 942–1023). It does not find the ear:
the mesh carries ear geometry, so the knob is *inside* the silhouette.

**Dark paint inside the head band.** Returns 283–3,786 px per view, but it **conflates the
drawn face with the ear** — exactly the class §2 just measured. v5 (a pale ear, no drawn face
at that yaw) returns a 2,823 px largest component; v6 returns 3,439. The two objects are not
separated by this predicate.

### 3b. And my eyeballed rects failed their own walk

Rects were proposed from the full-size crops and overlaid for the walk that
[Ruling 18](E37-ruling.md) made standing practice — **at this seat, before anything moved.**
They are wrong:

| view | proposed | what the walk shows |
|---|---|---|
| v3 | two ear rects | **both sit on empty background**; the ear disc is inboard of them |
| v5 | ear rect | **sits on background** right of the skull; the pale disc is inside the outline |
| v6 | nose wedge | sits over the **cheek and mouth**, not the nose |
| v7 | face band | covers most of the skull — too coarse to be a repair mask |
| v4 | two ear rects | roughly on the ears, loose |
| v1 | chest patch | plausible; clips the arms at both edges |

Receipt: `phase2/proposed_repair_rects.png` + `.json`, status **CANDIDATE — not ratified, no
job fired**.

**So the halt.** A masked repaint against those rects would repaint background where the ear
is and cheek where the nose is, at the same seed and conditioning, and the composite would
bake it in. The defect would not be that the repair failed — it would be that the repair
landed somewhere else, on a set that currently passes both eyes.

**What this is not:** it is not a claim the regions are invisible. They are plainly visible at
full size — the Director named them, the advisor's walk named one, this seat named two. What
failed is **turning a named region into a pixel rect at mask precision**, and reading
coordinates off a downscaled sheet is how the wrong rect got proposed.

### 3c. What would close it, priced

Each region located at **1:1 or better on a tight crop**, one region at a time, the rect read
against a grid at that scale and re-overlaid before use — six regions, local and free, no
cloud job. That is the missing step between "the Director named it" and "a mask exists."

---

## 4. Item 1a is also blocked, and for the same reason

The v0 face tone lift is deterministic and local — no cloud job, magnitude to his eye, exactly
as Ruling 19 specifies. But **"the face" is still a region**, and a lift applied to the whole
head band raises the skull and the ear with it. It needs the same 1:1 localisation as the rest,
so it is held with them rather than shipped on a looser rect than the ruling intends.

---

## 5. State

- **Spend 51 of 80, unmoved. No cloud job fired this phase.**
- Set A is untouched; nothing was masked, composited or written over.
- No protected tree was written to. Manifest gates HELD at open.
- Phase 2's mechanics are verified and its inventory is measured; only the geometry of the
  masks is missing.

---

## 6. Region protocol executed — rects re-derived at 1:1 ([Ruling 20](E37-ruling.md))

Seven regions, one local 1:1 crop each at 8× (v1 at 7×, 5× on the overlay), rect read against
a source-pixel grid, re-overlaid, walked at this seat. **Zero cloud. Spend 51 of 80.**

| region | view | rect (twin px) |
|---|---|---|
| v0 lift — features + cheeks, **excluding skull and ear** | 0 | 133, 122, 234, 192 |
| v1 chest patch | 1 | 137, 246, 207, 420 |
| v3 ear knob | 3 | 135, 141, 161, 174 |
| v4 ear L / ear R | 4 | 110, 143, 133, 179 / 235, 143, 258, 179 |
| v5 ear knob | 5 | 205, 141, 230, 181 |
| v6 nose wedge | 6 | 225, 146, 250, 178 |
| v7 face band | 7 | 165, 120, 235, 190 |
| **HELD** v6 brows / v7 brow | 6 / 7 | 196, 112, 224, 142 / 214, 116, 236, 134 |

Receipt: `phase2/repair_rects_v2.{png,json}`, status **proposed — awaiting the advisor's walk**.

### 6a. ⚠ A correction to §3b, owed and made

**My v6 rect was not wrong.** §3b reported it as sitting "over the cheek and mouth"; re-read at
1:1 the nose wedge is **x 225–250, y 146–178**, and the original proposal (222, 138, 252, 178)
frames it. That call was made off a **3.16× downscaled overlay** — the same unreliable read the
halt was written against, committed in the act of reporting it. The genuine failures stand and
are larger than stated: **v3's ear is at x 135–161 against a proposed 93–132** (no overlap at
all), and **v5's at x 205–230 against a proposed 233–276** (no overlap). v4's were loose, v7's
coarse, v1's plausible.

### 6b. Two conflicts this seat will not resolve

1. **The v7 face-band repair rect CONTAINS the v7 brow that Ruling 20 just HELD**
   (165,120,235,190 ⊃ 214,116,236,134 in x; the brow's top edge sits 4 px above the band).
   Repainting the band repaints the held feature. Either the band is cut to exclude the brow,
   or the hold yields on that view — a ruling, not an executor's call.
2. **v1's chest rect clips the left arm** at its top-left corner. Tightening it loses upper
   chest, which is where the dark tone is strongest.

---

## 7. The masks are built; the v1 cut is NOT delivered; several clip their target

Feather **R = 5 px**, stated once and used everywhere. Eight masks written to
`phase2/masks/` with `masks.json`.

**Ruling 21 clause 1 is DONE and measured.** v7's band = band − dilate(held brow, R), and the
guarantee is asserted rather than reasoned: **the mask value on every held pixel measures
exactly 0.0000**, on v7 (479 px removed) and on v6. The check `raise`s; it is not an `assert`.

**Ruling 21 clause 2 is NOT done.** The measured cut I built — rect ∩ figure, largest
connected component — removed **1,313 px of background** (the rect's left edge sits off the
figure at rows ~250 and ~400, where there is a background gap between arm and torso). It did
**not** remove the arm, because the arm is *connected to the torso* inside the rect, so a
largest-component rule keeps it. The overlay shows green over the shoulder and down the arm's
inner edge. **The corner cut the ruling asked for is still owed, and it has to be a polygon,
not a connectivity rule.**

**And five masks clip their own target**, read at 8× on the overlay:

| mask | what the walk shows |
|---|---|
| v4 earL / earR | tight — each ear's outboard wedge tip falls outside the mask |
| v3 ear | slightly tight at the disc's right edge |
| v6 nose | the wedge's lower-left hard edge runs outside the mask |
| v7 band | the right edge cuts through the nose |
| v0 lift | boundary runs **through** the brows at the top and the mouth at the bottom — a tone lift with a boundary mid-feature steps across a drawn line |

**So no job fires.** Repainting v1 as masked would repaint the arm; the five tight masks would
leave a repaired region with its original defect still protruding past the seam. Both are
cheaper to fix now than after seven jobs and a composite.

**Priced:** the rects grow by the measured overshoot per region and v1 gains its polygon — one
more local pass, zero cloud, one re-walk. Spend stays **51 of 80**.
