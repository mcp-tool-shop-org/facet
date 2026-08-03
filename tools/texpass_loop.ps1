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
$views = @(
  @{y=90;  e=0},  @{y=270; e=0},  @{y=45;  e=0},  @{y=135; e=0},
  @{y=225; e=0},  @{y=315; e=0},  @{y=0;   e=55}, @{y=180; e=55}
)

$prompts = Get-Content $PromptsJson -Raw | ConvertFrom-Json
New-Item -ItemType Directory -Force -Path $StateDir, $OutDir | Out-Null

Write-Output "[loop] tools       $Tools"
Write-Output "[loop] prep        $Prep"
Write-Output "[loop] glb         $Glb"
Write-Output "[loop] state       $StateDir"
Write-Output "[loop] prompts     $PromptsJson"
Write-Output "[loop] thin-extent $ThinExtent   seed $Seed   strokes $From..$To"

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
  $v   = $views[$i - 1]
  $job = ("job_y{0:+000;-000}_e{1:+00;-00}" -f $v.y, $v.e)
  $key = ("y{0:+000;-000}_e{1:+00;-00}" -f $v.y, $v.e)
  $p   = $prompts.$key
  if (-not $p) { throw "ANDON: no prompt for $key in $PromptsJson" }
  Write-Output "[loop] --- stroke $i/$($views.Count)  $job ---"
  $sw = [Diagnostics.Stopwatch]::StartNew()

  & $Python "$Tools\texpass_iter.py" emit --state $StateDir --prep $Prep --glb $Glb `
      --yaw $v.y --el $v.e --thin-extent $ThinExtent 2>&1 |
      Select-String '\[emit\]|ANDON'

  & $Python "$Tools\texpass_brush.py" --job "$StateDir\$job" --seed $Seed --prompt $p 2>&1 |
      Select-String '\[brush\]|ANDON'

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
