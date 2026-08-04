# E08 step 1 — the canon specification, PROPOSED for ratification

**Amendment 11:** [E08-ruling-gate0.md](E08-ruling-gate0.md) ·
**Armour test:** [E08-armour-test.md](E08-armour-test.md)
**Status:** PROPOSAL. Canon is the Director's; nothing here is adopted until he rules.

**Twins belong to a mesh. Identity belongs to the prompt.** This is the attempt to write the
identity down — the delta between what `restylize_views.py`'s prompt already names and what the
canon twin actually shows.

---

## Evidence so far: two one-term tests, and they do not agree

| element | named? | result |
|---|---|---|
| **gold knee plates** | added | **landed fully** — faceted gold plate, correctly placed on the knee, fur reduced to a trim beneath |
| **gold-trimmed brown leather bracers** | added | **SPLIT** — "brown leather" landed (fur cuff → smooth segmented leather); **"gold-trimmed" did not** — the canon bracer carries a distinct gold plate on the outer forearm and the new one carries none |

Both runs used a byte-matched control (20,973 px, canny 15,325 + contour 9,958), so the prompt
term was the only variable in each.

**This matters for the gate at step 2.** One of two named elements reproduced completely. A
compound term — *material* plus *trim* — delivered its head noun and dropped its modifier.
Per Amendment 11, that is reported and **not tuned**: adding "gold bracer plate" until it
appears would be fitting the spec to the outcome, and a spec tuned until it works is not a spec.

---

## Proposed specification

### A. Already named, and landing

bald · long red beard · dark green knitted sleeveless tunic · polished gold pauldrons ·
dark red layered cloth skirt · leather belt · heavy dark boots · massive greatsword ·
painterly visible brushstrokes, worked matte surface

### B. Named, proven to need naming

- **gold knee plates** — proven, landed

### C. Named, landing only in part — flagged, not tuned

- **gold-trimmed brown leather bracers** — material lands, gold trim does not

### D. Visible in the canon twin, NOT in any prompt — proposed additions

Read off `canon/twin_front.png` at full resolution. Confidence is mine; the ratification is not.

| # | element | confidence | note |
|---|---|---|---|
| D1 | **small round gold medallion at the front of the belt** | high | present in canon and in both new twins; the current prompt says *"gold necklace"* instead, and there is **no necklace at the throat** in canon — the prompt appears to misname this element |
| D2 | **ornate gold crossguard and pommel on the greatsword** | high | canon shows a worked gold crossguard with scrollwork and a gold pommel cap; the prompt says only *"massive greatsword"* |
| D3 | **fur trim edging the knee plates** | medium | canon shows fur at the plate edges; the new twins produce it too, so it may not need naming |
| D4 | **green skirt layer beneath the wine-red panel** | medium | canon layers green under red; *"layered"* is in the prompt but the second colour is not |
| D5 | **gold scrollwork on the pauldrons** | medium | canon's pauldrons carry a raised spiral motif; *"polished gold pauldrons"* does not name it |

### E. Explicitly NOT canon — the artifact the Director ruled on

- **the canon twin's proportions** — taller, narrower, longer-limbed, small head against the
  body, filling 17.38% of frame against a 19.01% mesh silhouette. Ruled an artifact of a
  control missing a quarter of the figure. **The mesh's proportions are correct; do not
  reproduce the twin's.**
- **the "gold necklace" term** — proposed for removal or correction to D1, since no necklace is
  visible in canon and the term may be what produced the belt medallion by accident.

---

## What ratification would settle

1. **D1–D5**: which are canon, which are incidental, which are wrong.
2. **The necklace**: remove, or keep alongside the medallion.
3. **C**: whether a bracer without gold trim is acceptable canon, or whether the split result
   means the specification premise needs re-testing before Arm B.

Step 2 — generating from the full ratified spec and checking every named element lands — is the
gate and has not been run. On present evidence it would report **one full, one split**.
