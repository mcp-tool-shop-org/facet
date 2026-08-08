"""T27 - the packaging shape, pinned.

These ride the extraction commit (the tests-ride-the-commit law). They exist
because extraction introduced a failure mode the repo did not previously have:
**the same version is now declared in four places, and bin/facet.js installs an
EXACT pinned version from PyPI.** If the wrapper's pin drifts from what the
Python package publishes, `npx @mcptoolshop/facet` fetches a version that does
not exist and fails at the user's hands rather than in CI.

release.yml gates the same agreement before publishing. This file is the
hermetic half: it fails in 0.1s on a developer's machine instead of after a tag
is already immutable.

Nothing here builds a wheel - that is release.yml's job and it needs network.
These read declarations and assert they agree.
"""

import json
import pathlib
import re
import sys

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]
TOOLS = REPO / "tools"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def _read(rel):
    return (REPO / rel).read_text(encoding="utf-8")


def _pyproject():
    # tomllib is stdlib on the pinned 3.11+ interpreter; no new dependency.
    import tomllib

    return tomllib.loads(_read("pyproject.toml"))


def _bin_js_const(name):
    m = re.search(r'const %s = "([^"]+)"' % name, _read("bin/facet.js"))
    assert m, "bin/facet.js does not declare a %s constant" % name
    return m.group(1)


def _server_version():
    m = re.search(r'^SERVER_VERSION = "([^"]+)"', _read("tools/record_mcp.py"), re.M)
    assert m, "record_mcp.py does not declare SERVER_VERSION"
    return m.group(1)


# ---------------------------------------------------------------------------


def test_t27_all_four_version_declarations_agree():
    """The load-bearing one. Four sites, one number."""
    versions = {
        "pyproject.toml": _pyproject()["project"]["version"],
        "package.json": json.loads(_read("package.json"))["version"],
        "bin/facet.js": _bin_js_const("VERSION"),
        "tools/record_mcp.py": _server_version(),
    }
    assert len(set(versions.values())) == 1, (
        "version drift across the four declarations: %s" % versions
    )


def test_t27_the_agreement_check_can_fail():
    """A check that cannot fail is not a check (this repo's own law).

    Proves the comparison above actually discriminates, rather than passing
    because every lookup happened to return the same accidental value.
    """
    drifted = {"a": "0.1.0", "b": "0.1.0", "c": "0.2.0"}
    assert len(set(drifted.values())) != 1


def test_t27_wrapper_pins_the_package_pyproject_publishes():
    """bin/facet.js installs a package NAME too, not only a version."""
    assert _bin_js_const("PKG") == _pyproject()["project"]["name"] == "facet-mcp"


def test_t27_wrapper_execs_a_console_script_that_pyproject_declares():
    """The wrapper runs ENTRY from the venv; pyproject must actually create it."""
    entry = _bin_js_const("ENTRY")
    assert entry in _pyproject()["project"]["scripts"], (
        "bin/facet.js execs %r but pyproject declares %s"
        % (entry, sorted(_pyproject()["project"]["scripts"]))
    )


@pytest.mark.parametrize("script,target", sorted(_pyproject()["project"]["scripts"].items()))
def test_t27_every_console_script_resolves_to_a_real_callable(script, target):
    """An entry point naming a function that does not exist installs fine and
    fails only when a user runs it. Import it here instead."""
    module_name, _, func_name = target.partition(":")
    module = __import__(module_name)
    fn = getattr(module, func_name, None)
    assert callable(fn), "%s -> %s is not callable" % (script, target)


def test_t27_py_modules_all_exist_in_the_package_dir():
    """package-dir + py-modules ships files, not a package. A typo here builds
    a wheel that is missing a module and only breaks on import."""
    cfg = _pyproject()["tool"]["setuptools"]
    where = REPO / cfg["package-dir"][""]
    for mod in cfg["py-modules"]:
        assert (where / (mod + ".py")).is_file(), "%s.py not found under %s" % (mod, where)


def test_t27_wrapper_source_is_ascii():
    """Same law as the rest of the tree: a non-ASCII byte in a file that gets
    retyped through a shell is how a defect arrives invisibly."""
    raw = (REPO / "bin" / "facet.js").read_bytes()
    bad = [(i, b) for i, b in enumerate(raw) if b > 0x7F]
    assert not bad, "non-ASCII bytes in bin/facet.js at offsets %s" % [i for i, _ in bad[:5]]


def test_t27_release_workflow_filename_is_the_one_both_publishers_are_bound_to():
    """PyPI's pending publisher and npm's trusted publisher are both configured
    against the literal filename release.yml. Renaming it silently breaks BOTH
    OIDC handshakes, and npm masks that as a 404 rather than an auth error."""
    assert (REPO / ".github" / "workflows" / "release.yml").is_file()
