# E35 arm slate — executor report

**Run 2026-08-14 at the Director's word.** Spec [E35-armslate-spec.md](E35-armslate-spec.md);
bands registered blind and pushed at `3095cf1` **before** the first arm was emitted.

**Three jobs spent, not four.** The pre-registered (d) rule landed on branch 4 and (d) did
not fire. **Spend: 33 → 36 of 45.** The fourth job is unspent and returns to the ceiling.

**No gate fired.** Nothing here says whether any of it is good.

---

## 1. The walk — every visible class, before any number

Full size and at 3× on the head ([E35_armslate_sheet.png](../../../../AI/training/facet_E35/diag/E35_armslate_sheet.png),
`E35_armslate_head3x.png`, both under `facet_E35\diag\`).

**Identity.** **(b) is the same man. (a) and (c) are not.** (a) has a narrower, more angular
jaw, a larger and more detailed ear, and its face is drawn in *hard graphic lines* — the brows
and the smile read as inked strokes rather than sculpted relief. (c) has a rounder, fuller
head, thin hard-drawn brows, and a broader smile. Both read as a different performer at his
zoom. **No instrument in this slate measures this**, it was pre-declared as unmeasurable
here, and it is the first thing on the sheet.

**Material / register.** (c)'s surface is **glossier and smoother** — the matte thumbprint
hatching is largely gone from the face, and the body carries strong vertical striations that
read closer to corduroy than to sculpted clay. (a) is more saturated overall. (b) is matte
like the recorded twin.

**The pale wash** on the crown and forehead is present in all four, and by eye it is heaviest
in (a) and (c) — which the numbers agree with, though §5 argues the number may not mean what
its name says.

**Out of scope, named anyway.** (a)'s backdrop is darker with a stronger gradient than the
other three. (c)'s pose reads more frontal than the recorded twin's despite an identical seed
and an identical figure support in its control.

## 2. Provenance

Right of the divider on the sheet: the clay init (node 9, shared by all four), the canny
control (node 10, used by the recorded twin and by (a) and (b)), and the depth hint (node 10,
(c) only). The depth panel is what arm (c) actually fed the model.

**One property of the hint, recorded before submission and not tuned:** normalisation is over
the whole figure's depth range, and the near limb takes the top of that range, so the **head
occupies only 110–179 of the 254 available levels**. The hint carries less contrast in exactly
the region the pale class lives in. Left as built.

## 3. The measurements

Base is the recorded twin at view 1, seed 770700 — **not** R2-a's eight-view 770700 mean
(734.5 / 11.67 / 170.4), which is a different population.

| arm | pale area | L\*-rise | dark count | dark px² | largest | C\* | reg-IoU |
|---|---|---|---|---|---|---|---|
| **recorded r3** (base) | **278** | **4.97** | **16** | **157** | 19 | **23.77** | **0.9372** |
| (a) euler_ancestral | 948 | 22.81 | 17 | 49 | 5 | 32.23 | 0.9446 |
| (b) flat even lighting | 226 | 4.09 | 18 | 155 | 27 | 23.91 | 0.9374 |
| (c) depth hint | 1047 | 16.77 | 26 | 81 | 11 | 25.83 | 0.8991 |

**The dark class read two ways, and they disagree.** By *count* every arm is flat-to-worse
(16 → 17 / 18 / 26). By *area* (a) and (c) cut it hard (157 → 49 and 81) with much smaller
largest components (19 → 5 and 11). More specks, less speck. The pre-registered score uses
count, which is the unit the selection scorer has always used; the area column is reported
beside it rather than substituted for it after the fact.

**(c) registered worse to the geometry than the canny arms** — reg-IoU 0.8991 against
0.9372/0.9374/0.9446, on a keyed figure 4,118 px larger. The depth hint's support is
byte-identical to the mask (G3), so this is the sampler painting outside the hint, not the
hint being wrong.

## 4. The (d) rule, applied

Arithmetic in code (`facet_E35/diag/s4_selection.json`), rule fixed in the spec before any
arm existed.

```
score(X) = (1 - pale/278) + (1 - dark_count/16)
(a) -2.4726    (b) +0.0621    (c) -3.3912
1. register exclusion at C* <= 10.00 (the highest MEASURED 2b register-death rung): NONE
2. surviving arms with score > 0: [(b) flat even lighting]  -> |C| = 1
4. BRANCH 4 -> (d) DOES NOT FIRE. A best pair of one arm is not a pair.
```

**Branch 4 was written into the spec before the inputs existed**, together with branch 5, on
R2-c's own law that a fork over a signed quantity has at least three branches. It is being
taken, not improvised.

## 5. ⚠ What the pale number may not be measuring — reported, not ruled

R2-c's mechanism reading was that the pale class is the clay init surviving where the sampler
is least anchored. Down the 2b denoise ladder that reading is supported on both axes: the pale
regions marched toward the init's L\* 76.43 **and** their chroma collapsed toward its C\* 1.12
(12.45 → 7.16 → 2.82).

**On this slate the chroma does not collapse.** The pale components' own C\*:

| | recorded | (a) | (b) | (c) | *(2b ladder for contrast)* |
|---|---|---|---|---|---|
| pale-region C\* | 23.25 | 26.16 | 23.88 | 23.00 | *12.45 → 7.16 → 2.82 → toward 1.12* |

These pale regions are **chromatic** — terracotta at high lightness, not grey clay. And the
non-pale reference moved in the opposite direction on (a): L\* ref 47.88 → **41.39** while the
pale rose 52.86 → **64.20**. The whole render got more contrasty, and the pale measure is a
*local excursion* (≥ 6 L\* above a 31 px local median), so it fires on increased local
lightness contrast whether or not any init survived.

So the measure may be counting two different things, which coincided on the ladder (where
everything converged on the init) and separate here. **This is a measurement, not a ruling** —
what it means for R2-c's mechanism is the advisor's and the Director's. The executor seat that
ran R2-c registered exactly this objection in its own blind bands at the time ("if the cn arms
come back unchanged, the honest reading is init-**influenced**, not raw init bleed"); it now
has three more arms behind it.

The same fact cuts at my own band B4, which registered this confound as a risk for arm (b)
only. It fired on (a) and (c) instead.

## 6. Bands, scored honestly

Registered at `3095cf1`. **5 hit, 8 missed, 2 mixed.**

| band | predicted | measured | verdict |
|---|---|---|---|
| A1 pale falls, 120–260 | falls | **948** | **MISS** — nearly 4× the base, direction wrong |
| A2 dark count rises, 14–28 | 14–28 | **17** | **HIT** — but see mixed note below |
| A3 C\* 21.0–24.5 | holds | **32.23** | **MISS** — chroma rose far above the band |
| B1 dark count falls, 6–14 | falls | **18** | **MISS** — rose |
| B2 pale ~unchanged, 200–400 | 200–400 | **226** | **HIT** |
| B3 C\* 19.0–24.5 | holds | **23.91** | **HIT** |
| C-i union accepts depth (~0.6) | coherent figure | coherent | **HIT** — the clause held |
| C1 pale falls hardest, 60–220 | falls hardest | **1047** | **MISS** — rose hardest |
| C2 dark count falls, 8–18 | falls | **26** | **MISS** — rose most of the three |
| C3 C\* 22.0–25.0 | holds | **25.83** | **MISS** — just outside |
| C4 if C-i fails, identity moves | — | C-i held, identity moved anyway | **MIXED** |
| D1 branch 3, pair (c)+(b) | fires | **branch 4** | **MISS** |
| D2 (a) is the marginal arm | marginal | (a) −2.47, **(b)** +0.06 | **MISS** — (b) was |
| D3 no register exclusions | none | none | **HIT** |

**A2 is a hit I am not comfortable banking.** The band was on count and count landed in it,
but I predicted a rise *because ancestral noise makes more discrete blobs*, and the same arm
cut speck **area** by 69%. The band's unit was right and my reasoning under it was not.

**C4 is the interesting miss.** I wrote that a union unable to read the hint would fail
loudly, with material and identity change — the documented signature of a control that
constrains nothing. The union **did** read the hint (the figure is coherent and follows the
geometry), and identity moved anyway. So identity change is not diagnostic of control failure
on this route, which is the opposite of what I registered.

**The direction I was most wrong about, across the board:** I reasoned from R2-c that *more
anchoring* (depth) and *more trajectory entropy* (ancestral) would both reduce init survival
and therefore pale. Both raised it, by 3.4× and 3.8×. Whether that falsifies the mechanism or
falsifies the instrument is §5's open question and is not mine to close.

## 7. Gates — all six, none fired

| gate | result |
|---|---|
| G1 frame | **PASS** — all four twins exactly 352×1024 |
| G2 single lever | **PASS** — 1 override each; graph diff against the recorded base is exactly `13.sampler_name` / `7.text` / `10.image`; node set and every class_type identical |
| G3 depth support | **PASS** — `depth > 0` differs from `armclay_1_mask.png` by **0 px**, and from `masks_300k/armclay_1.png` by 0 px |
| G4 non-perturbing edit | **PASS** — `--anchor` on views 0, 1, 4: **0 differing px, IoU 1.000000** each |
| G5 pale-instrument anchor | **PASS** — all six R2-c rows to the digit (278/4.97, 932/12.99, 1220/19.68, rungs 183/404/511, L\* 61.79/67.66/72.08, C\* 12.45/7.16/2.82) |
| G5b register-instrument anchor | **PASS** — recorded 0.9372 / 23.77; death rungs 10.00 / 3.91 / 1.89; 2c arms 24.29 / 22.40 |
| G6 prompt diff | **PASS** — enforced in the builder: term 15 of 16, `soft studio light` → `flat even lighting`, whole-string equality to a single replacement, no file on failure |

## 8. What was built, and what it cost

**`tools/silhouette_masks.py --depth`** — the raycast already computed `t_hit` and kept only
`isfinite`; this emits it. Camera is ortho so `t_hit` is linear depth; the depth and the mask
are the same cast, so registration is by construction rather than by re-derivation. The figure
encodes into **1–255 with background 0** deliberately: a 0–255 map gives the farthest surface
the background's own value and G3 could then never fail.

**Tests ride the commit: `tests/test_t69_silhouette_depth.py`, 10 tests, all green.** Hermetic
(synthetic sphere, built in-process, synthetic tag). Includes the non-perturbing leg (mask
byte-identical with and without `--depth`), a not-vacuous leg, and **the can-fail proof**: a
copy of the tool with the `1 +` floor removed is run and the ANDON is shown FIRING — under
plain Python **and** under `PYTHONOPTIMIZE=1`.

⚠ **One assertion I wrote and then withdrew, measured:** a whole-file ASCII-source leg. This
repo's law is *ASCII prints*, and `silhouette_masks.py` already carried **51** non-ASCII bytes
before I touched it (`project_twins.py` carries 357). The leg would have asserted something
untrue about the tree, so it was narrowed to the depth block's own printed strings — which it
then caught an em-dash in, and that was fixed.

**Two diag instruments parameterised**, not reimplemented: `r2c_pale_vs_levers.py` and
`t2_register_all.py` both took `--twins/--out-json` with the recorded run as the default, so
the slate is graded under the code path that produced the tables it is graded against. Both
carry their anchors above (G5, G5b). The fork/ladder readouts are suppressed under `--twins`
because `rows[1:3]` and `rows[3:]` name R2-c's arms by position and would be a wrong number in
a right format over any other set.

**Payloads were transcribed, and the transcription was proven before spending** — each one
written to a scratch file and compared as parsed graphs against the emitted payload, with a
can-fail check that a one-field change is detected. No hand-authored graph reached the cloud.

**Spend:** 3 jobs, ≈ $0.054 at the measured $0.018/job. **36 of 45.** No re-rolls were taken
and none is proposed.

### 8a. The harness, and three errors of mine that it caught

**Counts moved 985/940 → 995/950** (T69's ten tests, both tiers). All **16** pinned surfaces
were rewritten by importing `T34.PINS` and driving the substitution from the table itself —
never a hand list, per the standing rule — plus digits-only on all seven translated READMEs,
each of which carried exactly 2 stale sites of each value and now carries 2 fresh and 0 stale.
**`translate-all.mjs` was NOT run.** Translations are the advisor's hands; changing a numeral
inside an already-translated sentence is not generating a translation, and regenerating the
seven files is.

**T31's E23 scope pin fired, and was moved on purpose in this commit** — `silhouette_masks.py`
4 → 5 raises, route total 57 → 58, both with the reason written at the site. This is the pin
performing the exact service E23 Ruling 9 built it for: a scope that cannot drift silently.
The new ANDON is **not** added to T31's `FIRE` list, and the reason is stated there: every
FIRE entry fires on crafted *input*, and this one fires on an internal invariant no CLI
argument can violate, so it has no honest `build(tmp_path)`. T69 carries its two properties
instead — firing under plain Python and `PYTHONOPTIMIZE=1`, and writing nothing.

⚠ **And T31's sibling property made me change the tool.** The gate originally created its
`--depth` directory before checking, which would have made it a *third* member of
`DIR_AHEAD_OF_GATE` — a set deliberately pinned at two so a third joining fails rather than
passing under a loosened rule. `makedirs` now runs **after** the ANDON, so "nothing is
created when it fires" is true by construction rather than pinned as an exception. The
shipped depth maps were re-rendered at HEAD after that move and compared **pixel-wise**:
**0 differing values** on both `_depth` and `_depth_far`, so the hint arm (c) consumed still
reproduces.

**Three errors of mine, all caught by instruments rather than by my reading:**

1. **I re-emitted the census flagless.** `instrument_census.py` with no arguments covers only
   `tools/diagnostics` and silently dropped `tools/verify`; T41 caught it in two legs. The
   correct invocation is `--committed`. I ran a tool without reading its flags, on the same
   day this arc's spec opened with a finding about not reading what already exists.
2. **I read a suite result off a `tail -12`** and reported 7 failure names against a summary
   of 27. The capture file was itself a 10-line tail, so 20 names were never written. Third
   family instance in this repo, first at this seat. Re-run to a file and read complete:
   `grep -c "^FAILED"` now agrees with the summary line, which is the check that makes a
   truncation surface as a mismatch.
3. **I trusted a reported exit code over the tool's own summary.** The harness reported
   "exit code 0" for a run whose pytest summary said `27 failed`; the 0 was the wrapper's.

**Suite at the close: 995 passed, 0 failed** (`995 total / 950 hermetic`, 45 artifacts
deselected), read from a complete capture whose `grep -c "^FAILED"` returns 0 in agreement
with the summary line — the cross-check, not the eyeball.

## 9. Artifacts

```
E:\AI\training\facet_E35\
  depth\armclay_{0,1,4}_depth.png  + _depth_far.png     the hint, near=white and inverted
  twins\twin_s4{a,b,c}_*_v1.png                          the three arms
  payloads\payload_s4{a,b,c}_*_v1.json + .meta.json      graph + override dict + sha256
  diag\s4_pale.json  s4_census.json  s4_register.json  s4_selection.json
  diag\E35_armslate_sheet.png  E35_armslate_head3x.png
docs/experiments/E35-twin-prompts-r3L-view1.json         the probe prompt, versioned
```

| arm | prompt_id | payload sha256 |
|---|---|---|
| (a) s4a_eulanc | `b3a6ae07-873a-4cd5-8bb3-ee8e485986d3` | `dceb55fcf58e6728…` |
| (b) s4b_flatlight | `b536ccc2-884c-475c-9631-9019bcfc665f` | `177a5b7722a2f041…` |
| (c) s4c_depth | `ebac0f95-a824-43d1-b511-b77022f0a863` | `c48c03a43126c893…` |

Depth hint uploaded as `4368c3ca66b55bb2389c3d9f61da87f80232ab2ad039ad52ccdcf365351123af.png`.

## 10. HALT

The arc stops here for the Director's eye. The sheet is the deliverable; the numbers sit
under it. Nothing after this — no rebuild, no second view, no route change, no re-roll —
fires without his word.

**A negative result is a full success, and this is close to one:** of three single levers,
one held the man and moved neither class much, and two moved both classes the wrong way while
replacing the performer. That is a result, and it cost three jobs.
