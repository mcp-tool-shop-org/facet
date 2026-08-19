# E68 — the head-band withhold: geometry says hair, paint says wall, leave a hole

**Advisor spec, 2026-08-19. One executor seat (Sonnet), background. Tree
`E:\AI\training\facet_E68\`. ZERO CLOUD. ZERO THRESHOLD CHANGES. Prep stays halted until
this sitting's remap exists.**

**Direction (the Director, 2026-08-19, paraphrased):** on the head band only, withhold
projection where the twin pixel is backdrop. Geometry says hair, paint says wall — leave a
hole; dilation or a later brush fills from real hair paint. That is the thin-structure rule
without importing the greatsword's number. Prove it by remapping: the amber mass should
collapse and the 2% limit should pass **without being touched**.

## The finding this executes

E67's map, pooled over 27,761 flagged pixels: **hair/silhouette fringe 78.94%**, declared
material 2.14% (sleeves only), true exterior 0.22% (sixty pixels, all 1 px off the
silhouette — rounding), unclassified 18.71%. Mouth and face_skin matched nothing. The
advisor's cream-vs-grey ruling is **dead**; the instrument is **right**.

The mechanism, stated as the Director stated it: **TRELLIS blunt volume against Qwen fluffy
curl.** The painted curls stick out past the raycast mesh line — the left puff most — and
`project_twins` still owns those texels (head band, looser facing floor), looks up the twin,
and finds pale-grey studio wall. The ANDON exists to catch exactly that: *do not bake the
wall onto the hair.*

⚠ **The amber in E67's overlay is the MAP, not a glow on the man.** The twins do carry a
warm rim light at the crown — that is paint. The amber is the contamination class drawn on
top. A future reader must not confuse them.

## The change — one rule, no new constant

On **head-band faces only** (the same band E67 Stage 1 measured: 139,603 of 990,670 faces
across 5,080 islands — reuse that definition, do not re-derive a different one), a texel
whose twin sample is background is **NOT WRITTEN**. It becomes a hole.

**The background test is the tool's OWN existing `dE_bg` computation at its existing
window** — the same number that flagged, used as a write gate instead of only a halt
condition. **No new threshold is introduced and neither limit is touched.** Do not build a
colour key: corner-median keying has failed four times here and this backdrop spans
L\* 48.14–81.12.

**Nothing outside the head band changes.** The body, sleeves, garment and shoes project
exactly as before — their texels are not in the band and the rule cannot reach them.

## Proof — the remap is the deliverable

Re-run E67's own classification, unchanged, on the withheld bake:
- **The amber (class 3) mass should collapse.** Report the new pooled share against 78.94%.
- **The 2.0% limit should pass without being touched.** Report the per-view flagged
  percentage against it. If it does not pass, that is the result — report it and halt; do
  not touch the limit.
- **Report the hole cost honestly**: what fraction of head-band texels ended up unwritten,
  per view and pooled, and where they sit. A withhold that leaves the whole crown empty is a
  finding, not a success.
- **The 18.71% unclassified stays DRAWN, not absorbed.** Re-examine it: if it is
  hair-adjacent with no palette box, it is the same phenomenon and the withhold should take
  it too — report whether it did, and by how much.

## Gates

- **Gate A** — no cloud call; a submission attempt halts.
- **Gate B** — `bg-de` and `bg-max-pct` are byte-unchanged at close; assert it in code and
  print both values in the report. Changing either is a halt.
- **Gate C** — the withhold touches only head-band faces; prove it by comparing a
  non-head-band region's written texels before and after (they must be identical).

## Out of scope, named — all the Director's

Remeshing the hair; regenerating the ring; loosening `bg-max-pct` or `bg-de`; starting the
brush; the palette-aware probe (**dead — E67's map killed it**); dilation or hole-filling
(a later step: this sitting leaves holes and measures them); binding, which still does not
gate any of this.

## Standards compliance

1. **PIN_PER_STEP — 3.** Same mesh, same accepted ring, same cameras, same thresholds; one
   rule changes, on one face band, with the band's definition inherited rather than re-derived.
2. **ANDON_AUTHORITY — 2.** Gates A/B/C halt; the 2% limit failing is a reported result, not
   a tuning opportunity.
3. **NAMED_COMPENSATORS — 2.** Zero spend, new training tree, repo edits by pathspec.
4. **DECOMPOSE_BY_SECRETS — 2.** The withhold rule, the bake and the remap are separable.
5. **UNCERTAINTY_GATED_HUMANS — 2.** Prep stays halted; the first brush still waits on the
   Director, and this sitting does not approach it.
6. **EXTERNAL_VERIFIER — 3.** The proof re-runs E67's own unchanged classifier over the new
   bake — the instrument that produced the finding judges the repair, and it was never
   tuned for either.
