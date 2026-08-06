# E12 handoff 2, Task 2 — predictions, written blind

**Executor session, 2026-08-05.** Committed **before the prep bake runs**: no
`E12_prep/` exists, `e08_ceiling` has not been pointed at anything, no thin-extent curve
has been computed, and no elevated-camera coverage has been measured. The status is
**blind** in the strict sense. The only dragon information in hand is Gate 0's own record
(`E12-gate0-report.md`), the profile, and the fixture.

The commit that carries this file is the proof of blindness; nothing in Task 2 runs before
it lands. My Gate 0 scorecard was **13 of 21**, and its named failure mode was *pricing the
dragon off the ship* — P1/P14/P19/P20 all did that, and the subject landed an order of
magnitude the other side of the character. That error is explicitly on the table below:
where a ship number is the obvious anchor, I say so and say which way I expect it to break.

---

## Priors, each checked to source this session

| prior | value | source |
|---|---|---|
| ship valid texels at res 4096 | 3,111,817 | E04 session record |
| ship stage-1 reach ceiling | 42.72% of valid | E04 pre-registration |
| character reach ceiling | 74.1% of valid | README / E08-eightcam |
| ship `pos.npy` off-surface | 2.5%, painted not padding | E10 Ruling 4 |
| character `thin_extent` | 0.03, **sized to the greatsword** | `character.json`, E08 Task 3 |
| ship `thin_extent` | 0.01, filament-derived | beast.json's own note |
| **tool** `thin_extent` default | **0.0 — the guard runs disabled** | measured this session, Task 1 |
| designated mesh | 986,825 f · 9 shells · extent 1.0017 / 1.0004 / 0.5743 · membranes closed slabs 1–2 px at render scale · 7,138 non-manifold edges through the folded wing | E12 Gate 0 |
| W3 face rect on this mesh | `rect_frac_of_figure` **0.5688** | E12 Gate 0 stats JSON |

---

## 2.1 — the prep bake

| # | prediction | falsified by |
|---|---|---|
| **Q1** | The bake completes **exit 0 with no ANDON**. | any assert firing |
| **Q2** | Specifically, `bake_hero_prep.py:216` (`assert n_head > 500`) does **not** fire, and `n_head` exceeds **100,000**. W3's crop rect covers 56.88% of this figure's projected area, so the "head band" it selects on a dragon is most of the front of the animal — the assert was written to catch an empty band and this band is enormous. **The band being huge is not the band being right**: it is inert at `head-scale 1.0` and Ruling 2 already decided allocation NONE. | the assert firing, or n_head ≤ 100,000 |
| **Q3** | Prep reports **native UVs** — it uses the atlas the mesh arrived with and does not re-unwrap (`smart_decimate` stays off-route, as `beast.json` predicts). | any re-unwrap, or a report that native UVs were unusable |
| **Q4** | Valid texels at `res 4096` land in **2.4M–3.6M**. The ship's 3,111,817 is the anchor and I expect the dragon **lower** — its surface area is 2.277 against the galleon's rigging-rich hull, and a big smooth membrane packs efficiently. | outside the band |

## 2.2 — the reach ceiling, pre-registered before any projection

| # | prediction | falsified by |
|---|---|---|
| **Q5** | Eight eye-level cameras reach **55–72%** of valid texels. Between the character's 74.1% and the ship's 42.72%, and nearer the character: a dragon hides less of itself than a ship (no decks, no interior), but the wings shadow the back and flanks in a way a standing human does not. | outside the band |
| **Q6** | The ladder **saturates**: the 12-camera set adds **< 3 points** over the 8-camera set. | ≥ 3 points |
| **Q7** | Reach is **above** the ship's 42.72% on every set of 8 or more. | any 8+ set at or below 42.72% |
| **Q8** | `pos.npy` off-surface rate at the >1 px threshold lands in **1–6%**, i.e. the same order as the ship's 2.5% — this is a bake artifact class, not a subject property, so here the ship IS the right anchor. | outside the band |

## 2.3 — `thin_extent`, measured fresh, membrane fraction reported separately

The membranes are the reason this subject exists, and the dispatch's warning is that a
filament-tuned value could withhold a third of them. My predictions are stronger than that
warning.

| # | prediction | falsified by |
|---|---|---|
| **Q9** | At the character's **0.03**, more than **50%** of membrane-field area is withheld. The value was sized to fill a *greatsword blade* solid; a membrane measured 1–2 px at render scale is far thinner than a blade. | ≤ 50% |
| **Q10** | At the ship's **0.01**, more than **15%** of membrane area is still withheld. | ≤ 15% |
| **Q11** | The largest value withholding **< 5%** of membrane area is **below 0.005**. | ≥ 0.005 |
| **Q12** | The thin mask is **concentrated**, not diffuse: at 0.03 the membrane-area fraction withheld is at least **3×** the whole-figure visible-area fraction withheld. This is the number that decides whether one global value can serve this subject. | ratio < 3× |
| **Q13** | The 7,138-edge pinch field behaves **differently from clean membrane** on the facing/visibility chain — measurably more withheld at the same value. | no measurable difference |

## 2.4 — the elevated-camera question

| # | prediction | falsified by |
|---|---|---|
| **Q14** | The eight eye-level cameras alone leave **> 25%** of up-facing surface area (normal_z > 0.5) unreached at first hit. The spread wing tops and the back are this subject's decks and they face the sky. | ≤ 25% |
| **Q15** | The best single addition by marginal gain is an **elevated pair**, not the single top-down. | top-down wins on marginal gain |
| **Q16** | **0/180 @ 55 beats 0/180 @ 40** on up-facing area. The wings are near-horizontal in this mesh's stance, so a steeper look sees more of them. | 40 ≥ 55 |
| **Q17** | After the best pair is adopted, unreached up-facing area falls **below 10%**. | ≥ 10% |
| **Q18** | Whatever is adopted **stays inside** `cull_unseen`'s default superset (which carries `0,55` and `180,55` but no 40s and no top-down), so **no union re-issue is needed**. If a 40-pair or a top-down wins, a re-issue IS needed and that is a finding for the ruling. | an adopted camera outside the 26-camera default |

---

## What I am not predicting, and why

- **Any adopted value.** `thin_extent` is measured and reported with its cost curve; choosing
  from the curve is the ruling's, not this session's.
- **Whether the reach ceiling is "enough".** `e08_ceiling`'s own docstring refuses that, and
  so do I.
- **The styled pair's appearance.** Task 4 generates it; the Director's eye is the verdict,
  and the fixture is authored forward precisely so nobody predicts it into existence first.
