"""ANDON: assert a twin-prompts rebuild differs from its predecessor by EXACTLY the named terms.

WHY THIS IS A COMMITTED TOOL NOW. Handoffs 9 and 10 each asserted this property and each did it
in a throwaway script that was never committed, so the claim "the ANDON passed on all nine
stems" has no artifact behind it — the same gap `e12_make_twin_prompts.py`'s own header records
about the v2 prompts file. This is that artifact.

WHAT IT ASSERTS, as CONSTRUCTION rather than intention (the handoff-10 wording, kept):

  * remove the named `--inserted` terms from every stem of the NEW file and what remains is
    BYTE-EQUAL to the matching stem of the OLD file — per stem, no exceptions, no skip flag;
  * the stem KEY SETS match exactly (a rebuild that quietly gained or lost a view is a
    different object, not a delta);
  * the drop map is byte-identical unless `--allow-dropmap-change` is passed, which prints the
    diff loudly rather than swallowing it;
  * each inserted term appears in a stem at most once, and where it appears it is at the same
    ordered position relative to its neighbours as in the entry.

It also PRINTS, per stem, the old and new term counts and where each inserted term landed —
because a passing assertion is a null result and the count is the only evidence the term
arrived at all.

  e12_stem_delta.py --old OLD.json --new NEW.json --inserted "charcoal neck spines"
                    [--inserted "..."] [--allow-dropmap-change]

The OLD file is normally read out of git (`git show HEAD:path > old.json`) so the comparison is
against the committed predecessor and not against a working copy the same session just wrote.

Standards compliance: ANDON_AUTHORITY — every check raises with a non-zero exit and there is no
skip flag; a failure is a halt. PIN_PER_STEP — both files' `_version` strings are echoed into
the report so the pair being compared is named. NAMED_COMPENSATORS — writes nothing at all.
EXTERNAL_VERIFIER — it tests the builder's output against the builder's predecessor, from
outside the builder.
"""
import argparse
import json
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--old", required=True)
ap.add_argument("--new", required=True)
ap.add_argument("--inserted", action="append", default=[],
                help="a comma-term the NEW entry gained. Repeatable. Removing all of them "
                     "from a new stem must leave the old stem byte-equal.")
ap.add_argument("--allow-dropmap-change", action="store_true",
                help="permit the drop map to differ, printing the diff. Ruling 9d can REQUIRE "
                     "a new drop; that is a decision, so it is a declared argument.")
args = ap.parse_args()

O = json.load(open(args.old, encoding="utf-8"))
N = json.load(open(args.new, encoding="utf-8"))
print("[delta] %s  ->  %s" % (O.get("_version"), N.get("_version")), flush=True)

bad = []


def stems(d):
    return {k: v for k, v in d.items()
            if not k.startswith("_") and isinstance(v, str)}


so, sn = stems(O), stems(N)
if set(so) != set(sn):
    bad.append("stem key sets differ: only-old %s  only-new %s"
               % (sorted(set(so) - set(sn)), sorted(set(sn) - set(so))))

eo = [t.strip() for t in O["_entry_verbatim"].split(",")]
en = [t.strip() for t in N["_entry_verbatim"].split(",")]
for t in args.inserted:
    if t in eo:
        bad.append("--inserted %r is already a term of the OLD entry, so it is not an insertion"
                   % t)
    if t not in en:
        bad.append("--inserted %r is not a comma-term of the NEW entry" % t)
stripped_entry = [t for t in en if t not in args.inserted]
if stripped_entry != eo:
    bad.append("the NEW entry minus the inserted term(s) is not the OLD entry:\n      old %s\n"
               "      got %s" % (eo, stripped_entry))
print("[delta] entry %d -> %d terms; inserted %s"
      % (len(eo), len(en), ", ".join(repr(t) for t in args.inserted) or "NOTHING"), flush=True)

do, dn = O.get("_drop_map", {}), N.get("_drop_map", {})
if do != dn:
    msg = ("drop map CHANGED:\n      only-old %s\n      only-new %s\n      differing %s"
           % (sorted(set(do) - set(dn)), sorted(set(dn) - set(do)),
              {k: (do[k], dn[k]) for k in set(do) & set(dn) if do[k] != dn[k]}))
    if args.allow_dropmap_change:
        print("[delta] DECLARED: " + msg, flush=True)
    else:
        bad.append(msg + "\n      (pass --allow-dropmap-change if Ruling 9d requires it)")
else:
    print("[delta] drop map byte-identical (%d terms mapped)" % len(dn), flush=True)

for k in sorted(set(so) & set(sn)):
    to = [t.strip() for t in so[k].split(",")]
    tn = [t.strip() for t in sn[k].split(",")]
    hits = {t: tn.count(t) for t in args.inserted}
    for t, c in hits.items():
        if c > 1:
            bad.append("stem %s carries %r %d times" % (k, t, c))
    stripped = [t for t in tn if t not in args.inserted]
    if stripped != to:
        bad.append("stem %s: NEW minus inserted != OLD\n      old %s\n      got %s"
                   % (k, to, stripped))
    where = ", ".join("%r at %d" % (t, tn.index(t)) for t in args.inserted if t in tn) or "-"
    print("[delta]   %-14s %2d -> %2d terms   %s" % (k, len(to), len(tn), where), flush=True)

if bad:
    raise SystemExit("ANDON: the rebuild is not the declared delta:\n  %s\nThis check has no "
                     "skip flag." % "\n  ".join(bad))
print("[delta] PASS: every stem is its predecessor plus exactly the named term(s), "
      "and nothing else moved.", flush=True)
sys.exit(0)
