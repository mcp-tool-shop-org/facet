"""Build the E14 STROKE STEMS v3, as Ruling 24g rules them.

The twin builder's construction is inherited whole: stems are the profile's live prompt
entry with WHOLE COMMA-TERMS DELETED, never retyped, term order the entry's throughout.
This file adds exactly one thing the twin builder never needed, and it is the ruling's:

  ⚠ ONE TERM IS SUBSTITUTED, AND ONLY ONE. Ruling 24g strengthens L5 from `a dark garnet
  gem pommel` to `a deep red garnet gem pommel` for the STROKE LANE ONLY - the fixture's
  L5 word is unchanged, the identity is the Director's. A substitution is a retype, which
  is exactly what the deletion construction exists to forbid, so it is bounded here by
  assertion rather than by care: the v3 entry must differ from the twin entry in EXACTLY
  ONE comma-term, at the position the ruling names, and every other term must be
  byte-identical. A second changed term writes no file.

Then the drop map, unchanged from v2 (E14 Ruling 15a): the boss term drops on the two
edge-on cameras (a plate on the guard FACE, subsumed edge-on); the rings term drops
nowhere. Keys are the JOB keys `texpass_iter emit` writes, so `brush_cloud_step --key`
addresses them directly.

Standards compliance: PIN_PER_STEP - the entry is read from the live profile, never
transcribed, and the output records which profile and which ruling. ANDON_AUTHORITY - the
one-substitution bound, the subsequence assertion and the byte-equality assertion all raise
before any file is written, with no skip flag. DECOMPOSE_BY_SECRETS - the drop map is this
subject's, measured at Task 4 and ruled at 15a; the term change is this LANE's, ruled at
24g; neither reaches into the other. EXTERNAL_VERIFIER - `brush_cloud_step`'s pre-flight
checks these strings by PROVENANCE against the profile's fixture pointer, so the file is
checked by a tool that did not write it.
"""
import argparse
import json
import os

ap = argparse.ArgumentParser()
ap.add_argument("--profile", default="profiles/prop.json")
ap.add_argument("--out", default="docs/experiments/E14-brush-prompts.json")
ap.add_argument("--twins", default="docs/experiments/E14-twin-prompts.json")
args = ap.parse_args()

prof = json.load(open(args.profile, encoding="utf-8"))
ENTRY = prof["tools"]["restylize_views.py"]["prompt"]["value"]
NEG = prof["tools"]["restylize_views.py"]["negative"]["value"]
twins = json.load(open(args.twins, encoding="utf-8"))

# ---- the one ruled substitution, bounded ----
OLD_TERM = "a dark garnet gem pommel"
NEW_TERM = "a deep red garnet gem pommel"
terms = [t.strip() for t in ENTRY.split(",")]
assert terms.count(OLD_TERM) == 1, (
    f"ANDON: the entry carries {terms.count(OLD_TERM)} copies of {OLD_TERM!r}; the ruled "
    f"substitution addresses exactly one term or it addresses none")
v3_terms = [NEW_TERM if t == OLD_TERM else t for t in terms]
V3_ENTRY = ", ".join(v3_terms)
diff = [(a, b) for a, b in zip(terms, v3_terms) if a != b]
assert len(diff) == 1 and diff[0] == (OLD_TERM, NEW_TERM), (
    f"ANDON: the v3 entry differs from the twin entry in {len(diff)} terms, not one: {diff}")
assert len(v3_terms) == len(terms), "ANDON: the substitution changed the term COUNT"
assert V3_ENTRY == twins["_entry_verbatim"].replace(OLD_TERM, NEW_TERM), (
    "ANDON: the v3 entry is not the twin entry with exactly the ruled term replaced")
print(f"[stems] entry terms {len(terms)}; ONE substitution, asserted:")
print(f"[stems]   - {OLD_TERM!r}\n[stems]   + {NEW_TERM!r}")

# ---- the drop map, unchanged from v2 (Ruling 15a) ----
DROP = {"a gold diamond boss at the crossing": ["y+090_e+00", "y+270_e+00"]}
ORDER = ["y+000_e+00", "y+180_e+00", "y+045_e+00", "y+225_e+00",
         "y+315_e+00", "y+135_e+00", "y+090_e+00", "y+270_e+00"]

out = {
    "_version": "E14-brush-3",
    "_built_by": "tools/diagnostics/e14_make_brush_prompts.py",
    "_ruled_by": "E14 Ruling 24g (the term) + Ruling 24e (the order) + Ruling 15a (the drop map)",
    "_derived_from": ("prop.json tools['restylize_views.py'].prompt - stems are that string "
                      "with whole comma-terms DELETED, never retyped, EXCEPT the one ruled "
                      "substitution below, which is asserted to be exactly one term."),
    "_entry_verbatim_twins": ENTRY,
    "_entry_verbatim_v3": V3_ENTRY,
    "_the_substitution": {
        "from": OLD_TERM, "to": NEW_TERM,
        "ruled_by": "E14 Ruling 24g",
        "why": ("The term did not fail on the twins - byte-identical stems landed 305 deg "
                "apart by seed alone - but a stroke faces what no twin ever did: the violet "
                "it must replace is its strongest local signal. 12e grammar holds: red IS "
                "garnet's colour. THE FIXTURE'S L5 WORD IS UNCHANGED; this is the stroke "
                "lane's string, not the identity."),
        "watch": ("RED OUTSIDE L5 is the signature, armed with the term - the gold watch's "
                  "analogue, judged by eye at every stroke gate (Ruling 24g).")},
    "_the_rule": twins["_the_rule"],
    "_drop_map": DROP,
    "_assertions": ("The substitution is asserted to touch EXACTLY ONE comma-term. Each stem "
                    "is asserted an ordered SUBSEQUENCE of the v3 entry's term list; each key "
                    "with no drops is asserted BYTE-EQUAL to the v3 entry. All enforced here "
                    "with no skip flag; a failure writes no file."),
    "_order": ",".join(ORDER),
    "_order_why": ("RULED - E14 Ruling 24e. Spiral outward from the most-painted frames; the "
                   "union is order-independent so the order's freight is RISK CADENCE - the "
                   "two 20b-hazard edge-on strokes run LAST."),
    "_negative": NEG,
    "_negative_provenance": twins["_negative_provenance"],
    "_status": ("BUILT for the stroke lane under Ruling 24. Consumed by brush_cloud_step's "
                "lane 'base' pre-flight, which checks these strings BY PROVENANCE against "
                "the profile's _fixtures.brush_prompts pointer."),
}

per_terms, full_keys, extra = {}, [], {}
for key in ORDER:
    dropped = sorted([t for t, ks in DROP.items() if key in ks])
    stem_terms = [t for t in v3_terms if t not in dropped]
    stem = ", ".join(stem_terms)
    # ordered-subsequence assertion, the twin builder's own
    it = iter(v3_terms)
    assert all(any(t == u for u in it) for t in stem_terms), (
        f"ANDON: {key}'s stem is not an ordered subsequence of the v3 entry")
    if not dropped:
        assert stem == V3_ENTRY, f"ANDON: {key} has no drops but is not byte-equal to the entry"
        full_keys.append(key)
    assert NEW_TERM in stem, f"ANDON: {key} lost L5's ruled term"
    assert OLD_TERM not in stem, f"ANDON: {key} still carries the superseded L5 term"
    out[key] = stem
    per_terms[key] = len(stem_terms)
    extra[key] = {"dropped": dropped, "terms": len(stem_terms)}
    print(f"[stems] {key}  {len(stem_terms)} terms"
          + (f"  DROPPED {dropped}" if dropped else "  FULL"))

out["_per_key_term_count"] = per_terms
out["_full_string_keys"] = full_keys
out["_extra_stems"] = extra
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print(f"\n[stems] wrote {args.out}  ({len(ORDER)} keys, "
      f"{len(full_keys)} full / {len(ORDER) - len(full_keys)} with drops)")
