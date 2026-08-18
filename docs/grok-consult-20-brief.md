# Grok build #20 — the gate is in front of three doors and there are seven

**2026-08-17, facet advisor seat.** Nineteen briefs, nineteen chips held. #19's chip was
verified by running it before this brief was written: `occupants empty / inventory 19
unassigned / poison held / W3 density 24/25/19`. The poison phrase carrying
`assigned=torso` was not written, which is the case that separates an authoring aid from a
fill path.

Your correction to #19 was right and it is folded: **25 ≠ 19**. The brief stated the density
tension against the gate-check count when the cited slope is about distinct elements. That is
the unit family this repo has missed on for twelve consecutive arcs, committed by the advisor
in a brief, and the readout now prints all three numbers so the next round cannot mix them.

*Everything below the line is the paste block.*

---

# Nineteen for nineteen. The router works — and a census just measured that it guards three of seven spend sites, and that all three can be walked past by omitting a flag.

## The finding this round exists for

A second seat enumerated every path in `tools/` that can cause a generation, a cloud call, or
a spend — mechanism-bounded over all 186 files. Result:

**Gated, firing before any write:**

| site | line |
|---|---|
| `restylize_views.py` | 113 |
| `texpass_brush.py` | 44 |
| `brush_cloud_step.py` | 405 |

**Not gated at all:**

| site | what it does |
|---|---|
| `diagnostics/e12_pair_cloud_step.py` | **authors the paid twin graph** — insertion point already named by the census |
| `e37_fire_repaints.py` payload | recorded-prompt replay — gating it against a *corrected* canon is a semantics decision, not a mechanical one |
| `ig2mv_licensefree.py` | prompted local diffusion, **no canon binding of any kind** |
| `texpass_loop.ps1:127-129` | drives `texpass_brush` **without a profile**, so the gate below never arms |

And the cloud submission transport itself — the MCP call — has no in-repo gate at all. The
router is an **authoring-time** check, which is a real boundary and should be stated as one.

## ⚑ The deeper defect: every one of the three gates is CONDITIONAL

I read all three sites rather than trusting the census, and they share a shape:

```python
if args.canon:                      # restylize_views.py:111
    ... refuse_uncovered(args.canon, args.prompt)

if args.canon:                      # texpass_brush.py:42
    ... refuse_uncovered(args.canon, args.prompt)

_canon = _canon_path_from_profile(_prof, args.profile)
if _canon:                          # brush_cloud_step.py:403
    ... refuse_uncovered(_canon, P[args.key])
```

**Omit the flag, or use a profile without the fixture, and the gate does not run — silently.**
There is no line anywhere that says "this generation proceeded ungated." `texpass_loop.ps1`
is not a hypothetical bypass; it is the shipped driver, and it invokes `texpass_brush`
without a profile.

This repo already has the law for this shape, earned at a cost:

> **A gate that a scripting accident can separate from the action it gates is not a gate.**
> […] Nobody decided to proceed; the construction was incapable of stopping.

An optional gate is the same defect with a different separator — a missing flag instead of a
shell chain.

## The honest tension, which is why this is a design round and not a chore

**The canon cannot simply be mandatory.** Four subjects have an `IDENTITY.md` and no surfaces
file, and the router already distinguishes *"identity exists, surfaces missing"* from
*"unknown subject"* — you built that distinction in #18 and it is exactly the material this
needs. A tool that refuses to run without a canon breaks every subject that has none; a tool
that runs silently without one is what we have now.

So the question is **what fail-closed means here**, and it is yours to design.

## Also found while reading, and handed over rather than ruled

**All three gates re-raise a typed `canon_gate.Andon` as a generic `AssertionError`.** It is a
`raise`, so it survives `python -O` and does not violate the letter of E21/E22's law — but it
discards the domain type at the exact site where the type carries the meaning. Whether that is
right is yours; I am reporting it, not ruling it.

**`canon_gate.py`'s own calibration docstring is stale on four measured claims** — it says 16
where the measurement is now 14, 6 where it is 5, "is 20" against a measured 19, and carries a
"neither count moved" line that no longer holds. **The router's self-description disagrees with
the router**, and the calibration claim is what a reader trusts first. This was blocked by a
fence last round and is now unowned.

## What to build

Your call on scope as always, but the shape I would defend:

1. **A fail-closed decision at every spend site**, with a named, explicit, logged escape for
   the subjects that genuinely have no canon. Silence is the thing to kill — a run that
   proceeds ungated should say so in its own output.
2. **The four ungated sites**, or a reasoned refusal of any of them. `e12_pair_cloud_step` is
   the one that authors a *paid* graph, so it is the one that matters most;
   `e37_fire_repaints` is a semantics question and a refusal there would be well-founded.
3. **`texpass_loop.ps1`** — the shipped driver that walks past the gate. A PowerShell caller is
   a transport, not a guard, and the repo's own law says the check lives inside the tool that
   performs the irreversible step.
4. **The stale calibration docstring**, repaired against measurement.

## Argue

1. **What does fail-closed mean for a subject with no canon?** An explicit `--no-canon`
   acknowledgement, a profile field that must be present-and-null, a census-backed refusal
   that names the subject, or something better. Whatever you pick, say what stops it becoming
   the checkbox everyone passes — that is the same trap you named in #17 and answered well.
2. **Is `e37_fire_repaints` gateable at all?** It replays a *recorded* prompt. Gating a
   recorded prompt against a canon that has since been corrected would refuse a faithful
   replay — and t87 just measured exactly that drift (a recorded ARMB string that was 16-of-17
   when written and is 14-of-19 now, entirely because the canon moved under it). A replay and a
   fresh generation may want different verdicts, and if so, say what the second verdict is and
   why it is not a warn-shaped checkbox.
3. **Where does the boundary honestly sit?** The MCP submission transport has no in-repo gate.
   Is "authoring-time only" the correct and permanent boundary, or is there a submission-time
   check that is not theatre? State the boundary sentence plainly — the last one went on the
   front page and earned it.
4. **`AssertionError` vs the typed ANDON** at the three sites. Consistency with the other 88
   converted sites, or a reason the canon path differs.
5. **Anything unnamed.** Eight rounds running you have cut a brief down and been right.

## Constraints

No GPU, no cloud generation, **no credits**. Read `E:\AI\training\facet_E*\`; write to none of
them. Change-set uncommitted for the advisor's fold. Gates `raise`, never a bare `assert`;
`IMPLEMENTATION:`-labelled asserts are allowed and must say why. Tests ride the commit.

**Next free test file is `t94`.**

⚠ **An Opus seat is live in this tree** working under `E:\AI\training\facet_E55\` on whether
the plates already paid for can separate element *count* from element *identity* — the density
question you left open in #19, settled without credits or shown unsettleable. **It is fenced
OFF `tools/canon_gate.py` and `tools/canon_worksheet.py`; those are yours.** It has `t95`. It
writes `docs/experiments/E55-density-vs-identity-report.md`.

**Count surfaces are at 1295 / 1241 / 54.** State what your change-set assumes; the advisor
reconciles after both land. Do not touch `docs/experiments/E55-*`.

## Calibration

Nominate **one checkable claim** we verify by running it before anything trusts the rest.
Nineteen for nineteen, and a round where the chip loses is still reported.
