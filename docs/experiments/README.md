# Experiments

Each experiment is a spec written by an advisor session, run by a separate executor
session, and judged by the Director. The separation is deliberate: the session that
designs an experiment does not get to grade its own results, and the session that runs
it does not get to decide what the results mean.

**A spec is written before the work. A report is written after. Conclusions come last,
from the advisor, only once the Director has seen the evidence.**

| id | question | status |
|---|---|---|
| [E01](E01-facial-structure-ceiling.md) | Where is the facial-structure ceiling — framing, generation resolution, generator, or reconstruction itself? Does any configuration produce a connected surface rather than shell soup? | SPEC, not yet run |

## Why it works this way

An earlier arc of this project ran ten sessions in which each session judged its own
output, wrote its conclusions to a shared memory store, and the next session read those
conclusions as established fact. Errors compounded silently because nothing in the loop
was checkable and nothing was gated on the Director's eye.

The repo is the fix. A claim sitting next to runnable code can be tested in minutes.
A tool marked *superseded* with its failure documented cannot quietly become doctrine,
because anyone can run it and watch it fail the same way.
