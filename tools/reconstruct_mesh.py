"""RECONSTRUCT MESH - image to 3D through TRELLIS.2, at a CHOSEN seed.

WHY THIS FILE EXISTS. Every reconstruction recorded in this repo ran at seed 42 and
nobody chose it. `pipe.run` takes `seed: int = 42` and applies it with
`torch.manual_seed(seed)` immediately before conditioning and all three samplers
(`trellis2/pipelines/trellis2_image_to_3d.py:489,537`), but the recorded runner
`_mesh_character.py:43` calls `pipe.run(img, pipeline_type=args.ptype)` and never passes
it. The productized sibling `sprite-foundry/3d-prerender/mesh_character.py:87` makes the
same call. So the library has always been able to answer "what does another seed give"
and no runner on this rig could ask it.

E37 Stage A is six seeds on one plate. That is why this exists, and the enumeration above
is why it is a new file rather than a flag somebody forgot: this repo's most-fired law is
*enumerate the resource before commissioning one*, and enumeration here says commission.

WHAT IS DELIBERATELY UNCHANGED. The call path is the recorded one, value for value -
`from_pretrained("microsoft/TRELLIS.2-4B")` -> `.cuda()` -> `pipe.run(...)[0]` ->
`mesh.simplify(16777216)` -> `o_voxel.postprocess.to_glb(...)` -> `export(extension_webp=True)`.
The recorded defaults are passed EXPLICITLY, as E29's report did, so the pin sits in the
command line rather than in a default a future edit could move. The single addition is
`seed=`.

THE ANCHOR THAT MAKES THAT CLAIM CHECKABLE. E29 Ruling 5 measured three reconstructions of
one input at one seed BIT-IDENTICAL through `pipe.run()` - divergence begins only inside
`to_glb`'s decimation. So at `--seed 42` this runner must reproduce E29's recorded RAW
counts to the digit on E29's own inputs. `--anchor` runs exactly that comparison and
refuses on a mismatch. A runner that claims to be the recorded call path and cannot
reproduce the recorded call path's numbers is not the recorded call path.

WHY THE SEED GATE IS AN ANDON AND NOT A COMMENT. If a future TRELLIS drops or renames the
parameter, `pipe.run(**{"seed": N})` would raise - but a signature that quietly accepts and
ignores it would hand this arc six IDENTICAL meshes wearing six seed labels, and the whole
Stage-A sheet would be a comparison of one thing with itself. That is the failure mode this
tool is gated on, checked by introspection BEFORE the model loads. Ask what the operation
would look like if it went wrong, then check for that.

ASCII prints. Writes exactly two files per run: the GLB and its sidecar.
"""
import argparse
import hashlib
import json
import os
import sys
import time

# The recorded invocation, value for value (E29 report S3.1 / E33 premise table).
RECORDED = {
    "ptype": "1024_cascade",
    "decimation": 1000000,
    "texture": 4096,
    "remesh": 1,
    "remesh_project": 0,
}
# The library default that every reconstruction in this record silently ran at.
RECORDED_SEED = 42
RECORDED_ATTN = "sdpa"

# E29's inputs and the raw counts they produced, for --anchor. These are the numbers
# E29 Ruling 5 measured bit-identical across three runs through pipe.run().
ANCHORS = {
    "concept": {
        "image": r"E:\AI\facet_scratch\clay_arm\minotaur_concept.png",
        "sha256": "29fc8b87bf9d759541d418ad94d9004499115ced23f3134af754e3b0ab8962d2",
        "raw_vertices": 2081716, "raw_faces": 4229386,
    },
    "clay": {
        "image": r"E:\AI\facet_scratch\clay_arm\minotaur_clay.png",
        "sha256": "95f519351b31757c2bc6e1c0e67230c05ae92e865fbf569f14b86632e5ef885a",
        "raw_vertices": 2208416, "raw_faces": 4430096,
    },
}


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                return h.hexdigest()
            h.update(b)


def run_kwargs(args):
    """The kwargs handed to `pipe.run`.

    THIS FUNCTION IS THE WHOLE POINT OF THE TOOL, which is why it is a function rather
    than an inline dict: it is the one place that decides whether the seed reaches the
    sampler, and a test can call it with no GPU and no model. If `seed` ever stops
    appearing here, six candidates become one candidate measured six times.
    """
    return {"pipeline_type": args.ptype, "seed": args.seed}


def check_vram_headroom(free_bytes, total_bytes, min_free_gb):
    """ANDON: refuse to start a reconstruction that cannot fit.

    WHY THIS IS A GATE AND NOT A COMMENT. Twice in one session the rig's VRAM watchdog
    killed a job at ~31.6 GB of a 31.2 GB ceiling, and BOTH times the cause was a
    COLLISION rather than this run's own appetite: another GPU consumer was still resident
    (an Ollama model pinned `keep_alive: -1`; then ComfyUI still holding 26 GB after a
    plate edit). A watchdog kill arrives as a bare exit code with no output - it reads like
    a crash in this tool, and it cost a diagnosis both times.

    So the tool asks the one question that separates the two: is there room right now. A
    refusal here names the number and costs nothing; a kill costs the run, looks like a
    bug, and leaves a half-built tree. Reconstruction's own measured peak on this route is
    3.4 GB (E29), so the default floor is generous and still catches every collision seen.

    This does NOT raise the ceiling and does not free anything - freeing is the caller's
    policy, and CLAUDE.md measures that freeing buys no headroom anyway because ComfyUI
    stages to fill whatever it sees free. It only refuses to walk into a wall.
    """
    free_gb, total_gb = free_bytes / 1e9, total_bytes / 1e9
    if free_gb < min_free_gb:
        raise SystemExit(
            "ANDON: only %.1f GB of %.1f GB VRAM is free; this run wants at least %.1f GB.\n"
            "       Something else is holding the card. Free it and re-run - do NOT raise\n"
            "       the watchdog ceiling. Common holders on this rig: a resident ComfyUI\n"
            "       (it keeps models loaded after a job) and an Ollama model pinned with\n"
            "       keep_alive=-1." % (free_gb, total_gb, min_free_gb))
    print("[gate] VRAM %.1f GB free of %.1f GB (floor %.1f GB)"
          % (free_gb, total_gb, min_free_gb))
    return True


def check_seed_is_honoured(run_callable):
    """ANDON: the pipeline must actually take a `seed` parameter.

    A signature that lost it would make every Stage-A candidate identical while the
    filenames said otherwise. Raises - never asserts - because `python -O` and
    PYTHONOPTIMIZE=1 delete `assert` and this decides whether an expensive run proceeds
    (E21 Ruling 2 / E22 Ruling 9).
    """
    import inspect
    try:
        params = inspect.signature(run_callable).parameters
    except (TypeError, ValueError) as exc:            # pragma: no cover - defensive
        raise SystemExit("ANDON: cannot introspect pipe.run (%s) - refusing to run "
                         "blind, because an ignored seed yields identical candidates"
                         % exc)
    if "seed" not in params:
        raise SystemExit(
            "ANDON: pipe.run has no 'seed' parameter (found: %s). Every candidate this "
            "run produced would be the same mesh under different names."
            % ", ".join(sorted(params)))
    return True


def reconstruct(pipe, image, args):
    """The seam: hand the image and the seed to the pipeline and return the mesh.

    `pipe` is injected so a test can pass a spy and prove the seed traverses CLI ->
    run_kwargs -> pipe.run without loading a 4B model.
    """
    check_seed_is_honoured(pipe.run)
    return pipe.run(image, **run_kwargs(args))[0]


def sidecar(args, image_path, raw_v, raw_f, out_path, wall_s, peaks):
    """Everything needed to re-ask this exact question later. PIN_PER_STEP: a candidate
    with no recorded parameters is not a candidate, it is a file."""
    return {
        "tool": os.path.basename(__file__),
        "tool_sha256": sha256(os.path.abspath(__file__)),
        "image": image_path.replace(os.sep, "/"),
        "image_sha256": sha256(image_path),
        "seed": args.seed,
        "params": {k: getattr(args, k) for k in RECORDED},
        "recorded_defaults_unchanged": {k: getattr(args, k) == v
                                        for k, v in RECORDED.items()},
        "env": {"ATTN_BACKEND": os.environ.get("ATTN_BACKEND"),
                "SPARSE_ATTN_BACKEND": os.environ.get("SPARSE_ATTN_BACKEND"),
                "HF_HOME": os.environ.get("HF_HOME"),
                "python": sys.version.split()[0]},
        "raw_vertices": raw_v, "raw_faces": raw_f,
        "out": out_path.replace(os.sep, "/"),
        "out_bytes": os.path.getsize(out_path),
        "out_sha256": sha256(out_path),
        "wall_seconds": round(wall_s, 1),
        "peak_gb": peaks,
    }


def build_argparser():
    ap = argparse.ArgumentParser(
        description="image -> 3D through TRELLIS.2 at a chosen seed; the recorded call "
                    "path with `seed=` added")
    ap.add_argument("--image", help="required unless --anchor supplies one")
    ap.add_argument("--out", required=True, help="output .glb; a sidecar .json lands beside it")
    ap.add_argument("--seed", type=int, default=RECORDED_SEED,
                    help="passed to pipe.run; %d is the library default every recorded "
                         "reconstruction in this repo ran at" % RECORDED_SEED)
    ap.add_argument("--ptype", default=RECORDED["ptype"])
    ap.add_argument("--decimation", type=int, default=RECORDED["decimation"])
    ap.add_argument("--texture", type=int, default=RECORDED["texture"])
    ap.add_argument("--remesh", type=int, default=RECORDED["remesh"])
    ap.add_argument("--remesh-project", dest="remesh_project", type=int,
                    default=RECORDED["remesh_project"])
    ap.add_argument("--trellis-repo", default=r"E:\AI-Models\TRELLIS.2-repo",
                    help="prepended to sys.path so the recipe is in the command, not in "
                         "an env var the caller has to remember")
    ap.add_argument("--hf-home", default=r"E:\AI-Models\hf-cache")
    ap.add_argument("--anchor", choices=sorted(ANCHORS),
                    help="reproduce E29's recorded RAW counts for this input and refuse "
                         "on a mismatch; implies --image and --seed %d" % RECORDED_SEED)
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing --out (refused by default)")
    ap.add_argument("--min-free-gb", type=float, default=8.0,
                    help="refuse to start below this much free VRAM; the measured peak on "
                         "this route is 3.4 GB, so this floor catches a COLLISION with "
                         "another GPU consumer rather than bounding this run")
    return ap


def resolve_input(args):
    """Decide which image this run reads, and REFUSE rather than pick.

    THIS FUNCTION EXISTS BECAUSE ITS FIRST VERSION WAS WRONG AND T71 CAUGHT IT. `--anchor`
    used to overwrite `args.image`, so `--anchor clay --image <anything-else>` silently
    read the recorded file and reported a passing anchor about an input the caller never
    named. A run that quietly measures a different object than the one on its command
    line is this repo's own recurring defect - *a number that reproduces exactly can
    still be measured against the wrong object* - and the fix is to refuse the ambiguity,
    not to resolve it.
    """
    if args.anchor and args.image:
        raise SystemExit(
            "ANDON: --anchor and --image are mutually exclusive. --anchor %s supplies "
            "its own recorded input (%s); passing both asks this run to measure one "
            "image and report about another."
            % (args.anchor, ANCHORS[args.anchor]["image"]))
    if args.anchor:
        return ANCHORS[args.anchor]["image"], RECORDED_SEED
    if not args.image:
        raise SystemExit("ANDON: one of --image or --anchor is required")
    return args.image, args.seed


def check_anchor_input(anchor, image_path):
    """ANDON: the anchor's input must still be the file whose numbers are recorded.

    Separated from main() so it is testable against a decoy with no model, no GPU and no
    subprocess - the leg that used to need one ran a 4B reconstruction to make its point.
    """
    if not os.path.isfile(image_path):
        raise SystemExit("ANDON: anchor input missing - %s" % image_path)
    got = sha256(image_path)
    want = ANCHORS[anchor]["sha256"]
    if got != want:
        raise SystemExit("ANDON: anchor input moved - %s\n       recorded %s\n"
                         "       actual   %s" % (image_path, want, got))
    return True


def main(argv=None):
    args = build_argparser().parse_args(argv)
    args.image, args.seed = resolve_input(args)

    if not os.path.isfile(args.image):
        raise SystemExit("ANDON: --image does not exist: %s" % args.image)
    if os.path.exists(args.out) and not args.force:
        raise SystemExit("ANDON: --out already exists and --force was not given: %s\n"
                         "       a silently overwritten candidate is an unrecoverable "
                         "one; this arc's candidates are the record." % args.out)
    if args.anchor:
        check_anchor_input(args.anchor, args.image)

    # Scripts must create their own output directories - two runs in this repo died here.
    outdir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(outdir, exist_ok=True)

    # HEAVY IMPORTS LIVE HERE, NOT AT MODULE LEVEL. `restylize_views` imports cv2 at
    # module level and CI's pinned install never had it, so no test could reach any of
    # twelve tools until the first one tried (E23's fired CI gate). Everything above this
    # line is importable with no torch, no trellis2, no GPU - which is what lets T71 test
    # the seam.
    os.environ.setdefault("OPENCV_IO_ENABLE_OPENEXR", "1")
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
    os.environ.setdefault("ATTN_BACKEND", RECORDED_ATTN)
    os.environ.setdefault("HF_HOME", args.hf_home)
    if args.trellis_repo not in sys.path:
        sys.path.insert(0, args.trellis_repo)

    import torch
    from PIL import Image
    from trellis2.pipelines import Trellis2ImageTo3DPipeline
    import o_voxel

    t0 = time.time()
    print("=== reconstruct: image=%s seed=%d ptype=%s remesh=%s decim=%d ==="
          % (args.image, args.seed, args.ptype, bool(args.remesh), args.decimation),
          flush=True)

    # Before the 4B model loads, and before anything expensive: is there room.
    check_vram_headroom(*torch.cuda.mem_get_info(), min_free_gb=args.min_free_gb)

    # The gate runs on the CLASS before the 4B model loads: fail fast and free.
    check_seed_is_honoured(Trellis2ImageTo3DPipeline.run)
    print("[gate] pipe.run accepts seed - candidates can differ", flush=True)

    pipe = Trellis2ImageTo3DPipeline.from_pretrained("microsoft/TRELLIS.2-4B")
    pipe.cuda()
    print("[load] %ds | VRAM %.1f GB" % (time.time() - t0,
                                         torch.cuda.memory_allocated() / 1e9), flush=True)

    img = Image.open(args.image)
    torch.cuda.reset_peak_memory_stats()
    t1 = time.time()
    mesh = reconstruct(pipe, img, args)
    torch.cuda.synchronize()
    gen_peak = torch.cuda.max_memory_allocated() / 1e9
    raw_v, raw_f = len(mesh.vertices), len(mesh.faces)
    print("[mesh] %ds | GEN PEAK %.1f GB | verts %d faces %d"
          % (time.time() - t1, gen_peak, raw_v, raw_f), flush=True)

    if args.anchor:
        a = ANCHORS[args.anchor]
        ok = (raw_v == a["raw_vertices"] and raw_f == a["raw_faces"])
        print("[anchor] recorded %d v / %d f   measured %d v / %d f   %s"
              % (a["raw_vertices"], a["raw_faces"], raw_v, raw_f,
                 "IDENTICAL" if ok else "DIFFER"), flush=True)
        if not ok:
            raise SystemExit(
                "ANDON: the anchor did not reproduce. E29 Ruling 5 measured pipe.run "
                "bit-identical across three runs of this input at this seed, so a "
                "difference here means this runner's call path is NOT the recorded one. "
                "Halt and report; do not adjust a parameter and re-run.")

    mesh.simplify(16777216)
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    t2 = time.time()
    glb = o_voxel.postprocess.to_glb(
        vertices=mesh.vertices, faces=mesh.faces, attr_volume=mesh.attrs,
        coords=mesh.coords, attr_layout=mesh.layout, voxel_size=mesh.voxel_size,
        aabb=[[-0.5, -0.5, -0.5], [0.5, 0.5, 0.5]],
        decimation_target=args.decimation, texture_size=args.texture,
        remesh=bool(args.remesh), remesh_band=1, remesh_project=args.remesh_project,
        verbose=True)
    glb_peak = torch.cuda.max_memory_allocated() / 1e9
    glb.export(args.out, extension_webp=True)
    print("[GLB] %s (%.1f MB) | to_glb %ds | OVERALL PEAK %.1f GB | TOTAL %ds"
          % (args.out, os.path.getsize(args.out) / 1e6, time.time() - t2,
             max(gen_peak, glb_peak), time.time() - t0), flush=True)

    side = os.path.splitext(args.out)[0] + ".json"
    payload = sidecar(args, args.image, raw_v, raw_f, args.out, time.time() - t0,
                      {"gen": round(gen_peak, 1), "to_glb": round(glb_peak, 1)})
    with open(side, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1)
    print("[sidecar] %s" % side, flush=True)
    print("=== MESH RUN COMPLETE ===", flush=True)


if __name__ == "__main__":
    main()
