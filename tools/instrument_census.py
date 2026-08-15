"""E28 - the census of `tools/diagnostics/`, measured rather than curated.

WHY THIS FILE EXISTS. `docs/specs/measurement-mcp-spec.md` open question 1 asked
which instruments enter the measurement surface first, and estimated the
directory at "~80 files" from docstrings and the record. Measured, it holds 99 -
*the spec estimated its own denominator*, which is this repo's oldest defect. The
Director ruled: commission the census first, and set the boundary against it
rather than against a curation.

SO THIS FILE DECIDES NOTHING. It measures, and axis G *proposes*. The boundary is
the advisor's to rule and the Director's to adjust.

THE INSTRUMENT IS THE DELIVERABLE AS MUCH AS ITS OUTPUT IS. A hand-read is what
produced "~80"; a committed re-runnable script is what lets the next arc DIFF
rather than re-read. Its file count is under a test (T41), the E23 Ruling 9
pattern: moving it requires editing that test, on purpose, in the commit that
moves it.

AXES A-F ARE MECHANICAL - the script measures them and a human does not
adjudicate them. AXIS G IS A JUDGMENT and is labelled as one everywhere it
appears. `no opinion` is a real value in it and is used; a table of confident
`none`s would read as a measurement while being nothing of the kind.

WHERE A PROPERTY IS NOT DEFINED FOR A MEMBER THE VALUE IS `n/a` WITH A REASON,
NEVER A SILENT `false`. E27 Ruling 5: a prediction about members of a real
population still fails if it assumes a property none of them was checked for.
Axis F is where that bites - a module with no CLI has no `--help` to exit 0, and
a module whose import needs `bpy` tells you about the environment rather than
about the module.

    AND AXIS F ONLY PROBES INVOCABLE FILES, WHICH IS A SAFETY PROPERTY AS WELL AS
    A DEFINITIONAL ONE. `python <file> --help` runs the module body BEFORE
    argparse ever sees `--help`, so probing a file that calls its own `main()` at
    module level would EXECUTE it - against whatever subject its constants name.
    The recorded trees are not in git and there is no revert for them. A file
    with no `if __name__ == "__main__"` guard is therefore never run by this
    census; it is `n/a (no CLI)`, which is what it would be anyway.

USAGE
    python tools/instrument_census.py --committed        # the committed pair:
                                                         # diagnostics + verify
    python tools/instrument_census.py                    # diagnostics only
    python tools/instrument_census.py --dir tools/verify # any one home
    python tools/instrument_census.py --skip-probe       # axes A-E and G only
    python tools/instrument_census.py --json-only
"""
import argparse
import ast
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
DIAG_REL = "tools/diagnostics"
DIAG = os.path.join(REPO, "tools", "diagnostics")

# THE COMMITTED OUTPUTS COVER BOTH HOMES (E28 Amendment 1 / Ruling 5): the
# boundary is the backing map and the map spans `tools/diagnostics` and
# `tools/verify` by construction, so a census over one home measures a
# different population than the one the boundary is ruled against. `--dir` on
# the command line censuses any one directory (diagnostics stays the default,
# per the amendment); the COMMITTED artifact is emitted with `--committed`,
# which is this tuple, and T41 pins that the committed JSON covers exactly
# these homes so a partial re-emit cannot land silently.
COMMITTED_DIRS = ("tools/diagnostics", "tools/verify")

if HERE not in sys.path:
    sys.path.insert(0, HERE)

# ---------------------------------------------------------------------------
# axis B - the recorded-tree markers, from the E28 dispatch, verbatim
# ---------------------------------------------------------------------------
SUBJECT_MARKERS = ("E:\\", "E:/", "facet_next", "facet_E0", "training",
                   "saltroad", "ARMB")

# ---------------------------------------------------------------------------
# axis G - THE JUDGMENT. A PROPOSAL, NOT A DECISION.
# ---------------------------------------------------------------------------
# The spec's eight job-shaped tool questions. A file is mapped to one when it
# answers that question for an arbitrary subject or could plainly be pointed at
# one; `none` when it answers a question the spec does not list; `ambiguous`
# when it straddles; `no opinion` when the docstring and the filename do not
# settle it and reading the body would be inventing an answer.
SPEC_TOOLS = ("mesh_stats", "mesh_topology", "reach_ceiling",
              "thin_extent_curve", "offsurface_rate", "texel_provenance",
              "anchor_check", "measure_report")
G_VALUES = SPEC_TOOLS + ("none", "ambiguous", "no opinion")

# EVERY file in a censused directory must appear in exactly one list below. A
# missing one is an ANDON rather than a silent `none`, so a file added later
# forces a deliberate judgment instead of inheriting a default - which is why
# `none` is spelled out 58 times rather than left as the fall-through.
#
# THE RULE APPLIED, stated so a re-judging session can disagree with it
# deliberately rather than by accident. Judged from docstring line 1 (axis C)
# and the filename, NOT from the body:
#   - a spec tool  : line 1 names that tool's question in substance
#   - `none`       : line 1 names a question the spec does not list
#   - `ambiguous`  : it straddles two of the eight, or answers one partially
#                    (an offsurface CONSUMER sweep is not the offsurface RATE)
#   - `no opinion` : line 1 does not say what the file measures, and reading
#                    the body to find out would be inventing an answer
#
# AT TASK 1 two of the eight attracted nothing from diagnostics, and both were
# findings: `mesh_stats` lives at `tools/verify/mesh_stats.py`, outside that
# directory entirely; `anchor_check` has no implementation anywhere - E27
# Ruling 4 established that the file NAMED `e13_anchor_check.py` is the
# spiral-law painted-adjacency guard, a different question, so it is judged
# `none` here on its own docstring's evidence.
#
# AT TASK 2-PRE the census extended to `tools/verify/` (Amendment 1 / Ruling 5)
# and its 8 files were judged under the same rule - docstring line 1 plus
# filename, not the body - with task 1's own precedent applied deliberately:
# comparison-sheet builders map to `measure_report` (nine diagnostics files
# already do), so `gate0_sheet` / `gate1_sheet` / `head_crop` go there;
# `mesh_stats` states the spec's sentence as its own line 1; `montage` is a
# sheet PLUS a per-view brightness readout no spec tool covers - `ambiguous`;
# `gate_mesh` is a VERDICT tool ("may the pipeline spend money... Exit 0 =
# yes"), and the spec's surface never says whether output is good - `none`;
# the two render stages are `none`. `anchor_check` still attracts nothing
# from either home.
_G = {
    "reach_ceiling": [
        "brush_reach.py", "e04_ship_cameras.py", "e04_stroke_cameras.py",
        "e08_ceiling.py", "e12_elevated.py", "e13_stroke_cameras.py",
    ],
    "mesh_topology": [
        "e12_nonmanifold.py", "e14_topology.py",
    ],
    "offsurface_rate": [
        "e10_offsurface.py", "e12_offsurface.py",
    ],
    "thin_extent_curve": [
        "e12_thin_curve.py",
    ],
    "texel_provenance": [
        "texel_provenance.py",
    ],
    "measure_report": [
        "e04_g7_sheet.py", "e04_sheet_renders.py", "e12_ab_sheet.py",
        "e12_head_sheet.py", "e12_n_sheet.py", "e12_pair_sheet.py",
        "e13_gate1_sheet.py", "e13_payoff_sheet.py", "e14_pair_sheet.py",
        # tools/verify (task 2-pre)
        "gate0_sheet.py", "gate1_sheet.py", "head_crop.py",
        # E33, judged under the rule above - docstring line 1 plus filename, NOT
        # the body. Line 1 is "the register sheet: concept | clay | control | one
        # column per CANDIDATE register", which is a comparison-sheet builder, and
        # task 2-pre's own precedent puts comparison-sheet builders here (it is why
        # gate0_sheet / gate1_sheet / head_crop sit in this list). Following that
        # precedent deliberately rather than opening a new bucket for one file.
        "e33_register_sheet.py",
    ],
    "mesh_stats": [
        "mesh_stats.py",
    ],
    "anchor_check": [
        # tools/verify (task 2c) - the FIRST file this question has ever
        # attracted: commissioned at E28 Ruling 10, entered by ruling + wrap
        # per Ruling 3's entry rule, census re-run in the entering commit.
        "anchor_compare.py",
    ],
    "ambiguous": [
        "blade_band.py", "e04_frame_agree.py", "e04_replay_owner.py",
        "e10_claim_replay.py", "e10_consumers_subject.py",
        "e10_offsurface_consumers.py", "e10_offsurface_where.py",
        "e12_agree_probe.py", "e12_crop_silhouette.py",
        "e12_mouth_geometry.py", "e12_view_visibility.py", "e13_hole_map.py",
        "e13_thin_inputs.py", "e14_atlas_anatomy.py", "flagged_identity.py",
        "keyed_outside.py", "silhouette_agree.py",
        # tools/verify (task 2-pre)
        "montage.py",
    ],
    "no opinion": [
        "e07_score_arm.py", "e14_deep_share.py", "texpass_metrics.py",
    ],
    # AT THE E35 CLOSE one file joined `tools/verify/`: `tree_manifest.py`, judged under
    # the same rule. Line 1 - "Protection manifests for the read-only trees: verify one,
    # or emit a new one" - names tree integrity, which is not one of the eight spec
    # questions, and the tool returns HELD/FIRED rather than a measurement. `gate_mesh`
    # is the precedent applied deliberately: a VERDICT tool is `none`.
    "none": [
        "build_masks.py", "canny_probe.py", "commit_funnel.py",
        "e04_backdrop.py", "e04_bands.py", "e04_blotch.py",
        "e04_g7_landing.py", "e04_g7_where.py", "e04_invar_probe.py",
        "e04_make_brush_prompts.py", "e04_profile_check.py",
        "e04_registry_sweep.py", "e04_seam_sources.py", "e04_ship_measure.py",
        "e04_twin_baseline.py", "e07_gate0.py", "e07_l1_andon.py",
        "e07_l2_bound.py", "e08_acceptance.py", "e08_bg_derive.py",
        "e08_bg_separation.py", "e08_contradiction.py", "e08_deltaE.py",
        "e08_intersect_delta.py", "e08_metric_probe.py", "e08_registration.py",
        "e12_canny_derive.py", "e12_family_mass.py", "e12_frame.py",
        "e12_head_evidence.py", "e12_head_render.py",
        "e12_help_format_scan.py", "e12_make_twin_prompts.py",
        "e12_pair_cloud_step.py", "e12_region_colour.py",
        "e12_region_crops.py", "e12_stem_delta.py", "e12_twin_gate.py",
        "e12_twin_readout.py", "e13_a2_allocation.py", "e13_anchor_check.py",
        "e13_crop_registration.py", "e14_backdrop_checks.py",
        "e14_band_density.py", "e14_band_edges.py", "e14_demote_garnet.py",
        "e14_garnet_reproject.py", "e14_make_brush_prompts.py",
        "e14_pair_readout.py", "e14_repair_collar.py", "e14_stroke_watch.py",
        "e14_twin_registration.py",
        # E32, judged under the rule above - docstring line 1 plus filename,
        # NOT the body. `e32_plate_geometry` line 1 is "a concept plate's OWN
        # geometry, before anything reconstructs it": the spec has no tool that
        # measures an INPUT IMAGE, and its widths are a 2D mask's local
        # thickness, not `thin_extent_curve`'s per-view front-to-back extent of
        # a mesh. `e32_route_preprocess` line 1 is "what the reconstructor
        # ACTUALLY sees, reproduced from its own source" - a preprocessing
        # reproduction, which is also a question the spec does not list.
        "e32_plate_geometry.py", "e32_route_preprocess.py",
        "foreshorten_table.py",
        "gained_bg_check.py", "hair_agree.py", "hair_edge.py", "head_yaw.py",
        "prep_front.py",
        # tools/verify (task 2-pre)
        "gate_mesh.py", "head_render.py", "turn_render.py", "tree_manifest.py",
    ],
}
G_PROPOSAL = dict((fn, verdict) for verdict, fns in _G.items() for fn in fns)


def read_text(p):
    with io.open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def members(dir_rel=DIAG_REL):
    """The population of one home. Every `.py` file directly in `dir_rel`.

    A CURATED MEMBERSHIP IS THE THING THIS ARC EXISTS TO STOP, so there is no
    filter here - not `__init__.py`, not files without a docstring, not
    libraries imported by other diagnostics. Those are members that score
    `false` on axis A; that is a RESULT, not an entry condition.

    Parameterized at E28 task 2-pre (Amendment 1): the boundary's backing map
    spans two homes, so the census must reach both. Diagnostics stays the
    default."""
    d = os.path.join(REPO, dir_rel.replace("/", os.sep))
    if not os.path.isdir(d):
        raise RuntimeError(
            "ANDON: %s does not exist, so this census has no population."
            % d)
    names = sorted(fn for fn in os.listdir(d)
                   if os.path.isfile(os.path.join(d, fn))
                   and fn.endswith(".py"))
    others = sorted(fn for fn in os.listdir(d)
                    if os.path.isfile(os.path.join(d, fn))
                    and not fn.endswith(".py"))
    return names, others


# ---------------------------------------------------------------------------
# axes A, B, C - source-text properties, read from the AST
# ---------------------------------------------------------------------------

def _module_level_strings(tree):
    """String constants reachable from a module-level statement WITHOUT
    entering a function or class body - the strict `hardcoded subject constant`
    reading, which is the shape that made `e10_offsurface` un-wrappable."""
    out = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            continue
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            continue                                  # the module docstring
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                out.append(sub.value)
    return out


def _docstring_nodes(tree):
    out = set()
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(node, (ast.Module, ast.FunctionDef,
                                 ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if body and isinstance(body[0], ast.Expr) \
                and isinstance(body[0].value, ast.Constant) \
                and isinstance(body[0].value.value, str):
            out.add(id(body[0].value))
    return out


def _all_strings_excluding_docstrings(tree):
    doc = _docstring_nodes(tree)
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in doc]


def _subject_hits(strings):
    """The literals themselves, not a boolean - the dispatch's requirement.
    A boolean would hide which subject a file is bound to, which is the part a
    reader needs to decide whether it can be pointed elsewhere."""
    out = []
    for s in strings:
        if any(mk in s for mk in SUBJECT_MARKERS):
            out.append(s if len(s) <= 120 else s[:117] + "...")
    return sorted(set(out))


def source_axes(path):
    """A, B and C for one file. A SyntaxError is a FINDING, not a crash."""
    text = read_text(path)
    row = {"parse_error": None, "lines": text.count("\n") + 1}
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        row["parse_error"] = "SyntaxError at line %s" % exc.lineno
        row.update(a_argparse=None, a_add_argument=None, a_main_guard=None,
                   invocable=None, b1_literals=[], b2_literals=[],
                   docstring_line1=None)
        return row

    imports_argparse = any(
        (isinstance(n, ast.Import)
         and any(al.name.split(".")[0] == "argparse" for al in n.names))
        or (isinstance(n, ast.ImportFrom)
            and (n.module or "").split(".")[0] == "argparse")
        for n in ast.walk(tree))
    n_add_argument = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
        and n.func.attr == "add_argument")
    main_guard = any(
        isinstance(node, ast.If) and "__main__" in ast.dump(node.test)
        for node in tree.body)

    # REPORTED COMPONENT, added after the first pass and moving NO
    # pre-registered count. The first run measured 93 files with a flag surface
    # against 6 with a `__main__` guard, which is not a near-miss - it is the
    # directory's house style: a straight-line script that calls `parse_args()`
    # at module level and does its work below. Such a file HAS a command-line
    # surface and is pointable at a new subject; what it lacks is
    # importability-without-side-effects. Those are two different properties
    # and the census reports both rather than letting one stand for the other.
    parse_args_module_level = False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute) \
                    and sub.func.attr == "parse_args":
                parse_args_module_level = True

    doc = ast.get_docstring(tree, clean=False)
    line1 = None
    if doc is not None:
        line1 = ""
        for ln in doc.split("\n"):
            if ln.strip():
                line1 = ln.strip()
                break

    row.update(
        a_argparse=imports_argparse,
        a_add_argument=n_add_argument,
        a_main_guard=main_guard,
        a_parse_args_module_level=parse_args_module_level,
        # the flag surface alone - "can this be pointed at a new subject",
        # which is the property axis A's rationale actually names. Reported
        # BESIDE `invocable` rather than instead of it: `invocable` is the
        # definition pre-registered in E28-predictions.md and it does not move
        # after the fact.
        flag_surface=bool(imports_argparse and n_add_argument > 0),
        # ALL THREE, because the property is "can this be pointed at a new
        # subject from a command line" and no one clause delivers it.
        invocable=bool(imports_argparse and n_add_argument > 0 and main_guard),
        b1_literals=_subject_hits(_module_level_strings(tree)),
        b2_literals=_subject_hits(_all_strings_excluding_docstrings(tree)),
        docstring_line1=line1,
    )
    return row


# ---------------------------------------------------------------------------
# axis D - cited in the corpus   /   axis E - anchored by a test
# ---------------------------------------------------------------------------

def corpus_files():
    """`record_markdown()`'s set, UNMODIFIED - E26 ruled that function
    unchanged, and this census reads it rather than widening it."""
    import facet_index
    return list(facet_index.record_markdown())


# The census's own outputs live under `docs/` and are therefore INSIDE
# `record_markdown()`'s set. `instrument-census.md` tabulates all 99 filenames,
# so on any run after the first it cites every member and axis D reads 99/99.
# THAT IS CIRCULAR BY CONSTRUCTION: a derived artifact of this measurement is
# not evidence about this measurement's subject.
#
# Measured, first run against second: axis D read 76 before the output existed
# and 99 after. Excluded here rather than merely noted, because a headline
# number that flips to 100% on a second invocation is not a number.
SELF_OUTPUTS = ("docs/instrument-census.md", "docs/instrument-census.json")

# AND THE SAME RULE REACHES THE ARC'S OWN DOCUMENTS, which is where it first
# bit hard. `E28-instrument-census-report.md` discusses this census by naming
# the files it found - the uncited ones, the unanchored ones, the ambiguous
# ones - so committing the report made **every one of the 99 cited**:
#
#     cited-at-all, committed census (before the report existed)      76
#     cited-at-all, with the report in the corpus                     99
#     cited-at-all, excluding this arc's documents                    76
#
# Caught by `test_t41_axis_d_is_idempotent_across_runs`, which FIRED on the
# closing suite run - 51 rows drifted. The exclusion is the rule already
# written above applied to a member of its class that the first pass missed,
# not a threshold moved after seeing a result: the headline does not move (76
# either way, measured both before and after), and the unexcluded count is
# still computed and reported as `cited_count_raw`.
#
# A LATER ARC THAT RE-CENSUSES ADDS ITS OWN PREFIX HERE, on purpose, in the
# commit that writes its report.
SELF_DOC_PREFIXES = ("docs/experiments/E28-",)


def is_self_document(rel):
    """True for a corpus file that exists to describe this census."""
    return rel in SELF_OUTPUTS or rel.startswith(SELF_DOC_PREFIXES)


def test_files():
    out = []
    for dirpath, dirnames, filenames in os.walk(os.path.join(REPO, "tests")):
        dirnames.sort()
        for fn in sorted(filenames):
            if fn.endswith(".py"):
                out.append(os.path.relpath(os.path.join(dirpath, fn), REPO)
                           .replace("\\", "/"))
    return sorted(out)


def naming_files(rels, names):
    """{name: [rel, ...]} - which of `rels` contain each name as literal text.

    AXIS E'S UNIT, STATED: a GLOB DOES NOT NAME A MODULE. A test that walks
    `tools/diagnostics/*.py` exercises every file and names none of them, so
    those files score `false` here. That is the honest reading of "would an
    edit to this be CAUGHT by name", and it is the axis most likely to be
    misread afterwards."""
    out = dict((n, []) for n in names)
    for rel in rels:
        try:
            body = read_text(os.path.join(REPO, rel.replace("/", os.sep)))
        except OSError:
            continue
        for n in names:
            if n in body:
                out[n].append(rel)
    return out


# ---------------------------------------------------------------------------
# axis F - import-safe, in three interpreter modes
# ---------------------------------------------------------------------------
MODES = (("normal", [], None),
         ("-O", ["-O"], None),
         ("PYTHONOPTIMIZE=1", [], "1"))

_IMPORTERR = re.compile(
    r"(?:ModuleNotFoundError|ImportError): (?:No module named )?'?([\w.]+)")


def help_probe(python, path, timeout):
    """({mode: verdict}, blocker) for one invocable file.

    verdict: 'clean' | 'rc=N' | 'stderr' | 'timeout' | 'spawn-error'
    blocker: the module whose absence stopped the import, or None."""
    verdicts, blocker = {}, None
    for name, flags, optimize in MODES:
        env = dict(os.environ)
        env.pop("PYTHONOPTIMIZE", None)
        if optimize is not None:
            env["PYTHONOPTIMIZE"] = optimize
        try:
            p = subprocess.run([python] + flags + [path, "--help"],
                               cwd=REPO, capture_output=True,
                               timeout=timeout, env=env)
        except subprocess.TimeoutExpired:
            verdicts[name] = "timeout"
            continue
        except OSError as exc:
            verdicts[name] = "spawn-error:%s" % exc.__class__.__name__
            continue
        err = p.stderr.decode("utf-8", "replace")
        if blocker is None:
            m = _IMPORTERR.search(err)
            if m:
                blocker = m.group(1)
        if p.returncode != 0:
            verdicts[name] = "rc=%d" % p.returncode
        elif err.strip():
            verdicts[name] = "stderr"
        else:
            verdicts[name] = "clean"
    return verdicts, blocker


def axis_f(row, python, path, timeout, skip):
    """'true' | 'false' | 'n/a', plus the reason and the per-mode verdicts."""
    if skip:
        return "n/a", "probe skipped (--skip-probe)", {}
    if row.get("parse_error"):
        return "n/a", "does not parse: %s" % row["parse_error"], {}
    if not row["invocable"]:
        # THE REASON IS SPLIT because "axis A false" covers two very different
        # states and calling both "no CLI" would be inaccurate for 88 files.
        # The VERDICT is n/a either way and no count moves; only the sentence
        # a reader gets changes.
        if not row["flag_surface"]:
            return "n/a", "no flag surface: no argparse or no add_argument", {}
        return "n/a", ("has a flag surface but no `__main__` guard, so probing "
                       "it would EXECUTE the module body - against whatever "
                       "subject its constants name. Not probed, deliberately"), {}
    verdicts, blocker = help_probe(python, path, timeout)
    vals = set(verdicts.values())
    if blocker is not None:
        return "n/a", "import blocked: %s absent from this interpreter" % blocker, verdicts
    if "timeout" in vals:
        return "n/a", "timed out after %ds; the measurement did not run" % timeout, verdicts
    if any(v.startswith("spawn-error") for v in vals):
        return "n/a", "could not spawn the interpreter", verdicts
    if vals == {"clean"}:
        return "true", "", verdicts
    bad = sorted(m for m, v in verdicts.items() if v != "clean")
    return "false", "not clean in: %s" % ", ".join(bad), verdicts


# ---------------------------------------------------------------------------
# the census
# ---------------------------------------------------------------------------

def build(python, timeout, skip_probe, progress=False, dirs=(DIAG_REL,)):
    per_dir = []
    names = []
    home = {}
    for dir_rel in dirs:
        d_names, d_others = members(dir_rel)
        per_dir.append({"dir": dir_rel, "py_files": len(d_names),
                        "non_py_files": len(d_others),
                        "non_py_names": d_others})
        for fn in d_names:
            # FILENAMES ARE THE KEY for axes D/E and axis G, so a name that
            # appears in two censused homes would silently merge two files'
            # evidence. Refuse rather than merge.
            if fn in home:
                raise RuntimeError(
                    "ANDON: %s exists in both %s and %s. The census keys "
                    "axes D/E/G on the filename; two homes sharing one name "
                    "would merge two files' evidence. Rename one, or key the "
                    "census on relative paths - deliberately."
                    % (fn, home[fn], dir_rel))
            home[fn] = dir_rel
        names.extend(d_names)
    names.sort()
    corpus_raw = corpus_files()
    corpus = [r for r in corpus_raw if not is_self_document(r)]
    # the unexcluded set, kept so the contamination stays visible rather than
    # merely handled
    corpus_outputs_only = [r for r in corpus_raw if r not in SELF_OUTPUTS]
    tests = test_files()

    # A WHOLLY EMPTY `G_PROPOSAL` IS THE BOOTSTRAP STATE and is allowed here on
    # purpose: axis G is read off axis C, and nobody can judge 99 docstrings
    # they have not read yet, so the first pass runs mechanically and the
    # judgments are written against its output. What makes that state
    # non-shippable is T41's `every_member_has_an_axis_g_judgment`, not this
    # function - the gate lives in the harness where it stays runnable. Once
    # ANY judgment exists, a MISSING one is an ANDON: a file added later must
    # force a deliberate judgment rather than inherit a default.
    missing_g = [n for n in names if n not in G_PROPOSAL]
    if missing_g and G_PROPOSAL:
        raise RuntimeError(
            "ANDON: axis G has no entry for %d file(s): %s. A missing "
            "judgment must not default to `none` - a table of confident "
            "`none`s reads as a measurement. Judge them, or write "
            "'no opinion', which is a real value here."
            % (len(missing_g), ", ".join(missing_g[:8])))

    cited = naming_files(corpus, names)
    cited_raw = naming_files(corpus_outputs_only, names)
    # AXIS E TAKES BOTH FORMS. The definition registered in E28-predictions.md
    # before any measurement is "basename OR DOTTED MODULE NAME as literal
    # text". The first implementation matched only `foo.py` and under-reported
    # the axis by two: tests in this repo name modules both ways - T40 writes
    # `e12_offsurface`, T35/T38 and a fixture write `texel_provenance`. The
    # stricter basename-only read is kept beside it rather than discarded,
    # because `texel_provenance` is ALSO one of the spec's eight tool names, so
    # a test naming the TOOL is indistinguishable from one naming the MODULE by
    # this method. Both readings ride in the payload; neither is picked here.
    stems = [n[:-3] for n in names]
    anchored_ext = naming_files(tests, names)
    anchored_stem = naming_files(tests, stems)

    rows = []
    for i, fn in enumerate(names, 1):
        if progress:
            sys.stderr.write("\r  [%d/%d] %-44s" % (i, len(names), fn))
            sys.stderr.flush()
        path = os.path.join(REPO, home[fn].replace("/", os.sep), fn)
        row = {"file": fn, "dir": home[fn]}
        row.update(source_axes(path))
        f, reason, verdicts = axis_f(row, python, path, timeout, skip_probe)
        row["import_safe"] = f
        row["import_safe_reason"] = reason
        row["import_safe_modes"] = verdicts
        row["cited_in"] = cited[fn]
        # THE HEADLINE: over the corpus minus every document that exists to
        # describe this census - its own outputs AND this arc's papers.
        row["cited_count"] = len(cited[fn])
        # the same count with only the outputs excluded, so a reader can see
        # exactly how much of axis D this arc contributed to itself.
        row["cited_count_raw"] = len(cited_raw[fn])
        row["anchored_in"] = sorted(set(anchored_ext[fn])
                                    | set(anchored_stem[fn[:-3]]))
        row["anchored"] = bool(row["anchored_in"])
        row["anchored_in_basename_only"] = anchored_ext[fn]
        row["anchored_basename_only"] = bool(anchored_ext[fn])
        row["g_proposal"] = G_PROPOSAL.get(fn, "no opinion")
        rows.append(row)
    if progress:
        sys.stderr.write("\r" + " " * 62 + "\r")
    return {
        "population": {
            "dirs": per_dir,
            "py_files_total": len(names),
        },
        "provenance": {
            "probe_interpreter": python,
            "probe_interpreter_version": sys.version.split()[0],
            "probe_timeout_s": timeout,
            "probe_skipped": bool(skip_probe),
            "corpus_files": len(corpus),
            "corpus_files_before_self_exclusion": len(corpus_raw),
            "self_documents_excluded": [r for r in corpus_raw
                                        if is_self_document(r)],
            "test_files": len(tests),
        },
        "rows": rows,
    }


def totals(c):
    r = c["rows"]
    return {
        "invocable": sum(1 for x in r if x["invocable"]),
        "flag_surface": sum(1 for x in r if x.get("flag_surface")),
        "argparse": sum(1 for x in r if x["a_argparse"]),
        "main_guard": sum(1 for x in r if x["a_main_guard"]),
        "any_add_argument": sum(1 for x in r if (x["a_add_argument"] or 0) > 0),
        "parse_args_module_level":
            sum(1 for x in r if x.get("a_parse_args_module_level")),
        "flag_surface_unguarded":
            sum(1 for x in r if x.get("flag_surface") and not x["a_main_guard"]),
        "subject_bound_b1": sum(1 for x in r if x["b1_literals"]),
        "subject_bound_b2": sum(1 for x in r if x["b2_literals"]),
        "has_docstring": sum(1 for x in r if x["docstring_line1"] is not None),
        "cited": sum(1 for x in r if x["cited_count"] > 0),
        "cited_raw": sum(1 for x in r if x["cited_count_raw"] > 0),
        "anchored": sum(1 for x in r if x["anchored"]),
        "anchored_basename_only":
            sum(1 for x in r if x.get("anchored_basename_only")),
        "import_safe_true": sum(1 for x in r if x["import_safe"] == "true"),
        "import_safe_false": sum(1 for x in r if x["import_safe"] == "false"),
        "import_safe_na": sum(1 for x in r if x["import_safe"] == "n/a"),
        "parse_errors": sum(1 for x in r if x["parse_error"]),
        "g_mapped": sum(1 for x in r if x["g_proposal"] in SPEC_TOOLS),
        "g_none": sum(1 for x in r if x["g_proposal"] == "none"),
        "g_ambiguous": sum(1 for x in r if x["g_proposal"] == "ambiguous"),
        "g_no_opinion": sum(1 for x in r if x["g_proposal"] == "no opinion"),
    }


def _cell(s, n):
    s = (s or "").replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= n else s[:n - 1] + "\u2026"


def to_markdown(c):
    t = totals(c)
    p, pv = c["population"], c["provenance"]
    N = p["py_files_total"]
    homes = " + ".join("`%s/`" % d["dir"] for d in p["dirs"])
    L = []
    A = L.append
    A("# The instrument census — %s" % homes)
    A("")
    A("**Generated by [`tools/instrument_census.py`](../tools/instrument_census.py). "
      "Do not hand-edit — re-run it (`--committed` emits this pair).** E28 task 1, at "
      "the Director's ruling on [the spec](specs/measurement-mcp-spec.md)'s open "
      "question 1: *commission the census first* — extended to `tools/verify/` at "
      "task 2-pre ([Amendment 1](experiments/E28-instrument-census-kickoff.md)), because "
      "the boundary's backing map spans both homes.")
    A("")
    A("**Axes A–F are mechanical.** **Axis G is a judgment and is a PROPOSAL** — the "
      "boundary is the advisor's to rule and the Director's to adjust. `no opinion` is "
      "a real value in it.")
    A("")
    A("## The population")
    A("")
    A("| | |")
    A("|---|---|")
    for d in p["dirs"]:
        A("| `.py` files in `%s` | **%d** |" % (d["dir"], d["py_files"]))
        A("| — files of any other extension there | %d |" % d["non_py_files"])
    A("| **total members** | **%d** |" % N)
    A("| corpus files read for axis D | %d |" % pv["corpus_files"])
    A("| test files read for axis E | %d |" % pv["test_files"])
    A("| probe interpreter | `%s` (%s) |"
      % (pv["probe_interpreter"], pv["probe_interpreter_version"]))
    A("")
    A("## Totals")
    A("")
    A("| axis | measure | count | of |")
    A("|---|---|---:|---:|")
    A("| A | **invocable** (argparse **and** ≥1 `add_argument` **and** a `__main__` guard) | **%d** | %d |"
      % (t["invocable"], N))
    A("| A | — imports `argparse` | %d | %d |" % (t["argparse"], N))
    A("| A | — has ≥1 `add_argument` | %d | %d |" % (t["any_add_argument"], N))
    A("| A | — has a `__main__` guard | %d | %d |" % (t["main_guard"], N))
    A("| A | — **flag surface** (argparse **and** ≥1 `add_argument`, guard not required) | **%d** | %d |"
      % (t["flag_surface"], N))
    A("| A | — calls `parse_args()` at module level | %d | %d |"
      % (t["parse_args_module_level"], N))
    A("| A | — **flag surface but UNGUARDED** (the house style) | **%d** | %d |"
      % (t["flag_surface_unguarded"], N))
    A("| B1 | **subject-bound**, module-level literal | **%d** | %d |"
      % (t["subject_bound_b1"], N))
    A("| B2 | subject marker in any non-docstring literal | %d | %d |"
      % (t["subject_bound_b2"], N))
    A("| C | has a docstring | %d | %d |" % (t["has_docstring"], N))
    A("| D | **cited** in ≥1 corpus file | **%d** | %d |" % (t["cited"], N))
    A("| D | — with this arc's own documents left IN (the contaminated read) | %d | %d |"
      % (t["cited_raw"], N))
    A("| E | **anchored** — basename *or* module name as literal text under `tests/` | **%d** | %d |"
      % (t["anchored"], N))
    A("| E | — basename-with-`.py` only (the stricter read) | %d | %d |"
      % (t["anchored_basename_only"], N))
    A("| F | **import-safe** in all three modes | **%d** | %d |"
      % (t["import_safe_true"], N))
    A("| F | — not clean in some mode | %d | %d |"
      % (t["import_safe_false"], N))
    A("| F | — **`n/a`**, property not defined (reason per row) | %d | %d |"
      % (t["import_safe_na"], N))
    A("| G | *proposed* to answer one of the spec's eight | *%d* | %d |"
      % (t["g_mapped"], N))
    A("| G | *proposed* `none` | *%d* | %d |" % (t["g_none"], N))
    A("| G | *proposed* `ambiguous` | *%d* | %d |" % (t["g_ambiguous"], N))
    A("| G | *`no opinion`* | *%d* | %d |" % (t["g_no_opinion"], N))
    if t["parse_errors"]:
        A("| — | **files that do not parse** | **%d** | %d |"
          % (t["parse_errors"], N))
    A("")
    A("## Axis G — the proposal, by tool")
    A("")
    A("| the spec's question | files proposed |")
    A("|---|---|")
    for tool in SPEC_TOOLS:
        hits = [x["file"] for x in c["rows"] if x["g_proposal"] == tool]
        A("| `%s` | %s |" % (tool, ", ".join("`%s`" % h for h in hits) or "—"))
    A("")
    A("## Every file")
    A("")
    A("`A` invocable · `B1` module-level subject literal · `D` citing corpus files · "
      "`E` anchored by a test · `F` import-safe in three modes · "
      "`G` *proposal*")
    A("")
    A("| # | file | home | A | flags | B1 | D | E | F | G *(proposal)* | the question (docstring line 1) |")
    A("|---:|---|---|:-:|---:|:-:|---:|:-:|:-:|---|---|")
    for i, x in enumerate(c["rows"], 1):
        f = x["import_safe"]
        fcell = {"true": "yes", "false": "**no**", "n/a": "n/a"}[f]
        A("| %d | `%s` | %s | %s | %s | %s | %d | %s | %s | %s | %s |" % (
            i, x["file"],
            x["dir"].rsplit("/", 1)[-1],
            "—" if x["invocable"] is None else ("yes" if x["invocable"] else "no"),
            "—" if x["a_add_argument"] is None else x["a_add_argument"],
            "**yes**" if x["b1_literals"] else "no",
            x["cited_count"],
            "yes" if x["anchored"] else "no",
            fcell,
            x["g_proposal"],
            _cell(x["docstring_line1"] if x["docstring_line1"] is not None
                  else "*(no docstring)*", 88)))
    A("")
    A("## Axis F — every `n/a` and every `false`, with its reason")
    A("")
    A("A silent `false` where the property is undefined is the error E27 Ruling 5 "
      "names. Each row below says which.")
    A("")
    A("| file | F | reason | normal | `-O` | `PYTHONOPTIMIZE=1` |")
    A("|---|:-:|---|---|---|---|")
    for x in c["rows"]:
        if x["import_safe"] == "true":
            continue
        m = x["import_safe_modes"]
        A("| `%s` | %s | %s | %s | %s | %s |" % (
            x["file"], x["import_safe"], _cell(x["import_safe_reason"], 74),
            m.get("normal", "—"), m.get("-O", "—"),
            m.get("PYTHONOPTIMIZE=1", "—")))
    A("")
    A("## Axis B — the literals themselves")
    A("")
    A("A boolean would hide *which* subject a file is bound to, which is the part that "
      "decides whether it can be pointed elsewhere.")
    A("")
    A("| file | B1 (module-level) | B2 only (deeper) |")
    A("|---|---|---|")
    for x in c["rows"]:
        if not x["b1_literals"] and not x["b2_literals"]:
            continue
        b2only = [s for s in x["b2_literals"] if s not in x["b1_literals"]]
        A("| `%s` | %s | %s |" % (
            x["file"],
            "<br>".join("`%s`" % _cell(s, 60) for s in x["b1_literals"]) or "—",
            "<br>".join("`%s`" % _cell(s, 60) for s in b2only) or "—"))
    A("")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Census an instrument home across six mechanical axes "
                    "plus one labelled judgment.")
    ap.add_argument("--dir", action="append", dest="dirs", metavar="REL",
                    help="a directory to census, relative to the repo root; "
                         "repeatable. Default: %s alone. The COMMITTED outputs "
                         "are emitted with --committed, which is %s - T41 pins "
                         "that shape so a partial re-emit cannot land silently."
                         % (DIAG_REL, " + ".join(COMMITTED_DIRS)))
    ap.add_argument("--committed", action="store_true",
                    help="census exactly the homes the committed outputs "
                         "cover: %s" % ", ".join(COMMITTED_DIRS))
    ap.add_argument("--out-md", default=os.path.join(REPO, "docs",
                                                     "instrument-census.md"))
    ap.add_argument("--out-json", default=os.path.join(REPO, "docs",
                                                       "instrument-census.json"))
    ap.add_argument("--python", default=sys.executable,
                    help="interpreter for the axis-F probe (default: this one)")
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--skip-probe", action="store_true",
                    help="axes A-E and G only; axis F becomes n/a everywhere")
    ap.add_argument("--json-only", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    if args.committed and args.dirs:
        ap.error("--committed and --dir are mutually exclusive")
    dirs = tuple(args.dirs) if args.dirs else \
        (COMMITTED_DIRS if args.committed else (DIAG_REL,))

    c = build(args.python, args.timeout, args.skip_probe,
              progress=not args.quiet, dirs=dirs)
    t = totals(c)

    for p in (args.out_json, args.out_md):
        d = os.path.dirname(p)
        if d and not os.path.isdir(d):
            os.makedirs(d)                 # scripts create their own dirs
    with io.open(args.out_json, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"population": c["population"], "provenance": c["provenance"],
                   "totals": t, "rows": c["rows"]},
                  fh, indent=2, sort_keys=True)
        fh.write("\n")
    if not args.json_only:
        with io.open(args.out_md, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(to_markdown(c))

    if not args.quiet:
        for d in c["population"]["dirs"]:
            print("[census] %s -> %d .py, %d other"
                  % (d["dir"], d["py_files"], d["non_py_files"]))
        for k in sorted(t):
            print("    %-22s %d" % (k, t[k]))
        print("[census] %s" % args.out_json)
        if not args.json_only:
            print("[census] %s" % args.out_md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
