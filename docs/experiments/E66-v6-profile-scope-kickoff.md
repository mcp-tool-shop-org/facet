# E66 — view 6, the leftover crank

**Advisor spec, 2026-08-19. Executor: this session (Grok). Tree
`E:\AI\training\facet_E66\`. Spend: 1 generation.**

**Direction (the Director, on the E65 sheet):** E65 is perfect except view 6 —
the head turns toward the camera when it should stay straight ahead.

## What the pixels already show

Opened at full size this sitting:

- `clay_6.png` — true profile, head with the body, nose to frame-left.
- `a1_e65_v2.png` — same face-set prompt, the other profile, head aligned.
- `a1_e65_v6.png` — body in profile, face three-quarter to camera, both
  eyes and the smile visible.
- `a1_ring_v6.png` (E58) — the same crank, so this is not an E65 regression.

E65 v6's composed text still carries `olive skin`, `curious brown eyes`,
`a slight smile`, `crisp readable facial features` — the conservative
"profile keeps the face set" list ratified at E64. That list was reserved
as a phrase-vs-visibility mismatch (N9 plural eyes on a one-eye profile)
and was **not probed**. v2 survived it. v6 did not. The probe is now
justified, and it is only this view.

v6's graph has **no** E63 extra negative (`looking at the viewer…`). The
positive face terms are the remaining conflict.

## The one change

`scopes.views.6` drops `eyes` and `mouth`. `style_face` follows (legal
clause, keys off face-bearing surfaces). **Kept:** hair, face (olive
skin), neck, collar, garments, hands. The clay shows a profile cheek —
olive skin stays. Do not touch views 0–5 or 7. Do not raise cn.

One variable against E65 v6: those two occupant phrases (and the style
clause they take with them).

## Probe

One graph, cloned from `facet_E65/stage2/graph_6.json`. Only node 7
(positive text) and node 15 (prefix) change. Seed 770700, denoise 0.92,
E58/E65 controls. Gate at `view:6`. Gate E: 576×1024.

Sheet: clay_6 | E58 v6 | E65 v6 | E66 v6. Rank nothing.

## Prediction

Dropping the frontal face terms on this view will take the head back
toward the clay profile, the way dropping them took v3/v5 off the
over-the-shoulder crank. If it does not, the leftover is this camera's
control-vs-prior, and cn comes off the shelf for **one view**, not the
ring.

## Out of scope

The other seven views; a ring regen; cn unless this cell fails; W3;
painting; N9 re-word (still not this sitting).
