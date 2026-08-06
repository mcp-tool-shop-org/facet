# FACET LOGO — identity specification (brand fixture)

**Status:** authored by the advisor, 2026-08-05, on the Director's instruction. **A brand
asset, not a route subject** — but it borrows the subject fixtures' grammar because the
logo enacts the route's own thesis: **form first (a clay), style second (a canon-bound
bake)**. The logo generated today is the *clay stage* — five sculpted letters in
monochrome — and this file fixes what each letter's material IS, so the textured version
is baked later against canon rather than improvised. Any line here is the Director's to
overrule in a sentence.

Instruction trail, recorded: three textures → corrected to **five** → corrected again to
span **subject classes beyond the current profile list, including profiles we will
build**. Read as one distinct texture per letter, the set covering the route's past and
future subjects; flagged for a one-sentence correction if misread.

---

## The scheme — five letters, five subject classes

Each letter carries the signature texture of one class the route textures. Three point
at live profiles; two are **pre-registered future classes** whose profiles do not exist
yet — labeled as such, per the house evidence-status discipline.

| letter | class | texture element (noun phrase) | relief signature (the clay stage) | bake identity (the later texture pass) | profile status |
|---|---|---|---|---|---|
| **F** | **Figure** — characters | embossed scrollwork armour | baroque scroll filigree on a hammered field | warm burnished gold | LIVE — `character.json`; the gold family is the studio's proven binding material (W3's armour; the galleon's G1/G5/G6/G12/G13) |
| **A** | **Architecture** — buildings, ruins | dressed stone masonry | cut ashlar blocks, mortar joints, chisel marks | pale warm limestone, matte | **FUTURE profile, pre-registered** — the class E10's law already names ("moss on ruins") |
| **C** | **Creature** — beasts, monsters | overlapping scale plates | imbricated scallop relief | deep moss-green | LIVE — `beast.json`; inherits D1 verbatim |
| **E** | **Environment** — terrain, flora, minerals | a faceted crystal | sharp angular planes, geometric cut faces | cool ice-blue crystal, glassy sheen | **FUTURE profile, pre-registered.** ⚠ *Corrected 2026-08-06 on the Director's eye at the v1 artifact: was "furrowed tree bark" — wood-family, adjacent to T's wood, and the two mushed. The crystal is the one relief family nothing else in the set occupies, it is genre-native (the JRPG tradition runs on crystals), and the logo of facet now contains a faceted letter* |
| **T** | **Transport** — ships, vehicles | oak hull planking | plank courses, caulked seams, treenail pegs | warm oak-brown with black tarred seams | LIVE — `ship.json`; inherits G2/G3 verbatim |

**Distinctness is a property of the MATERIAL FAMILY, not the relief pattern** —
⚠ *learned at the v1 artifact, 2026-08-06.* The v1 set checked pairwise distinct in
words (bark fissures vs plank courses) and failed in clay, because bark and planks are
both **wood** and read as one family the moment they stand together; adjacency doubles
the requirement. The ruled set — ornamental metalwork / cut stone / organic scale /
geometric mineral / carpentered wood — carries five families, no two alike, no
neighbours related. Materials whose clay signature is weak (smooth steel, fine canvas
weave) remain excluded.

**And the form stage carries no colour words.** ⚠ *Also learned at v1:* the prompt said
"gold-scroll relief" and the model painted F gold while four letters stayed clay — a
colour word in the clay stage is an instruction, and it was obeyed. Form first means
the clay prompt names RELIEF ONLY; every colour lives in the bake column and arrives at
the bake. This is the route's own discipline applied to its own logo, violated once by
its own author, corrected here.

## Grammar rules, inherited from the subject fixtures

- **One letter, one material, occupancy-complete.** No letter carries two textures, and
  any future edit that *decorates* a letter (gold banding on the bark, moss on the
  masonry) is predicted to drop — to change a letter, **replace its material** on the
  whole letterform (E08 Amendment 15, measured twice).
- **Every element is its own noun phrase** — head noun + minimal modifier (Amendment 13).
- The three LIVE identities inherit their colour registers from their subject canons and
  must track them: if `DRAGON-IDENTITY.md` D1 ever changes, the C letter changes with it.

## The clay-stage prompt — v2, versioned here so the recipe travels with the identity

```
a sculpted clay logo maquette of the word "FACET", five massive dimensional capital
letters standing in a row on a studio floor, form-exaggerated sculpt-like clay, matte
warm-grey monochrome throughout, every letter the same grey clay, each letter carved
with a different surface relief: the letter F embossed with baroque scrollwork filigree,
the letter A built from dressed stone masonry blocks with mortar joints, the letter C
covered in overlapping dragon scale plates, the letter E cut as a faceted crystal with
sharp angular planes, the letter T built from ship hull planking with caulked seams and
treenail pegs, bold exaggerated planes, soft studio grey backdrop with a gentle
gradient, soft ground shadow
```

*v1 (superseded 2026-08-06, kept because rejected artifacts stay in the record): as
above but with "armoured in embossed gold-scroll relief" for F and "carved as deeply
furrowed tree bark" for E, and without "monochrome throughout, every letter the same
grey clay." Rolled once; the Director's eye rejected the texture combination — the two
wood textures adjacent read as one family, and the colour word painted F gold in an
otherwise-clay set. Both corrections are in the table above.*

**Generation notes:**

- **Generator:** the studio's Qwen-Image stack (cloud or local per standing policy) —
  chosen deliberately: legible letterforms are its measured strength, and the staging
  aesthetic matches the subject clays (`dragon_clay_p1_*`: warm-grey studio backdrop,
  gradient, soft ground shadow).
- **Frame:** landscape, ÷16-legal — 1792×1024 matches the staging convention.
- **Negative:** `watermark, blurry, photo, deformed` — the standing negative **minus**
  `text, logo`, which would fight the goal of this specific asset. Recorded so the
  omission is a decision, not a drift.
- **Pre-registered stressor — five-way binding drift.** Assigning five attributes to
  five objects in one prompt is a known diffusion weakness: expect some rolls to swap or
  blend letter↔texture assignments. Judge at full size, roll freely (a brand asset, not
  an experiment — no bounded re-roll here), and pick by eye. **The assignment is
  enforced at the bake, not the clay**: the textured pass masks per letter and applies
  this table's identities, exactly as the route's brush masks per stroke — so a clay
  pick with one soft assignment is usable if its forms are good.

## The bake contract (later)

The textured logo is produced FROM the chosen clay: canny-locked on the clay's own
contours, masked per letter, each letter taking its bake identity from the table above —
the same mechanism the route uses on subjects (control from geometry, identity from the
named element, style from the LoRA register: `visible brushstrokes, painterly worked
surface`). If a palette check is ever wanted on the result, its bands derive from this
table's five identities, cross-checked against the chosen artifact — never invented.

## What this fixture is for

1. The logo IS the pipeline's story: five subject classes, form first, canon-bound style
   second. The two future-class letters are a pre-registration the studio grows into.
2. When the textured bake happens — next week or next year — the materials are already
   decided, cited, and tracking their source canons. Nothing about the logo's look will
   depend on who is prompting that day.
