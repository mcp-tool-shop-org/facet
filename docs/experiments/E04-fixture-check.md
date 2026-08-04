# E04 — checking stressor S1 before the dispatch spends generation on it

**Executor session, 2026-08-04.** Local, no GPU, no generation, nothing written outside this
file. Run *before* the next dispatch exists, because
[`canon/GALLEON-IDENTITY.md`](../../canon/GALLEON-IDENTITY.md) states a mechanism that the
dispatch would inherit, and this repo's first rule is that an inherited claim is a hypothesis
wearing a fact's clothes — *including numbers written by the advisor.*

**This does not touch the canon.** G4's colour is an authoring choice and the Director's.
What is measured here is the *stated reason* for it.

---

## The claim

> **S1 — canvas is the blade problem at sail scale.** W3's steel keyed out against the grey
> studio backdrop at C\* 1.6–2.8 (§9a); **pale canvas is the same physics across a vastly
> larger area.** G4 is authored *warm tan* partly for this reason.

## The mechanism, reproduced first

`project_twins.figure_mask` keys the twin's trust mask as
`max_channel |pixel − backdrop| > 0.06`, where the backdrop is the 8×8 corner median of the
twin itself. Measured on the shipped ARMB twins, inside the exact mesh silhouette:

| | twin_2 | twin_6 |
|---|---|---|
| backdrop (corner median) | rgb(114,114,115) | rgb(117,117,118) |
| residual inside the figure, median | 0.3569 | 0.3549 |
| **px at or under the 0.06 cut** | **1,602 (1.77%)** | **2,221 (2.45%)** |
| **their median colour** | **rgb(111,113,115)** | **rgb(119,116,113)** |

**The pixels that key out are mid-grey pixels sitting within ~3/255 of a mid-grey backdrop.**
That is the blade, and it reproduces the documented mechanism.

## S1's physics is inverted

The backdrop is **mid** grey — rgb(106,106,107) as the median over all eight twins, i.e.
0.415. Distance from it is what the key measures, so a *pale* material is the **safest**
possible value, not the most dangerous:

| candidate material | residual vs backdrop | 0.06 cut |
|---|---|---|
| **white canvas** rgb(242,240,235) | **0.5343** | passes by **8.9×** |
| off-white canvas rgb(232,228,216) | 0.4951 | passes |
| pale deck planking rgb(214,196,166) | 0.4245 | passes |
| **weathered tan canvas** rgb(206,180,140) | **0.3931** | passes |
| warm tan canvas rgb(190,163,122) | 0.3304 | passes |
| *W3 steel, as measured* | *≈0.065* | *straddles it* |

**White canvas is the furthest of every candidate from the backdrop, and tan is closer to
the danger than white is.** Both clear the cut by an enormous margin, so **the sail colour is
not a keying risk in either direction** — the choice between them cannot be justified or
attacked on this mechanism. The blade did not fail because it was pale. It failed because
steel renders at *the backdrop's own value*.

**What this does and does not overturn.** It overturns the sentence *"pale canvas is the same
physics"* and the clause *"partly for this reason."* It does **not** overturn G4 — warm tan
may be right for canon, for the style, or for looking like weathered sailcloth, and none of
those need this argument. A choice with one wrong reason and three good ones is still the
choice; it just should not carry the wrong reason into a spec that later gets read as
measured.

## The real S1-class risk on this subject, measured

If mid-grey is the failure value, the danger is anything that *renders* mid-grey — and a thin
structure does that regardless of what colour it is named, because it antialiases toward the
backdrop. Keying failure by local half-width (distance transform inside the silhouette):

| local half-width | px | twin_2 keyed out | twin_6 keyed out |
|---|---|---|---|
| **≤ 2 px (thin)** | 6,284 | **5.68%** | **10.77%** |
| 2–5 px | 9,755 | 2.42% | 3.79% |
| > 5 px (bulk) | 74,514 | 1.35% | 1.58% |

**Keying failure is 4.2–6.8× enriched in thin structure.** So on the galleon the S1-class risk
is not the sails at all — it is **G9, the tarred rigging and ratlines**, which are thinner
than the blade that already failed, and which the concept shows as single-pixel filaments.

**S1 and S2 are the same failure on this subject.** The fixture lists them as two stressors;
measured, thin structure is *both* the thin-policy problem and the keying problem, and the
merged risk is larger than either alone. That is a strengthening of the fixture, not a
weakening — it just points at a different element.

## The lever is the backdrop, and it is one word

The backdrop is **prompted**, not rendered — W3's twin prompt ends *"plain grey background"*
and the diffusion paints it. So it is fixture data, changeable in a word, and it is the only
operand in `|pixel − backdrop|` that is free. A backdrop chosen *away* from the ship's
materials — rather than a mid grey sitting in the middle of everything — moves every material
off the cut at once, including the rigging.

The fixture already says *"the backdrop question stays open in the E04 spec."* This measurement
says it is not a side question: **it is the main lever, and material colour is the weak one.**

## One observation on G11, offered with numbers, not as an objection

Admitting blue as a declared material is exactly the palette-as-subject-data point and it is
well made. Its cost is quantifiable, and the bands are not declared yet (S3 defers them), so
this is input to that derivation rather than a criticism of it:

| | allowed hue | **forbidden** |
|---|---|---|
| W3 | warm 0–105, green 125–210 | 105–125 + 210–360 = **170° (47.2%)** |
| galleon, if blue ≈ 210–260 is admitted | warm, green, blue | 105–125 + 260–360 = **120° (33.3%)** |

The gate keeps most of its reach but loses about a third of it, on the one subject where S3
says it carries the judgment no eye can. Worth deriving the blue band tightly rather than
broadly, and worth noting that G6 verdigris and G11 sea-blue are adjacent in hue — if their
bands merge, the forbidden set shrinks further than the table shows.

## What I did not do

Nothing from the dispatch: no ship-profile value measured from the designated mesh, no twins,
no palette bands, no spec. The dispatch is the advisor's to write and it is not written. This
file is one pre-registered claim checked against the artifacts that already exist, because it
was cheaper to check than to inherit.
