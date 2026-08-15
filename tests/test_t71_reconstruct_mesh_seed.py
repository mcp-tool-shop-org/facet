"""T71 - `tools/reconstruct_mesh.py`: the seed reaches the sampler, and the gates raise.

WHY THIS FILE EXISTS. E37 Stage A varies one thing - the reconstruction seed - and no
runner on this rig could vary it. `pipe.run` has taken `seed: int = 42` all along
(`trellis2_image_to_3d.py:489`, applied at :537 as `torch.manual_seed(seed)`) and both
runners drop it on the floor: `_mesh_character.py:43` and
`sprite-foundry/3d-prerender/mesh_character.py:87` both call
`pipe.run(img, pipeline_type=...)`. The new tool adds exactly that argument.

WHAT WOULD THIS LOOK LIKE IF THE CODE WERE WRONG IN THE SPECIFIC WAY THESE CHECKS EXIST
TO CATCH? That is the question this repo requires of a fixture, and here it has a sharp
answer: if the seed silently fails to reach the sampler, six Stage-A candidates are ONE
mesh under six filenames, every downstream number is a comparison of a thing with itself,
and NOTHING ELSE IN THE ARC WOULD NOTICE - the files differ in name, the run takes the
same time, the sidecars record six different integers. So leg 3 does not check that the
seed is in a dict; it hands the tool a SPY PIPELINE and reads back what the tool actually
called, and leg 4 proves that check can fail by running the pre-tool call shape
(`pipe.run(img, pipeline_type=...)`) through the same assertion and watching it catch it.

THE TOOL IS IMPORTED, unlike the twelve in T31. That is deliberate and it is what the
tool's structure buys: every heavy import (torch, trellis2, o_voxel) lives inside main(),
so the module is importable with none of them present - the E23 lesson (a module-level
`cv2` made twelve tools untestable until CI's first invocation found it) turned into a
property a test can hold the tool to. Leg 1 is that property.

Everything printed here is ASCII (the repo's law).
"""
import ast
import io
import os
import py_compile
import subprocess
import sys

import pytest

from conftest import REPO, tool

sys.path.insert(0, str(REPO / "tools"))
import reconstruct_mesh as RM          # noqa: E402

REL = "reconstruct_mesh.py"
SRC = io.open(tool(REL), encoding="utf-8").read()

MODES = [("normal", [], {}),
         ("dash-O", ["-O"], {}),
         ("PYTHONOPTIMIZE", [], {"PYTHONOPTIMIZE": "1"})]
MODE_IDS = [m[0] for m in MODES]


# THE TIMEOUT IS A GATE, NOT A CONVENIENCE, and it is here because this file failed that
# way once. Every subprocess leg below is a fast refusal or a `--help`; NONE may
# reach the model. The first version of the decoy leg did - `--anchor` overrode its
# `--image`, the hash matched the recorded file, and three legs each ran a full 4B
# reconstruction (~105 s, 36 MB of GLB) while still reporting only "rc was 0". Loading
# TRELLIS alone exceeds this budget, so a leg that ever reaches the model fails LOUDLY
# here instead of quietly spending a GPU. Put the andon on the direction the invariant
# does not bound.
NO_MODEL_SECONDS = 60


def run(flags, args, cwd, env_extra=None, script=None, timeout=NO_MODEL_SECONDS):
    """One command, one process, interpreter FLAGS as well as env, in a scratch cwd."""
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)          # the ambient value must not leak in
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable] + list(flags) + [script or tool(REL)]
                       + [str(a) for a in args],
                       cwd=str(cwd), env=env, capture_output=True, timeout=timeout)
    return (p.returncode,
            p.stdout.decode("utf-8", "replace"),
            p.stderr.decode("utf-8", "replace"))


# ---------------------------------------------------------------------------
# 1. it compiles, and it imports with NO torch / trellis2 / o_voxel present
# ---------------------------------------------------------------------------

def test_t71_compiles(tmp_path):
    py_compile.compile(tool(REL), cfile=str(tmp_path / "x.pyc"), doraise=True)


def test_t71_module_level_is_free_of_the_heavy_imports():
    """E23's fired CI gate, as a property instead of a memory.

    `restylize_views` imports cv2 at module level, CI's pinned install never had it, and
    no test could invoke ANY of twelve tools until the first one tried. This tool's
    heavy imports are inside main(); the AST is what holds it there, because a future
    edit that hoists one to the top would re-create that gap silently.
    """
    heavy = {"torch", "trellis2", "o_voxel", "PIL", "cv2", "numpy", "scipy", "trimesh",
             "open3d"}
    tree = ast.parse(SRC)
    top = []
    for node in tree.body:                                   # module level ONLY
        if isinstance(node, ast.Import):
            top += [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            top.append(node.module.split(".")[0])
    offenders = sorted(heavy.intersection(top))
    assert offenders == [], (
        "%s imports %s at MODULE level. Move it inside main(): a module that cannot be "
        "imported without a GPU stack cannot be tested, which is exactly how twelve "
        "route tools went untested until CI's first invocation (E23)." % (REL, offenders))


def test_t71_importing_the_module_runs_nothing(tmp_path):
    """Eleven of T31's twelve execute at import. This one must not: importing it is how
    the legs below reach `run_kwargs` and `check_seed_is_honoured`."""
    probe = tmp_path / "probe.py"
    probe.write_text(
        "import sys; sys.path.insert(0, r'%s')\n"
        "import reconstruct_mesh\n"
        "print('IMPORTED_CLEAN')\n" % str(REPO / "tools"), encoding="utf-8")
    rc, out, err = run([], [], tmp_path, script=str(probe))
    assert rc == 0 and "IMPORTED_CLEAN" in out, (
        "importing the module failed or did work:\n%s\n%s" % (out[-2000:], err[-2000:]))
    assert sorted(p.name for p in tmp_path.iterdir()) == ["probe.py"], (
        "importing the module wrote %s into the scratch cwd"
        % sorted(p.name for p in tmp_path.iterdir()))


# ---------------------------------------------------------------------------
# 2. --help reaches argparse and writes nothing, in every mode
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
def test_t71_help_is_clean_in_every_mode(mode, flags, envx, tmp_path):
    rc, out, err = run(flags, ["--help"], tmp_path, env_extra=envx)
    assert rc == 0, "--help exited %d under %s:\n%s" % (rc, mode, err[-2000:])
    assert "--seed" in out, "--help under %s does not offer --seed:\n%s" % (mode, out)
    assert not list(tmp_path.iterdir()), (
        "--help wrote %s into the scratch cwd under %s"
        % (sorted(p.name for p in tmp_path.iterdir()), mode))


# ---------------------------------------------------------------------------
# 3. THE SEAM - the seed the CLI was given is the seed the pipeline is called with
# ---------------------------------------------------------------------------

class SpyPipe(object):
    """A pipeline that records its call instead of doing 105 seconds of work.

    Its `run` carries the REAL signature - `seed` present with the library's default -
    so `check_seed_is_honoured` sees what it would see on the genuine class.
    """

    def __init__(self):
        self.calls = []

    def run(self, image, num_samples=1, seed=42, pipeline_type=None, **kw):
        self.calls.append({"image": image, "seed": seed,
                           "pipeline_type": pipeline_type})
        return ["MESH"]


def _args(*extra):
    return RM.build_argparser().parse_args(
        ["--image", "in.png", "--out", "out.glb"] + list(extra))


@pytest.mark.parametrize("seed", [0, 1, 42, 770700, 987654, 2 ** 31 - 1])
def test_t71_the_seed_reaches_the_pipeline(seed):
    """Not 'is seed in a dict' - what did the tool ACTUALLY call the pipeline with."""
    spy = SpyPipe()
    got = RM.reconstruct(spy, "IMG", _args("--seed", str(seed)))
    assert got == "MESH"
    assert len(spy.calls) == 1
    assert spy.calls[0]["seed"] == seed, (
        "CLI --seed %d reached the pipeline as %r. Six Stage-A candidates would be one "
        "mesh under six names." % (seed, spy.calls[0]["seed"]))
    assert spy.calls[0]["pipeline_type"] == RM.RECORDED["ptype"]


def test_t71_the_seam_check_can_fail():
    """THE DISCRIMINATING CASE. A fixture that passes under the implementation being
    REPLACED does not test the change - so here is the pre-tool call shape, the one
    both recorded runners use, run through the SAME assertion the leg above makes.

    If this does not raise, the leg above is decoration.
    """
    spy = SpyPipe()
    args = _args("--seed", "770700")
    spy.run("IMG", pipeline_type=args.ptype)          # `_mesh_character.py:43`, verbatim
    assert spy.calls[0]["seed"] == RM.RECORDED_SEED, "the fixture itself is wrong"
    with pytest.raises(AssertionError):
        assert spy.calls[0]["seed"] == 770700, "the seed did not reach the pipeline"


def test_t71_run_kwargs_carries_the_seed_and_nothing_surprising():
    kw = RM.run_kwargs(_args("--seed", "123"))
    assert kw == {"pipeline_type": RM.RECORDED["ptype"], "seed": 123}


# ---------------------------------------------------------------------------
# 4. the seed ANDON - it fires when the pipeline cannot honour a seed
# ---------------------------------------------------------------------------

def test_t71_seed_andon_fires_on_a_signature_without_seed():
    def no_seed(image, pipeline_type=None):           # a future TRELLIS that dropped it
        return ["MESH"]
    with pytest.raises(SystemExit) as e:
        RM.check_seed_is_honoured(no_seed)
    assert "ANDON" in str(e.value) and "seed" in str(e.value)


def test_t71_seed_andon_is_silent_when_the_seed_is_honoured():
    assert RM.check_seed_is_honoured(SpyPipe().run) is True


@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
def test_t71_seed_andon_survives_the_optimizers(mode, flags, envx, tmp_path):
    """`assert` is deletable by -O and PYTHONOPTIMIZE=1; this gate decides whether an
    expensive run proceeds, so it must fire in all three modes (E21 Ruling 2 / E22
    Ruling 9). T30 pins the stripping mechanism itself, which is what stops these legs
    passing vacuously."""
    probe = tmp_path / "probe.py"
    probe.write_text(
        "import sys; sys.path.insert(0, r'%s')\n"
        "import reconstruct_mesh as RM\n"
        "def no_seed(image, pipeline_type=None): pass\n"
        "try:\n"
        "    RM.check_seed_is_honoured(no_seed)\n"
        "    print('GATE_SILENT')\n"
        "except SystemExit as e:\n"
        "    print('GATE_FIRED', 'ANDON' in str(e))\n" % str(REPO / "tools"),
        encoding="utf-8")
    rc, out, err = run(flags, [], tmp_path, env_extra=envx, script=str(probe))
    assert "GATE_FIRED True" in out, (
        "the seed gate did not fire under %s:\n%s\n%s" % (mode, out, err[-1500:]))
    assert "GATE_SILENT" not in out


# ---------------------------------------------------------------------------
# 5. the pre-flight ANDONs refuse in every mode, and leave nothing behind
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
def test_t71_missing_image_refuses_in_every_mode(mode, flags, envx, tmp_path):
    rc, out, err = run(flags, ["--image", str(tmp_path / "nope.png"),
                               "--out", str(tmp_path / "o" / "x.glb")],
                       tmp_path, env_extra=envx)
    assert rc != 0, "a missing --image did not refuse under %s" % mode
    assert "ANDON" in (out + err), "refused without an ANDON under %s:\n%s" % (mode, err)
    assert not list(tmp_path.iterdir()), (
        "the refused run left %s behind under %s"
        % (sorted(p.name for p in tmp_path.iterdir()), mode))


@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
def test_t71_existing_output_refuses_and_does_not_overwrite(mode, flags, envx, tmp_path):
    """A silently overwritten candidate is unrecoverable, and this arc's candidates ARE
    the record. Prefer eliminating the risk to detecting it afterwards."""
    img = tmp_path / "in.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"not really a png")
    out = tmp_path / "cand.glb"
    out.write_bytes(b"THE EARLIER CANDIDATE")
    rc, o, err = run(flags, ["--image", str(img), "--out", str(out)],
                     tmp_path, env_extra=envx)
    assert rc != 0, "an existing --out did not refuse under %s" % mode
    assert "ANDON" in (o + err)
    assert out.read_bytes() == b"THE EARLIER CANDIDATE", (
        "the refused run overwrote the existing candidate under %s" % mode)


@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
def test_t71_anchor_and_image_together_refuse_in_every_mode(mode, flags, envx, tmp_path):
    """THE REGRESSION LEG, and the defect it pins was found by this file, not reasoned
    about. `--anchor` used to overwrite `--image`, so this exact command line read the
    RECORDED file, reconstructed it, and reported a passing anchor about an input the
    caller never named - three times, once per mode, ~105 s each. The tool now refuses
    the ambiguity instead of resolving it silently.
    """
    decoy = tmp_path / "minotaur_clay.png"
    decoy.write_bytes(b"NOT THE RECORDED INPUT")
    rc, o, err = run(flags, ["--anchor", "clay", "--image", str(decoy),
                             "--out", str(tmp_path / "o" / "a.glb")],
                     tmp_path, env_extra=envx)
    assert rc != 0, "--anchor with a conflicting --image was accepted under %s" % mode
    blob = o + err
    assert "ANDON" in blob and "mutually exclusive" in blob, (
        "refused without naming the conflict under %s:\n%s" % (mode, err[-1500:]))
    assert not (tmp_path / "o").exists(), (
        "the refused run created an output directory under %s" % mode)


def test_t71_anchor_refuses_a_moved_input():
    """`--anchor` is only evidence if the thing it anchors against is still the recorded
    file - *a number that reproduces exactly can still be measured against the wrong
    object*. Tested against the FUNCTION, so proving it costs no GPU."""
    with pytest.raises(SystemExit) as e:
        RM.check_anchor_input("clay", str(REPO / "README.md"))
    assert "ANDON" in str(e.value) and "moved" in str(e.value)


def test_t71_anchor_accepts_the_recorded_input_when_it_is_present():
    """The other side of the leg above: if this returned True on ANY path, the leg above
    would be passing for the wrong reason."""
    p = RM.ANCHORS["clay"]["image"]
    if not os.path.isfile(p):
        pytest.skip("anchor input absent on this rig: %s" % p)
    assert RM.check_anchor_input("clay", p) is True


def test_t71_neither_image_nor_anchor_refuses():
    with pytest.raises(SystemExit) as e:
        RM.resolve_input(RM.build_argparser().parse_args(["--out", "x.glb"]))
    assert "ANDON" in str(e.value)


def test_t71_anchor_alone_resolves_to_its_recorded_input_at_seed_42():
    img, seed = RM.resolve_input(
        RM.build_argparser().parse_args(["--anchor", "clay", "--out", "x.glb"]))
    assert img == RM.ANCHORS["clay"]["image"]
    assert seed == RM.RECORDED_SEED


# ---------------------------------------------------------------------------
# 5b. the VRAM headroom gate - it refuses a COLLISION, and it can be silent
# ---------------------------------------------------------------------------
# Added after the rig's watchdog killed two jobs in one session at ~31.6 GB of a 31.2 GB
# ceiling. Both were collisions with another resident GPU consumer, and both arrived as a
# bare exit code with no output - indistinguishable from a crash in this tool. The gate
# converts that into a refusal that names the number.

GB = 1e9


def test_t71_vram_gate_refuses_when_the_card_is_occupied():
    """The measured case: 31.2 GB card, ~5 GB free because something else holds it."""
    with pytest.raises(SystemExit) as e:
        RM.check_vram_headroom(5.0 * GB, 32.6 * GB, min_free_gb=8.0)
    msg = str(e.value)
    assert "ANDON" in msg
    assert "5.0" in msg and "8.0" in msg, "the refusal must name the numbers: %s" % msg
    assert "ceiling" in msg, "the refusal must say not to raise the ceiling"


def test_t71_vram_gate_is_silent_with_room():
    assert RM.check_vram_headroom(30.9 * GB, 32.6 * GB, min_free_gb=8.0) is True


def test_t71_vram_gate_can_fail_at_its_own_boundary():
    """Both sides of the floor, so the threshold is a threshold and not a formality."""
    assert RM.check_vram_headroom(8.01 * GB, 32.6 * GB, min_free_gb=8.0) is True
    with pytest.raises(SystemExit):
        RM.check_vram_headroom(7.99 * GB, 32.6 * GB, min_free_gb=8.0)


@pytest.mark.parametrize("mode,flags,envx", MODES, ids=MODE_IDS)
def test_t71_vram_gate_survives_the_optimizers(mode, flags, envx, tmp_path):
    """It decides whether an expensive run proceeds, so `-O` must not delete it."""
    probe = tmp_path / "probe.py"
    probe.write_text(
        "import sys; sys.path.insert(0, r'%s')\n"
        "import reconstruct_mesh as RM\n"
        "try:\n"
        "    RM.check_vram_headroom(1e9, 32.6e9, min_free_gb=8.0)\n"
        "    print('GATE_SILENT')\n"
        "except SystemExit as e:\n"
        "    print('GATE_FIRED', 'ANDON' in str(e))\n" % str(REPO / "tools"),
        encoding="utf-8")
    rc, out, err = run(flags, [], tmp_path, env_extra=envx, script=str(probe))
    assert "GATE_FIRED True" in out, (
        "the VRAM gate did not fire under %s:\n%s\n%s" % (mode, out, err[-1500:]))
    assert "GATE_SILENT" not in out


def test_t71_the_vram_floor_is_above_the_measured_peak():
    """E29 measured this route's reconstruction peak at 3.4 GB. The floor is deliberately
    well above it, because the gate exists to catch a COLLISION with another consumer -
    not to bound this run's own appetite. If someone lowers it to ~3.4 they have quietly
    changed what the gate is for."""
    a = _args()
    assert a.min_free_gb >= 8.0, (
        "the default floor is %.1f GB; below 8 it stops catching the collisions that "
        "actually killed jobs on this rig" % a.min_free_gb)


# ---------------------------------------------------------------------------
# 6. no ANDON here is a bare `assert` - by AST, with a leg that can catch one
# ---------------------------------------------------------------------------

def _andon_asserts(src):
    """E22's definition, reused verbatim so the arcs count the same population."""
    return [n for n in ast.walk(ast.parse(src))
            if isinstance(n, ast.Assert) and n.msg is not None
            and "ANDON" in (ast.get_source_segment(src, n.msg) or "")]


def test_t71_no_andon_is_a_bare_assert():
    found = _andon_asserts(SRC)
    assert found == [], (
        "%s carries %d ANDON(s) as bare asserts, at line(s) %s. `python -O` deletes "
        "them and the run proceeds past the gate in silence."
        % (REL, len(found), [n.lineno for n in found]))


def test_t71_the_bare_assert_detector_can_fail():
    """Planted defect, exactly the shape leg 6 exists to catch. Without this, a detector
    that matched nothing would look identical to a clean file."""
    planted = SRC + '\n\ndef _planted():\n    assert False, "ANDON: planted"\n'
    found = _andon_asserts(planted)
    assert len(found) == 1, "the detector missed a planted ANDON assert"


def test_t71_every_andon_in_this_tool_raises_systemexit():
    """The converted form. SystemExit is not deletable by -O."""
    raises = [n for n in ast.walk(ast.parse(SRC))
              if isinstance(n, ast.Raise) and isinstance(n.exc, ast.Call)
              and getattr(n.exc.func, "id", None) == "SystemExit" and n.exc.args
              and "ANDON" in (ast.get_source_segment(SRC, n.exc.args[0]) or "")]
    assert len(raises) >= 5, (
        "expected the tool's ANDONs to be SystemExit raises; found %d" % len(raises))


# ---------------------------------------------------------------------------
# 7. the recorded invocation is PINNED - moving it must be deliberate
# ---------------------------------------------------------------------------

def test_t71_the_recorded_defaults_are_the_recorded_ones():
    """E29's report S3.1 records the invocation value for value. This tool claims to be
    that call path plus a seed; if a default moves, the claim quietly stops being true
    and every candidate becomes incomparable with every recorded mesh."""
    assert RM.RECORDED == {"ptype": "1024_cascade", "decimation": 1000000,
                           "texture": 4096, "remesh": 1, "remesh_project": 0}
    assert RM.RECORDED_SEED == 42, (
        "42 is the library default that every reconstruction in this record ran at; it "
        "is the anchor's seed and is not a preference")
    assert RM.RECORDED_ATTN == "sdpa", "E29 S2.2: ATTN_BACKEND=sdpa alone reconstructs"


def test_t71_the_cli_defaults_match_the_recorded_block():
    a = _args()
    for k, v in RM.RECORDED.items():
        assert getattr(a, k) == v, "CLI default for %s is %r, recorded is %r" % (
            k, getattr(a, k), v)
    assert a.seed == RM.RECORDED_SEED


def test_t71_the_anchor_targets_are_e29s_recorded_numbers():
    """E29 report S3.1's raw counts and E29-predictions' input hashes, pinned here so a
    later edit to either has to be deliberate."""
    assert RM.ANCHORS["concept"]["raw_vertices"] == 2081716
    assert RM.ANCHORS["concept"]["raw_faces"] == 4229386
    assert RM.ANCHORS["clay"]["raw_vertices"] == 2208416
    assert RM.ANCHORS["clay"]["raw_faces"] == 4430096
    assert RM.ANCHORS["concept"]["sha256"] == (
        "29fc8b87bf9d759541d418ad94d9004499115ced23f3134af754e3b0ab8962d2")
    assert RM.ANCHORS["clay"]["sha256"] == (
        "95f519351b31757c2bc6e1c0e67230c05ae92e865fbf569f14b86632e5ef885a")
