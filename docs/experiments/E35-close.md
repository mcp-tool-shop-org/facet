# E35 — close

**Task 5, at the Director's word ([E35-ruling.md §10](E35-ruling.md)).** Nothing new was
attempted: manifests, count surfaces, census, report, commits, index. **Spend closes at
47 of 60.** The close ruling is the advisor's and follows the Director's three sheet calls.

---

## 1. Manifest gates at close — four, all HELD

| manifest | scope | result |
|---|---|---|
| **A** `E33_manifest.json` | `facet_E33` | **HELD** — 116 declared / 116 present, **0/0/0**, 835,059,987 bytes. Its self-reference is reported on its own line and not counted |
| **B** `E34_manifest.json` | `facet_E34` | **HELD** — 84 / 84, **0/0/0**, **177,563,094 bytes against the declared 177,563,094** |
| **C** eight protected subtrees | `facet_next`, `facet_E01/E02/E05/E06/E07/E08`, `saltroad_bake_fix` | **HELD** — **7,312 files / 17,072,807,610 bytes**, delta **+0 files / +0 bytes** against the E23 record |
| **D** `E35_manifest.json` | `facet_E35` — **new at this close** | emitted **335 files / 284,096,148 bytes**, `excludes_self: true` per the E34 form, then verified in a second pass: **HELD**, 0/0/0 |

Manifest C, per subtree: `facet_next` 5,040 · `facet_E01` 156 · `facet_E02` 146 ·
`facet_E05` 129 · `facet_E06` 96 · `facet_E07` 51 · `facet_E08` 818 ·
`saltroad_bake_fix` 876.

### The walk itself is now committed, which it was not before

Three arcs rewrote this verifier inline. E35's open session rebuilt it, **fired a false halt**
on `E34_manifest.json` — which declares `excludes_self: true` and is absent from its own file
list by construction — repaired the walk, and the repair went nowhere. It is now
`tools/verify/tree_manifest.py`, and it handles **both encodings the record actually uses**:

- **E34 form** — `root`, `files` as a dict, `excludes_self: true`.
- **E33 form** — `_root`, `files` as a **list**, and the manifest **lists itself** with a hash
  that is stale by construction. That entry is reported on its own line and excluded from the
  change count; the exclusion is printed, never silent.

Both encodings say the same thing about the same hazard: a manifest cannot record its own
hash, because writing the hash changes the file.

**Its can-fail fixture rides with it** — `--selftest`, eight legs: clean HELD under
self-exclusion; intruder, changed byte and removed file each FIRE; the E33 form HELDs while
reporting its staleness, and still catches an intruder. ⚠ **One fixture leg fired on its
first run and the fixture was the thing at fault** — my synthetic E33 manifest did not declare
the *other* manifest sitting in the same tree, so the walk correctly reported it as added.
Recorded because the walk was right and my fixture was wrong.

## 2. Count surfaces — two-pass, off `T34.PINS`

Order as specced: **pin edits first, collect second, surfaces last.**

- **Pass one, pins:** `tests/test_t70_tree_manifest.py` added (6 tests); `T41`'s
  `tools/verify` population pin moved **9 → 10** with its reason at the site; `tree_manifest.py`
  judged **`none`** for census axis G, in this same commit, under the file's own stated rule —
  line 1 names tree integrity rather than one of the eight spec questions, and the tool returns
  HELD/FIRED rather than a measurement, on `gate_mesh`'s verdict-tool precedent.
- **Pass two, collect**, then **pass three, surfaces:** all **16** pins rewritten by importing
  `T34.PINS` and driving the substitution from the table itself, never a hand list — README.md,
  SHIP_GATE.md, docs/advisor-kickoff.md, site-config.ts, and the two handbook pages. Plus
  **digits-only on the seven translated READMEs**, each verified to carry both counts twice
  with zero stale values remaining. Final: **1002 total / 957 hermetic**, 45 deselected.

### ⚠ The specced two-pass order is necessary and NOT sufficient — a correction to the procedure

*"Pin edits first, collect second, surfaces last"* holds only if **every** pin edit lands
before the collect, and one new file moved **four** pinned populations, three of which the
guard batch could not see:

| pin | moved | found by |
|---|---|---|
| `T41` `tools/verify` population | 9 → 10 | the guard batch |
| `T33` SystemExit ANDON census | 32 / 15 → **35 / 16** | **the full suite** |
| `T62` runnable instrument set | + `verify/tree_manifest.py` | **the full suite** |
| census axis D | contaminated | **the full suite** (idempotency gate) |

**`T62` parametrises over the tuple it pins.** Adding one entry added one test, so the
collected count moved **1001 → 1002 / 957** *after* the surfaces had been written to 1001 —
and all 25 count-surface assertions failed, correctly. A third pass was needed.

**The order that actually works, offered as a correction to the recorded procedure:** land
all pin edits → **run the full suite to discover the pins you did not know about** → collect
→ surfaces → census last. The middle step is the one this close was missing, and the reason
is structural: a guard batch tests the guards you thought of.

⚠ **And my own ordering error, separately:** the dispatch says *census regenerated after all
documents are final*. I emitted it before writing this file, which names tools and
recorded-tree paths, so axis D moved and its idempotency gate fired. The E28 self-reference
family — an arc's own paper contaminating the census's evidence — caught by the gate built
for exactly that. Re-emitted last.

⚠ **`translate-all.mjs` was NOT run.** Translations are the advisor's hands; changing a
numeral inside an already-translated sentence is not generating a translation.

## 3. Census

Re-emitted with **`--committed`** after the documents were final, covering both homes
(`tools/diagnostics` + `tools/verify`). ⚠ **Its ANDON fired first**, on my own new file:
*"axis G has no entry for 1 file(s): tree_manifest.py. A missing judgment must not default to
`none`."* That is the guard doing exactly what it was built for — the judgment was made
deliberately and recorded in the table's comment block, then the census re-ran clean.

## 4. What the arc spent and what it produced

**47 of 60.** The arc ran E-series arms, a 2509 pilot, an anchored recovery sequence, a
corruption discriminator and an un-confounding job.

Measured artifacts of the close, without judgement:

- the arm slate's negative result (branch 4, `(d)` unspent)
- the 2509 route's corruption trigger, closed to the input's quantisation character
- the route's class numbers, un-confounded: pale **2.9×** and dark **2.8×** the recorded
  route's, register C\* **26.99** against **23.77**, reg-IoU **0.9311** with no ControlNet
- four new instrument capabilities committed with their fixtures: `silhouette_masks --depth`
  (T69), `tree_manifest` (T70), and the pale and register instruments parameterised with
  their anchors re-verified after every edit

## 5. Suite and index

**Suite: 1002 passed, 0 failed** (1002 collected / 957 hermetic, 45 artifacts deselected),
read from a complete capture whose `grep -c "^FAILED"` returns 0 in agreement with the summary
line — the cross-check, not the eyeball. Two intermediate readings during this close were
truncated captures whose FAILED count disagreed with their summary (3 against 27 earlier in
the arc; 3 against 25 here); both were discarded and re-run to a controlled file rather than
diagnosed from.

The index pair is rebuilt via `record_build` in a **fresh interpreter** as the terminal
commit, scratch-gate **19/19** first, per the ritual.

## 6. What is not in this document

No verdict on the candidate, the identity, or the register. **The Director's three sheet calls
stand as given, and the close ruling is the advisor's.**
