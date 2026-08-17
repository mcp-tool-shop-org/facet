# Grok build #15 — are the flats in the twins, or did we make them?

**2026-08-17, facet advisor seat. BUILD round.** Fourteen briefs, fourteen chips held.
Brief 14's chip corrected my framing and two citations in the law book.

*Everything below the line is the paste block.*

---

# Fourteen for fourteen. You were right that the magenta is the louder paint and not the class he named. So go after the class he named — and answer the one question that decides whether the money gets spent.

## Where your last round left it

The magenta is settled and it is **cosmetic**: 304 exact-magenta pixels on view 0, **0.22%
of the figure**; unmapped total **0.79%**. Confirmed the mechanism (fills operate on valid
texels, unmapped texels are not valid, so no fill could ever reach it), confirmed the 46x
atlas-sentinel cut moved the on-screen count by six pixels, and ranked an atlas-side stamp
of ~374 unique texels as the repair that needs no re-bake. **Repairing it would not change
how the asset looks**, and that is worth having established before anyone spent a re-bake
on it.

That leaves the class the Director actually named: **the flat olive / gold / green angular
patches on the tunic, collar and skirt.** E50 measured them at **90–99% `written`** — the
ordinary directly-painted class — and found the identical defect in a render built from an
atlas that predates every repair this session shipped.

`written` means the per-texel scatter wrote it from a twin. **Nobody has asked whether the
twin was wrong.**

## The question, and why it is the expensive one

The remaining plan is: complete W3's canon (four holes — both hands, both greaves, measured
coverage 20 of 24, 0.833), regenerate all eight twins from the completed canon, recomposite.
**That costs Comfy Cloud credits and the Director approves the spend personally.**

That plan is correct **if and only if the flats are in the twins.** If a flat region is
already flat and wrong in `twin.png`, regeneration is the lever and the canon is the reason.
If the twin is clean there and the flat appears only after projection, then regeneration
buys nothing and we would be spending his money on the wrong stage.

**Nothing in the record answers this.** Your #11 established that the plate-disagreement map
cannot separate those worlds. This question can be answered directly, from files already on
disk, for free.

## The instrument, which you have already proven

`surfid` is invertible and out-of-bounds-free on all eight views — your own #12 chip. So a
defect pixel in a render maps to an atlas texel, and that texel maps back into whichever
view's twin the scatter took it from. The twins are at
`E:\AI\training\facet_E45\aov\view_{0..7}\twin.png`, and E51's own sheets cite that path in
their provenance footer.

Build the trace: **render pixel → atlas texel → contributing view → that view's twin pixel**,
then compare what the twin holds there against what the atlas holds and against the
reference. Tool in `tools/`, tests at **t89** — note the number moved, the canon-gate wiring
I had queued as t89 is now **t90** and stays queued behind this.

## What it has to report

1. **For each confirmed flat: is the source twin flat there too?** Not a similarity score —
   the twin crop beside the atlas crop beside the render crop, at native zoom, plus the
   numbers. Build the sheet before the metrics; a number says a region is wrong and the
   sheet says what it was supposed to be.
2. **Which view contributed**, and whether the flats concentrate in views that were poorly
   positioned for that surface. A flat on a surface whose only contributing view sees it at
   a grazing angle is a different finding from a flat whose contributing view sees it
   head-on.
3. **Whether a flat is one triangle.** A triangle-sized flat with one contributing view is a
   scatter artifact. A flat that crosses triangle boundaries and is present in the twin is a
   generation artifact. Report the island/triangle extent, and the largest connected
   component beside the total.
4. **The straight answer to the spend question**, stated as what the evidence can and cannot
   close. If the flats are in the twins, say so and the regeneration is justified. If they
   are not, say that just as plainly — it kills the plan the whole session has been building
   toward, and that is a full result.

## Calibrate before you read a verdict off it

This repo's most recent losses are all one shape: a rule placed where the instrument cannot
discriminate.

- **Establish both poles.** What does your twin-vs-atlas comparison read on a region that is
  unambiguously fine, and on one that is unambiguously the defect? A decision line outside
  that interval is not a line. Your #14 did exactly this with exact-magenta against an
  interior control and it is why that result is usable.
- **Say which side your evidence can close.** *The twin is flat here* proves the defect
  predates projection. *The twin is clean here* proves it about **that view only** — it
  cannot poll the other seven unless you check them. State the asymmetry before you look.
- **Do not let E50's two confirmed instances define your detector.** They are a validation
  that it fires where a human pointed, not its input. Write it against the specification of
  the defect and locate flats over the whole figure, all eight views.

## Argue

1. **Is "in the twin" even binary?** A twin region can be correctly painted and still produce
   a flat if one view wins a whole triangle under the facing weights. That is a third world
   and it has a different repair from both branches above.
2. **Is the reference the right comparator, or the twin?** The twin is the projection source;
   the reference is what the Director judges against. They can disagree, and which one a
   flat departs from decides whether this is a generation defect or a canon defect.
3. **Would a completed canon plausibly touch these regions at all?** The four holes are hands
   and greaves. The flats are on tunic, collar and skirt — surfaces that **are** named. If
   the flats sit on already-named surfaces, the canon build-out may not be the repair for
   them, and that reframes the whole staged plan.
4. **Anything unnamed.** Four rounds running you have refused a brief's framing and been right.

## Constraints

No GPU, no cloud generation, **no credits**. Read `E:\AI\training\facet_E4*\` and
`facet_E5*\`; write to neither. Change-set uncommitted for the advisor's fold. Gates
`raise`, never a bare `assert`. Tests ride the commit, and a test that cannot fail is not a
test. No quality words — the Director's eye is the only acceptance gate.

Counts: HEAD is folded through t88 at **1233 / 1181 / 52**. State what your change-set
assumes; reconcile nothing you did not move.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Fourteen for fourteen, and a round where the chip loses is still reported.
