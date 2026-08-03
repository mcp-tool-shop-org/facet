# Subject profiles — design note

**Status:** agreed, not built. Sequenced **after E02 closes, before E04 starts.**
**Origin:** the Director, 2026-08-04 — "create profiles (or lanes) so that we don't break
the humanoid character pipeline to make the ship, monster, asset, etc."

---

## Why, beyond tidiness

Every constant in this pipeline was calibrated on one standing human figure. Nobody can
currently say which are principles and which are that warrior's measurements wearing a
principle's clothes — and that confusion is this project's entire failure history.

**Extracting the profile answers "does the route generalise" as a byproduct.** Every value
must declare itself:

- **goes in the profile** → it was a subject assumption all along
- **stays in the code** → it is a real principle

That list is as much the deliverable as the config is. If E04 needs a change *outside* the
profile, that is the signal that something in the shared code was never a principle.

## Timing

**After E02**, so the character profile is written from settled values rather than
mid-experiment ones. **Before E04**, so the ship never has a reason to touch a character
default. Doing it during either run would mean tuning a config and an experiment at once,
with no way to attribute a result to either.

## Shape

```json
{
  "name": "character",
  "provenance": "calibrated on subject W (bearded warrior), E01–E02, 2026-08-04",
  "framing":    { "render_w": 752, "render_h": 1024,
                  "fit_axis": "height", "margin": 1.204 },
  "allocation": { "anchor": "face_rect", "rect": [360,240,700,600], "rect_res": 1024,
                  "target_faces": 150000, "protection_factor": 10.0,
                  "body_weight": 0.8, "head_scale": 3.0 },
  "thin_policy":{ "enabled": true, "extent_threshold": 0.030,
                  "why": "smallest value filling the greatsword solid; 0.020 leaves the fuller grooves open" },
  "cameras":    { "yaws": [45, 315, 135, 225, 90, 270], "elevated": [[0, 55], [180, 55]] },
  "gates":      { "mesh_gate": "character", "head_rect_metrics": true },
  "prompts":    { "identity_words": "…", "negatives": "…", "per_view": { "…": "…" } }
}
```

**Every field carrying a tuned value carries its `why` alongside**, as `thin_policy` does.
A profile is otherwise a perfect hiding place for unexplained magic numbers, which is
precisely how the previous memory store became doctrine.

## Stays in the code — principles, not settings

Physics and measured traps, subject-independent:

- weld before decimating (an exported mesh is seam-split, not solid)
- `mesh_mask ∧ erode(twin_mask)` — two masks answer two different questions
- judge textures under FLAT, geometry under `--clay`
- twins belong to the mesh they were rendered from, and are a pipeline stage
- build the control image; Canny cannot find a silhouette that is not there
- spiral stroke order outward from the styled poles
- no volumetric predicate on an exported mesh
- a ray along the surface normal measures the tessellation, not the geometry

## Expected `ship` profile deltas — the E04 stressors

| field | character | ship (expected) |
|---|---|---|
| `framing.fit_axis` | height | **width** — a galleon is wider than tall |
| `framing.render_w/h` | 752×1024 | landscape, aspect TBD from the clay (1216×1024) |
| `allocation.anchor` | face rect | **none**, or a stern-castle rect where the carved detail lives |
| `thin_policy.extent_threshold` | 0.030 (a greatsword) | far smaller — ratlines and shrouds are thinner than a blade |
| `gates.mesh_gate` | character | **none** — `gate_mesh.py`'s head/shoulder logic is meaningless on a ship |
| `cameras.elevated` | ±55 at 0/180 | decks need looking *into*; the elevation set is a real design question |

## Naming

The studio already uses "lanes" in `style-dataset-lab` for a related idea. These are
subject profiles for a geometry/texture route rather than dataset lanes; if the two ever
need to align, that is a later decision and not a reason to delay this one.
