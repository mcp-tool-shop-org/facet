# E73 — the v0.8.1 treatment, and the identity scrub that preceded it

**Type:** treatment report. There is no spec, and that is stated rather than papered over:
this ran as a Director-directed treatment ("give facet the full treatment and then publish
with a patch bump"), not as a dispatched experiment. It is recorded because two of its
actions **changed bytes a future session might replay against**, and a record that only
holds experiments cannot warn anyone about those.

**Date:** 2026-09-22 · **Version:** 0.8.0 → 0.8.1

---

## What was actually done, in order

| phase | action | evidence |
|---|---|---|
| 0 | identity scrub over the git-tracked tree | scan `RESULT HIT 75` → `RESULT CLEAN` |
| 0 | `shipcheck audit` | 1 unchecked → **28 checked / 0 unchecked / 9 skipped, 100%** |
| 0 | full suite | **1376 passed** in 875.28 s, exit 0 |
| 1 | README: the sixth subject, the two contracts, clause 7, two interpreters | `README.md` |
| 1 | translations regenerated **before** publish | seven `README.*.md` |
| 2–3 | handbook: new page `props-and-rigs`, synced, site built | `dist/pagefind/` present, 8 pages |
| 4 | GitHub topics `+rigging +gltf` | `gh repo view` |
| 5 | repo-knowledge: re-scan, two stale notes replaced, one convention added, one relationship added | `rk show facet` |
| — | pre-tag re-count | 1376 total / 1319 hermetic / 57 deselected |
| — | index rebuild + four-leg verify + claims sweep | VERIFY PASSED, **0 STALE** |

---

## ⚠ The thing a future session needs to know: recorded bytes changed

The identity scrub rewrote operator-identifying strings across **31 files**. Almost all of
it is prose. **Two consequences are not prose:**

**1. `E08-anchor-workflow-api.json` no longer has its original bytes.** The `lora_name`
value's first segment is the operator's Hugging Face namespace, and it was replaced with
`<operator>`. The file is an *anchor*, and this repo's own law is that an artifact whose
bytes are the contract must not drift silently — so it is named here rather than left to be
discovered.

Nothing in the tree pins that file's sha256 (checked: no test, no report cites one), so no
gate fired and none was suppressed. The practical loss is bounded: the LoRA it names lives
in a **private** repository under that namespace, so the anchor was never replayable by
anyone outside this rig, and the E08 documents already record that this import path is
redundant and has since vanished. **To replay it, restore the namespace by hand from the
off-repo identity file.**

**2. Absolute home paths in reports are now portable forms** — `%USERPROFILE%\…` and
`$HOME/…` rather than one machine's paths. Recorded *command lines* in reports therefore no
longer copy-paste verbatim on the rig that produced them. They still name the same
locations.

**What was NOT touched:** no measurement, no number, no verdict, no tool logic. The two
`tools/` files the scrub reached (`brush_cloud_step.py`, `record_mcp.py`) changed **only in
comments**, verified by reading the diff rather than by assuming it, and the full suite
passed afterwards.

---

## Two errors made in this session, kept per the corrections rule

**The site build was declared broken at HEAD, and it was not.** A local `npm run build`
failed Starlight config validation, the config was "fixed", and a CHANGELOG line was written
saying v0.8.0 shipped a landing page that did not build. All of it was wrong: the local
`node_modules` held **starlight 0.37.7** while the lockfile pins **0.42.1**, and 0.37.7 is
the version that rejects the nested `{autogenerate}` shape. CI's Pages deploy had succeeded
on the commit in question. The config change was reverted, `npm ci` installed the locked
tree, and the **original** config built clean — 8 pages, pagefind index at `dist/pagefind/`.
The false CHANGELOG claim was removed before it left the machine.

*The general form is one this repo already has a law for: a conclusion read off a stale
instrument is not a measurement. A `node_modules` directory is an instrument.*

**An experiment count was "corrected" against a worse instrument.** A hand-written regex
over the status table returned 70 where the README says seventy-two. T34's fourth leg
already counts that table and gates every surface against it, and it was green — so the
regex was the thing that was wrong, and the README was right. Nothing was changed. *Ask what
already measures this before writing something that measures it worse.*

---

## What this treatment does NOT claim

- **That the Drell arc has a record.** The tools, canon documents and tests that arc
  produced are in the repo with their measurements; the arc itself has **no numbered
  experiment**, because it had no spec written before the work. A spec written afterwards
  would be a fabrication, so none was written. The finding — four causes eliminated, the
  discriminator unidentified — lives in `canon/BASE-FIGURE.md` where it was recorded as it
  happened.
- **That the historical tags are clean.** The scrub covers the working tree and everything
  published from `main` forward. **A later commit does not unpublish a tag**, and this repo
  has eight of them.
- **That anything about the assets improved.** This treatment moved documentation,
  packaging and metadata. No asset was re-baked, re-brushed or re-judged.

---

## Addendum — a third error, made at the tag itself

`v0.8.1` was tagged and pushed **without `.github/release-notes-v0.8.1.md`**, which
`release.yml` passes to `gh release create` as `--notes-file`. A tag without one fails at
that step.

The document that warns about this is the one this session had already opened:
`docs/advisor-kickoff.md`'s release row records that **the first v0.8.0 tag failed the same
way**, that the file is REQUIRED, and that nine prior releases each carry one. The tag went
out before that line was read. *Reading the handoff is not the same as reading the row you
are about to depend on.*

**Nothing irreversible ran.** `gh release create` is step 10 of the publish job and both
registries are steps 11 and 14, so the failure sits ahead of every publish. The run was
cancelled while the binaries were still building; `gh release list` confirmed no `v0.8.1`
release existed and neither PyPI nor npm had been touched. The notes file was written,
committed, and the tag force-moved onto that commit rather than a `v0.8.2` being cut for a
missing file — the same remedy the v0.8.0 row records.

**Why this is worth a paragraph rather than a line.** The workflow's ordering is what made
the mistake cheap: the cheapest check in the job runs before the two expensive irreversible
ones. That is not luck, it is the shape the file was written in, and it is the argument for
putting a gate in front of a publish rather than after it.

**What would have caught it earlier:** nothing in the repo. `release.yml` names the file at
run time and no test asserts that a notes file exists for the version in `package.json`.
That is a gap, it is named here rather than fixed in the same breath, and the fix is one
leg in `test_t27_packaging_shape.py` — which already reads the release workflow and already
checks the four version declarations agree.
