# E11 — advisor ruling on the run

**Advisor, 2026-08-05 evening.** Evidence: [E11-report.md](E11-report.md) (Step 0 all
anchors first run; X1/X2 both validate through the lane; X3 enumerated as specced) and
the advisor's own look at the W3 render pair (Ruling 2 below — the looking rule,
seat-independent).

## Ruling 1 — the run is accepted as reported

X-H1 through X-H4 confirmed per the spec's own pre-registered table. The
cross-codebase digit reproduction — the lane's JS palette gate reproducing the staged
manifest's blob digits **1738 / 1495 / 263 px** from freshly emitted renders — is the
external verifier working as designed and is worth its name in the record.
`e11_export_turnaround.py` and `e11_manifest.py` enter the README tool table.

## Ruling 2 — the W3 render generation: the EMIT generation is the standing export and the training input

Grounds, in order of weight:

1. **Reproducible.** X-H1 proved the export a pure function; the recorded
   `renders_flat` are another generator's output that no current invocation
   reproduces. A recipe that does not reproduce its output is not a recipe — the
   dataset carries renders the exporter can regenerate, sha-linked.
2. **Geometry-anchored.** Emit's silhouette is byte-identical to the recorded mask
   (0 px) and the figure count matches `silhouettes.json` to the pixel (146,356).
3. **The difference does not read as content.** The advisor put both view-0 renders
   side by side before ruling: identical paint at every compared element — the
   blade's patched steel, the beard, the pauldron scrollwork, the skirt panels, the
   knee plates. The visible difference is the background level (emit's darker
   constant), with per-pixel rounding accounting for "all 770,048 px differ"; and the
   background is augmentation-side by X3's own conclusion — every render ships with
   its exact silhouette precisely so the lane composites backdrops.

The recorded `renders_flat` stay frozen in the E08 record; nothing is deleted, and
they remain what the E08 arc's sheets were built from. **Director's overrule window,
one look:** `out/renders_flat/final_0.png` beside
`export/turnaround/views/y+000_e+00/asset.png` — a sentence reverses this if the emit
generation does not read as the asset he accepted.

## Ruling 3 — acceptance-block semantics

A Gate-1 verdict covers the **asset** — the mesh and atlas the Director's eye ruled
on. Renders in a dense tree are post-verdict *derivations* of that accepted asset by
the route's own anchored readout. The dense manifests' verbatim reuse of the staged
acceptance blocks is ruled to MEAN that, and the next manifest emission adds a
one-line field saying it explicitly (`renders_are`: post-verdict derivations by the
anchored emit path; the verdict covers the asset). The validated trees are not
churned now for a wording field.

## Ruling 4 — recommendation for the Director's sdlab paste

**The dense manifests, both subjects**: the galleon's 28-camera tree with the native
owner channel (the first asset that has one), and W3's 26-camera tree with owner
honestly absent. Density is the point of E11. The staged 3-render manifests stand as
the validated first form, superseded for training; W3's staged ingest from yesterday
is superseded by the dense ingest — one lane-side paste, the Director's timing.

## Ruling 5 — X3's flat-only conclusion is RATIFIED

Flat renders are what facet honestly exports; lighting variation is
augmentation-side, or a future lit-renderer arm with its own Step-0 anchors if a
ruling ever wants it. That arm is parked, not specced.

## Ruling 6 — the render-space owner/admission channels

They ride undeclared beside the declared channels per Ruling 29's
translate-at-the-boundary pattern. The schema item (per-view `owner_id_*.npy` /
`admission_*.json` as first-class lane concepts) belongs to the lane and is noted for
the sdlab session. Facet takes no action.

## Ruling 7 — the 27 unanchored cameras

The trust chain as reported — X-H1 purity, the byte-anchored beam, the shared code
path, and the lane's independent digit reproduction — is accepted. No additional
anchor is commissioned: a same-session re-render compared to itself would be the
exporter checking its own output, a check that cannot fail.

## Housekeeping ruled into the record

The executor's caution against pushing was honourable and moot in one part: Task 1's
commit (`cd41ee5`) was already public — the advisor's `e719101` push carried it,
because both sessions share one working copy and commits travel with a push while
working trees do not. The remaining two commits (`602640b`, `20f2a0a`) publish with
this ruling's push. The E12 lane discovered live in the same tree (blind predictions
committed before any dragon mesh exists — the discipline holding across three
concurrent sessions) is untouched by this fold.

## Post-ingest addenda (2026-08-06, on the lane session's ingest report)

**Both dense trees are REGISTERED in the lane** — galleon `e04_galleon_dense` 28/28,
W3 `w3_warrior_dense` 26/26, zero rejections, dry-run and live run digit-identical,
receipts in the lane's project tree. **The external verifier reproduced a third
time**: the galleon's blobs measured 1738 / 1495 / 263 px from the dense tree — the
same digits Ruling 1 credits from the staged manifest, now through a third path.

**Ruling 2 gains independent corroboration, measured at ingest:** W3's emit renders
run *cooler* on the lane's palette gate than the recorded generation did — all 26
dense views between 22 and 287 px against the 800 px bound, where the recorded
`renders_flat` measured 266–447 on 2026-08-04. The generation chosen on
reproducibility and geometry grounds is also the quieter one. Confirmation, not a
new ground; recorded because it arrived from an instrument this ruling never
consulted.

**The supersession mechanism is RULED: curate-to-rejected, not delete.** The staged
`w3_warrior` records (8) are curated to `rejected` with the supersession reason
citing this ruling's Ruling 4 — reversible, reason-traced, and the frozen E08 record
untouched. The lane session's hazard finding that forced the decision is banked as a
schema class: **the split engine guesses subject identity from id stems**, and
`w3_warrior` / `w3_warrior_dense` strip to different stems — the same warrior could
have landed in train and test. The mechanism fix (`identity.subject_name` as a
declared field, never a stem guess) is endorsed into the lane's schema-2.x scope
alongside its own proposal (declared render-space roles for `owner_id_*.npy`,
`admission_*.json`, `cam.json`). The lane owns the schema; facet's part is that its
exports are the first content for every one of those sockets — including the owner
channel, which the lane confirmed is carried, hashed, and consumed by nothing
(`lib/` greps zero): the argument for 2.x, exactly as Ruling 6 anticipated.

**⚠ A durability dependency is now load-bearing and is recorded here by name.** The
lane ingests mesh, atlas and all texture-space channels as `materialized: false` —
sha-verified pointers into facet's export trees. **The dataset's hold on those
channels depends on these directories continuing to exist:**
`E:\AI\training\facet_next\E04_stroke\export\turnaround\` and
`E:\AI\training\facet_E08\ARMB\export\turnaround\`. They must not move, and they
belong in any backup that claims to cover the dataset. (This studio has lost
unpushed artifacts to a drive event before; pointers inherit the pointee's
fragility.)

## Standards compliance (this ruling)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every ruling cites the report section or artifact path it rests on; the overrule pair is named by file |
| ANDON_AUTHORITY | 2 | the render-generation question was halted to this seat rather than decided executor-side; the overrule window keeps the Director's halt authority explicit |
| NAMED_COMPENSATORS | 2 | nothing deleted in Ruling 2 (both render generations stand); manifest field deferred to next emission rather than churning validated trees; undo is reverting this commit |
| DECOMPOSE_BY_SECRETS | 3 | export-side rulings stay in facet; the schema item is routed to the lane that owns it; the training-input choice is separated from the historical record's integrity |
| UNCERTAINTY_GATED_HUMANS | 3 | the sdlab paste and its timing stay the Director's; Ruling 2 carries an explicit one-look overrule window with the exact files named |
| EXTERNAL_VERIFIER | 3 | the lane's validator and palette gate (different codebase) verified both trees; the advisor's look was performed on the artifacts, not the report's description of them |
