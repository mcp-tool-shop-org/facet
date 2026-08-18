**The gate closes fail-closed, a generation gets an identity, and a surface starts becoming a set of faces.**

v0.6.0 made the canon data and put a gate in front of the spend. This release closes the
three holes that were still in it — the gate was optional, a generation could not be
replayed, and a canon surface was still only a *word*.

## Fail-closed at every authoring site

The v0.6.0 gate read `if args.canon:`. Omit the flag and it did not run, and nothing said
so — and `texpass_loop.ps1`, the shipped driver, called `texpass_brush` without a profile.
A gate a missing flag can separate from the action it gates is not a gate.

Now a tool that authors a spend and is given no canon **refuses**:

```
$ python tools/restylize_views.py --emit-only --inputs IN --outdir OUT --prompt "..."
canon_gate.Andon: ANDON: no canon: pass --canon PATH, or --subject NAME,
                  or --no-canon --subject NAME for an identity-only subject
```

`--outdir` is never created. The escape for a subject that genuinely has no canon is
**census-backed and cannot be worn by a subject that does**:

```
--no-canon --subject GALLEON   ->  proceeds, prints  [canon] UNGATED: GALLEON identity exists, surfaces missing
--no-canon --subject W3        ->  REFUSED: W3 has surfaces at canon/w3.surfaces.json
```

Wearing the escape means a deliberate edit of the census, and you cannot invent a subject
that has no IDENTITY. That is what stops it becoming a checkbox. Wired at
`restylize_views`, `texpass_brush`, `brush_cloud_step` — which writes the JSON that gets
submitted to the cloud — and `e12_pair_cloud_step`, which authors the paid twin graph. Two
sites were refused with reasons rather than wired: `ig2mv_licensefree` is a different
backbone with no subject, and `e37_fire_repaints` replays a *recorded* prompt, where a
refusal would halt a faithful replay.

## The gate now reads both directions

Checking that a prompt **contains** the canon finds a thin prompt. Checking that everything
in the prompt **is** canon finds a phrase naming something the subject does not have — and
there was one in the live default: `gold necklace`, which this repo had already measured as
misnaming the gold belt medallion, *"and the element survives by accident."*

A covering prompt with that phrase appended now returns `missing: 0` and refuses anyway,
naming the clause. Schema 2 declares the legal non-surface clauses so the reverse check does
not fire on `plain grey background`; schema 1 files stay one-directional, so an older
subject cannot start refusing its own style words.

## A generation record with an identity

`gen_record` **extends** the existing sidecar rather than replacing it — every recorded
`*_gen.json` still reads. It adds an immutable `recipe_id` (content hash after NFC and
CRLF→LF normalisation), a movable `alias` excluded from that hash, the declared producer,
and the canon the gate allowed.

The fields we **cannot** reach are recorded absent with a reason rather than omitted or
faked: `checkpoint_hash`, `lora_weight_hash`, driver, hardware and library are not returned
by the cloud transport, and validation **refuses** a string in those slots. A field that
reads as filled when nobody can know it is worse than a hole. The LoRA is half-reachable and
says so — the declared card name is in the graph we write, the weight tensor is not, and
hashing a filename and calling it provenance is a known bug in another tool's history.

## A worksheet, and the first face binding

`canon_worksheet` emits every surface a subject's *kind* implies, so a hole is a row before
anyone has named it, and is **structurally incapable of filling an occupant** — tested with
a poison phrase that arrives with a surface already assigned and is not written.

`canon_bind` gives a surface a face set. Today it is honest rather than impressive: **27
rows, every one empty, 0.00% of the figure bound.** Two rows reach `proposal` — `blade` and
`grip`, the only names in the hand-box file that resolve as surface ids — each carrying its
boxes as seeds with their original *"PROPOSAL. Not a ruling"* provenance. `skirt` stays
**unmatched** rather than being silently mapped to `kilt`.

The unit is the **face**: faces survive a re-bake, texels do not, and this route re-bakes.

## Measured, and closed as negative

- **The target-view compositor does not fix the flat class.** It already existed and was
  already the default; against the flat classifier it *raises* the count at the named target
  (38 → 40) and sharply at two others (23 → 64, 36 → 110). Shape is ownership, colour is
  not — an ownership policy cannot repair a cross-view colour disagreement on a
  correctly-attributed surface.
- **Co-location survives from-scratch specification.** The gold forearm plate is absent from
  the sixteen-element from-scratch arm, and the compound form had already been tried and
  split.
- **Element count cannot be separated from element identity** on the plates already paid
  for, and the reason is structural rather than statistical. What they do give is a
  one-sided bound: over an element ladder of 10 → 17, count removed **nothing** that was
  present at 10.

## Corrected in place

- The front page told readers a target-view compositor was *"the scoped repair and costs
  nothing."* Measured, it goes the wrong way. Corrected with the measurement beside it.
- **The asset accepted at Gate 1 and the asset later called far from perfect are the same
  file.** Nothing said so until a seat assembling a labelled accept/reject set found its two
  classes collapsing onto one tree and halted. Acceptance is a ruling on an artifact at a
  date, not a permanent grade — and any comparison treating "accepted" as a label needs a
  per-surface class. Noted on both handbook copies.
- A `DIRECTOR-VERIFIED` label on a set of region boxes is **unsupported at source**. It sits
  in a read-only tree and stays a record item rather than an edit.

## Known

The canon binds **0.00%** of the figure — `scopes.views` is empty by construction, and the
hand-box file reaches 7.95% strictly. Until a surface is a set of faces, *is this region the
wrong material* is not computable, and no automated check for that class exists: the nearest
detector fires at 39.90% on a pauldron that is correctly gold, above five of the seven
regions the Director named. Filling the face sets and the scope lists is a human walk, and
the worksheet only makes it cheap.

Suite **1338 tests**, 1284 hermetic. Fifty-six experiments in the record, verified on four
legs with byte-identical determinism.
