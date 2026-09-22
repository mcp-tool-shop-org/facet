# Prop library contract — separate GLBs, at true size

**Director, 2026-09-22.** Props are **separate GLB files**, each authored at its **true
size**, kept as a library of add-on options. A character is generated empty-handed
([BASE-FIGURE.md](BASE-FIGURE.md)); a prop is attached afterwards.

## The premise, measured

**Every reconstruction this route produces is normalised to 1.002 on its longest axis.**
Measured 2026-09-22 across four unrelated assets:

| asset | size (x, y, z) | longest |
|---|---|---|
| `drell_body_s42.glb` | 0.4190, 1.0021, 0.3207 | **1.00207** |
| `drell_apose_s42.glb` | 0.4185, 1.0020, 0.2643 | **1.00196** |
| `drell_shield_emblem_s42.glb` | 0.7013, 1.0018, 0.2013 | **1.00181** |
| `drell_shield_s42.glb` | 0.5873, 1.0021, 0.1335 | **1.00213** |

So **a prop mesh carries no true scale whatsoever.** A shield loaded as-is is 1.8 m tall —
a door. A figure is only correctly sized by coincidence: a human happens to be the thing the
unit box was fitted to.

That is what the old compose script's `HEIGHT_FRAC = 0.42` was standing in for — a size
chosen by eye, per placement, with nothing recording what the object was supposed to be.
(It landed at 0.4209 units = **758 mm**, which is a plausible heater shield, by luck rather
than by declaration.)

## The rule

1. **One GLB per prop.** Never a variant of the character mesh, never fused into it.
2. **The GLB is stored at true size**, in the scene's unit system, so loading it is the
   whole of "getting it right". No consumer rescales a prop.
3. **The scene's unit system is stated once here: `1.0 unit = 1.8 m`.** A prop whose real
   longest dimension is `L` millimetres is stored with its longest axis at
   `L / 1800` units.
4. **Every prop carries a sidecar** declaring what it is and how big it really is, so the
   number is a property of the object rather than of whoever placed it last:

```json
{
  "prop": "heater_shield_sunburst",
  "source_glb": "drell_shield_emblem_s42.glb",
  "real_mm": 758,
  "real_axis": "height",
  "units_per_metre": 0.55556,
  "stored_longest_axis_units": 0.42111,
  "attach": "forearm_l",
  "grip": {"point_local": [0.0, 0.042, 0.0], "axis_local": [0, 0, 1]},
  "face_normal_local": [0, -1, 0]
}
```

5. **The declared size is checked against the mesh**, not trusted. A prop whose stored bbox
   disagrees with `real_mm / 1800` is refused, the same way a placement is refused when its
   contact area is too small.

## Why this is the thing that makes a thousand sprites possible

With it, a prop is data: a file, a real size, a grip point, a socket name. Attaching it to
any character is a lookup and a bone transform, and the only judgement left is a number
`tools/verify/prop_contact.py` reports. Without it, every prop on every character is an eye
judgement about scale *and* position at the same time — which is two guesses multiplied, and
is why four placements in a row missed.

It also survives the thing that is currently blocking the rig: **a prop library is useful
whether or not a given character can be auto-rigged.** A socket is the best consumer of it;
a hand-placed transform is a worse one, and still consumes the same file at the same size.

## What is not settled

- **Where the grip point comes from.** For a reconstructed prop nothing declares it. It is
  currently a stated constant per prop, like `real_mm`, and that is honest — but it has no
  gate, so a wrong grip point is invisible until a contact sheet shows it.
- **Real sizes themselves are authored numbers.** 758 mm for the heater shield is the size
  the existing placement happened to land on, recorded so it stops moving. It is not
  researched, and a Director's number should replace it.
