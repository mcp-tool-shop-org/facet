# Base-figure pose contract

**Director, 2026-09-22.** Every base figure is generated and reconstructed **empty-handed,
arms down and clear of the torso**. Props are attached afterwards, on the rig. This is the
default for the sprite route, not a per-character choice.

## The clause

The prompt must say all of these, in positive language:

1. Both arms hang down and are **held away from the torso**, with clear open space between
   each arm and the body.
2. Both hands are **empty and open**, fingers relaxed and slightly apart.
3. **Nothing is held and nothing is carried.**
4. `feet planted and visible`, flat on the ground.
5. Head level and aligned with the body.
6. Plain ground, no plinth.

## ⚠ THE DISCRIMINATOR IS UNIDENTIFIED. Read the table; do not read a cause into it.

**This section has carried two causal claims today and both were falsified within the hour.
It now carries none.** First "the pose is the cause" (falsified by a narrow A-pose that
still refused); then "the variable is arm-to-torso separation" (falsified by a true A-pose
that refuses at width 0.5412, within 1.3% of the wide pose that passes at 0.5483).

Both were inferences by elimination from a single comparison, which is this advisor's
recorded failure mode, and canon is the wrong place to keep testing one. **The data below
is measured and stands. The explanation is open.**

| subject / pose | width | depth | riggable |
|---|---|---|---|
| merchant, arms down | 0.3773 | 0.2197 | **True** |
| halle, arms down | 0.4978 | 0.3205 | **True** |
| drell, one arm forward | 0.4190 | 0.3207 | False |
| drell, same pose rebuilt watertight (182 comps, 99.2% shell) | 0.4190 | 0.3207 | False |
| drell, narrow A-pose, arms vertical | 0.4185 | 0.2643 | False |
| drell, **true A-pose**, arms down and out 45° | **0.5412** | 0.2502 | False |
| drell, wide pose, arms **up** and out | 0.5483 | 0.4202 | **True** |

**Ruled out by measurement, each on its own test:** untextured input; component count (on
the operand actually submitted, not an inherited figure); topology (a watertight rebuild in
the same pose still refuses); overall width; reach from the trunk axis (halle reaches
further than drell and passes); and depth (merchant is the shallowest of all and passes).

**The only clean split left in the table is that Drell passes with his arms ABOVE horizontal
and refuses below it, while merchant and halle pass below it.** That is a description, not a
mechanism. The standing hypothesis — **untested** — is an interaction between Drell's flared
pauldrons and arms below horizontal: the pauldron may bridge the upper arm into the torso in
a way a skeleton fitter cannot separate, and merchant and halle have no pauldrons to do it.
Nobody has measured that, and it must not be written here as though somebody had.

---

## ⚠ SUPERSEDED CLAIM, kept for the sequence — "the variable is SEPARATION"

**Third and final state of this section. Both earlier states are kept below, because the
sequence is the useful part.** The mechanism is **arm-to-torso separation**, and it is now
demonstrated in both directions on one character:

| Drell mesh | width | arms | riggable |
|---|---|---|---|
| original | 0.4190 | one forward, fists closed | **False** |
| watertight rebuild | 0.4190 | one forward, fists closed | **False** |
| narrow A-pose | 0.4185 | down, near-vertical, pauldrons overlapping them | **False** |
| **wide A-pose** | **0.5483** | **out, clear background between arm and body** | **TRUE** |

Same character, same generator, same reconstruction settings, same decimation. The only
thing that moved was how far the arms stand off the torso.

**And width alone is not the variable — separation is.** Merchant passes at width 0.3773,
*narrower* than the Drell A-pose that fails at 0.4185. Merchant is unarmoured, so its arms
hang clear of a narrow torso. Drell's flared pauldrons bridge the upper arm into the torso
silhouette, so an armoured figure needs the arms raised further to reach the same actual
separation. **Armour costs you arm angle.**

### So the clause needs the gap stated, not the direction

Clause 1 above says "held away from the torso". That was not enough: it produced arms
hanging near-vertical and the check refused. The requirement is a **visible, continuous gap
of background between each arm and the body, from armpit to wrist** — and for a figure in
plate with pauldrons, reaching that takes roughly a forty-five degree lift.

### The base figure is a BIND POSE, not a shipping pose

The pose that passed looks like a man surrendering. That does not matter and is worth
saying plainly: the base figure exists to be rigged, and a rigged figure is posed afterwards
by its bones. Optimise the base pose for the rigger, not for the eye. This is why T-pose and
A-pose are industry bind poses in the first place.

### What the rig came back with

`drell_rigged_mixamo.glb`, Mixamo spec, **23 joints**, skinned (JOINTS_0 + WEIGHTS_0),
root `Root`, hierarchy depth 9, anatomy coherent (hips 0.535 of height, head 0.840, toes
0.016). **Hand joints `mixamorig:LeftHand` and `mixamorig:RightHand` are the sockets.**
No finger joints - a 23-bone reduced biped, not the ~65-bone full Mixamo skeleton.

**Tripo DID replace the mesh**, as pre-registered: 140,234 vertices returned against
686,676 sent, re-normalised to height 1.0 with feet at the origin. That is why the route
takes only the bones. Mapping them back is a similarity transform, exactly because the proxy
was sent standing in the real mesh's own world space.

Sockets in our coordinates, and checked rather than assumed: `RightHand` sits **0.6 mm**
from the mesh surface with 831 vertices within 40 mm; `LeftHand` **33.3 mm** with 424. Both
are in real hand geometry; the left one is offset enough to want refining. `compute_occupancy`
reports False for both and means nothing here - this mesh class is a hollow double-walled
shell, and this repo already records that a volumetric predicate reads *outside* at a
standing figure's own chest.

---

## ⚠ SUPERSEDED CORRECTION, kept for the sequence — "the pose is not the cause"


**The causal claim below is FALSIFIED and is kept rather than deleted, because the
correction is the useful part.** I wrote that the pose is what decides whether a figure can
be auto-rigged. It was an inference by elimination from the watertight control, and
elimination only works if the candidate list is complete. It was not.

**Measured after this file was written:** Drell was regenerated in exactly the A-pose this
file specifies — arms down and clear, hands open and empty, nothing held — and reconstructed
(`drell_apose_s42.glb`, 34.1 MB, peak 3.4 GB). The mesh is the best of the character to
date: whole from front, both sides and back, two legs, two arms, two open hands. Depth fell
0.3207 -> 0.2643 and the front-most mass moved from 58.5% of height to 1.5%, so the pose
genuinely changed.

**`riggable = False`.** Byte-identical verdict file to the two earlier Drell runs.

So the pose is **not** the cause either. What is still established is only the negative set:
**untextured input, component count, topology and pose are all ruled out**, each by a
measurement rather than an argument. Drell refuses across three different meshes while
merchant and Halle pass. The cause is Drell-specific and **unidentified**. Untested
candidates, named so nobody re-derives them: the closed helm (no face for a head fit), the
overlapping plates of full armour, the flared pauldrons at the shoulder joint.

**Why the rule below survives its own broken justification:** the Director set it as a
standing instruction, and it is independently right for the thing it is actually for —
a prop that attaches to a socket must not be baked into the figure's hands. It is a
*pipeline* rule. It is not, on this evidence, a *riggability* rule, and this file must not
be cited as if it were.

## Why the rule is right anyway

A prop baked into a generated pose has to be re-solved against that geometry for every
asset, by eye. That is how one arc spent four placements getting **3.1 cm² of contact where
a grip needs ~16**. Arms at the side and empty hands means the figure is generated once and
every prop after it is a stored offset plus a measured gate.

## The evidence as it stands — read the correction above before using this table

Five free rig checks across three characters and four meshes, all untextured clay, all
decimated identically to 200k triangles and submitted through the same path:

| subject | components | largest shell | pose | riggable |
|---|---|---|---|---|
| merchant | 3,125 | 31.3% | neutral, arms down | **True** |
| halle | 2,059 | 28.0% | neutral, arms down | **True** |
| drell raw | 2,489 | 37.2% | one arm forward, fists closed | **False** |
| drell rebuilt watertight | **182** | **99.2%** | one arm forward, fists closed | **False** |
| **drell A-pose** (new plate, new reconstruction) | 2,176 | 19.9% | **neutral, arms down, hands open** | **False** |

The fourth row removed every topology pathology — rebuilt from first-hit raycasts and
Poisson-closed to a single 99%-dominant shell, silhouette and pose untouched — and still
failed. The fifth row changed the pose to the one this file specifies, on a freshly
generated plate and a fresh reconstruction, and **also failed**. Topology does not track the
answer. Neither does pose. Both were tested; both are out.

Two other candidate causes died on the way:

- **Untextured input.** All three are bare clay and two passed. The "not suitable for
  untextured meshes" warning belongs to Meshy's node, not Tripo's.
- **Component count.** The number that was being reasoned from — 38–41k — was a full-mesh,
  pre-weld count that the service never saw. On the operand it actually received, Drell sits
  *between* the two that passed.
- **Reach and depth.** Halle is as deep as Drell and reaches *further* from its own trunk
  axis, and passes. So "a limb sticks out" does not separate them either, which is why the
  pose had to be tested rather than assumed.

## What this changes about a prop

A prop is no longer something the figure is generated holding. It is a separate mesh,
attached to a named bone, placed by one stored offset, and graded by
`tools/verify/prop_contact.py` on measured contact area rather than by eye.

That is also what makes the route scale: **rig once per character, then every sword,
shield, spear or lantern after that is an offset and a gate.** A figure generated
mid-gesture has to be re-solved for every prop and cannot be rigged at all.

## Its relationship to HELD-PROP.md

[HELD-PROP.md](HELD-PROP.md) is not withdrawn and nothing measured in it is overturned. Its
scope narrows: it governs the case where the prop genuinely **must be in the conditioning
image** — a single-mesh reconstruction, or a canon quality that only exists where a hand and
an object meet. On this route that case is now the exception. The default is this file.

Note the two contracts give opposite instructions about the hands *by design*:
HELD-PROP replaces `hands empty and open`; this file requires it. Which one applies is
decided by whether the prop is a separate mesh, and on the sprite route it is.

## The trap this closes

The arc that produced this rule spent four placements trying to make a slab read as held
against a closed, solid fist — **3.1 cm² of contact where a grip needs ~16** — before anyone
asked whether the figure could be rigged at all.

**Stop generating the pose you want and placing a prop against it.** That half stands. The
other half — *generate the pose that rigs* — is currently unsupported for this character:
the pose was changed to the one that works on two other figures and the answer did not move.
Whatever Drell is refused for, it is not yet known.

---

## The bind-pose tax, measured 2026-09-22

The wide A-pose that passes the rig check is far from any shipping pose, and closing that
distance costs geometry. Measured on `drell_rigged_mixamo.glb`, same rig, same bake, one
variable — how far the upper-arm bones are rotated from the bind pose:

| rotation from bind | shoulders |
|---|---|
| 0° (bind) | clean |
| **~20°** | **clean** |
| **~110°** (arms to the sides) | **shredded** — pauldrons torn into spikes |

Tripo's auto-weights cannot carry a large arm rotation on this armour, and the mechanism is
visible in the class: **the pauldrons are separate shells**, partly weighted to the torso and
partly to the arm, so they come apart first and worst.

**So the base pose is a trade, not a free choice.** Raise the arms far enough and the rig
check passes but the shipping pose costs a 110° rotation the weights cannot survive. Lower
them and the check refuses outright. The usable base pose is **the smallest arm angle that
still passes the free rig check** — which is findable by bisection between the narrow A-pose
(refused) and the wide one (accepted), at zero cost per probe, and is a reusable pipeline
constant once measured rather than a per-character judgement.

⚠ **Not yet measured.** The bisection has not been run. Until it is, a shipping pose from
this route needs either a small rotation off a lucky bind pose, or weight repair, and
neither is currently automated.

### One more property of the service's output, recorded so nobody debugs it twice

**Tripo's rigged GLB ships a stray unskinned 42-vertex Icosphere at ±1.0** beside the body.
Taking every `MESH` object from the import blows a baked bbox to 1.90 × 2.00 × 2.00 and
adds 42 vertices that were never sent. `tools/pose_rig.py` filters on *has an ARMATURE
modifier* — semantic, not a name or a size threshold — and gates on both vertex count and
longest axis. Both gates fired on the first implementation, which is how the icosphere was
found at all.
