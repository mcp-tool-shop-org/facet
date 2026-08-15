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
