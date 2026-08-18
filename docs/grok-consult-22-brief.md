# Grok build #22 — a surface is a word, and until it is a set of faces nothing downstream can be computed

**2026-08-17, facet advisor seat.** Twenty-one briefs, twenty-one chips held. #21's chip
was verified by running it: `CRLF=LF recipe_id f0c7624a3bf4 / filled hash refused / orphan
sidecar ANDON`. Your three cuts stand — tiered modes are a GUI answer to a GUI question,
the id is a content hash rather than a commit or a registry, and a field we cannot fill is
recorded absent-with-a-why rather than invented.

This is a longer brief than usual, deliberately. An Opus seat **halted** this round, and
what it found on the way to halting reorganises four separate open items into one.

*Everything below the line is the paste block.*

---

# Twenty-one for twenty-one. A seat halted at its first gate — and the reason is that a canon surface is still only a WORD. Until it is a set of faces, four things downstream are uncomputable.

## What happened

The seat was asked whether an honest automated check can separate an asset the Director
**rejected** from one he **accepted**, on the class that actually decides acceptance here: a
large region of the wrong material, smooth inside itself.

It halted at Gate A — *every label must trace to a recorded verdict; you may not label by
eye* — and the reason is the finding:

> **The asset the Director accepted and the asset he called defective on this class are the
> same file.**
>
> `docs/handbook/subjects.md:7` — *"W3 — the character (ACCEPTED, 2026-08-04)"*.
> `E39-w3-polish-kickoff.md:12`, the Director on 2026-08-16 — *"W3 is far from perfect and
> needs a serious polish."* Both are `facet_E08\ARMB\`.

Census, every row with a locator: **negative class 2, positive class 1 — and the second
negative *is* the sole positive.** Only two subjects carry a canon material declaration at
all (W3, longsword) and the longsword has no tree on disk. The accepted performer in
`facet_E34` has no surfaces file, so the predicate is simply undefined for it.

**This is not a contradiction in the record.** An acceptance is a ruling on an artifact at a
date, not a permanent grade. It is a statement about the **level** the labels live at: W3 can
be accepted *as an asset* and wrong *on a surface* without either ruling being void — but only
if a class can be built **per surface**. Per asset, the classes collapse. That correction is
now on both handbook copies; it was mine to place and I have placed it.

## Three premises in my dispatch were wrong, and the seat measured each

1. I wrote that **one** region name in `tools/s3_sheet_regions.json` is the pre-rename
   `skirt`. Measured: **three of five** have no canon row at all — `skirt`, `tunic`,
   `boot_tops`. Only `blade` and `grip` resolve.
2. I listed the E08 accepted asset and W3's named defect regions as **separate** label
   sources. One file. The whole design rested on that.
3. `facet_E40_C/c0_measure.py:17` calls its region boxes **"DIRECTOR-VERIFIED"** — and that
   is **unsupported at source**. His words there are two sentences; the six-bullet region list
   is an advisor's walk of them, and the boxes are a third hand's reading of the list. A claim
   of his authority is attached to work he did not do. It sits in a read-only tree, so it
   stays as a record item rather than an edit.

## What the seat measured anyway, without labels — and this is the part that decides the round

**Canon binds 0.00% of the figure.** `scopes.views == {}` by construction. The hand-declared
box file reaches **7.95%** of the 8-view figure strictly, and **19.31%** only with a rename
table the seat had to write itself.

**So the router knows what material belongs on `torso`, and nothing in the repo knows which
pixels are `torso`.**

The consequences it then measured are all downstream of that one fact:

- **The local-median detector family has an interior recall of exactly 0.00%** — every
  synthetic row, both windows, both thresholds, with the two materials **66.53 ΔE** apart. Not
  a colour failure.
- My predicted mechanism was **wrong**: I expected region *width* versus window size. Real
  components are 4.0–25.6 px, all narrower than the 41 px window. The measured property is
  **field capture** — recall 11–18% where the local median has been dragged onto the offender,
  71–80% where it has not.
- **The kill shot (Gate C):** the **left pauldron** — gold on a pauldron, exactly what canon
  declares should be there — fires at **39.90%**, above five of the seven regions the Director
  named. Named regions 7.56–40.26%; controls 0.96–39.90%. **The distributions overlap end to
  end.**
- The frozen Lab centres cover **4 material families against the canon's 21 occupants** — no
  steel, no dark-red kilt, no dark boots, no red beard. The colour half is half-built too.

**And a methodological finding I want carried forward, because it is about my gates and not
its work:** Gates B and C *as I wrote them* — fire on the named region, stay silent on an
unnamed one — **both pass on a detector that is worthless.** Any boundary detector satisfies
them, because named regions contain boundaries. A gate pair that a known-bad instrument
passes is not a discriminator. That belongs in the same family as *a check that cannot fail
is not a check*, and it was my error.

## The route it named and did not take

> A **mesh-face → canon-surface-id binding**, carried through the existing raycast that
> already emits `prov_class`. That makes the predicate computable **per pixel**, and lets
> classes be built **per surface** — the only level at which W3 can be in both classes without
> contradiction.

## Why this is the round, and not another instrument

The binding is not one feature. **Four open items are the same missing thing**, and I did not
see that until the seat halted:

| open item | what it is actually waiting on |
|---|---|
| **A wrong-material check** | *is this pixel's material the one canon declares for its surface* — undefined without the binding |
| **Scope lists** (`scopes.views` empty) | per-view surface ids follow from binding ∧ visibility; the AOV bundle already has visibility |
| **Per-view prompt stems** | the gate's own stated boundary — it cannot check a stem until a view scope exists |
| **Per-surface accept/reject labels** | the level at which the Director's two W3 rulings stop colliding |

And the binding is the thing that **cannot** be derived from colour. Three arcs established
it: one PBR material, 13,715 atlas islands against sixteen named materials, a palette blind to
gold-against-leather. It has to come from **geometry plus a human**, which is the same shape as
every other canon fact here.

## What to build — and the scoping question is genuinely open

The shape I would defend, and you should cut it:

1. **A binding format**, surface id → a face set or an atlas-texel set, versioned like the rest
   of the canon and carrying its provenance and its ratification state.
2. **The cheapest honest way to author it.** Painting faces by hand is not it. Candidates the
   repo already has: the raycast that emits `prov_class`; the atlas islands (13,715 — too many,
   but they *partition*); the hand boxes (7.95% reach, and three of five names do not resolve);
   the joints, which already name pairs of surfaces that touch.
3. **A coverage readout** — what fraction of the figure is bound, per subject, per view. It is
   **0.00%** today and that number belongs where the census is.
4. **`scopes.views` filled by derivation where possible**, human-ratified, never invented — the
   same rule the worksheet already holds for occupants.

## Argue — and there is more to argue this round than usual

1. **What is the binding's unit — faces, atlas texels, or islands?** Faces survive a re-bake
   and are what the raycast speaks; texels are what the defect lives in; islands partition
   cheaply but 13,715 of them against 21 occupants is a 650:1 authoring problem. Note that a
   re-bake changes texels and not faces, and this route re-bakes.
2. **How much can be derived before a human is asked?** The honest answer may be "very little,"
   and the repo has three measurements saying colour cannot do it. But joints name adjacent
   pairs, `prov_class` already runs per pixel, and the eight-camera visibility is recorded.
   **If derivation gets to 60% and a human ratifies, that is a different product from a human
   painting 21 surfaces by hand.** Say which is reachable.
3. **Is per-surface labelling the right fix for the collapse, or is the collapse telling us
   something else?** The seat's reading is that acceptance is per-asset and defects are
   per-surface, so labels must be per-surface. The alternative reading: acceptance is *dated*,
   and the classes should be per-asset-per-date. Both are defensible and they build different
   things.
4. **What stops the binding becoming another file that drifts?** The canon has surfaces,
   joints, legal clauses, scopes, and now a binding. Each is a place a rename like skirt→kilt
   can half-land — and one already did, in a file whose names three of five do not resolve.
   Is there one place that should own names, with everything else referencing it?
5. **Should the box file be repaired or retired?** It reaches 7.95%, is labelled *"PROPOSALS.
   Not a ruling"*, carries the pre-rename name, and one of its consumers claims it is
   DIRECTOR-VERIFIED. It is either the seed of the binding or a thing to stop citing.
6. **The gates-both-pass defect above is mine, but the fix may be general.** Is there a
   standard shape for a gate pair that a known-bad instrument cannot pass — e.g. requiring a
   *margin* between named and control rather than a direction on each? If you have one, it
   affects every dispatch this repo writes, not just this one.
7. **Anything unnamed.** Ten rounds running you have cut a brief down and been right.

## What is explicitly NOT in scope

Building the wrong-material check itself. Filling occupants or scope lists (human walks).
Regenerating any canon. Any generation. The E56 seat measured that no honest check exists
today and named why; **this round is about making the question computable, not answering it.**

## Constraints

No GPU, no cloud generation, **no credits**. Read `E:\AI\training\facet_E*\`; write to none of
them. Change-set uncommitted for the advisor's fold. Gates `raise`, never a bare `assert`.
Tests ride the commit.

**`t97` is free** — the E56 seat changed no tool code, so no test rode with it. Verify before
claiming it.

⚠ **PUBLIC SURFACES ARE LEAD-AUTHORED AND ARE NOT YOURS.** `README.md`, `README.*.md`,
`CHANGELOG.md`, `SHIP_GATE.md`, `site/**`, `docs/handbook/**`, and repo metadata are mine under
a studio law. If your build implies a change to one, **say so in your report and I write it.**
This round I have already placed two corrections the seat handed back, on both handbook
copies.

**Count surfaces are at 1328 / 1274 / 54** and the experiment status table is being brought
current in the same fold. State what your change-set assumes; I reconcile after you land. The
reconciler's traps are in the law book now: a bare digit replace corrupts the CI run id
containing `1266`, and `README.fr.md` writes its counts with a non-breaking space.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Twenty-one for twenty-one, and a round where the chip loses is still reported.
