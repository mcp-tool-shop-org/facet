**A prop gets a real size, a rig gets read rather than assumed, and the interesting result is a negative one.**

v0.8.0 closed on a painted subject. This release is about what happens *after* paint — a
character that has to be posed, and objects that have to be held. Nothing here touches the
texture route.

## The finding, and it is still open

A sixth subject went in to test the after-paint stage. It reconstructs cleanly and then
**fails auto-rigging.** Four candidate causes were eliminated by measurement rather than by
argument:

| candidate | how it was tested | outcome |
|---|---|---|
| untextured input | a textured plate and an untextured one | **eliminated** — both fail |
| component count | against a subject that rigs, by shell count | **eliminated** |
| mesh topology | manifold edges, shells, watertightness | **eliminated** |
| the pose | a narrow A-pose and a wide one, by arm-to-torso separation | **eliminated** |

**The discriminator is unidentified**, and `canon/BASE-FIGURE.md` carries the table while
declining to name a cause. That refusal is the load-bearing part: this repo *did* name a
cause — arm-to-torso separation — and it was falsified inside the same hour, by a true
A-pose failing at separation **0.5412** while a wider pose passed at **0.5483**. The
variable moved the wrong way. The honest state is a table with no cause in it, not the most
plausible survivor.

Where a rig does exist, posing has a measured ceiling rather than a fix: roughly **20°** of
arm rotation stays clean, roughly **110°** shreds the shoulders. Rigid plate binding was
built to repair that and does not — all three repairs measured, all three failed — so it
ships in `tools/superseded/` where anyone can run it and watch it fail the same way.

## Two contracts, because "looks about right" is not a size and "touching" is not a grip

**Every reconstruction this route makes comes back normalised to 1.002 on its longest
axis** — measured on four unrelated assets, to three decimals. So a prop mesh carries no
true scale at all, and a heater shield loaded as it arrives is 1.8 m tall: a door. The
figure was correctly sized only by coincidence, because a human is what the unit box
happened to be fitted to.

A prop's real size is now **declared once in millimetres**, stored in a sidecar and checked
rather than trusted. Scene unit: **1.0 unit = 1.8 m**. A mesh still measuring ~1.002 that
wears a prop's sidecar exits 2 while reporting its real size — the exact mistake the
contract exists to prevent.

```bash
python tools/prop_scale.py --glb raw.glb --out props/shield.glb \
    --name heater_shield --real-mm 758 --axis height --attach forearm_l
python tools/prop_scale.py --verify props/shield.glb
```

And a prop that touches at one vertex is not held. The contact gate reports a minimum
point-to-surface distance **and a contact area**, because a count is a fraction of however
many samples the prop happened to get — a property of tessellation, not of contact. The
asset that prompted the tool measured a minimum of **0.00072** across **97 points out of
624,510** and was plainly not being gripped.

Both thresholds are flags rather than constants, and both are set independently of the
result they judge.

`tools/verify/rig_report.py` opens the GLB container directly and says what an auto-rigger
returned: mesh identity against the submitted file, joints by name, whether skinning is
there at all. `--require-same-shape` compares vertex and face **sets**, not counts — the
question is order-invariant, so the check is too.

## Clause 7 — five digits per hand

A six-fingered hand reached an accepted sheet **past four gates that could not see hands.**
The Director found it by looking. No metric in this repo could have caught it: every one of
them measures colour statistics, silhouette agreement or surface coverage. Hands are an
acceptance item now.

Clause 7 exists because clause 2 caused it, and the general lesson is one this repo keeps
re-learning: a measurable proxy is not a conservative substitute for asking.

## Also in this release

- **`turn_render.py` films transparent by default**; `--opaque` is the escape. The claim
  that an opaque render equals a transparent one composited over the background was tested
  and is **false** — the opaque background dithers over four values and the figure rim sits
  4.34/255 away in linear space. T99 pins the numbers rather than the claim.
- **Two interpreters, stated in the law.** The suite and the MCP servers run on the
  environment carrying the CI pins (3.12); the reconstruction stage runs on a separate 3.10
  environment for its TRELLIS wheels.
- **A new handbook page** — [Props and rigs](https://mcp-tool-shop-org.github.io/facet/handbook/props-and-rigs/).
- **29 tests** — T99–T102, can-fail leg first in every file.
- Paths throughout the record are written portably (`%USERPROFILE%`, `$HOME`) rather than as
  one machine's absolutes.

## What this release does NOT claim

- **That the rig question is answered.** Four causes are eliminated; the fifth is not known.
- **That any prop has been mounted and accepted.** Both contracts are tested against
  synthetic meshes at a known separation. Nothing has been placed in a hand and ruled on at
  the Director's zoom, so the contact gate has no scalp on a real asset.
- **That the sixth subject is finished.** Geometry, rig and props are measured; the texture
  route has not been run on it.

## Gates at this tag

identity scan `RESULT CLEAN` on the tree and on all three leaving artifacts (npm tarball,
sdist, wheel) · shipcheck **100%** (28 checked / 0 unchecked / 9 skipped) · suite **1376
passed** · re-count **1376 total / 1319 hermetic / 57 deselected** · record index four-leg
verify **PASSED** on byte-identity · claims sweep **0 STALE** · CI and Pages green ·
seven translations regenerated **before** this tag rather than after it.

The treatment that produced this release keeps its own report, including two errors made
during it: [E73](https://github.com/mcp-tool-shop-org/facet/blob/main/docs/experiments/E73-treatment-0-8-1-report.md).
