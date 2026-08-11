#!/usr/bin/env python
"""facet_index - facet's binding of the shared record index.

WHAT THIS IS NOW. The index that used to live here in full is the `record-index`
package (mcp-tool-shop-org/record-index); this file is facet's ADAPTER to it.
The parsers, the four-leg verify, the ranking and the determinism contract are
unchanged code that now lives in one place, and everything that was a fact about
FACET moved to `docs/index/conventions.json` - a full declaration, validated at
load, with no default for a field it does not state.

WHY EXTRACT RATHER THAN COPY. This repo's own law book records five hand-copies
of one background-model function living under four different names, invisible to
a name-based grep for months. Forking 4,448 lines into a second repo is that
error with three more zeros. The extraction condition was stated in advance and
gated on measurement - the index extracts when a second repo adopts the
conventions - and armature is that repo.

WHAT THE EXTRACTION CHANGED, BEYOND MOVING CODE:

  * `rulings` and `handoffs` gain an `experiment` column. `arc` is IDENTITY and
    is part of the primary key, so it stays stem-derived: measured before it was
    settled, keying on the E-number alone merges `E10-ruling.md` and
    `E10-offsurface-ruling.md` and collides on SEVEN primary keys. `experiment`
    is GROUPING - the `E\\d\\d` prefix, non-key - so "every ruling for E10" is
    one WHERE clause and nothing pays for it with a row's identity.
  * `verify` prints two new REPORT-ONLY sections before its verdict: the
    declaration audit (declared-but-absent and undeclared-but-present corpora)
    and the vocabulary report. The second exists because a second record
    measured two SILENT failures - 38 laws with `paid_for_by` NULL, and six
    video artifacts dropped by an extension map with no video entry. A missing
    file raises; a non-matching vocabulary used to return nothing and say
    nothing.
  * twelve values that lived INSIDE function bodies with no constant name - nine
    arc bounds in verify(), an experiment span, a list of facet's own filename
    fragments, an `E15-` self-reference exclusion - are declared fields now.

THE VERB SURFACE AND THE INVOCATION FORM ARE UNCHANGED. `python
tools/facet_index.py build|verify|q|claims` works exactly as it did, the exit
codes are the same four, and this module still exposes the names the suite and
`record_mcp` bind. `record_mcp.py` still imports this module and is NOT itself
extracted yet - that is named as remaining work rather than implied to be done.
"""
import os
import sys

import record_index
from record_index import cli as _cli

#: facet's binding: the record root resolved by testing for the declared
#: markers, plus `docs/index/conventions.json` loaded and validated.
#: The fallback identity keeps `--help` and a `--db`-explicit `q` alive on an
#: installed copy that has no record beside it: `$FACET_INDEX_DB` and `--db`
#: select an INDEX, never a corpus, so neither may require one to exist.
BINDING = record_index.bind(__file__, name="facet",
                            db_rel="docs/index/facet.db",
                            db_env="FACET_INDEX_DB")

#: Every name the suite and the server bind, re-exported from the binding.
#: Explicit rather than a `dir()` sweep: this surface is a contract.
globals().update(BINDING.exports())

RootNotFound = record_index.RootNotFound
ContractParser = _cli.ContractParser
DEBUG_HELP = _cli.DEBUG_HELP
prog_name = _cli.prog_name
user_error = _cli.user_error
debug_requested = _cli.debug_requested
run_contract = _cli.run_contract

HERE = os.path.dirname(os.path.abspath(__file__))


def is_record_root(path):
    """Does this directory contain the record. The property, not a proxy.

    TWO markers, not one, and the second is not decoration: `CLAUDE.md` alone is
    an ordinary filename - 26 directories under E:\\AI on the rig this was
    measured on carry one, and EXACTLY ONE of those also carries
    `docs/experiments`. A single-marker resolver would bind a working directory
    that is some other repo entirely and then fail deeper in.
    """
    return record_index.is_record_root(path, RECORD_MARKERS)


def repo_candidates():
    """The declared search order, most specific first: the directory this
    module's parent sits in (a source checkout), then the working directory
    (where an INSTALLED command is run from).

    There is deliberately no walk UP from cwd. It would resolve a subdirectory
    of a checkout, and would also reach a parent that is a DIFFERENT record.
    """
    return (os.path.dirname(HERE), os.getcwd())


def resolve_repo(candidates=None):
    """The first candidate that contains the record, or None.

    None, never a guess: a resolver that cannot find a corpus REFUSES.
    Returning a plausible-looking directory is how `<venv>/Lib` became a banner
    four releases in a row, and a fallback here would only move that failure one
    caller downstream.
    """
    for cand in (repo_candidates() if candidates is None else candidates):
        if is_record_root(cand):
            return os.path.abspath(cand)
    return None


#: ⚑ THE MODULE GLOBAL IS AUTHORITATIVE, and the binding reads it on every call
#: rather than capturing it - the suite monkeypatches this name to point the
#: corpus gate at an empty directory, and a captured value would make that test
#: measure nothing.
REPO = BINDING.root
BINDING.set_root_provider(lambda: globals().get("REPO"))


def repo():
    """The record's root, or a refusal."""
    if REPO is None:
        raise RootNotFound(
            "no record corpus found - neither %s nor the working directory %s "
            "contains %s"
            % (os.path.dirname(HERE), os.getcwd(), " + ".join(RECORD_MARKERS)))
    return REPO


def main(argv=None):
    """The console-script entry point. `[project.scripts]` binds this name, so
    the contract wrapper has to be HERE and not in the `__main__` guard."""
    return _cli.run_contract(lambda a: _cli.main(BINDING, a), argv,
                             db_env=BINDING.conv.db_env)


if __name__ == "__main__":
    sys.exit(main())
