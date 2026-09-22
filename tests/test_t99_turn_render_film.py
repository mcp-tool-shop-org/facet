"""T99 - turn_render's film mode, after the default moved to transparent (2026-09-22).

WHY THIS FILE EXISTS. `turn_render.py` imports bpy, so the pinned interpreter cannot run
it and no test here can render anything - the same wall T31 met and stated openly for the
Blender pair. What is checkable without bpy is that the flag exists, that the default is
the one the Director asked for, and that the tool's own help still carries the MEASURED
claim rather than a plausible one. That last leg is the point: an earlier draft of this
change asserted in the help text that an opaque render is "exactly the transparent one
composited over --bg", and the measurement says it is not. If a later edit softens or
re-states the claim, these legs fail and someone has to re-measure.

THE ANCHOR, measured once on drell_composite_emblem_s42.glb, view 0, 768x1024, --clay,
both modes, Blender 5.2.0 LTS:

    fully-opaque figure pixels     181,487    max |diff| 0.0000   <- bit-identical
    fully-transparent pixels       597,234    opaque side dithered over FOUR values
                                              154,154,156 / 154,154,157 /
                                              155,155,157 / 155,155,158
    antialiased rim pixels           7,711    max 4.34/255, mean 0.80/255 after a
                                              LINEAR composite; 10.91 max in sRGB

So byte-identity for a pre-2026-09-22 invocation needs --opaque, not arithmetic, and no
measurement that reads the FIGURE is affected by the default at all.

Everything printed here is ASCII (the repo's law).
"""
import ast
import pathlib

TOOL = pathlib.Path(__file__).resolve().parents[1] / "tools" / "verify" / "turn_render.py"
SRC = TOOL.read_text(encoding="utf-8")
TREE = ast.parse(SRC)


def _film_assignments(tree):
    """Every `<...>.film_transparent = <value>` in the tree, as (node, value) pairs."""
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Attribute) and t.attr == "film_transparent":
                    out.append((t, node.value))
    return out


def _opaque_flag(tree):
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument" and node.args
                and isinstance(node.args[0], ast.Constant) and node.args[0].value == "--opaque"):
            return node
    return None


def test_t99_the_opaque_flag_is_declared_store_true():
    """store_true means absent -> False -> film_transparent True. The default IS the flag."""
    call = _opaque_flag(TREE)
    assert call is not None, "turn_render.py declares no --opaque flag"
    actions = [k.value.value for k in call.keywords
               if k.arg == "action" and isinstance(k.value, ast.Constant)]
    assert actions == ["store_true"], (
        "--opaque must be store_true so that OMITTING it gives a transparent film; got %r"
        % (actions,))
    assert not any(k.arg == "default" for k in call.keywords), (
        "--opaque must not carry an explicit default - store_true's False IS the contract")


def test_t99_film_transparent_is_driven_by_the_flag_not_hardcoded():
    """A hardcoded True would pass a corner-pixel check and still ignore --opaque."""
    assigns = _film_assignments(TREE)
    assert len(assigns) == 1, "expected exactly one film_transparent assignment, got %d" % len(assigns)
    _, value = assigns[0]
    assert isinstance(value, ast.UnaryOp) and isinstance(value.op, ast.Not), (
        "film_transparent must be `not args.opaque`, not a literal; got %s"
        % ast.dump(value))
    assert isinstance(value.operand, ast.Attribute) and value.operand.attr == "opaque", (
        "film_transparent is negating something other than args.opaque: %s"
        % ast.dump(value.operand))


def test_t99_the_hardcode_is_what_this_check_catches():
    """CAN-FAIL LEG. The two checks above must reject the shape they exist to reject,
    or they are asserting a 1 that nothing could have made a 0."""
    bad = ast.parse("scene.render.film_transparent = True\n")
    assigns = _film_assignments(bad)
    assert len(assigns) == 1
    _, value = assigns[0]
    assert not isinstance(value, ast.UnaryOp), "planted hardcode was not seen as a hardcode"
    assert _opaque_flag(bad) is None, "planted source has no --opaque and the finder found one"


def test_t99_alpha_actually_reaches_the_file():
    """film_transparent with an RGB color_mode writes the alpha away again."""
    assert 'color_mode = "RGBA"' in SRC, (
        "film_transparent is set but the PNG color_mode is not RGBA - the alpha is discarded")


def test_t99_the_help_carries_the_measurement_not_a_plausible_claim():
    """The retracted draft said the opaque frame is recoverable by compositing. It is not.
    These substrings are the measured facts; softening them without re-measuring fails here."""
    call = _opaque_flag(TREE)
    helps = [k.value for k in call.keywords if k.arg == "help"]
    assert helps, "--opaque carries no help"
    text = "".join(p.value for p in ast.walk(helps[0]) if isinstance(p, ast.Constant))
    for needle in ("181,487", "0.0000", "7,711", "4.34/255", "DITHERED"):
        assert needle in text, (
            "--opaque's help no longer states %r; the anchor in this file's docstring was "
            "measured, so either restore the claim or re-measure and move both" % needle)
    assert "exactly the transparent one composited" not in text, (
        "the retracted equivalence claim is back in the help text; it was measured false "
        "(rim max 4.34/255 linear, 10.91 sRGB, background dithered over four values)")


def test_t99_the_log_line_says_which_film_was_used():
    """A replay that cannot tell which mode produced a PNG is a silent comparability hole."""
    assert "film {'opaque' if args.opaque else 'transparent'}" in SRC, (
        "the [turn] log line must record the film mode, or a recorded run cannot say "
        "which default it ran under")
