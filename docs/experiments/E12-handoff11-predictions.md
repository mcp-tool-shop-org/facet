# E12 handoff 11 — blind predictions, registered before anything runs

**Executor session, 2026-08-06.** Written before the v8 rebuild, before any v8 artifact exists,
before the nape-visibility check, and before `project_twins.py` is touched.

## Blind status, disclosed exactly

**Blind to every outcome. Not blind to the baselines, and could not be** — the dispatch asks for
predictions *against* the handoff-8/9/10 numbers, so those were read first. Specifically:

| what I have read | what I have NOT done |
|---|---|
| CLAUDE.md, E12 Rulings 19/20, E13 spec + amendment, `profiles/beast.json`, `canon/DRAGON-IDENTITY.md`, the handoff-8 / 8-tasks23 / 9 / 10 reports, `E12-twin-prompts.json` (v7), the builders and `project_twins.py` | run the v8 builder · look at any v8 stem · check nape visibility on any render · submit anything · touch `project_twins.py` · run the anchor · open any twin, gate or registration number produced this session |

One deterministic check **was** run before writing this, and it is disclosed rather than hidden:
a term-level diff of `beast.json`'s prompt entry against v7's `_entry_verbatim`. It returns one
inserted term, `charcoal neck spines`, at term index 8. That is the input to the work, not an
outcome of it, and P1a below is therefore near-certain by construction — it is registered anyway
because an ANDON that is expected to pass still has to be *stated* before it runs.

---

## Task 1 — the v8 stems

- **P1a — the delta is exactly one inserted term.** Entry goes **19 → 20 terms**;
  `charcoal neck spines` lands at index 8, immediately after `bone-ivory crown and cheek spikes`
  and immediately before `charcoal dorsal and tail spines`. The ANDON asserted as *construction*:
  strip that one term from each v8 stem and what remains is **byte-equal to the matching v7 stem**
  — on **all nine stems**, companion included. *Confidence: near-certain (it is arithmetic).*
- **P1b — the drop map does not move.** The six `--drop` arguments are byte-identical to v7's;
  the new term is in neither the mouth family {3,4,5} nor the horn family {3,5}. Per-view counts
  predicted **20 / 20 / 20 / 14 / 16 / 14 / 20 / 20**, `headclay_0` **18**; full-string views
  unchanged at {0,1,2,6,7}.
- **P1c — the nape is visible from every yaw, so no drop is added.** Predicted **8 of 8**.
  *Confidence: high on 0,1,2,6,7; **medium** on 3 and 5*, which hide the whole head behind the
  near wing membrane (Ruling 10i: head-box first-hit 0.81% of figure). The nape sits behind the
  skull toward the shoulders and is **continuous with the dorsal ridge** (Ruling 20c), whose term
  already rides 3 and 5 — that is the reason I expect it visible there. **Pre-registered branch:**
  if the render shows the nape occluded on 3 and/or 5, Ruling 9d *requires* the drop, I add it,
  and I say plainly that P1c was falsified and the per-view arithmetic for those views is
  therefore 13 rather than 14.
- **P1d — `headclay_0` KEEPS the new term, and this is mechanical rather than chosen.** The
  companion's recorded drop list is `charcoal dorsal and tail spines` + `charcoal claws`; a term
  not on that list arrives in the stem by the deletion construction, exactly as v6's wing term
  did without a new flag. **Predicted side effect, reported not decided:** this gives the
  shoulder-end crest entering the companion's bottom edge a declared colour for the first time —
  the `_companion_rationale_VOID` flag carried since v5. `headclay_0` is not submitted.

## Task 2 — the exemplar base coat, all eight, seed 770700

### The three new/changed terms are not the same delta on every view

Stated first because it governs everything below. Against **what actually generated the twin
that exists**: views 1,2,3,5,6,7 are v5 artifacts and gain **three** terms (both wing phrases +
neck spines); view 0 is v6 and gains the split + neck spines; view 4 is v7 and gains **neck
spines alone**.

- **P2a — the nape converts.** The defect is crown-ivory vertebrae on an unnamed surface; the
  wing term's precedent is −66.4% on view 0. Predicted: on a **geometry-derived** nape box (not
  hand-placed — the wide-box error of handoff 9 §4 is the reason), pale-family mass falls
  **≥ 30% relative** on at least **5 of the 8** views. *Confidence: medium-high.* The named
  alternative is Ruling 20a's seed resistance recurring on this term.
- **P2b — the wing skeleton, per view, at the pinned seed.**
  - **View 0: holds green.** Whole-figure ivory **25,000–40,000 px** (v6 measured 31,601).
    *Confidence: high.*
  - **View 4: resists again.** Wing-box ivory **13–18%** at 770700 (v7 measured 15.4% after three
    stems all resisted at this seed). *Confidence: medium-high, and this is the 20a caveat's
    direct test.* At its bounded re-roll (770701) I predict the struts bind at **≤ 8%** wing-box
    ivory (the recorded 6.0%).
  - **Views 1,2,3,5,6,7 (folded wings): small move.** These kept the skeleton green by context at
    v5 with no term at all, so naming it should change little. Predicted whole-figure ivory within
    **±25%** of each view's v5 value.
- **P2c — re-roll spends, pre-registered so spending reads as process.** Predicted **1–3 of 8**.
  **Named: view 4** (near-certain, on P2b). **Possible: view 3** — its v5-at-770700 carried the
  43,999 px flat-black foreleg; but three added terms re-roll that landing anyway, so I predict
  the void does **not** recur (≈60/40). Any view whose eye-check shows a spec-visible miss on a
  declared surface spends its one allowance at 770701 and no further.
- **P2d — the gate rises where the terms convert, and stays shoulder-dominated.** Measured twice
  already (view 0 13.37 → 18.78%, view 4 1.68 → 7.14%, shoulder 80.6% / 99.6%). Predicted: **at
  least 5 of 8 rise** against their v5/v6/v7 baselines; **view 6 remains the outlier above 20%**;
  the **median of the eight lands 4–12%**; residual-after-attribution largest component stays
  **below the 4,882/5,068 E07 precedents** on at least 6 of 8.
- **P2e — achromatic mass rises slightly** (charcoal is achromatic; ivory is not). Predicted eight
  readings **9–18%** with largest component **< 25,000 px** on 7 of 8, and **view 4 stays the low
  outlier below 8%** at 770700.
- **P2f — registration.** Predicted **0.955–0.990** on all eight, wider than handoff 8's
  0.9687–0.9860 because a prompt term moved view 0 to 0.9620 at v6. **Separate pre-registration:**
  **0 or 1** of the eight paints a *vignetted* backdrop; if one does, its IoU collapses below 0.60
  and the **bbox check catches it before the number is believed** (handoff 10 §5). A vignetted
  twin is flagged as a projection keying hazard, not acted on.
- **P2g — views 1 and 5 will NOT reproduce the accepted pair, and that is expected.** Three added
  terms. Predicted **> 50% of pixels differ** on both. This is registered so the loss of a
  pixel-identity that held since handoff 8 is read as the directive working, not as a defect.
- **P2h — 0 credits, verified not assumed.** All sixteen reused inputs (eight clays, eight
  controls) return handoff 8's recorded content-hash names; `estimate_credits` returns 0.
- **P2i — the exemplar bar.** I predict my eye flags **at least one** defect on the eight that no
  armed number reports (three of four Director-caught defects were invisible to every instrument).
  If it flags none, I will say so plainly rather than manufacture one.

## Task 3 — E13 Gate 0, the projector's crop cameras

- **P3a — the anchor is EXACTLY 0 differing pixels.** The extended `project_twins.py`, invoked
  through the new `--ortho-scale` / `--centre` path at full-figure values, reproduces the recorded
  eight-camera projection **pixel-identical** — 0 differing pixels on the atlas PNG, on
  `_holes.png`, on `_styled_mask.npy`, and additionally on `_owner.npy` and `_blend.png`. Not
  "within tolerance"; **zero**. *Confidence: high — the parameters default to the values the tool
  already derives.* Any deviation halts E13 at zero spend and is the finding.
- **P3b — the baseline is established before the change, not after.** Predicted: **current HEAD**,
  unmodified, already reproduces `E04_anchor/final_8cam.png` at 0 differing pixels from
  `facet_E06/C1/prep` + the eight ARMB twins + `--edge-absolute`. If HEAD does *not* reproduce it,
  that is a finding about the anchor and the extension has not been tested at all — I halt there
  rather than comparing new code against a baseline I cannot reproduce.
- **P3c — bytes are not pixels.** I predict the anchor PNGs are **byte-identical too** on this
  path (same encoder, same machine), but the comparison that decides is **pixels**, and a byte
  mismatch alone would be reported as a non-finding per CLAUDE.md's standing rule.
- **P3d — nothing projects.** No crop projection runs. The capability is proven, not used.

## What would falsify the dispatch's own framing

Registered so it cannot be claimed afterwards:

- If **every** view binds every term at 770700 with zero re-rolls, Ruling 20a's seed caveat is
  weaker than the dispatch assumes on this stem set.
- If the nape stays ivory across all eight after being named, the founding law has a counter-case
  on this element and that is the session's headline, not a failure to report.
- If the Gate 0 anchor deviates by even one pixel, E13 halts and **no twin number in this report
  licenses a projection**, whatever Task 2 measured.

## The works-perfectly test, stated for each arm

- **The stems:** if the insertion did nothing, v8 would reproduce v7's stems exactly — so the
  ANDON's *pass* is the null result and the per-view count is the only evidence the term arrived.
- **The nape term:** does nothing → the twin reproduces its predecessor near-exactly at the pinned
  seed on views that gained only this term (view 4). Works perfectly → charcoal crest, ivory mass
  down, achromatic mass up.
- **The anchor:** cannot fail in the direction of *0 differing pixels being wrong* — a 0 here
  means the new path is inert at defaults, which is exactly what it must be. What a 0 does **not**
  prove is that the crop parameters do anything at all; that is E13's next gate, not this one.
