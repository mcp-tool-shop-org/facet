# E10 LAYER — identity specification (environment-contact, boot-top edition)

**Status:** authored by the advisor, 2026-08-05, in [E10 Ruling 5](../docs/experiments/E10-ruling.md).
Landed by the executor as authored. This is the layer's identity fixture — the galleon's
own [GALLEON-IDENTITY.md](GALLEON-IDENTITY.md) is untouched by it, because **the layer is
a second surface over the same UVs, not an edit of the first.**

---

## Form — the grammar rules, inherited as measured

**Every element is its own noun phrase** (E08 Amendment 13: head noun + minimal modifier
lands; stacked compound modifiers drop). **A specification determines what occupies a
surface and cannot add a second element to an occupied surface** (Amendment 15) — and
this is exactly why the waterline became a layer rather than an edit: the hull's planking
already occupies the hull, so a band asked *onto* it is an addition and would drop. On its
own surface, the coat is the occupant.

## NAMED — must appear in the prompt, or it leaves

| # | element | note |
|---|---|---|
| L1 | **a weathered tallow-white hull coat below the waterline** | The period "white stuff" — tallow-and-resin — its **top edge forming the painted line** at the placed `waterline_z`. Three grounds, all from [Ruling 5](../docs/experiments/E10-ruling.md): it is what the static half of a period waterline *is* (RG02 Q3 separated the static boot-top, which is genuinely painted art, from the dynamic wet/foam band, which every shipped source computes shader-side); its pale warm register sits **inside the ship's existing warm band**, so no new palette band is invented; and it **contrasts hard with the dark foot planking** (the re-roll's tar at h 43, L\* ~10), which matters because the toggle's legibility *is* W3's gate. |

## GEOMETRY-SUPPLIED — arrives from the contact mask, not the prompt

| element | note |
|---|---|
| **the line's height** | `waterline_z = −0.43095`, canonical mesh frame — placed by the Director (E10 Ruling 3, *"I agree. C is the winner"*). Not a prompt term. |
| **the coat's extent** | the geometric contact mask: 98,543 texels, every one on the mesh's surface. The band's shape is a plane ∩ hull, so the hull's rocker is in it for free. |
| **the layer's alpha** | the contact mask itself (Ruling 1 decision 3). **No model-generated alpha in v1** — a boot-top's top edge is a painted hard line and the geometry already knows where it is. |

## NOT THE TARGET — recorded so it cannot drift back in

- **The founding exemplar's blue-grey** (rejected view-7 twin, seed 770700 — h 262.6,
  C\* 14.4, L\* 31.7). It painted the **dynamic** half: implied water against the hull.
  Under Amendment 1 that half belongs to the shader, and the exemplar's role is reduced to
  validating the band's **geometry** — it painted contact exactly where contact lives.
  W1 measures that and nothing else.
- **Foam, spray, a lap line, or any water surface.** Struck from W2's prompt by Amendment 1.
  Sea of Thieves generates foam from depth-buffer comparisons in the *water's* material;
  Horizon passes it through the *water's* vertex colour. It does not live on the hull's skin.

## The Director's open window

One sentence changes any of this. **Tarred black below the line**, or **a black boot-top
stripe above the coat**, are both authoring sentences and neither costs anything but a
re-run. The default, absent his word, is the tallow-white coat.

## What this fixture is for

W2's prompt takes **L1's element phrase verbatim**. If the coat arrives, it arrived because
it was named — and if a future layer element is not named here, it is arriving by accident
and will leave the same way.
