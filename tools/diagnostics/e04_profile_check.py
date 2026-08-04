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
    sys.exit(1)
print("[chk] PURE RELOCATION: every profile value equals its tool's own default.")
