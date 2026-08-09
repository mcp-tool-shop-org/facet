# E25 — predictions, committed before any file under `tools/` was opened

**Executor session, 2026-08-08.** Spec:
[E25-diagnostics-gates-kickoff.md](E25-diagnostics-gates-kickoff.md). Committed **before
the first `tools/` file is read as source**, and scored in
`E25-diagnostics-gates-report.md`.

**A second session (E24) is live in this working copy.** Its uncommitted work —
`tools/facet_index.py`, `tools/record_mcp.py`, `tests/test_t32_installed_wheel.py` — is
present in the tree at this commit and is visible to my baseline suite run. Predictions
that depend on the suite say so.

---

## What I knew when I wrote this, stated exactly

Both prior calibration lessons bind, and they pull in opposite directions:

- **E22:** *check that the population is real before you predict its density.* P18 missed
  by ~44× because it predicted a property of a class that did not exist. So the
  population was **measured first**.
- **E23:** *check what the metric's unit is.* P4b missed 4-vs-20 because it reasoned about
  **files** while the instrument measured a **scope**. So every count below names its
  unit.

**Measured before this file was written** (`census.py`, AST, counts only — no source text
entered my view):

```
tools/diagnostics/   ANDON assert 132 across 42 files    non-ANDON assert  2
tools/verify/        ANDON assert   1 across  1 file     non-ANDON assert  3
                     -------------------------------
  IN SCOPE           133 sites across 43 files
tools/superseded/    ANDON assert   1  (texpass_thin_mask.py:160)  PERMANENTLY OUT
```

**Every quantity the dispatch says it measured reproduces to the digit:**

| dispatch claim | measured here |
|---|---|
| 133 sites across 43 files | **133 / 43** |
| 50 multiline | **50** |
| 5 `not`-conditions | **5** |
| 0 sharing a first line | **0** |
| 0 missing a message | **0** |
| 28 `SystemExit` ANDONs across 12 files | **28 / 12** |
| `superseded/` 1 site | **1** |

The five `not`-conditions are one each in `e08_intersect_delta`, `e14_demote_garnet`,
`e14_garnet_reproject`, `e14_repair_collar`, `gained_bg_check`.

**Two denominators measured rather than inherited**, because P3 is the seat where E22's
P18 died and the whole failure was an unreal denominator:

- **`bpy` is imported by exactly 1 of the 43** (`e12_head_render.py`, 3 sites) — the
  dispatch's exclusion is confirmed, not assumed. So P3's denominator is **130 sites in
  42 files**, not 133.
- **Third-party imports across the 43**, against CI's pinned install line
  (`numpy scipy pillow trimesh open3d mcp opencv-python-headless`): `numpy` 37 files ·
  `PIL` 30 · `trimesh` 23 · `open3d` 17 · `scipy` 13 · `cv2` 3 — **all present in CI**.
  The only two absent are `bpy` and `mathutils`, both in the one Blender file the smoke
  tier already excludes. This is the exact shape that fired E23's gate 4.

**Handed to me by the dispatch or a prior ruling, so no row is blind on these:** the two
smoke exclusions and their reasons · that 41 of 43 exit 0 writing nothing under all three
modes · the T-number collision · E22 Ruling 3's axis · E22 Ruling 5 / E23 Ruling 13's
`SystemExit` population · E23's own outcomes (P1 57/57, P3 16 of 38, P4 0).

**Not known to me at this commit:** any source line of any of the 133 sites; where in its
file's control flow each site sits; what input each tool takes; which sites sit inside a
`try`; what any of these tools is for beyond its filename.

Blindness classes: **B** blind · **S** semi-blind, leaning on something named in the row ·
**M** measured first, as above · **C** a commitment rather than a forecast · **F**
**FORFEITED** — see P5.

---

## The five the dispatch names

| id | class | prediction |
|---|---|---|
| **P1** | S | **133 of 133 splice with no hand fix.** Band **126–133**. Leans on the four measured shape claims and on E22 88/88 + E23 57/57 under the same bar. |
| **P2** | B | **Yes to both.** `py_compile` **43/43** after conversion; the `--help` smoke **41 files x 3 modes = 123/123** exit 0 with the scratch cwd still empty. |
| **P3** | M | **46 of 130 fire hermetically.** Band **22–78**. Denominator measured (133 − 3 `bpy`), not inherited. |
| **P4** | B | **0 of the 133 is not a gate** by E22 Ruling 3's test. Band **0–4**. Separately: **3 sites** flagged as ANDONs whose failure decides nothing irreversible, band **0–12**, routed to the ruling rather than changed. |
| **P5** | **F** | **BLINDNESS FORFEITED — see below. Measured: 3 of 42.** |

### P1 — what a hand fix would look like

The splice fails where the line range is not exactly the statement. Forms I expect if
this comes in under 133: a **trailing comment on the site's last line** (which surfaces
as a non-zero comment-token diff, not a syntax error); a **backslash continuation**; an
implicit string concatenation carrying an interior comment; a closing paren sharing a
line with the next statement. "0 share a first line" does not constrain the *last* line,
and at 133 sites there is 2.3x E23's surface for exactly this.

The **5 `not`-conditions are the named risk**, and they are why the band is not tight:
E23 had zero, so the negation branch of the rule has never once executed in this repo.
`negate(not X) = X` is trivially right on paper and is the branch with no track record.

### P2 — what a "no" would look like, since I predicted yes

**`py_compile`:** an `IndentationError` on one named file, from a continuation line
re-indented by the wrong amount inside one of the 50 multiline sites. Caught before
anything else runs, and it names its file and line.

**The smoke:** a non-zero exit whose realistic cause is an exception at *import* — a
splice that re-parented a statement out of a function into module scope. A
mode-dependent failure (passing normally, failing under `-O`) cannot be caused by this
conversion on the `--help` path, so if one appears it is a finding about the file.

I also predict the **baseline** smoke passes 123/123 before conversion, so the after-run
is a real before/after rather than a first measurement.

### P3 — the reasoning, and the unit stated explicitly

**The unit is a SITE'S INPUTS**, not a file's character. A site fires hermetically when
everything between process start and that site can be satisfied by files I can author in
a scratch directory. That is a property of control-flow depth and of what the prior steps
consume — so "diagnostics are readers, therefore easy" is exactly the file-character
reasoning E23 Ruling 12 convicts, and I am not using it.

**Denominator: 130 sites in 42 files** (measured — `bpy` is in exactly one file, 3 sites).

What pushes the count **up**: the authorable input formats dominate. PNG (30 files),
NPZ/NPY (37), JSON, and even GLB (23 files, and `trimesh` authors a valid one in a line)
are all constructible. A gate validating an argparse path fires by pointing at a path
that does not exist.

What pushes it **down**: a gate sitting after a cloud round-trip, a GPU render, an
`open3d` reconstruction (17 files), or behind a hardcoded recorded-tree path. The
dispatch already names one instance of the last shape — `e04_make_brush_prompts` does
file work before argparse and dies on a missing profile path — which is evidence that
this class is populated, not hypothetical.

46/130 is **35%**, near E23's measured 16/38 = 42% adjusted down for the recorded-tree
dependence these instruments have and route tools do not. **The band is wide in both
directions because the variance is entirely control-flow depth, which I have not
measured** — the same honesty E23's P3 used to land inside its band.

### P4 — and the quantity that is easy to confuse with it, predicted separately

All 133 carry the token, so "not a gate" can only mean an ANDON whose failure decides
nothing irreversible. E22 Ruling 3 found the taxonomy maintained rather than accidental,
and E22 Ruling 4 says of exactly this class that these sites *"mislead a reader when they
fail silently; they do not corrupt an artifact."* That is a statement about consequence,
not about declaration, and the axis is declaration — so I predict **0** misapplied
tokens and **3** sites worth flagging on consequence.

**Distinct, and this is E23's P4b seat, where the advisor's own instrument missed 4-vs-20:**
the count of the 133 with **no write later in their own enclosing scope**. E23's miss was
reasoning about files when the unit was a *scope*, and the mechanism was that decomposed
tools factor the write out into a caller. **These are one-shot scripts, which is the
opposite architecture** — a flat `main()` that loads, measures and writes a sheet means
the enclosing scope usually does contain the write. So I predict **28 of 133** have no
write in scope (21%), band **10–60**, *lower* than E23's measured 35% — and I am stating
the mechanism so a miss is diagnosable rather than just wrong.

### P5 — FORFEITED, and the forfeit is my own defect

The dispatch asks me to predict **how many of the 42 diagnostics files carry a
`SystemExit` ANDON beside an assert one.** I cannot: **my census script counted
`SystemExit` raises in the same pass as the assert sites, and I read the output.**

Counting `SystemExit` was **not required** by the population check that E22's lesson
mandates. I bundled an unnecessary measurement into a required one and spent a
prediction's blindness on it. Measured value, recorded as a measurement and **not scored
as a prediction**:

```
3 of 42   -  e12_head_evidence (4 SystemExit) . e12_region_colour (2) . e12_twin_readout (2)
```

The wider collision, also measured: **28 `SystemExit` ANDONs across 12 files**, of which
those 3 also hold assert ANDONs. Reported, not resolved (E22 Ruling 5).

**The lesson, which belongs in the report whatever else happens:** a blindness-preserving
census must measure the *narrowest* thing that answers the population question. Mine
measured everything cheap, because everything cheap was in one AST walk.

---

## The rest, so the report has something to score

| id | class | prediction |
|---|---|---|
| **P6** | M | The four shape claims reproduce exactly: **50 multiline · 5 `not`-conditions · 0 shared first lines · 0 missing messages.** Already measured above; recorded so the report's table is complete. |
| **P7** | C | **Whole-file AST equality 43 of 43, zero reverts.** A commitment: a file that does not prove identical reverts rather than being adjusted. |
| **P8** | C | **0 comment tokens changed** across the 43. |
| **P9** | B | Gate 1 baseline: **370–400 collected, 0 failed**, artifacts tier live. The band's width is E24 — its uncommitted `test_t32_installed_wheel.py` is in this tree and will be collected by my run. **If anything is red at baseline it is in T32 and it is E24's, and I report it rather than fixing it.** |
| **P10** | B | T33 adds **330 cases**, band **150–500** (43 `py_compile` + 123 smoke + 43 structural + a can-fail leg + 3 modes x the fired set). Suite after in band **520–900**. |
| **P11** | M | The `SystemExit` collision is **reported, not resolved**: 28 sites, 12 files, 3 overlapping. |
| **P12** | B | Manifest **>= 7,312 files**, holding **0 added / 0 removed / 0 changed** at all three checks. |
| **P13** | S | **CI green, no workflow edit, gate 4 does not fire.** Measured basis: every third-party import across the 43 except `bpy`/`mathutils` is already in CI's pinned install, and both of those live in the one file the smoke tier excludes. This is the same check whose absence fired E23's gate 4. |
| **P14** | B | **4–8 findings.** At least **2 of them not handed to me by the dispatch** (the T-number namespace gap and `e04_make_brush_prompts`' pre-argparse file work are both already named in it, so neither counts). |
| **P15** | C | `tests/test_t31_route_gates.py:80`'s **`REMAINING_ELSEWHERE` moves 134 -> 1**, deliberately, in the commit that earns it. |
| **P16** | C | **`tools/superseded/texpass_thin_mask.py:160` is untouched**, and the report says so. |
| **P17** | B | **0–1 `fold`-marked failures.** On one: run-then-rerun once, and the report says a second session was live so the failure stays attributable. |
| **P18** | S | **T33 is still free** when the test file lands. `test_t32_*` is the highest taken as of this commit. |
| **P19** | B | **0 of the 133 sit inside a `try` whose handler swallows the raise.** Band **0–3**. Structurally, `assert cond, msg` already raises `AssertionError(msg)`, so under a normal interpreter no handler can newly catch anything; the useful question is whether any of these files eats its own halt today. |

---

## What this session will not do

Convert anything outside the 133 · touch `superseded/` · touch `tools/facet_index.py`,
`tools/record_mcp.py`, `tests/test_t28_*`, `tests/test_t32_installed_wheel.py` or
`release.yml` · fix a defect found in E24's files · unify `SystemExit` · improve a
message in passing · `git add -A` or `git commit -a` · `git pull --rebase` · run
`e12_head_render.py` or build a Blender harness · point any tool at a recorded tree ·
assert that `PYTHONOPTIMIZE=1` disables a gate · write to the memory store · tag or
publish.
