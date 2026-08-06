"""Build a subject's twin-prompts file by DELETING whole comma-terms from the profile's own
protective prompt entry — never by retyping it.

WHY A TOOL AND NOT A HAND-WRITTEN JSON. The first E12 prompts file (v1, 75b9a02) carried a
with-clause opening and one constant string on all eight views; both were the advisor's errors
and both were caught only by reading (E12 Rulings 9c/9d). v2 was rebuilt by hand and its own
`_authored` note claims "the builder asserted that each stem is an ordered subsequence" — but
no builder was committed, so that claim had no artifact behind it. This file is that artifact.
The register swap of Ruling 10b is exactly the edit that would silently desynchronise a
hand-copied stem from the profile entry, so the third build is mechanical.

THE RULE IT ENFORCES (E12 Ruling 9d, deviation measured at Ruling 10i):
an element whose surface a view cannot see is DROPPED from that view's stem, because a term
present in a view's prompt is an instruction to paint it and the text wins against the control
(the W3 beard mechanism, measured). Every stem is therefore an ordered SUBSEQUENCE of the
profile entry's term list, asserted here, and the views that drop nothing are asserted
BYTE-EQUAL to the entry. Term order is the entry's throughout.

  e12_make_twin_prompts.py --profile profiles/beast.json --out docs/experiments/X.json
                           --tag dragonclay --views 0,1,2,3,4,5,6,7
                           --drop "ember-orange eyes:3,4,5" --drop "..." ...

ANDON_AUTHORITY: every --drop term must match a term in the entry exactly, and each built stem
must be an ordered subsequence; either failure raises and NO file is written. There is no skip
flag. PIN_PER_STEP: the built file records the entry it derived from, the drop map, and the
per-view term counts, so the derivation is replayable from the artifact alone.
NAMED_COMPENSATORS: writes one JSON; undo = git checkout that path.
"""
import argparse
import json
import os

ap = argparse.ArgumentParser()
ap.add_argument("--profile", required=True)
ap.add_argument("--tool", default="restylize_views.py")
ap.add_argument("--key", default="prompt", help="the profile entry the stems derive FROM")
ap.add_argument("--negative-key", default="negative")
ap.add_argument("--out", required=True)
ap.add_argument("--tag", required=True, help="stem prefix; must equal the render --tag")
ap.add_argument("--views", default="0,1,2,3,4,5,6,7")
ap.add_argument("--drop", action="append", default=[],
                help="TERM:views - drop this exact comma-term from those view stems. "
                     "Repeatable. The term must appear in the entry verbatim.")
ap.add_argument("--version", required=True)
ap.add_argument("--supersedes", default="")
ap.add_argument("--note", action="append", default=[], help="KEY=TEXT, recorded in the file")
args = ap.parse_args()

prof = json.load(open(args.profile, encoding="utf-8"))
blk = prof.get("tools", {}).get(args.tool, {})
entry = blk.get(args.key, {}).get("value")
neg = blk.get(args.negative_key, {}).get("value")
if not isinstance(entry, str) or not isinstance(neg, str):
    raise SystemExit("ANDON: %s tools['%s'] has no decided string for %r / %r"
                     % (args.profile, args.tool, args.key, args.negative_key))

TERMS = [t.strip() for t in entry.split(",")]
if any(not t for t in TERMS):
    raise SystemExit("ANDON: the profile entry has an empty comma-term; refusing to derive "
                     "stems from a string this file cannot round-trip.")

VIEWS = [v.strip() for v in args.views.split(",") if v.strip()]
drops = {}                      # term -> set(views)
bad = []
for spec in args.drop:
    term, views = spec.rsplit(":", 1)
    if term not in TERMS:
        bad.append("--drop term %r is not a comma-term of the profile entry. The entry's "
                   "terms are:\n    %s" % (term, "\n    ".join(TERMS)))
        continue
    for v in views.split(","):
        drops.setdefault(term, set()).add(v.strip())
        if v.strip() not in VIEWS:
            bad.append("--drop %r names view %r, which is not in --views" % (term, v.strip()))
if bad:
    raise SystemExit("ANDON: drop map does not match the profile entry:\n  %s\n"
                     "No file was written." % "\n  ".join(bad))


def subsequence(sub, full):
    """Is `sub` an ordered subsequence of `full`? The whole point of deriving by deletion."""
    it = iter(full)
    return all(t in it for t in sub)


out = {
    "_version": args.version,
    "_built_by": "tools/diagnostics/e12_make_twin_prompts.py",
    "_derived_from": "%s tools['%s'].%s - stems are that string with whole comma-terms "
                     "DELETED, never retyped. Term order is the entry's throughout."
                     % (os.path.basename(args.profile), args.tool, args.key),
    "_entry_verbatim": entry,
    "_entry_terms": len(TERMS),
    "_the_rule": "E12 Ruling 9d: an element whose surface a view cannot see is dropped from "
                 "that view's stem - a term present in a view's prompt is an instruction to "
                 "paint it, and the text wins against the control (the W3 beard mechanism, "
                 "measured). Split deviation measured and ruled at E12 Ruling 10i.",
    "_drop_map": {t: sorted(v, key=int) for t, v in sorted(drops.items())},
    "_assertions": "Each stem asserted an ordered SUBSEQUENCE of the entry's term list; each "
                   "view with no drops asserted BYTE-EQUAL to the entry. Both enforced in the "
                   "builder with no skip flag; a failure writes no file.",
}
if args.supersedes:
    out["_supersedes"] = args.supersedes
for n in args.note:
    k, _, t = n.partition("=")
    out["_" + k] = t

counts, full_views = {}, []
for v in VIEWS:
    kept = [t for t in TERMS if v not in drops.get(t, ())]
    if not subsequence(kept, TERMS):
        raise SystemExit("ANDON: view %s stem is not an ordered subsequence of the entry. "
                         "No file written." % v)
    s = ", ".join(kept)
    if len(kept) == len(TERMS):
        if s != entry:
            raise SystemExit("ANDON: view %s drops nothing but is not byte-equal to the "
                             "profile entry - the join does not round-trip the split. "
                             "No file written." % v)
        full_views.append(v)
    out["%s_%s" % (args.tag, v)] = s
    counts[v] = len(kept)

out["_per_view_term_count"] = counts
out["_full_string_views"] = full_views
out["_negative"] = neg
out["_negative_provenance"] = ("%s tools['%s'].%s, transcribed. An authored negative would be "
                               "a second variable in the run that introduces the first."
                               % (os.path.basename(args.profile), args.tool,
                                  args.negative_key))

os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
    fh.write("\n")

print("[prompts] entry: %d terms, %d chars" % (len(TERMS), len(entry)))
print("[prompts] drops: %s" % ("; ".join("%r -> views %s" % (t, ",".join(sorted(v, key=int)))
                                         for t, v in sorted(drops.items())) or "none"))
for v in VIEWS:
    print("[prompts]   %s_%-2s %2d terms%s" % (args.tag, v, counts[v],
                                               "   FULL (byte-equal to entry)"
                                               if v in full_views else ""))
print("[prompts] all stems asserted ordered subsequences; %d full-string views byte-equal"
      % len(full_views))
print("[prompts] wrote %s" % args.out)
