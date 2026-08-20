# Grok consult #23 — the advisor shipped five defects of one shape in one session, and the outside channel found the two that were still live

**2026-08-19, facet advisor seat.** Twenty-two briefs, twenty-two chips held. **#23's chip
held too, and it was the highest-value one of the run: it named a live defect in a spec a
seat was executing at that moment.**

⚠ **This round is recorded differently from the twenty-two before it, and the reason is the
failure it documents.** The advisor ran the entire session — two dispatched seats, an E71
fold, an E72 spec, a push — **without opening this channel once**, and was asked why. The
channel is named in the advisor kickoff as one of four things that held this project
together, the repo carries twenty-two prior briefs, and `~/.grok/bin/grok -p` takes a
single-turn prompt headlessly, so there was never even a paste-block dependency. Worse: the
repo's own **EXTERNAL_VERIFIER** standard says no model verifies its own output and the
verifier must be a different family — and the advisor **scored its own E71 and E72 specs
against that standard, awarding itself 2/3, while never using the external verifier that
exists.** A self-assessed external-verifier score is the standard's own defect, written by
the person the standard exists to check.

## The brief that was sent

Four questions: whether E71's scoped fill arm was recoverable or pointless; which of two
face-banding remedies to take; which side of a corpus-definition split to repair; and — the
one that mattered — *"three advisor defects shipped this session and a Sonnet seat caught all
three. Find the fourth."* Full text as sent is in the session record; the four questions are
restated with their answers below.

## The chip — PASSED, and verified by running it

Nominated: *`texpass_iter.py emit` with the flags E72 actually writes (`--state --prep --glb
--yaw --el`, no `--profile`, no `--aspect`) ANDONs and exits 1.*

Verified at source, all four parts:

| claim | site | verdict |
|---|---|---|
| `emit` ANDONs without a frame | `texpass_iter.py:133` | **holds** |
| the ANDON is narrowed to `mode == "emit"`, so **`selftest` skips it** | same line | **holds** |
| `brush_cloud_step.py graph --profile` is `required=True` | `brush_cloud_step.py:156` | **holds** |
| `e70_build_sheet.py` is not reusable — hardcoded `ROOT`, two columns, SHA literals | `:14` | **holds** |

**Twenty-three for twenty-three.**

## The fourth defect — and it was LIVE

E72's Stage 0 step 3 and Stage 1 step 1 both invoke `texpass_iter.py emit` **without
`--profile` or `--aspect`**. A1's measured frame is **576x1024**; the tool's default is W3's
**752x1024**. Neither line can run as written, and the seat executing Stage 0 was heading
straight at it.

**The trap inside the trap**, which is why this is worth a document: the ANDON is narrowed to
`mode == "emit"` on purpose (`commit` reads W/H from the emitted `cam.json` and gating it
would fire on correct work). **`selftest` therefore skips the ANDON entirely and emits at the
752 default.** Stage 0's hard gate — the thing standing between the arc and a paid
generation — would have **passed on W3's frame while the real stroke ran on A1's.** A green
gate that never saw the thing it gates.

## The FIFTH — the advisor's own correction re-armed the trap

The advisor steered the seat to *prefer `--profile profiles/a1.json` over `--aspect`*. The
channel caught that too, before the seat acted on it:

```
texpass_iter.py:132-133
_aspect_explicit = any(a == "--aspect" or a.startswith("--aspect=") for a in _argv)
if args.mode == "emit" and args.profile is None and not _aspect_explicit:
```

Passing `--profile` makes `args.profile is None` **false**, so **the ANDON goes quiet**. The
frame is then read at `:142` from `args.aspect`, which `bind()` overwrites **only if the
profile carries a block for this tool**. `profiles/a1.json`'s `tools` keys are exactly
`['verify/turn_render.py', 'silhouette_masks.py', 'restylize_views.py']` — **no
`texpass_iter.py`**; its `576,1024` sits on `silhouette_masks`, which `bind()` never reads
here. So the documented cure silently re-opens the documented defect, on exactly the subject
whose profile is incomplete.

**That is a new law and it is now in CLAUDE.md**: an ANDON that checks a source was NAMED is
satisfied without the value ever ARRIVING, and the proxy fails *precisely when you need the
guard* — a complete profile would have supplied the frame anyway.

**E14's guard is NOT retuned in this arc** (Director, 2026-08-19). The law is recorded, the
live invocations carry `--aspect 576,1024` explicitly, and changing that construction is a
separate sitting.

## Steer sent to the live seat

`--aspect 576,1024` on **every** `emit` **and on `selftest`**; `--profile` for
`brush_cloud_step.py graph` only, where it is identity/provenance and **not a frame**; the
**verbatim argv** reported for every emit and the selftest rather than a description of it;
and any emit or selftest already run unframed declared **void** rather than quietly re-run
over. `e70_build_sheet.py` recorded as a new script for a three-column sheet, not a reuse.

## Q1 — the scoped fill arm: NOT pointless

Ruled: the repair (full `holes.png` for a correct source pool, then restore unreachable
texels to 107) is right, and **Amendment 1 was wrong about the source pool, not about the
population to grade.** Restoring grey is worth wanting on three counts: `styled_mask` /
`holes.png` stay honest, so a later elevated camera cannot mistake a 3D smear for paint;
provenance keeps unseen surface as the declared constant rather than a neighbour walk; and
**57% of valid texels no eye-level camera can see** — filling them changes the approved atlas
in a way no sheet can convict. If `__reachable__` is right, eight-view renders of Arm F and
of (full-holes fill + restore grey) should match while the **atlases will not**. Grade the
58,346. **Adopt neither arm this sitting.**

## Q2 — the face bands

**Do not ship blend-everywhere.** Vest and shirt edges are supposed to be sharp; softening the
whole figure to fix UV-owner steps on the cheeks is the compositor family. `sumW`/`sumWC` at
`project_twins.py:934-935` do accumulate a weighted average and
`facet_E69\bake\atlas_widescope_blend.png` is on disk from the same run — **put it in front of
the Director as a look, not as doctrine.** Free, and it can fail.

**Front-owns-the-head-band is the cheap correct shape for the face**, because the band already
exists as a first-class region (`--head-facing-min`, `--head-edge-dist`, the crop rect). **What
breaks is the band's own boundary — jaw, hairline, collar: vertical cheek stripes traded for a
ring at the crop. Predict that and sheet the jaw.** Three crops, one sitting: winner-take-all
(approved) | blend atlas | head-band-front-owned. His eye. **Neither is stroke one; styled is
frozen.**

## Q3 — the corpus split

`conventions.json` is wrong to list three of five. **Declare `profiles/a1.json` and
`profiles/prop.json`** — a1 is the approved character, and leg 0 cannot see
present-but-undeclared, which is why prop moved silently. **Do not stop the MCP server adding
`PROFILE_FILES`**: profiles are decisions. The library's `corpus_manifest` walking
markdown-only is the narrower, stale definition; **unify it onto the server's list (markdown +
declared profiles), then declare all five.** Own commit, own count pins. **Not E72.**

## What this round costs the advisor's calibration

Five defects of one shape in one session — *name the file, open the file* — of which the
first three were caught by a Sonnet seat **after** it had spent its time, and the last two by
this channel **before** anything was spent. The fifth was in a correction to the fourth.
Recorded here rather than in a summary, because the session that reads this next needs to
know which parts of today's specs to distrust: **E71 Amendments 1-4 and E72's Stage 0/1
invocations were all written by a seat that named tools without opening them.**
