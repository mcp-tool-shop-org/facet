# Ship Gate

> No repo is "done" until every applicable line is checked.
> Copy this into your repo root. Check items off per-release.

**Tags:** `[all]` every repo · `[npm]` `[pypi]` `[vsix]` `[desktop]` `[container]` published artifacts · `[mcp]` MCP servers · `[cli]` CLI tools

**Detected tags at the treatment's audit: `[all]`** — `shipcheck init` v1.0.7,
2026-08-08. At that moment facet carried no dependency manifest, no entry point and
no published artifact of any kind.

> ⚠ **THAT TAG SET IS NOW OUT OF DATE, and this line says so rather than quietly
> reading as current.** The Director fired the extraction gate the same day:
> `pyproject.toml` and `package.json` both exist, so a fresh `shipcheck init` will
> detect **`[pypi]`** and **`[npm]`** and turn on gate families that are SKIP-ed
> below with *"nothing publishes until the extraction gate"* as their written
> re-open condition. **The 100% pass rate recorded here is true for the
> pre-extraction tag set only.** A re-audit is owed at the next fold — it is the
> gate that remembers what was forgotten, which is exactly why the SKIPs carry
> conditions instead of just reasons.

**How to read the SKIPs below.** Most of them share one reason and it is a ruled
one: **facet publishes nothing until the extraction gate.** The four MCP tools
specced in `docs/specs/` are placed but not extracted; until they are, there is no
package, no installed command, and no product surface for a product-surface item to
bind to. Each SKIP names its own re-open condition, because a SKIP whose condition
is unwritten quietly becomes doctrine — the failure mode this repo exists to avoid.

---

## A. Security Baseline

- [x] `[all]` SECURITY.md exists (report email, supported versions, response timeline) (2026-08-08) — [SECURITY.md](SECURITY.md); report address, `main`-only support table, 48h/7d/30d timeline
- [x] `[all]` README includes threat model paragraph (data touched, data NOT touched, permissions required) (2026-08-08) — README **Trust and threat model**, with the three sharp edges disclosed rather than claimed away
- [x] `[all]` No secrets, tokens, or credentials in source or diagnostics output (2026-08-08) — swept the whole tree for provider-prefixed keys, `ghp_`/`github_pat_`, `xox[baprs]-`, `AKIA…`, private-key blocks, bearer tokens and inline `api_key`/`password` assignments: **zero matches**; `git ls-files` carries no `.env`, `.pem`, `.key` or credential-shaped file
- [x] `[all]` No telemetry by default — state it explicitly even if obvious (2026-08-08) — none collected, none sent, stated in README and SECURITY.md. Measured: exactly two of thirty-four tools open a socket (`restylize_views.py`, `texpass_brush.py`), both to a ComfyUI HTTP API at `--host`, **default `127.0.0.1:8188`**

### Default safety posture

- [ ] `[cli|mcp|desktop]` SKIP: facet is not tagged `[cli]`, `[mcp]` or `[desktop]` and installs no command — and where a tool performs an irreversible step the ruled design is the **opposite** of an opt-in flag: the gate lives *inside* the tool with **no skip flag** (E08 Amendment 32, earned after a shell chain walked past a fired gate and committed 47,020 texels anyway). An `--allow-*` escape hatch here would be a regression against a ruling, not an improvement. Re-opens at extraction, when a tool becomes an installed command someone else runs.
- [ ] `[cli|mcp|desktop]` SKIP: file operations are **not** constrained to known directories, and the honest move is to disclose that rather than check a box. Every path is supplied by the operator on the command line; there is no allow-list and no confinement. Stated plainly in SECURITY.md and the README threat model. Re-opens at extraction — a shipped tool needs a real boundary, and specifying it is extraction work.
- [x] `[mcp]` Network egress off by default (2026-08-08, **re-run at the E19 ruling** — this line was SKIP-ed as "no MCP server on `main` at this audit"; `tools/record_mcp.py` landed and the SKIP's own re-open condition fired) — `record_mcp.py` imports no `socket`, `requests`, `urllib` or `http.client`, and makes zero network calls in 868 lines. The transport is stdio. Egress here is not "off by default", it is **absent**.
- [x] `[mcp]` Stack traces never exposed — structured error results only (2026-08-08, re-run at the E19 ruling) — every deliberate refusal leaves through a single site (`_raise`), so the wire shape has one implementation; measured live at the ruling with two bad inputs, both returning `code`/`message`/`hint`/`retryable` and no traceback. `record_build` additionally wraps *unexpected* exceptions into `INTERNAL` with the class name and message and no traceback. ⚑ **Bounded, and the bound is stated rather than smoothed over:** the other five tools carry no such wrapper and rely on the MCP framework's own error envelope for a genuinely unexpected exception. Extending the wrapper is want 10 at [E19 Ruling 5](docs/experiments/E19-ruling.md).

## B. Error Handling

- [ ] `[all]` SKIP: facet has no structured error shape, and retrofitting one across ~34 research instruments is neither this treatment's scope nor this lane's (`tools/` belongs to E18). What it has instead is a named convention: deliberate halts `raise SystemExit("ANDON: …")` carrying the measurement that fired them, so a halt is legible at the point of failure rather than at a log aggregator. **The condition is written, not implied:** the `code`/`message`/`hint` contract is a *product-surface* contract and lands with the extracted MCP tools, whose specs already require structured tool results. Disclosed in SECURITY.md so no reader has to discover it.
- [ ] `[cli]` SKIP: not tagged `[cli]` — nothing is installed as a command. Measured behaviour, recorded so the SKIP is not hiding anything: tools ending `sys.exit(main())` return `0` on success and non-zero on failure, and `ANDON` halts exit non-zero — so 0-vs-nonzero is real, but the **0/1/2/3 registry is absent**. Re-opens at extraction.
- [ ] `[cli]` SKIP: not tagged `[cli]`. Measured and disclosed: unexpected failures surface as raw Python tracebacks and there is no `--debug` gate. Re-opens at extraction.
- [x] `[mcp]` Tool errors return structured results — server never crashes on bad input (2026-08-08, **fired live at the E19 ruling**, not attested) — two independent bad inputs through the mounted server: `limit=999` returned `BAD_ARGUMENT` / *"limit must be between 1 and 50"* / a hint naming the valid range, and `table="not_a_table"` returned `BAD_ARGUMENT` naming all eight valid tables. Both carry `code`, `message`, `hint` and `retryable`. **The server stayed up** — `record_health` answered normally in the same exchange.
- [x] `[mcp]` State/config corruption degrades gracefully (stale data over crash) (2026-08-08, re-run at the E19 ruling) — `health()`'s contract is *"Never raises — it returns the refusal instead"*, so a caller can ask what state the index is in without being refused, and the surface carries a literal `SERVING_STALE` state that serves the older record behind a banner naming the one fix command. E18's dogfood fired this for real on a hand-corrupted DB: every read tool refused with its code, health kept answering, and one `record_build` recovered.
- [ ] `[desktop]` SKIP: not a desktop application — no UI of any kind.
- [ ] `[vscode]` SKIP: not a VS Code extension.

## C. Operator Docs

- [x] `[all]` README is current: what it does, install, usage, supported platforms + runtime versions (2026-08-08) — the README is the repo's measured-state document and is maintained as one: claims corrected in place beside the measurements that overturned them. Requirements names Blender 5.x, Python 3.11+ and the dependency set; the treatment added the CI matrix (ubuntu-latest / Python 3.12, pinned) and both local test invocations
- [x] `[all]` CHANGELOG.md (Keep a Changelog format) (2026-08-08) — [CHANGELOG.md](CHANGELOG.md), with the v0.1.0 entry stating what the version asserts **and what it does not**
- [x] `[all]` LICENSE file present and repo states support status (2026-08-08) — MIT, `LICENSE`; support status stated in both the README threat-model section and SECURITY.md (`main` is the only supported state; no release channel, no backport policy, no SLA)
- [ ] `[cli]` SKIP: not tagged `[cli]`; no installed command has a `--help` contract to be accurate about. Measured note so this is not hiding behind a tag: 32 of 34 tools use `argparse`, and `tools/diagnostics/e12_help_format_scan.py` gates help-string *formatting* — **not accuracy**, which is a different property and is not claimed here. Re-opens at extraction.
- [ ] `[cli|mcp|desktop]` SKIP: there are no logging levels, deliberately. In this repo **stdout is the measurement record** — a tool prints the numbers a report is written from, and suppressing them behind a level would suppress the evidence. Nothing is redacted because nothing sensitive is printed (see A3). Re-opens at extraction, where a shipped tool needs a quiet mode.
- [x] `[mcp]` All tools documented with description + parameters (2026-08-08, re-run at the E19 ruling) — all six tools (`record_query`, `record_get`, `record_build`, `record_verify`, `record_health`, `record_claims`) carry a description, and each documents its parameters with meaning and range in that description; the server also carries `instructions` telling a caller how the query→read loop is meant to run. ⚑ **Bounded:** the JSON schema carries no per-field `description` keys, so the parameter docs are in the prose a caller reads rather than machine-readable per-parameter. Checked on substance; the schema gap is want 9 at [E19 Ruling 5](docs/experiments/E19-ruling.md).
- [ ] `[complex]` SKIP: no daemon, no background service, no state files requiring recovery procedures, no operational modes. Every tool is a one-shot invocation the operator watches. (The Starlight handbook the treatment adds is a *product* handbook, not the C7 operations runbook.)

## D. Shipping Hygiene

- [x] `[all]` `verify` script exists (test + build + smoke in one command) (2026-08-08) — `python -m pytest` runs the full **213-test** suite; `python -m pytest -m "not artifacts"` runs the **205** hermetic tests CI reproduces. There is no build step because nothing is built. The artifacts tier is the smoke layer — it replays recorded trees and anchors. Configured in `pytest.ini`, gated in `.github/workflows/ci.yml`, established in [E17 Ruling 5](docs/experiments/E17-ruling.md) and extended by [E18](docs/experiments/E18-ruling.md). *Re-counted 2026-08-08 at the E19 ruling: this line read 32/24, true when written and stale the same day when E18 landed 60 tests in the parallel lane. It was then corrected to 92/84 and went stale **again within the ruling session** when E20 committed its unit tier, and **twice more** as the extraction's own T27 grew to eleven tests. Lineage 27 → 32 → 92 → 202 → 213 in one day. Re-counted at the tagging commit per [E19 Ruling 7](docs/experiments/E19-ruling.md) — **the gate fired five times and caught a stale number on every one of them**, which is the strongest argument in the record for want 2: a live-moving quantity on a presentation surface needs a gate, not a habit.*
- [ ] `[all]` SKIP: **no manifest carries a version**, so there is nothing to match a tag against. facet has no `package.json`, `pyproject.toml` or equivalent. `v0.1.0` lives as a git tag plus the CHANGELOG heading and nowhere else — CHANGELOG.md states this explicitly rather than implying a package exists. ⚑ **Note (2026-08-08): the npm name `@mcptoolshop/facet` is reserved by a `0.0.0` placeholder published from a sibling directory OUTSIDE this repo**, deliberately, so facet's root stays manifest-free and this SKIP does not re-open on a name reservation. Re-opens at extraction, when an extracted tool gains a real manifest.
- [ ] `[all]` SKIP: facet declares **no dependency manifest**, so there is no dependency graph for a scanner to read. Its runtime deps are documented prose in the README and pinned inline in `ci.yml`'s install step. ⚑ **Flagged for the ruling, not decided here:** if the ruling wants D3 executed rather than skipped, the cheapest honest form is a `pip-audit` step over the versions `ci.yml` already pins — that is one step in **E18's lane**, so it is named here and not edited.
- [ ] `[all]` SKIP: no automated dependency-update mechanism, by two independent reasons — the org's own GitHub Actions rule (*"Do NOT add dependabot.yml unless explicitly requested"*), and no manifest for dependabot to track even if it were requested.
- [ ] `[npm]` SKIP: **executed, not attested** — `npx @mcptoolshop/shipcheck pack` (Gate H, v1.0.7) ran against this repo on 2026-08-08 and reported *"no publishable packages found"*, exit 0. There is no workspace, no `package.json`, and nothing to pack. Re-opens at extraction.
- [ ] `[npm]`/`[pypi]` SKIP: no `package.json` and no `pyproject.toml`, so neither `engines.node` nor `requires-python` has a file to live in. The runtime floor is stated in the README (Python 3.11+, Blender 5.x) and pinned in CI (3.12). Re-opens at extraction.
- [ ] `[npm]`/`[pypi]` SKIP: no lockfile because no manifest; no wheel or sdist because nothing is packaged. CI pins its install set inline instead, which is the honest equivalent at this state. Re-opens at extraction.
- [ ] `[vsix]` SKIP: not a VS Code extension.
- [ ] `[desktop]` SKIP: not a desktop application.

## E. Identity (soft gate — does not block ship)

- [x] `[all]` Logo in README header (2026-08-08) — the clay **FACET** wordmark, chosen and pushed by the Director to `mcp-tool-shop-org/brand/logos/facet/readme.png`; referenced from the README at the brand raw URL, centred at width 400, verified live (HTTP 200). Rationale and the separate four-accepted-assets showcase sheet are documented in [docs/brand/README.md](docs/brand/README.md)
- [x] `[all]` Translations (polyglot-mcp, 8 languages) (2026-08-08) — **RUN at the advisor's hands, before the tag**, per the release-ordering law: `translate-all.mjs` on TranslateGemma 27B, zero API cost, against the FINAL README (corrected 202/194 counts, landing-page badge, rewritten threat model). Seven files land with the source in one commit — `ja zh es fr hi it pt-BR` — and the language nav bar is in the source README. ⚑ **Six headings arrived carrying two candidate translations each** (the model declining to choose, e.g. `## Qual é a situação atual? / Em que ponto estamos?`); each was resolved against the ENGLISH heading rather than by position, in `fr`, `hi`, `it`×2, `pt-BR`, `zh`. Caught by reading the output, not by trusting exit 0
- [x] `[org]` Landing page (@mcptoolshop/site-theme) (2026-08-08) — `site/`, built and walked at desktop width: `dist/index.html`, six handbook pages under `dist/handbook/`, and the Pagefind search index (at `dist/pagefind/` — current Starlight, not the playbook's `dist/_pagefind/`). `secondaryCta` is the org invariant `handbook/`. The **Pages deploy** is a separate irreversible act and is staged for the Director's word
- [x] `[all]` GitHub repo metadata: description, homepage, topics (2026-08-08) — **FIRED and verified by read-back**: description set, `homepage` → `https://mcp-tool-shop-org.github.io/facet/` (serving since Pages run `31266198261`, so the field resolves rather than 404s — the condition this line was held on), and **ten topics** (`3d texturing game-assets blender python diffusion comfyui trellis pipeline mcp`; `mcp` added because facet now ships an MCP server). Compensator unchanged at [E19-treatment-report.md](docs/experiments/E19-treatment-report.md) §8a — restore the verbatim pre-treatment description, `--homepage ""`, `--remove-topic` each. ⚑ **Honestly recorded: this sat done-able for hours after the Director's go-ahead and he had to ask why the repo had no landing-page link.** The staging was right; not firing it was not

---

## Gate Rules

**Hard gate (A–D):** Must pass before any version is tagged or published.
If a section doesn't apply, mark `SKIP:` with justification — don't leave it unchecked.

**Soft gate (E):** Should be done. Product ships without it, but isn't "whole."

**Checking off:**
```
- [x] `[all]` SECURITY.md exists (2026-02-27)
```

**Skipping:**
```
- [ ] `[pypi]` SKIP: not a Python project
```
