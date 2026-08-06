"""Find every argparse help string this repo cannot print. E12 Ruling 4b's consumer grep.

THE DEFECT. `argparse` expands a help string with `help % params` where `params` is a
DICT, so a literal `%` in help text is read as a conversion specifier. `4.68% on` becomes
`% o` -> "%o format: an integer is required, not dict"; `within 1%.` becomes `%.` ->
"unsupported format character"; `0.18% against` becomes `% a` -> "not enough arguments for
format string". The tool then exits 1 and prints a traceback instead of its flags. Four
sites were found by hand on two route-active tools (project_twins, turn_render); a root
cause has as many sites as it has callers, so this finds the rest by construction.

WHY STATIC, AND WHY THAT IS NOT A PROXY HERE. Running `--help` is the ground truth, but it
costs a torch/open3d/bpy import per tool and cannot run Blender scripts and plain ones the
same way. The failure is decided ENTIRELY by the help string's own text, so this parses
each file with `ast` (which handles implicit multi-line concatenation natively, where a
regex does not) and applies argparse's own operation - `s % dict` - to each literal. Same
operation, same operand type, same exception. Non-literal help (an f-string, a variable) is
reported separately as UNTESTABLE rather than silently passed.

WHAT IS LEGITIMATE, stated exactly, because the first version of this scanner got it wrong
and flagged correct code. Only two `%` uses are valid in an argparse help string: `%%` (a
literal percent) and `%(name)s` (a lookup into the action's own dict, e.g. `%(default)s`).
**Every other `%` is the defect**, and the scan walks the string rather than diffing the
formatted output - a diff marks correctly-escaped `%%` as changed, which is how the first
pass produced eight false positives against four real ones.

A SECOND CLASS, found by the verification step rather than by the scan, and now gated here
too. With every `%` escaped, `project_twins.py --help` STILL exited 1: its help text carries
`⚠`, and Windows writes the console in cp1252, so `file.write(message)` raises
UnicodeEncodeError before a single flag prints. That is CLAUDE.md's standing "prints are
ASCII-only" rule, violated in help text. Note the boundary precisely, because it decides the
blast radius: an em dash (U+2014, 28 sites here) and a section sign (U+00A7) ARE cp1252
characters and print fine; only characters outside cp1252 break. Reported as UNPRINTABLE.

TWO SEVERITIES, because the same defect fails two ways:
  * FAILS   - `s % params` raises. `--help` exits 1 with a traceback and prints no flags.
  * SILENT  - it does NOT raise, because the offending `%` happens to form a valid
              conversion (`% a` is a space-flagged `%a`) and Python hands the whole params
              DICT to it. argparse's params is `dict(vars(action), prog=...)`, so the help
              text prints with the action's entire internal state spliced into it. Worse
              than the crash: nothing announces it.

  e12_help_format_scan.py [--root tools] [--json out.json]

Standards compliance: ANDON_AUTHORITY - exits 1 when any FAILS site remains, so it can gate
a commit rather than merely inform one. EXTERNAL_VERIFIER - it reports sites; it changes no
file and judges no fix. NAMED_COMPENSATORS - read-only apart from an optional JSON.
"""
import argparse
import ast
import json
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--root", default="tools", help="directory tree to scan")
ap.add_argument("--json", default=None)
ap.add_argument("--quiet", action="store_true", help="print only the failing sites")
args = ap.parse_args()

# argparse formats with the action's __dict__ plus prog; a mapping that answers every key
# reproduces %(default)s-style substitution without needing a real parser.
class _Params(dict):
    def __missing__(self, k):
        return "<%s>" % k


def bad_percents(s):
    """Offsets of every `%` that is neither `%%` nor a `%(name)s` mapping conversion."""
    out = []
    i = 0
    while i < len(s):
        if s[i] != "%":
            i += 1
            continue
        if i + 1 < len(s) and s[i + 1] == "%":
            i += 2
            continue
        if i + 1 < len(s) and s[i + 1] == "(" and ")" in s[i:]:
            i = s.index(")", i) + 1
            # skip flags/width/precision to the conversion character
            while i < len(s) and s[i] in "#0- +.0123456789hlL":
                i += 1
            i += 1
            continue
        out.append(i)
        i += 1
    return out


def literal(node):
    """The help= value if it is a string literal (including implicit concatenation)."""
    try:
        v = ast.literal_eval(node)
    except Exception:
        return None
    return v if isinstance(v, str) else None


rows = []
for dirpath, _dirs, files in os.walk(args.root):
    if os.path.basename(dirpath) == "__pycache__":
        continue
    for fn in sorted(files):
        if not fn.endswith(".py"):
            continue
        path = os.path.join(dirpath, fn)
        try:
            tree = ast.parse(open(path, encoding="utf-8").read())
        except SyntaxError as e:
            rows.append({"file": path, "line": e.lineno, "status": "UNPARSEABLE",
                         "detail": str(e)})
            continue
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "add_argument"):
                continue
            flag = None
            for a in node.args:
                s = literal(a)
                if s and s.startswith("-"):
                    flag = s
                    break
            for kw in node.keywords:
                if kw.arg != "help":
                    continue
                s = literal(kw.value)
                if s is None:
                    rows.append({"file": path, "line": kw.value.lineno, "flag": flag,
                                 "status": "UNTESTABLE",
                                 "detail": "help= is not a string literal"})
                    break
                unprintable = []
                for c in sorted({ch for ch in s if ord(ch) > 127}):
                    try:
                        c.encode("cp1252")
                    except Exception:
                        unprintable.append(c)
                if unprintable:
                    i = s.index(unprintable[0])
                    rows.append({"file": path, "line": kw.value.lineno, "flag": flag,
                                 "status": "UNPRINTABLE",
                                 "detail": "help carries %s, outside cp1252: the console "
                                           "write raises before any flag prints"
                                           % " ".join("U+%04X" % ord(c) for c in unprintable),
                                 "near": s[max(0, i - 50):i + 50].encode(
                                     "ascii", "replace").decode("ascii")})
                bad = bad_percents(s)
                if not bad:
                    break
                try:
                    s % _Params()
                    status, detail = "SILENT", ("does not raise; the params DICT is "
                                                "spliced into the printed help")
                except Exception as e:
                    status, detail = "FAILS", "%s: %s" % (type(e).__name__, e)
                i = bad[0]
                rows.append({"file": path, "line": kw.value.lineno, "flag": flag,
                             "status": status, "detail": detail,
                             "bad_percents": len(bad),
                             "near": s[max(0, i - 55):i + 55]})
                break

fails = [r for r in rows if r["status"] == "FAILS"]
silent = [r for r in rows if r["status"] == "SILENT"]
unprint = [r for r in rows if r["status"] == "UNPRINTABLE"]
other = [r for r in rows if r["status"] in ("UNTESTABLE", "UNPARSEABLE")]
for group, label in ((fails, "FAILS       (--help exits 1 on the %-format)"),
                     (unprint, "UNPRINTABLE (--help exits 1 on the console encoding)"),
                     (silent, "SILENT      (params dict spliced into the help text)"),
                     (other, "OTHER")):
    if args.quiet and not (label.startswith("FAILS") or label.startswith("UNPRINTABLE")):
        continue
    print("\n=== %s: %d ===" % (label, len(group)))
    for r in group:
        print("  %s:%s  %s  [%s bad %%]  %s"
              % (r["file"], r["line"], r.get("flag") or "?",
                 r.get("bad_percents", "?"), r["detail"]))
        if r.get("near"):
            print("      ...%s..." % r["near"].replace("\n", " "))

print("\nscanned root %s | FAILS %d | UNPRINTABLE %d | SILENT %d | UNTESTABLE/UNPARSEABLE %d"
      % (os.path.abspath(args.root), len(fails), len(unprint), len(silent), len(other)))
if args.json:
    os.makedirs(os.path.dirname(os.path.abspath(args.json)) or ".", exist_ok=True)
    json.dump(rows, open(args.json, "w"), indent=1)
    print("wrote %s" % os.path.abspath(args.json))
sys.exit(1 if (fails or unprint) else 0)
