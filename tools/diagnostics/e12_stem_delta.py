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
# SUBSTITUTION, added at handoff 12. v6/v7/v8 were all INSERTIONS; Ruling 22b strengthens an
# existing term in place instead (`storm-grey wing membranes` -> `leathery storm-grey wing
# membranes`), which the insertion assertion cannot express: the term count does not change and
# neither term is new-or-gone on its own. The assertion is the same shape — substitute NEW back
# to OLD in each new stem and the old stem must come back byte-equal — and it is checked
# ALONGSIDE the insertion rule, not instead of it, so a mixed round is expressible.
ap.add_argument("--substituted", action="append", default=[], metavar="OLD=>NEW",
                help="a comma-term the NEW entry REPLACED in place. Repeatable. Mapping NEW "
                     "back to OLD in a new stem must leave the old stem byte-equal.")
ap.add_argument("--allow-dropmap-change", action="store_true",
                help="permit the drop map to differ, printing the diff. Ruling 9d can REQUIRE "
                     "a new drop; that is a decision, so it is a declared argument.")
# NEW STEM KEYS, added at handoff 13. E13 A1 adds head-crop stems (`headcrop_0`, `headcrop_1`)
# alongside the eight turnaround stems and the companion — a stem key the predecessor does not
# have. The key-set check below is right to halt on that by default: a stem appearing or
# vanishing is exactly the class of silent change this tool exists to catch. So it is a
# DECLARED argument in the same shape as --allow-dropmap-change: each new key must be NAMED,
# every shared stem is still asserted byte-equal, and a key that DISAPPEARS is still a halt
# with no flag at all. Naming a key that is not actually new is itself an error.
ap.add_argument("--allow-new-stem", action="append", default=[], metavar="KEY",
                help="permit exactly this NEW stem key, which the old file does not carry. "
                     "Repeatable. A new stem is a decision (E13 A1's crop stems), so it is "
                     "declared per key rather than waved through as a set difference. Every "
                     "shared stem is still asserted byte-equal and no key may vanish.")
args = ap.parse_args()

O = json.load(open(args.old, encoding="utf-8"))
N = json.load(open(args.new, encoding="utf-8"))
print("[delta] %s  ->  %s" % (O.get("_version"), N.get("_version")), flush=True)

bad = []


def stems(d):
    return {k: v for k, v in d.items()
            if not k.startswith("_") and isinstance(v, str)}


so, sn = stems(O), stems(N)
_gone = sorted(set(so) - set(sn))
_new = sorted(set(sn) - set(so))
_declared = sorted(set(args.allow_new_stem))
if _gone:
    bad.append("stem key(s) VANISHED from the new file: %s — there is no flag for this" % _gone)
for k in _declared:
    if k not in _new:
        bad.append("--allow-new-stem %r names a key that is not new (old file already has it, "
                   "or the new file does not)" % k)
_undeclared = [k for k in _new if k not in _declared]
if _undeclared:
    bad.append("stem key(s) appeared undeclared: %s — name each with --allow-new-stem or the "
               "builder added a stem nobody decided on" % _undeclared)
elif _new:
    print("[delta] NEW stem key(s), declared: %s" % _new, flush=True)

eo = [t.strip() for t in O["_entry_verbatim"].split(",")]
en = [t.strip() for t in N["_entry_verbatim"].split(",")]
SUB = {}
for spec in args.substituted:
    old, sep, new = spec.partition("=>")
    if not sep:
        bad.append("--substituted wants OLD=>NEW, got %r" % spec)
        continue
    old, new = old.strip(), new.strip()
    if old not in eo:
        bad.append("--substituted OLD %r is not a comma-term of the OLD entry" % old)
    if new not in en:
        bad.append("--substituted NEW %r is not a comma-term of the NEW entry" % new)
    if old in en:
        bad.append("--substituted OLD %r still appears in the NEW entry, so it was not "
                   "replaced" % old)
    SUB[new] = old


def unsub(terms):
    """Map the NEW terms back to their OLD spellings, so the comparison is against the old."""
    return [SUB.get(t, t) for t in terms]


for t in args.inserted:
    if t in eo:
        bad.append("--inserted %r is already a term of the OLD entry, so it is not an insertion"
                   % t)
    if t not in en:
        bad.append("--inserted %r is not a comma-term of the NEW entry" % t)
stripped_entry = unsub([t for t in en if t not in args.inserted])
if stripped_entry != eo:
    bad.append("the NEW entry minus the inserted term(s), with substitutions reversed, is not "
               "the OLD entry:\n      old %s\n      got %s" % (eo, stripped_entry))
print("[delta] entry %d -> %d terms; inserted %s; substituted %s"
      % (len(eo), len(en), ", ".join(repr(t) for t in args.inserted) or "NOTHING",
         "; ".join("%r -> %r" % (o, n) for n, o in SUB.items()) or "NOTHING"), flush=True)

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
    hits = {t: tn.count(t) for t in list(args.inserted) + list(SUB)}
    for t, c in hits.items():
        if c > 1:
            bad.append("stem %s carries %r %d times" % (k, t, c))
    for new, old in SUB.items():
        if old in tn:
            bad.append("stem %s still carries the OLD spelling %r" % (k, old))
    stripped = unsub([t for t in tn if t not in args.inserted])
    if stripped != to:
        bad.append("stem %s: NEW minus inserted, substitutions reversed, != OLD\n      old %s\n"
                   "      got %s" % (k, to, stripped))
    where = ", ".join("%r at %d" % (t, tn.index(t))
                      for t in list(args.inserted) + list(SUB) if t in tn) or "-"
    print("[delta]   %-14s %2d -> %2d terms   %s" % (k, len(to), len(tn), where), flush=True)

if bad:
    raise SystemExit("ANDON: the rebuild is not the declared delta:\n  %s\nThis check has no "
                     "skip flag." % "\n  ".join(bad))
print("[delta] PASS: every stem is its predecessor plus exactly the named term(s), "
      "and nothing else moved.", flush=True)
sys.exit(0)
