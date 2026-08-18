# A1 — identity specification (the reference-first exemplar)

**Status:** authored by the advisor, 2026-08-17, on the Director's direction (a brand new
humanoid exemplar, canon solid from the start, **no weapon** — a held object only confuses
the profile). **RATIFIED by the Director, 2026-08-17, as drafted** — all rows and all five
queue positions (the name A1 *the archivist*; the ink phrase as attested; one garment;
stubble unnamed, leaves; the umber word stands), recorded in
[a1.surfaces.json](a1.surfaces.json). His standing principle at ratification, paraphrased:
the quality is made in the edit — ratification is a baseline, not a freeze, and a
post-ratification canon edit is an ordinary versioned move whose test is the next
generation. Spec: [E57](../docs/experiments/E57-a1-reference-first-kickoff.md).

**Read off `canon/A1_reference.png` at full size.** That file is the visual target AND the
identity source at once, because — unlike W3 — the identity below is not reconstructed
from an artifact: it is the reference's **own generating prompt**, extracted from the
PNG's embedded ComfyUI graph. The phrase IS what produced the image. Provenance is
COMPLETE (see the recipe section at the bottom), where W3's founding pair is recorded
INCOMPLETE in [MANIFEST.md](MANIFEST.md).

**No weapon.** The figure holds nothing, wears no sheath, and the generating prompt
forbids it in so many words: *no weapons, no held objects, nothing crossing the body
silhouette*. There are no prop surfaces in this canon and none may be added without a
new ruling.

---

## Form

**Every element is a phrase from the generating prompt, verbatim.** W3's grammar law
([E08 Amendment 13](../docs/experiments/E08-ruling-gate0.md)) measured that stacked
compound modifiers are unreliable when ADDING to a generation — but A1's prompt used
compound and prepositional forms throughout (*"plum long-vest with fine gold embroidery
over a cream high-collared shirt"*) and they landed **at fresh generation**. Those
phrases are kept exactly as attested rather than decomposed, because a decomposed phrase
is a phrase that never generated anything. Whether the compound form survives
**restylize onto an already-painted surface** is the W3 Q3 question and stays open —
nothing here tests it.

## NAMED — must appear in the prompt, or it leaves

| # | element | note |
|---|---|---|
| N1 | plum long-vest with fine gold embroidery | ONE garment per the prompt: buttoned panel at the chest, open skirt below the sash, knee-length. The two-garment reading (coat + under-vest) is queue item Q3 |
| N2 | a cream high-collared shirt | collar shows at the throat; full billowed sleeves with banded cuffs are this garment's — the prompt names the shirt once and the sleeves arrive with it |
| N3 | an umber sash | the painted sash reads olive-gold; the WORD is the attested canon and the palette band will record what landed (queue item Q5) |
| N4 | slim dark-green trousers | |
| N5 | polished brown shoes | low shoes, not boots — laced, brown leather |
| N6 | olive skin | face, neck, hands |
| N7 | tousled dark curls | |
| N8 | ink-stained fingertips | ⚠ the painted extent EXCEEDS the phrase — marks across both hands, palms and backs. Queue item Q2: the phrase is canon by law; adopting the painted extent means re-wording, untested until the next generation |
| N9 | curious brown eyes | |
| N10 | a slight smile | |

**The archivist's working identity:** the framing clause *"A young archivist in his
20s"* is the subject's register — a scholar, not a soldier. It is a framing clause, not
a surface (see `legal_clauses` in the surfaces file).

## MESH-SUPPLIED — arrives through the control from geometry; record the dependency

| element | note |
|---|---|
| the silhouette itself | no mesh exists yet — binds at E57 Stage 2. The twin's only job will be to register to it |
| proportions | dual-attested: the prompt says *realistic stylized proportions* AND the mesh will carry them once built. Per the W3 precedent (Amendment 12), once the mesh exists, the mesh's body is the character's body |

## STYLE-SUPPLIED — arrives from prompt style terms (and any future LoRA); record so a model change is noticed

| element | note |
|---|---|
| painterly digital art with visible brushwork | in the generating prompt; whether a LoRA also carries it is not yet separated (same open state as W3) |
| rich saturated palette | prompt style term |
| crisp readable facial features | prompt style term |

## UNDER TEST — not yet filed

- **Stubble.** Light stubble is painted on the jaw and appears in no phrase. By the law
  it is arriving by accident and will leave the same way. Queue item Q4: name it (the
  compound *olive skin with light stubble* is a candidate — same untested compound class)
  or let it leave.
- **The N1 compound under restylize.** Fresh generation landed it; add-to-occupied is
  the open W3 Q3 class. First A1 restylize generation is the test.

## Provenance — COMPLETE

| | |
|---|---|
| source | `C:\Users\mikey\Downloads\Qwen-Image-2512_00021_.png`, frozen to `canon/A1_reference.png` |
| sha256 | `9417cd6492df34354e5d3f3d7809bf89ddd074f5b1b18725c166a59b97b48dde` |
| frame | 1136 × 1472 RGB — ÷16 both axes, generator-legal by construction |
| model | `qwen_image_2512_fp8_e4m3fn.safetensors` |
| sampler | euler / simple, denoise 1.0, seed 106 |
| recipe | full graph in `canon/A1-RECIPE.json` (machine-extracted, both text encoders, staging clause included) |
| staging | the pose and backdrop clauses (relaxed A-pose, hands empty and open, plain warm pale-grey studio backdrop, soft even lighting) live in the recipe — they are generation staging, not identity |

**Replay untested.** The recipe is complete; nobody has re-run seed 106 to confirm
byte-level reproduction, because a replay spends. If one is ever run, the hardware-anchor
law applies (an anchor before any measured use on other hardware).
