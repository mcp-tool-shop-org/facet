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

### Added

- **Presentation surface** (E19 treatment): a landing page, a six-page Starlight
  handbook rendered from the canonical `docs/handbook/`, the clay wordmark logo,
  `SECURITY.md` with a measured threat model, `SHIP_GATE.md`, `SCORECARD.md`, and
  this file.
- **A repo-knowledge entry** — thesis, architecture, conventions, environment traps,
  drift risks and three mapped relationships.

### Changed

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

## [0.1.0] — 2026-08-08

Cut at the close of the E19 treatment, at the Director's word. There is no manifest to
bump, so this version exists as a git tag and this heading and nothing else.

**Why 0.1.0 and not 1.0.0.** The Director set the number. It is the honest one: the
extraction gate is open, three testability seams are dispatched and untaken, and the
repo's own highest-value question (P5 — `fit_background` at frame-edge figures) has
never been looked at. A 1.0.0 would assert a stability this route has not earned yet.
What the four accepted assets earn is a *first* release, not a stable one.

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
- **202 tests, 202 passing at two seats' hands** — 194 hermetic + 8 artifacts — plus the
  repo's first CI workflow, paths-gated and pinned
  (the harness at [E17 Ruling 5](docs/experiments/E17-ruling.md), which closed that arc
  at 32; [E18](docs/experiments/E18-ruling.md) rode 60 more in on the commits that built
  the record-index MCP; [E20](docs/experiments/E20-ruling.md) is adding the unit tier).
  Counted at this commit rather than inherited: `pytest --collect-only` over the
  committed `tests/` returns 202, and 194 with `-m "not artifacts"`. **The lineage is
  27 → 32 → 92 → 202 in a single day** — E20 has since closed and been ruled, and the
  figure is re-counted at the tagging commit before the tag is cut, per
  [E19 Ruling 7](docs/experiments/E19-ruling.md).
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
