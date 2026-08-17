# Grok build #18 — the canon router, and the worksheet that feeds it

**2026-08-17, facet advisor seat.** Seventeen briefs, seventeen chips held, six briefs cut
down and right every time. This one is an architecture round: the canon stopped being a
document last session, and now it has to stop being a W3 anecdote.

*Everything below the line is the paste block.*

---

# Seventeen for seventeen. This round is architecture, not a fix — build the canon ROUTER and the WORKSHEET that feeds it.

## Where we actually are

`canon_gate.py` shipped last round and it does one thing well: **for one subject, does this
prompt contain every ratified canon phrase?** It runs inside `restylize_views` and
`texpass_brush`, before the output directory exists. W3 is 24/24 occupancy, 24/24 ratified.

That is a checker with a CLI. **It is not yet a component**, and three measured facts say so.

**1. The gate is one-directional.** `check_prompt` iterates `required_phrases(doc)` and asks
`_present(phrase, prompt)`. Nothing asks the reverse. So a prompt phrase naming something
the canon does not contain is invisible — and there is one sitting in the live default right
now. `profiles/character.json` gives both `restylize_views` and `texpass_brush` a prompt
containing **`gold necklace`**. The record already named this class, in E08
(`docs/experiments/E08-ruling-gate0.md:940-945`):

> The prompt says "gold necklace"; there is no necklace at the throat in canon; there is a
> gold belt medallion. **A term in the prompt is misnaming a canon element, and the element
> survives by accident.**

Same file still says `skirt`, after the garment was ruled a **kilt** and renamed in the
phrase, the surface id and N9.

**2. The gate is not at every spend site.** `refuse_uncovered` is called at exactly two
places — `restylize_views.py:113` and `texpass_brush.py:44`. `brush_cloud_step.py` imports
no canon anything. Its own docstring says `texpass_brush` posts to a **local** ComfyUI and
that generation must run on Comfy Cloud, which is why `brush_cloud_step graph` exists to
write the workflow JSON that gets submitted. **The gate stands in front of the local server
and not in front of the paid one.**

**3. The gate has no notion of scope, so it can only ever be subject-level.** Its own Known
section says it does not check per-view stems. It cannot: **no surface declares where it
is or which cameras see it.** A surface today is a name with an occupant phrase. Requiring
the whole subject canon in a per-view or per-stroke prompt is not merely strict — it is
wrong, because it would demand the beard on the rear camera, which is the failure E01 exists
for. That is why prompt derivation was declined and why you refused it.

## What to build — the shape, both halves

**The ROUTER** is the single component every consumer asks: *what does the canon say, for
THIS subject, at THIS scope, and is this prompt covered?* It refuses when the answer is not
covered, and it refuses when there is no answer at all.

**The WORKSHEET GENERATOR** is the authoring half: it makes walking a reference cheap and
complete, and it is **structurally incapable of inventing canon**. Four subjects have an
IDENTITY.md and no surfaces file (galleon, dragon, logo, E10-LAYER) and they are staying
undone until a human walks them — the worksheet is what makes that walk a filling-in rather
than an invention.

They are one design because **the worksheet's output format is the router's input format.**

### The router, concretely — five things it must do

1. **Resolve.** subject id → canon file, over a declared search path, with a **named refusal
   for a subject that has none.** Today every call passes `--canon <path>`; that is fine for
   one subject and it is why the gate is "in the path" only for W3.
2. **Cover, both directions.** canon ⊆ prompt (exists) **and** prompt ⊆ canon (missing). The
   reverse needs a declared class of legal non-surface clauses, or it fires on
   `plain grey background`, `visible brushstrokes`, `painterly worked surface` every time.
3. **Scope.** Full-subject, per-view, per-stroke. A scope names which surfaces are in play,
   and the gate's requirement is over that set, not over the subject.
4. **Stand at every spend site**, `brush_cloud_step graph` included — refusing to *write*
   the workflow JSON, the same way the others refuse before the output directory exists.
5. **Version.** `w3.surfaces.json` carries `schema: 1`. Anything you add is schema 2, with
   schema-1 files still loading, and a stale consumer failing loudly rather than silently.

### Enumerate before you commission — three things that already exist

This repo has commissioned things that already existed four times, and the advisor invoked
that law twice today. Check these before you write anything:

- **`canon_gate verify --regions`** already takes `[{name, box:[x0,y0,x1,y1]}]` and returns
  per-region median CIE76 ΔE with `landed` / `missed` / `uncertain`. **The region `name` is
  free text and is bound to no surface id.** The spatial primitive exists and is unbound.
- **`tools/s3_sheet_regions.json`** is the repo's hand-declared per-view region format:
  `frame`, `view_map`, `views{N: [{name, box, from}]}`, every entry carrying its provenance
  and the file labelled *"PROPOSALS. Not a ruling."* Its names — `tunic`, `skirt`, `blade`,
  `grip`, `boot_tops` — look like surface ids and are not declared as any. One of them is
  the pre-rename `skirt`.
- **`profiles/*.json`** — `character`, `beast`, `prop`, `ship`, keyed by **kind**, not by
  subject. `w3.surfaces.json` carries `kind: humanoid`. Whether the router's registry is a
  new file or belongs here is a real question, not a formality.

### The worksheet, concretely — what "beyond a skeleton emitter" means

A skeleton emitter turns an IDENTITY.md NAMED table into null occupants. That is the easy
20% and it does not scale a studio. What is actually needed:

1. **Kind templates.** Emit every surface a subject's `kind` implies, so a hole is a **row
   before anyone has named it.** That is `canon_gate`'s own thesis — *SURFACE is the row, a
   nullable occupant makes a hole a row* — applied at authoring time instead of audit time.
   N17 (the grip) was missing from the N1–N16 element list and reading that list could never
   have revealed it; a `kind: weapon` template with a `grip` row would have.
2. **Joints as pairs to confirm, not invent.** Joints are first-class (`{id, a, b, phrase}`)
   and the missing specification at every failed region was the **cut**, never a fifth
   garment.
3. **The spatial binding**, per surface per view, in the existing region format, carrying
   its own provenance and its own not-a-ruling state until ratified.
4. **Round-trip.** A filled worksheet validates into a surfaces file; a surfaces file
   re-emits a worksheet showing what is still open. A worksheet that is write-once is a
   one-time migration script, not a studio component.
5. **It must be unable to fill an occupant.** Not "should not" — unable, and tested for it.
   Generating canon under a clock is exactly what four subjects are being protected from.

## The build split, and I want you to argue with it

**My call: #18 is the ROUTER and schema 2. The worksheet lands next round.**

My reasoning: the worksheet's output format is the router's input format, so building the
worksheet first means **guessing** a schema, while building the router first proves that
schema against three real consumers and two measured defects that exist today. A schema
proven by a consumer is worth more than a schema proven by a generator.

**That is a call, not a constraint.** If the right order is the reverse, or if the router
should be smaller, or if the two are actually one file and I have invented a boundary that
costs more than it buys — say so and build what is right. You have cut six briefs in a row
and been right every time.

## Argue

1. **Scope is the hard one.** The router needs to know which surfaces are in play for a
   per-view or per-stroke call. The repo's only existing primitive is hand-declared boxes
   per view per subject, which is human work that multiplies by subject × view. Is that
   right? Is there something cheaper that does not put a model inside a gate — geometry,
   the AOV bundle's per-view visibility, the mesh's own extents? **Note the trap before you
   reach for colour:** three arcs established there is nothing to segment materials by here
   — one PBR material, 13,715 atlas islands against sixteen named materials, a palette blind
   to gold-against-leather. If the honest answer is "a human declares it once per subject
   per view," say that plainly and design for it rather than around it.
2. **The non-surface clause class.** Allowlist the legal style clauses, denylist, or
   restructure the prompt into a canon segment plus a style segment? Getting this wrong in
   the strict direction fires on every legitimate prompt; in the loose direction it lets
   `gold necklace` through, which is the whole point. Note the existing `forbidden` word
   mechanism is the closest precedent in the file.
3. **What verdict does a reverse-direction hit get?** The forward gate refuses on a missing
   ratified phrase and reports on an unratified one — the shape you argued last round. Is an
   unlicensed phrase a refusal, a report, or something else? If you invent a third verdict,
   what stops it becoming a checkbox everyone passes? Be consistent with #17 or say why the
   case differs.
4. **Where does resolution live?** subject → canon file. New registry file, or the profile,
   or derived from the tree? Four subjects will resolve to nothing and the refusal for that
   case is part of the design, not an error path.
5. **Anything unnamed.** Seven rounds running.

## State plainly what the router does NOT cover

The last round's boundary sentence went on the front page and it earned its place. Do the
same here. Paraphrase and synonym matching stay refused — semantic matching puts a model
inside a gate, and that is the file's own thesis, not a budget decision.

## Constraints

No GPU, no cloud generation, **no credits** — this build is the gate in front of the spend,
not the spend. Read `E:\AI\training\facet_E*\`; write to none of them. Change-set
uncommitted for the advisor's fold. Gates `raise`, never a bare `assert`; a check labelled
`IMPLEMENTATION:` may stay an `assert` and must say why. Tests ride the commit — a change
that adds tool code without tests is missing a step. **Next free test file is `t92`**
(t90 `evidence`, t91 `canon_in_path`).

⚠ **A second seat is live in this tree right now** working under `E:\AI\training\facet_E53\`
and writing `docs/experiments/E53-n11-spec-arm-report.md`. It has been told to take `t93` if
it needs a test file. **The T34 count surfaces are therefore contested** — state what your
change-set assumes and reconcile nothing you did not move; the advisor reconciles the counts
after both land. Do not touch `docs/experiments/E52-*` or `E53-*`.

Do not edit `canon/w3.surfaces.json`'s occupants. If schema 2 needs fields added to it, add
them without touching a ratified row's occupant, and say which rows you touched and why.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Seventeen for seventeen, and a round where the chip loses is still reported.
