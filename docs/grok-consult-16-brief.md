# Grok build #16 — the diagnostic layer, because we keep rebuilding it

**2026-08-17, facet advisor seat. BUILD round.** Supersedes brief 15's *form*. Its
question stays and becomes a query against this layer instead of another bespoke script.

*Everything below the line is the paste block.*

---

# Fourteen for fourteen. Stop me: every arc here rebuilds the same diagnostic from scratch, and I have been commissioning one-off scripts while calling it tool-building.

## The waste, counted

**Seven sheet builders**, one per arc: `facet_E40_A/task3_sheet.py`,
`facet_E41/.../find_regions_and_build_sheets.py`, `facet_E47/build_sheets.py`,
`facet_E48/build_sheets_e48.py`, `facet_E49/build_sheets_e49.py`,
`facet_E50/build_sheets_e50.py`, `facet_E51/build_sheets_e51.py`. Same sheet. Seven
implementations, 7–16 KB each.

**33 throwaway scripts** written into training trees in this session alone — base-rate
computers, cross-tabulators, provenance classifiers, gate scripts. **Three separate seats
wrote a `surfid` decode this session**, in three files, none of them reusable by the next
one. E50 found a fifth provenance class *by accident, while rebuilding base rates for
something else*, because no standard readout existed to have shown it four arcs earlier.

None of that is in the repo. None of it is tested. None of it survives its arc. The next
arc will write an eighth sheet builder.

This is not a tooling gap at the edges — **it is the diagnostic layer missing entirely**,
and every arc pays for it in a session that could have been a command.

## What to build

**One entry point that takes a subject and a state and emits the standard evidence
bundle.** Tool(s) in `tools/`, tests at **t89**. Invocable in this repo's sense —
`argparse`, real flags, a `__main__` guard — and, more importantly, **importable**, so the
next arc extends it instead of re-rolling it.

The bundle, at minimum:

1. **Provenance classification, one implementation.** All five classes — `written`,
   `filled`, `orphan_fill`, `no_view_visible`, `unmapped` — in both atlas and rendered-pixel
   space, with the space named in every field. Three seats wrote this three ways this
   session and one of those ways found a class the other two missed.
2. **The acceptance sheet.** `reference | shipped | candidate(s)`, native zoom, per view,
   with region crops driven by a spec file rather than hardcoded boxes, and the provenance
   footer that already carries sha256 per consumed artifact. **The sheet comes before the
   metrics** — a number says a region is wrong, the sheet says what it was supposed to be.
3. **The standard numbers, with their denominators declared.** Every rate beside its base
   rate; every count beside its largest connected component; every share carrying which
   space it is in. Atlas share and rendered share differ by 5.4x on this subject and the
   record has been burned by that exact confusion.
4. **A manifest that makes the whole bundle replayable** — inputs, hashes, resolved
   parameters. The arcs already do this by hand, unevenly.

## Reuse, and do not re-roll

`emit_view_aovs` (surfid, and its invertibility is your own proven chip) · `palette_gate`
(LAB bands, chroma floor, two-threshold reporting) · `callieri_border` · `canon_gate` ·
`s3_sheet` and `tools/s3_sheet_regions.json` · `region_disagreement` · `unmapped_readout` ·
`texel_provenance` and the eight instruments behind `measure_mcp`. **Enumerate before you
commission** — this advisor has lost three sessions to building something that was already
a flag on an existing tool, and the seven sheet builders above are the same failure at
arc scale.

## Argue, and I expect you to cut this down

1. **Is one entry point right, or is it a library plus thin verbs?** A monolith that must
   know every subject class is how this ends up unusable for the galleon.
2. **What actually belongs in the layer versus in an arc?** Some of those 33 scripts
   *should* be throwaway. Drawing that line wrongly in either direction is the failure —
   name the test for which side something falls on.
3. **Does this subsume brief 15's question** — are the flat patches present in the source
   twins — as a query against the bundle, or does that need its own instrument? If the
   layer is right, that question should be a flag, not a build. If it genuinely needs its
   own tool, say so and it goes back to being its own round.
4. **What does this cost the arcs that already ran?** Their numbers were produced by the
   throwaway scripts. A layer that cannot reproduce a recorded figure is a layer with an
   unmeasured discontinuity underneath it — pick which recorded numbers you re-derive as
   anchors, and report any that do not come back.
5. **Anything unnamed.** Five rounds running you have refused a brief's framing and been
   right every time. This brief is the most likely yet to deserve it.

## Constraints

No GPU, no cloud generation, **no credits**. Read `E:\AI\training\facet_E*\`; write to
none of them. Change-set uncommitted for the advisor's fold. Gates `raise`, never a bare
`assert`. Tests ride the commit, and a test that cannot fail is not a test. No quality
words — the Director's eye is the only acceptance gate.

Counts: HEAD folded through t88 at **1233 / 1181 / 52**. State what your change-set
assumes; reconcile nothing you did not move.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Fourteen for fourteen, and a round where the chip loses is still reported.
