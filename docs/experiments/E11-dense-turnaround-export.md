# E11 — the dense-turnaround exporter: accepted assets become training data

**Spec written before the work.** Advisor, 2026-08-05, the day E10 closed. This is
facet's declared debt to the sdlab asset lane ([Ruling 28](E04-ruling.md)'s queue;
the lane's own receiving-dock findings are the requirements list). The flywheel's
premise: a finished asset re-rendered from N angles is perfectly view-consistent by
construction — the property per-view diffusion lacks (the owner-seam class, ΔE 17.97)
— so every accepted asset should improve the generator that builds the next one.

## The question

**Can facet emit, for any accepted asset, a dense render set the asset lane ingests
without translation loss** — every channel in the declared contract, every number
carrying its provenance — such that the export is a pure function of the accepted
artifacts (byte-reproducible, no generation, no judgment)?

## The contract (the lane's measured requirements, not invented here)

Per accepted asset, the exporter emits:

1. **Dense turnaround renders** — the production camera superset (the profile's
   `cull_unseen.production`, 28 cameras for the ship), flat light (`emit` is the
   renderer: it reaches elevation and its raycast output is the flat readout the
   judging rules require). 30–50 views per the lane's Phase-0 finding; the superset
   plus the eye-eight satisfies the floor.
2. **Exact silhouettes per view** — the raycast masks, byte-stable.
3. **Provenance renders in the E09 indexed discipline** — indexed PNG, PLTE = the
   declared class palette (reference/brush/dilation/background + the layer class when
   present). The current truecolor provenance artifacts are converted **losslessly**:
   the class map must be pixel-identical before and after indexing, proven per file.
4. **`view_owner`** — the native `_owner.npy` sidecar as the channel the lane's
   owner-seam gate consumes (the galleon is the first asset that has it; W3's is
   recorded absent, not synthesized).
5. **Admission/loss masks per render** — reference-share per region and the
   owner-boundary distance field, stored beside samples per the lane's schema (whether
   they gate admission or weight loss is the lane's Phase-0 decision; the export
   carries both).
6. **Conditioning pairs** — every clay render ↔ styled twin pair with its silhouette,
   linked losslessly (the lane holds these as raw material until its ~500–1,000-pair
   threshold; the linkage is what lets the threshold activate retroactively).
7. **The manifest** — `asset-source.json` per the lane's contract, acceptance
   provenance attached (Gate verdict, date, ruling link), suspension translated at the
   boundary per [E04 Ruling 29](E04-ruling.md) (the derived sentinel, canon `null`
   intact), `waterline_z` and the layer channel carried when the asset has them.

## Hypotheses, predictions first

| # | hypothesis | prediction | blind? |
|---|---|---|---|
| X-H1 | the export is a pure function | two runs byte-identical across every emitted file | yes — designed-true; the anchor proves the construction |
| X-H2 | the shared views reproduce the record | the exporter's renders at the Gate-1 sheet cameras are byte-identical to the sheet renders on disk | yes |
| X-H3 | indexed conversion is lossless | class maps pixel-identical through truecolor→PLTE, all files, both assets | yes |
| X-H4 | the lane ingests without edits | `sdlab asset ingest --dry-run`-equivalent validation passes on the emitted manifest with zero schema deviations beyond the recorded sentinel translation | partially — the W3 fixture already validated once; the dense set is new |

## Step 0 — anchors before volume

1. **One-view anchor**: export the beam view of the galleon only; every channel checked
   against the artifacts already in the record (render byte-identical to the sheet's,
   silhouette to Step 0.2's, owner slice to the sidecar). HALT on any digit.
2. **The three-frame discipline**: any world quantity the exporter touches names its
   frame (raw GLB / canonical / unit-cube — the Ruling 2 and Ruling 4 traps; the
   canonical-frame module from the bundle is the preferred consumer once it exists,
   transcription with the frame named until then).
3. **Watchdog standing** for any GPU render leg; report either way.

## Arms

- **X1**: the galleon, full superset — the first complete export, measured against the
  contract item by item.
- **X2**: W3 — the fixture asset re-exported dense (its owner channel honestly absent;
  the lane's schema already handles absence). Proves the exporter is not
  galleon-shaped — the two-subjects-from-birth lesson, applied.
- **X3 (report-only)**: the lighting-variation question. The lane's research flags the
  synthetic domain gap (flat-lit, clean-backdrop training data); `emit` is flat by
  design and the judging rules require flat. **This arm only enumerates what lighting
  variation would require and what it would cost** — a lit renderer is a different
  tool with different provenance; nothing is built. A negative ("flat-only is what
  facet honestly exports; lighting is augmentation-side") is a full success and
  probably the answer.

## Gates

Step 0 anchors (byte-identity, halt on any digit) · X-H3's lossless proof per file ·
the manifest validation · no generation anywhere · the base assets never opened for
writing · suspend rather than invent for anything the lane's schema cannot yet express
(translate at the boundary, annotate, file the schema item to the lane — the Ruling 29
pattern).

## Out of scope

Training runs (the lane's, gated on asset volume) · the ingest itself (the sdlab
session's) · generating new styled content · lighting-variation implementation (X3
enumerates only) · touching either accepted asset.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Byte-identity anchors against recorded artifacts; the export is deterministic by design and X-H1 proves it |
| ANDON_AUTHORITY | 2 | Step 0 halts on any digit; lossless-conversion proof per file; manifest validation is the lane's own gate |
| NAMED_COMPENSATORS | 2 | Read-only over accepted assets; all writes new files; undo is delete the export directory; no spend |
| DECOMPOSE_BY_SECRETS | 3 | The contract IS the boundary: facet exports, the lane ingests; a requirement expressible only by teaching facet about datasets (or the lane about meshes) is a primary finding |
| UNCERTAINTY_GATED_HUMANS | 2 | No Director gate — this is plumbing between two proven systems; the lane's admission remains gated on his Gate verdicts, carried in the manifest |
| EXTERNAL_VERIFIER | 2 | The lane's validator is a different codebase asserting against facet's output — the two-sided check neither side can pass alone |

## The advisor's record, for this spec

The ledger stands at forty-four. The entries that bind here: enumerate before asserting
(the artifacts exported are checked against disk, not described from memory — the
`_owner.npy` lesson), name every frame (Rulings 2/4 of E10), the consumer-grep is part
of any fold, and nothing reaches an eye — the Director's or the lane's — unviewed by
the seat that sends it. When a number disagrees with this spec, trust the number,
report it, and halt for the ruling.
