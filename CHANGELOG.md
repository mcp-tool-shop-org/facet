# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

**A note on what a version means here.** A version in this file is a claim about
**the state of the record**: which experiments are closed, which assets the Director
has accepted, and what the tools measurably do at that commit. The tag carries it —
there is no manifest to bump. Every entry below points at the ruling that established
it, so a reader can check the claim rather than trust it.

## [Unreleased]

## [0.6.0] — 2026-08-17

**The canon becomes data, and the gate stands in front of the money.** The identity
specification named seventeen elements; the workflow that generated the twins named
sixteen; the profile default a fresh run would use named six. Nothing connected them, so
four arcs spent themselves repairing composition downstream of paint that was wrong at
the source. The canon is now a surface-keyed database and `canon_gate` runs **inside**
`restylize_views` and `texpass_brush`, before the output directory exists.

### Added

- **`tools/canon_gate.py`** (t87, t91) — coverage, occupancy, the author-time prompt
  check, the cross-subject census, and a sidecar verifier. **SURFACE is the row**: an
  element list cannot show what is missing, and a nullable occupant makes a hole a row.
  Joints are first-class between two surfaces, because the missing specification at every
  failed region was the cut and never a fifth garment. Sleeveless is a bare occupant plus
  a forbidden word. Verification writes a sidecar so the canon cannot certify itself.
- **`canon/w3.surfaces.json`**, **`canon/longsword.surfaces.json`** — W3 at
  **24/24 occupancy, 24/24 ratified** by the Director on 2026-08-17.
- **`tools/evidence.py`** (t90) — the diagnostic layer. Seven arcs had each written their
  own sheet builder and three seats wrote a `surfid` decode in a single session. It also
  caught the eighth wrong classifier before it shipped: the atlas four-way is exhaustive
  over *valid*, `unmapped` lives *outside* valid, and treating `~valid` as unmapped is the
  packer gutter — millions of texels, not the 374 that were being looked for.
- **`tools/flat_trace.py`** (t89), **`tools/region_disagreement.py`** (t85),
  **`tools/boundary_repair.py`** (t86), **`tools/unmapped_readout.py`** (t88).

Suite **1182 → 1266** (1212 hermetic).

### Measured, and closed as negative

- **The flat coloured patches are not a fill artifact.** Orphan fill measures *below* its
  own base rate at them (0.27x), and the identical defect is present in a render built
  from an atlas that predates the repair blamed for it.
- **There is no geometry to snap a material boundary to** — one PBR material, 13,715 atlas
  islands against sixteen named materials, a palette blind to gold-against-leather. 354
  texels of 2.4 million.
- **The magenta is cosmetic** — 0.22% of the figure; a 46x atlas-side cut moved the
  on-screen count by six pixels.
- **The flats trace to a plate nobody had checked.** The render view's twin is clean; a
  different view owns 97 of 115 defect pixels at facing 0.68 against 0.60. The patch is a
  scatter artifact and the colour is a real cross-view disagreement on an already-named
  surface — so a twin regeneration is **not** justified by "the defect is in the twins".

### Corrected in place

- **Two of three Blender citations in CLAUDE.md were wrong**, resolved one call each at
  `/api/v1/`: #162226 is open rather than merged, and #119393 is a single defect rather
  than a catalogue. Load-bearing, because the merged fix cannot reach a UV in a gutter.
- **"The generation prompt names six elements"** welded two files into one false sentence.
  The workflow that made the twins named **sixteen of seventeen**; the six is the profile
  default, which is left broken on purpose as the specimen.
- **Four readings of the reference by the advisor were wrong** and the Director caught
  each: bare hands, asymmetric armour, a knee-plate fur trim, and N11 as mis-specified.
  All four came from treating a straight-on projection as a description while the back
  reference sat unopened. **Amendment 15 is undisturbed.**

### Known

The gate checks that the subject prompt contains the ratified canon phrases. It does not
check paraphrases, per-view stems, unratified drafts, subjects with no surfaces file, or
whether a named material landed on the right surface. Four subjects have an IDENTITY.md
and no surfaces JSON; those are left undone rather than generated without walking the
reference.

## [0.5.0] — 2026-08-16

**The plates compose, and the projector question closes.** One session ran five arcs
([E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md)),
two dispatched executor seats and three runner seats, and six build rounds through an
outside channel whose nominated calibration claims held **ten for ten** — every one
verified here by running it before anything trusted it. The rebuilt-atlas renders
cleared the Director's acceptance bar for the first time on this route — twice, across
two arcs — beside a shipped atlas whose route had been destroying paint the eight plates
agree on.

### Added

- **The S3 chain, seven tools** — `emit_view_aovs.py` (per-view G-buffers of the
  shipped state, anchored by pixel-exact reproduction of the recorded silhouettes,
  16/16 cameras at 0 px), `s3_composite.py` (the existence-proof compositor:
  view-dependent and view-independent stills, disagreement diagnostics, a flow hook),
  `flow_estimate.py` (dense LK with sparse per-component confidence and the aperture
  problem handled rather than hallucinated), `s3_run.py` (the bundle runner, flow A/B
  built in), `s3_sheet.py` + regions (native-pixel acceptance sheets with provenance
  as a panel), `atlas_from_aovs.py` (texel-driven atlas rebuild, owner/blend ×
  flow off/on), `twin_mesh_warp.py` (the per-tile correspondence instrument, validated
  on constructed truth before any real measurement). Tests t77–t84; the suite grew
  **1098 → 1182** (1135 hermetic) with the thirteen T34 count surfaces moved in the
  same commits.
- **The warp is measured** ([E45 report](docs/experiments/E45-warp-and-aov-report.md)):
  interior tile offsets exceed silhouette offsets on **8 of 8 views** (medians
  3.46–11.12 px vs 1.16–3.00), wrong-pairing controls separate 12.5×, and the twin
  ring is **eight flat cameras** — the el-55 pair are brush cameras, and no twin
  exists at elevation.
- **Flow-corrected compositing reduces cross-view disagreement on 18 of 18 measured
  rows** ([E46 report](docs/experiments/E46-s3-run-report.md)) — directionally
  uniform, magnitude a trim (1.4–3.2 px median at 16–27% coverage), the lever was the
  projection policy itself.

### Changed

- **`callieri_border.py` 1.0.0 → 1.0.1** — the inf−inf RuntimeWarnings at :209/:214
  silenced by masked subtraction, proven byte-identical across all four public
  surfaces on an inf-background fixture **and** a real frame, with the warning
  provocation demonstrated against the old form and the T76 pin untouched (t84).
- **`docs/index/conventions.json` `paid_for_by`** marched E4[0-4] → E4[0-9] as five
  arcs landed — the t24 andon fired three times in one day, each firing a designed
  leg doing its job, and the standing order it earned is written into the record: the
  arc bound and the instrument census re-run are the **last** corpus-touching steps
  of every fold.

### Known, named, and staged

- The fill-pass **polygon class** (the Director's one open ruling on the
  accepted-grade sheets), **never-seen surface** (4.65–5.57% of valid texels,
  needs a policy), and the **canon build-out** he named as the crux — all carried
  with their evidence in the [E49 dispatch record](docs/experiments/E49-finish-and-cap-kickoff.md)
  and on the front page.

## [0.4.0] — 2026-08-09

**The measurement server ships.** Four releases put a record index in the wheel and left
the eight measurement tools behind — invisible because this repo *is* the checkout, so the
tool worked where it was built and had never been anywhere else. `pip install
facet-mcp[measure]` now runs a measurement from a clean venv, and the four tools that need
a dependency PyPI cannot deliver refuse with the reason instead of looking broken. Three
arcs close with it: [E29](docs/experiments/E29-ruling.md) (the clay hop measured, both
paths kept at the Director's ruling), [E30](docs/experiments/E30-ruling.md) (the polish
arc's anchors, and the halt that caught a route tool changed under an accepted asset), and
[E31](docs/experiments/E31-ruling.md) (this).

### Added

- **T34 gained a fourth leg, pinning the EXPERIMENT count**
  ([E28](docs/experiments/E28-instrument-census-kickoff.md) task 0). Legs 0–3 pin the
  test count; this one pins a second live-moving quantity on the same front door,
  against the status table in `docs/experiments/README.md` rather than a constant. It
  fired on **two real stale sites** on the tree it was written against —
  `site/src/site-config.ts` read *"Twenty"* and `docs/advisor-kickoff.md` read *27*,
  against a status table holding **28 rows** — which is the E26 gate-2 can-fail proof
  discharged on a live tree rather than a synthetic one. Its notation boundary is
  declared and itself under a test: digits and English cardinals 0–99 are read, other
  languages' number words are **declined rather than mis-read**, and the seven generated
  translations are outside it for the reason leg 3 already carries.

- **`tools/instrument_census.py` — the census of `tools/diagnostics/`, measured rather
  than curated** ([E28](docs/experiments/E28-instrument-census-kickoff.md) task 1, at the
  Director's ruling on [the spec](docs/specs/measurement-mcp-spec.md)'s open question 1).
  Six mechanical axes plus one labelled judgment over all **99** files — the spec estimated
  its own denominator at "~80". Outputs `docs/instrument-census.md` and
  `docs/instrument-census.json` so the next arc diffs rather than re-reads; the population
  is under a test (T41). **The headline measurement: 93 of 99 carry a flag surface and only
  6 have a `__main__` guard** — the directory's house style is a straight-line module-level
  script, which is why axis F declines to probe 88 of them rather than executing arc
  scripts against recorded trees. Axis G is a **proposal**, not a boundary: that is the
  advisor's to rule and the Director's to adjust.

  ⚑ **Axis D excludes the documents that describe the census, and a fired gate is why.**
  The census's own output tabulates all 99 filenames and its report names the files it
  found, so both sit inside the corpus the axis reads — leaving them in makes every file
  "cited" (**76 → 99**). `test_t41_axis_d_is_idempotent_across_runs` fired on a closing
  suite run and caught it; the headline is unmoved at 76 and the contaminated read rides
  beside it as `cited_raw`. **Four self-references were found in one arc, three of them by
  a check that fired rather than by reading.**

- **The measurement server serves all eight of the spec's tools**
  ([E28](docs/experiments/E28-instrument-census-kickoff.md) tasks 2a/2b/2c, after the
  census halt was ruled). The `e14_topology` tie crash is repaired under a discharged
  proof — a guard dead on every input the old code returned on, shown identical by a
  10,000-triple randomized sweep, a two-way-tie sweep, tool-conformance runs, and a
  byte-level comparison of both trees on all seventeen recorded subjects (stdout and JSON
  byte-identical, seventeen of seventeen). Three wraps land with anchors reproducing
  recorded digits at the served surface — E14's longsword topology, E12's dragon curve and
  its off-surface row — and the eighth tool, `anchor_compare`, is **compare-only by
  Ruling 10's honesty decomposition**: the tool compares, the caller replays. Its fixture
  is the pair this repo owed itself twice — a pixel-identical, byte-different PNG pair —
  and the false-halt class that produced two live halts now separates in one payload.
  `facet-measure` 0.1.0 → 0.3.0 across the two surface moves; `NOT_WRAPPED` has no live
  site.

- **⚑ THE MEASUREMENT SERVER SHIPS.** `pip install facet-mcp[measure]` now installs
  `facet-measure` and the instruments it invokes, and runs a measurement from a clean venv
  with no checkout anywhere near it ([E31](docs/experiments/E31-ruling.md) Ruling 6, at the
  Director's word). Verified the way [E24](docs/experiments/E24-ruling.md) taught — by
  running a **verb**, never `--help`: `mesh_stats` on a control mesh returns 786,432 faces
  with a full identity envelope whose instrument sha256 matches the one this rig produces.

  **Two extras.** `[measure]` is the tier that resolves on **every** Python this package
  claims — `mesh_stats`, `mesh_topology`, `measure_report`, `anchor_check`, which includes
  **both anchor tools**. `[measure-full]` adds the four geometry instruments, and what it
  delivers depends on the interpreter: **all eight on 3.11/3.12**, four on 3.13, because
  `open3d` 0.19.0 is the latest *release* and publishes cp38–cp312 wheels with **no
  sdist**. The requirement carries **`python_version < "3.13"`** so the install succeeds
  there without it and the four refuse with exit 4, rather than the whole install dying on
  a resolver error.

  ⚑ **Corrected before release, at the Director's question.** The first cut of this shipped
  **no** full extra at all, on the reading that one *"cannot be declared"*. That conflated
  two things: the only open3d that exists **for 3.13** is a direct-URL devel wheel and
  genuinely cannot be declared — but open3d itself is an ordinary PyPI package on
  cp38–cp312, and E31 measured the full tier at **0 of 8 failing** on py3.12. What fails on
  3.13 is *resolution*, not *declaration*. **All eight on 3.13 is one documented command**,
  because Open3D publishes current cp313 wheels on a rolling devel channel and a direct URL
  is legal on a command line — see the README. *This route's own open3d-dependent numbers
  were measured against that devel build.*

  ⚠ **`facet-measure`'s version stays independent of this package's.** It versions a
  payload surface, not a distribution; the two numbers coinciding at 0.4.0 is a
  coincidence and they are not locked.

- **The polish arc's entry gates** ([E30](docs/experiments/E30-ruling.md)) — eight per-profile
  anchors as permanent tests (T50–T57), three at the **byte** tier and the rest at the value
  tier, no sha256 literal in any of them. ⛔ **The halt is the most valuable thing the arc
  produced:** W3's projection no longer reproduces — styled **1,718,750** against a recorded
  **1,653,659** — because `project_twins`' erosion was rebuilt. *A route tool changed under
  an accepted asset and nothing noticed until an anchor was built for it*, which is exactly
  the condition the Director's clause exists to detect, found on its first outing.

- **The clay hop measured against the concept it came from** ([E29](docs/experiments/E29-ruling.md)).
  One arm, one variable: the clay mesh returns **9 shells against 82** and **1,461
  non-manifold edges against 4,201** — 73× and 152× a run-noise floor the arc had to measure
  first. ⚖ **The Director ruled both paths KEPT**: *"they both are great… keep them both as
  options."* Stage 0 is a per-subject choice, not a replacement.

- **A reconstruction noise floor, which nothing in this record had** (E29 Ruling 5). Three
  runs of one input at one seed are **bit-identical through `pipe.run()`, hole-filling and
  remeshing** and diverge inside decimation: faces **±0.27%**, shells **±1**, non-manifold
  edges **±18**. Every prior single-run mesh comparison here therefore carries an
  *unmeasured* floor — which overturns nothing, and does mean re-litigating one requires
  measuring its floor rather than asserting it was small.

### Changed

- **The hollow finding's reach is NARROWED, and the character class is ruled UNMEASURED**
  ([E29](docs/experiments/E29-ruling.md) Ruling 4). [E14 Ruling 3](docs/experiments/E14-ruling.md)
  reads *"every reconstruction this route has made is a hollow double-walled shell"*; read
  verbatim, its evidence base is three longswords, a dragon and a galleon — **prop, beast and
  vehicle, no character** — and the character is this route's founding class. `mesh_topology`'s
  nested-wall leg **declines to compute** on all five character meshes tested, including two
  recorded ones. ⚠ **That is not a finding that characters are solid**: an inner wall shredded
  into sub-1% pieces produces the same signature while still being hollow. The finding stands
  unchanged for the classes it was measured on; E14's closed text is untouched and the
  narrowing lands in `CLAUDE.md`, where the standing constraint lives. Every consumer-facing
  clause is unaffected — a volumetric predicate still meets a shell.

- **A recorded inference about which attention backend ran is corrected in place**
  (E29 Ruling 3). [E04's Gate 0 report](docs/experiments/E04-gate0-report.md) concluded
  *"what ran is what the log says"* from a `[SPARSE] … Attention backend: flash_attn` line,
  and E12 carried it forward. Measured: that banner printed on **all six runs of a session in
  which `flash_attn` is not installed, cannot be imported, and which ran to completion.** It
  is a **declared preference emitted at import, not a record of execution.** Kept with its
  correction beside it rather than deleted. And `ATTN_BACKEND=sdpa` **alone** reconstructs —
  `SPARSE_ATTN_BACKEND` is inert on this route while riding in every recorded invocation.

### Fixed

- **The experiment count on two public surfaces**, corrected in place with the
  measurement that overturned it — **28 status-table rows**, agreeing with what
  `record_health` reports. Third instance of this drift in 24 hours, second inside a fix —
  [E27's ruling](docs/experiments/E27-ruling.md) corrected the front door to
  *"twenty-six"* and undercounted by one while doing it.

- **`pip install facet-mcp` gave a record server and NO measurement server, and nothing
  had ever noticed** ([E31](docs/experiments/E31-ruling.md), Rulings 1–6). The wheel held
  **two `.py` files**; the eight served tools invoke instruments as *subprocesses*, so an
  install had nothing to invoke. Six tiers were measured, each an actual wheel in its own
  clean venv with every tool called through the server's own dispatch: today's wheel
  **8 of 8 failing**, and with the instruments and the light dependency tier, **0 of 8**.
  The wheel goes **58,401 B / 2 entries → 509,413 B / 118**. Invisible for four releases
  because this repo *is* the checkout — the tool worked where it was built and had never
  been anywhere else.

- **`measure_mcp`'s resolver, which was [E24](docs/experiments/E24-ruling.md)'s defect
  verbatim in a file written after E24 fixed it elsewhere** — `REPO = dirname(HERE)`,
  which in a wheel resolves to `<venv>/Lib`. The repair is the distinction E24 never drew:
  **`REPO` answers *where is the corpus*** (the two-marker property test, returning `None`
  rather than guessing) and **`tool_path` answers *where is the instrument*** (resolved
  beside the module — one expression correct in a checkout and an install, because record
  markers key on a corpus that cannot ship while instruments are code that does). The
  identity envelope now hashes through `tool_path` too: two path expressions for one file
  is how a payload comes to certify an instrument that did not run.

- **A missing dependency reported as a runtime failure**, which made a four-of-eight
  install look like a broken tool. `MISSING_DEPENDENCY` is now **exit 4 REFUSED** — the
  environment failing to answer is the tool working and telling you not to proceed — and
  the refusal names the instrument, the module and what to install. Every part of that
  sentence was already at the call site and nothing composed it.

- **The measurement server was reachable by no session at all.** `.mcp.json` declared one
  server; `tools/measure_mcp.py` was in neither it nor the workspace config
  ([E29](docs/experiments/E29-ruling.md) Ruling 7). Registered **with a test** rather than
  a line: T58 starts the declared arguments as a subprocess, speaks stdio, and asserts the
  payload's instrument sha256 equals the file on disk.

## [0.3.1] — 2026-08-09

**The install that could not find the record.** Every released version through v0.3.0
shipped a wheel whose `facet-index` and `facet-mcp` could not locate the corpus they
exist to serve. The patch is that fix, plus the arc that closed the deletable-gate
class and the arc that put the front door's own counts under a test.

### Fixed

- **`pip install facet-mcp` resolves the record's root by TESTING FOR IT**
  ([E24](docs/experiments/E24-ruling.md)). The wheel installs `facet_index` as a
  top-level module, so up to and including v0.3.0 the root was resolved against
  `<venv>/Lib` — which holds neither corpus nor index — and `build`, `claims`, and `q`
  without `--db` all failed. The root is now found by testing candidates for the
  record's own markers; from inside a checkout both commands find it, and from anywhere
  else they exit **`4` REFUSED**, naming both directories tried and both markers looked
  for. Measured on a wheel built from `main` into a clean venv.

  **How four green releases shipped it:** every check exercised `--help`, which needs no
  record. `release.yml`'s wheel step said *verify the wheel runs from a clean venv* and
  ran the one surface that could not fail. It now runs a **verb**.

- **`$FACET_INDEX_DB` is read by both commands**, and it selects which *index* — never
  which *corpus*.

- **CI was skipping the artifacts tier rather than running it** ([E24 Ruling 3](docs/experiments/E24-ruling.md)) —
  the defect's own shape, in the tier that would have caught it.

### Changed

- **The deletable-gate class closes.** [E25](docs/experiments/E25-ruling.md) converted
  the last **133** ANDON sites across **43** files — the measurement instruments — from
  `assert` to `raise`, after [E22](docs/experiments/E22-gates-report.md)'s 88 and
  [E23](docs/experiments/E23-route-gates-report.md)'s 57 in v0.3.0. **278 converted in
  total.** Exactly **one** bare ANDON `assert` remains anywhere under `tools/`:
  `superseded/texpass_thin_mask.py`, which is permanently out of scope because those
  tools are kept so anyone can run them and watch them fail the same way.

  These 133 are **not** in the published wheel — it ships `facet_index` and
  `record_mcp` only — so this is an internal change, and the patch bump is not
  concealing a published behaviour change.

- **28 ANDONs that already `raise SystemExit`** across 12 files are unchanged and
  pinned. `SystemExit` is not deletable by `-O`, so none of them carried the defect,
  and normalising a type nobody ruled is not a pure move.

### Added

- **The front door's counts are under a test** ([E26](docs/experiments/E26-ruling.md)).
  `T34` collects both tiers live and fails CI on any watched surface stating a stale
  one. It caught a real drift on its first run that no coordination rule had seen. The
  matcher is **phrase-shaped, not proximity-shaped** — a ±90-character window returned
  45 hits of which six were not test counts at all — and the translations are covered by
  a digits leg instead, a declared boundary rather than an oversight.

- **`T28`, `T31`, `T33`, `T34`.** The remaining-gate count and the surviving
  `superseded/` site are pinned **by name**, so a future sweep cannot tidy either away
  without editing the test on purpose.

  *No suite total is quoted here on purpose.* It is a live-moving number, and a released
  CHANGELOG entry is one of the two regions `T34` deliberately does not sweep — so a
  total written here would be the one kind of count nothing can catch when it goes stale.
  `pytest --collect-only` at the tag is the answer, and it is step 1 of the release
  sequence for exactly this reason.

## [0.3.0] — 2026-08-08

**The gates stop being deletable.** Two arcs, one theme: `assert` is a statement the
interpreter is licensed to remove, and this repo had been using it for checks that decide
whether an irreversible step proceeds. **145 of them now `raise`** — [E22](docs/experiments/E22-gates-report.md)'s
88 in the write-head, the index and the published server, and [E23](docs/experiments/E23-route-gates-report.md)'s
57 in the route tools that produced four accepted assets. A minor bump because a
published command's exit surface changes: a fired gate and a failing `verify` leg both
leave as **`4 = REFUSED`**.

**A gate is never a bare `assert`.** [E22](docs/experiments/E22-gates-report.md)
converted the **88 ruled ANDON gate sites** in five write-path tools plus the two
published console scripts from `assert` to `raise AssertionError`, because `assert`
is a statement the interpreter is licensed to delete: `python -O` and
`PYTHONOPTIMIZE=1` removed them silently and execution continued past them. Measured
before the repair, on the pinned interpreter: the gate never spoke, the write
proceeded, the process exited `0`. That is strictly worse than the shell chain
[E08 Amendment 32] was written for — the chain at least let the ANDON print.

Every conversion is a **pure move**, and that is proved rather than asserted: the AST
of each of the seven files is identical to the negation rule applied to the same file
at the prior commit, over the whole module, and their comment tokens are unchanged.
The three named anchors reproduce — T7's byte-identical atlas replay (its sidecar json
too), the twin-projection anchor, and T26's three fired ANDONs. **No conversion was
reverted.**

**Exit code `4 = REFUSED` lands**, carrying [E21 Ruling 4]: a failing `verify` leg and
a fired ANDON both leave it, off the `1` they shared with a mistyped flag. `verify`'s
value is also the certificate's `verify_exit_code`, and `record_mcp.parse_verify` keys
on `rc != 0` rather than `rc == 1` — verified before the value moved — so the health
state machine is indifferent to which non-zero it is. The test fixture that carried
this as a hardcoded `1` now reads the tool's own constant.

**T30 rides the commit** — 27 cases, 14 functions — asserting that each converted gate
refuses under a normal interpreter **and** under `-O` **and** under
`PYTHONOPTIMIZE=1`, that the write-path gates leave nothing behind when they fire, and
that the `-O` legs are not vacuous (proved on a throwaway script, never on a facet
gate). **No test asserts that `PYTHONOPTIMIZE=1` disables a gate**; that would anchor
the defect. Suite 248 → 275.

**What this does NOT do, measured and reported rather than implied:** E22 converted
the 88 sites its scope ruled. A census taken at the same time found **278 of the 294
asserts in `tools/` carry the ANDON token**, not the 87 the dispatch inherited — so
**191 ANDON-carrying gates across 56 files are still bare asserts**, and **175 of them
sit before a write in their own scope**. Those are a finding for the advisor, not a
scope extension taken by an executor.

*⚑ This line read "192 … outside the five named tools" and was corrected at
[E22 Ruling 4](docs/experiments/E22-ruling.md). 192 counts `facet_index.py:343`, which
was in scope and was converted; the count of gates that are **still asserts** is 191
across 56 files (278 − 87). The slip is the same shape as the one this arc caught in
its own dispatch — a subtotal read as a total — and it landed in the number that scopes
the next arc.*

*⚑ **The 191 is now 134**, by [E23](docs/experiments/E23-route-gates-report.md) below.
E22's statement was accurate when written and is left standing.*

**The route's 57 gates follow, on twelve files no test had ever executed.**
[E23](docs/experiments/E23-route-gates-report.md) converted the **57 ANDON gate sites
in the twelve `tools/` top-level scripts** that produced the four accepted assets —
[E22 Ruling 4](docs/experiments/E22-ruling.md)'s route split — leaving **134** ANDON
asserts elsewhere (132 in `diagnostics/`, 1 in `verify/`, and `superseded/`'s one,
which is **never** converted because those tools are kept so they fail the same way).
The enumeration was re-measured before the work rather than inherited, and every
per-file cell of the dispatch's table reproduced.

**Pure move again, and this time the AST proof carried the whole load.** E22 had T7's
byte-identity replay and T26's fired ANDONs underneath it; **zero of these twelve files
were reached by any test**, so the only verifier was whole-file AST equality against
the negation rule applied at the prior commit — **12 of 12 identical, 0 comment tokens
changed, 57/57 per-site, no file reverted.**

**T31 rides the commit — 95 cases, 8 functions.** All twelve still compile; the ten
non-Blender tools reach argparse and write nothing under a normal interpreter, `-O` and
`PYTHONOPTIMIZE=1`; no ANDON gate in the twelve is an `assert`, by AST, with a can-fail
leg; and the **sixteen gates reachable on synthetic input refuse in all three modes**,
each matched against its own message rather than on a bare non-zero exit. The two
Blender scripts (`bake_hero_prep`, `bake_hero_pack`, 19 sites) get compile and AST only
— they `import bpy`, and that reason is itself asserted rather than left as prose.
Suite 275 → 370.

**Reported, not acted on:** `brush_cloud_step:204` cannot fire — `:353` tests the same
precondition harder and stands in front of it on the only path that calls `preflight`,
measured across every block shape. `silhouette_masks` and `restylize_views` create
their empty output directory *before* their gate fires. `bake_hero_prep` already
carried one ANDON that raised, which reconciles E22 Ruling 5's repo-wide
`AssertionError 88` as 87 conversions plus that site. And three of the twelve carry
`SystemExit` ANDONs alongside `AssertionError` ones (`brush_cloud_step` 4,
`e13_harmonize` 3, `restylize_views` 3) — [E22 Ruling 5](docs/experiments/E22-ruling.md)
ruled those stay, so the collision is recorded and not resolved.

**CI now installs `opencv-python-headless`, and the reason is the arc's own premise.**
The first push went red: `tools/restylize_views.py` imports `cv2` at module level, CI's
pinned test install had never carried it, and **no test in this repo's history had ever
invoked one of these twelve tools** — so the gap could not surface until T31 existed.
Module-level imports were measured across all twelve before repairing (`cv2` is the only
real gap; `mathutils` belongs to the Blender pair nothing here runs), and `cv2` joins
`REQUIRED_CHILD_MODULES` so a missing module refuses loudly instead of producing the
partial-green misreading E17 Ruling 2 closed. **This is a test-install pin only —
`pyproject.toml` is untouched and the published package still depends on `mcp>=2.0.0`
alone.** [E23 Ruling 2](docs/experiments/E23-ruling.md) ratified repairing rather than
narrowing a test, and drew the boundary: a gate measuring the *result* halts, a gate
measuring the environment's ability to *run* the measurement may be repaired when the
repair adds capability rather than removing coverage.

## [0.2.0] — 2026-08-08

**The operator contract of the two installed commands.** A behaviour change to a
published CLI, so it takes a minor bump. Scope was ruled to what facet actually
installs — `facet-index` and `facet-mcp` — and no other tool in `tools/` is touched.
The full evidence is [E21](docs/experiments/E21-cli-contract-report.md).

### Changed

- **Exit codes now mean what `SHIP_GATE.md` says they mean.** Measured before the
  change, through a subprocess, on twenty rows across both commands: a user error
  exited **2** (argparse's convention) and a runtime error exited **1** (CPython's
  default for an uncaught traceback). **The surface was inverted at both ends, not
  one** — the gate line had named only the argparse half. Now: `0` ok, `1` user
  error, `2` runtime error.
- **`3` is declared and deliberately unused.** No verb of either command has a
  partial-completion path. `verify` reporting three passing legs and one failing one
  has *completed*, and reports a measured outcome. A code is not populated by
  inventing a path for it to describe.

### Added

- **No raw traceback reaches an operator without `--debug`.** An unexpected exception
  now leaves as a structured failure naming its cause and the next step; `--debug`
  restores the traceback and changes nothing else. Proven rather than asserted: same
  exit code with and without, and the artifact a `build` writes is byte-identical
  across the pair.
- **`--debug` is confined by test, not by intention.** E08 Amendment 32 rules that a
  gate carries no skip flag, so the new flag is checked against that: an AST walk
  pins that the identifier is read only in the two functions that decide what gets
  *printed* after a failure has already been decided, and a fired gate still refuses
  with `--debug` set. T21's closed flag allowlist — the guard that exists to make a
  new flag expensive — widened by exactly one, in writing, with the condition
  attached.
- **T29, 30 tests**, every code asserted through a subprocess (a console script's
  exit status is a property of a *process*; `main()` returning 2 is a different
  claim), and every code paired with a can-fail leg that must produce a *different*
  number.

### Unchanged, and unchanged on purpose

Two outcome classes keep the codes they had, because what they *deserve* is a
ruling and not an executor's pick: **a failing `verify` leg** (its return value is
also the `verify_exit_code` field of the schema-versioned certificate that
`record_health` serves — moving it moves a persisted artifact, not just a shell's
`$?`) and **a fired ANDON**. Both are reported for the advisor with their options and
consequences. `claims` stays `0` whatever it finds, which was already ruled at
E15 Ruling 9b.

### Not done, and named rather than quietly dropped

**Logging levels are not shipped.** The dispatch reserved the silent/normal/verbose
boundary for the advisor to rule *before* it ships, and the census that ruling needs
is now measured: of `verify`'s 35 print sites, **zero are progress chatter** — they
are separators, leg headers, measurements and verdicts — and `record_mcp` parses
`verify`'s stdout to build the certificate, so a quiet `verify` would break it. That
is not a philosophical objection to suppressing output; it is a live dependency.

## [0.1.1] — 2026-08-08

**Fixes a defect that only exists in the artifact a user receives.**

`0.1.0`'s binary told operators the wrong thing about their own machine. Inside a
PyInstaller onefile, `__file__` lives in a temp extraction directory, so the server
resolved its default index against that — printing
`db: C:\Users\…\Temp\docs/index/facet.db`, a path that cannot exist — and every
refusal hint said *"run `python tools/facet_index.py build`"*, a command with no
`tools/` directory to run it in and possibly no Python at all.

- **The index default now resolves against the working directory when frozen**, which
  is the honest default: an operator runs `facet` from inside the checkout whose
  record they want served. An explicit `--db` or `$FACET_INDEX_DB` still wins.
- **The refusal hint follows the runtime** — `facet-index build --db <path>` (or the
  env var) in a binary, the source command in a checkout. Every refusal in this repo
  names the next step; the next step has to be one the reader can actually take.

**How it was found, because that is the transferable part.** Not by CI, which was
green; not by the wheel test, which passed; not by the console scripts, which ran.
Every one of those exercises the *source checkout*, where `REPO` is the repo and the
advice is correct. It was found by installing the published package and reading what
it printed. **A green pipeline verifies the thing it built, not the thing a user
receives** — T28 now exercises the frozen branch directly rather than trusting that a
source-tree run implies a binary run.

Also corrected, twice, and the second correction is the useful one: `npx
@mcptoolshop/facet` was reported as broken on Windows, then explained away as registry
propagation. **Both were wrong.** `npx` works from any ordinary directory, on both
versions, exit 0.

It fails in exactly one place — **inside facet's own checkout** — because the repo root
now declares `"bin": {"facet": …}` for the wrapper it publishes. npm resolves the
command against the local project first, that project has no `node_modules`, and the
shell reports `'facet' is not recognized`. A self-reference artifact of testing a
published package from inside the repo that publishes it. No user encounters it.

**The diagnosis took three attempts because the comparison was invalid.** The runs that
worked were from a temp directory and the runs that failed were from the checkout — the
version changed *and* the working directory changed, and the result was read as
version-specific. This repo's own law, committed again: *"one variable" is a property of
the dependency graph, not of the parameter you edited.* The Director found it with a
one-word question after two confident wrong explanations.

**218 tests, 218 passing** — 210 hermetic + 8 artifacts, counted at this commit. The
five new ones are T28, and they exercise the frozen branch directly rather than
inferring it from a source-tree run. *(The v0.1.0 entry below keeps 213/205 — that is
what that release actually shipped, and a blanket count update very nearly rewrote it.
A released version's record states what it was, not what came after.)*

## [0.1.0] — 2026-08-08

Cut at the close of the E19 treatment, at the Director's word. There is no manifest to
bump, so this version exists as a git tag and this heading and nothing else.

**Why 0.1.0 and not 1.0.0.** The Director set the number. It is the honest one: the
extraction gate is open, three testability seams are dispatched and untaken, and the
repo's own highest-value question (P5 — `fit_background` at frame-edge figures) has
never been looked at. A 1.0.0 would assert a stability this route has not earned yet.
What the four accepted assets earn is a *first* release, not a stable one.

### ⚑ Corrected 2026-08-08 at the v0.2.0 seat — these three entries were filed under `[Unreleased]`

They shipped here, in this release, and sat under `[Unreleased]` through **two tags**
before anyone read the section against the tag below it. **The measurement:**
`git show v0.1.0:CHANGELOG.md` puts the `[Unreleased]` heading at line 14 and
`[0.1.0]` at line 40 — so the block was already misfiled *at the moment the tag was
cut*, and this entry's own opening line says the release was "cut at the close of the
E19 treatment," which is exactly the work the block describes. Moved rather than
rewritten; nothing in the wording below is changed. They are restored here because a
released version states what it shipped, and this one was understating itself while a
front-door document told readers a live landing page was unreleased.

- **Presentation surface** (E19 treatment): a landing page, a six-page Starlight
  handbook rendered from the canonical `docs/handbook/`, the clay wordmark logo,
  `SECURITY.md` with a measured threat model, `SHIP_GATE.md`, `SCORECARD.md`, and
  this file.
- **A repo-knowledge entry** — thesis, architecture, conventions, environment traps,
  drift risks and three mapped relationships.
- **The README is a front door, not a changelog** (at the Director's word). It went
  from 867 lines to 208 by **relocating** — never deleting — the chronological arc
  narrative to [docs/arc-history.md](docs/arc-history.md), the durable findings and
  hard-won rules to [docs/findings.md](docs/findings.md), the tool status tables to
  [docs/tools.md](docs/tools.md), and the defect list to
  [docs/known-defects.md](docs/known-defects.md).

  **Nothing measured was lost, and that is audited rather than asserted:** every
  non-blank line of the old README was diffed against the union of its new homes.
  Three lines differ, and all three are the marketing tagline, deliberately rewritten.
  All six ⚠ annotations survive. Corrections stay in place beside the measurements
  that overturned them, exactly as before — they just live one click deeper.

### What v0.1.0 asserts

**Four accepted assets across four subject classes, at zero credits.**

- **W3, the character** — accepted 2026-08-04 at the Director's own zoom
  ([E08 Amendment 35](docs/experiments/E08-ruling-gate0.md)). Mix 68.8% reference /
  4.2% brush / 27.0% dilation against the rejected asset's 28.4 / 37.7 / 33.9.
- **The galleon** — accepted 2026-08-05 ([E04-ruling.md](docs/experiments/E04-ruling.md),
  29 rulings). The first non-character subject; every subject value drawn from
  `profiles/ship.json` and `canon/GALLEON-IDENTITY.md`.
- **The dragon** — accepted 2026-08-07 ([E12-ruling.md](docs/experiments/E12-ruling.md),
  Rulings 1–30). Designation to acceptance in three days; 87.49% of the surface a
  viewer can see is the accepted pair's own paint.
- **The longsword** — accepted 2026-08-08 ([E14-ruling.md](docs/experiments/E14-ruling.md),
  Rulings 1–35). The first portrait-framed subject; the drifted gem returned to
  garnet by arithmetic rather than regeneration.

**The record is instrumented.**

- `tools/facet_index.py` — SQLite+FTS5 over the whole record, verified on four legs
  (byte-identical determinism across interpreters, counts against independent greps,
  zero dangling pointers, a seeded question gate)
  ([E15-ruling.md](docs/experiments/E15-ruling.md)).
- **213 tests, 213 passing at two seats' hands** — 205 hermetic + 8 artifacts — plus the
  repo's first CI workflow, paths-gated and pinned
  (the harness at [E17 Ruling 5](docs/experiments/E17-ruling.md), which closed that arc
  at 32; [E18](docs/experiments/E18-ruling.md) rode 60 more in on the commits that built
  the record-index MCP; [E20](docs/experiments/E20-ruling.md) is adding the unit tier).
  Counted at this commit rather than inherited: `pytest --collect-only` over the
  committed `tests/` returns 213, and 205 with `-m "not artifacts"`. **The lineage is
  27 → 32 → 92 → 202 → 213 in a single day** — E20 closed and was ruled, then the
  extraction's own T27 added eleven more. Re-counted at the tagging commit before the
  tag was cut, per [E19 Ruling 7](docs/experiments/E19-ruling.md); that gate fired five
  times and caught a stale number on every one of them.
- The claims sweep (`facet_index.py claims`) reads **0 STALE** against the record.

**Four dense assets are in the training dataset**, 114 records across five ingests
([E11-ruling.md](docs/experiments/E11-ruling.md),
[E14 Ruling 34](docs/experiments/E14-ruling.md)).

### What v0.1.0 does NOT assert

- That the texture stage is finished. The blade band, the unlevelled stroke seams and
  the cross-island dilation bleed are named, measured and open — see **Known defects,
  named** in the README, which the treatment left standing word for word.
- That any claim in this repo is safe to inherit unchecked. Six inherited claims were
  falsified in the founding session alone; the corrections are kept in place beside
  the measurements that overturned them, which is the point.
