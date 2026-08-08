"""Subject profiles — the loader.

WHAT THIS IS FOR. Every constant in this pipeline was calibrated on one standing human
figure, and until now nobody could say which of them are principles and which are that
warrior's measurements wearing a principle's clothes. A profile is where the second kind
lives. The classification that produced it — every constant argued into one column or the
other — is in docs/experiments/E04-profile-extraction.md and is as much the deliverable as
this file is.

HOW IT WORKS, and why this shape. `bind()` is called after every `add_argument` and before
`parse_args`. It adds `--profile`, pre-scans argv for it, and calls `ap.set_defaults()` with
the profile's values for this tool. That ordering matters twice:

  * `set_defaults` only changes what `parse_args` uses when the flag is ABSENT, so an
    explicit command-line argument still wins over the profile. A recorded invocation keeps
    meaning what it meant.
  * With no `--profile`, nothing happens at all. Every historical command reproduces
    byte-for-byte because it takes the same code path it always did.

THE PROFILE IS A RELOCATION, NOT A CHANGE. The character profile's values are the tools'
current defaults, digit for digit. That is a testable claim rather than an intention, and
E04's gate 1 tests it: the eight-camera projection run WITH the character profile must
reproduce `stage1_8cam.png` pixel-identically. If any digit differs, something was
transcribed wrong and the profile is wrong, not the code.

AN UNKNOWN KEY IS AN ERROR, LOUDLY. A profile naming a flag its tool does not have is the
exact failure this system exists to prevent: a value that looks configured, reads as
authoritative, and does nothing. It raises here rather than being skipped.

EVERY VALUE CARRIES ITS `why` AND ITS `from`. A profile is otherwise a perfect hiding place
for unexplained magic numbers, which is precisely how the previous memory store became
doctrine. `bind()` enforces their presence.

  import subject_profile
  ...
  args = ap.parse_args(subject_profile.bind(ap, "project_twins.py", argv))

NAMED `subject_profile`, NOT `profile`: `profile` is a Python standard-library module (the
deterministic profiler), and `tools/` goes on `sys.path` for every script here. A file named
profile.py would shadow it for this process and everything it imports.

Standards compliance: PIN_PER_STEP — a profile is a versioned file named on the command
line and echoed into the log, so a run records which subject it was run as. ANDON_AUTHORITY
— an unknown key, a missing `why` and a malformed entry each raise. DECOMPOSE_BY_SECRETS —
this file IS that standard applied: what changes with the subject is grouped here, what does
not stays in the tools.
"""
import json
import os
import sys

_LOADED = {}


def _read(path):
    if path in _LOADED:
        return _LOADED[path]
    with open(path, encoding="utf-8") as fh:
        prof = json.load(fh)
    if not ("name" in prof and "tools" in prof):
        raise AssertionError(
            "ANDON: %s is not a subject profile - it needs 'name' and 'tools'" % path)
    _LOADED[path] = prof
    return prof


def bind(ap, tool, argv=None):
    """Add --profile, apply it to `ap`'s defaults, and return argv with it removed.

    Returns the argv to hand to parse_args. --profile is consumed here rather than left
    for the tool, so a tool that does not know about profiles cannot trip over it.
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    path = None
    out = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--profile":
            if not (i + 1 < len(argv)):
                raise AssertionError("ANDON: --profile needs a path")
            path = argv[i + 1]
            i += 2
            continue
        if a.startswith("--profile="):
            path = a.split("=", 1)[1]
            i += 1
            continue
        out.append(a)
        i += 1
    # declared so --help lists it and so an unprofiled run records "none" rather than
    # leaving the reader to wonder whether one was in play
    ap.add_argument("--profile", default=path,
                    help="subject profile JSON; its values become defaults, and an "
                         "explicit flag on the command line still overrides them")
    if path is None:
        return out

    prof = _read(path)
    known = {}
    for act in ap._actions:
        if act.dest in ("help", "profile"):
            continue
        known[act.dest] = act
    block = prof["tools"].get(tool)
    if block is None:
        print("[profile] %s: %s has no block for this tool - defaults unchanged"
              % (os.path.basename(path), tool), flush=True)
        return out
    applied = {}
    for key, entry in block.items():
        if key.startswith("_"):
            continue
        dest = key.replace("-", "_")
        if not (dest in known):
            raise AssertionError(
                "ANDON: profile %s names '%s' for %s, which has no such argument. A profile "
                "value that does not reach its tool reads as configuration and does nothing - "
                "that is the failure this system exists to prevent."
                % (os.path.basename(path), key, tool))
        if not (isinstance(entry, dict) and "value" in entry):
            raise AssertionError(
                "ANDON: profile %s entry '%s' must be an object with 'value'" % (path, key))
        if not (entry.get("why")):
            raise AssertionError(
                "ANDON: profile %s entry '%s' carries no 'why'. Every tuned value states why "
                "it holds that value, or the profile becomes the hiding place the old memory "
                "store was." % (os.path.basename(path), key))
        if not (entry.get("from")):
            raise AssertionError(
                "ANDON: profile %s entry '%s' carries no 'from' - which experiment measured it"
                % (os.path.basename(path), key))
        applied[dest] = entry["value"]
    ap.set_defaults(**applied)
    print("[profile] %s (%s): %d values applied to %s"
          % (prof["name"], os.path.basename(path), len(applied), tool), flush=True)
    return out


def value(path, tool, key, default=None):
    """Read one profile value directly, for code that is not behind an argparse flag."""
    if not path:
        return default
    blk = _read(path)["tools"].get(tool, {})
    ent = blk.get(key)
    return default if ent is None else ent["value"]
