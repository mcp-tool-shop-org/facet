# E14 — rulings

Running record. Advisor rules; evidence cited per ruling; corrections in place.

---

## Ruling 1 — DESIGNATION: 00001 is the longsword (Director, 2026-08-07)

**"00001 is my favorite."** Ruled on the full-size Gate 0 sheets, the hilt crops at
zoom and the 4× tip crop ([E14-gate0-report.md](E14-gate0-report.md)), viewed by the
advisor first per the looking rule, with the per-candidate observations presented as
data and nothing ranked.

Consequences:

- **The prop is `longsword_00001_raw.glb`** (TRELLIS.2 `1024_cascade`, seed 42, from
  `longsword_clay_p1_00001_.png`) — 999,474 faces, **1 welded shell at fraction
  1.000000**, zero boundary edges, 121 non-manifold edges (0.0081%, the fewest of
  the three), widest-horizontal/height **0.2258** (the route's first portrait
  subject), Gate 0 frame **240×1024**.
- **00002 and 00003 are not designated and are preserved as measured** — meshes,
  sheets, stats, topology and overlay JSONs stay staged at `E14_gate0/`; nothing is
  deleted. Their numbers remain the class-family context.
- **The designated-in facts ride as subject facts, not defects**: the softer
  gem-pommel apex and the lumpier wrap relief were on the artifacts he designated
  on. The tip's hair of apex rounding (visible only at 4×) rides with them.
- **The pose fact is banked**: tip-standing, bilaterally symmetric, quillon span on
  one horizontal axis — the mesh's stance. Twins belong to this mesh.

## Ruling 2 — the Gate 0 halt is ACCEPTED; practices settled; the frame flag named (2026-08-07)

Evidence: the report (`82c123c`), its blind predictions (`a4d587a`, 17 of 25 held
with the misses located), and this seat's eye on all three sheets, all three hilt
crops and the tip crop before the presentation.

**2a — the two declared deviations are RATIFIED, and the first becomes standing
practice.** Instruments live in `tools/diagnostics/`, not under the experiment
tree — the executor demonstrated the reason rather than asserting it (three E12
instruments reused unmodified this session; an instrument outside the repo cannot
be re-run from a clone). Future dispatch compensator lines read "new files only;
instruments in `tools/diagnostics/`, artifacts under the experiment tree." The
structural-landmark hilt method (quillon flare = global width maximum; blade
shoulder = the local minimum below it) is ratified WITH its named cost — it
disables the two-view Z-disagreement ANDON by construction, and the compensating
overlay check (the box drawn back onto all eight views, looked at) is the
accepted substitute on this subject class.

**2b — the two-definitions-of-shells finding is BANKED**: vertex-connected
components (every family number the route quotes) versus manifold-edge components
differ by a factor of hundreds on these meshes, and the first-draft instrument
that conflated them was thrown away rather than published. 00002's 331 shells are
its INNER WALL in fragments — on this subject the shells column counts wall
fragmentation, not detached detail, the opposite of what it counted on the
galleon. A number that reproduces exactly can still be measured against the
wrong object; both quantities are now computed and named apart.

**2c — the pinch-locus finding is BANKED as the prop spec's prior** (hypothesis,
labelled, with its evidence): on this pipeline, **relief finer than the voxel
scale becomes non-manifold pinching at roughly constant density, not denser
mesh** — the pinches enrich 2.1–3.9× on the grip wrap (finest relief) while the
blunt cutting edges stay clean, ordering with wrap pitch across all three
candidates; and the hilt's density contrast is the lowest the route has measured
(1.102–1.135× against the dragon head's 1.189×).

**2d — `mesh_stats`' silent warning is the errand batch's newest member.** The
character instrument did not notice it was not looking at a character — its
condition ("vertical extent is not the largest") is a proxy a tip-standing prop
passes, while `rect_frac_of_figure` at 1.45–1.90 (a face rect larger than the
figure) is the honest condition sitting unused in the same JSON. Queued with the
batch; not changed mid-arc on a shared instrument.

**2e — THE FRAME FLAG is named for the profile fold**: the derived portrait
frames put the blade at roughly 60–110 px of generator width if kept as twin
frames per the ship's precedent. Whether the prop's generation frame is the
Gate 0 frame or a wider derivation is a profile decision taken with the fixture
in hand — flagged here so it is decided, not inherited.

**2f — accepted as logged**: the watchdog verified before and after the GPU leg
with heartbeats in the log · peak VRAM 3.4 GB flat, the lowest the route has
recorded · the E12 two-backend refinement reproduced exactly · the ~1M face
counts read off the log as a decimation target, closing an inference with a
source · the E15 index verified byte-identical at a third seat before any work ·
the executor's three noted departures from the advisor's clay descriptions
(00002's unnamed quillon span — the largest geometric separator — among them)
enter the advisor's ledger as observation misses at full size.

## Ruling 3 — THE HOLLOW FINDING IS BANKED ROUTE-WIDE (2026-08-07)

**Every reconstruction this route has made is a hollow double-walled shell** —
measured three mutually independent ways (ray-crossing counts, cross-section
clustering, signed volumes of separable walls) on all three candidates AND on
two out-of-family controls including the accepted dragon; wall thickness sits on
a hard floor of 0.00196–0.00213 against a ~1.0 bounding box, **almost exactly
two voxels of the 1024³ grid** (the voxel arithmetic rides as a labelled
hypothesis — nobody opened the extractor). Invisible for eleven experiments
because the route only ever touches visible surface, and the cull excludes the
inner wall by construction. **Nothing banked is invalidated** — no recorded
claim asserted solidity, and the standing volumetric-predicate constraint gains
its deeper ground: E01's "signed distance at the chest centre reads *outside*"
is consistent with the chest centre sitting in the cavity, genuinely outside
the material (hypothesis, recorded with the connection). The CLAUDE.md standing
constraint is extended this fold; any future volumetric consumer (collision,
printing, booleans, thickness policy) meets a shell, not a solid.

## Ruling 4 — ALLOCATION: NONE, decided with Gate 0's evidence in the profile (2026-08-07)

The ship ruled NONE; the beast ruled NONE on its own head evidence; neither is
inherited — this is decided on the designated mesh's own numbers:

1. **The mesh has no privileged region to serve.** The hilt's density contrast
   is 1.135× — the lowest the route has measured, against the character-face
   3.1–4.5× that made E01's allocation matter.
2. **A hilt-crop second reconstruction would buy pinches, not polygons** — 2c's
   measured prior: this pipeline answers fine relief with non-manifold pinching
   at roughly constant density. Spending the crop lever here prices the prior,
   not the subject.
3. The null intervention is the baseline every future privileged-region arm
   needs (the ship's Ruling 14 grounds, held through three accepted assets).

**Director-overrulable in a sentence**, as always. The re-open condition is the
E12 pattern's: if the painted hilt disappoints at a gate, the evidence returns
here with the ladder's cheap rungs first.
