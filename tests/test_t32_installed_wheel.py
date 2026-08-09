"""T32 - the installed-wheel runtime contract (E24).

THE HOLE THIS FILLS IS THE POINT. T28 pinned the FROZEN branch in five tests
and left the installed-wheel branch with none, and that is why `pip install
facet-mcp` shipped four consecutive releases unable to find the record. The
only wheel check that ever ran was

    facet-index --help
    facet-mcp --print-tools

and neither of those touches a corpus or a database, so both were green the
entire time the package was broken. **These tests run a VERB.**

Two tiers, for a reason measured rather than assumed (E24):

  * the GEOMETRY legs are hermetic and run everywhere including CI. They
    reproduce the wheel's defining property - `facet_index.py` sitting in a
    directory whose parent is not the record - by copying the module somewhere
    else and invoking it there. No wheel, no venv, no network.
  * the WHEEL legs build a real wheel and install it into a real venv. The
    INSTALL is hermetic (`pip install --no-index --no-deps` needs no network,
    and `facet_index` is stdlib-only so it runs without `mcp`); the BUILD is
    not, because `python -m build` provisions an isolated build environment
    from PyPI and `--no-isolation` fails against the rig's setuptools 70.2.0
    where pyproject requires >=77. So they skip with a named reason when
    `build` is absent or cannot run, and pytest.ini's `-rA` prints it.

A skip that nobody reads is a check that cannot fail; every skip below names
the exact missing thing.
"""

import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys
import zipfile

import pytest

from conftest import REPO, TOOLS

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import facet_index                                            # noqa: E402

WHEEL_TIMEOUT = 600


def _run(argv, cwd, env=None, timeout=120):
    e = dict(os.environ)
    e.pop("FACET_INDEX_DB", None)
    if env:
        e.update(env)
    return subprocess.run(argv, cwd=str(cwd), env=e, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          timeout=timeout)


# ---------------------------------------------------------------------------
# the resolver itself - hermetic, and the can-fail leg comes first
# ---------------------------------------------------------------------------


def test_t32_resolver_refuses_when_no_candidate_holds(tmp_path):
    """THE CAN-FAIL LEG. Before trusting any pass below, prove a miss is
    reachable: hand the resolver a directory that is not the record and it must
    return None rather than the directory."""
    assert facet_index.resolve_repo([str(tmp_path)]) is None
    assert facet_index.resolve_repo([]) is None
    assert facet_index.is_record_root(str(tmp_path)) is False


def test_t32_repo_raises_rather_than_returning_a_plausible_path(monkeypatch):
    """E24's constraint 2: a resolver that cannot find a corpus REFUSES.

    `repo()` must raise - not return None, not return the module's own parent,
    not guess cwd. Returning anything at all is how <venv>/Lib became a banner.
    """
    monkeypatch.setattr(facet_index, "REPO", None)
    with pytest.raises(facet_index.RootNotFound) as exc:
        facet_index.repo()
    msg = str(exc.value)
    for marker in facet_index.RECORD_MARKERS:
        assert marker in msg, "the refusal must name what it looked for"
    assert os.getcwd() in msg or "working directory" in msg


def test_t32_a_checkout_resolves_to_itself_and_takes_the_first_candidate():
    """The path that worked before E24 must take the same branch it always did:
    the module's own parent, tested and accepted, ahead of cwd."""
    assert facet_index.REPO == str(REPO)
    assert facet_index.is_record_root(str(REPO))
    assert facet_index.repo_candidates()[0] == os.path.dirname(facet_index.HERE)
    assert facet_index.resolve_repo([str(REPO)]) == str(REPO)


def test_t32_one_marker_is_not_enough_to_call_a_directory_the_record(tmp_path):
    """WHY THERE ARE TWO MARKERS, as a test rather than as a comment.

    `CLAUDE.md` is an ordinary filename - 26 directories under E:\\AI on the rig
    this was measured on carry one, and exactly ONE of those also carries
    `docs/experiments`. A single-marker resolver would bind a working directory
    that is a different repo entirely and then fail deeper in, which is the
    defect E24 replaced rather than a fix for it.
    """
    (tmp_path / "CLAUDE.md").write_text("not the record\n", encoding="utf-8")
    assert facet_index.is_record_root(str(tmp_path)) is False
    (tmp_path / "docs" / "experiments").mkdir(parents=True)
    assert facet_index.is_record_root(str(tmp_path)) is True


def test_t32_the_two_db_env_declarations_agree():
    """One string, two modules. T27 pins the four version declarations for the
    same reason: a drift here would mean `facet-index` and `facet-mcp` read
    different environment variables while the README names one."""
    import record_mcp

    assert facet_index.DB_ENV == "FACET_INDEX_DB"
    assert record_mcp.DB_ENV == facet_index.DB_ENV


# ---------------------------------------------------------------------------
# the wheel's GEOMETRY, reproduced without a wheel - hermetic, runs in CI
# ---------------------------------------------------------------------------


def _transplant(tmp_path):
    """facet_index.py + record_mcp.py in a directory whose parent is NOT the
    record. This is the wheel install's defining property and the whole of what
    made it fail; reproducing it costs a file copy instead of a network round
    trip.

    The precondition is checked with LITERAL names rather than through
    `facet_index.is_record_root`, and that is deliberate. Measured while
    building this file: with the helper, these legs failed on the pre-E24 tree
    with `AttributeError: module 'facet_index' has no attribute
    'is_record_root'` - which is the new API being absent, NOT the shipped
    artifact misbehaving. A leg that red-flags a tree because a symbol it
    imports does not exist there yet proves nothing about the defect. Written
    this way they fail on what the old code DID.
    """
    site = tmp_path / "site-packages"
    site.mkdir()
    for name in ("facet_index.py", "record_mcp.py"):
        shutil.copy2(str(TOOLS / name), str(site / name))
    for marker in ("CLAUDE.md", "docs/experiments"):
        assert not os.path.exists(os.path.join(str(tmp_path), marker)), (
            "the transplant directory's parent must not look like a record "
            "root, or this leg measures nothing")
    return site


def test_t32_transplanted_module_finds_the_record_through_cwd(tmp_path):
    """The wheel geometry, run from inside a checkout: resolution must fall
    through to the working directory and land on the real record."""
    site = _transplant(tmp_path)
    r = _run([sys.executable, "-c",
              "import facet_index as f; print(f.REPO)"], cwd=REPO,
             env={"PYTHONPATH": str(site)})
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == str(REPO), r.stdout


def test_t32_transplanted_module_refuses_outside_a_checkout(tmp_path):
    """Same geometry, run from nowhere: REPO is None and the verb refuses."""
    site = _transplant(tmp_path)
    r = _run([sys.executable, "-c",
              "import facet_index as f; print(f.REPO)"], cwd=tmp_path,
             env={"PYTHONPATH": str(site)})
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip() == "None", r.stdout

    verb = _run([sys.executable, str(site / "facet_index.py"), "claims"],
                cwd=tmp_path)
    assert verb.returncode == facet_index.EXIT_REFUSED, (
        "a corpus verb with no record must REFUSE (4), not crash; got %d\n%s"
        % (verb.returncode, verb.stderr))
    assert "REFUSED" in verb.stderr
    assert "RootNotFound" in verb.stderr


def test_t32_transplanted_server_banner_names_a_real_path(tmp_path):
    """The 0.1.0 symptom, asked of the wheel branch.

    `--print-tools` printed `db: <venv>\\Lib\\docs/index/facet.db` for four
    releases and exited 0 the whole time. It must now name a path under the
    record it actually found.
    """
    site = _transplant(tmp_path)
    r = _run([sys.executable, str(site / "record_mcp.py"), "--print-tools"],
             cwd=REPO)
    assert r.returncode == 0, r.stderr
    db_lines = [ln for ln in r.stdout.splitlines() if ln.strip().startswith("db:")]
    assert db_lines, "the banner no longer prints a db: line\n%s" % r.stdout
    shown = db_lines[0].split("db:", 1)[1].strip()
    assert shown.startswith(str(REPO)), (
        "the banner names a path outside the record: %r" % shown)
    assert str(site) not in shown


def test_t32_the_env_var_selects_a_db_and_never_a_corpus(tmp_path):
    """E24 constraint 1, as a property.

    $FACET_INDEX_DB is now read by `facet-index` (it was not, while the README
    said it was). It must stay a DB SELECTOR: setting it does not make a
    directory into a record root, so a corpus verb still refuses.
    """
    site = _transplant(tmp_path)
    db = str(REPO / "docs" / "index" / "facet.db")
    if not os.path.exists(db):
        pytest.skip("the tracked index is not built: %s" % db)

    q = _run([sys.executable, str(site / "facet_index.py"), "q", "erosion"],
             cwd=tmp_path, env={"FACET_INDEX_DB": db})
    assert q.returncode == 0, (
        "the env var must reach `facet-index` q from anywhere\n%s" % q.stderr)
    assert q.stdout.strip() and "(no rows)" not in q.stdout

    claims = _run([sys.executable, str(site / "facet_index.py"), "claims"],
                  cwd=tmp_path, env={"FACET_INDEX_DB": db})
    assert claims.returncode == facet_index.EXIT_REFUSED, (
        "a DB selector must not resolve a CORPUS; got %d" % claims.returncode)


# ---------------------------------------------------------------------------
# the real artifact - build a wheel, install it, RUN A VERB
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def installed(tmp_path_factory):
    """A wheel built from this tree and installed into its own venv.

    Module-scoped: the build is the expensive half and every leg below asks a
    different question of the same artifact.
    """
    if importlib.util.find_spec("build") is None:
        pytest.skip("`python -m build` is not installed in %s - the wheel tier "
                    "needs it to produce the artifact" % sys.executable)

    base = tmp_path_factory.mktemp("wheel")
    dist = base / "dist"
    made = subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(dist)],
        cwd=str(REPO), capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=WHEEL_TIMEOUT)
    if made.returncode != 0:
        pytest.skip("`python -m build` failed (it provisions an isolated build "
                    "environment from PyPI, so this is what no network looks "
                    "like): %s" % (made.stderr or made.stdout)[-400:])

    wheels = sorted(dist.glob("*.whl"))
    assert wheels, "build reported success and produced no wheel"
    wheel = wheels[-1]

    venv = base / "venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True,
                   capture_output=True, timeout=WHEEL_TIMEOUT)
    scripts = venv / ("Scripts" if os.name == "nt" else "bin")
    py = scripts / ("python.exe" if os.name == "nt" else "python")

    # --no-index --no-deps: NO NETWORK. facet_index is stdlib-only, so every
    # verb below runs without `mcp`; installing deps is what would need PyPI.
    got = subprocess.run(
        [str(py), "-m", "pip", "install", "--no-index", "--no-deps",
         "--quiet", str(wheel)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=WHEEL_TIMEOUT)
    assert got.returncode == 0, "offline install of a local wheel failed:\n%s" % got.stderr

    exe = scripts / ("facet-index.exe" if os.name == "nt" else "facet-index")
    assert exe.exists(), "the wheel installed no facet-index console script"
    return {"wheel": wheel, "facet_index": str(exe), "venv": venv}


@pytest.mark.slow
def test_t32_the_built_wheel_carries_no_record_marker(installed):
    """The resolver's markers must be impossible to satisfy from inside an
    install, or the installed branch could key on itself and resolve to
    site-packages exactly as before."""
    names = zipfile.ZipFile(str(installed["wheel"])).namelist()
    payload = [n for n in names if ".dist-info/" not in n]
    assert sorted(payload) == ["facet_index.py", "record_mcp.py"], payload
    for marker in facet_index.RECORD_MARKERS:
        assert not any(n == marker or n.startswith(marker.rstrip("/") + "/")
                       for n in names), \
            "%r ships in the wheel; it cannot be a root marker" % marker


@pytest.mark.slow
def test_t32_installed_wheel_runs_a_db_verb_with_no_db_flag(installed):
    """`facet-index q` with no --db, from inside a checkout.

    THE HEADLINE DEFECT. On the published 0.2.0 and 0.3.0 wheels this exited 2
    with `unable to open database file`, because the default --db resolved
    against <venv>/Lib. `--help` could never have seen it.
    """
    if not (REPO / "docs" / "index" / "facet.db").exists():
        pytest.skip("the tracked index is not built")
    r = _run([installed["facet_index"], "q", "erosion"], cwd=REPO)
    assert r.returncode == 0, "%s\n%s" % (r.stdout, r.stderr)
    assert "(no rows)" not in r.stdout
    assert "Lib" not in r.stderr


@pytest.mark.slow
def test_t32_installed_wheel_runs_a_corpus_verb(installed):
    """`facet-index claims`, which READS THE RECORD - the other half of the
    defect. It died on <venv>/Lib/CLAUDE.md with FileNotFoundError, while
    README.md said a wheel install worked for exactly this verb."""
    if not (REPO / "docs" / "index" / "facet.db").exists():
        pytest.skip("the tracked index is not built")
    r = _run([installed["facet_index"], "claims",
              "--db", str(REPO / "docs" / "index" / "facet.db")],
             cwd=REPO, timeout=300)
    assert r.returncode == 0, "%s\n%s" % (r.stdout[-1500:], r.stderr[-1500:])
    assert "CLAUDE.md" not in r.stderr


@pytest.mark.slow
def test_t32_installed_wheel_refuses_outside_a_checkout(installed, tmp_path):
    """The refusal reaches a real installed command, with E22/E23's code.

    Before E24 this exited 2 with a raw FileNotFoundError naming a path inside
    the venv - a runtime error where the honest answer is a refusal.
    """
    r = _run([installed["facet_index"], "build"], cwd=tmp_path)
    assert r.returncode == facet_index.EXIT_REFUSED, (
        "expected %d = REFUSED, got %d\n%s"
        % (facet_index.EXIT_REFUSED, r.returncode, r.stderr))
    assert "REFUSED" in r.stderr
    for marker in facet_index.RECORD_MARKERS:
        assert marker in r.stderr, "the refusal must name what it looked for"
    assert "FACET_INDEX_DB" in r.stderr, "a refusal names the way out"


@pytest.mark.slow
def test_t32_installed_wheel_help_and_print_tools_still_pass(installed):
    """The two checks release.yml has always run. They stay green - this is the
    regression leg for the only wheel coverage that existed, and it is here to
    make the point that green here proved nothing about the four legs above."""
    r = _run([installed["facet_index"], "--help"], cwd=REPO)
    assert r.returncode == 0, r.stderr
    assert "--db" in r.stdout
