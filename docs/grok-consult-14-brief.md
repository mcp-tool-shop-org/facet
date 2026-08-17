# Grok build #14 — the class nobody has looked at, and it is the one the eye lands on

**2026-08-17, facet advisor seat. BUILD round.** Briefs 11–13 folded; thirteen nominated
claims, thirteen held. Brief 13's chip corrected a claim the record had carried for days.

*Everything below the line is the paste block.*

---

# Thirteen for thirteen. E50 found a fifth provenance class at 11.58x enrichment and stopped, because it was out of its scope. Nobody has been back. Go look.

## Why this and not the canon wiring

`canon_gate.py` exists and nothing calls it — that is the same defect as the canon
existing and nothing reading it, one layer up, and it is queued as the next build (t89).
It is not this one, because it gates a spend that has not happened yet.

This build is about what is on screen **now**. The Director's judgment on the current
renders is that they still look bad. Three arcs of composition repair did not move that,
and E50 handed us the strongest unexplained signal in the whole session and then correctly
declined to chase it out of scope.

## The measured facts you are starting from

**E50's per-class enrichment at the confirmed defect pixels**, over 2,028,512 figure
pixels across 16 view/mode cells:

| class | base rate | enrichment at flagged pixels |
|---|---|---|
| `written` | 96.996% | 0.93x |
| `filled` | 2.259% | 1.18x |
| `orphan_fill` | 0.0821% | **0.27x — depleted** |
| `no_view_visible` | 0.0860% | 2.21x, but 98.9% of it is magenta-hued |
| **`unmapped`** | **0.5777%** | **11.58x — the strongest measured, and untested** |

E50 found `unmapped` while building base rates for something else. It is not in any
dispatch, has no report of its own, and no repair has ever addressed it.

**The advisor's own observation, walked at full size and marked as an assumption, not a
measurement.** E51 cut sentinel from 5.57% to 0.121% of valid texels in blend mode — a
46x reduction — and its renders still carry substantial magenta in the same regions as
E49's. A 46x cut in the atlas that does not appear on screen means the denominator
excludes whatever is actually visible. **My hypothesis is that the visible magenta is
`unmapped`, and that both fill arms were structurally unable to reach it because they
operate on valid texels and unmapped texels are not valid.** I have not verified this.
It is exactly the kind of inherited claim this repo treats as a hypothesis wearing a
fact's clothes — check it before building on it, and say so if it is wrong.

**The space law, which governs every number you report here.** Every `dilation` figure
this repo argues from is in atlas texels; the defect is judged in rendered pixels; on W3
those differ by **5.4x** — 26.95% of the written atlas against 4.95% of what a camera
sees, a ratio of 0.18x. Paint lives in big charts and holes live in small ones. The
question is what the asset looks like, so **rendered pixels is the space that decides**,
and any atlas share you quote carries its space in the sentence.

## The mechanism already on the front page, and never repaired

`docs/known-defects.md` and the README both carry this: some visible surface maps to
atlas space that no bake ever writes, and renders as the image's untouched default.
Blender's baker uses texel-centre sampling, so a triangle overlapping no texel centre is
left empty. Its own developers named the mechanism and merged a fix — reportedly
`projects.blender.org` PR **161752** — about two weeks after the build every number here
was measured on. Adjacent prior art in that tracker: PR **162226** and issue **119393**
on the `ADJACENT_FACES` extend behaviour and its defect catalogue.

⚠ **Those citations are the advisor's, second-hand, and this repo has been burned by an
identifier written down without being resolved.** Resolve each at its primary source
before weighting it — `projects.blender.org` 403s a plain fetch and answers at `/api/v1/`
— and report any that do not say what this brief says they say. The measured share is
that roughly 60% of the dark-mark class was atlas texels no bake ever writes; that figure
is also inherited and also worth checking.

## What to build

A tool in `tools/` plus tests at **t88**, invocable in this repo's sense — `argparse`,
real flags, a `__main__` guard.

It has to answer, in rendered-pixel space, on the E49 and E51 render sets:

1. **Is the visible magenta `unmapped`?** Confirm or refute my hypothesis outright, per
   view, per mode, with the classes separated rather than lumped.
2. **How much of what a camera sees is unwritten atlas**, and where — by region, by
   material, and with the largest connected component beside the total, because a total
   alone must choose between missing the defect and firing on speckle.
3. **What would fix it**, scoped and measured rather than asserted. Candidates, all
   hypotheses: the merged upstream sampling fix; the `EXTEND` / `ADJACENT_FACES` arm that
   an earlier hunt found working; a high-to-low transfer bake, which every documented
   pipeline keeps and this route skips; or a purely atlas-side repair that needs no
   re-bake at all. Rank them by what they cost and what they can reach.

## Argue

1. **Is `unmapped` even one class?** 11.58x on a class that is 0.58% of the figure could
   be one mechanism or three wearing one label — bake misses, UV gutter, and genuinely
   unassigned texels are different problems with different repairs.
2. **Can this be repaired without re-baking?** A re-bake re-opens every number measured
   against the current atlas. An atlas-side repair does not. That difference may decide
   the ranking on its own.
3. **Does the enrichment survive a proper control?** 11.58x came out of a scan E50 itself
   disclosed as over-inclusive. Before anything is built on that number, establish what
   the instrument reads when the answer is definitely yes and definitely no, and say
   where a decision line can honestly sit between them.
4. **Is the magenta even the thing the Director is reacting to?** He may be reacting to
   something else entirely and the magenta may be the loudest thing rather than the worst
   one. The sheets are at `E:\AI\training\facet_E49\sheets\` and
   `E:\AI\training\facet_E51\sheets\`. Look before you agree with the brief.
5. **Anything unnamed.** Three rounds running you have refused a brief's framing and been
   right each time.

## Constraints

No GPU, no cloud generation, **no credits** — everything you need is on disk. Read
`E:\AI\training\facet_E4*\` and `facet_E5*\` freely; write to neither. Leave the
change-set uncommitted for the advisor's fold. Gates `raise`, never a bare `assert`.
Tests ride the commit, and a test that cannot fail is not a test — construct the case
that fails if the code is wrong in the way the leg exists to catch, and show it failing.

Count surfaces: HEAD is now folded through t87 at **1223 / 1173 / 50 artifacts**. State
what your change-set assumes and reconcile nothing you did not move.

No quality words in the output. The Director's eye is the only acceptance gate, and the
deliverable that reaches him is an image.

## Calibration

Nominate **one checkable claim** — about the tree, a number, or a mechanism in a file you
cite — that we verify by running it before anything trusts the rest. Thirteen for
thirteen, and a round where the chip loses is still reported.
