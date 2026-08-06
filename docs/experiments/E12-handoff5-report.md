# E12 handoff 5 — the tongue's geometry, the view-5 re-roll, and the head-crop companion

**Executor session, 2026-08-06.** Predictions registered blind in `9fd0fe9`
([E12-handoff5-predictions.md](E12-handoff5-predictions.md)), sha256
`569d2bea7a5730…`, before the first measurement — including the companion's frame
arithmetic, so it could not be tuned afterwards. *(⚠ Advisor annotation, E12 Ruling
12a: `9fd0fe9` was the duplicate dropped in the divergence reconciliation; main
carries the content-identical `f504d6e`. The file's sha256 re-verified against the
tree — the blind anchor holds independent of which commit hash survived.)* This report ranks nothing and attaches no
verdict; the three questions the dispatch pre-stated are the Director's.

**0 credits** (`estimate_credits` before every submission: *"0 credits — no paid API nodes
found in this workflow"*). **Two generations. 1 re-roll spent of view 5's allowance; the
companion's own re-roll UNSPENT; view 1's UNSPENT.** All jobs `succeeded` with zero warnings.

**Look at these before the numbers:** `tongue_check/MOUTH_v1_clay_control_styled_6x.png` ·
`view5_reroll/VIEW5_AB_SHEET.png` + `AB_haunch_3x.png` + `AB_membrane_3x.png` ·
`head_companion/companion_y0.png` + `COMPANION_EYE_4x.png` + `COMPANION_MOUTH_3x.png`.

---

## 0. Environment and one process finding

| leg | result |
|---|---|
| watchdog | **alive**, verified before every local Blender/GPU leg and reported either way — heartbeat ages 0.4–1.1 s, pid 22324, VRAM 2,250–2,278 MiB against the 31,200 ceiling. No `_watchdog_DEAD` |
| frame correspondence | **PASSES** — `dragon_00003_raw.glb` and `prep_uv.glb` have byte-identical raw-import bboxes, matching `head_00003.json`'s `mesh_bbox_blender` exactly. The head box is valid in the route's frame. This was recorded as *owed* in the predictions file before it was run |

**⚠ A concurrent lane is live in this working copy, and it cost a commit.** `git status` was
clean at session start; `docs/advisor-kickoff.md` was modified by another session mid-run and
a `git add -A` swept it into the predictions commit. It was **backed up, split out with
`git reset --soft` + `git restore --staged`, and verified byte-identical to the backup
afterwards** — the other lane's content is intact and unstaged, where it was. Every commit
after that used explicit paths. The dispatch's warning was right and `git add -A` is the
wrong verb in this working copy.

## 1. Predictions scored — 8 held, 5 falsified, 2 partial

*⚠ Advisor annotation, 2026-08-06 (E12 Ruling 12a): the header miscounts its own
table, which reads **7 held / 7 falsified / 1 partial** (held: T1a, T1b, T2a, T3a,
T3e, T3f, T3g; partial: T3c). The table is ground truth; the falsifications being
the content is unchanged.*

| # | prediction | outcome |
|---|---|---|
| **T1a** | no separate tongue SHELL | **held** (low-information, as flagged — it follows from the closed 8-shell census) |
| **T1b** | cavity carries first-hit-reachable interior surface | **held** — 53.12% of cavity-box triangles / 53.32% by area reachable from ≥1 of 98 directions |
| **T1c** | the mouth floor does NOT read as a distinct tongue | **FALSIFIED, decisively** — §2 |
| **T1d** | lands on the middle branch (present but not a tongue form) | **FALSIFIED** — it is the dispatch's FIRST branch, present and visible |
| **T2a** | the pale-tan region moves | **held** |
| **T2b** | D1's miss persists somewhere | **FALSIFIED** — §3 |
| **T2c** | the membranes do NOT resolve to storm-grey | **FALSIFIED** — §3 |
| **T2d** | headline: the two misses do NOT both resolve on a seed change alone | **FALSIFIED** — both resolved. *This is the better outcome for the asset and a full success for the file being wrong* |
| **T3a** | face more defined: ≥2 of separated lids / muzzle scales / nostril structure | **held** — 2 of 3 (muzzle scale plates and nostril structure; no lids) |
| **T3b** | the eye shows separated lids | **FALSIFIED, and it inverts the confound** — §4 |
| **T3c** | D9 does not land as a distinguishable tongue | **PARTIAL** — its **form** lands; its **colour** does not (§4) |
| **T3d** | D11 reads wine-red a third time | **FALSIFIED** — it reads slate, on the tongue (§4) |
| **T3e** | D10 fangs and tooth rows land clearly | **held** |
| **T3f** | the full-figure subject noun does NOT produce a whole-body composition | **held, decisively** — IoU 0.9940, bboxes identical |
| **T3g** | D3 membranes ARE in the companion crop and the term is kept | **held** — verified against the clay render before the stem was written |

## 2. Task 1 — the tongue. **PRESENT, and visible from exterior cameras.**

**The one-line answer the dispatch asks for: `dragon_00003_raw.glb` carries a large tongue
inside the mouth cavity as main-shell geometry, and it is first-hit visible from the route's
own eye-level cameras — including view 0, view 1 and view 2 of the profile-rendered clay.**

**This falsifies an inherited claim.** Gate 0 §6 recorded *"a tongue visible inside on 00001
and 00002"* — saying nothing about 00003, which the Director's "the tongue is missing" and
Ruling 11c both read as *absent*. It is not absent. Gate 0's observation was made on
full-figure renders where the mouth spans ~1.1–1.6% of the frame; at mouth scale the tongue
is unmistakable. *An inherited claim is a hypothesis wearing a fact's clothes*, and this one
took one render to overturn.

Evidence, three instruments (`tools/diagnostics/e12_mouth_geometry.py`, new):

- **Sections.** Mid-sagittal slices at x = −0.060 / −0.035 / −0.012 / +0.012 / +0.040 through
  the cavity box. Near the midline they show a distinct body between the upper-jaw blade and
  the lower jaw. `tongue_check/MOUTH_SECTIONS.png`.
- **Census.** 29,256 triangles have centroids in the cavity box; **15,542 (53.12%), 53.32% by
  area, are reachable** — cast outward from the centroid along 98 Fibonacci-sphere directions
  with `dot(n,d) > 0`, counting a face reachable when the ray escapes. Ruling 10f's method,
  pointed at a region instead of a shell.
- **Renders, which are decisive.** `--clay` crops into the open jaw at yaw −40/−20/0/+20/+40
  (`tongue_check/mouth/`). At yaw 0 and +20 a large, smooth, rounded, tapered body fills the
  mouth between the tooth rows, with a small bump at its tip. It is a tongue.

**And the operative measurement — what the ROUTE sees.** The mouth box projects to
**149 × 134 px at view 0 (1.08% of frame), 222 × 134 at view 1 (1.62%), 165 × 134 at view 2
(1.20%)**. The tongue is a sub-part of that. `MOUTH_v1_clay_control_styled_6x.png` is the
mechanism in one picture: the clay carries the tongue; the control at the ruled 0.05/0.10
carries its **outline** and little else, because the tongue is a large smooth low-contrast
body; and the styled pair painted the whole cavity as one dark wine mass.

**Branch: "present and visible" — D9 stands.** Its landing is judged at the companion's
scale, which §4 reports. **No fixture or profile was edited.**

## 3. Task 2 — the view-5 re-roll. Both named misses resolved.

**Seed 770701**, the deterministic increment (E04's view-7 re-roll precedent). The graph diff
against the seed-770700 submission is **exactly two entries** — `KSampler.seed` and
`SaveImage.filename_prefix` — enumerated in code and printed. Everything else byte-identical,
including the content-hash names of both uploaded inputs. The rejected artifact is preserved
at `view5_reroll/target_5_REJECTED_seed770700.png`.

Against the conditions **pre-registered before the run** (not chosen after):

| | seed 770700 (rejected) | **seed 770701** |
|---|---|---|
| D1 hide on haunch / shoulder / near hindquarter | large pale-tan region | **moss-green scaled hide, individual plates legible** |
| D3 wing membranes | bone-ivory, both wings | **cool storm-grey; struts and wing arms moss-green with ivory claws** |

`AB_haunch_3x.png` and `AB_membrane_3x.png` and `AB_farwing_3x.png` are the evidence at the
zoom the E07 class is judged at. **No statistic is armed** (Ruling 10d).

### One new observation in the re-roll, offered as data

**The far wing's scalloped trailing rim is painted as a small gaping mouth** — white teeth, a
pink-red interior, a tongue-like form — at x 1331–1411, y 426–514.
`AB_wingbodygap_7x.png` at 7×. Measured: **273 px** of the red/pink family (C\* ≥ 12,
h 340–30°) inside a 22,400 px box, **against 0 px in the same box on seed 770700**; median
C\* 17.8, h 26°, L\* 37.4. That hue is **not** D9's wine (h ≈ 345 on the rejected pair) — it
is a new colour on a surface no declared element claims.

**Mechanism, offered as a hypothesis with its evidence, not as a finding:** view 5's stem
**drops the whole mouth family** (D8/D9/D10/D11, per the 9d split), so no prompt term asked
for a mouth. The denser control at 0.05/0.10 draws the membrane rim's serrations, which have
the shape of a tooth row; with `a winged dragon` as the subject noun and denoise 0.92, one
seed of two resolved that serrated edge as a mouth. The other seed, same control and same
stem, painted folded membrane. If that reading is right, it is a **cost of the denser
control**, and it is the first one measured — which is why it is reported here rather than
absorbed.

## 4. Task 3 — the head-crop companion, the resolution rung

### The frame, derived and pre-registered before the render existed

`head_00003.json`'s head box has y and z extents **equal to five decimals (0.1992)**, so the
route's own rule (`turn_render --fit-axis width`: `ortho_scale = max(size.x, size.y) *
margin`, `sensor_fit = HORIZONTAL`) yields **aspect exactly 1.000** — a square frame falls
out rather than being chosen. Padded 1.12 (Gate 0's own head-crop padding) →
**ortho_scale 0.223104**. Scale fixed by matching the route's standing pixel budget
(1792 × 1024 = 1,835,008) so the generator stays in the regime the arc has run in:
√1,835,008 = 1354.6 → **1360 × 1360**, both axes ÷16, neither the standing 1024.

That number differs from `e12_head_render.py`'s yaw-invariant span (0.305005). Rather than
solve for a `--pad` of 0.82 — which would print as under-padding and read as a retune — an
explicit `--ortho-scale` override was added, and **both values are printed at the site**.

**Resolution gained:** the mouth box goes from 222 × 134 px at view 1 to **608 × 549 px** in
the companion frame — **11.2× the pixel area**. The head box goes from ~1.6% of the pair's
frame to filling this one.

### Inputs, and the mask check

Clay at that frame via `e12_head_render` (`--ortho-scale 0.223104 --res 1360 --clay`).
The figure mask is a **direct raycast at the crop camera** (`e12_crop_silhouette.py`, new) —
*not* an upscaled crop of the full-frame silhouette, which would have handed a 4.1× blocky
staircase to the contour term. The camera is `e12_head_render`'s, reproduced line for line,
and it was **checked rather than asserted**: geometry mask 1,137,368 px (61.493%) against the
render's keyed figure 1,094,245 px (59.161%), **bboxes identical at (0, 115, 1359, 1359)**,
IoU 0.9575 — the 2.6% difference is the known grey-on-grey keying loss, not misregistration.
Control at the ruled 0.05/0.10: **108,994 px** (canny 98,546 + contour 17,861).

### The stem

Built by the same committed builder from the same profile entry by the same deletion
construction, and added to `E12-twin-prompts.json` as `headclay_0` (v4) so the cloud guard's
provenance check holds **without a skip flag**. The eight `dragonclay` stems were verified
**byte-identical v3 → v4**, and still byte-equal to what was actually submitted for views 1
and 5. **15 of 17 terms.** Verified against the companion's own clay render before writing:
**D3 KEPT — both wings enter the crop at the left and right edges**, exactly the case Gate 0
flagged (membrane passing behind the skull). **Dropped: D6** (dorsal *and tail* spines — the
tail is far out of frame, and the ivory family is redundantly declared by D4/D5/D10, so the
shoulder-end spines keep their colour by family) and **D7** (feet out of frame; no wing-claw
spur legible at the edges). The subject noun stays.

### The registration diagnostic (halt suspended at 0.0, as everywhere on this subject)

| | |
|---|---|
| geometry silhouette | 1,137,368 px, 61.493% of frame, bbox (0, 115, 1359, 1359) |
| styled figure, keyed | 1,143,004 px, 61.797% of frame, bbox **(0, 115, 1359, 1359)** |
| **IoU styled vs geometry** | **0.993953** |

**T3f held decisively**: a full-figure subject noun in a bust frame produced no whole-body
composition. The control holds composition — the measured architecture, confirmed.

### What the companion shows — landings at scale, no verdicts

- **D4 horns, D10 fangs and tooth rows, D2 throat bands** — land clearly.
- **D1 hide** — lands; muzzle and cheek scale plates individually legible; nostril structure
  distinct. **T3a's two of three.**
- **D5 crown and cheek spikes** — **split**: the crown spikes read bone-ivory, the cheek and
  jaw spikes read the hide's green.
- **D3 membranes** — **land ORANGE/RUST, not storm-grey.** 64,602 px, **5.68% of the figure**,
  median C\* 35.8, h 50°, L\* 34.1, spanning the full frame width. A large region of an
  undeclared colour, on the element the backdrop derivation was bound by (Ruling 8b). *The
  same element resolved correctly on view 5's re-roll in the same session, at a different
  frame and scale.*
- **D8 ember-orange eyes** — **did NOT land as an eye.** In the socket region there is a
  **crimson/magenta teardrop with a small orange bead at its top**: 2,185 px, bbox
  (913, 604, 958, 694). `COMPANION_EYE_4x.png` is the clay | control | styled triptych there:
  the **clay shows overlapping brow plates and no lens recess in this crop**, the control is a
  thicket of plate edges, and the model painted plates and a bead.
  *(The ember-orange-family mass of 48,897 px measured inside the figure is the wing
  membranes, not the eye — stated because a colour-family count alone would have read as a
  D8 landing, and it is not one.)*
- **D9 tongue and D11 mouth interior** — **the tongue's FORM lands and its COLOUR does not.**
  `COMPANION_MOUTH_3x.png`: the clay carries the tongue, the control carries its outline (the
  interior is smooth and empty), and the styled output paints that exact shape in **slate
  blue-grey** — D11's declared colour, on D9's declared surface.

### The finding that belongs in front of the advisor's fixture question (Ruling 11c)

**The two cavity elements swap surfaces with scale.** At pair scale, D9's wine took the whole
cavity and D11 did not appear as slate. At bust scale, D11's slate took the tongue and D9's
wine did not appear. Two declared elements share one cavity and **neither reliably owns its
surface** — the Amendment 15 occupancy question, measured on two frames of the same subject
in one session. The fixture consequence is the advisor's to draft and the Director's to rule;
**no fixture or profile was edited here.**

### The allocation ladder's rung, reported as the dispatch pre-registered it

The pre-registered readings were *face reads defined at bust resolution → resolution-starved*
versus *face still soft → the mesh's own head is the limit*. What was measured:

- Definition **did** increase where the geometry carries structure — muzzle scale plates,
  nostrils, horn surface, tooth rows, all newly legible.
- The **eye did not appear at 11.2× the mouth's pixel area and ~33× the face's**, and the clay
  at that location shows overlapping brow plates rather than a lens recess.

**My pre-registered confound did not fire, and it inverted.** I predicted a convincing eye
might be painted onto a recess that has none, and warned that would prove nothing. The
opposite happened: *more* resolution and a *denser* control produced *less* eye than the pair
did — consistent with the control constraining the model to the actual geometry where the
pair's sparse control left it free to invent one. **That is a mechanism hypothesis with its
evidence, not a ruling**, and the branch it points to is the Director's to take.

## 5. What this session does not settle

- **Whether any of it is good.** The register, the re-roll and the companion all go to the
  Director; his three questions were pre-stated by the dispatch and are unanswered here.
- **Whether the wing-rim mouth artifact recurs.** One observation on one seed; no third roll
  exists and none was run.
- **Whether D3's orange is a frame effect or a register effect.** The same element landed
  storm-grey on view 5's re-roll and orange on the companion, in the same session — that is
  the evidence, and isolating it needs an arm this dispatch does not have.
- **Bands and the D8 closure** (handoff 4's Task 3) stay acceptance-gated.

## 6. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions hashed and committed before the first measurement, including the companion's frame arithmetic; saved workflow JSONs carry the uploaded cloud names, so each saved file IS its submitted graph; both seeds recorded and the re-roll's two-field diff enumerated in code; the frame derivation printed beside both the used and the replaced ortho_scale |
| ANDON_AUTHORITY | **3** | Watchdog before every local leg; the mask's registration checked against the render rather than assumed; four guards proven to fire before use (the prompts builder's three defect classes, its new `--extra` term check, the no-LoRA scan, the crop-silhouette bound); re-roll bounded at one and the companion's left unspent; no skip flag anywhere |
| NAMED_COMPENSATORS | **3** | New subdirectories only (`tongue_check/`, `view5_reroll/`, `head_companion/`); the rejected view-5 artifact copied, never moved, so the handoff-4 sidecar's provenance stays valid; the concurrent lane's file backed up before being split out and verified identical after; 0 credits |
| DECOMPOSE_BY_SECRETS | **3** | The tongue answer comes from the mesh, not from a styled artifact; the companion derives every value from recorded artifacts (head box, ruled canny, protective entry) and re-derives nothing; the companion stem lives in the same versioned prompts file so provenance holds without a bypass; fixture consequences routed to the seats that own them and nothing edited here |
| UNCERTAINTY_GATED_HUMANS | **3** | All three outcomes halt to eyes; the D9/D11 swap and the wing-rim artifact go up as measurements plus a labelled hypothesis rather than as conclusions; the allocation branch is named and left to the Director |
| EXTERNAL_VERIFIER | **2** | The tongue answer checks a styled claim against geometry from three independent instruments; the re-roll puts two generations against one pre-registered spec condition; the companion's mask is checked against a render made by a different code path. Marked 2 because the eye-region reading rests on one generation, and `skip:` on a second model per the arc's precedent |

---

**All three tasks complete. HALT.** Everything staged goes to the **advisor's eye first, then
the Director's**. His pre-stated questions: **does view 5 now wear its declared materials · does
the face define at resolution · what may the mouth hold.** Handoff 4's Task 3 (bands
re-derivation + D8 closure) remains acceptance-gated behind that look; nothing past the halt
was run.
