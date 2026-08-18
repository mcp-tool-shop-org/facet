# E55 — can the plates we already paid for separate element COUNT from element IDENTITY?

**Dispatched 2026-08-17 by the advisor seat. Opus executor, background, open line.**
This document is the spec. Mid-flight rulings are appended here with dates.

**Opus rather than Sonnet, and the reason is stated:** this seat must *design an instrument
rather than run one*, and the failure mode is a measurement that looks sound and is
measured against the wrong object. That is the expensive-and-hard-to-detect class.

---

## The question, and why it is now load-bearing

`canon_gate` requires **25 phrase checks** for W3 at subject scope. Brief #19's research
grounding surfaced a measurement pricing each additional prompt component at **~8.53% of
mean component-inclusion score**, with quality falling alongside (Foong, Kotyan, Mao &
Vargas 2023, arXiv:2311.13620, N=175,918) — over a tested range that **tops out well below**
our density. Binding one attribute to one object already fails ~41% of the time
(T2I-CompBench++, arXiv:2307.06350); at two objects DALL-E 3 scores 0.45 (GenEval,
arXiv:2310.11513).

If that transfers, the canon gate is enforcing a prompt the generator cannot render, and
`scopes` stops being a convenience and becomes the mechanism that makes the canon
renderable at all. If it does not transfer, the 25 is fine and scopes are ergonomics.

**Nobody knows which, and the outside channel's judgement was that the cheap settlement is a
re-read of plates already paid for rather than a generation.** That is your job.

⚠ **Correct the advisor's own framing before you use it.** Brief #19 stated this tension
against the wrong number. W3 is **24 prompt surfaces / 25 required gate checks / 19 unique
elements**, and the cited slope is about *distinct elements*. Any comparison you build uses
the element count, not the gate-check count. `tools/canon_worksheet.py`'s density readout
prints all three; read it rather than re-deriving.

## The confound, named up front — this is the whole experiment

Every recorded arm differs in **more than one thing**. In particular, element **count** and
element **identity** move together across the arms on disk:

- **N11** (`a gold plate on each outer forearm`) is absent at *low* density (the patch arm,
  median ΔE 1.07) **and** at *high* density (the 16-element from-scratch SPEC arm, E53:
  forearm reads C\* 20.5 / h 54.1, inside the leather cluster).
- **N9** (`green cloth panels in the kilt`) is present at high density **and** arrives with
  no prompt at all (Amendment 16).

So on the two elements we know most about, **outcome is invariant to count and tracks
identity.** That is either the answer, or it is two data points doing the work of a study.

**Your first duty is to decide whether these plates can separate the two factors at all.**
A clean *"the existing evidence cannot separate count from identity, and here is precisely
why"* is a **full success** and is the outcome the advisor considers most likely. Do not
manufacture a separation to have a result.

## The corpus — enumerate it before you design anything

Under `E:\AI\training\facet_E08\`: `SPEC/`, `N11/`, `BRACER/`, `ARMOUR/`, `CONTRA/`,
`ANCHOR/`, `ARMB/`, `A2/`, `A2R/`, `A3/`, `A4/`, `BG/`, `BG2/`, `armA/`, `gate0/`, `LOOK/`.
Several carry a `w3clay_0_gen.json` with the **prompt as generated**; `SPEC/` does **not**
(a provenance gap E53 found and reported — do not treat its absence as a missing arm).

Repo-side: `docs/experiments/E08-spec-prompt.json`, `E08-contradiction.json`,
`E08-armB-prompts.json`, `E08-brush-prompts.json`, `E08-cloud-build-order.md:76` (the prompt
that made the shipped twins), `canon/w3.surfaces.json`, `canon/W3-IDENTITY.md`.

**Enumerate the resource before commissioning one.** This repo has commissioned things that
already existed at least five times and the advisor invoked that law three times today.
Before writing any instrument, check `tools/` — `canon_gate.py`, `canon_worksheet.py`,
`palette_gate.py`, `diagnostics/e08_deltaE.py`, `evidence.py`, `flat_trace.py` and
`tools/verify/montage.py` all exist and several do part of this.

## What a sound design has to hold

1. **One prompt, many elements: the unit is the ELEMENT-ARM PAIR.** For each recorded arm,
   the observation is *(this element, in a prompt of N elements, landed / dropped /
   unassessable)*. Unassessable is a real third state — E53 established that the
   sword-gripping forearm has **no visible surface in this camera in any arm, canon
   reference included**. Forcing it to a binary is the error that law warns about.
2. **The outcome measure must not be a proxy.** *Did this named element appear on its
   surface* is the question. A high-pass statistic, a global ΔE, or a palette count answers
   a different question — E07 lost four arms to exactly that. Where an element's presence
   can only be decided by eye, say so and put it on a sheet.
3. **Calibrate the instrument's range before predicting.** State what your measure reads
   when an element is *definitely present* and when it is *definitely absent*, on this image
   family, before any arm's number is read. A prediction outside that interval could not have
   been right at any state of the world.
4. **Say which side your evidence can close.** *This element is absent here* is decisive
   about that arm. *This element is present* does not tell you the prompt caused it — N9
   arrives unprompted, and that single fact voids a whole class of "it landed, so naming
   works" reasoning.
5. **Report n honestly.** If the design yields five usable observations, the report says
   five, and does not fit a slope to them.

## Gates — halt and report, never improvise past one

- **Gate A — the prompts are what the record says.** For every arm you use, establish the
  prompt text from a primary artifact (`w3clay_0_gen.json` or the committed JSON), not from
  a report's paraphrase. If an arm's prompt cannot be established, **exclude it and say so**;
  do not infer it.
- **Gate B — the element count is derived, not asserted.** Count elements by a stated rule
  applied identically to every arm, and print the rule. Two arms counted by different rules
  is the defect this whole spec exists to avoid.
- **Gate C — the instrument reproduces a known number.** Before any new reading, reproduce
  one figure the record already publishes (E53's BRACER forearm `[65,39,26]` / C\* 18.5, or
  E08's contradiction ΔE for a named element). If it does not reproduce, **halt** — your
  instrument is not comparable to the record.
- **Gate D — write only under `E:\AI\training\facet_E55\`.** Every other `facet_E*` tree is
  read-only. Do not read the `facet_E50`–`E54` working trees.

## Predictions

Write `predictions.md` **before** reading any arm's pixels. Predict at minimum:

- **P1** — whether the corpus can separate count from identity at all, stated as a yes/no
  with your reason and what would falsify it.
- **P2** — the number of usable element-arm observations you will end up with, as a band.
  ⚠ **This repo has missed on population-shaped predictions for twelve consecutive arcs.**
  Check that every member of your population *has* the property you are counting before you
  predict how many there are, and state each clause of any conjunction separately.
- **P3** — if a separation is possible, its direction; if not, what the minimal experiment
  that could settle it would cost.

Disclose blindness honestly: you will have read this spec, which argues the
identity-dominates reading in the confound section on purpose.

## Terminus

A report, and — where presence is an eye question — a sheet at the Director's zoom, native
pixels, defects first, reusing `tools/verify/montage.py` or `tools/evidence.py`. Seven seats
have each written their own sheet builder in this repo; an eighth is avoidable.

## Rules that bind this seat

1. **Never judge whether output is good.** The words *verified, shipped, works, decisive,
   validated, proven* do not belong in the report. You measure; the Director judges.
2. **A negative result is a full success**, and here it is the expected one.
3. **Stop at every gate.** Do not change a parameter and re-run.
4. `handoff.md` first, kept current. Transcripts have been lost mid-arc here twice.
5. Do not delegate your core measurement to a child agent.
6. Do not commit; leave the change-set uncommitted. Do not `git add -A`. No memory-store writes.
7. **Zero spend** — no GPU, no cloud, no generation. This arc reads plates already paid for.
8. Gates `raise`, never a bare `assert`. Tests ride any tool change — **next free test file
   for you is `t95`** (`t94` is reserved for the outside channel; verify before claiming it).
9. Absolute python `E:\AI-Models\trellis2-env\Scripts\python.exe`; `pytest` needs
   `--basetemp=<scratch>`; `argparse` eats leading minus signs; scripts create their own dirs.
10. **Read every listing complete** — no `head`, `tail`, `Select-Object -Last` on anything
    that decides a number.
11. **The count surfaces (T34) are the advisor's** — currently 1295 / 1241 / 54. If your
    change-set adds tests, state what it assumes and reconcile nothing.

## Out of scope

Any generation. The canon schema. `canon_gate.py` and `canon_worksheet.py` (a second builder
is live in those). The scope lists — filling them is a human walk. Whether the canon *should*
require 25 checks; that is the Director's, and this arc supplies the evidence for it.

## Standards compliance

| standard | score | evidence |
|---|---|---|
| PIN_PER_STEP | 2 | Every input artifact is named by path and the seat must cite primary prompt JSONs rather than report paraphrases; scored 2 because this dispatch does not pin the executor's own model/prompt hash into the arc manifest. |
| ANDON_AUTHORITY | 3 | Four gates with halt conditions; Gate C halts on the instrument failing to reproduce a published figure, which is the direction that voids every downstream number. |
| NAMED_COMPENSATORS | 3 | Writes confined to `facet_E55\` plus one repo report. Compensator is delete-the-tree; owner is the advisor. No irreversible call exists in this arc. |
| DECOMPOSE_BY_SECRETS | 2 | Prompt extraction, element counting, presence measurement and sheet building are separable and the seat is told to reuse existing tools; the module boundary is the seat's to choose. |
| UNCERTAINTY_GATED_HUMANS | 3 | No pass condition, deliberately — the *suspend rather than invent one* precedent. The terminus is a sheet plus separated numerators for the Director's eye, and the escalation (does the canon's 25 stand) is explicitly his. |
| EXTERNAL_VERIFIER | 2 | Gate C forces agreement with a figure produced by a different seat with a different instrument. Scored 2 because no second differently-sourced computation over the same pixels is required. |

**No pass condition, by design.** No calibrated threshold exists for "how much does count
predict drop," and inventing one while looking at the arms is retuning however principled the
reasoning.
