# E67 — A1 paint prep: unwrap, bake, and the face crop measured on this subject

**Advisor spec, 2026-08-19. One executor seat (Sonnet), background. Tree
`E:\AI\training\facet_E67\`. ZERO CLOUD SPEND — this sitting is local prep only. The first
brush waits on the Director's look at the UV sheet.**

**Direction (the Director, 2026-08-19, paraphrased):** paint is the next stage and it does
not wait on binding; scopes already exist and the ring is accepted. First sitting is local
prep. Two numbers must NOT be inherited: W3's face rect and W3's thin-extent constant.

## Inputs, pinned

| | |
|---|---|
| mesh | `E:\AI\training\facet_E57\mesh\A1_1024_cascade_seed42.glb` (Director-approved, E57) |
| twins | `E:\AI\training\facet_A1_accepted_ring\a1_v0..v7.png` + `MANIFEST.json` (sha256 per file — **verify every hash before use**; a twin that does not match its manifest halts) |
| cameras | the E58 ring's recorded `cam.json` per view — the twins were generated against those controls and the projection must use the same |

## ⚠ TWO NUMBERS THAT MUST BE MEASURED, NOT INHERITED

**1. The face crop.** W3's rect `(360, 240, 700, 600)` on a 1024-frame is **W3's head on
W3's silhouette** and must not be copied. A1's front clay is **752×1024** and the head sits
elsewhere. **The seat measures the crop on `E:\AI\training\facet_E57\renders\clay\clay_0.png`**
— from the geometry, by the same method used for any per-structure quantity here — draws
the measured rect on the clay as a visible overlay in the sheet, and reports how it was
derived. This is the one number the Director declined to invent, and it is the repo's own
law: *a global constant must not govern a local feature*, three instances, each costing a
session.

**2. Thin-extent.** The `0.03` constant is **the greatsword's**. A1 has no weapon — the
canon has no prop surfaces and none may be added. Do not import it. If a thin-structure
threshold is needed at all, derive it from A1's own geometry and say what it is a fraction
of; if nothing needs it this sitting, report that it was not needed rather than carrying a
number forward silently.

## Stages — all local, all free

**0. Provenance (Gate 0).** Verify all eight twin sha256 against the manifest and the GLB
against E57's recorded hash. Any mismatch halts. Report the E57 mesh's face/vertex counts
as read now against E57's recorded 990,679 faces — a drift means the file moved under us.

**1. Weld, then unwrap.** The standing constraint is law here: **weld before decimating,
and no volumetric predicate on an exported mesh.** Enumerate the recorded route's existing
tools first (`project_twins.py`, `texpass_*`, the E06 prep tree at `facet_E06\C1\prep\`)
and reuse what exists — *enumerate the resource before commissioning one*, four instances
in this record. Report chart/island counts and any non-manifold or degenerate geometry the
unwrap encounters. Do not modify geometry to make the unwrap tidier without reporting
exactly what was modified and why.

**2. Bake the projection.** Project the accepted ring through the E58 cameras onto the
unwrapped mesh. Report per-view contribution and the atlas's written/unwritten split.
**State every share in the space it was measured in** (atlas texels vs rendered pixels —
they differ by 5.4× on W3 and the record already paid for confusing them).

**3. The UV sheet — the deliverable.** For the Director: the measured face rect drawn on
clay_0; the UV layout with chart boundaries; the baked atlas; and a render of the baked
mesh beside the accepted twin at the same view, at his zoom. Full-size on disk. **Nothing
in this arc judges whether the bake is good** — his eye gates the first brush.

## Gates

- **Gate 0** — provenance (hashes, counts). Halts.
- **Gate 1** — the face rect is measured on clay_0 and shown; a rect that arrived from any
  other subject halts the arc.
- **Gate 2** — no cloud call is made. This sitting is local; a submission attempt is a halt.

## Out of scope, named

Any generation or cloud call; the first brush (waits on his look); binding/facesets — **the
named debt under paint, explicitly NOT a gate on it** (the only measured need for binding
is E56's wrong-material check); reopening twins for the clay-ridge at v6's chest seam
(named, untested, and not a reason); W3.

## Standards compliance

1. **PIN_PER_STEP — 3.** Mesh, twins and cameras pinned by hash; the two forbidden
   constants named explicitly so an inherited number is a visible violation.
2. **ANDON_AUTHORITY — 2.** Gates 0/1/2 halt; a cloud call is a halt by construction.
3. **NAMED_COMPENSATORS — 2.** Nothing irreversible: zero spend, all outputs in a new
   training tree, repo edits by pathspec.
4. **DECOMPOSE_BY_SECRETS — 2.** Provenance / unwrap / bake / sheet are separable stages
   over on-disk artifacts.
5. **UNCERTAINTY_GATED_HUMANS — 3.** The first brush is gated on his look at the sheet,
   structurally ahead of any paint spend.
6. **EXTERNAL_VERIFIER — 2.** Hashes and geometry counts are deterministic; his eye rules
   the sheet; the seat judges nothing.
