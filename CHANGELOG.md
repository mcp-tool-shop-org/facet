# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

**A note on what a version means here.** facet publishes nothing — no npm package,
no PyPI package, no installer, no manifest with a version field. A version in this
file is a claim about **the state of the record**: which experiments are closed,
which assets the Director has accepted, and what the tools measurably do at that
commit. Every entry below points at the ruling that established it, so a reader can
check the claim rather than trust it.

## [Unreleased]

### Added

- Presentation surface (E19 treatment): landing page, Starlight handbook, README
  header, `SECURITY.md`, this file, GitHub metadata. **No measured claim, correction
  or ⚠ annotation in the record was rewritten, trimmed or deleted** — the treatment
  adds surface and leaves the record intact.

## [1.0.0] — proposed, awaiting the Director's word

Proposed at the close of the E19 treatment. Not yet tagged; there is no manifest to
bump, so this version exists as a tag and this heading and nothing else.

### What v1.0.0 asserts

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
- **32 tests, 32 passing at two seats' hands** — 24 hermetic + 8 artifacts — plus the
  repo's first CI workflow, paths-gated and pinned
  ([E17 Ruling 5](docs/experiments/E17-ruling.md), which closed the arc; Ruling 1's
  27/27 is the earlier state and is superseded by it). Counted at this commit rather
  than inherited: `pytest --collect-only` over the committed `tests/` returns 32.
- The claims sweep (`facet_index.py claims`) reads **0 STALE** against the record.

**Four dense assets are in the training dataset**, 114 records across five ingests
([E11-ruling.md](docs/experiments/E11-ruling.md),
[E14 Ruling 34](docs/experiments/E14-ruling.md)).

### What v1.0.0 does NOT assert

- That the texture stage is finished. The blade band, the unlevelled stroke seams and
  the cross-island dilation bleed are named, measured and open — see **Known defects,
  named** in the README, which the treatment left standing word for word.
- That anything here is packaged, installable, or supported as a product. Nothing
  publishes until the ruled extraction gate.
- That any claim in this repo is safe to inherit unchecked. Six inherited claims were
  falsified in the founding session alone; the corrections are kept in place beside
  the measurements that overturned them, which is the point.
