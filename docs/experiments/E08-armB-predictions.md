# Arm B — predictions, before the eight twins exist

**NOT BLIND.** Full E08 record in context. Recorded before submission.

## What the contradiction test licenses me to predict

The prompt controls named attributes at a **7.4× margin over the held control**, measured
within-cloud. The advisor's reshaping follows from that: per-view prompts carrying the full
spec are the **mechanism** for holding identity across views, not a hope. So:

| # | prediction |
|---|---|
| **B1** | **Named elements arrive at front-view reliability on every view they are visible from.** Gold pauldrons, red beard, green tunic, dark red skirt, gold knee plates on all eight, subject to visibility. |
| **B2** | **Any drift lands in structure, not in named attributes** — proportions, silhouette registration, blade thickness — because structure is mesh- and control-held and the attributes are prompt-held. |
| **B3** | **Reference coverage rises to ~55% of valid** from A2's 39.1%, per 74.10% reach × 81.6% acceptance. I hold this loosely: the acceptance rate was measured on two near-orthogonal cameras, and eight overlapping ones may accept differently. |

## The one I expect to be wrong about, and why it is stated

**B4 — the rear views.** I deliberately did **not** view-gate the beard out of the rear prompts
(reasoning in `E08-armB-prompts.json`): E01's face-on-the-back-of-the-head came from a *broken*
control, and the control is now the exact silhouette at IoU 1.000000. Gating would have removed
the very thing B1 is about.

**If a beard, a face or frontal detail appears on views 3, 4 or 5, B4 is falsified and the cause
is my prompt choice, not the control.** That is a real failure with a known fix (view-gating),
and it is recorded now so it cannot be reinterpreted as something else afterwards. I hold "no
frontal detail on rear views" at roughly **75%** — the control locks orientation, but nothing
measured on this stack says an unfiltered frontal spec is safe at denoise 0.92.

## The instrument's floor applies here too

From the contradiction test: **held regions moved 5.06–6.91 ΔE from a prompt change alone.** An
element effect below roughly **ΔE 6** is indistinguishable from global repaint. Any per-view
comparison I report will be read against that floor, not against zero.

## Pinned

Seed 770700, steps 20, cfg 2.5, euler/simple, denoise 0.92, lora_w 0.75, cn 0.9 start 0.0
end 1.0, shift 3.1 — identical to the anchor and to both contradiction arms. Eight views, one
batch, within-cloud. Controls built locally by `restylize_views.py --emit-only`, so control
construction stays in one place; view 0's control reproduced N11's sidecar exactly at
**20,973 px (canny 15,325 + contour 9,958)**.
