"""E55 — Gate B: count the elements in a generation prompt, by ONE mechanical rule.

WHY THIS EXISTS. E55 asks whether element COUNT or element IDENTITY predicts whether a
named element drops. Comparing arms by count requires a count, and "two arms counted by
different rules" is the defect the E55 spec exists to avoid. So the rule is mechanical,
it is printed in full beside every result, and it is applied identically to every arm.

WHAT IT IS NOT. This does not decide what an element MEANS, does not map a phrase to a
canon N-id, and does not judge whether a phrase landed. Those are separate questions and
two of them are eye questions. This counts phrases.

THE RULE, in the order it is applied:

  1. Load the prompt from a PRIMARY artifact only — an as-generated `*_gen.json` or a
     committed input JSON. The manifest names the file and the key. A missing file or key
     raises; it is never inferred from a report's paraphrase. (E55 Gate A, in code.)
  2. Split on commas -> PROMPT SURFACES. Purely mechanical, no judgement.
  3. Split each surface on " with " -> ELEMENT PHRASES. A comma-phrase of the form
     "X with Y" packs two occupants onto two different surfaces
     ("dark red layered cloth skirt with a leather belt" is a skirt AND a belt), and a rule
     that misses that undercounts the low-density arms specifically — which would bias the
     very comparison this tool exists to serve.
  4. Drop phrases on the declared STYLE/FRAMING stop-list. These are not elements of the
     subject: background, brushstroke/surface style, and camera orientation.
  5. Deduplicate case-insensitively, keeping first-seen order -> UNIQUE ELEMENTS.

Step 5 is deliberately the same definition `canon_worksheet.density()` uses for
`unique_elements` — distinct prompt-provenance phrases, case-insensitive, first-seen order
— so an arm's count is comparable with the canon's own readout (W3: 24 prompt surfaces /
25 required checks / 19 unique elements).

KNOWN LIMITATION, stated rather than hidden. The rule counts a phrase, not an attribute.
"a burly bald warrior" is ONE element carrying two attributes (burly, bald), while a prompt
that writes "a burly warrior, a bald head" scores TWO. That is a real difference between the
two prompts and the rule surfaces it rather than smoothing it — but it means a count
difference between arms can come from re-phrasing as well as from adding an element, and any
reading of these numbers must say which. The per-arm phrase lists are printed so a reader can
check every increment by eye.

  e55_prompt_elements.py --manifest M.json [--out-json J.json] [--selftest]

Manifest shape:
  {"arms": [{"name": "ARMOUR", "file": "...gen.json", "key": "prompt", "tier": "as-generated"},
            {"name": "SPEC", "file": "...json", "key": "w3clay_0", "tier": "committed-input"}]}
"""
import argparse
import json
import os
import sys

# --- the declared stop-list. Printed with every run; nothing is dropped silently. ---
STOP_EXACT = {
    "plain grey background",
    "plain flat grey background",
    "visible brushstrokes",
    "painterly visible brushstrokes",
    "painterly worked surface",
    "worked matte surface",
    "seen from the front",
    "seen from the side",
    "in profile",
    "seen from behind",
    "at three-quarters",
    "seen from directly behind",
}

TIERS = ("as-generated", "committed-input")


def split_surfaces(prompt):
    """Rule step 2 — comma split."""
    return [p.strip() for p in prompt.split(",") if p.strip()]


def split_elements(surfaces):
    """Rule step 3 — split each surface on ' with '."""
    out = []
    for s in surfaces:
        for part in s.split(" with "):
            part = part.strip()
            if part:
                out.append(part)
    return out


def drop_style(phrases):
    """Rule step 4 — remove declared style/framing phrases."""
    kept, dropped = [], []
    for p in phrases:
        (dropped if p.strip().lower() in STOP_EXACT else kept).append(p)
    return kept, dropped


def unique_first_seen(phrases):
    """Rule step 5 — case-insensitive dedupe, first-seen order.

    Same definition as canon_worksheet._unique_element_phrases, so the numbers compare.
    """
    seen, out = set(), []
    for p in phrases:
        low = p.strip().lower()
        if low in seen:
            continue
        seen.add(low)
        out.append(p.strip())
    return out


def count_prompt(prompt):
    surfaces = split_surfaces(prompt)
    elements = split_elements(surfaces)
    kept, dropped = drop_style(elements)
    uniq = unique_first_seen(kept)
    return {
        "prompt": prompt,
        "prompt_surfaces": len(surfaces),
        "surfaces": surfaces,
        "element_phrases": kept,
        "style_dropped": dropped,
        "unique_elements": len(uniq),
        "unique": uniq,
    }


def load_prompt(path, key):
    """Rule step 1 — primary artifact only. Raises rather than inferring. E55 Gate A."""
    if not os.path.isfile(path):
        raise FileNotFoundError(
            "ANDON: E55 Gate A — prompt artifact not found: %s. A prompt is never "
            "inferred from a report's paraphrase; exclude the arm instead." % path)
    with open(path, encoding="utf-8") as fh:
        obj = json.load(fh)
    # key may be a dotted path, so a saved ComfyUI workflow's node text
    # ("7.inputs.text") is reachable as a primary artifact rather than being
    # retyped into the manifest by hand — retyping is how E04 Arm G7 got a
    # self-referencing link past a dry_run.
    val = obj
    for part in str(key).split("."):
        if not isinstance(val, dict) or part not in val:
            raise KeyError(
                "ANDON: E55 Gate A — key %r absent from %s (stopped at %r). "
                "Keys present there: %s"
                % (key, path, part,
                   sorted(val.keys()) if isinstance(val, dict) else type(val).__name__))
        val = val[part]
    if not isinstance(val, str) or not val.strip():
        raise ValueError("ANDON: E55 Gate A — %s[%r] is not a non-empty string" % (path, key))
    return val


def run(manifest_path):
    with open(manifest_path, encoding="utf-8") as fh:
        man = json.load(fh)
    arms = man.get("arms") or []
    if not arms:
        raise ValueError("ANDON: manifest has no arms")
    rows = []
    for a in arms:
        for req in ("name", "file", "key", "tier"):
            if req not in a:
                raise KeyError("ANDON: arm %r missing %r" % (a.get("name"), req))
        if a["tier"] not in TIERS:
            raise ValueError(
                "ANDON: arm %s tier %r not one of %s — provenance tier is part of the "
                "record, not a free-text note." % (a["name"], a["tier"], TIERS))
        r = count_prompt(load_prompt(a["file"], a["key"]))
        r.update(name=a["name"], file=os.path.abspath(a["file"]), key=a["key"],
                 tier=a["tier"])
        rows.append(r)
    return {"rule": RULE_TEXT, "stop_list": sorted(STOP_EXACT), "arms": rows}


RULE_TEXT = [
    "1. prompt loaded from a PRIMARY artifact only (as-generated *_gen.json or committed "
    "input JSON); missing file or key raises, never inferred",
    "2. split on commas -> prompt surfaces",
    "3. split each surface on ' with ' -> element phrases",
    "4. drop phrases on the declared style/framing stop-list",
    "5. case-insensitive dedupe, first-seen order -> unique elements "
    "(same definition as canon_worksheet.density unique_elements)",
]


def report(res):
    print("e55_prompt_elements — Gate B counting rule, applied identically to every arm")
    for line in res["rule"]:
        print("  RULE %s" % line)
    print("  STOP-LIST (%d): %s" % (len(res["stop_list"]), "; ".join(res["stop_list"])))
    print()
    print("  %-8s %-16s %10s %10s" % ("arm", "tier", "surfaces", "unique"))
    for r in res["arms"]:
        print("  %-8s %-16s %10d %10d" % (r["name"], r["tier"], r["prompt_surfaces"],
                                          r["unique_elements"]))
    for r in res["arms"]:
        print()
        print("  === %s (%s)  %s [%s]" % (r["name"], r["tier"], r["file"], r["key"]))
        print("      prompt_surfaces %d  unique_elements %d"
              % (r["prompt_surfaces"], r["unique_elements"]))
        for i, p in enumerate(r["unique"], 1):
            print("      %2d. %s" % (i, p))
        if r["style_dropped"]:
            print("      dropped as style/framing: %s" % "; ".join(r["style_dropped"]))


def selftest():
    """Legs that FAIL if the rule is wrong in the specific way each exists to catch."""
    # step 3 must split 'X with Y' — without it the low-density arms undercount, which
    # would bias the count comparison this tool serves.
    r = count_prompt("dark red layered cloth skirt with a leather belt, heavy dark boots")
    if r["prompt_surfaces"] != 2:
        raise AssertionError("ANDON selftest: comma split gave %d, want 2"
                             % r["prompt_surfaces"])
    if r["unique_elements"] != 3:
        raise AssertionError(
            "ANDON selftest: ' with ' split not applied — unique %d, want 3 (%s)"
            % (r["unique_elements"], r["unique"]))
    # step 4 must drop style, and ONLY the declared phrases
    r = count_prompt("a gold pommel, plain grey background, visible brushstrokes, "
                     "painterly worked surface")
    if r["unique_elements"] != 1 or r["unique"] != ["a gold pommel"]:
        raise AssertionError("ANDON selftest: stop-list wrong -> %s" % r["unique"])
    if len(r["style_dropped"]) != 3:
        raise AssertionError("ANDON selftest: dropped %s" % r["style_dropped"])
    # step 5 must dedupe case-insensitively
    r = count_prompt("gold knee plates, Gold Knee Plates, a gold pommel")
    if r["unique_elements"] != 2:
        raise AssertionError("ANDON selftest: dedupe gave %d, want 2" % r["unique_elements"])
    # Gate A must RAISE on a missing artifact rather than return a default
    try:
        load_prompt(os.path.join(os.path.dirname(__file__), "__e55_no_such_file__.json"), "p")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("ANDON selftest: Gate A did not raise on a missing artifact")
    print("e55_prompt_elements selftest OK (4 legs)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest")
    ap.add_argument("--out-json")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        sys.exit(0)
    if not args.manifest:
        raise SystemExit("ANDON: --manifest is required (or --selftest)")
    res = run(args.manifest)
    report(res)
    if args.out_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.out_json)) or ".", exist_ok=True)
        with open(args.out_json, "wb") as fh:
            fh.write(json.dumps(res, indent=1).encode("utf-8"))
        print("\n[e55] wrote %s" % args.out_json)
