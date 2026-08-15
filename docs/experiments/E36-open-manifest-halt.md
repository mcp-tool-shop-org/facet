# E36 — open halt: the manifest gate fired on `facet_E35`

**Seat:** executor · **Date:** 2026-08-15 · **Task:** 0, mechanics (zero cloud) ·
**Spend at halt: 0 of 15 cloud jobs — nothing was submitted.**

Premise 7 of the [E36 amendment](E36-route-arms-kickoff.md) — *"`facet_E33/E34/E35` +
the eight subtrees verify 0/0/0 via `tree_manifest`"*, carried as **MEASURED at the E35
close** with the instruction *re-verify at open and close* — **is falsified at open on one
of its four clauses.** Reported here with its evidence; halted per executor rule 3. No
parameter was changed and nothing was re-run.

---

## 1. The four gates at open

| gate | scope | result |
|---|---|---|
| **A** `E33_manifest.json` | `facet_E33` | **HELD** — 116 declared / 116 present, 0/0/0, 835,059,987 bytes; self-reference reported and not counted |
| **B** `E34_manifest.json` | `facet_E34` | **HELD** — 84 / 84, 0/0/0, 177,563,094 against declared 177,563,094 |
| **C** eight protected subtrees | `facet_next`, `facet_E01/E02/E05/E06/E07/E08`, `saltroad_bake_fix` | **HELD** — 7,312 files / 17,072,807,610 bytes, delta **+0 / +0** against the E23 record |
| **D** `E35_manifest.json` | `facet_E35` | **FIRED** — 335 declared / **336 present**, **added 1**, removed 0, changed 0 |

Manifest C reproduces the E35-close per-subtree table to the file: `facet_next` 5,040 ·
`facet_E01` 156 · `facet_E02` 146 · `facet_E05` 129 · `facet_E06` 96 · `facet_E07` 51 ·
`facet_E08` 818 · `saltroad_bake_fix` 876.

The tool exited **1** and its last line was `MANIFEST GATE: FIRED`.

## 2. What was added

```
added: diag/close_manifest_D.json          256 bytes
```

Its entire content, which is the whole finding:

```json
[ { "manifest": "E35_manifest.json", "root": "E:/AI/training/facet_E35",
    "declared": 335, "present": 335, "total_bytes": 284096148,
    "added": [], "removed": [], "changed": [], "held": true,
    "self_reference_stale": null } ]
```

**This file is the E35 close's own manifest-D verification receipt** — the `--out-json`
output of the very walk whose result it records.

## 3. The sequence, from mtimes — the receipt falsified itself by existing

| time (2026-08-14) | event | effect on the census |
|---|---|---|
| 23:45:44 | `diag/close_manifests_AB.json` written — the A/B verify receipt | tree not yet sealed; this file **is declared** in the manifest |
| 23:46:24 | `E35_manifest.json` emitted — **335 files sealed**, `excludes_self: true` | the seal; it declares `close_manifests_AB.json` because that already existed |
| 23:46:35 | `diag/close_manifest_D.json` written — the D verify receipt | **+1 undeclared file, 11 seconds after the seal** |

The receipt asserts `"present": 335, "held": true`. That was true at the instant the walk
ran and false eleven seconds later, **because writing the receipt is what made it false.**
The close's recorded row — *"verified in a second pass: HELD, 0/0/0"* — was accurate when
written; the act of recording it is what moved the count.

A sweep for any post-seal write under `facet_E35` returns exactly two files: the manifest
itself (23:46:24) and this receipt (23:46:35). **Nothing else in the tree moved.**

## 4. The mechanism, at the line

`tools/verify/tree_manifest.py`:

- **the emit path self-guards** — line 118:
  `excl = set(exclude) | {os.path.basename(out).replace(os.sep, "/")}`
- **the verify path does not** — lines 226–227:
  ```python
  if a.out_json:
      json.dump(rows, open(a.out_json, "w"), indent=1)
  ```
  written after the walk, with no check that the destination lies outside the root just
  walked.

The guard exists on one of the tool's two writing paths. The walk behaved exactly as its
docstring specifies — *"The walk honours the flag and nothing else: any OTHER new file is
still `added`, which is what the fixture proves."* **The tool is not what failed; an
invocation wrote its receipt inside the tree it was sealing.**

### The harness does not cover this

`tests/test_t70_tree_manifest.py` has five legs: the selftest runs; it covers both
encodings and all three deltas; it fails when the walk is broken; a missing manifest is an
error not a pass; the ANDON is a `raise` not an `assert`. **None constructs a receipt
written into the verified root.** Asked in the form CLAUDE.md requires — *what would this
look like if the code were wrong in the specific way this check exists to catch* — this
exact contamination passes T70 today.

## 5. What is NOT damaged — measured, because E36's inputs live in this tree

`changed 0` covers all 335 declared files. Checked individually against their declared
sha256, since arm 2 reads them:

| file | declared | actual | |
|---|---|---|---|
| `depth/armclay_1_depth.png` | `c74eaf49a6130078…` | `c74eaf49a6130078…` | **MATCH** |
| `depth/armclay_1_depth_far.png` | `fb822670203fa661…` | `fb822670203fa661…` | **MATCH** |
| `depth/armclay_0_depth.png` | `199abc9abb3ad2cc…` | `199abc9abb3ad2cc…` | **MATCH** |
| `depth/armclay_4_depth.png` | `9e920d21baf8fc86…` | `9e920d21baf8fc86…` | **MATCH** |
| `payloads/payload_s4c_depth_v1.json` | `c48c03a43126c893…` | `c48c03a43126c893…` | **MATCH** |
| `twins/twin_s4c_depth_v1.png` | `0f9bd58635776a9b…` | `0f9bd58635776a9b…` | **MATCH** |

**Premise 3 — the authored view-1 depth map — is byte-intact.** The fired condition is one
added 256-byte JSON receipt, not a modification of anything E36 reads.

## 6. This is the E28 self-reference family, and the sibling was swept while this was not

CLAUDE.md states the law and this is a new site of it: *"An instrument that lives inside
its own population must be checked against itself on every axis, each time — and one clean
check is not clearance."* The remedy it lists as having held — *"exclude the instrument's
own derived artifacts from its evidence by construction"* — is precisely the guard the emit
path has and the verify path lacks.

The same close recorded this family firing on its census (axis D contaminated by the arc's
own report) and repaired it by re-emitting last. **The receipt path is the same shape one
layer down, in the same session, and was not swept when its sibling was found** — which is
the standing instruction *when you fix a root cause, find its other consumers.*

## 7. Halted — dispositions named, none chosen

Executor rule 3: report the gate with its evidence and halt. The disposition is not mine
and I have not taken one. What each would require, factually:

- **Re-emit `E35_manifest.json` at 336** — records the receipt as part of the tree. Changes
  a closed arc's seal after the fact.
- **Delete the receipt** — restores 335. Destroys a close artifact; forbidden to me on a
  protected tree without a word.
- **Amend the `excludes_self` contract** to cover named receipts — a tool change, and by
  this repo's standing rule it rides with its tests in the same commit.
- **Rule the firing characterized and proceed** — premise 7 stands falsified as written,
  with the reason recorded and E36's inputs measured intact.

⚠ **I did not re-run the gate, adjust it, or narrow it.** The one move this record calls
always wrong is retuning a condition while looking at the result it judges.

**Awaiting the ruling. Zero cloud spent; the blind bands are unwritten and unsealed, so
nothing about the arms has been seen or set.**

---

## 8. RESOLVED — the Director's ruling, 2026-08-15: delete the receipt

He ruled the second disposition. Executed in this order:

1. **The bytes recorded before the delete** — `sha256
   C2E97E11523CA88CB6CC7EF0C8DB60080015F3000A6D90999976D2A67966CA1D`, 256 bytes. Its
   complete content is transcribed in §2 above, in a document committed at `842f734`
   **before** the file was touched, so nothing about it is lost. It is derived output of a
   committed, re-runnable walk; re-deriving it costs one command.
2. **Deleted** — `diag/close_manifest_D.json` removed from `facet_E35`. Nothing else in any
   protected tree was touched.
3. **Re-verified** — `MANIFEST GATE: HELD`, exit **0**:

| gate | result after |
|---|---|
| A `facet_E33` | HELD — 116 / 116, 0/0/0 |
| B `facet_E34` | HELD — 84 / 84, 0/0/0 |
| **D `facet_E35`** | **HELD — 335 / 335, 0/0/0, 284,096,148 against declared 284,096,148** |

**Premise 7 holds at open.** The existing seal was made true rather than rewritten — the
manifest of a closed arc still declares exactly what that arc closed with.

⚠ **The re-verification wrote its own `--out-json` receipt OUTSIDE every protected tree**
(to the session scratchpad). That is the correct invocation and it is the whole lesson of
this halt: the destination of a verify receipt must not be the root being verified.

### Still open, and deliberately not taken here

The **mechanism** is unrepaired — `tree_manifest.py`'s verify path still accepts an
`--out-json` destination inside the root it walks, and T70 still has no leg that fires on
it. This halt removed the instance; the class remains. That is a tool change carrying its
own tests by the standing rule, and it was not folded into an arc whose subject is two
route arms. **Named here so it is not lost:** the guard is one comparison against the
walked root, and its fixture is a receipt written into a synthetic tree.
