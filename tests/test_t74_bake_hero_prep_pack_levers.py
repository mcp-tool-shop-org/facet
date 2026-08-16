"""T74 - bake_hero_prep.py's new --margin-method/--shape-method flags (E38 Phase 2, A1/A3).

WHY THIS EXISTS. E38 Phase 2's lever sweep needed bpy.ops.uv.pack_islands' margin_method
and shape_method exposed on the command line -- previously bake_hero_prep.py:319 (now moved
by this edit) passed only margin=. Both are OPTIONAL, default=None, so an unqualified
invocation (every historical command, including A0's own) takes the exact code path it
always did: pack_islands() is called WITHOUT the two new kwargs, and Blender's own operator
default governs (SCALED / CONCAVE, confirmed by RNA introspection on this rig's 5.2 with NO
scene-level mirror overriding either property -- unlike bake's own margin_type/use_clear,
which DO have a scene mirror that silently wins, the trap this session found the hard way
on a neighbouring tool before trusting this one the same way twice).

WHAT THIS FILE DOES NOT DO, and why, matching T31's own stated convention exactly:
bake_hero_prep.py imports bpy at module level (test_t31_route_tool_compiles and
test_t31_the_blender_pair_cannot_run_under_this_interpreter already establish this for the
whole file), so no test here executes the tool or its --help -- that is T31's own "openly
stated gap" for the Blender pair, unchanged by this edit. Every check below is AST-only,
needing no bpy.

THE FUNCTIONAL PROOF LIVES OUTSIDE PYTEST, BY THIS REPO'S OWN ESTABLISHED PATTERN FOR THIS
GAP: E38 Phase 2 ran the full reconstructed A0 command (prep -> material -> pack -> render
-> census) through this EDITED file with the two new flags OMITTED, and diffed the result
against the recorded A0 build. Atlas PNG byte-identical, all 8 renders PIXEL-identical,
fresh census 425/1322/22 -- exact match, per-view and total
(E:/AI/training/facet_E38/phase2/logs/tool_edit_anchor_*.txt). That is the anchor this file
cannot replace and does not try to; it is named here so a reader does not mistake AST-only
coverage for the whole story.

CORRECTED AT THE RULING SEAT (E38 Ruling 5, 2026-08-16), in place rather than quietly:
this paragraph read "all 8 renders byte-identical". Re-run independently, all eight PNG FILE
HASHES DIFFER (view 0: bb89fbffefcf0e79 vs 86d9b2b0e458a0c3, and so for all eight) while all
eight are pixel-identical -- 0 differing pixels, maxabs 0, over (1024, 368, 4). The two
atlases genuinely ARE byte-identical. This is the third live firing of this repo's own law
that a PNG hash mismatch is not evidence a render changed, because file bytes are not pixel
values; a byte-check re-run of this anchor would have produced a FALSE HALT on a correct
result. The anchor holds and its force is undiminished -- pixel identity is the stronger
claim here anyway, being a statement about the render rather than about the encoder.

Standards compliance: PIN_PER_STEP -- the RNA-confirmed legal enum values are pinned here so
a future edit that lets an illegal choice through fails this test rather than failing inside
Blender at runtime. ANDON_AUTHORITY -- this edit adds zero new ANDON sites; the pinned
per-file census (test_t31_the_census_is_the_one_e23_measured, bake_hero_prep.py: 15) is
unmoved by design and re-run (not duplicated) rather than re-pinned here.
"""
import ast
import io

from conftest import tool

REL = "bake_hero_prep.py"

# Confirmed by fresh RNA introspection on this rig's Blender 5.2, both at the operator
# level and the scene-level BakeSettings-style mirror search (none exists for these two
# properties) -- E:/AI/training/facet_E38/phase2/logs/introspect_pack_islands.txt and
# probe_pack_islands_scene_mirror.txt. Not re-derived here; cited as the ground truth an
# illegal choices= list would silently diverge from.
LEGAL_MARGIN_METHOD = {"SCALED", "ADD", "FRACTION"}
LEGAL_SHAPE_METHOD = {"CONCAVE", "CONVEX", "AABB"}


def _add_argument_calls(src):
    """Every ap.add_argument(...) call in the module, as AST Call nodes."""
    tree = ast.parse(src)
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and n.func.attr == "add_argument"]


def _kwarg(call, name):
    for kw in call.keywords:
        if kw.arg == name:
            return kw.value
    return None


def _first_str_arg(call):
    if call.args and isinstance(call.args[0], ast.Constant):
        return call.args[0].value
    return None


def _find_flag(calls, flag_name):
    for c in calls:
        if _first_str_arg(c) == flag_name:
            return c
    return None


def test_t74_both_new_flags_are_declared():
    """--margin-method and --shape-method exist as real add_argument() calls."""
    src = io.open(tool(REL), encoding="utf-8").read()
    calls = _add_argument_calls(src)
    assert _find_flag(calls, "--margin-method") is not None, (
        "--margin-method is not declared in %s" % REL)
    assert _find_flag(calls, "--shape-method") is not None, (
        "--shape-method is not declared in %s" % REL)


def test_t74_both_new_flags_default_to_none():
    """default=None on BOTH is what makes an unqualified command (A0's own, and every
    historical invocation) take the exact code path it always did -- the reproducibility
    guarantee this whole edit rests on. A non-None default here would silently change A0's
    own behaviour the next time someone reruns the reconstructed command without either
    flag, which is exactly the failure this test exists to catch before it reaches Blender.
    """
    src = io.open(tool(REL), encoding="utf-8").read()
    calls = _add_argument_calls(src)
    for flag in ("--margin-method", "--shape-method"):
        call = _find_flag(calls, flag)
        default_node = _kwarg(call, "default")
        assert default_node is not None, "%s has no default= kwarg" % flag
        assert isinstance(default_node, ast.Constant) and default_node.value is None, (
            "%s defaults to %r, not None -- an unqualified command would no longer "
            "reproduce A0 byte-for-byte" % (flag, ast.dump(default_node)))


def test_t74_choices_match_the_rna_confirmed_legal_values():
    """The choices= list for each flag is EXACTLY the enum Blender's own pack_islands
    operator accepts on this rig -- not a superset (which argparse would accept, then
    Blender would refuse to interpret) and not a subset (which would need no test, but a
    silently-narrowed set is still worth catching if it happens by accident).
    """
    src = io.open(tool(REL), encoding="utf-8").read()
    calls = _add_argument_calls(src)

    mm = _find_flag(calls, "--margin-method")
    mm_choices = _kwarg(mm, "choices")
    assert mm_choices is not None and isinstance(mm_choices, ast.List)
    mm_values = {n.value for n in mm_choices.elts if isinstance(n, ast.Constant)}
    assert mm_values == LEGAL_MARGIN_METHOD, (
        "--margin-method choices %r do not match the RNA-confirmed legal set %r"
        % (mm_values, LEGAL_MARGIN_METHOD))

    sm = _find_flag(calls, "--shape-method")
    sm_choices = _kwarg(sm, "choices")
    assert sm_choices is not None and isinstance(sm_choices, ast.List)
    sm_values = {n.value for n in sm_choices.elts if isinstance(n, ast.Constant)}
    assert sm_values == LEGAL_SHAPE_METHOD, (
        "--shape-method choices %r do not match the RNA-confirmed legal set %r"
        % (sm_values, LEGAL_SHAPE_METHOD))


def test_t74_pack_islands_call_site_builds_kwargs_conditionally():
    """The call site must NOT pass margin_method=/shape_method= as bare literal keyword
    arguments to bpy.ops.uv.pack_islands(...) -- that would send an explicit value on
    EVERY run (including an unqualified A0 rebuild), which is exactly what default=None
    above is designed to prevent one level up. This checks the call site itself: the
    pack_islands Call node's own keyword list must carry ONLY 'margin' literally; the two
    new levers must arrive via a **kwargs-style Starred/dict expansion instead, which is
    what makes them absent from the call unless a flag was explicitly passed.
    """
    src = io.open(tool(REL), encoding="utf-8").read()
    tree = ast.parse(src)
    pack_calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute) and n.func.attr == "pack_islands"]
    assert len(pack_calls) == 1, (
        "expected exactly one bpy.ops.uv.pack_islands(...) call, found %d"
        % len(pack_calls))
    call = pack_calls[0]
    literal_kw_names = {kw.arg for kw in call.keywords if kw.arg is not None}
    assert "margin_method" not in literal_kw_names, (
        "pack_islands() is called with a LITERAL margin_method= kwarg -- this would send "
        "an explicit value on every run and break A0's own reproducibility; it must be "
        "conditional, via a dict built beforehand and expanded with **")
    assert "shape_method" not in literal_kw_names, (
        "pack_islands() is called with a LITERAL shape_method= kwarg -- same risk as "
        "margin_method above")
    has_double_star = any(kw.arg is None for kw in call.keywords)
    assert has_double_star, (
        "pack_islands() call carries no ** expansion -- margin_method/shape_method have "
        "no way to reach the call at all, which would silently make both new flags "
        "no-ops regardless of what the user passes on the command line")
