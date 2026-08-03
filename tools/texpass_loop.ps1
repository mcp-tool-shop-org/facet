# TEXTURE-SPACE PASS — full loop: clean v3 state -> 8 guarded strokes -> finalize -> renders
$ErrorActionPreference = 'Stop'
$T  = 'E:\AI\training\saltroad_bake_fix\tools'
$X  = 'E:\AI\training\saltroad_bake_fix\warrior\texpass'
$S  = "$X\state"
$P  = 'E:\AI\training\saltroad_bake_fix\warrior\hero_bake'
$G  = "$X\stage1_v3.glb"
$py = 'E:\AI-Models\trellis2-env\Scripts\python.exe'
$bl = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'

# reset state to the clean stage-1 v3 output
Get-ChildItem $S -Directory -Filter 'job_*' -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Copy-Item "$X\styled_v3.png" "$S\atlas.png" -Force
Copy-Item "$X\styled_v3_holes.png" "$S\holes.png" -Force
Copy-Item "$X\styled_v3_styled_mask.npy" "$S\styled_mask.npy" -Force
Remove-Item "$S\atlas.prev.png" -Force -ErrorAction SilentlyContinue
Write-Output "[loop] state reset to v3"

$views = @(
  @{y=90;  e=0;  job='job_y+090_e+00'},
  @{y=270; e=0;  job='job_y+270_e+00'},
  @{y=45;  e=0;  job='job_y+045_e+00'},
  @{y=135; e=0;  job='job_y+135_e+00'},
  @{y=225; e=0;  job='job_y+225_e+00'},
  @{y=315; e=0;  job='job_y+315_e+00'},
  @{y=0;   e=55; job='job_y+000_e+55'},
  @{y=180; e=55; job='job_y+180_e+55'}
)
foreach ($v in $views) {
  & $py "$T\texpass_iter.py" emit --state $S --prep $P --glb $G --yaw $v.y --el $v.e 2>&1 | Select-String '\[emit\]|ANDON'
  if ($v.job -eq 'job_y+270_e+00') {
    # blade flank + invented-medallion zone: policy exclusion (dilated projected steel, not diffusion)
    & $py -c "import numpy as np; from PIL import Image; p=r'$S\job_y+270_e+00\mask.png'; m=np.asarray(Image.open(p).convert('L')).copy(); m[80:580,385:470]=0; m[675:785,365:445]=0; Image.fromarray(m).save(p); print('[loop] y270 mask surgery applied')"
  }
  & $py "$T\texpass_brush.py" --job "$S\$($v.job)" 2>&1 | Select-String '\[brush\] E|ANDON'
  & $py "$T\texpass_iter.py" commit --state $S --prep $P --edited "$S\$($v.job)\inpainted.png" --cam "$S\$($v.job)\cam.json" 2>&1 | Select-String '\[commit\]|ANDON'
}

& $py "$T\texpass_finalize.py" --state $S --prep $P --out "$X\atlas_final.png" 2>&1
& $bl -b -P "$T\bake_hero_pack.py" -- --prep-glb "$P\prep_uv.glb" --atlas "$X\atlas_final.png" --out "$X\warrior_texpass.glb" 2>&1 | Select-String '\[pack\]|ANDON'
& $bl -b -P "$T\turn_render.py" -- --glb "$X\warrior_texpass.glb" --out "$X\renders_final" --tag fin --flat 2>&1 | Select-String 'view 7'
& $bl -b -P "$T\head_render.py" -- --glb "$X\warrior_texpass.glb" --out "$X\renders_final" --tag fin_head --views 0 --flat 2>&1 | Select-String '\[head\]'
Write-Output "[loop] DONE"
