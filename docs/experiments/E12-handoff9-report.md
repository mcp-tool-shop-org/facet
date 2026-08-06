# E12 handoff 9 — the wing-skeleton term: v6 stems, views 0 and 4 regenerated

**Executor session, 2026-08-06**, executing E12 Ruling 17e. Predictions registered blind in
`02da393` ([E12-handoff9-predictions.md](E12-handoff9-predictions.md)), git blob `eef2956`,
written before the v6 rebuild and before this seat had opened either view at full size.

**0 credits. 2 generations. 0 re-rolls — both allowances remain.** Both jobs `succeeded`, zero
warnings. Watchdog verified alive before the local leg (heartbeat 0.4 s, VRAM 1,871 MiB against
the 31,200 ceiling); no Blender ran — controls and masks were reused byte-identical.

**The term worked, and it worked unevenly.** On view 0 the bone skeleton is gone entirely —
arms *and* finger struts read moss-green. On view 4 the **leading-edge arms went green and the
finger struts stayed cream.** That split is the result.

**Look at these before the numbers:** `AB_view0_v5_v6.png` · `AB_view4_v5_v6.png` ·
`AB_V4_CROWN_3x.png`.

---

## 1. The one variable, and why this comparison is unusually sharp

Enumerated in code against the v5 twin graphs: **exactly two entries differ per view** — node 7's
text (one term inserted at index 2) and node 15's output prefix. Clay, control, **seed**, steps,
cfg, denoise, cn-strength and the negative were each asserted identical by name; zero LoRA nodes.
All four reused inputs returned handoff 8's content-hash names, so they are byte-identical.

**The seed is pinned at 770700 — the same seed the v5 twins ran.** A term that did nothing would
have reproduced v5 almost exactly. So every difference below is attributable to one noun phrase,
which is a cleaner attribution than any re-roll comparison in this arc.

The v6 rebuild passed its ANDON on all nine stems: **remove the inserted term and what remains
is byte-equal to v5.** Entry 17 → 18 terms; per-view counts each exactly one greater; drop map
byte-identical.

## 2. Predictions scored — 6 held, 4 falsified, 1 held-by-eye-against-its-own-number

| # | prediction | outcome |
|---|---|---|
| **P1a** | the term claims the structure | **HELD on view 0, PARTIAL on view 4** — §3 |
| **P1b** | whole-figure ivory mass falls ≥ 40% on both | **view 0 −66.4% (held); view 4 −29.3% (FALSIFIED)** |
| **P1c** | *the gate number RISES as the defect leaves*, shoulder-dominated | **HELD on both** — 13.37% → 18.78% and 1.68% → 7.14%, shoulder 61.5% → 80.6% and 99.9% → 99.6% |
| **P2a** | the crown and horn ivory HOLD | **HELD** — and the number that appeared to contradict it was measuring something else (§4) |
| **P2b** | view 0's claws stay 0.39–0.77, view 4's stay ≤ 0.05 | **both mildly FALSIFIED** — 0.51 → **0.32** and 0.02 → **0.07** |
| **P2d** | membranes stay inside 13e's lit-translucency class | **judgement item, reported not ruled** — §5 |
| **P3** | achromatic mass inside the pair's band, components under 20,000 / 5,000 | **HELD on all four clauses** — 11.14% / CC 14,942 and 3.74% / CC 2,848 |
| **P4** | registration 0.975–0.990; a shift beyond ±0.005 means a prompt term moved the silhouette | **view 4 held (0.9856); view 0 FALSIFIED (0.9620) — and my stated INTERPRETATION of a large shift is falsified too** (§6) |
| **P5a** | the four uploads return handoff 8's names | **held** — all four |
| **P5b** | 0 credits, verified per submission | **held** |
| **P5c** | 0 re-rolls needed | **held** |
| **P5d** | the exact-one-term diff holds on all eight stems | **held** — nine, including the companion |

## 3. The wing skeleton — the result, and it is a split

`AB_view0_v5_v6.png`: in A the entire wing arm and finger skeleton is bone-white against the
membranes, unmistakably a bat-wing skeleton. In B the arms and every finger strut read
**moss-green**, matching the hide.

`AB_view4_v5_v6.png`: in A the same bone-cream skeleton runs the length of both wings. In B the
**leading-edge arms are moss-green** while the **finger struts crossing the membrane remain
cream.**

| view | whole-figure ivory mass, v5 → v6 | change |
|---|---|---|
| **0** | 94,184 → **31,601 px** | **−66.4%** |
| **4** | 96,197 → **68,023 px** | **−29.3%** |

The numbers and the eye agree on the split: view 0 clears, view 4 half-clears. Ruling 17e's two
pre-registered branches were *lands green* and *ivory persists*; **the measured outcome is
neither cleanly, and the difference between the two views is the finding to rule on.**

What this does **not** settle, stated because it is the obvious next question and no measurement
here answers it: whether view 4's residue is the term reaching the arms but not the struts on a
rear presentation, or the bat-anatomy prior holding a structure the term names, or a seed
accident. One generation per view exists. **No re-roll was spent**, because a re-roll tests
whether a defect is the seed's and the *interesting* question here is whether the term's reach
differs by presentation — which a second seed on view 4 would confound rather than separate.
Both allowances remain available if the ruling wants that seed.

## 4. The crown — held, and the box that said otherwise

**P2a is the discriminating regression check**: if the crown ivory left with the wing ivory, the
green term would be over-claiming.

| box | v5 | v6 |
|---|---|---|
| wide (700,180)–(1100,420) | 36.3% ivory | 23.5% ivory |
| **crown only (777,216)–(953,388)** | **41.1%** | **41.0%** |

**The crown is unchanged to a tenth of a point.** The wide box's apparent 35% relative fall is
entirely the **wing arms entering the same box at its lower corners** — cream in A, green in B.
The box was measuring the fix and reporting it as a regression. `AB_V4_CROWN_3x.png` shows the
ivory frill, horns and cheek spikes identical in both panels. **Check what your operands are
before reading a number from them** — the fourth instance in this repo, and the first where the
wrong box would have manufactured a regression rather than hidden one.

## 5. The rest of the view, scored — because a changed prompt re-rolls every landing

- **The gate rose on both views as the defect left.** Ivory sits at h 96.4, *inside* the adopted
  warm-olive band; D1's greens run h 119–137 against a band edge of 147.3, so hide green landing
  past 147 is *outside* it. Turning a large ivory structure green therefore moves mass from
  inside the band to its shoulder — 80.6% and 99.6% of the new off-palette is shoulder. **This
  is the second measured instance on this subject of a metric moving opposite to quality**
  (Ruling 17d was the first, when view 3's re-roll took its gate number from 0.36% to 11.11% by
  fixing a black hole). Registered before the run; held.
- **Achromatic mass held** on both views, inside the accepted pair's band, with no new dark mass
  of the view-3A kind.
- **The claws moved slightly, in opposite directions, and neither move is large.** View 0's ratio
  fell 0.51 → 0.32 — but its ivory count barely moved (5,347 → 5,058); the ratio fell because
  *charcoal rose* 10,484 → 15,809. View 4's rose 0.02 → 0.07 on 675 ivory px. The fangs term is
  untouched, so 17c's channel is not obviously disturbed; both are reported as data.
- **The membranes changed and it is a judgement item, not a measurement.** On view 0's v6 the
  trailing fields read a warm tan/peach where v5 read cream; on view 4 they read grey-to-cream as
  before. Ruling 13e's accepted class is *slate through the leading fields, cream where the
  trailing half is lit*. Whether view 0's warm tan is inside that class is the advisor's, and
  17f already named membrane cross-view variance a stage-1 watch item. **No twin is churned for
  it here.**

## 6. Registration — and a pre-registered inference rule of mine that was wrong

| view | v5 | v6 |
|---|---|---|
| 0 | 0.982525 | **0.962032** |
| 4 | 0.986011 | 0.985585 |

I registered that *a shift beyond ±0.005 would mean a prompt term changed the silhouette*. View 0
shifted −0.0205. **The inference rule is falsified, and the measurement says why:** of the 12,694
newly-keyed pixels, **12,101 (95.3%) lie OUTSIDE the geometry silhouette**. The v6 twin's bbox
matches geometry to 1 px on three edges and extends 7 px at the bottom — a stronger ground
shadow. The figure did not move; the generator painted more contrast just outside its boundary,
and the border-ring key caught it.

**A registration IoU built on a keyed mask measures paint placement as well as figure placement**,
and cannot distinguish them without the inside/outside split. That split is cheap and it is now
the honest way to read this number.

## 7. What this session does not settle

- **Whether either twin is good.** Both go to the advisor's eye, then the Director's.
- **Why view 4's finger struts kept their cream** while its arms went green and view 0's did
  neither. Three hypotheses named in §3, no arm run.
- **Whether view 0's warm-tan membranes stay inside 13e's class.**
- **Whether the v6 term should be re-run across the other six views.** They stand under v5 per
  17e; the term now rides their stems in the committed prompts file, so regenerating them is one
  paste whenever a ruling wants it — at the cost of breaking views 1 and 5's pixel-identity with
  the accepted pair.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions blob-pinned before the rebuild; the v6 build's full invocation saved as `E12_twins/build_v6.ps1`; each graph written before submission with content-hash input names; sidecar at birth naming the superseded v5 twins; seeds pinned and printed |
| ANDON_AUTHORITY | **3** | The exact-one-term ANDON checked in code against v5 read out of git, on all nine stems, before anything was submitted; pre-flight, topology and inverted no-LoRA scan per graph; `dry_run` + `estimate_credits` per submission; both bounded re-rolls left unspent with the reason stated |
| NAMED_COMPENSATORS | **3** | 0 credits; the v5 twins retained and named superseded, never overwritten; all new files suffixed `_v6`; `profiles/beast.json` and `canon/` untouched |
| DECOMPOSE_BY_SECRETS | **3** | The term is the only changed input, asserted in code; clay, control, mask and seed byte-identical or pinned; the fix reaches the run only through the committed builder reading the committed profile — no new flag was needed, because stems derive from the entry by deletion |
| UNCERTAINTY_GATED_HUMANS | **3** | Both twins halt to eyes; the view-0/view-4 split is handed up as the result rather than resolved by spending a re-roll that would confound it; the membrane question routed to the seat that owns it; two of my own errors scored in §4 and §6 |
| EXTERNAL_VERIFIER | **2** | Two generations against one named spec change with the seed pinned, so the term is the sole attribution; gate and achromatic channels run against baselines derived from artifacts this run did not produce. Marked 2 because each view rests on one generation, and `skip:` on a second model per the arc's precedent |

---

**Tasks 1–3 complete. HALT.** Both v6 twins, the sidecar, the A|B sheets and crops, the gate /
achromatic / registration tables and the scored predictions go to the **advisor's eye first**,
then the Director's. Stage 1 is handoff 10 and runs only after the completed twin set is ruled
in.
