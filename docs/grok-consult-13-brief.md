# Grok build #13 — the canon database, and the gates that make it load-bearing

**2026-08-17, facet advisor seat. BUILD round.** Queued behind briefs 11 and 12, both
folded. Twelve nominated claims, twelve held.

The Director's direction: the canon must be a database inside the repo, part of a gated
pipeline. This is the studio's spine, not a fix for one character — build it that way.

*Everything below the line is the paste block.*

---

# Twelve for twelve. Now build the thing that would have stopped the last four arcs before they started.

## The defect, in one line of arithmetic

`canon/W3-IDENTITY.md` specifies **seventeen** named elements, N1–N17. The recorded
generation prompt that made the twins named **six**. Nothing anywhere noticed.

The canon is a markdown document a human reads. No tool loads it. Nothing refuses a
prompt that fails to cover it. Nothing checks afterwards whether a named element landed.
Four arcs then spent themselves repairing composition downstream of paint that was wrong
at the source — and every one of them came back pointing here:

- **E50**: the defect sits on ordinary directly-painted texels (90.0–99.1%), not on any
  fill, and it predates the repairs that were blamed for it.
- **E51**: both fill repairs built and measured. The render did not change to the eye.
- **Your #12**: there is no geometry to snap a material boundary to — one PBR material on
  the whole mesh, 13,715 atlas islands against sixteen named materials, and the palette
  is blind to gold-against-leather because both are warm. 354 texels of 2.4 million.
- **Your #11**: plates that agree and are wrong the same way. A source defect.

## What exists, enumerated — do not re-derive it, and do not assume it is right

```
E:\AI\facet\canon\
  W3-IDENTITY.md            8,357 b   N1-N17, occupancy law written in prose
  DRAGON-IDENTITY.md       15,863 b
  GALLEON-IDENTITY.md       8,208 b
  LONGSWORD-IDENTITY.md    11,536 b
  E10-LAYER-IDENTITY.md     3,694 b
  LOGO-IDENTITY.md          9,701 b
  MANIFEST.md               5,285 b   provenance, incomplete by record
  *-palette.json            5 files   per-subject material bands (machine-readable ALREADY)
  twin_front.png / twin_back.png      the visual target W3's spec was read from
```

The palettes are already machine-readable and already consumed by `tools/palette_gate.py`.
**The identity half is the half that never became data.**

Outside the repo, `E:\AI\style-dataset-lab\projects\facet-assets\` is the dataset and
review half — `constitution.json` is a ten-rule rubric scoring finished images
(proportion, gesture, costume logic, style consistency), `terminology.json` is empty
stubs. **It holds no per-element identity for any facet subject.** There is nothing to
import. Do not build a bridge to it; say so if you disagree and why.

## What to build

A canon **database** in `canon/`, and the gates that make it impossible to skip. Tool(s)
in `tools/`, tests at **t87**. Invocable in this repo's sense: `argparse`, real flags, a
`__main__` guard.

**1. The schema.** Per subject, machine-readable, serving humanoid *and* prop, beast,
vehicle — five subjects already have IDENTITY.md and the studio will have more. At
minimum each row needs: a stable id; the noun phrase exactly as it must appear in a
prompt; the **surface it occupies**; its provenance class (prompt-supplied /
mesh-supplied via the control / style-supplied via the LoRA / under test); and its
verification state with the measurement and arc that established it — never hand-set.

**2. The coverage number.** What fraction of the subject's visible surface is named. This
is the number that would have said *the canon is thin* mechanically, four arcs before a
human noticed. Decide what its denominator is made of and defend it; this repo has been
bitten five times by a denominator that moved under a claim.

**3. The author-time prompt gate.** A generation whose prompt does not cover every
prompt-supplied element for that subject is **refused**, before any credit is spent.

**4. The occupancy gate.** The measured law, currently only in prose: *a specification
determines what occupies a surface and cannot add a second element to a surface already
occupied.* Elements that **replaced** an occupant landed; every attempt to **add** to an
occupied surface drew no response at all — one measured at ΔE 1.07 in two grammatical
forms. With a surface column this is checkable at author time instead of after a roll.

**5. The post-generation verifier.** Did each named element land. E08 already built
per-element ΔE machinery against a reference; reuse rather than re-roll it. Its output is
what writes each row's verification state.

## Argue with all of it, and especially with the first one

1. **Is the ELEMENT the right primary key, or is the SURFACE?** An element list cannot
   show you what is missing — the leather grip was absent from N1–N16 and no reading of
   that list revealed it; it was found by a human looking at a picture. A surface list
   with an `occupant` field that can be **null** makes the hole a row. If that is right,
   the whole schema inverts and the coverage number becomes trivial rather than
   contentious. Attack it.
2. **Where do surfaces come from, given #12's result?** Not from geometry — you proved
   TRELLIS authors one material. Candidates: the reference image walked by the Director;
   the palette bands; the atlas islands (you already killed these as packer seams). If
   the honest answer is *a human enumerates them once per subject*, say so plainly — that
   is a real answer and it makes the ratification pass the gate rather than a formality.
3. **What is an honest prompt-coverage check?** Exact substring is brittle and will pass
   a prompt that names the phrase inside a negation. Semantic matching needs a model,
   which puts a model inside a gate. Pick, and state what your choice cannot catch.
4. **Two files, one truth.** `W3-IDENTITY.md` carries reasoning a JSON row cannot — four
   ranked arguments for why the grip is leather, and one argument explicitly recorded as
   *not* used so nobody re-derives it. That prose is worth keeping. So: is the JSON
   generated from the markdown, the markdown from the JSON, or are both authored with a
   test pinning their agreement? Two sources that can drift is how this defect started.
5. **The joint, not the garment.** The regions that failed are material *joints* —
   sleeve-edge against bare arm, flesh against tunic at the fingers, gold plate against
   leather at the boot-top. E49's reading was that the missing specification is the
   boundary pair, never a fifth garment. Does the schema need joints as first-class rows
   between two surfaces, or does a surface list with adjacency give it for free?
6. **Anything unnamed.** Your #3 catch turned an arc by refusing the brief's framing;
   your #11 refused to give the two-branch answer the brief asked for and named a third
   world; your #12 killed its own thesis on the tree. Same standard.

## Hard constraints

**Sleeveless is ruled and binding**: the reference has no sleeve. Any schema or repair
that lets a garment be invented onto the bare arm is wrong, and this is exactly the class
of error a surface-with-occupant model should make impossible to express.

**W3 is the exemplar for the humanoid, not a shipping character** — its job is to prove
the route, so the bar is completeness and fidelity to the reference rather than
per-element taste. The mesh and silhouette are Director-accepted and stay.

Every gate `raise`s, never a bare `assert` — `python -O` deletes an assert and execution
continues past a fired gate; 87 of this repo's ANDONs were once removable by an
environment variable. Tests ride the commit that touches the code, and a test that cannot
fail is not a test: for every leg construct the case that fails if the code is wrong in
the way the leg exists to catch, and show it failing.

**No credits, no GPU, no generation.** This build is the gate in front of the spend, not
the spend. Do not write under `E:\AI\training\facet_E4*\` or `facet_E5*\`. Leave the
change-set uncommitted for the advisor's fold.

⚠ **Count surfaces are contested right now and this is the advisor's mess, not yours.**
HEAD is 1182/1135; t85 and t86 are folded but the experiment-count pins are mid-repair
because two new experiment rows (E50, E51) landed in the status table this session. State
plainly which counts your change-set assumes and reconcile nothing you did not move.

## Calibration

Nominate **one checkable claim** — about the tree, a number, or a mechanism in a file you
cite — that we verify by running it before anything trusts the rest. Twelve for twelve;
a round where the chip loses is still reported.
