# E62 report — the schema patch: depends_on, the collision law, unavailable as a convention

Charter: [E62-schema-patch-kickoff.md](E62-schema-patch-kickoff.md). The charter's item 2
was corrected in place by the advisor mid-flight, commit `c3da18e`, before any code in
this arc was written — the corrected two-branch (M/D) form is what this report and its
implementation follow throughout; nothing here was written against the defective first
landing.

Working tree for logs/scratch: `E:\AI\training\facet_E62\`. This is a zero-spend
schema/tool patch — no generation, no cloud call, no image compared. Repo edits land
directly in `E:\AI\facet\`.

No word in this report is `verified`, `shipped`, `works`, `decisive`, `validated`, or
`proven`. Nothing here is ranked. The Director's eye chooses; this report gives
measurements and transcripts.

---

## Premises vs measured

| premise | status |
|---|---|
| The advisor's steer (c3da18e) landed before any code in this arc was written | measured true — charter re-read in full immediately on receipt, before any Edit/Write call |
| The SLEEVE matcher (`\bsleeve(?!less)\b`) fires on none of A1's licensed phrases | measured true, independently reconfirmed (39 licensed phrases, 0 matches) — matches the advisor's own spec-correction-time measurement exactly |
| The SLEEVE matcher, as a `\b`-bounded pattern, matches the plural "sleeves" the same way it matches singular "sleeve" | measured **false** — caught building the first synthetic Branch M fixture (see "A genuine catch" below) |
| Adding `depends_on` data to A1 would not disturb `canon_gate.census()`'s occupancy/ratified numbers | measured true — census output byte-identical, git-stash-verified against true HEAD |
| A1's own `canon_compose.selftest()` calls that use the bare `garment_join` default would start refusing once A1 carries `depends_on` data | measured true, and treated as the intended consequence (fence 1a working), not a defect — four call sites updated to pass `garment_join="over"` explicitly, each with its own reason unrelated to the fence-1 concern documented in place |
| Zero new pytest-collected test functions keeps T34 green without touching any of its pinned surfaces | measured true — `pytest --collect-only` reports exactly 1342 both before and after, T34 52/52 both before and after |
| `docs/experiments/README.md`'s status table is advisor/fold territory, not executor territory | measured true — E61's own row there is written in the advisor's/fold's voice ("the advisor's table", correction language), confirming the pattern; no E62 row added by this seat |

---

## Item 1 — `depends_on` (fence 1)

### Schema (canon_gate.py)

`_validate_depends_on(doc, occ_ids)` — a surface row (or joint) may carry
`depends_on: [<parent occupant id>]`. Refuses (`raise Andon`, never `assert`) when a
parent id names no occupant declared anywhere in the doc, or when a row depends on its
own occupant. Checked on both surfaces and joints because the charter's schema line
names both locations; only surfaces carry real data in this arc (A1's two vest rows) —
a joint's `depends_on` is licensed by the validator and consulted by nothing, matching
this repo's own "licensed, never required" shape applied to a schema location rather
than a word, stated explicitly in the function's own docstring so a future reader does
not have to infer it.

`depends_on_pairs(doc)` — every edge as a `frozenset({child_id, parent_id})`, collapsed
across every surface a shared occupant sits on (N1 sits on both `vest_torso` and
`vest_skirt`; both declare the same edge, which collapses to one).

### Canon data (canon/a1.surfaces.json) — DRAFT, UNRATIFIED

`vest_torso` and `vest_skirt` (occupant N1, the vest) gain `depends_on: ["N2"]` (N2 is
the shirt). **This is drafted canon data, not ratified.** Marked inline, per-row, dated
2026-08-18, attributed to this executor seat, explicitly pending the Director's word at
the fold — matching the standing this arc's charter assigns depends_on rows. Quoting the
added note in full (vest_torso):

> DEPENDS_ON DRAFTED 2026-08-18 (E62, schema patch executor seat) - DRAFT CANON,
> UNRATIFIED, pending the Director's word at the fold: depends_on: ["N2"] spells the
> vest-over-shirt layering as a parented relation rather than more prose in N1. [...]

### Composer (canon_compose.py)

`_refuse_if_and_joins_a_dependent_pair(doc, composed_text)` — reads
`canon_gate.depends_on_pairs(doc)`, resolves each edge to its two occupants' *current*
phrases via `named_occupants()` (honest against a `with_occupant_phrase`-modified doc
too), and refuses if the composed text contains either phrase directly adjacent to
`" and "` the other (case-insensitive, both orders — an exact two-phrase substring test,
not a bare `"and"` search, which would fire on a phrase's own internal "and", e.g.
"hands empty and open"). Called at **both** of `compose()`'s return points (flat's early
return and the grouped/consolidated final join) so the rule is checked on every form's
actual output rather than assumed safe for forms that structurally shouldn't need it.

**Load-bearing consequence, measured and documented in place, not glossed over:** once
A1's canon carries the depends_on edge, `compose(doc, form="grouped")` with **no**
`garment_join` argument (the bare default, which has always been `"and"`) now refuses.
`canon_compose.selftest()`'s own four call sites that relied on that bare default
(`p_front`, `p_rear`, `p_joint`, `p_pre`) needed `garment_join="over"` added explicitly;
each site's own test purpose (face-dropping across views, joint-phrase emission,
occupant-phrase override) is unrelated to the garment connector and unaffected by the
switch — confirmed by re-running `selftest()` clean after the change (below).

### Can-fail legs, all three REQUIRED by the charter, all against A1's REAL patched canon

Added to `canon_compose.selftest()`, no synthetic fixture — the charter's own words name
the concrete case, and A1's real (patched) data exercises all three legs directly:

- **(a)** `compose(doc, view="front", form="grouped")` — bare default, `garment_join`
  unspecified (`"and"`) — must refuse, naming the coordination. **REFUSES**, message
  contains `"depends_on pair coordinated with"`.
- **(b)** The flat form (`p_flat`, already computed earlier in `selftest()`) must contain
  **both** N1's and N2's phrases with **no** `" and "` directly between them in either
  order. **HOLDS** — flat form never emits `"and"` between garment phrases by
  construction (bare-comma join only).
- **(c)** `garment_join="over"` (`p_over`, already computed) must place `"over"` directly
  between N1's and N2's own phrases specifically, not merely present somewhere in the
  prompt. **HOLDS**.

### Revert proof (fence 1) — monkeypatch, not repeated file edits

`canon_compose.compose()` looks up `_refuse_if_and_joins_a_dependent_pair` as a
module-global at **call time**, so patching the module attribute after import genuinely
disables the exact code path `compose()` runs, without ever touching a file on disk.
Full transcript: `E:\AI\training\facet_E62\fence1_revert_proof.log`. Compressed:

```
BEFORE revert (real code):  compose(doc, form="grouped") [bare default]  -> ANDONs
DURING revert (patched to no-op):  same call                             -> SUCCEEDS,
    composed text verified (independently, via a second substring check in the proof
    script) to actually CONTAIN the illegal join: True
AFTER restore:  same call                                                -> ANDONs again
sanity: 'over' and 'flat' forms both still compose successfully throughout
```

---

## Item 2 — the collision law (fence 2, corrected spec)

### Branch M (mechanical)

`_forbidden_matches(word, text)` factored out of the **existing** `forbidden_hits` —
behavior-preserving refactor (traced by hand; both branches of the old inline
`if/elif` are reproduced exactly). `collision_hits(doc)`'s Branch M calls this same
function against `licensed_phrases(doc)` (the gate's own full aggregate: occupant
phrases, blocked additions, legal_clauses, joint phrases — broader than "occupant
phrase alone," matching the corrected spec's own wording, "a licensed phrase," not
"a licensed occupant phrase"). No pattern was ever re-typed from markdown — the actual
compiled `SLEEVE` object at `canon_gate.py:185` is called directly, satisfying the
advisor's correction verbatim.

**A genuine catch, not a footnote.** The first version of the synthetic Branch M
fixture used the phrase `"a linen shirt with rolled sleeves"` (plural). It silently
failed to trigger Branch M — `canon_gate.py --selftest` reported an ANDON, but tracing
it showed the *wrong* leg failing (the Branch D leg, further down, for an unrelated
reason: A1 didn't have `protected_tokens` yet at that point in the build). Measured
directly: `SLEEVE.search("rolled sleeves")` → `False`; `SLEEVE.search("rolled sleeve")`
→ `True`. The pattern `\bsleeve(?!less)\b` requires a word boundary **immediately**
after "sleeve" — and "sleeve" → "s" inside "sleeves" has none, both being word
characters. **The gate's own matcher is singular-only.** This is not a defect in
`canon_gate.py` (which the corrected spec explicitly forbids re-deriving or "fixing" —
Branch M's whole point is to use the matcher exactly as it is) — it is a property of
"the gate's own matching semantics" that fence 2 requires respecting, and it matches
existing precedent already in this repo: `test_t87_sleeve_on_bare_arm_andon_sleeveless_
does_not`'s own fixture already uses the singular `"a shirt sleeve"`. The synthetic
fixture was corrected to `"a linen shirt with a rolled sleeve"` (singular) and then
triggered Branch M correctly. Reported here because it is exactly the class of error
this repo's own law warns about — "a check that cannot fail is not a check" — and this
one very nearly shipped as one.

**W3, the named fixture** (charter: must stay green): `canon_gate.load_canon(resolve_
subject("W3"))` still succeeds; `collision_hits(w3_doc) == []`. The two real
`forbidden: ["sleeve"]` declarations (`upper_arm_L`/`upper_arm_R`) do not collide,
because the only licensed phrase containing "sleeve" anywhere in W3's canon is
`"a dark green knitted sleeveless tunic"`, and the lookahead exempts it. Confirmed by
re-loading the real file, not a copy.

### Branch D (declared)

`protected_tokens` is a new doc-level field, `{token: reason}`, both strings, validated
structurally by `_validate_protected_tokens`. `collision_hits`'s Branch D fires when a
`forbidden` entry's word (case-insensitive) is a key in `doc["protected_tokens"]`,
regardless of what Branch M can see.

**A1 gets `protected_tokens: {"sleeve": "..."}`, DRAFT canon, UNRATIFIED**, marked
inline and dated, same standing as the depends_on rows. Reason, quoted in full from the
file:

> A1's shirt sleeves are real surfaces (sleeve_L/sleeve_R both carry occupant N2, whose
> ratified phrase is "a cream high-collared shirt"), but N2's phrase under-names them -
> the literal word 'sleeve' appears in no A1 occupant phrase, so canon_gate's own
> mechanical matcher (Branch M) cannot see the collision a forbidden:["sleeve"]
> declaration would cause here. [...] the shirt's sleeves are real surfaces; N2's
> ratified phrase under-names them.

Independently reconfirmed the advisor's own spec-correction-time measurement rather
than trusting it: `licensed_phrases(load_canon(A1))` has **39** entries; **0** of them
trigger `_forbidden_matches("sleeve", ...)`. Exact match to the advisor's stated number.

### Can-fail legs, all proven by reversion, added to `canon_gate._selftest_collision`

- **(a)** W3 fixture green with Branch M live. **HOLDS** (above).
- **(b)** A synthetic subject (`COLFIX`) whose licensed phrase carries a true, singular
  sleeve token (`"a linen shirt with a rolled sleeve"`) plus `forbidden: ["sleeve"]`
  elsewhere **refuses** under Branch M. **HOLDS.** A negative control — the identical
  fixture with the forbidden list emptied — loads clean, proving the refusal was about
  the collision specifically.
- **(c)** A copy of A1's real doc with `forbidden: ["sleeve"]` injected onto
  `shirt_collar` **refuses** under Branch D. **HOLDS.** The same injected copy with
  `protected_tokens` **removed** loads **clean** — the charter's own required proof that
  the protection lives in the data, not a comment. **HOLDS.**

### Revert proof (fence 2) — monkeypatch, not repeated file edits

`canon_gate.load_canon()` looks up `collision_hits` as a module-global at **call time**,
so patching the module attribute genuinely disables the exact code path under test.
Full transcript: `E:\AI\training\facet_E62\fence2_revert_proof.log`. Compressed:

```
BEFORE revert (real code):
  Branch M synthetic (COLFIX)    -> ANDONs
  Branch D A1-injected           -> ANDONs
DURING revert (collision_hits patched to always return []):
  Branch M synthetic             -> loads clean
  Branch D A1-injected           -> loads clean
AFTER restore:
  Branch M synthetic             -> ANDONs again
  Branch D A1-injected           -> ANDONs again
W3 sanity: collision_hits(W3) == [] throughout (real code)
```

---

## Item 3 — `unavailable` as a measurement convention

Documentation only, per the charter (item 3's own words: "the authoring gate is
untouched by this item"). No code change; `check_prompt`'s verdict set
(`ok`/`missing`/`forbidden`/`unlicensed`) is unmodified — the boundary the convention
page itself states explicitly under "The boundary this convention does NOT cross."

**Enumerated before writing** (this repo's own law — "enumerate the resource before
commissioning one"): `docs/tools.md` (stale since the E19 move — does not mention
`canon_gate.py` or anything built after it; rejected as a dead reference), `docs/known-
defects.md` (a catalogue of specific measured defects, wrong shape for a methodology
note; rejected), `docs/profiles-design.md` (a real precedent for this KIND of page, but
about the profile/code boundary specifically; rejected), `docs/index/conventions.json`
(the `record-index` tool's own file-layout config, unrelated to measurement rows;
**not touched** — adding a new page to its `prose_files` sweep list is an index-registry
decision outside this arc's zero-spend, no-index-changes scope, and running the
`record_build` rebuild it would imply carries the two-live-sessions risk this session's
own instructions name as measured this session).

**Delivered:** `docs/measurement-conventions.md` (new page, inside the claims-sweep-
eligible `docs/` tree, unlike `site/`) — the three states kept exactly as the corrected
spec requires (UNAVAILABLE / AVAILABLE+present / AVAILABLE+occluded, never collapsed),
the SPATIAL-only rule for UNAVAILABLE with the backdrop-departure-inverts-on-this-image
worked counter-example, E61's real two-axis row cited verbatim from
`facet_E61/stage3/n2_two_axis_rows.json` (not paraphrased), a minimal reusable row
schema, and the `tools/s3_run.py` exit-4 precedent named as the one-site origin this
page generalises. A short pointer section (`### The UNAVAILABLE convention`) added under
`site/src/content/docs/handbook/reference.md`'s existing `## Verification` heading —
confirmed via `docs/handbook/sync_to_site.py`'s own docstring that `reference.md` is a
site-only page "authored directly in site/," never overwritten by the handbook sync, so
hand-editing it is safe and permanent.

---

## Gates

| gate | result | evidence |
|---|---|---|
| Non-perturbing anchor: `canon_gate.census()` byte-identical, W3/GALLEON/DRAGON/LONGSWORD/E10-LAYER/LOGO/A1, before and after | **PASSED** | `git stash` to true HEAD, census captured both states, `diff` empty — `census_before.log` / `census_after.log` |
| Every existing canon file validates unchanged | **PASSED** | W3, LONGSWORD, A1 all `load_canon()` clean with `collision_hits() == []`; only 3 files in the repo carry a schema (`w3.surfaces.json`, `longsword.surfaces.json`, `a1.surfaces.json` — GALLEON/DRAGON/E10-LAYER/LOGO are identity-only, never reach `load_canon`) |
| Every new check raises, never bare-asserts | **PASSED** | AST walk over `tools/canon_gate.py` post-patch: zero `ast.Assert` nodes (same check `test_t87_no_andon_is_a_bare_assert` enforces in CI) |
| Every new check carries a can-fail leg proven by reverting the implementation | **PASSED**, both fences, monkeypatch transcripts above |
| Fence 1, three REQUIRED legs (a)/(b)/(c) | **ALL HOLD**, against A1's real patched canon |
| Fence 2, Branch M + Branch D + removal-proves-data leg | **ALL HOLD**, W3 real file + one synthetic (Branch M) + A1 real copy (Branch D) |
| Fence 3: UNAVAILABLE never becomes a fourth `check_prompt` failure | **PASSED** — no code touched `check_prompt`'s verdict set; stated as an explicit boundary in the new doc page |
| T34: collector counts move in the same change-set as any added test | **N/A by construction** — zero new pytest-collected test functions added (following the E59/E60/E61 precedent exactly); `pytest --collect-only` reports **1342** both before and after |

No gate fired. No fence was weakened to make a check pass. No canon file needed a
correction to keep loading.

## Verification re-run, in order

- `python tools/canon_gate.py --selftest` → exit 0: `... collision branch-M held
  collision branch-D held` (`stage1_after_a1_data.log`).
- `python tools/canon_compose.py --selftest` → exit 0: `... depends-on and-refused
  depends-on flat-held depends-on over-held` (`stage2_compose_after.log`).
- `pytest tests/test_t87_canon_gate.py tests/test_t92_canon_router.py -q -m "not
  artifacts"`: **30 passed, 1 deselected** (`stage3_t87_t92.log`).
- `pytest --collect-only -q` (full tree): **1342 tests collected**
  (`stage3_collect_after.log`) — unchanged from the session-start baseline
  (`stage0/collect_baseline.log`).
- `pytest tests/test_t34_front_door_counts.py -q`: **52 passed**, re-run three times
  across this session (after test extensions, after docs additions) — every run 52/52,
  matching the session-start baseline exactly (`stage0/t34_baseline.log`,
  `stage3_t34_after.log`, `stage4_t34_after_docs.log`).
- `pytest tests/test_t87_canon_gate.py tests/test_t91_canon_in_path.py tests/
  test_t92_canon_router.py tests/test_t93_canon_worksheet.py tests/test_t94_fail_
  closed.py tests/test_t97_canon_bind.py -q -m "not artifacts"` (every canon-adjacent
  file, widened past the charter's own minimum): **76 passed, 1 deselected**
  (`stage5_canon_wide.log`).
- Full hermetic suite (`pytest -q -m "not artifacts"`, index tests `test_t01_index_
  verify.py` / `test_t30_gates_survive_optimize.py` excluded per this session's own
  two-live-sessions instruction): **1258 passed, 0 failed, 54 deselected (artifacts
  tier), 8 warnings, 486.91s** (`stage6_full_hermetic.log`; zero `FAILED` lines,
  confirmed by direct count). 1258 + 54 deselected + the two excluded files' own
  ~30 collected items reconciles against the 1342 collect-only baseline.
- Consumer check: every `tools/*.py` importing `canon_gate` outside the module itself
  (`brush_cloud_step.py`, `restylize_views.py`, `texpass_brush.py`) calls only
  `canon_gate.require_canon(...)`, which resolves to `load_canon` + `check_prompt` on
  one of the three real canon files — all three confirmed clean above, so none of these
  spend-gate call sites is affected by this patch.
- CRLF check on every new/edited file: `git ls-files --eol` on the six tracked edits
  reports `i/lf w/lf` uniformly; the new `docs/measurement-conventions.md` (edited once
  after its first draft, to fix a dangling "named below" citation caught on re-read —
  see below) read as raw bytes shows 0 CR bytes (`153` LF, `8562` total bytes, final
  state) — direct byte check, not `grep $'\r'`, per this repo's own recorded
  shell-quoting trap.
- A second, smaller self-check on the new documentation page itself: re-reading
  `docs/measurement-conventions.md` after drafting it caught its own defect — "this
  repo's own record has one entry for exactly that failure mode (named below)" never
  actually named the entry below. Fixed to cite the concrete instance (this arc's own
  kickoff, first landing item 3 as two states, corrected at `c3da18e`) rather than leave
  a claim with no citation — the same discipline this repo asks of every other claim,
  turned on a page written this session.

## git status --short (verbatim, read fresh at close)

```
 M canon/a1.surfaces.json
 M site/src/content/docs/handbook/reference.md
 M tests/test_t87_canon_gate.py
 M tests/test_t92_canon_router.py
 M tools/canon_compose.py
 M tools/canon_gate.py
?? docs/experiments/E62-schema-patch-report.md
?? docs/measurement-conventions.md
```

Every line is this executor's own edit — no concurrent-session footprint this time
(contrast E61's report, which found six unrelated modified files from another live
session; this run's `git status` at both the session-start baseline check and here at
close shows only files this arc touched).

## Working tree — file map

- Report: `E:\AI\facet\docs\experiments\E62-schema-patch-report.md` (this file)
- Handoff: `E:\AI\training\facet_E62\handoff.md`
- Modified: `tools/canon_gate.py`, `tools/canon_compose.py`, `canon/a1.surfaces.json`,
  `tests/test_t87_canon_gate.py`, `tests/test_t92_canon_router.py`,
  `site/src/content/docs/handbook/reference.md`
- New: `docs/measurement-conventions.md`
- Logs: `E:\AI\training\facet_E62\*.log` (baseline, per-stage, both revert-proof
  transcripts, census before/after)
- Revert-proof scripts (scratchpad, not part of the repo):
  `C:\Users\mikey\AppData\Local\Temp\claude\E--AI-facet\428295a0-ff4d-49f0-b0a2-
  024d00acf529\scratchpad\revert_proof_fence{1,2}.py`

## Standards compliance — re-affirmed against what was actually built

Both edited tools carry their own scored standards-compliance addenda in their module
docstrings (`canon_gate.py`'s new "DEPENDS_ON AND THE COLLISION LAW" section;
`canon_compose.py`'s "E62 ADDENDUM" under its existing scored block) — not duplicated
here at length. Compressed: PIN_PER_STEP holds (every edge/phrase read live, never
retyped); ANDON_AUTHORITY holds (raise, not assert, confirmed by AST walk; every new
refusal carries a can-fail leg proven by reversion, both fences, transcripts above);
NAMED_COMPENSATORS is n/a (zero spend, every edit reverts by pathspec — no irreversible
tool call anywhere in this arc); DECOMPOSE_BY_SECRETS holds (schema validation /
collision detection / composer consultation / documentation land as four separable
edits across four files, none of which reimplements another); UNCERTAINTY_GATED_HUMANS
holds (both canon-data additions marked DRAFT/UNRATIFIED inline, dated, attributed,
reported here for the Director's word rather than presented as settled); EXTERNAL_
VERIFIER holds (the census anchor and the two monkeypatch revert transcripts are the
cross-checks; nothing here grades its own output as good or bad — that judgment is
explicitly left to the Director and the advisor, per this arc's own role discipline).
