# Spec 2 — the mesh/texture measurement MCP

**Charter.** Authored by the advisor (spec-author seat), 2026-08-08. **Nothing is built.**
Second in the banked build order, after [the record index](index-mcp-spec.md).

---

## The job

**Identical measurement of any mesh or textured asset — the numeric half of a
comparison.**

The reason this is a product and not a folder of scripts is one sentence from
`mesh_stats.py`'s own docstring: *comparisons across generation arms are only worth as
much as the sameness of the instrument.* Two meshes made months apart by different tools
are comparable only if one code path measured both. Every studio pipeline that generates
3D — the golden 3D path, sprite pre-render, the facet route — currently answers "did that
change help?" with numbers whose instrument identity nobody can guarantee.

This serves the games directly. The pipeline is the studio.

**Extraction timing is met:** the banked note said extract *after* four subject classes,
and the fourth (the prop) closed at Gate 1. A four-class-proven instrument beats a
three-class one, and the classes disagree in ways that were only visible because all four
ran — see the shells operand warning below.

## The tools

Job-shaped. A tool answers a question someone has, not "run script X".

| tool | the question |
|---|---|
| `mesh_stats` | *measure this mesh identically to every other mesh* — components (welded **and** unwelded), face-region curvature variance, bbox and std-frame extents, projected silhouette area |
| `mesh_topology` | *the topology facts `mesh_stats` does not print* — non-manifold edges and where they concentrate, boundary edges, shell census under **both** definitions, hollow/double-wall detection |
| `reach_ceiling` | *how much of this surface can a given camera set actually paint?* — the ceiling computed **before** an expensive arm is spent, using the consumer's own acceptance construction rather than an optimistic proxy |
| `thin_extent_curve` | *what does this thin-structure threshold cost on THIS mesh?* — the per-view screen-space front-to-back extent curve, with a region fraction beside it |
| `offsurface_rate` | *does this bake's position map lie on the mesh?* — with the erode test, reported as a **margin statistic** |
| `texel_provenance` | *where did this pixel's colour come from?* — projected / synthesised / dilated, per texel, as a map and a census |
| `anchor_check` | *does this recorded output still reproduce from its recorded parameters?* — the anchored-regression pattern, with the residual's **shape** reported, not only its magnitude |
| `measure_report` | *put the numbers on one sheet beside the reference* — reference · asset · provenance · error |

## The instrument laws it must carry

These are not documentation. They are behaviours, and an implementation that drops one
ships a different product.

**Quote both units, always.** *"Shells" has two definitions and they do not agree.*
Components joined by a shared **vertex** is one number; components joined by a shared
manifold **edge** is another, and on a pinched mesh the second can be enormously larger.
One tool's first draft reported "3 shells" for a longsword whose vertex-shell count is 1.
**Every count that has more than one defensible definition returns all of them, named.**

**Name the denominator, and check what it is made of.** Four pass conditions in the
source repo were mis-specified because a denominator moved. A boundary quantity is
normalised by perimeter, not area — figure area swings 1.65× between a profile and a
rear three-quarter on the same subject, so an area-fraction bound fails a clean view and
passes a dirty one. **Any ratio this server returns names its numerator and denominator
separately in the payload**, so a caller can re-normalise rather than trust ours.

**A statistic of angles is circular.** An arithmetic median of hues reported a +49.1°
move where the true direction was −8.4°, because the family straddles the 0/360 wrap.
**And below a chroma floor, hue is not a colour** — it is undefined and will read as a
rotation; a steel blade at C\* 1.6–2.8 reads as blue at hue 267 on every view. The floor
decides who votes before any statistic of them means anything, and **a hue number carries
its chroma or it is not quoted.**

**Weld before any topology or curvature number.** A glTF export splits a vertex at every
UV seam; an unwelded read reports far more shells than the surface has. The unwelded
number is kept *beside* the real one to make the difference visible rather than
confusing.

**No volumetric predicate on an exported mesh.** It is not a solid — and even welded, a
`1024_cascade` reconstruction on this route is a hollow double-walled shell, walls ~two
voxels around a cavity (E14 Ruling 3, measured three independent ways with two accepted
assets as controls). A containment query returns *outside* at the centre of a standing
figure's chest. **Tools that would need solidity refuse rather than return a number**,
and say why.

**A ray along the surface normal measures the tessellation, not the geometry.**

**A global constant must not govern a local feature.** Three instances, each costing a
session: a rectangle measured on one silhouette applied to a mesh 38% narrower; an
erosion tuned on a wide figure eating 480k texels where the surface turns edge-on; an
edge distance scaled by global width leaving a 15 px blade with no interior. **Quantities
derive per structure, or are bounded as a fraction of that structure's own width — and
the tool reports, per structure, how much of its area the operation touched.**

**Diagnostics are not gates, and the server must not blur them.** Stratum area-loss is
the best evidence in the source repo that a shipped erosion was annihilating thin
structure, and it is unusable as a halt: it is a perimeter-to-area statistic that swings
±10 points on shape alone. **Every returned metric is labelled `diagnostic` or
`gate-eligible`**, and a metric becomes gate-eligible only when someone has asked what
*else* moves it besides the thing being watched.

**A gate tests the failure mode, not the success mode — and not a proxy for it.**
Silhouette IoU returned 1.00000 on a mesh with a hole clean through it, because the ray
behind a removed face still hits geometry. A surface-aware lookup was gated on *normal
disagreement*, a stand-in that inverted on the subject's own geometry. **Where the
quantity of interest is directly measurable, the tool measures it and leaves the proxy as
a reported diagnostic.**

**Instrument identity is the contract.** Two assets measured by different versions of
this server are not comparable. **Every payload carries the server version and a hash of
the measurement configuration**, and `measure_report` refuses to place two measurements
side by side when those differ — loudly, naming which.

## The home

**IN FACET, as a Python MCP server over the tools that are already here.**

**This reverses the first draft of this spec, which said "its own repo in
`mcp-tool-shop-org`"** (ruled in the memo's rewrite, 2026-08-08, after the Director's
question). The reversal is recorded rather than silently applied — and the sharpest thing
about it is that **the first draft's own grounds argue for staying.** They were pointed at
the wrong conclusion.

Python is not a preference here. `trimesh`, `scipy.sparse.csgraph` and the numeric stack
these instruments are written against have no TypeScript equivalent worth the port, **and
a port would break instrument identity — the one property this product exists to
provide.** That sentence was in the first draft as an argument for a Python *package*. It
is a stronger argument for **not moving the files at all**: a repo migration plus the
refactor it invites is precisely the version boundary that makes two measurements
incomparable, applied retroactively to four subject classes of banked numbers.

The record already refuses this move at a smaller scale. `e12_offsurface.py` exists as a
separate file **specifically so a shipped instrument whose numbers are cited in a closed
ruling would not be edited** — its own docstring says so, in those words. Extracting the
whole family is that hazard several orders larger.

**An in-repo server imports the tools without moving a file.** The MCP surface is new; the
instruments are untouched; no version boundary is crossed. And reachability is not the cost
it looks like — a session working in another repo *mounts* this server; it does not need
the code in its tree. (The studio already runs a Python MCP server, `ai-eyes-mcp`, verified
live on this rig this session, so the form has precedent either way.)

**Extraction stays available and is gated**: the trigger is a consumer outside facet that
needs these measurements **in-process** rather than over a mount. On that day the
extraction owes an explicit re-anchoring — measure the four banked subjects with the
extracted server and record the deltas before any new comparison is trusted.

**The extraction boundary is already specified** and does not need re-deriving —
and note that it is a *code-versus-profile* boundary, not a repo boundary, so it is
satisfied inside one repo:
[docs/profiles-design.md](../profiles-design.md). Every value declares itself —
**goes in the profile** (it was a subject assumption all along) or **stays in the code**
(it is a real principle). That list is as much the deliverable as the code. A value that
turns out to need changing *outside* the profile is the finding.

**Blender is an optional backend, not a dependency.** Render-dependent tools degrade to
unavailable with a clear reason rather than failing at import; measurement tools that need
no render must work in a bare environment.

## What it does NOT do

- **It never says whether output is good.** No verdict field, no score, no quality label.
  It produces measurements and comparison sheets; the Director judges. The words
  *verified, shipped, works, decisive, validated, proven* do not appear in a payload.
- **It does not generate, repair, decimate, or modify a mesh.** Read-only on every asset.
  Where a companion pipeline needs a destructive operation, this server measures before
  and after; it does not perform it.
- **It does not decide subject values.** Thresholds come from the caller's profile. The
  server returns curves and costs so a human can decide, and will return a curve where it
  is asked for a threshold.
- **It does not judge identity or canon.** Canon is a ground truth the Director holds and
  no metric approximates it. Grading material identity with high-pass statistics and
  *character* identity with silhouette IoU are two recorded advisor errors; **a
  better-registered twin that is a different man is worse, not better.**
- **It does not gate on its own numbers by default.** Gate-eligible metrics are gates only
  where a caller arms them, and the server states what else moves each one.

## Compensators

| action | irreversible? | compensator | post-rollback state | owner |
|---|---|---|---|---|
| every measurement tool | no | none needed — read-only on all assets | unchanged | — |
| writing a report sheet / JSON to disk | no | delete the output file; it is derived | regenerable from the same inputs | the caller |
| `anchor_check` regenerating an output | no | writes to a scratch path, never over the recorded artifact | recorded artifact untouched | the caller |
| **extraction to its own repo** (gated, later) | **yes in the property that matters** | re-measure the four banked subjects and record the deltas against the in-repo numbers **before** any new comparison is trusted; the in-repo tools stay in git history either way | comparisons re-anchored, or knowingly un-anchored | the extraction session |
| npm/PyPI publish (only after extraction) | **yes** | `npm deprecate` / PyPI yank-equivalent; publish a fixed patch | bad version visible, marked | the publishing session |
| `gh release create` (only after extraction) | **yes** | `gh release delete <tag>` + `git push --delete origin <tag>` | tag gone, commit remains | the publishing session |
| repo creation (only after extraction) | **yes** | `gh repo delete` same session, or archive | gone or archived | the Director |

**The read-only property is the compensator for the whole measurement surface**, and it is
worth naming as such: an instrument that cannot modify its subject needs no undo.

**Under in-facet placement the bottom four rows do not fire at all** — an in-repo server
publishes nothing, creates no repo and cuts no release. They are listed because extraction
is a live option, and the first row is the one that matters: **a port is a new instrument,
so the compensator is re-anchoring, not a rollback.** Naming it here is how the extraction
session avoids discovering it after the fact.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | instrument identity is the product's central contract — version + config hash on every payload, and `measure_report` refuses to compare across a mismatch. The subject/principle split is pinned by an already-written boundary document rather than decided per call |
| ANDON_AUTHORITY | 2 | tools refuse rather than return a number where the mesh cannot support the question (the solidity refusal); `measure_report` halts a mismatched comparison. Scored 2 rather than 3 because most of this surface is deliberately *diagnostic* — it reports and does not stop a pipeline, which is correct for an instrument. **Remediation: none — the andon belongs to the pipeline that consumes these numbers**, and arming it here would re-create the diagnostic/gate confusion the laws forbid |
| NAMED_COMPENSATORS | 3 | complete above, including the publish-path actions that do not exist yet; the read-only property is named as the compensator it is rather than left implicit |
| DECOMPOSE_BY_SECRETS | 3 | the profile/code split *is* this decomposition, already specified and already tested by four subject classes — subject assumptions change per subject, physics does not, and the boundary document predicted the ship's deltas before the ship ran |
| UNCERTAINTY_GATED_HUMANS | 3 | every metric is labelled diagnostic or gate-eligible; ratios return their numerator and denominator separately so a caller can disagree with our normalisation; the refusal to produce a verdict *is* the human checkpoint, and it is enforced by having no field to put one in |
| EXTERNAL_VERIFIER | 2 | `anchor_check` is the external-verifier pattern for the instrument itself — a recorded output reproduced from recorded parameters, with the residual's shape read and not just its magnitude (a uniform residual is two float kernels; a structural difference concentrates). Scored 2 because the server has no cross-family check on its own numbers. **Remediation: an adoption test that measures two known assets and compares against committed expected values, owner = the first build session** |

## The build bar and the named consumer (E14 Ruling 35)

**Landed mid-session, after this spec's first draft, and it governs.** The Director's
word, 2026-08-08: the four MCP tools are **built and verified properly with tests — the
studio's shipcheck bar, not a prototype bar** — and only then does the polish arc open.

**This tool's first consumer is the polish arc itself**, and it is the best possible one:
every accepted exemplar (W3, the galleon, the dragon, the longsword) gets a polish pass,
which means **the same instrument measures the same four subjects before and after a
change** — the exact comparison this product exists to make, on four classes, on real
work. Instrument identity stops being a claim in a README and becomes the thing the arc
depends on.

Two of the arc's named upgrades land squarely on this surface: the humanoid re-made
photo-real without the style adapter, and the sword's activated state. Both are
before/after comparisons across a register change, which is where a shared instrument
either holds or is exposed.

## Open questions for the Director

**Narrowed by the placement ruling.** The first draft's opening question — alone, or inside
an existing 3D repo — is answered by a third option it did not list: **neither, it stays
here.** `sprite-foundry/3d-prerender/` remains a real alternative home *if* extraction is
ever ruled, and you know that lane's plans better than I do.

What remains:

1. **Which instruments enter the server's surface first.** `tools/diagnostics/` holds ~80
   files; the eight tools in this spec are a curated surface over the subject-independent
   subset. **I selected them from docstrings and the record, not from an exhaustive audit
   of all 80** — the boundary is a judgment call and it is yours to adjust.
2. **Whether the arc-specific diagnostics (`e12_*`, `e14_*`) are in scope at all.** My
   recommendation: **no** — they are per-arc instruments whose numbers sit in closed
   rulings, and generalising them is how a shipped instrument gets edited. The server wraps
   the subject-independent family and leaves the rest where they are.
3. ~~**`ai-eyes-mcp` overlap.**~~ **CLOSED 2026-08-09 by measurement, at the advisor seat
   that handed off.** The spec flagged this rather than asserting it, which was right; the
   check cost one look at a mounted server. `ai-eyes-mcp`'s live tool surface is **seven
   tools, all image-grading**: `image_classify`, `image_compare`, `image_contains`,
   `image_verify`, `image_score_batch`, plus `eyes_selftest` and `eyes_status`. This
   server measures **geometry and texels** — components, curvature, silhouette area,
   non-manifold edges, screen-space extent, off-surface rate, per-texel provenance.
   **Disjoint, and now measured rather than believed.** The one adjacency worth naming is
   `measure_report`, which composes a *sheet* — if that sheet is ever graded rather than
   looked at, `image_compare` is the tool for it and this server should call it, not
   reimplement it.
