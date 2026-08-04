# E08 — Director's ruling: the shipped twin is the character

**Date:** 2026-08-04 · **Director's verdict, on the full-resolution twins:**
*"The image to the left is the character that I originally designed. I'll take the gold over
the fur, because the character is on point."*

Left = the shipped twin. Right = BG2-grey.

---

## What it decides

**Identity dominates registration.** BG2-grey registers better on every stable measure — IoU
0.9314 / 0.9222 against 0.9088 / 0.8900, painted fraction 18.95% / 19.93% against 17.38% /
17.01% on a 19.01% truth — and is visibly more legible: the open right hand is a smudge on the
shipped twin, the lower legs go vague, the figure sits smaller in frame.

**None of that outranks being the right character.** The gold knee plates, the charcoal boots
and the gold necklace are the design; the fur wraps are not.

## What is withdrawn

**A2R is off-canon and does not stand.** Its +4.0 points (39.1% → 43.0% of valid, 74.2% →
81.6% of reachable) were bought with a reference that is a different character. The measurement
was correct and the arm is not adoptable.

**The geometry-derived CONTROL is withdrawn as a twin-generation path.** It is what moved the
character — same mesh, same seed, same prompt, only the ControlNet input changed, and the man
changed with it. Adopted two amendments ago on registration evidence; the evidence was real and
the criterion was wrong.

## What stands

- **A2 stands, unchanged: 681,212 → 938,718 texels, 28.4% → 39.1% of valid, 53.8% → 74.2% of
  reachable.** It never touched the twins — it replaced the *projection* stage's keyed clay
  mask with the exact mesh silhouette. Canon-safe by construction.
- **The geometry mesh mask in `project_twins`** — same reasoning, different consumer. Adopted.
- **The fitted-background estimator and the bbox andon.** Both measure as no-ops on a
  flat-background twin (−0.1 points, bbox within 1.2%), and both catch a failure that has now
  occurred three times. Harmless to keep, and they are the only reason a gradient-background
  twin was measurable at all.
- **A3's finding**: the absolute erosion's cost at the blade is necessary, not accidental.

## The correction to the record

**Amendment 4's original halt was right, and the reframing away from it was wrong.**

> *"An arm that improves keying by changing the reference has broken the thing it was
> protecting."*

That halt fired on BG1, was re-examined as a registration question, and registration said the
new twin was better. It was better *as a registration target* and wrong *as the character*.
The pre-registered line — *"better registration is a better reference by our own criterion, no
taste required"* — is now falsified. **Taste was required, it was the Director's, and it was
the deciding input.**

**Executor's share of this:** the Director named gold knee plates as his choice and I answered
with an IoU table, which is how a canon call briefly became "fur, then". Canon is not a
measurement's to argue with. And these twins were shown for several turns only as columns in
downscaled contact sheets, against this repo's own standing rule — *at the Director's zoom, not
from a contact sheet.* The ruling arrived within one exchange of showing them at full
resolution.

## The provenance defect is now critical, not filed

The canon reference **cannot be regenerated.** Built identically — same clay, same default
prompt, same seed, same keyed-mask control — BG1-grey does not reproduce the shipped twin
(painted 17.73% vs 17.38%, IoU 0.9040 vs 0.9088). Its generation parameters are not in the
repo: `E02-prompts.json` holds the eight brush strokes, not the two twin cameras, and
`restylize_views.py` takes a single front-flavoured `--prompt`.

**The asset the whole route is built to carry is a file we can copy and cannot recreate.** That
was an inconvenience while it was one candidate among several. It is now the canon, and any
change to the generation path risks a character we cannot get back.

## Open

1. **The blade.** Untouched by this ruling and still the loudest defect: the erosion's cost is
   necessary, the shipped twin's blade is thin, and nothing in E08 has moved it.
2. **Arm B (eight cameras).** The arithmetic that justified it — 74.10% reach × 81.6%
   acceptance ≈ 60.5% coverage — used A2R's acceptance rate. On A2's canon-safe 74.2% it is
   **~55%**, still against 28.4%, and still the largest change available. But it requires
   generating six new twins through a path that just demonstrated it can move the character.
3. **Whether gold knee plates can be had on a legible twin at all** is untested. The prompt
   that produced the shipped twin's knee plates does not mention them.
