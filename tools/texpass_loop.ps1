# TEXTURE-SPACE PASS — the loop: seed state -> N guarded strokes -> finalize -> renders.
#
# Parameterised, because the previous version hardcoded one character's paths AND one
# character's blade rectangle. Two things changed and both matter:
#
#   1. THE BLADE POLICY IS NO LONGER A PIXEL RECTANGLE. It used to be
#        m[80:580, 385:470] = 0  on the yaw-270 job
#      applied by an inline python -c inside this file. That rect was measured against
#      A0's silhouette in A0's framing; W3 reconstructs the same clay 38% narrower, so
#      the rect is not merely unportable, it is wrong on the very next mesh. The policy
#      is unchanged — thin hard-surface props take projected/dilated colour, never
#      invented content — but it is now derived per view by -ThinExtent, which measures
#      the figure's extent ALONG THE VIEW RAY. See texpass_iter.py --thin-extent, and
#      tools/superseded/texpass_thin_mask.py for the two probes that failed first.
#      Measured on W3: the blade is a large hole in ALL EIGHT views, not only yaw 270,
#      so the single-rect surgery was already insufficient in principle.
#
#   2. PROMPTS ARE PER VIEW, from -PromptsJson, keyed by job name. A shared prompt is
#      what put a face on the back of the head (E01) and what invented a corroded wavy
#      blade and a belt medallion in the first full loop. The recipe lives in a file
#      under version control rather than only in a log, because the previous run's
#      recipe was lost exactly that way.
#
# Gates: -StopBeforeCommit runs emit + brush for the selected strokes and stops without
# writing to the atlas, so the first stroke can be judged before seven more are spent.
#
# Standards compliance:
#   PIN_PER_STEP — every path, the seed, the prompts file and the thin-extent threshold
#     are explicit parameters echoed into the log; no literal is buried in the body.
#   ANDON_AUTHORITY — $ErrorActionPreference='Stop'; texpass_iter's commit asserts holes
#     strictly shrink and that styled texels are never touched; the brush raises on a
#     comfy execution error; -StopBeforeCommit is a human gate between stroke 1 and 2.
#   NAMED_COMPENSATORS — the only mutation is the atlas under -StateDir. commit writes
#     atlas.prev.png before every stroke, and every brush output is seed-stamped, so a
#     re-roll never destroys a prior stroke. Undo = re-seed state from -Stage1Atlas and
#     re-run. Owner: the session running the loop.
#   EXTERNAL_VERIFIER — this script grades nothing. It emits renders for a human.
#
#   texpass_loop.ps1 -Tools E:\AI\facet\tools -Prep DIR -StateDir DIR -Glb packed.glb
#                    -Stage1Atlas styled.png -OutDir DIR -PromptsJson prompts.json
#                    [-ThinExtent 0.03] [-Seed 770700] [-From 1] [-To 8]
#                    [-SeedState] [-StopBeforeCommit] [-SkipFinalize]

param(
  [Parameter(Mandatory=$true)][string]$Tools,
  [Parameter(Mandatory=$true)][string]$Prep,
  [Parameter(Mandatory=$true)][string]$StateDir,
  [Parameter(Mandatory=$true)][string]$Glb,
  [Parameter(Mandatory=$true)][string]$Stage1Atlas,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [Parameter(Mandatory=$true)][string]$PromptsJson,
  [double]$ThinExtent = 0.03,
  [int]$Seed = 770700,
  [int]$From = 1,
  [int]$To = 8,
  [switch]$SeedState,
  [switch]$StopBeforeCommit,
  [switch]$SkipFinalize,
  [string]$Python  = 'E:\AI-Models\trellis2-env\Scripts\python.exe',
  [string]$Blender = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
)
$ErrorActionPreference = 'Stop'

# The eight cameras. Six yaws at eye level plus two at +55 elevation, which are the only
# cameras that can see the crown, the tops of the pauldrons and the tops of the boots.
#
# ORDER IS LOAD-BEARING, not cosmetic, and it lives in the recipe file rather than here.
# The brush runs at denoise 1.0 inside the mask; a hole texel has no content to preserve,
# so the model composes freely and anchors only on the prompt and the contour. How much
# anchoring context a camera gets is therefore decided by what has already been committed
# when its turn comes. Measured on W3: opening on yaw 90 — 95% hole, the camera furthest
# from both styled poles — returned a plaited belt, a strap across the upper arm, and a
# tunic extended to mid-thigh. Spiralling outward from the styled poles instead means the
# first stroke already sees roughly half its surface painted. Give -PromptsJson an
# `_order` array of job keys to set it; the fallback below is the historical order.
$default_order = @('y+090_e+00','y+270_e+00','y+045_e+00','y+135_e+00',
                   'y+225_e+00','y+315_e+00','y+000_e+55','y+180_e+55')

$prompts = Get-Content $PromptsJson -Raw | ConvertFrom-Json
$order = if ($prompts.PSObject.Properties.Name -contains '_order') { $prompts._order } else { $default_order }
$negative = if ($prompts.PSObject.Properties.Name -contains '_negative') { $prompts._negative } else { $null }
New-Item -ItemType Directory -Force -Path $StateDir, $OutDir | Out-Null

Write-Output "[loop] tools       $Tools"
Write-Output "[loop] prep        $Prep"
Write-Output "[loop] glb         $Glb"
Write-Output "[loop] state       $StateDir"
Write-Output "[loop] prompts     $PromptsJson"
Write-Output "[loop] thin-extent $ThinExtent   seed $Seed   strokes $From..$To of $($order.Count)"
Write-Output "[loop] order       $($order -join ' -> ')"
if ($negative) { Write-Output "[loop] negative    $negative" }

if ($SeedState) {
  $base = [IO.Path]::Combine([IO.Path]::GetDirectoryName($Stage1Atlas),
                             [IO.Path]::GetFileNameWithoutExtension($Stage1Atlas))
  Copy-Item $Stage1Atlas            "$StateDir\atlas.png"       -Force
  Copy-Item "${base}_holes.png"     "$StateDir\holes.png"       -Force
  Copy-Item "${base}_styled_mask.npy" "$StateDir\styled_mask.npy" -Force
  Remove-Item "$StateDir\atlas.prev.png" -Force -ErrorAction SilentlyContinue
  Write-Output "[loop] state seeded from $Stage1Atlas"
}

for ($i = $From; $i -le $To; $i++) {
  $key = $order[$i - 1]
  if ($key -notmatch '^y([+-]\d+)_e([+-]\d+)$') { throw "ANDON: malformed order key '$key'" }
  $yaw = [int]$Matches[1]
  $el  = [int]$Matches[2]
  $job = "job_$key"
  $p   = $prompts.$key
  if (-not $p) { throw "ANDON: no prompt for $key in $PromptsJson" }
  Write-Output "[loop] --- stroke $i/$($order.Count)  $job ---"
  $sw = [Diagnostics.Stopwatch]::StartNew()

  & $Python "$Tools\texpass_iter.py" emit --state $StateDir --prep $Prep --glb $Glb `
      --yaw $yaw --el $el --thin-extent $ThinExtent 2>&1 |
      Select-String '\[emit\]|ANDON'

  $brushArgs = @('--job', "$StateDir\$job", '--seed', $Seed, '--prompt', $p)
  if ($negative) { $brushArgs += @('--negative', $negative) }
  & $Python "$Tools\texpass_brush.py" @brushArgs 2>&1 | Select-String '\[brush\]|ANDON'

  if ($StopBeforeCommit) {
    $sw.Stop()
    Write-Output ("[loop] stroke {0} painted, NOT committed ({1:0.0}s) — gate" -f $i, $sw.Elapsed.TotalSeconds)
    continue
  }

  & $Python "$Tools\texpass_iter.py" commit --state $StateDir --prep $Prep `
      --edited "$StateDir\$job\inpainted.png" --cam "$StateDir\$job\cam.json" 2>&1 |
      Select-String '\[commit\]|ANDON'
  $sw.Stop()
  Write-Output ("[loop] stroke {0} done ({1:0.0}s)" -f $i, $sw.Elapsed.TotalSeconds)
}

if ($StopBeforeCommit -or $SkipFinalize) { Write-Output "[loop] HALTED before finalize"; return }

& $Python "$Tools\texpass_finalize.py" --state $StateDir --prep $Prep --out "$OutDir\atlas_final.png" 2>&1
& $Blender -b -P "$Tools\bake_hero_pack.py" -- --prep-glb "$Prep\prep_uv.glb" `
    --atlas "$OutDir\atlas_final.png" --out "$OutDir\hero_texpass.glb" 2>&1 |
    Select-String '\[pack\]|ANDON'
Write-Output "[loop] DONE"
