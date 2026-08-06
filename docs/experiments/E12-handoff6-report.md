# E12 handoff 6 — the regeneration under the corrected canon

**Executor session, 2026-08-06.** Predictions registered blind in `8d02517`
([E12-handoff6-predictions.md](E12-handoff6-predictions.md)), git blob `e833abf`, sha256
`8d80da50…`, written before the v5 rebuild, before any upload, and before this seat had opened
a single PNG. This report ranks nothing and attaches no verdict; the Director's one sentence —
*does this read as the dragon he wants* — is his.

**0 credits.** `estimate_credits` before each of the two submissions: *"0 credits — no paid API
nodes found in this workflow."* **Two generations. Both bounded re-rolls UNSPENT** — the
reasoning for not spending view 1's is in §6 and is the one discretionary call in this
dispatch. Both jobs `succeeded` with zero warnings.

**Look at these before the numbers:**
`repaint_v2/AB_view5_sameseed_oldpalette_vs_new.png` ·
`repaint_v2/AB_AB_TAILUNDER_3x.png` · `repaint_v2/AB_AB_WINGARMS_3x.png` ·
`repaint_v2/ABC_view5_progression.png` · `repaint_v2/AB_V1_LEGS_3x.png` ·
`repaint_v2/FEET_view1_4x.png` beside `repaint_v2/FEET_view5_4x.png` ·
`repaint_v2/ABC_WINGRIM_7x.png`.

---

## 0. Environment

| leg | result |
|---|---|
| watchdog | **DEAD at session start** — heartbeat 12.78 h old (last 02:56:01), no watchdog process. **Restarted** under the dispatch's standing authorization before any local leg: `stale heartbeat (0.5d old) — previous watchdog died hard. Clearing.` → `watchdog UP — kill@ VRAM 31200 MiB`. Re-checked live: heartbeat age 1.0 s, VRAM 2,181 MiB against the 31,200 ceiling. The ceiling was not touched |
| GPU work | **none local.** Generation is cloud-only; every local leg this session is CPU image compositing and colour arithmetic. No Blender ran |
| working copy | clean at session start and at every commit; **explicit paths only**, never `git add -A` (the handoff-5 finding) |

## 1. Predictions scored — 9 held, 3 falsified, 4 partial

Full text in the predictions file; the branch each falsification landed on was **named there
before the run**.

| # | prediction | outcome |
|---|---|---|
| **P1a** | view 5 clears the bone reads decisively | **held** — §3 |
| **P1b** | view 1 clears at the limbs; pale mass confined to horns, crown spikes, tooth rows | **PARTIAL, and it falsified on its own named branch** — the limbs cleared, the **claws did not** (§4) |
| **P1c** | both halves leave — declared canon *and* family-pressure invention | **partial** — both left on view 5; on view 1 the declared half left and the family-pressure half persists (§4) |
| **P2a** | D1's moss-green holds on view 5's haunch/shoulder/hindquarter at seed 770700 | **held** — §3 |
| **P2b** | D3's membranes hold storm-grey on view 5 | **PARTIAL** — a slate-to-pale gradient, not a uniform storm-grey, and not the companion's orange (§5) |
| **P2c** | view 1's head elements hold — D4 horns, D10 tooth rows, D2 throat bands | **held** — §5 |
| **P3** | the wing-rim mouth artifact does NOT recur | **held** — 0 px, and 0 px in the whole frame (§5) |
| **P4a** | D6 spines and D7 claws land as dark neutrals | **SPLIT** — D6 landed on both views; D7 landed on view 5 and **not on view 1** (§4) |
| **P4b** | charcoal separates from storm-grey; no collision with slate | **held** — §5 |
| **P4c** | no grey invention on green-declared surfaces | **PARTIAL** — no grey wash on the hide, but charcoal reached a surface no grey term names (§4) |
| **P5a** | the four uploads return the four recorded content-hash names | **held** — all four exactly |
| **P5b** | 0 credits on both submissions | **held** |
| **P5c** | both allowances unspent | **held on spend**; whether view 1 *needs* its re-roll is not this seat's call (§6) |
| **P5d** | the builder's ANDON fires on the companion's stale drop strings | **held** — fired deliberately first: exit 1, no file written |
| **P5e** | `headclay_0`'s D6 rationale is void under the correction | **held** — recorded in the file, not repaired here (§7) |
| **v5 file** | 17 terms · counts 17/17/17/11/13/11/17/17 + 15 · full-string views {0,1,2,6,7} · drop map byte-identical · exactly 3 substituted terms per `dragonclay` stem and 1 in `headclay_0` · **view 5's stem carries zero pale-bone words** | **every clause held**, checked in code against v4 read out of git |

### Three corrections this seat owes on its own method

1. **The predictions proposed pre-computing the upload names as sha256 of the file bytes. That
   is wrong**, and it was measured wrong *before* any upload: the local sha256 of all four
   inputs matches none of the recorded names (`dragonclay_1_control.png` hashes to
   `102c888c…`, recorded `7501744e…`). The cloud's content hash is not plain sha256 of the
   file, so byte-identity is confirmable only **at** upload — which is where handoff 4
   confirmed it and where this dispatch confirmed it. The check was right; the shortcut was
   not, and it would have read as a four-way input mismatch halt if taken at face value.
2. **An eyeball reading of mine was overturned by measurement.** Looking at the head at 3× I
   read D5's cheek and jaw spikes as *"gone dark where they were ivory."* The tight box says
   they carried **41 px of the pale family in the old arm and 36 px in the new**, out of
   15,500 — no ivory in either. The ivory I was seeing was the crown spikes higher up. What
   changed at the cheek fan is **green → charcoal**, not ivory → charcoal.
3. **My first D5 box was the wrong operand** — (395,235)–(650,410) contains D4's horns and a
   large field of hide, so its 10.95% → 8.25% understates a change that is plain at 5×. Both
   boxes are reported below; neither is dropped.

## 2. What was actually varied

Enumerated in code against handoff 4's submitted graphs, not asserted. **Exactly two entries
differ per view**: node 7 `CLIPTextEncode.text` and node 15 `SaveImage.filename_prefix`. The
clay render, the control, the seed, steps, cfg, denoise, cn-strength and the negative were each
checked **identical by name** rather than merely absent from the diff, and both graphs carry
**zero LoRA nodes**. All four uploaded inputs returned the content-hash names handoff 4
recorded, so the two images and two controls are byte-identical to that run's.

**Seed 770700 on both views — the seed that produced the Ruling 11d misses on view 5.** That is
the point: if the canon is the lever, it has to work at the seed that was worst.

## 3. View 5 — the Director's named defect, at the seed that carried it

`AB_view5_sameseed_oldpalette_vs_new.png` is the whole finding in two panels. In A the tail's
blade rows are white, a **smooth white rib-shaped element runs the length of the tail's
underside**, and every wing arm and finger is bone-white. In B, at the same seed and the same
control, the blades are charcoal, the rib is gone, and the wing arms and fingers wear D1's
moss-green with dark claw tips.

**Pale-bone family** (CIELAB D65, L\* ≥ 62 **and** C\* ≤ 20; hue not quoted — this family is
defined by low chroma), masked to the geometry silhouette because the ruled lavender-grey
backdrop sits *inside* the band and an unmasked count would be mostly backdrop. Total and
largest connected component both reported.

| region (px of masked area) | A · 770700 old | B · 770701 old (the SEED move) | C · 770700 corrected (the CANON move) |
|---|---|---|---|
| LEGS (83,069) | 8,498 · 10.23% · CC 1,394 | 9,424 · 11.34% · CC 3,326 | **2,636 · 3.17% · CC 237** |
| TAIL UNDERSIDE (64,689) | 14,056 · 21.73% · CC 5,734 | 12,788 · 19.77% · CC 5,281 | **1,679 · 2.60% · CC 607** |
| WING ARMS (145,734) | 47,998 · 32.94% · CC 34,754 | 13,717 · 9.41% · CC 2,482 | **15,649 · 10.74% · CC 9,403** |
| MEMBRANE (125,776) | 46,879 · 37.27% · CC 15,637 | 10,599 · 8.43% · CC 4,529 | **16,564 · 13.17% · CC 9,334** |
| **WHOLE FIGURE (490,941)** | **140,970 · 28.71% · CC 38,263** | **63,820 · 13.00% · CC 6,828** | **37,736 · 7.69% · CC 9,403** |

Read as a progression rather than as three numbers: **the seed move took the figure 28.71% →
13.00%; the canon move, back at the seed the seed-move was run away from, took it 28.71% →
7.69%.** The residual in C is concentrated in the wing/membrane fields, not at the legs or the
tail — its largest component (9,403 px) is the membrane's pale trailing half, described in §5,
and not a bone read.

**P2a held:** the haunch, shoulder and near hindquarter wear moss-green with individual plates
legible, at the seed that painted them pale tan under the old palette.

**These are diagnostics and not gates** (Ruling 10d). No threshold above decides anything; the
sheets are the evidence and the eye rules the E07 class.

## 4. The finding: family bleed persists on view 1, and it runs in both directions

This is the part of the dispatch that did not go as predicted, and it is the most useful thing
measured here.

**Same element. Same subject. Same seed. Same recipe. Two views, two outcomes.**

`FEET_view1_4x.png` beside `FEET_view5_4x.png`:

| | view 1 stem (17 terms, carries `bone-ivory` ×2 + `pale ivory fangs and tooth rows`) | view 5 stem (11 terms, **zero** pale-bone words) |
|---|---|---|
| D7 `charcoal claws`, feet box | old 1,185 px · 5.46% · CC 314 → **new 1,113 px · 5.13% · CC 305** | old 2,574 px · 13.48% · CC 803 → **new 199 px · 1.04% · CC 17** |
| to the eye at 4× | **ivory claws, unchanged from the old arm** | **near-black claws** |

The correction moved D7 by 92% on the view whose stem has no ivory in it, and by nothing
(−6% relative, inside the noise of the box) on the view whose stem still does.

**And the trade runs the other way at the same time.** On view 1, D5's cheek and jaw spike fan
— declared `bone-ivory` — carries essentially no pale family in **either** arm (41 px old,
36 px new of 15,500) and reads **green in the old arm and charcoal-brown in the new**
(`AB_V1_CHEEKFAN_6x.png`). A grey landed on a surface that no grey term names, on the view that
gained two charcoal terms.

**Mechanism, offered as a labelled hypothesis with its evidence, not as a finding:** a colour
term appears to reach structures that **resemble** the structure it names, not only the
structure it names. View 1's string says `pale ivory fangs and tooth rows`; its claws — pointed
keratin of the same kind — take ivory, over the top of `charcoal claws` in the same string.
View 5 drops the fangs term and its claws take charcoal. If that reading is right it is the
same class as handoff 5's wing-rim serration resolving as a mouth, and it has a fixture
consequence the advisor owns: **the 9d/10i drop map's job may be larger than "hide what a view
cannot see" — a term can paint a surface it does not name.**

What this does **not** say: that P4c was simply wrong. Its headline held — there is no grey
wash down the flanks and the hide is green on both views. What is falsified is its *reasoning*,
that `charcoal` having no anatomical referent makes it inert. It does not invent anatomy; it
does bleed. The correction moved family mass from pale to grey (5 terms → 3, 2 terms → 4) and
**the bleeding moved with it.**

## 5. The rest, measured

- **The wing-rim mouth artifact does not recur.** The instrument was re-measured against the
  record before a new number was read from it: on the transcribed box it returns **0 px on
  770700-old and 273 px on 770701-old**, both published figures reproduced exactly. It returns
  **273 px on the whole frame** for 770701, which resolves the report's box-size ambiguity —
  the artifact is the only red/pink in that frame. On the new output: **0 px in the transcribed
  box and 0 px in the whole 1792×1024 frame.** `ABC_WINGRIM_7x.png` shows a plain membrane fold
  in panels 1 and 3 and the gaping mouth only in panel 2.
- **D6 landed on both views** — charcoal blade rows the length of view 5's tail, and view 1's
  tail spines went from bright ivory to dark (`AB_V1_TAILUNDER_3x.png`).
- **D3 is a gradient, not a colour.** On view 5 the membranes read slate-grey through the upper
  and leading field and pale cream toward the trailing edge; MEMBRANE-box pale mass 37.27% →
  13.17%. It is not the old arm's bone-ivory and it is not the companion's orange/rust. Whether
  a lit translucent membrane reading pale where light passes through it is a miss on
  `storm-grey` is a judgement, not a measurement.
- **P2c held.** D4's horns stay the dominant pale mass on view 1 (39.57% → 32.11% of the horn
  box — still ivory to the eye); D10's tooth rows read white; D2's throat and belly bands read
  olive-tan. **D8's ember-orange eye landed on view 1 in both arms** (`AB_V1_HEAD_3x.png`) —
  worth recording beside Ruling 12g, since the eye did *not* appear on the bust-scale companion
  at ~33× the pixels.
- **D9/D11**: view 1's cavity reads wine-dark with white teeth — D9's colour on the cavity,
  D11's slate absent, the same pair-scale behaviour Ruling 12c banked. View 5 drops the whole
  mouth family and shows none of it.
- **P4b held**: charcoal spines against mid-grey membranes separate by lightness at 3×, and
  charcoal never meets slate — the mouth interior is inside the cavity and is dropped from view
  5 entirely.

## 6. Why neither bounded re-roll was spent

View 1's D7 miss is a spec violation on a named element's surface, which is the Ruling 11d
class where the re-roll precedent applies. The allowance exists and was not used. The reasoning,
stated so it can be overruled:

**A re-roll tests whether a defect is the seed's. This one is measured not to be.** View 5
carries the same element, at the same seed, under the same control and recipe, with the ivory
terms absent — and it lands charcoal. That cross-view control at a fixed seed is a stronger
test of the cause than a seed change would be, and it is already in hand at zero spend. Ruling
12e's own sentence applies unchanged: *the seed is not the lever, the canon is.* Spending an
allowance against a cause the evidence locates elsewhere would buy a second sample of a
canon-caused effect and leave nothing for a case that needs it.

**Both allowances remain unspent and available to the advisor or the Director.** If the call is
that view 1 should be re-rolled anyway, nothing here forecloses it.

## 7. What this session does not settle

- **Whether any of it is good.** Both outputs, the progression sheet and every named crop go to
  the advisor's eye and then the Director's. His question was pre-stated by the dispatch.
- **Whether the resemblance hypothesis in §4 is right.** It rests on two views of one subject
  in one session. The cheapest test the advisor could specify is one generation of view 1 with
  the fangs term dropped — which would be a new arm, not a re-roll, and none was run.
- **Whether D3's trailing-edge pale is a miss.** Measured and described; not judged.
- **`headclay_0`'s void rationale.** v4 justified dropping D6 from the companion partly as
  *"the ivory family is already carried by D4/D5/D10, so the shoulder-end spines keep their
  colour by family."* Under the correction D6 is charcoal and no other term in that stem carries
  it, so those spines have no declared colour. The out-of-frame clause stands on its own, so the
  stem was built exactly as the dispatch instructs and the void clause is recorded **in the
  prompts file** for the advisor. **No fixture or profile was edited from this seat.**
- **Bands and the D8 closure** (handoff 4's Task 3) stay acceptance-gated.

## 8. Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | **3** | Predictions hashed, blob-pinned and committed before the rebuild and before any upload; the v5 build's full invocation saved as `repaint_v2/build_v5.ps1`; each saved workflow JSON IS its submitted graph, carrying the content-hash input names; both prompt_ids, both cloud filenames and the whole 770700 seed lineage in the sidecar, written at birth before the outputs were looked at |
| ANDON_AUTHORITY | **3** | Watchdog found dead, reported, restarted and re-checked before any local leg; the prompts builder's ANDON fired deliberately on stale drop strings before the tool was trusted (exit 1, no file); pre-flight + link topology + inverted no-LoRA scan before each submission; the graph diff asserts the pinned inputs identical **by name** rather than inferring it from absence; `dry_run` then `estimate_credits` before either execution; no skip flag anywhere |
| NAMED_COMPENSATORS | **3** | Every write lands in the new `repaint_v2/` subdirectory or is a new repo file; the two rejected/superseded view-5 artifacts are read, never moved, so the handoff-4 and handoff-5 sidecars stay valid; prompts v4 preserved in git history; 0 credits; both re-roll allowances left unspent |
| DECOMPOSE_BY_SECRETS | **3** | The prompt is the only changed input, enumerated in code against the prior submission; the canon correction reaches the run only through the committed builder reading the committed profile; controls, frames, canny, register and seed all pinned to recorded values and confirmed byte-identical at upload |
| UNCERTAINTY_GATED_HUMANS | **3** | Every outcome halts to eyes; the §4 mechanism goes up as a labelled hypothesis with its evidence, not a conclusion; the one discretionary call (not spending view 1's re-roll) is stated with its reasoning so it can be overruled; three corrections to this seat's own method are in §1 rather than quietly fixed |
| EXTERNAL_VERIFIER | **2** | The family instrument was re-measured against two published figures on two published artifacts and reproduced both exactly before any new number was read from it; the cross-view control at a fixed seed tests D7's cause from a direction the generator does not control. Marked 2 because both readings rest on one generation per view, and `skip:` on a second model per the arc's precedent |

---

**Both tasks complete. HALT.** Everything staged goes to the **advisor's eye first, then the
Director's**. Handoff 4's Task 3 remains acceptance-gated behind that look; nothing past the
halt was run.
