#!/usr/bin/env bash
# E08 Amendment 32 step 2 — void and replay.
#
# One operation that is simultaneously the ROLLBACK of stroke 7's illegitimate commit, the
# VERIFICATION of that rollback, and the ANCHOR for the A32 fix: the backdrop was flat on all
# six eye-level strokes, so intersecting the trust mask with geometry must be a NO-OP where the
# premise held. If any count moves, the fix is not a no-op on clean input and the whole
# remediation is suspect.
#
# Pre-registered gate: 2,507 / 3,859 / 2,017 / 4,103 / 6,526 / 10,636 -> holes 719,503, and the
# final atlas byte-identical to the preserved pre-stroke-7 atlas. Any digit differs -> HALT.
#
# emit is re-run per stroke because the A32 emit writes hit.png, which the fixed commit needs.
# It must reproduce render.png and mask.png byte-for-byte from the same state, and that is
# asserted here rather than assumed — if render.png moved, the saved inpainted.png no longer
# corresponds to its input and the replay is invalid.
set -u
A=/e/AI/training/facet_E08/ARMB
P="E:/AI-Models/trellis2-env/Scripts/python.exe"
PREP=E:/AI/training/facet_E06/C1/prep
TOOLS=E:/AI/facet/tools

ORDER=(y+090_e+00 y+270_e+00 y+045_e+00 y+135_e+00 y+225_e+00 y+315_e+00)
YAWS=(90 270 45 135 225 315)
EXPECT=(2507 3859 2017 4103 6526 10636)
EXPECT_HOLES=(746644 742785 740768 736665 730139 719503)

echo "=== RE-SEED from the banked 8-camera atlas ==="
cp $A/stage1_8cam.png             $A/state/atlas.png
cp $A/stage1_8cam_holes.png       $A/state/holes.png
cp $A/stage1_8cam_styled_mask.npy $A/state/styled_mask.npy
rm -f $A/state/atlas.prev.png
echo "seeded"

FAIL=0
for i in "${!ORDER[@]}"; do
  k=${ORDER[$i]}; yaw=${YAWS[$i]}; exp=${EXPECT[$i]}; exph=${EXPECT_HOLES[$i]}
  d=$A/state/job_$k
  echo ""
  echo "--- stroke $((i+1))  $k ---"
  ( cd /e/AI/training && "$P" $TOOLS/texpass_iter.py emit --state $A/state --prep $PREP \
      --glb $A/stage1_8cam.glb --yaw $yaw --el 0 --thin-extent 0.03 ) 2>&1 | grep -E "hole px|ANDON"
  # emit determinism: the saved inpainted.png was generated FROM these bytes
  for f in render mask; do
    if cmp -s $d/$f.png $d/$f.orig.png; then echo "    $f.png byte-identical to the original"
    else echo "    !! $f.png DIFFERS from the original — inpainted.png no longer corresponds"; FAIL=1; fi
  done
  out=$( ( cd /e/AI/training && "$P" $TOOLS/texpass_iter.py commit --state $A/state --prep $PREP \
      --edited $d/inpainted.png --cam $d/cam.json --facing-min 0.25 ) 2>&1 \
      | grep -E "trust mask|diagnostic|\[commit\] wrote|ANDON" )
  echo "$out" | sed 's/^/    /'
  # NB: tr -d '>-,' treats '>-,' as a RANGE and errors. Extract digits positionally.
  got=$(echo "$out" | grep -oE "wrote [0-9,]+ texels" | grep -oE "[0-9,]+" | tr -d ',')
  goth=$(echo "$out" | grep -oE "holes [0-9,]+ -> [0-9,]+" | grep -oE "[0-9,]+$" | tr -d ',')
  if [ "$got" = "$exp" ] && [ "$goth" = "$exph" ]; then
    echo "    ANCHOR OK: $got texels, holes -> $goth"
  else
    echo "    !! ANCHOR FAILED: got $got texels / holes $goth, expected $exp / $exph"; FAIL=1
  fi
done

echo ""
echo "=== GATE: atlas byte-identical to the preserved pre-stroke-7 atlas? ==="
if cmp -s $A/state/atlas.png $A/out/TARGET_pre_stroke7_atlas.png; then
  echo "  IDENTICAL — the rollback is exact and the A32 fix is a no-op on clean input"
else
  echo "  !! DIFFERS"; FAIL=1
  "$P" - <<PY
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
a=np.asarray(Image.open("E:/AI/training/facet_E08/ARMB/state/atlas.png")).astype(np.int32)
b=np.asarray(Image.open("E:/AI/training/facet_E08/ARMB/out/TARGET_pre_stroke7_atlas.png")).astype(np.int32)
d=np.abs(a-b); print("  differing px:", int((d.max(axis=-1)>0).sum()), " max|d|:", int(d.max()))
PY
fi
echo ""
[ $FAIL -eq 0 ] && echo "REPLAY GATE: PASS" || echo "REPLAY GATE: FAIL — halt"
exit $FAIL
