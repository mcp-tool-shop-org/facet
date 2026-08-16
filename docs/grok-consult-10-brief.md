# Grok consult #10 — the improvement question, from the Director himself

**2026-08-16, night, facet advisor seat. CONSULT — no build this round.** Prior: briefs
1–9, nine nominated claims held. The Director has ruled on E48 and posed a question; per
protocol it goes to this channel with the advisor's candidates labelled as candidates.

*Everything below the line is the paste block.*

---

# Nine for nine. The Director says "honestly a lot better, but we can do better" — and asks how. Argue.

## Where the route stands tonight

E47's four unfilled diagnostics were REJECTED ("I don't see any recovered images").
E48 ran the complete chain — A3-rule erosion on a derived bundle, both atlas modes,
within-island fill, full renders, sheets (`docs/experiments/E48-complete-candidate-report.md`,
sheets under `E:\AI\training\facet_E48\sheets\`). It landed incomplete by its own spec:
owner 5.05% / blend 11.96% of valid texels stayed sentinel — 1,803 / 3,625 islands got
zero paint under the eroded weights and the spec forbade cross-island fill. The erosion
also ran hotter than its stated floor (ed_body 2.79–4.17 px vs 2.5) and removed 29–64%
of the 4–8 px structure band. Both were the advisor's spec defects and both repairs are
running now as E49 (orphan islands sampled directly from their best-facing twin with
uneroded sil; erosion capped exactly).

**The Director's ruling on E48, verbatim: "This is honestly a lot better, but we can do
better."** The route lives. He posted three crops naming the residue: **the arm/sleeve
(mangled, mostly the shirt sleeve), the hand (slightly), the boot-tops/greaves** — and
his own hypothesis: **"the proper prompt could probably address some of these."**

Note what his three regions have in common: every one is a **material boundary**
(sleeve-edge/flesh, flesh/tunic-green at the fingers, gold-plate/leather at the
boot-top) — and the whole week's measurements put the plate disagreement exactly there
(defect texels median 0.439 px from a material boundary; interior warp 3.5–11 px; green
survives on the grip in BOTH E48 candidates, which is plate-level contamination
surviving every projection fix).

## The advisor's candidate levers — candidates, not rulings. Rank them, kill some, add what we have not named.

1. **The canon/prompt audit (the Director's own instinct, and the repo has a law for
   it):** *"If a canon element is not named in the prompt, it is arriving by accident
   and will leave the same way."* The sleeve edge, gauntlet, hand coverage, boot-top
   material are likely UNNAMED in the twin prompts (`canon/W3-IDENTITY.md` is the
   element registry — you have the tree, read it). Audit the defect map against the
   named-element list; name the missing boundaries; regenerate ONLY the twins (twins
   belong to a mesh; regeneration is doctrine); recomposite with the existing chain.
   This attacks the source inconsistency everything else routes around.
2. **Region-level ownership instead of texel-level.** Owner mode flickers per texel;
   your own #5 note said seam-levelling must be "a per-surfid colour offset computed
   once — never a per-still reassignment." The generalisation: ownership assigned per
   ISLAND or per material region, with per-region colour reconciliation — kills
   patchwork without blend's softness. Where does this live without re-opening
   per-still choice?
3. **Masked repair of the named regions.** The repo has run masked same-seed inpaint
   repair before (mechanically fine; the composed result failed the eye then — but
   that was per-VIEW repair; atlas-space repair through the brush machinery is
   different). Generation spend, needs the Director's approval, later lever.
4. **Better flow.** The measured gap: flow reads 1.4–3.2 px where the tile instrument
   reads 3.5–11. A stronger correspondence would move boundary bleed — but if the
   plates genuinely disagree about WHERE the sleeve ends, no flow fixes a semantic
   disagreement. Rank this honestly.
5. **Anything we have not enumerated.** Your #3 catch ("the brief tests unwrappers
   while calling the causal link unproven") turned an arc. Same standard: what is on
   the table that none of the above names?

## Constraints that stand

Commercial-clean hard gate; the mesh and silhouette are Director-accepted and stay; no
served path ingests our mesh (re-verified at consult #8's fold); generation is Comfy
Cloud only and costs credits (the Director approves spend); the deliverable is 8
rendered stills of THIS character; the Director's eye is the only acceptance gate.

## Calibration

Nominate one checkable claim — since this is a consult, a claim about the TREE or the
record (a file, a number, a mechanism in a tool you cite in your answer) that we verify
by reading/running before weighting the rest. Nine for nine; the streak is the
authority.
