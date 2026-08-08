"""Is the character profile a pure RELOCATION of the tools' own defaults?

The E04 byte-identity gate re-runs three things - the eight-camera projection, one emit, and
e08_acceptance's anchor - and proves those reproduce to the byte with the profile loaded.
That is strong where it reaches and silent everywhere else: it never runs cull_unseen,
bake_hero_prep, smart_decimate, restylize_views or the render tools, so a mistranscribed
value in any of those would sail past it. One did, and was caught by reading rather than by
the gate: cull_unseen's --production defaults to a 24-yaw superset, and writing the
character's ten cameras there would have narrowed a safety margin into a subject list.

So this checks the claim STATICALLY and for every tool at once: for each value in the
profile, find that flag's `default=` in the tool's source and compare. A difference is
either a mistranscription (fix the profile) or a deliberate change (which means the profile
is not a relocation and the E04 report has to say so).

It reads source text rather than importing, because these tools execute their work at
import time - there is no way to ask them for their defaults without running them.

  e04_profile_check.py --profile profiles/character.json --tools tools

Standards compliance: EXTERNAL_VERIFIER - this checks the profile against a source of truth
the profile's author did not write (the tools' own defaults) and reports mismatches without
deciding what they mean. ANDON_AUTHORITY - exits non-zero on any mismatch.
"""
import argparse
import ast
import json
import os
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--profile", required=True)
ap.add_argument("--tools", default="tools")
ap.add_argument("--coverage", metavar="REFERENCE_PROFILE",
                help="ALSO check what is ABSENT. Diffs this profile against the reference's "
                     "per-tool keys and requires an explicit decision for every key the "
                     "reference has and this one does not — a value, a vacuous suspension, "
                     "or `_not_on_route`. Silence is the failure this exists to catch: an "
                     "absent key means the tool uses ITS OWN default, which on this route is "
                     "the other subject's measurement. E04 Ruling 21.")
ap.add_argument("--allow-differ", action="append", default=[],
                help="tool:key that is INTENDED to differ from the source default; each "
                     "one must be argued in the E04 report")
args = ap.parse_args()

prof = json.load(open(args.profile, encoding="utf-8"))
allow = set(args.allow_differ)


def defaults_of(path):
    """{flag: default-source-text} for one tool, by brace-matching each add_argument."""
    src = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"\b\w+\.add_argument\(", src):
        i = m.end() - 1
        d = 0
        while i < len(src):
            if src[i] == "(":
                d += 1
            elif src[i] == ")":
                d -= 1
                if d == 0:
                    break
            i += 1
        blob = src[m.start():i + 1]
        nm = re.search(r'"(--[A-Za-z0-9\-_]+)"', blob)
        if not nm:
            continue
        j = blob.find("default=")
        if j < 0:
            out[nm.group(1)[2:]] = None
            continue
        # Walk to the comma that ends this keyword argument -- STRING-AWARE. A default of
        # "360,240,700,600" contains commas that are not argument separators, and the first
        # version of this walker stopped at one, reporting five real values as unevaluable.
        k = j + len("default=")
        depth = 0
        quote = None
        while k < len(blob):
            c = blob[k]
            if quote:
                if c == "\\":
                    k += 2
                    continue
                if c == quote:
                    quote = None
            elif c in "\"'":
                quote = c
            elif c in "([{":
                depth += 1
            elif c in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif c == "," and depth == 0:
                break
            k += 1
        out[nm.group(1)[2:]] = blob[j + len("default="):k].strip()
    return out


bad = []
checked = 0
for tool, block in prof["tools"].items():
    path = os.path.join(args.tools, tool)
    if not os.path.exists(path):
        bad.append((tool, "-", "TOOL NOT FOUND at %s" % path))
        continue
    dflt = defaults_of(path)
    for key, entry in block.items():
        if key.startswith("_"):
            continue
        checked += 1
        if key not in dflt:
            bad.append((tool, key, "no such flag in the tool"))
            continue
        raw = dflt[key]
        if raw is None:
            bad.append((tool, key, "flag has no default= in source (required arg?)"))
            continue
        try:
            got = ast.literal_eval(raw)
        except Exception:
            try:
                got = eval(raw, {"__builtins__": {}}, {})       # e.g. 1.0 / 3.0
            except Exception:
                bad.append((tool, key, "default %r not evaluable" % raw))
                continue
        want = entry["value"]
        same = (got == want) or (
            isinstance(got, float) and isinstance(want, (int, float))
            and abs(got - float(want)) <= 1e-12 * max(1.0, abs(got)))
        if not same:
            if "%s:%s" % (tool, key) in allow:
                print("[chk] ALLOWED DIFFER %s %s: source %r, profile %r"
                      % (tool, key, got, want))
            else:
                bad.append((tool, key, "source default %r != profile value %r" % (got, want)))

print("[chk] %s: %d values checked against %d tools"
      % (os.path.basename(args.profile), checked, len(prof["tools"])))
if bad:
    print("[chk] NOT A PURE RELOCATION - %d mismatches:" % len(bad))
    for t, k, why in bad:
        print("[chk]   %-24s %-20s %s" % (t, k, why))

# ---------------------------------------------------------------- COVERAGE
# THE SECOND QUESTION, and the one that cost three halts in one arc. The check above
# compares values that are PRESENT. It is structurally blind to values that are ABSENT —
# and an absent key is not neutral: the tool falls back to its own default, which on this
# route is the CHARACTER's measurement. Three instances in E04, the third one firing inside
# project_twins and stopping the projection:
#
#   reg-iou-min / bbox-tol   suspended in ship.json's prose, armed at W3's 0.80 / 0.25
#   texpass_brush --prompt   absent, defaults to W3's literal identity string
#   bg-de / bg-max-pct       absent, defaulted to W3's 10.0 / 2.0 and HALTED view 0
#
# So: diff the subject profile against a reference profile's per-tool keys and require every
# absent key to carry an EXPLICIT decision. Three forms count as decided, per E04 Ruling 21 —
# a real value, a vacuous suspension (a value the tool receives that cannot fire, the
# reg-iou-min 0.0 pattern), or `_not_on_route`. Silence does not count. That is the whole
# point: the failure mode is a value nobody decided, not a value someone chose wrongly.
#
#   _not_on_route: {"key": "why"}          inside a tool block, per key
#   _per_invocation: {"key": "why"}        inside a tool block, per key - E12 Ruling 6d's
#                                          fifth form: the key IS exercised every run, and
#                                          the profile supplies no value BY DESIGN because
#                                          the correct one arrives from the job context
#   _tools_not_on_route: {"tool": "why"}   at profile top level, for a whole tool
if args.coverage:
    ref = json.load(open(args.coverage, encoding="utf-8"))
    tools_skip = prof.get("_tools_not_on_route", {})
    undecided, decided = [], 0
    for tool, rblock in ref["tools"].items():
        sblock = prof["tools"].get(tool)
        rkeys = [k for k in rblock if not k.startswith("_")]
        if sblock is None:
            if tool in tools_skip:
                decided += len(rkeys)
                print("[cov] %-24s WHOLE TOOL not on route: %s" % (tool, tools_skip[tool]))
            else:
                for k in rkeys:
                    undecided.append((tool, k, "tool has no block in this profile"))
            continue
        # `_per_invocation` is E12 Ruling 6d's fifth form, migrated in E16-11 and
        # merged here rather than tracked separately: for THIS check both mean the
        # key is decided-with-no-profile-value, and the distinction between "never
        # runs" and "runs every time, supplied by the job" is carried by the registry
        # sweep's `how` column, which is where it is actually read.
        skip = dict(sblock.get("_not_on_route", {}))
        skip.update(sblock.get("_per_invocation", {}))
        # `_NOT_CLEARED` is the FOURTH accepted form (E04 Ruling 22) and the STRONGEST: it
        # decides a whole tool by forbidding its use, rather than excusing a key. The
        # lifecycle is the point — when a ruling lifts the block, the marker goes, its keys
        # revert to undecided, and coverage fires again, so the ruling that clears the tool
        # must decide its keys as the price of clearing it.
        if "_NOT_CLEARED" in sblock:
            decided += len(rkeys)
            print("[cov] %-24s NOT CLEARED (all %d keys): %s"
                  % (tool, len(rkeys), str(sblock["_NOT_CLEARED"])[:96]))
            continue
        for k in rkeys:
            if k in sblock:
                decided += 1
            elif k in skip:
                decided += 1
            else:
                rv = rblock[k]
                rv = rv.get("value") if isinstance(rv, dict) else rv
                undecided.append((tool, k, "absent — reference carries %r" % (rv,)))
    print("[cov] coverage against %s: %d reference keys decided, %d UNDECIDED"
          % (os.path.basename(args.coverage), decided, len(undecided)))
    if undecided:
        print("[cov] every row below is a flag whose value this subject inherits from the "
              "reference subject BY SILENCE:")
        for t, k, why in undecided:
            print("[cov]   %-24s %-20s %s" % (t, k, why))
        sys.exit(1)
    print("[cov] every reference key has an explicit decision in this profile.")

if bad:
    sys.exit(1)
print("[chk] PURE RELOCATION: every profile value equals its tool's own default.")
