# Measurement conventions

*How a measurement tool reports that it could not measure, kept separate from how it
reports what it found. One convention, named once, so the next instrument does not
reinvent it — or worse, hides a withhold inside a "measured" number.*

---

## Enumerated first

Before this page existed the convention lived in one place: `tools/s3_run.py` exits 4
for "could not run" (missing `--aov` input), distinct from exit 2 ("ran, and the input
was bad" — an `ANDON`) and exit 0 (ran, succeeded). That is the whole precedent this
page generalises — one site, promoted to a convention because a second instrument
(E61's sleeve-occlusion readout) needed the identical distinction and had nowhere to
cite it from.

Checked before writing this page, not assumed: `docs/tools.md` (stale since the E19
move, does not mention any tool built after E19 — wrong shape, a dead reference doc, not
a place a live instrument should cite), `docs/known-defects.md` (a catalogue of specific
measured defects, not a measurement methodology — the wrong shape even though its
subject matter is adjacent), `docs/profiles-design.md` (a real design-boundary
precedent for this kind of page, but about a different, specific question — the
profile/code boundary). None fit, so this is a new page rather than a squatted section.

## The three states

A measurement row that classifies a defect (or its absence) at one location in one
image answers **two separable questions**, and conflating them is how a withhold gets
counted as a measurement:

1. **Is there anything here to measure at all?** — a SPATIAL question. Does the sampled
   region land on the surface it is supposed to sample, or on backdrop / a different
   material / nothing?
2. **Given there is something to measure, what does it show?** — a MATERIAL question.
   Does the sampled region show the expected material, or something else?

Three states, not two, because question 2 has two live answers and collapsing them
erases the finding:

| state | question 1 | question 2 | meaning |
|---|---|---|---|
| `UNAVAILABLE` | no | — | the region does not land on measurable surface; nothing said about material |
| `AVAILABLE+present` | yes | expected material | the surface is there and reads correctly |
| `AVAILABLE+occluded` | yes | wrong material | the surface is there and reads WRONG — this is the defect |

**`AVAILABLE+occluded` is not a lesser-confidence `UNAVAILABLE`.** It is the state the
instrument exists to catch. A convention that lets `present` and `occluded` collapse
into one `MEASURED` bucket is functionally identical to hiding the defect inside a
withhold count — this repo's own record has one entry for exactly that failure mode:
this page's own kickoff (`docs/experiments/E62-schema-patch-kickoff.md`) first landed
item 3 as "MEASURED / UNAVAILABLE," two names for what should have been three states,
and it was corrected in place before any code was written (commit `c3da18e`) precisely
because collapsing `present` and `occluded` is how the defect gets counted as a
withhold again. It is why the state names stay three, spelled out, not two with a
sub-flag.

## The rule question 1 must answer

**UNAVAILABLE is decided by a SPATIAL question only.** The instrument that answers it
may look at *where* the sample lands and *what texture/structure* is there — never at
*what colour* it is relative to the thing being searched for. This is not a style
preference; it is a measured trap:

- **Departure-from-backdrop keying is forbidden as the availability test**, because it
  inverts on exactly the images this convention exists to grade. E61's own palette file
  records `sleeve_L` reading 8.25 dE from the backdrop corners at hue 77.5°, in the
  backdrop's own neighbourhood — a region SITTING ON THE GARMENT reads *close* to
  background colour. A "mark unavailable if it looks like backdrop" rule would silently
  withhold the defect it was built to find.
- **The working signal instead: does the region hold texture, or a smooth gradient?**
  E61's calibration used local standard deviation of L\* within the sample box — a
  question about STRUCTURE, blind to which material is present. Measured across 13
  known images: backdrop corners read 0.25–0.50; every sleeve box (garment fabric of
  either kind) reads 13.73–31.02. A >27x gap, zero overlap, and neither side of that
  statistic references hue or a reference colour at all.
- **The readout may never gate its own availability against the very question it is
  trying to answer.** If the spatial test and the material test share an input, a
  region that fails the material test can silently relabel itself UNAVAILABLE instead
  of OCCLUDED — the exact defect-hiding failure mode section "the three states" names
  above, arrived at by a different route.

## The worked example — cite this row shape

E61 (`docs/experiments/E61-layering-repairs-report.md`, Stage 3) is the exemplar this
convention was extracted from. Its two-axis row (`stage3/n2_two_axis_rows.json` in that
arc's working tree) carries both axes explicitly, never merged:

```json
{
  "arm": "R", "seed": 106, "label": "armR_seed106",
  "sleeve_L_local_L_std": 13.83, "sleeve_R_local_L_std": 17.58,
  "any_tripwire_flagged": false,
  "axis1_default": "AVAILABLE",
  "hue_meas": 77.5, "hue_ref": 77.5, "hue_delta": 0.0,
  "chroma_meas": 23.27, "low_chroma": false,
  "dE_to_N1_ref": 50.3, "dE_to_N2_ref": 8.47, "closer_to": "N2(shirt)",
  "axis2_material": "present",
  "dE_vs_reference": 0.0
}
```

Reading the shape, not just the sample: `axis1_default` carries the SPATIAL verdict
(`AVAILABLE` / `UNAVAILABLE`) computed from the local-std signal and the tripwire flag,
with its own raw numbers (`sleeve_L_local_L_std`, `sleeve_R_local_L_std`,
`any_tripwire_flagged`) kept on the row rather than discarded once the verdict is
written — so a later reader can re-derive the classification without re-measuring.
`axis2_material` carries the MATERIAL verdict (`present` / `occluded`), computed only
when axis 1 is `AVAILABLE`, from a hue-delta band AND an independent nearest-reference-
colour test (`dE_to_N1_ref` vs `dE_to_N2_ref`, `closer_to`) that must agree with the
hue read before the verdict is trusted — disagreement is its own reported state, never
silently resolved one way. On E61's own 15-row corpus, zero rows fell in the
disagreement band and the tripwire fired on none of them; both are reported findings
about that corpus, not properties assumed of the convention.

**A minimal schema for a measurement row that carries the state explicitly:**

```json
{
  "row_state": "UNAVAILABLE | AVAILABLE+present | AVAILABLE+occluded",
  "axis1_signal": {"...": "the raw spatial measurement(s), kept on the row"},
  "axis1_verdict": "AVAILABLE | UNAVAILABLE",
  "axis2_signal": {"...": "the raw material measurement(s), kept on the row, present only when axis1_verdict == AVAILABLE"},
  "axis2_verdict": "present | occluded | indeterminate | null"
}
```

`indeterminate` is the fourth honest value axis 2 may need (E61 reserved it: hue-band
and nearest-reference disagreement, or a hue landing outside both defined bands) — not
a third availability state, but a real outcome for the material question that a
convention must have room to say rather than force into `present` or `occluded` by a
coin flip.

## The boundary this convention does NOT cross

**UNAVAILABLE lives on readout rows and never becomes a fourth `check_prompt` failure.**
The authoring gate (`tools/canon_gate.py`) answers a different question — does a prompt
cover the canon — and its verdict set (`ok` / `missing` / `forbidden` / `unlicensed`) is
untouched by this convention. A measurement tool built after generation may report
UNAVAILABLE about a rendered pixel; nothing about that changes what the gate required
before the pixel existed. Keeping the two separate is what stops "the region I sampled
was mislocated" from ever being read as "the canon was not covered."

## Precedent index

- `tools/s3_run.py` — exit 4, could-not-run vs exit 2 ANDON vs exit 0 (the one-site
  origin).
- `docs/experiments/E61-layering-repairs-report.md`, Stage 2.5 and Stage 3 — the full
  derivation (two candidate spatial signals tested against genuinely labeled
  populations; the steer that corrected a wrong worked example before any pixel was
  scored) and the row format cited above.
- `docs/experiments/E62-schema-patch-report.md` — this convention's own origin as a
  named, documented rule rather than a one-arc practice.
