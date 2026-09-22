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

## ⚠ CORRECTION, same day — the rule stands, my reason for it did NOT

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
