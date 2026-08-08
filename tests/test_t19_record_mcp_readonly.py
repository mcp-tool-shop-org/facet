"""T19 - record_mcp is read-only BY CONSTRUCTION, checked rather than promised.

Source: index-mcp-spec.md section 4.1 - "There is no write path to a markdown
file anywhere in the package, and that is a testable claim - an adoption test
that greps the built artifact for corpus write calls is cheap and belongs in
CI." Section 4.2 bounds the writes to exactly two paths (the DB and the
certificate sidecar).

The scan is an AST walk rather than a regex over the text, because a regex over
source cannot tell `open(p, "w")` from the word "w" in a docstring - and this
file is full of prose about writing.

BOTH DIRECTIONS ARE DEMONSTRATED. A guard that has only ever passed is a check
that cannot fail (the house law, and E16-9's method: the inverse guards were
proved by injecting a truncated list). Every assertion about the real source is
paired with the same scanner run over a synthetic source that violates it.
"""
import ast
import io

import pytest

from conftest import TOOLS

SOURCE = TOOLS / "record_mcp.py"

# Modes that mutate. `open(p)` with no mode is a read; anything carrying one of
# these characters can write.
WRITE_MODE_CHARS = set("wax+")

# Calls that move or destroy a file regardless of an open() mode, split by how
# safely the name alone identifies one.
#
# THE SPLIT IS A FIRST-RUN FINDING, not a design. The first version matched on
# the attribute NAME alone and flagged `os.path.relpath(...).replace("\\", "/")`
# in record_build - a str method, not os.replace. Matching a bare name is the
# proxy-instead-of-the-property error in miniature: `replace`, `remove`, `copy`
# and `mkdir` all exist on ordinary builtins, so the name is evidence only when
# the receiver is a filesystem module.
FS_RECEIVERS = {"os", "shutil", "pathlib", "Path", "path"}
AMBIGUOUS_ATTRS = {          # flagged only on a filesystem receiver
    "remove", "rename", "replace", "rmdir", "truncate", "copy", "copy2",
    "move", "mkdir",
}
UNAMBIGUOUS_ATTRS = {        # these exist on no builtin; always flagged
    "unlink", "removedirs", "copyfile", "copytree", "rmtree",
    "write_text", "write_bytes", "touch", "makedirs",
}
MUTATING_ATTRS = AMBIGUOUS_ATTRS | UNAMBIGUOUS_ATTRS

# The ONLY function permitted to write. The DB is written by facet_index.build,
# which this module calls but does not implement.
ALLOWED_WRITERS = {"write_certificate"}


def _enclosing(tree):
    """{node: enclosing function name} for every node under a FunctionDef."""
    owner = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for node in ast.walk(fn):
                owner.setdefault(node, fn.name)
    return owner


PATH_CTORS = {"Path", "PurePath", "PosixPath", "WindowsPath"}


def _receiver(attr_node):
    """The receiver of an attribute call, as a name, or None when it is the
    result of a call whose type is unknown.

    Walking THROUGH a call happens only for a pathlib constructor. The first
    cut walked through every call and so read
    `os.path.relpath(...).replace("\\\\", "/")` - a str method - as `os`
    mutating a file. Two false-positive shapes, one lesson: the receiver is
    evidence, and a call result is not a receiver.
    """
    cur = attr_node.value
    if isinstance(cur, ast.Call):
        f = cur.func
        name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", None)
        return "Path" if name in PATH_CTORS else None
    while isinstance(cur, ast.Attribute):
        cur = cur.value
    return cur.id if isinstance(cur, ast.Name) else None


def scan_writes(source):
    """Every file-mutating call site: [(function, what, lineno)].

    Module level counts as the function `<module>` - a write there is worse
    than one inside a tool, not better.

    BOUND, stated rather than implied: this is a source-level guard, so a Path
    bound to a variable and mutated through it (`p = Path(x); p.rename(y)`)
    would pass. The guard's complement is the two properties it cannot be
    fooled about - the only sqlite handle in the module is `mode=ro`, and the
    corpus is only ever reached through facet_index's read helpers.
    """
    tree = ast.parse(source)
    owner = _enclosing(tree)
    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        where = owner.get(node, "<module>")
        fn = node.func
        if isinstance(fn, ast.Name) and fn.id == "open":
            mode = ""
            if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                mode = str(node.args[1].value)
            for kw in node.keywords:
                if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                    mode = str(kw.value.value)
            if set(mode) & WRITE_MODE_CHARS:
                hits.append((where, "open(mode=%r)" % mode, node.lineno))
        elif isinstance(fn, ast.Attribute) and fn.attr in MUTATING_ATTRS:
            if (fn.attr in UNAMBIGUOUS_ATTRS
                    or _receiver(fn) in FS_RECEIVERS):
                hits.append((where, "%s(...)" % fn.attr, node.lineno))
    return hits


def scan_sqlite_connects(source):
    tree = ast.parse(source)
    owner = _enclosing(tree)
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "connect"):
            out.append((owner.get(node, "<module>"), node.lineno))
    return out


@pytest.fixture(scope="module")
def source():
    with io.open(str(SOURCE), encoding="ascii") as fh:
        return fh.read()


def test_t19_source_is_ascii():
    """Section 8: ASCII on every print path. Enforced at the byte level here,
    because the tool's own prose is one of the print paths - E16-1's crash was
    a single `up-arrow` literal killing a verify that had already passed two
    legs."""
    with io.open(str(SOURCE), "rb") as fh:
        raw = fh.read()
    try:
        raw.decode("ascii")
    except UnicodeDecodeError as exc:
        pytest.fail("record_mcp.py is not ASCII at byte %d: %r"
                    % (exc.start, raw[max(0, exc.start - 40):exc.start + 40]))


def test_t19_only_the_certificate_writer_writes(source):
    hits = scan_writes(source)
    bad = [h for h in hits if h[0] not in ALLOWED_WRITERS]
    assert not bad, (
        "record_mcp.py mutates files outside %s:\n  %s"
        % (sorted(ALLOWED_WRITERS),
           "\n  ".join("%s:%d in %s -> %s" % (SOURCE.name, ln, fn, what)
                       for fn, what, ln in bad)))
    # and the permitted writer is actually there - an empty scan would pass the
    # assertion above while proving nothing
    assert any(h[0] == "write_certificate" for h in hits), (
        "no write call found at all; the scanner is not looking at what it "
        "thinks it is looking at")


def test_t19_the_scanner_catches_a_corpus_write():
    """The can-fail proof. Same scanner, a source that violates the property."""
    guilty = (
        "def record_query(q):\n"
        "    with open('CLAUDE.md', 'w') as fh:\n"
        "        fh.write('fixed the heading')\n"
        "    return {}\n")
    hits = scan_writes(guilty)
    assert hits and hits[0][0] == "record_query", hits
    assert [h for h in hits if h[0] not in ALLOWED_WRITERS], (
        "the guard would have accepted a corpus write inside a query tool")

    for snippet, needle in (
            ("import os\ndef record_get(a):\n    os.remove(a)\n", "remove"),
            ("import os\ndef f(a, b):\n    os.replace(a, b)\n", "replace"),
            ("import shutil\ndef f(a, b):\n    shutil.copyfile(a, b)\n", "copyfile"),
            ("import shutil\ndef f(a):\n    shutil.rmtree(a)\n", "rmtree"),
            ("from pathlib import Path\n"
             "def g(p):\n    Path(p).write_text('x')\n", "write_text"),
            ("import pathlib\n"
             "def g(p, q):\n    pathlib.Path(p).rename(q)\n", "rename"),
            ("def h(p):\n    p.unlink()\n", "unlink")):
        hits = scan_writes(snippet)
        assert any(needle in h[1] for h in hits), (
            "the scanner missed %s in:\n%s" % (needle, snippet))


def test_t19_the_scanner_does_not_fire_on_ordinary_builtins():
    """The other half of the first-run finding. A guard that flags
    `"a/b".replace("/", "\\\\")` teaches its readers to ignore it, and a guard
    people ignore is not a guard."""
    innocent = (
        "import os\n"
        "def record_build(p, root):\n"
        "    q = p.replace('\\\\', '/')\n"
        "    r = os.path.relpath(p, root).replace('\\\\', '/')\n"
        "    seen = ['a']\n"
        "    seen.remove('a')\n"
        "    d = {}.copy()\n"
        "    return q, r, seen, d\n")
    assert scan_writes(innocent) == [], scan_writes(innocent)


def test_t19_every_sqlite_handle_is_read_only(source):
    sites = scan_sqlite_connects(source)
    assert sites, "no sqlite3.connect found; the scanner is looking at nothing"
    outside = [s for s in sites if s[0] != "_ro_con"]
    assert not outside, (
        "sqlite3.connect outside the read-only helper at line(s) %s - a "
        "read-write handle makes read-only a policy instead of a property"
        % [ln for _, ln in outside])
    tree = ast.parse(source)
    body = [n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name == "_ro_con"]
    assert len(body) == 1
    text = ast.unparse(body[0])
    assert "mode=ro" in text, "_ro_con does not open the DB read-only:\n%s" % text
    assert "uri=True" in text, "_ro_con does not enable URI mode:\n%s" % text


def test_t19_read_only_handle_actually_refuses_a_write(tmp_path):
    """Not just the literal - the handle. Proves `mode=ro` reaches sqlite."""
    import sqlite3
    import sys

    sys.path.insert(0, str(TOOLS))
    import record_mcp

    db = tmp_path / "tiny.db"
    con = sqlite3.connect(str(db))
    con.execute("CREATE TABLE t (a TEXT)")
    con.commit()
    con.close()

    ro = record_mcp._ro_con(str(db))
    try:
        assert ro.execute("SELECT COUNT(*) FROM t").fetchone()[0] == 0
        with pytest.raises(sqlite3.OperationalError) as exc:
            ro.execute("INSERT INTO t VALUES ('x')")
        assert "readonly" in str(exc.value).lower(), str(exc.value)
    finally:
        ro.close()
