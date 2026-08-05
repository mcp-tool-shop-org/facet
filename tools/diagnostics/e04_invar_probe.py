"""What did brush_cloud_step's invariance ANDON actually fire on?

The check calls a pixel "outside the figure" when the EMITTED render is within 1.5 levels
of 107 (= 0.42 grey). E08 Amendment 32 recorded that 0.42 is ALSO project_twins'
--hole-grey, so an unpainted HOLE ON REAL SURFACE renders at exactly the background value
and is indistinguishable from background BY COLOUR, by construction. A32 fixed that operand
inside texpass_iter's commit by intersecting with emit's geometry `hit.png`. This asks
whether the same colour proxy is what fired here - measured, not assumed.

geometry hit -> the brush painting surface it was told to paint (false ANDON)
no geometry  -> the cloud repainting the backdrop (true ANDON)
"""
import json
import os

import numpy as np
from PIL import Image
from scipy.ndimage import label, maximum_filter

J = r"E:\AI\training\facet_next\E04_stroke\state\job_y+300_e+00"
em = np.asarray(Image.open(os.path.join(J, "render.png")).convert("RGB"), dtype=np.float32)
ed = np.asarray(Image.open(os.path.join(J, "inpainted.png")).convert("RGB"),
                dtype=np.float32)
hit = np.asarray(Image.open(os.path.join(J, "hit.png")).convert("L"), dtype=np.float32) > 127
job = np.asarray(Image.open(os.path.join(J, "mask.png")).convert("L"), dtype=np.float32) > 127
thin = np.asarray(Image.open(os.path.join(J, "thin.png")).convert("L"),
                  dtype=np.float32) > 127

# the check's own two masks, reproduced exactly
bg = np.abs(em - 107.0).max(axis=-1) < 1.5
outside = maximum_filter((~bg).astype(np.float32), size=9) < 0.5
resid = np.abs(ed - em).max(axis=-1)
hot = (resid > 4.0) & outside
lab, nl = label(hot)
sizes = np.bincount(lab.ravel())[1:]
order = np.argsort(-sizes)

print("[probe] the check's 'outside the figure' set: %d px" % int(outside.sum()))
print("[probe]   of which ON GEOMETRY (hit.png):      %d px  (%.2f%%)"
      % (int((outside & hit).sum()), 100 * (outside & hit).sum() / max(outside.sum(), 1)))
print("[probe]   of which inside the JOB MASK:        %d px" % int((outside & job).sum()))
print("[probe] hot pixels (>4 levels, outside): %d" % int(hot.sum()))
print("[probe]   on geometry: %d (%.1f%%)   off geometry: %d"
      % (int((hot & hit).sum()), 100 * (hot & hit).sum() / max(hot.sum(), 1),
         int((hot & ~hit).sum())))
print()
print("[probe] the five largest hot components:")
print("  %-5s %8s %10s %10s %10s   %s" % ("cc", "px", "on hit", "in job", "in thin", "bbox"))
for i in order[:5]:
    m = lab == (i + 1)
    ys, xs = np.where(m)
    print("  %-5d %8d %9d%% %9d%% %9d%%   x %d..%d  y %d..%d"
          % (i + 1, int(m.sum()),
             round(100 * (m & hit).sum() / m.sum()),
             round(100 * (m & job).sum() / m.sum()),
             round(100 * (m & thin).sum() / m.sum()),
             xs.min(), xs.max(), ys.min(), ys.max()))

# the honest counterfactual: what would the check say with A32's operand?
out32 = maximum_filter(hit.astype(np.float32), size=9) < 0.5
ro = resid[out32]
hot32 = (resid > 4.0) & out32
lab2, nl2 = label(hot32)
cc2 = int(np.bincount(lab2.ravel())[1:].max()) if nl2 else 0
print()
print("[probe] WITH A32's OPERAND (geometry, not colour):")
print("[probe]   outside-the-figure set %d px" % int(out32.sum()))
print("[probe]   mean residual %.3f lv, max %.1f lv" % (ro.mean(), ro.max()))
print("[probe]   pixels over 4 lv: %d   largest connected component: %d px"
      % (int(hot32.sum()), cc2))
print("[probe]   the shipped bounds are mean<=1.0 and cc<200 -> %s"
      % ("PASS" if (ro.mean() <= 1.0 and cc2 < 200) else "STILL FIRES"))

# a crop of the largest component for the eye
i = order[0]
m = lab == (i + 1)
ys, xs = np.where(m)
pad = 60
y0, y1 = max(0, ys.min() - pad), min(em.shape[0], ys.max() + pad)
x0, x1 = max(0, xs.min() - pad), min(em.shape[1], xs.max() + pad)
sheet = np.concatenate([em[y0:y1, x0:x1], ed[y0:y1, x0:x1],
                        np.repeat((hit[y0:y1, x0:x1, None] * 255).astype(np.float32), 3, 2)],
                       axis=1)
Image.fromarray(sheet.astype(np.uint8)).save(
    r"E:\AI\training\facet_next\E04_stroke\out\invar_cc1_emitted_edited_hit.png")
print()
print("[probe] wrote invar_cc1_emitted_edited_hit.png (emitted | edited | geometry)")
