# Comfy consult #11 — brief

**Written 2026-08-16, facet advisor seat. No build unless you find a route worth building.**

Subject: **the fourth domain you and we jointly landed on in #10 — the atlas/UV layout — now
measured on a second subject and a second axis.** Rounds #8–#10 are in
`docs/comfy-consult-8-10-log.txt`.

⚠ **Advisor's note for the record, not part of the paste block:** an earlier draft of this brief
was numbered #9 because this repo's `docs/` stops at consult 8 — rounds 9 and 10 were never filed
here. That draft re-asked things #8–#10 had already answered (`TencentModelTo3DUVNode`,
`TripoImportModelNode`'s external-mesh path, the task-id wall) and would have wasted a round. The
log is now committed alongside this file so it cannot happen again.

*Everything below the line is the paste block.*

---

## Where this round comes from

#10's give-back was our `margin_method`/SCALED finding: the packer silently ran Blender's default,
so gutters scale with island size and our ~88-texel median islands got sub-texel gutters —
5.73% of 4-adjacent valid texel pairs cross-island and touch. You banked it as the fourth-domain
lesson: *"the defect wasn't in any process you were hunting through, it was in the shared
substrate every process inherited."*

**We have now measured the same substrate on our other subject and on a different axis.**

⚠ **Different subject from #8–#10.** Those rounds were the performer — the jointed wooden
mannequin with the painted-on face. This measurement is **W3**, a standing dwarf warrior holding a
greatsword, textured by the older per-view projection route. Same pipeline family, different
asset. Please don't conflate them.

**W3's atlas, 4096×4096, 2,402,810 valid texels:**

- **9,166 separate UV islands.**
- **Median island 102 texels** (~10×10 px) — consistent with the performer's ~88.
- Largest single island: **0.79%** of painted area.
- **93% of islands are under 500 texels**, holding **43.6%** of painted area.
- **17.8% of painted area lies within one texel of an island edge** — and that is a *one-texel*
  rim; our dilation runs wider.
- The sword blade alone (7,582 faces) is spread across **2,276** separate atlas components.

So the margin finding was gutter *width*; this is island *count* and boundary *fraction*. Same
domain, two axes, two subjects. Rendered, the atlas is confetti: thousands of ~10×10 blobs in a
packed grid, every one with a boundary that gets dilated.

## What we killed this week, so you don't propose any of it

Four arcs on the colour side, all negative — which is what pointed us back at the substrate.
**Correct us if any of this looks wrong; that is worth more than agreement.**

- **Blend-weight variants** (multi-band, hard-select, flat facing-weighted) — Director looked at
  all four at native scale, called them indistinguishable.
- **A Callieri-style border-distance weight** — ceiling 45.97% against a null of 100%; the owning
  view is already the best available view 47.53% of the time. Nothing to reallocate to.
- **Camera rig changes** — blade already **96.35%** reachable against a measured **99.75%**
  ceiling; a ±30° interleaved ring and a downward camera each buy ~2 points. Coverage is not the
  problem. *(This also withdrew our own long-cited "74.28% of the blade is never hit" — it turned
  out to be a rasterized-sampling statistic, not a visibility one. The reductio: the same
  instrument reports 97.99% never-hit on the **torso**, which is the best-covered surface on the
  figure.)*
- **Source resolution** — a 2× twin frame reaches only ~15% of the affected population; the rest
  persists at 4×.
- **Straight-vs-premultiplied alpha in our sampler** — measured **0.00e+00** against a fixture
  calibrated to detect the error.
- **Minification aliasing as the differentiator** — defect texels are *less* minified than clean
  neighbours (0.380 px vs 0.650 px footprint).

## What we already hold locally, so you don't route us to a vendor for it

**`xatlas 0.0.11` is installed and current on our rig**, alongside `pymeshlab 2025.7` and Blender
5.2 LTS with every packer lever exposed. **We can re-unwrap locally.** So a served UV path only
earns its place if it produces a *materially better layout* than xatlas with well-chosen
parameters — not merely if it exists.

Please answer with that in mind: we are not asking you to find us an unwrapper. We are asking what
the served ones actually *emit*, so we can decide whether any is worth the round trip.

## Q1 — The Tencent UV/topology pair, traced to producers

`TencentModelTo3DUVNode` (your #8 enumeration: UV only, face cap <30,000) and
`TencentSmartTopologyNode`. For each:

- Exact input and output types, **traced to their producers** — the MODEL_PATCH lesson.
- **Is the face cap on the input mesh or the output mesh?** Decisive for us: W3 is **287,170
  faces**, so a 30k input cap means a ~10× decimation before the node ever sees it.
- **What UV layout does it actually emit** — roughly how many charts for a humanoid, are seams
  authored or automatic, is there any margin/gutter control exposed?
- Do the two chain — our mesh → smart topology → UV — and does topology preserve UVs or discard
  them?
- Licence bucket.

## Q2 — Anything that operates on a UV atlas *as an image*, with its mesh

Distinct from texturing, and distinct from #9's albedo-recovery question and #10's material-map
question, both of which came back empty. We mean: **seam repair, chart merging, gutter/dilation
control, or UV-space inpainting** on an atlas we supply together with the mesh it belongs to.

If the answer is another empty population, say so plainly — three empties in a row is itself a
finding about where this catalog's coverage ends, and we would rather have that than a stretch.

## Q3 — The face-cap ceiling across the whole external-mesh population

Every cap named in #8: Tripo P1 20,000 · Tencent texture-edit 100,000 · `ModelTo3DUV` <30,000 ·
`TripoImportModelNode` ≤150 MB. Our prep target is ~300,000 faces.

**Is there ANY served path that accepts an external mesh above 100,000 faces for any topology or
UV operation?** If not, decimation before any served route is a hard planning constraint and we
want it stated as one, because it interacts with a silhouette we have already measured and do not
want to lose.

## Q4 — Currency, mesh side

#10 covered the material side and found it thin and static. Same question for the **mesh/topology/
UV** population specifically: anything landed that bears on getting a coherent UV layout onto a
mesh someone else made?

## Calibration

Nominate **one checkable claim**, schema- or catalog-level, resolvable by a single fetch on our
side before anything acts on it.

Standing scorecard across ten rounds, said plainly because it is how we weight you: **your
inventory has held every time we have checked it; five mechanism claims have fallen** (MODEL_PATCH's
producer, Seedance 2.x, "closest thing to a coupled operator", the relight direction, and Route A's
UV-space reasoning). We take your inventory and do our own mechanisms. That is not a demotion — it
is using the instrument on the axis it is calibrated for. Keep to inventory and we keep taking it.

## Build

**Only if Q1 or Q2 turns up a route worth having.** If it does, yes — build it, and the rules
below are binding.

### ⚠ RULE 0

**Before fetching ANY template, create and focus a new empty tab. A template fetch lands in the
focused tab and will overwrite whatever is there. If you cannot confirm the focused tab is empty,
STOP.**

### The eight rules

1. **Tabs** — new, empty tabs only. Never open/edit/repurpose/rename/overwrite an existing tab,
   however much it looks like a draft or scratch. Assume every tab holds work.
2. **Out of tabs → STOP.** Never reuse or clear one to make room. Partial delivery is fine.
3. **Never delete or rewire a node in a graph you did not create this session.** Report what looks
   broken; leave it alone. It may be deliberate.
4. **Named models/nodes are NOT substitutable.** Unavailable, deprecated, or you think something's
   better → stop and ask. A silent swap is a different deliverable.
5. **Exact names, saved.** Graphs are addressed by name later; a renamed graph is lost.
6. **Build only what is listed.** No adjacent tidying.
7. **Report precisely** — tabs created, nodes added, anything left alone under rule 3, and any
   deviation stated at the TOP of the reply, not in passing.
8. **Halt conditions** — missing named model, wiring the named node won't accept, a template with
   baked-in settings contradicting the stated config, or anything touching existing work.

## Give-back

**The W3 island census above** — 9,166 islands, median 102 texels, 17.8% of painted area within
one texel of an edge. It extends the margin/SCALED finding to a second subject and a second axis:
gutter width was the first axis, island *count* is the second, and they compound — many tiny
islands with sub-texel gutters is how you get 5.73% of adjacent texel pairs touching across a
chart boundary.

**A tooling lesson that generalises past this project.** Our own measurement server attaches an
identity envelope to every payload — server version, instrument file hash, config hash — and
refuses to compare across a mismatch. We found it can certify a *correct* instrument hash for a
call that **silently discarded half its own arguments**, because the long-lived wrapper module was
loaded before an edit landed while the subprocess it invokes reads from disk at spawn. Nothing
mismatched, so the refusal never fired. What caught it was an unrelated echo field printing the
parsed arguments back.

**An identity block describes what a tool IS. It cannot describe what a specific call DID.** Those
drift apart silently, and only an echo of what a call actually consumed closes the gap. Yours to
keep — it applies to any served node surface, including yours.
