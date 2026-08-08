"""T27 - the packaging shape, pinned.

These ride the extraction commit (the tests-ride-the-commit law). They exist
because extraction introduced failure modes the repo did not previously have,
and every one of them fails at a USER's `npx` rather than in CI:

  * the same version is declared in FOUR places, and bin/facet.js pins an exact
    tag and asset name. Drift means npm-launcher fetches a release asset that
    does not exist and 404s on someone else's machine.
  * npm-launcher derives asset names from a LOCKED convention
    (<tool>-<version>-<os>-<arch>[.exe], and `win`, not `windows`). release.yml
    must emit exactly what the launcher asks for.

release.yml gates the version agreement too. This file is the hermetic half: it
fails in half a second locally instead of after a tag is already immutable.

Nothing here builds a wheel or a binary - those need network and a matrix, and
they are release.yml's job. These read declarations and assert they agree.
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


def _package_json():
    return json.loads(_read("package.json"))


def _launch_config():
    """The JSON.stringify({...}) object bin/facet.js hands to npm-launcher.

    Parsed rather than regex-scraped per key, so a malformed config fails here
    instead of yielding a plausible-looking partial match.
    """
    src = _read("bin/facet.js")
    m = re.search(r"JSON\.stringify\((\{.*?\})\)", src, re.S)
    assert m, "bin/facet.js does not hand a JSON.stringify({...}) config to the launcher"
    body = m.group(1)
    body = re.sub(r"(\w+):", r'"\1":', body)      # bare keys -> quoted
    body = re.sub(r",(\s*})", r"\1", body)         # trailing comma
    return json.loads(body)


def _server_version():
    m = re.search(r'^SERVER_VERSION = "([^"]+)"', _read("tools/record_mcp.py"), re.M)
    assert m, "record_mcp.py does not declare SERVER_VERSION"
    return m.group(1)


# ---------------------------------------------------------------------------


def test_t27_all_four_version_declarations_agree():
    """The load-bearing one. Four sites, one number."""
    versions = {
        "pyproject.toml": _pyproject()["project"]["version"],
        "package.json": _package_json()["version"],
        "bin/facet.js": _launch_config()["version"],
        "tools/record_mcp.py": _server_version(),
    }
    assert len(set(versions.values())) == 1, (
        "version drift across the four declarations: %s" % versions
    )


def test_t27_the_agreement_check_can_fail():
    """A check that cannot fail is not a check (this repo's own law).

    Proves the comparison above discriminates, rather than passing because every
    lookup happened to return the same accidental value.
    """
    drifted = {"a": "0.1.0", "b": "0.1.0", "c": "0.2.0"}
    assert len(set(drifted.values())) != 1


def test_t27_launcher_tag_is_v_plus_the_version():
    """npm-launcher defaults tag to v<version>, but bin/facet.js states it
    explicitly - so an explicit wrong value would silently win."""
    cfg = _launch_config()
    assert cfg["tag"] == "v" + cfg["version"]


def test_t27_launcher_points_at_this_repo():
    """owner/repo decide which GitHub Release the binary is fetched from."""
    cfg = _launch_config()
    assert cfg["owner"] == "mcp-tool-shop-org"
    assert cfg["repo"] == "facet"
    assert cfg["toolName"] == "facet"


def test_t27_wrapper_declares_the_launcher_as_a_dependency():
    """bin/facet.js requires @mcptoolshop/npm-launcher at run time; if it is not
    in dependencies, `npx` installs a package that cannot start."""
    deps = _package_json().get("dependencies", {})
    assert "@mcptoolshop/npm-launcher" in deps, (
        "package.json must depend on @mcptoolshop/npm-launcher; got %s" % sorted(deps)
    )
    assert "@mcptoolshop/npm-launcher" in _read("bin/facet.js")


def test_t27_release_workflow_emits_the_asset_names_the_launcher_asks_for():
    """npm-launcher's platform table is LOCKED: linux-x64 and win-x64 (the
    string is `win`, never `windows`), and checksums-<version>.txt. This is the
    exact pairing that 404s at a user's npx if release.yml drifts."""
    wf = _read(".github/workflows/release.yml")
    assert "label: linux-x64" in wf
    assert "label: win-x64" in wf
    assert "windows-x64" not in wf, "the launcher expects `win-x64`, not `windows-x64`"
    assert 'facet-${VERSION}-${{ matrix.label }}${{ matrix.ext }}' in wf
    assert 'checksums-${VERSION}.txt' in wf


@pytest.mark.parametrize("script,target", sorted(_pyproject()["project"]["scripts"].items()))
def test_t27_every_console_script_resolves_to_a_real_callable(script, target):
    """An entry point naming a function that does not exist installs fine and
    fails only when a user runs it. Import it here instead."""
    module_name, _, func_name = target.partition(":")
    module = __import__(module_name)
    fn = getattr(module, func_name, None)
    assert callable(fn), "%s -> %s is not callable" % (script, target)


def test_t27_py_modules_all_exist_in_the_package_dir():
    """package-dir + py-modules ships files, not a package. A typo here builds a
    wheel that is missing a module and only breaks on import."""
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
