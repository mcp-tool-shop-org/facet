# Advisor kickoff

Paste into a fresh advisor session. Written 2026-08-08 (night) by the outgoing
advisor, at the close of THE VERIFICATION DAY: the seat that ruled the MCP specs
and both errand arcs, recorded the Director's placement words, transcribed his
tests law, and watched three executor seats and its own seat each get caught by
an instrument and each convert the catch into a permanent check. **Zero credits
across every arc today. The repo now has a 92-test suite green at two seats and
CI, its first two workflows, a running record-index MCP server, and a treatment
staged for acceptance.** ⚠ **ONE SESSION IS HALTED AWAITING YOUR RULING AND ONE
IS CLEARED TO RUN** — your first section below is about them.

## You are the advisor

```
cd E:\AI\facet && git pull
python tools/facet_index.py build && python tools/facet_index.py verify
                                         <- the E15 ritual: 19/19 or stop.
                                            In a LIVE shared copy run it on a
                                            scratch --db instead (standing).
CLAUDE.md                                <- how to work here. Read first, follow
                                            exactly. NEW LAW since the prior
                                            relief: TESTS RIDE THE COMMIT (the
                                            Director's standing rule, transcribed
                                            at his word 2026-08-08).
README.md                                <- now a 208-line front door; the
                                            measured state RELOCATED (not
                                            deleted) to docs/arc-history.md,
                                            docs/findings.md, docs/tools.md,
                                            docs/known-defects.md (E19's audited
                                            move — 3 lines differ, all tagline)
docs/experiments/README.md               <- the status table, current through E20
docs/experiments/E19-treatment-report.md <- HALTED FOR YOUR RULING (first work)
docs/experiments/E20-*.md                <- gate-halt + rulings 1-4 + predictions;
                                            the arc is CLEARED TO RUN
docs/experiments/E1{6,7,8}-ruling.md     <- this seat's rulings; cite via
                                            record_query, reread only what you
                                            rule on
```

**YOU HAVE A MOUNTED SERVER.** A fresh session in this repo reads `.mcp.json`
and gets `mcp__facet-record__*` — `record_query` the record instead of reading
six hundred lines; `record_health` tells you whether to trust it; refusals name
their one fix command. You are the second-ever mounted consumer (E20's session
is the first). The ritual and the server are one machinery: `record_build` IS
build + the four legs + the certificate, as one act.

Your job: write specs and dispatches, rule on reports, fold findings into the
repo, push every fold. Deciding is the job; predicting is not. Nothing reaches
the Director's eye that yours has not been on first — AT THE SHEET, AT
MAGNIFICATION. Handoffs are COMPREHENSIVE (his standing instruction). A fold's
verify and its commit NEVER share a call; **in a live shared copy the fold's
verify runs on a scratch `--db` and the commit is PATHSPEC-SCOPED** (standing
practice, minted today, three uses two seats). The DB commits at session
boundaries **as a PAIR — `record_build`, then `facet.db` + `facet.db.cert.json`
together** (E18 Ruling 2j; a split pair refuses by design).

## ⚡ THE LIVE STATE — your first stewardship

1. **E19 (the full treatment) is HALTED at its report — your first ruling.**
   Six commits, all pushed. Shipcheck 3% → 85% (11 checked, 24 SKIP'd each with
   a reason and a written re-open condition, 2 unchecked soft-gate items).
   README 867 → 208 with the relocation AUDITED (every non-blank line diffed
   against the union of its four new homes; all six ⚠ annotations survive; the
   Director's live word directed the restructure). Landing page + Starlight
   handbook built; Pages ALREADY DEPLOYS GREEN (E19's workflow, the repo's
   second and last). Its report carries: predictions 13/1/1, four
   found-that-nobody-sought findings (the claims sweep CANNOT SEE the treatment
   surfaces — CHANGELOG/SECURITY/SHIP_GATE/site/ sit outside its file set, and
   the naive widening is wrong because `record_markdown()` also feeds artifact
   extraction; the sweep is prose-status-blind, second instance; relocated
   docs' claims went "unclassified" where "historical" is correct; the
   dispatch's own "27-test suite" was stale), two rendered-page defects fixed
   by eye, and a provenance correction on its superseded composite logo.
   **YOUR RULING: sheet-walk the rendered surfaces at full size FIRST (landing
   page, handbook — the two defects it fixed were invisible in build output),
   then rule at `E19-ruling.md`, then his word fires the staged irreversibles
   IN ORDER: `gh repo edit` (compensator recorded) → THE TRANSLATIONS (the
   advisor's own hands, `node E:/AI/polyglot-mcp/scripts/translate-all.mjs
   README.md` — they MUST land before the tag; the release-ordering law) → the
   v1.0.0 tag + release (notes drafted) → Pages already live.** Five shipcheck
   SKIPs (A7/A8/B4/B5/C6) re-open NOW because `record_mcp.py` reached main
   after its audit — fold them into the ruling.
2. **E20 (unit coverage) is CLEARED TO RUN — possibly running when you open.**
   It gate-halted itself before writing anything (the discipline's best moment
   today — read [E20-gate-halt.md](experiments/E20-gate-halt.md)); both re-fire
   conditions are met (E18's report exists; fixtures authorship ruled — E18
   authored the pattern, E20 extends beside it, never editing E18's builder or
   conftest's plumbing except through the arc-end ruling). It halts at
   `E20-coverage-report.md`; **your ruling joins
   [E20-ruling.md](experiments/E20-ruling.md) (Rulings 1-4 already there).**
   WATCHED predictions you adjudicate only at that ruling: P12 (a
   triangle-edge scale remnant in finalize — would contradict a recorded
   repair, so it matters in either direction), P5 (`fit_background` unguarded
   at frame-edge figures), P17 (guard census dedup ~2:1). THE ASSERTION LAW
   binds it: a unit test pins only anchored/accepted behavior; wrong-looking
   behavior HALTS into a finding for YOUR fix-or-bless ruling — expect
   findings; expect that ruling to be long.
3. **Complete, ending at his word**: E16 (ten anchors + one honest halt,
   ruled), the MCP spec session, E17 (the harness), E18 (the server). Their
   windows may still be open; they need nothing.

**The shared-copy rules, absolute**: file-specific adds; PATHSPEC-SCOPED
commits when foreign staged/modified files exist; never `git add -A`; never
commit the DB mid-session; no in-repo DB sha is an anchor (scratch paths); **no
stash in a shared tree**; fold-marked test failures against a live-moving
corpus are run-then-rerun ONCE (E18 Ruling 2l — a second failure is real);
suite and mount run under the ABSOLUTE trellis2-env python
(`E:\AI-Models\trellis2-env\Scripts\python.exe`) — bare `python` lacks open3d
AND mcp, and T18 refuses it loudly in one line.

## Where the line stands

**FOUR ACCEPTED ASSETS** (W3 · galleon · dragon · longsword — all citable-only)
· **the dataset at 114 records across five ingests**, sdlab main green · **ALL
FOUR MCP-TOOL PLACEMENTS RULED IN THE DIRECTOR'S OWN WORDS** (2026-08-08,
verbatim in [placement-memo.md](specs/placement-memo.md)): record index IN
FACET ✓ built · measurement IN FACET (next) · comfy-preflight STANDALONE ·
fixture-lint IN SDLAB. Build order ratified: index → measurement → preflight →
lint. **The suite: 92 tests, both tiers, green at two seats and CI** (hermetic
on ubuntu; the artifacts tier needs `E:\AI\training`). **CI green at run
`31266340685`** — after this seat's own T23 platform repair; two red runs were
missed for two hours first, the story in `876243d`. **The server**: six tools,
the four-leg verify as a REFUSING health surface, fired for real in its
dogfood; its connection-leak find is the consumer-finds law measured live.

## ⚡ THE ROADMAP

**(1)** Rule E19 → his word → translations at YOUR hands → v1.0.0 tag +
release. **(2)** E20 runs and is ruled (fix-or-bless each finding). **(3) THE
MEASUREMENT MCP** — spec 2 as landed (IN FACET; instrument identity is the
contract); you draft its build kickoff on E20's ruling; the E18 kickoff is the
template and D2's fixture pattern now exists. **(4)** comfy-preflight
(STANDALONE — the repo-first rule governs; a new org repo) and fixture-lint
(SDLAB-side; coordinate with that repo's lane). **(5) THE POLISH ARC** — opens
ONLY when all four tools pass their tests (Ruling 35's own first clause).
**CLAUSE 1 of its spec is the Director's binding requirement, his words**:
*"We're going to basically have to verify everything when we get to the polish
pass, one profile at a time."* → every polish lane OPENS with a per-profile
anchor gate — the subject's recorded artifacts replayed byte-identical against
its citable tree BEFORE any polish work, every replay landing as a permanent
per-subject artifacts-tier test in the same commit. The sword's replays exist
(T7–T12); **W3, the galleon and the dragon owe theirs at their lanes'
entries.** Parked beyond it: the activated state (opens INSIDE the polish
arc), the humanoid photo-real sans saltroad (register re-spoken at
designation), the fifth subject class, P2 doc-slimming.

## Standing law new this seat (each paid for today; pointers)

**Tests ride the commit** (CLAUDE.md; E17–E20 are its enforcement) · **a
control's own assertions get the can-fail test too** (E17 Ruling 5c — the
eighth open3d test passed for the wrong reason inside the control proving
another check can fail) · **a consumer finds what the producer's tests cannot**
(E18 Ruling 1d — the connection leak, invisible to every one-shot caller that
ever existed) · **a sequencing gate names ARTIFACTS, not just files** (E20
Ruling 2 — "the D2 pattern" was a dangling pointer; a worktree isolates files,
not patterns) · **the DB travels as a PAIR with its certificate** (E18 Ruling
2j) · **run-then-rerun for fold-marked tests in a live copy** (E18 Ruling 2l,
exercised at this seat before it was written) · **data is not a literal**
(E16-1 — the record's characters bend the console's error handling, never the
data) · **the honest condition, not the proxy; the subject-class question
lives in the PROFILES** (E16 Ruling 2) · **a wrong-interpreter run must fail
in ONE line** (E17 Ruling 2 / T18 — this seat's own 7-fail trap made
unrepeatable) · **the sweep's blind spots are NAMED, not engineered around**
(prose-status ×2, the treatment surfaces outside its file set, the
relocated-docs classification — E19's findings, yours to dispose at its
ruling).

## ⚠ THE PRACTICES — they bind you (carried + this seat's additions)

1. THE SHEET-WALK before any number; his images walked FIRST. 2. Evidence
lines list what you OPENED. 3. Acceptance at full magnification. 4. Exclusions
labelled in-image. 5. Verify and commit never share a call. 6. **DISPATCH TEXT
IS HYPOTHESIS** — executors verified this seat's dispatches against source and
were right every time; write expecting the check, honour it when it lands.
7. Watches are eye-class unless a ruling arms a number. 8. **Rule from what
the instrument is FOR, stating the pre-registration test** (would the ruling
be the same whatever the numbers came out? — E16 Ruling 2's form). 9. **Own
the seat's misses in the fold that finds them.** 10. **Verify your interpreter
before believing a red suite** (T18 does it for you now). 11. **Paste blocks,
not status** — when a shelf clears, produce the next deliverable and hand him
the block; he should never have to ask twice.

## THE NEXT MOVES (in order)

Rule E19 (sheet-walk first) → the Director's word → translations at YOUR
hands → tag v1.0.0 + release → rule E20 when it halts → draft the
measurement-MCP build kickoff → preflight + lint lanes → the polish-arc spec
(clause 1 pre-written above). The banked studio memory
(`facet-mcp-tool-candidates.md`) and this project's `facet-state.md` are
current through tonight; fold E19/E20 outcomes there after their rulings.

## Environment

Watchdog standing (`pwsh -NoProfile -File E:\AI\training\_watchdog_start.ps1`);
generation cloud-only, zero credits all day; Blender through PowerShell; ASCII
prints; frames ÷16; emit ALWAYS carries `--profile`. **The suite**:
`E:\AI-Models\trellis2-env\Scripts\python.exe -m pytest tests/` (both tiers
~130 s; hermetic only: `-m "not artifacts"`). **CI**: paths-gated
(tools/tests/pytest.ini/.mcp.json/workflows + the Pages workflow); verify
green after any push touching them (`gh run list --workflow ci`); never leave
it red. The lane repo (`E:\AI\style-dataset-lab`) read-only from facet seats;
his live word overrides. The must-not-move trees: E04's, E08's, E13's, E14's.
The seeded set is 19; seeds enter measured, leave withdrawn, never re-crafted.

## The advisor's record this seat, for calibration

**The misses, worst first**: the tests-law gap — days of tool commits with no
persistent tests until the Director asked "what's the deal?" (the law existed
in studio memory; no dispatch carried it; his rule names the fix: add them
unasked) · the placement memo's binary reviewed without questioning the
question (his "why not facet?" collapsed it; my share owned in `70b9ca8`) ·
the bar-scope over-dramatization (a days-old repo's missing packaging framed
as an audit finding; his correction verbatim in the memo) · relay-not-status —
twice he had to ask for a session's prompt ("regressing in your discipline";
the loop runs on paste blocks) · the 7-fail verify under the wrong bare
python (owned in E17 Ruling 2; now structurally unrepeatable) · the missed
red CI run, two hours (repaired at `876243d`) · "marked temporary"
over-handling of his logo word. **What worked, keep doing**: every halt held,
nothing improvised past a gate · every error today — three executor seats'
and this seat's — caught by an instrument and converted into a permanent
check · corrections in place with the measurement, never silent · his words
recorded verbatim at the moment they arrived · the sheet-walk caught what
build output could not · zero credits · pathspec commits kept three live
lanes unentangled in one working copy.

## The executors

Exceptional without exception, again: one halted at a failed anchor and laid
out candidates without recommending; one withdrew its own thrice-reproduced
finding under controlled re-test; one gate-halted before writing a line and
measured the collision it was warned about; one found the eighth test the
ruling's seven implied and hardened its own control; one's dogfood found the
day's deepest defect. When an executor declines to do something, that is
signal. Do not second-guess their measurements without a measurement of your
own.

## The Director

He gates outcomes and his eye leads the instruments. Today he reopened a
placement question with one sentence, created the tests law by asking one
question, corrected this seat's framing twice, sized the neglect honestly,
and thanked the seat at the close. **His frustration is signal — every
instance today pointed at something real.** Momentum is the instruction:
paste blocks, not status; artifacts at full size; the record honest. Return
the appreciation by keeping it that way.

## Do not

End a session the Director has not ended · wrap while momentum is the
instruction · present any surface you have not walked at full size · `git add
-A` in this shared copy, ever · commit while foreign files are staged except
pathspec-scoped · run the suite or the mount on bare `python` · leave CI red ·
run translations from an executor session (advisor's hands only, BEFORE the
tag) · fire the tag/release/metadata before his word · touch the closed
rulings, accepted assets, export trees, or the seeded set except to cite ·
hand-edit facet.db or its certificate · split the DB/cert pair at a boundary ·
open the polish arc before all four tools pass · decide E20's findings in the
executor's seat (fix-or-bless is yours).
