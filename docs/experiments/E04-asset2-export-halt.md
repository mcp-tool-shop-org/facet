# E04 asset #2 — the galleon into the sdlab asset lane: manifest built, HALT at one field

**Executor session, 2026-08-05.** Task 1 of [Session handoff 3](E04-executor-kickoff.md).
Written after the work. The Director and the advisor decide what it means.

---

## The halt, first

The manifest is built and every proof in the sdlab contract passes **except one field**,
which cannot be filled without inventing a bound this subject's canon fixture suspends on
purpose.

```
VALIDATE: REFUSED
  code    ASSET_MANIFEST_INVALID
  message E:\AI\training\facet_next\E04_stroke\asset-source.json: 1 contract violation(s)
          - nothing was registered.
  - [ASSET_MANIFEST_INVALID] palette.gate.max_offpalette_blob_px:
        required integer >= 0 (the load-bearing blob gate)
```

**The collision, stated from both sides:**

| side | says |
|---|---|
| `canon/E04-galleon-palette.json` | `max_offpalette_blob_px: null`, with `_both_bounds_are_null_ON_PURPOSE` — "This subject has no baseline until its own twins exist. Run with `--report-only` and report numerator and denominator." Ratified in Ruling 8. |
| `style-dataset-lab/lib/asset-source.js:144` | `if (!Number.isInteger(gate.max_offpalette_blob_px) ...) bad(...)` — an integer is required. `max_offpalette_pct` is explicitly allowed to be `null` ("null = withdrawn, diagnostic only"); the blob bound is not. |

The schema has a representation for *withdrawn* on one bound and none on the other. The
fixture needs it on the other one.

**Nothing was invented.** The manifest carries `null`, which is what the fixture says.

## The halt is confined to exactly one field — proven, not assumed

`validateAssetSource` refuses at the **shape** stage *before opening a single referenced
file* ("a manifest whose SHAPE is wrong cannot be trusted to name files safely"), so the
refusal above proves nothing about the other 40-odd declarations. A throwaway copy beside
the real manifest, with that one field filled by E04's own unreachable sentinel and
deleted in a `finally`, ran the full proof chain against real bytes:

```
PROBE: every proof downstream of the refused field PASSES.
  atlas   out/galleon_final.png  4096x4096 rgb
  mesh    out/galleon_final.glb
  texture channels (encoding proven against bytes):
    provenance_atlas   export/provenance_atlas.png   4096x4096 indexed PLTE=4 entries
    view_owner         export/view_owner.npy         dtype |i1 shape [4096,4096]
    styled_mask        state/styled_mask.npy         dtype |b1 shape [4096,4096]
  renders:
    beam_y000_e00  1072x1024 rgb  sil 1072x1024 grayscale  ch [provenance_view, owner_view]  pair [clay]
    deck_y000_e40  1072x1024 rgb  sil 1072x1024 grayscale  ch [provenance_view, owner_view]  pair []
    deck_y180_e40  1072x1024 rgb  sil 1072x1024 grayscale  ch [provenance_view, owner_view]  pair []
```

The sentinel is **not a candidate threshold** and was never written to the shipped
manifest. It exists so the halt can be reported as one field rather than as an unknown
number of them.

## What the refused field would actually gate — measured, both readings

The bound is not decorative: at ingest it **rejects renders**
(`lib/asset-ingest.js:149`). So the question a ruling faces is what number does to a
Director-accepted asset. Measured with facet's own `palette_gate.py`, `--report-only`,
inside the **exact silhouettes**, both readings the fixture requires (its blue band is
SUSPENDED — the 273-301 deg span is a ±10 deg convention over a measured 283-291):

| render | figure px | off-palette px (blue allowed) | % | largest blob | off-palette px (blue excluded) | % | largest blob |
|---|---|---|---|---|---|---|---|
| `beam_y000_e00` | 293,865 | 11,743 | 4.00% | **1,738** | 11,747 | 4.00% | **1,738** |
| `deck_y000_e40` | 295,595 | 10,366 | 3.51% | **1,495** | 10,718 | 3.63% | **1,495** |
| `deck_y180_e40` | 292,066 | 2,588 | 0.89% | **263** | 2,900 | 0.99% | **263** |

Three things fall out, reported and not judged:

1. **W3's 800 px bound would reject two of the three renders of an accepted asset.**
   1,738 and 1,495 against 800; only the 263 admits. The ingest would register one render
   of three and call the other two palette-gate failures. This is the third instance in
   this repo of *a global constant must not govern a local feature*, and the first where
   the constant would travel between subjects through a schema rather than through code.
2. **The suspended blue band barely moves this asset.** Admitting G11's sea-blue changes
   the off-palette count by 4 px on the beam, 352 on one deck view, 312 on the other —
   0.03%, 3.4%, 12.1% of each view's off-palette mass. On the twins the same suspension
   was worth far more. Whatever the blue band's edges eventually are, they are not what
   decides this asset's numbers.
3. **The dominant off-palette mass is warm and sits just below the warm band's 50 deg
   edge** — hue 30-50 deg, median C\* 26-32, median rgb ≈ (88,30,21), 46-54% of the
   off-palette on every view. That is the region the fixture already flagged in
   `⚠_G7_has_no_band`: G7's red gun port lids landed at hue 41-45 and the bands were
   derived from an image where G7 had not landed. Reported separately, as the fixture
   requires, rather than swallowed or condemned.

## Two candidate resolutions, named and NOT chosen

Both are rulings, not executor calls. Recorded so the ruling has the options in front of it.

- **A — the schema gains a null.** `max_offpalette_blob_px: null` becomes legal and means
  the same thing `max_offpalette_pct: null` already means: measure, record, gate nothing.
  Cost: the receiving dock has no blob gate for assets that declare none, which is
  precisely the state E04 shipped under. Touches sdlab, not facet.
- **B — the suspension is encoded as an unreachable sentinel.** E04 already did this once:
  `E04_armT72/palette_blue_allowed.json` carries `max_blob_px: 1000000000`, and the eight
  twins were measured under it. Transcribing that is arguably carrying the suspension
  rather than inventing a bound. Cost: a manifest that *looks* gated and is not, which is
  the shape of defect this repo keeps paying for — a pass-shaped record for a condition
  nobody is checking.

A third option — **derive a bound now** — is the one move that is always wrong here: the
only numbers available to derive from are the results the bound would judge.

## What was built (and what it cost)

`tools/export_asset_source.py`. Writes four paths, all listed; undo is deleting
`E04_stroke/export/` and `E04_stroke/asset-source.json`.

| artifact | what it is |
|---|---|
| `E04_stroke/asset-source.json` | the manifest |
| `export/provenance_atlas.png` | `out/prov_atlas.png` re-encoded truecolor → **indexed, PLTE = the 4 declared classes, no padding** (E09 Amendment 1) |
| `export/view_owner.npy` | the native `_owner.npy`, copied from `E04_armT72/stage1/`, sha256 verified after the copy |
| `export/pair_clay_beam_y000_e00.png` | the beam view's clay pair, copied from `E04_armT72/clay/` |

**The base asset was never opened for writing.** `galleon_final.glb`
(`8b3a6088bf2a…`) and `galleon_final.png` (`65b4c6a3d5fb…`) are sha256'd before any write
and again after every write, **inside the tool**, with no skip flag — E08 Amendment 32's
lesson that a shell chain is a transport, not a guard. Both byte-identical.

**Three checks that could fail, and did not:**

- the indexed re-encode's **PLTE round-trips against the declaration** and its pixels are
  `array_equal` to the truecolor source. The writer is hand-rolled rather than left to an
  encoder, because a library that pads PLTE to 256 entries emits classes nobody declared
  and the contract refuses exactly that. sdlab's independent reader then confirmed
  `PLTE=4 entries`.
- the class palette is **asserted against the atlas's own measured colour set** before the
  conversion, not typed from `e04_replay_owner.py` and trusted — 4 colours found, 4
  declared, `found ⊆ declared`.
- the clay pair is admitted as the beam render's pair only because its silhouette is
  **byte-equal to that camera's raycast hit** (293,865 px, IoU 1.0000). The filename was
  not evidence.

## Findings that are not the halt

**1. The accepted atlas is `galleon_final.png`, not `atlas_final.png`.** The kickoff's
standing block and **E10's W-H3** both name `atlas_final.png` as the base asset. That file
does not exist in the galleon's tree — it is W3's atlas name, from `facet_E08/ARMB/out/`,
carried across from the character line. E10's base-invariance gate hashes a named file; it
must name `E:\AI\training\facet_next\E04_stroke\out\galleon_final.png`, sha256
`65b4c6a3d5fb8df17137fecbb46650b39d67ae0c0a5f092829cebf9e0de5c492`. An inherited claim
wearing a fact's clothes, caught by opening the directory.

**2. `view_owner` is stage-1 ownership, and the manifest says so.** The native sidecar
carries values −1 and 0..7 — the eight stage-1 cameras, −1 where nothing styled. The six
brush strokes committed *after* stage 1 own 213,852 texels between them; those read as
their stage-1 owner here, or −1 where stage 1 never reached them. Per-stroke ownership
lives in the provenance channel's `brush` class and in `out/provenance.json`'s
`per_stroke` counts. The channel is declared `categorical: false` because schema 1.x
refuses categorical npy — the classes are in the note, **not proven by the contract**. The
sdlab kickoff's flag ("`view_owner` becomes an *optional* channel role; the owner-seam
exclusion gate activates only when an asset declares that channel") is now answerable: an
asset declares it. Whether *stage-1* ownership is the ownership that gate wants is the
sdlab session's question, not this one's.

**3. Three renders, not eight.** W3 shipped 8 flat renders + 8 provenance renders. The
galleon has only the three ruled Gate-1 sheet cameras (beam, and the two deck cameras at
+40 deg), because those are the cameras E04 rendered the finished asset at. More views are
one `texpass_iter emit` per camera — the same renderer, raycast, no lighting — but that is
new measured work, not an export, and the dense-turnaround exporter already owns it in
Ruling 28's queue. Reported so nobody reads asset #2's render count as a dataset decision.

**4. One manifest per directory.** `ASSET_MANIFEST_FILENAME` is fixed, so a directory
holds one asset. The manifest sits at `E04_stroke/` — the lowest common ancestor of the
asset, its renders and its exact silhouettes — exactly as W3's sits at `ARMB/`. The two
artifacts that live in `E04_armT72/` are copied in rather than reached for, because
containment refuses a path that escapes the manifest's directory.

## Predictions, with blindness disclosed honestly

| # | prediction | blind? | outcome |
|---|---|---|---|
| P1 | the manifest will refuse on `max_offpalette_blob_px` | **no** — the schema and the fixture were both read before the manifest was written; the collision was predicted from the sources, not discovered by the run | refused there |
| P2 | the refusal is confined to that one field | **yes** — the file proofs had never run against these bytes; the indexed encoder, the npy headers and the silhouette dimension parity were all untested | confined |
| P3 | — | — | the palette-gate numbers, and the W3-800 comparison in particular, were **not** predicted. They were computed after the blobs were measured and are reported as first measurements, not as a test of anything |

## Standards compliance (this task)

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 3 | every class colour, dtype, shape and count written into the manifest is read from the artifact it describes; the exporter is in the repo and re-runnable; the probe is scripted and self-deleting |
| ANDON_AUTHORITY | 3 | the canon-invariance check lives inside the tool that writes, with no skip flag, and hashes before *and* after; the PLTE round-trip and pixel-equality halts fire before the manifest is written; the contract refusal was reported rather than tuned past |
| NAMED_COMPENSATORS | 3 | four written paths, all enumerated; undo is `rm -r E04_stroke/export/ E04_stroke/asset-source.json`; owner: this session. No irreversible or external action — the ingest is a different session's call and was not run, not even `--dry-run` |
| DECOMPOSE_BY_SECRETS | 3 | palette from `canon/`, identity from `canon/`, counts from the run's own `provenance.json`, contract mechanics in the tool. The one thing that could not be sourced this way is the halt |
| UNCERTAINTY_GATED_HUMANS | 3 | the halt goes up with both candidate resolutions, their costs, and the measurement that prices them — and with no choice made |
| EXTERNAL_VERIFIER | 3 | facet did not validate its own manifest: sdlab's `validateAssetSource` read the bytes and refused, and its independent PNG reader confirmed `PLTE=4 entries` against facet's hand-rolled writer |

## What has NOT been done

The ingest. `sdlab asset ingest` belongs to the sdlab session, per the kickoff, and cannot
run until the halt is ruled. No render was registered, no record written, no candidate
copied. Nothing outside `E04_stroke/export/` and `E04_stroke/asset-source.json` was
created by this task.
