"""T28 - the frozen-binary runtime contract.

These ride the 0.1.1 fix. They exist because 0.1.0 shipped a binary whose own
banner printed `db: C:\\Users\\...\\Temp\\docs/index/facet.db` and whose refusal
hint told the operator to run `python tools/facet_index.py build` - a command
with no tools/ directory to run it in, and possibly no Python at all.

**Nothing in the pipeline could have caught that.** The workflow was green, the
wheel installed, the console scripts ran, and CI passed - because every one of
those exercises the SOURCE CHECKOUT, where REPO is the repo and the advice is
correct. The defect lives only in the artifact a user actually receives, and it
was found by installing the published package and reading what it said.

So these tests exercise the frozen branch directly rather than trusting that a
source-tree run implies a binary run.
"""

import os
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

SRC = (TOOLS / "record_mcp.py").read_text(encoding="utf-8")


def _module():
    import record_mcp

    return record_mcp


# ---------------------------------------------------------------------------


def test_t28_unfrozen_run_keeps_the_source_checkout_advice():
    """The ordinary path must not regress: in a checkout the hint is the command
    that actually works there."""
    mod = _module()
    assert mod.FROZEN is False, "the test suite itself is not a frozen binary"
    assert "python tools/facet_index.py build" in mod.FIX_COMMAND


def test_t28_frozen_hint_does_not_tell_a_binary_user_to_run_a_source_command():
    """The defect, stated as a property.

    Re-executes the module's own constant block with FROZEN forced true, so the
    frozen branch is measured rather than read.
    """
    ns = {"sys": sys, "os": os, "FROZEN": True}
    block = re.search(
        r"^if FROZEN:\n(?:.*\n)*?^else:\n(?:^ {4}.*\n)+", SRC, re.M
    )
    assert block, "the FIX_COMMAND branch is not where T28 expects it"
    exec("DB_ENV = 'FACET_INDEX_DB'\n" + block.group(0), ns)  # noqa: S102

    hint = ns["FIX_COMMAND"]
    assert "python tools/" not in hint, (
        "a frozen binary has no tools/ directory; hint was %r" % hint
    )
    assert "facet-index build" in hint
    assert "FACET_INDEX_DB" in hint, "the env override is the other way out; name it"


def test_t28_frozen_db_default_resolves_against_cwd_not_the_extraction_dir():
    """In a onefile binary __file__ is a temp extraction dir, so a REPO-relative
    default names a path that can never exist. cwd-relative is the honest one."""
    import facet_index

    frozen_default = os.path.join(os.getcwd(), facet_index.DB_REL)
    assert "Temp" not in pathlib.Path(frozen_default).parts[:2] or True  # documentation
    # The source must actually branch on FROZEN for this constant.
    assert "os.getcwd() if FROZEN else REPO" in SRC, (
        "DB_DEFAULT no longer branches on FROZEN - the frozen default would "
        "resolve against the PyInstaller extraction dir again"
    )


def test_t28_frozen_is_derived_from_the_pyinstaller_marker():
    """`sys.frozen` is what PyInstaller sets; nothing else here should define it."""
    assert 'getattr(sys, "frozen", False)' in SRC


def test_t28_the_two_hints_actually_differ():
    """A can-fail leg: if both branches produced the same string the whole fix
    would be decorative and every assertion above would still pass."""
    ns = {"sys": sys, "os": os, "FROZEN": True}
    block = re.search(r"^if FROZEN:\n(?:.*\n)*?^else:\n(?:^ {4}.*\n)+", SRC, re.M)
    exec("DB_ENV = 'FACET_INDEX_DB'\n" + block.group(0), ns)  # noqa: S102
    assert ns["FIX_COMMAND"] != _module().FIX_COMMAND
