# Canon — the styled twin pair

**Ruled by the Director, 2026-08-04:** *"The image to the left is the character that I
originally designed. I'll take the gold over the fur, because the character is on point."*
Left was `twin_front.png`. → [E08-director-canon-ruling.md](../docs/experiments/E08-director-canon-ruling.md)

**This pair is an input, not an output.** It is versioned here against this repo's own
`.gitignore` rule, because that rule's stated premise — *"assets are large and regenerable"* —
is measured false for these two files.

---

## ⚠ ROLE CHANGED, 2026-08-04 — this is a SPECIFICATION SOURCE, not the projection reference

**Twins belong to a mesh. Identity belongs to the prompt.** E01 was right that a twin is
mesh-bound and must be regenerated per mesh; it was never the twin's job to carry identity.
The armour test proved it: the gold knee plates had only ever reached the image through **noise
in a broken ControlNet**, and one named phrase brought them back with the control byte-matched.
The Director further ruled that this pair's proportions — taller, narrower, longer-limbed than
the mesh — are the **same artifact**, painted freely because the control was missing a quarter
of the silhouette. → [E08-armour-test.md](../docs/experiments/E08-armour-test.md)

**Consequence: this pair's irreproducibility is no longer load-bearing.** It was critical only
while the artifact *was* the reference. As a source to read a specification off, it does not
need to be regenerable — **a specification reproduces where an artifact does not.** It stays
frozen and versioned; its role changed, not its status.

**Do not project from these.** They register at IoU 0.9088 / 0.8900 against a mesh whose
silhouette they under-fill (17.38% / 17.01% of frame against 19.01%), and the body they show is
not the mesh's body. Read canon off them; project from twins generated against an exact
silhouette control carrying the ratified spec.

| file | bytes | sha256 |
|---|---|---|
| `twin_front.png` | 505,710 | `a6158790525d8ac16cc2cc7f70731c165c2e21c7d46f62e7a161e6ba32448953` |
| `twin_back.png` | 481,616 | `a2be52130c1f2132b31604ea502683e4f0bcbcf27730b7d7eb3e71fd801c8e13` |

Originals remain at `E:\AI\training\facet_E01\tex_W3\twinsF\w3clay_{0,4}.png`. Every arm from
E02 to E08 that says "the shipped twins" means these.

---

## Provenance: INCOMPLETE, and recorded as incomplete rather than implied

### Known, and verified this session

| | |
|---|---|
| subject | W3 — TRELLIS.2 `1024_cascade` from `facet_E01/inputs/A0_source_clay.png`, seed 42 |
| mesh | `facet_E01/tex_W3/W3_287k.glb`, 287,170 faces, welded, decimated, native xatlas UVs |
| clay inputs | `facet_E01/tex_W3/views/w3clay_{0,4}.png` — **reproducible**, `turn_render.py --views 0,4 --clay` at default background re-renders them byte-for-byte (sha `4d65b67abae2928f`, `d2c6153be6e1d7ac`) |
| camera | ortho, `v_ext = bbox_z × 1.204`, 752×1024, centred on bbox mid; yaw 0 and yaw 180 |
| generator | `restylize_views.py` against a local ComfyUI — Qwen + saltroad LoRA + canny ControlNet |
| registration | painted figure 17.38% / 17.01% of frame against a 19.01% exact silhouette; IoU **0.9088 / 0.8900** |

### NOT known, and not derivable

- **The exact prompts.** `E02-prompts.json` holds the eight *brush-stroke* prompts, not the
  two twin cameras. `restylize_views.py` carries a single front-flavoured `--prompt` default.
  E02's report states the back twin used a per-view prompt; **its text is not in the repo.**
- **The exact sampler settings.** Seed, steps, cfg, denoise, LoRA weight and ControlNet
  strength all have defaults, and there is no record that the defaults were what ran.

### The reproduction attempt, and why it is not repeated

Rebuilt with the same clay, the same default prompt, seed 770700, and the same keyed-mask
control, the front twin **does not reproduce**: painted 17.73% vs 17.38%, IoU 0.9040 vs
0.9088. Close, not identical.

**Director's ruling, 2026-08-04: stop trying to derive it.** A seed sweep could produce a
match, and a match could not be verified as *the* recipe. The artifact is in hand; freezing it
is the answer, and its provenance is stated as incomplete rather than reconstructed.

---

## Standing constraints

**Do not regenerate this pair.** E08 measured that changing only the ControlNet input — mesh,
seed and prompt all pinned — produced a **different character**: gold knee plates and charcoal
boots became brown fur wraps, and the gold necklace was lost. A twin is two things at once, and
the pipeline only ever modelled one:

- a **mesh-bound projection source**, where "regenerate per mesh" is correct;
- a **canon identity reference**, where it is exactly wrong.

**Any new twin is a canon proposal and goes to the Director at full resolution**, one question
per twin — *is this the character* — not to a metric. Registration is not that question:
BG2-grey won every stable registration measure, was visibly more legible, and was the wrong
man.

**`restylize_views.py` now writes a `<stem>_gen.json` provenance sidecar** beside every twin it
produces, and takes per-view prompts from a versioned file. Neither existed when this pair was
made, which is why this manifest has an *unknown* section at all.
