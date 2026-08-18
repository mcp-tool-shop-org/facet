# E60 — the composer: canon → prompt → reference

**Advisor spec, 2026-08-18. One executor seat (Sonnet), background. Working tree
`E:\AI\training\facet_E60\`.**

**Direction (the Director, 2026-08-18, paraphrased):** the prompt that makes the reference
image should itself be informed by the detailed canon, so that painting the mesh later needs
less direction. Start from the top — detailed canon → prompt → a new reference image. He
separately removed the spend constraint for this window.

**Spend: 12 generations (4 arms × 3 seeds).** Not a scarcity ceiling — an experimental
design. Three seeds per arm exists because a one-seed comparison has no variance estimate
and this repo has been burned by n=1 readings; four arms because that is how many
research-grounded candidate forms exist. More seeds are available if a result is close.

---

## The question

Does a prompt COMPOSED from the ratified canon produce a reference at least as good as the
hand-written prose prompt that produced A1 — and which composition form survives attribute
binding best?

**Why this is the right next move.** A1's canon was *read off* an image, and that read lost
things silently: the positive half of the pose clause vanished, and face phrases leaked into
rear-view prompts. If the canon GENERATES the reference, nothing can be lost across that
step, because there is no interpretive step left to lose it in. The reference stops being a
source to interpret and becomes the canon's first test.

## Research grounding

Four parallel research agents, 2026-08-18. Every finding below carries its source; two
agents dropped citations that failed verification (one a mis-identified paper, one a
**fabricated industry statistic** whose number does not appear in the cited source), which
is why the ones that remain are usable.

**1. Entity count — not prompt length — drives binding failure.** Rassin et al., *Linguistic
Binding in Diffusion Models* (SynGen), NeurIPS 2023, arXiv:2306.08877: the accuracy gap
widens as modifiers per prompt grow, and repeated entities degrade every method tested.
Huang et al., *T2I-CompBench*, NeurIPS 2023, arXiv:2307.06350: **colour is the attribute
class models confuse most.** → *Design implication:* A1's prompt carries ~20 elements and
the failure is a colour one. Arm G tests consolidation directly.

**2. The mechanism matches our defect exactly.** Zarei et al., 2025, arXiv:2406.07844:
attribute embeddings leak across entities — in *"a green bench and a red car"* the **car**
token attends more to **green** than to its own **red**. → *Design implication:* plum → brown
with an olive under-vest is this failure, not a random miss.

**3. Grouping each entity with its own modifiers reduces it.** Feng et al., *Structured
Diffusion Guidance*, ICLR 2023, arXiv:2212.05032: constituency-parsed noun phrases beat a
flat token stream 42.2% win / 35.6% loss on the ABC-6K binding benchmark. → *Design
implication:* the composer emits **grouped prose**, and E58's flat comma list is the arm
predicted to lose.

**4. Our model is an LLM-encoder model, so CLIP-era tag habits do not transfer.** Qwen Team,
*Qwen-Image Technical Report*, arXiv:2508.02324: text is encoded by **Qwen2.5-VL**, not a
CLIP text tower. Saharia et al., *Imagen*, NeurIPS 2022, arXiv:2205.11487: scaling a T5-class
encoder buys more alignment than scaling the diffusion network. Betker et al., *DALL·E 3*
technical report, 2023: long descriptive **prose** captions were the biggest lever on prompt
following. → *Design implication:* prose sections, not tags. A flat comma list discards the
prepositions (*over*, *with fine gold embroidery*) that bind a modifier to its noun.

**5. ⚠ STRUCTURE ONLY HELPS WHEN IT IS THE RIGHT KIND — the finding that keeps this an
experiment.** T2I-CompBench measures a naive syntax-tree structuring approach at **0.499**
against a plain-SD2 baseline of ~0.51 — i.e. **no gain** — while attention-based structuring
reaches 0.64–0.66. → *Design implication:* a composer is a form of structuring, and the
literature says structuring can buy exactly nothing. **This is why Arm R (the hand-written
original) is in the design as a control that can win.** The composer is not assumed better.

**6. ⚠ A VLM IS THE WRONG JUDGE FOR "IS THE VEST PLUM", AND THIS CORRECTS THE ADVISOR IN
PLACE.** Earlier this session the advisor told the Director that the defects failing us are
"coarse questions — is the vest plum, is the face visible — which is what a VLM gate is good
at." **Measured false.** Butt et al., *GenColorBench*, 2025, arXiv:2510.20586: a general VLM
judge (Qwen2-VL-7B) scores **49% on binary colour verification** and **25% on named-colour
identification**; open-ended colour naming falls to **12%** for the best model tested, while
a narrow purpose-built method on the same benchmark reaches **92–96%**. Hayes et al.,
*FineGRAIN*, NeurIPS 2025, arXiv:2512.02161: three strong VLM judges reach only **74–76%**
agreement with human raters. → *Design implication:* **the colour half of any image-side gate
is facet's own Lab-band instrument, not a VLM** — this repo's narrow colour tooling is the
better instrument by a wide measured margin, and the prompt-craft adoption note is amended
accordingly.

**7. Prior art for the "same list used twice" gate exists and is named.** Cho et al.,
*Davidsonian Scene Graph*, ICLR 2024, arXiv:2310.18235 — decomposes a description into
atomic dependency-linked QA pairs precisely because naive QA generation (TIFA, ICCV 2023,
arXiv:2303.11897) hallucinates and self-contradicts. → *Design implication:* when facet builds
the image-side gate, its questions are atomic and dependency-ordered by construction, and the
naive form is known-bad rather than untried.

**8. What nobody has published — so this arc generates evidence rather than replicating it.**
No paper or shipped tool documents a typed-spec → prompt → same-spec-verification pipeline
with fidelity data; the one shipped analogue is a product page with no A/B. Scene-graph
conditioning beat text captions in **67.6%** of human comparisons and roughly doubled
per-object recall (Johnson et al., CVPR 2018, arXiv:1804.01622) — while scoring *worse* on
the automatic metric, which is its own lesson about who grades. **And no typed-spec →
cross-view identity-consistency number exists in the literature at all.**

## Stages

**Stage 0 — the composer (free).**
`tools/canon_compose.py`: canon file + view → prompt. Rules, each traceable to a finding:
- **Grouped prose in sections**, following the reference recipe's own shape: framing →
  staging → style → identity, the identity clause grouping each surface's occupant with its
  own modifiers and joining related garments with prepositions (finding 3, 4).
- **A view argument governs visibility.** Face-bearing clauses (eyes, smile, crisp facial
  features) appear only in views where the face is visible. This repo's own per-view law
  (E02: *a rear camera is never told about a beard*) is the authority; the composer is where
  it becomes mechanical instead of remembered.
- **`facing the camera` is never emitted for a non-front view** — it is view-specific
  staging and is deliberately excluded from `a1.surfaces.json`'s clause set for that reason.
- Every emitted prompt must pass `canon_gate.check_prompt` against its subject, including
  all `required: true` clauses. A composer that emits an ungated prompt is a defect.
- Tests ride the commit, and must include a can-fail leg: a rear-view compose that still
  contained a face phrase would fail.

**Stage 1 — anchor the composer against the known-good prompt (free).**
Compose A1 at the front view; diff against `canon/A1-RECIPE.json`'s positive text — the
prompt that produced the approved reference. This is **not** a byte match and must not be
tuned toward one. Report three sets explicitly: phrases in both; phrases the recipe has that
the canon does not (**canon debt** — the pose clause was one, and there may be more); phrases
the canon has that the recipe does not. **Gate 1:** if the composed prompt fails
`canon_gate`, halt — the composer is not shippable. Canon debt is *reported, not fixed*: a
canon edit is the Director's.

**Stage 2 — the four-arm A/B (spend 12).**
Everything held byte-identical to `canon/A1-RECIPE.json` except the positive text: same
model, sampler, scheduler, steps, cfg, negative text, latent size. **Seeds 106, 770700 and
one further pinned seed, recorded before submission; every arm sees the same three.**
- **Arm R — the original recipe text, verbatim.** The control. Seed 106 of this arm should
  reproduce `canon/A1_reference.png`; E58 measured that replay as pixel-identical, so this
  arm doubles as a venue re-anchor. If it does not reproduce, HALT — something moved.
- **Arm P — composed grouped prose.** The candidate.
- **Arm L — the E58 flat comma-list form.** The form predicted by findings 3 and 4 to lose;
  it is in the design so that the prediction can fail.
- **Arm G — composed prose with the garment consolidated** into fewer, richer noun phrases,
  testing the entity-count finding (1) rather than the grammar finding.

**Stage 3 — measurement (free), and it is deliberately narrow.**
Per image, against `canon/A1-palette.json`: does each declared material land in its declared
band, measured with **facet's own Lab instruments** (chroma floor before any hue; circular
hue statistics; per-region counts). **No VLM judges a colour in this arc** — finding 6.
Report per arm per seed: which of the ten NAMED elements are present and in-band, and which
are not. **Report the numbers; rank nothing.** The Director's eye chooses the reference.

**Stage 4 — the sheet.** Reference | Arm R | Arm P | Arm L | Arm G, one row per seed, at his
zoom, full-size PNGs on disk.

**Out of scope, named:** the head-turn fix (rear-view arms are a separate arc — do not test
per-view composition here, it confounds the form comparison); the twin ring; mesh work;
adopting `prompt-crafter` as a dependency; painting.

## Predictions

The seat states its own before Stage 2, blind status disclosed, each inside the interval its
instrument can return.

**The advisor's, recorded before the fact and falsifiable: Arm P beats Arm L on colour
landing, and Arm R beats or ties Arm P.** The second half is the one worth watching — finding
5 says structuring can buy nothing, and a hand-written prompt by someone who knows the
character is a strong baseline. **If Arm P loses to Arm R, the composer is not adopted**, and
the finding is worth more than the fix.

## Standards compliance

1. **PIN_PER_STEP — 3.** All non-prompt parameters byte-identical from the recipe; seeds
   pinned and recorded before submission; every emitted prompt saved with its image.
2. **ANDON_AUTHORITY — 2.** Gate 1 (composer emits an ungated prompt) and Arm R's
   reproduction check both halt; `raise`, never bare `assert`.
3. **NAMED_COMPENSATORS — 2.** Spend has no undo; the bound is the pre-registered design.
   Code and canon edits revert by pathspec.
4. **DECOMPOSE_BY_SECRETS — 2.** Composer / generation / measurement are separate stages over
   on-disk artifacts.
5. **UNCERTAINTY_GATED_HUMANS — 2.** The Director chooses the reference; the arc ranks
   nothing. Canon debt returns to him rather than being silently repaired.
6. **EXTERNAL_VERIFIER — 3.** The colour instrument is deterministic, external to the
   generator, and chosen over a VLM on measured grounds (finding 6) rather than by preference.

## Dispatch record (living)

- 2026-08-18 — spec written after a four-agent research pass. Finding 6 **corrects an advisor
  claim made earlier the same session** on a public-facing recommendation; the correction is
  in the grounding section above rather than in a deleted sentence, per this repo's rule that
  the correction is more useful than the original.

- 2026-08-18, at the fold — **THE ADVISOR'S PREDICTION IS FALSIFIED, AND THE GATE IS
  IMPLICATED IN ITS OWN EXPERIMENT.** The spec predicted *Arm P beats Arm L on colour
  landing*. Measured: Arm L — the flat comma list, the form findings 3 and 4 predicted would
  lose — **held the garment at all three seeds**, while the composed prose arms P and G
  rendered the sleeveless vest as a **full-sleeved coat** at seeds 106 and 770700, hue moving
  63.6–66.8° on N2 with the cream sleeve occluded entirely. Arm R reproduced the reference
  pixel-identically at seed 106 (0 of 1,672,192 differing), so the venue is re-anchored and
  nothing else moved.

  **The mechanism is ours, not the model's.** `canon_gate`'s reverse check strips licensed
  phrases and then permits only a fixed connective list —
  `a|an|the|with|and|or|of|on|in|at|to|for|from|by|as|his|her|its|their|this|that|each`.
  The reference's own recipe joins the two garments with **"over"** (*a plum long-vest …
  over a cream high-collared shirt*), and **"over" is not on that list**, so the composer was
  structurally barred from the one preposition that encodes the layering. `canon/A1-IDENTITY.md`
  already recorded that the raw recipe fails the gate for exactly this reason and nobody had
  read it as a design constraint. **The gate built to protect the canon forbade the word
  carrying the garment's structure.**

  **The seat did not resolve it and was right not to.** Two explanations fit — the prose form
  itself, or the missing preposition — and its instruments separate neither. The
  discriminating re-run is one arc.

  **And the canon gap underneath is the Director's.** Nothing in `a1.surfaces.json` declares
  the vest **sleeveless**. W3's canon carries explicit machinery for precisely this — the
  upper arm occupied by `kind: bare` with `forbidden: ["sleeve"]` — and A1's has none: it
  assigns the sleeves to the shirt but never denies them to the vest. **The reference got its
  sleevelessness from a preposition, not from canon**, which is the class of silent dependency
  this whole reference-first line exists to expose.

  **Two repairs proposed, the second preferred.** (1) Admit spatial prepositions to the
  connective list — they carry no material claim, and `on` is already admitted, so the
  exclusion of `over` is an inconsistency rather than a policy. (2) **License the JOINT
  phrases**: `a1.surfaces.json` already declares `vest_shirt` as *"plum vest edge against
  cream shirt"*, and a joint IS a layering relationship — licensing joint phrases lets the
  composer say *worn over* **from canon** instead of from a hardcoded word list, which is the
  fix that generalises.

  **Also folded here, and NOT this seat's work nor the advisor's:** the negation-window
  repair in `canon_gate._present` / `_neg_window`, authored in a concurrent session the
  Director started from a flagged chip. Its own finding, reproduced: in the recipe's positive
  text the 24 characters before *"no held objects"* are *"l features, no weapons, "*, so the
  negator belonging to the PRECEDING list item leaked forward and **two of A1's three staging
  clauses read absent while textually present and unnegated**. The fix cuts the look-back at
  the nearest clause boundary and declares the opposite error it accepts. Recorded as separate
  authorship because a fold that silently absorbs another session's work misattributes it.

  Reported, not fixed: raw ΔE-against-the-reference is **confounded by seed-to-seed lighting
  variance** — Arm R's own verbatim text reads "missed" at non-anchor seeds — so it is not an
  in-band instrument and no arm may be graded on it. And the seat **disclosed that it recorded
  no numeric predictions before Stage 2**, refusing to backfill them after seeing results,
  which is the one place the discipline is most tempting to break.
