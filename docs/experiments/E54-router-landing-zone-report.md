# E54 — Router landing-zone report

Executor seat, dispatched by the advisor 2026-08-17, to clear the tree ahead of the next
canon-router round: repair the index's arc reader (task 1), move the stale t87 artifacts
pin (task 2), and census every spend-capable path in `tools/` against
`canon_gate.refuse_uncovered` (task 3, measurement only). Uncommitted; the advisor folds.

Hard fence honored throughout: no edits to `tools/canon_gate.py`, `canon/*.surfaces.json`,
`canon/*IDENTITY.md`, any `README*`, or `docs/experiments/E52-*`/`E53-*`.

**Change-set (uncommitted, for the fold):**

| file | change |
|---|---|
| `docs/index/conventions.json` | line 237: `laws.paid_for_by` bound `E5[01]` -> `E5[0-4]` |
| `tests/test_t24_index_parsers.py` | literal E52/E53 pin added inside the existing span leg (no new collected test) |
| `tests/test_t87_canon_gate.py` | armb pin re-stated at the measured truth + renamed; profile-default test renamed to what it asserts; file header count corrected; `hashlib` import |
| `docs/experiments/E54-router-landing-zone-report.md` | this report (new) |

Collect counts after all edits: **1283 / 1229 / 54 — byte-identical to the reconciled T34
pins.** The change-set is count-neutral by construction (extension-in-place and renames
only), so the two-seat count-surface collision the record warns about does not arise from
this seat.

**Dispatch premise check** (the dispatch asked that its own premises be distrusted):
"Three defects remain" — CONFIRMED by running the full suite before touching anything:
`t24::test_t24_paid_for_by_reads_every_arc_the_record_has` (hermetic),
`t34::test_t34_every_readme_carries_both_counts_twice[README.fr.md]` (hermetic),
`t87::test_t87_armb_workflow_is_sixteen_of_seventeen` (artifacts). Initial hermetic run:
2 failed / 1227 passed. One premise was stale: the dispatch's git snapshot said clean at
`a7f7b0b`; the live tree is at `fd3ece2` with the router round's own change-set sitting
uncommitted (canon_gate.py, w3.surfaces.json, brush_cloud_step.py, t92, READMEs, census).
None of those files intersect this seat's lanes.

---

## Predictions vs outcomes

Predictions were registered in this file before opening any repo source, test, or canon
file, and before running any command (the first Write of this document precedes every
other tool call of the session; basis: the dispatch text plus the injected CLAUDE.md).

### P1 — why `PAID_RE` reads E01–E51 but not E52/E53

- **Predicted (primary):** an explicit numeric bound — an alternation/range/`<= MAX`
  written when the then-max arc was newest, needing a manual bump nobody made.
  **RIGHT on the cause.** Measured: `docs/index/conventions.json:237` declares
  `\b(E0[1-9]|E[1-4]\d|E5[01])\b` — an alternation bounded at E51, compiled by
  `record_index/conventions.py:162` and exported as `PAID_RE` via
  `record_index/__init__.py:177` -> `facet_index.py:60`. The E34 ruling documents the
  same defect class and the same site.
- **Predicted repair shape: "generalize the numeric part to the open form" — MISS.**
  The bound is deliberate design: `test_t24_paid_for_by_is_a_bound_and_not_a_wildcard`
  requires the pattern to STOP at the record's span (a wildcard would zero the vocabulary
  counter forever), and the WHY-A-BOUND comment above it says so. The lawful repair is
  extending the bound to the record's current span, which is what was done.
- **Predicted (secondary):** a format/boundary assumption breaking on the new arcs'
  citation form — dead; the numeric range was the whole mechanism.
- Blind: yes, to the code. The dispatch named no cause for this task.

### P2 — why t87 reads 14 where its name said sixteen-of-seventeen

- **Predicted:** recorded string byte-unchanged; denominator 17 -> 19 (N18/N19 postdate
  the recording, both must miss); 5 misses total = {the old N17} ∪ {N18, N19} ∪ {two
  phrases broken by the skirt->kilt rename}. **RIGHT on every measured part.** Measured
  miss set: `[N8, N9, N17, N18, N19]`; N8/N9 are exactly the two renamed kilt rows.
- Disclosed at registration: the point value 14 was carried by the dispatch's own failure
  message (14 != 16), so that digit was low-information; and the prediction was not blind
  to the advisor's guess, which the dispatch itself carried. The decomposition (which
  commits, which rows, string constancy) is what this seat added and measured.
- Not predicted: the same commit (`2da2e3e`) also reworded N18 (`bare hands` ->
  `brown leather gauntlets`) — immaterial to the count (the recording contains neither),
  found in the sweep. Also found, unpredicted: the profile default lost its N8 hit to the
  same rename (6/19 -> 5/19), and the sibling test's name still said "six" over an
  assertion of 5.
- Alternates, each closed by measurement rather than assumption: (a) recorded artifact
  moved — no recorded manifest exists for facet_E08 (the manifest ritual starts at E33),
  but the file's mtime is 2026-08-04 (13 days before the canon work) and today's bytes
  reproduce the recorded-era claim exactly (16/17, miss = [N17]) under the 17-era phrase
  list; (b) the router round changed the matcher — the uncommitted `canon_gate.py` delta
  touches none of `parse_named_table` / `phrase_hits_in_text` / `ARTICLE` /
  `w3_named_phrases` (checked over the full diff); (c) the test reads a different phrase
  source — unchanged (`canon/W3-IDENTITY.md` NAMED table).

---

## Task 1 — the index arc reader

**Failure at seat start** (before any edit): `laws.paid_for_by cannot read 3 of the
record's own arcs ... E52, E53, E54` — this report's own file had already joined the
record and widened the miss from the dispatch's 2 to 3, which is the mechanism
demonstrating itself.

**Repair, test-first:**

1. Extended the existing leg `test_t24_paid_for_by_reads_every_arc_the_record_has`
   in place with a literal pin on E52/E53 — the discriminating case by name. Rationale in
   the code: the span-derived check can only fail while `parse_experiments` still reads
   the record; a broken span computation would silently shrink its range, and the leg
   could then no longer fail for exactly the arcs it exists to cover. The literal pin
   fails whatever the span computation returns. Placed in the same function so the
   collected count does not move.
2. Ran it against the old declaration: **FAILED**, with the compiled pre-repair pattern
   named in the output (`re.compile('\\b(E0[1-9]|E[1-4]\\d|E5[01])\\b')`) — the
   fails-against-old evidence, recorded.
3. Edited `docs/index/conventions.json:237` to `\b(E0[1-9]|E[1-4]\d|E5[0-4])\b`
   (E01–E54 admitted, E55 refused).
4. Ran the complete t24 file: **71 passed**, including the bound-not-wildcard leg
   (beyond-span E55 still refused) and the real-corpus orphan leg.

**Consumers of the changed root, checked per the find-its-other-consumers law:**

- The only other occurrence of the old fragment in the repo is the documenting comment
  inside the new test pin (intentional).
- `docs/experiments/README.md:60` mentions PAID_RE only in the E34 row's historical
  narrative — not a current-state claim; untouched.
- The tracked index (`docs/index/facet.db` + `facet.db.cert.json`) consumes the
  declaration at build time. Record server measured after the edit: **SERVING_STALE** —
  certificate PASSED (record_build 2026-08-17T20:37:21Z, corpus 403 files), corpus now
  408 files (3 modified, 5 added, this report among them). The fold needs the advisor's
  `record_build` ritual; nothing for this seat to write.

**Coupling, stated for the fold:** the bound is at E54 because the record's span is 54 —
this report's file is the E54 arc. The span leg and the bound leg hold as a pair only
while this file stays in the record; dropping the report at fold requires re-bounding to
E53 in the same commit.

## Task 2 — the t87 artifacts pin

**The measurement.** Recorded ARMB workflow
`E:\AI\training\facet_E08\ARMB\out\stroke_1_y+090_e+00_workflow.json`
(sha256 `42547a4253f6b4d031b7e2d5c29ca6ada79751170e97009b7b77423982ddf576`), node 7
`inputs.text` held constant; the W3 NAMED list swept across every revision of
`canon/W3-IDENTITY.md` through the pin's own code path
(`canon_gate.parse_named_table` + `canon_gate.phrase_hits_in_text`):

| revision | NAMED | hit | miss | what moved |
|---|---|---|---|---|
| `54bf90d` | 17 | 16 | N17 | the recorded claim, reproduced from today's bytes |
| `2e73ba8` | 19 | 16 | N17,N18,N19 | +N18 `bare hands`, +N19 shin guard |
| `2da2e3e` | 19 | **14** | **N8,N9**,N17,N18,N19 | N8/N9 `skirt` -> `kilt`; N18 -> `brown leather gauntlets` |
| `79b8fb6` / `fd3ece2` / worktree | 19 | 14 | same | no further movement |

The recording says `skirt` twice and `kilt` never; grip/gauntlet/greave/hand/shin zero
times. The cause named in the dispatch is confirmed by measurement, with the refinement
that the hit-count fall to 14 happened at `2da2e3e` (the rename commit), not at the
17->19 widening — the widening alone had left it at 16/19.

**Repairs (all inside `tests/test_t87_canon_gate.py`, which the dispatch licensed):**

- `test_t87_armb_workflow_is_sixteen_of_seventeen` ->
  `test_t87_armb_workflow_is_fourteen_of_nineteen`: expected numbers moved to the
  measured truth (`hit == 14`, `miss == [N8, N9, N17, N18, N19]`), docstring carries the
  decomposition table and why the pin is re-stated rather than deleted (a frozen
  recording can only lose hits as the canon is corrected; each loss measures the distance
  between the recorded spend and today's canon). Added `skirt == 2` / `kilt == 0` counts,
  and a sha256 byte pin on the recorded file — E08 armB state is in the record's
  byte-hash-contract family, and the pin turns a future recorded-tree drift into a
  notification instead of a silent hit-count move. The canon was not touched.
- Same disease, same file, fixed and flagged as adjacent-scope:
  `test_t87_profile_default_is_still_six_while_the_canon_grew` asserted 5 while its name
  and docstring said six — renamed to `test_t87_profile_default_hits_five_of_nineteen`
  with the history corrected in place (6/17 -> 6/19 by widening, -> 5/19 when the rename
  took the profile default's N8 `skirt` hit; measured: profile hits = [N2,N3,N4,N13,N14]).
  Assertions unchanged.
- File header: "six of seventeen" -> "five of nineteen" (the header describes the current
  refusal specimen; the history lives in the test docstrings).
- No other repo surface references the old test name (searched complete, tracked and
  untracked).

**Result:** complete t87 file **14 passed**, including the artifacts pin against the
recorded tree.

## Task 3 — the spend-site census

Method: complete enumeration of `tools/` (186 files excluding `__pycache__`; 176 `.py`,
plus `.ps1`, `.sh`, `.json`, `.diff`, egg-info), then mechanism-bounded sweeps rather
than name-bounded reading — a path can spend only if it (a) carries network code,
(b) loads a model, or (c) authors the workflow JSON an external transport submits.
Sweeps over all of `tools/`, read complete:

- network (`requests|urllib.request|urlopen|http.client|httpx|websocket|socket.`):
  **2 files** — `restylize_views.py`, `texpass_brush.py`
- shell-out HTTP (`curl|wget|Invoke-WebRequest|Invoke-RestMethod`): **0 files**
- model loading (`import torch|diffusers|StableDiffusion|.cuda|onnxruntime`): **7
  files** — `reconstruct_mesh.py`, `sr_views.py`, `ig2mv_licensefree.py`,
  `diagnostics/canny_probe.py`, `diagnostics/e32_route_preprocess.py`,
  `superseded/project_multiview.py`, `superseded/facing_atlas.py`
- ComfyUI graph authorship (`class_type`): **5 files** — `brush_cloud_step.py`,
  `restylize_views.py`, `texpass_brush.py`, `e37_fire_repaints.py`,
  `diagnostics/e12_pair_cloud_step.py`
- `refuse_uncovered` call sites (complete): `restylize_views.py:113`,
  `texpass_brush.py:44`, `brush_cloud_step.py:405` (definition `canon_gate.py:603`)

Every file outside the union of those sweeps has no mechanism to generate, post, or
author a submission graph. Classification of the union:

### Spend-capable paths

| # | path | spend mechanism | router in front? | gate line | fires before anything is written? |
|---|---|---|---|---|---|
| 1 | `tools/restylize_views.py` | POSTs twin restylize jobs to ComfyUI (`/upload` 172, submit 263); `--emit-only` builds the cloud path's controls | YES — conditional on `--canon` | 113 | YES — gate precedes `makedirs` (120), all writes and all network; the in-code comment pins "canon check BEFORE mkdir", and t31's refuses-in-every-mode legs cover it under `-O`/`PYTHONOPTIMIZE` |
| 2 | `tools/texpass_brush.py` | POSTs brush inpaint jobs to local ComfyUI (upload 70, submit 117, downloads 140/143) | YES — conditional on `--canon` | 44 | YES — nothing is written or posted before 44 |
| 3 | `tools/brush_cloud_step.py graph` | authors the PAID brush workflow JSON (Amendment 30: the saved JSON is the recipe the MCP submits verbatim) | YES — conditional on profile canon (`_canon_path_from_profile`, 354–376: `_fixtures.canon` -> `texpass_brush.py.canon.value` -> none = legacy path, t92-pinned) | 405 | YES — `makedirs` 409 and the `--out` write 411 both follow the gate; t92 pins `--out` absent on refusal |
| 4 | `tools/diagnostics/e12_pair_cloud_step.py` | authors the PAID twin/restylize workflow JSON — the same Amendment-30 shape, its own docstring says so | **NO** | — | pre-flight and topology checks raise and leave no file, but no canon question is ever asked. Insertion point if the advisor wires it: after pre-flight, before the `--out` write, resolving canon from the already-required `--profile` exactly as `brush_cloud_step.py:354-376` does (subjects with no surfaces file resolve to none = no check, the t92 rule) |
| 5 | `tools/e37_fire_repaints.py payload` | authors PAID repaint payloads from a byte-pinned recorded base (`PHASE1/payloads/set2026081511_v*.json`); prompt/seed/cn byte-held, only init+mask move; writes under the E37 training tree | **NO** | — | link/self-link ANDONs precede the write (239). Design tension for the advisor, not a mechanical add: the prompt is a RECORDED artifact, and task 2's own measurement shows recorded prompts fall out of a corrected canon's coverage by construction (they say `skirt`). Gating replays against today's canon is a semantics decision |
| 6 | `tools/ig2mv_licensefree.py` | LOCAL prompted diffusion generation (SDXL + MV-Adapter), takes `--text` | **NO** — and no `subject_profile` binding at all | — | insertion point if wired: after `parse_args` (65), before pipeline construction and the saves (151/153) |
| 7 | `tools/texpass_loop.ps1` | driver: invokes `texpass_brush.py` once per stroke | **NO** — lines 127–129 pass only `--job/--seed/--prompt` (+`--negative`), so the gate in texpass_brush never arms | — | per-stroke stems are the router's DECLARED not-yet scope (W3 `scopes.strokes == {}`; canon_gate's Known section; and a subject-level check on stems would be wrong by design — the rear camera must omit the beard, E01). The honest wiring arrives with stroke scopes, not with a flag |
| 8 | `tools/reconstruct_mesh.py` | local GPU TRELLIS.2 image->3D generation | not applicable | — | no prompt operand exists; the router's contract is prompt coverage. Canon rides in the input image's provenance, upstream |
| 9 | `tools/sr_views.py` | local GPU deterministic GAN SR (RealESRGAN via spandrel) | not applicable | — | promptless and deterministic by design |

### Verified not spend-capable (the rest of the union)

- `diagnostics/canny_probe.py` — CPU-only Canny replication; "No models loaded, no VRAM
  touched" and no network.
- `diagnostics/e32_route_preprocess.py` — the reconstructor's preprocess transcribed in
  PIL/numpy precisely so the GPU pipeline is NOT loaded.
- `superseded/project_multiview.py`, `superseded/facing_atlas.py` — projection and
  bake arithmetic on tensors; no sampler, no model, no network.
- `region_disagreement.py` — the spend-DECISION instrument; measures, never spends.
- `replay_strokes.sh` — replays recorded strokes through emit/commit against
  pre-registered anchors; never calls the brush, generates nothing.
- prompt/sheet families (`e04/e12/e14_make_*_prompts`, `e12/e14_pair_sheet`, etc.) —
  author or read prompt files and sheets upstream of the gates; no mechanism.
- MCP servers in `tools/` (`record_mcp.py`, the measure server) — no network-submission
  code (the network sweep is the instrument).

### Boundary and residuals, stated plainly

- **The actual cloud submission transport is outside `tools/`**: the session drives the
  saved JSONs through the Comfy Cloud MCP. There is no in-repo gate at submission time;
  the router fires at authoring time, and the saved JSON is the recipe (Amendment 30).
  A hand-built JSON submitted directly through the MCP meets no gate anywhere.
- **Every present gate is conditional** on a canon reaching the tool (flag or profile).
  `profiles/character.json` binds `canon: canon/w3.surfaces.json` for both network tools
  and carries the `_fixtures.canon` block brush_cloud_step resolves; a bare invocation
  without `--profile`/`--canon` is ungated by construction, and both tools' built-in
  default prompts still contain `gold necklace` and `skirt` — the live-default lie the
  round exists to refuse is refused only when the profile rides along.
- **`texpass_brush.py:44` has no t31-style refuses-in-every-mode leg** (restylize and
  brush_cloud_step have theirs, sites 59/60 in t31's count comment). Measured gap,
  reported not repaired: adding legs would move the reserved count surfaces.
- `docs/grok-consult-18-brief.md:35` says the gate is "called at exactly two places" —
  true when written, three since the router round. Historical consult document; stands.

---

## Blocked by the fence

1. **`t34::test_t34_every_readme_carries_both_counts_twice[README.fr.md]`** — the last
   hermetic red. Measured: README.fr.md carries `1283` once and `1229` once (both at line
   207, the bullet); the Requirements paragraph carries no digits at all, and no stale
   `1266`/`1212` exists anywhere in the file — the translation dropped the second site
   rather than staling it. Repair is regenerating the eight translations together
   (`translate-all.mjs README.md --cache-clear`, the test's own remedy text) — fenced
   (`README.*.md`), and advisor-owned under the translation rule.
2. **`tools/canon_gate.py` module docstring, calibration paragraph** — measured-stale on
   four claims and fenced (second builder's file): "The ARMB workflow ... contains 16 and
   is missing only N17" (measured 14, missing N8,N9,N17,N18,N19); "contains exactly 6 of
   the W3 NAMED phrases" for the profile default (measured 5; the selftest itself prints
   `profile-default hits 5 of 19` and two tests pin that string); "W3_NAMED ... is 20
   since the Director caught the hand draft" (measured 19 at the worktree; the identity
   pin asserts 19); "Neither hit count moved at any step" (both moved at `2da2e3e`:
   16 -> 14 and 6 -> 5).

## Tree state at seat end

| run | result |
|---|---|
| hermetic, seat start | 2 failed (t24, t34[fr]) / 1227 passed |
| t87 armb pin, seat start | FAILED — 14 != 16, miss `[N8,N9,N17,N18,N19]` |
| hermetic, seat end | **1 failed (t34[fr], fenced) / 1228 passed** |
| complete t24 file | 71 passed |
| complete t87 file (incl. artifacts pin) | 14 passed |
| artifacts tier, `not slow` | 39 passed / 0 failed / 0 skipped (the other 15 of 54 are `slow`-marked and were not run) |
| collect counts | 1283 / 1229 / 54 — unchanged, equal to the T34 pins |
| record server | SERVING_STALE (certificate PASSED at 2026-08-17T20:37Z; corpus moved 3 modified + 5 added since) — advisor's `record_build` at fold |
| fold-marked tests, after this report's final content joined the corpus | 8 passed |

**Seat-end observation (two seats live):** after every run above completed, the second
seat's work began appearing in the tree — `tools/canon_worksheet.py` and
`docs/grok-consult-19-brief.citation-receipt.json` are new untracked files that did not
exist at any of this seat's measurements. `t92::test_t92_no_worksheet_was_commissioned`
asserts that worksheet file's absence and will fire on the tree as it now stands; t92 is
the second seat's surface and nothing here touched it. Every number in this report is
honest as of its run time; the reconciliation of the combined tree is the advisor's, per
the record's two-seats law.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | every measurement names instrument, revision and command; the decomposition method is restated in the t87 docstring so it replays from the repo; pytest runs pin the interpreter (`E:\AI-Models\trellis2-env\Scripts\python.exe`) and a scratch `--basetemp` |
| ANDON_AUTHORITY | 2 | both fired gates were repaired at the declaration/test layer with red-then-green evidence, never tuned past; the fenced red is left standing and reported as a fired gate |
| NAMED_COMPENSATORS | 2 | no irreversible action performed (no commit, no publish, no cloud call, no training-tree write); every change is an uncommitted worktree edit; undo = `git checkout -- <path>` per file in the change-set table; owner: advisor at fold |
| DECOMPOSE_BY_SECRETS | 2 | lanes grouped by what changes together (declaration + its test; artifacts pin + its in-file siblings; census read-only), and the fence respected as the second seat's boundary |
| UNCERTAINTY_GATED_HUMANS | 2 | the two design tensions (gating recorded-prompt replays against a corrected canon; per-stroke stems vs subject-level checks) are routed to the advisor with the contrastive framing, not decided here |
| EXTERNAL_VERIFIER | 1 | the seat that measured also wrote the repairs; in-seat checks are machine legs (red/green, byte pin), not a second judge. Remediation: the advisor's ruling on this report is the external verification step — owner: advisor, target: the fold session; the repo's role separation is the mechanism |

## Out of scope

- Wiring any gate (census rows 4–7 name insertion points; the dispatch forbids wiring).
- The README.fr.md regeneration and every fenced correction above.
- Refreshing the tracked index DB/certificate (`record_build` — the advisor's ritual).
- The 15 `slow`-marked artifacts tests (not run; the tier's non-slow set is clean).
- A t31-style leg for `texpass_brush.py:44` (gap reported; count surfaces reserved).
- The E54 row in `docs/experiments/README.md`'s status table (the fold's ritual).
- Any change to canon content, prompts, or profiles.
