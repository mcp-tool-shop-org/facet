"""E11 — emit the dense-turnaround tree's asset-source.json (the lane's contract).

Self-contained by construction: every path the manifest references is copied INTO the
export tree (sha256 recorded before and after the copy, compared) because the lane
contains manifest paths to the manifest's own directory. The staged 3-render manifest
at the subject root is NOT touched — it is another session's artifact awaiting the
Director's paste; which manifest that paste uses is his call, flagged in the report.

Contract details this file owns:
  - render ids sanitized to the lane's [A-Za-z0-9._-]+ allowlist (job keys carry '+',
    ids cannot; paths keep the job-key names).
  - the suspension translation at the boundary (E04 Ruling 29): canon's null blob
    bound becomes the whole-atlas sentinel 16777216, derived nowhere, gating nothing.
  - render-space npy is not legal in lane schema 1.x, so per-view owner_id_*.npy
    files ride as UNDECLARED files beside the declared channels, named in a manifest
    note — translate at the boundary, annotate, file the schema item (Ruling 29
    pattern) rather than teach either side the other's business.

  e11_manifest.py --subject ship|w3
"""
import argparse
import hashlib
import json
import os
import shutil

import numpy as np

J = os.path.join
STROKE = r"E:\AI\training\facet_next\E04_stroke"
W3_ROOT = r"E:\AI\training\facet_E08\ARMB"

SUBJECTS = {
    "ship": {
        "tree": J(STROKE, "export", "turnaround"),
        "staged_manifest": J(STROKE, "asset-source.json"),
        "asset_id": "e04_galleon_dense",
        "copies": {
            "mesh.glb": J(STROKE, "out", "galleon_final.glb"),
            "atlas.png": J(STROKE, "out", "galleon_final.png"),
            "provenance_atlas.png": J(STROKE, "export", "provenance_atlas.png"),
            "view_owner.npy": J(STROKE, "export", "view_owner.npy"),
            "styled_mask.npy": J(STROKE, "state", "styled_mask.npy"),
            # item 6: EVERY clay <-> styled-twin pair, linked losslessly. The ship's
            # eight live in E04_armT72 (the ruled 1072-frame generation; twin_7 is the
            # accepted re-roll — the rejected one stays in the record under its seed
            # suffix and is not a pair).
            **{f"pair_clay_y+{i*45:03d}_e+00.png":
               J(r"E:\AI\training\facet_next\E04_armT72", "clay", f"galleonclay_{i}.png")
               for i in range(8)},
            **{f"pair_twin_y+{i*45:03d}_e+00.png":
               J(r"E:\AI\training\facet_next\E04_armT72", "twins", f"twin_{i}.png")
               for i in range(8)},
        },
        "pairs": {f"y+{i*45:03d}_e+00": {"clay": f"pair_clay_y+{i*45:03d}_e+00.png",
                                         "twin": f"pair_twin_y+{i*45:03d}_e+00.png"}
                  for i in range(8)},
        "prov_atlas_encoding": "indexed",
        "owner_channel": True,
        "run_json": "x1_run.json",
        "class_palette": [("background", (0, 0, 0)), ("reference", (46, 176, 88)),
                          ("brush", (40, 110, 235)), ("dilation", (232, 132, 32))],
    },
    "w3": {
        "tree": J(W3_ROOT, "export", "turnaround"),
        "staged_manifest": J(W3_ROOT, "asset-source.json"),
        "asset_id": "w3_warrior_dense",
        "copies": {
            "mesh.glb": J(W3_ROOT, "out", "W3_final.glb"),
            "atlas.png": J(W3_ROOT, "out", "atlas_final.png"),
            "provenance_atlas.png": None,   # filled below: the X2-proven indexed file
            "styled_mask.npy": J(W3_ROOT, "state", "styled_mask.npy"),
            # item 6 on W3: eight styled twins (twin_2/twin_6 are the accepted
            # re-rolls; the rejected ones stay in the record under their seed
            # suffix), three clay renders on disk (views 0/4/6).
            **{f"pair_twin_y+{i*45:03d}_e+00.png":
               J(W3_ROOT, "twins", f"twin_{i}.png") for i in range(8)},
            "pair_clay_y+000_e+00.png": J(W3_ROOT, "out", "renders_clay", "clay_0.png"),
            "pair_clay_y+180_e+00.png": J(W3_ROOT, "out", "renders_clay", "clay_4.png"),
            "pair_clay_y+270_e+00.png": J(W3_ROOT, "out", "renders_clay", "clay_6.png"),
        },
        "pairs": {
            **{f"y+{i*45:03d}_e+00": {"twin": f"pair_twin_y+{i*45:03d}_e+00.png"}
               for i in range(8)},
            "y+000_e+00": {"twin": "pair_twin_y+000_e+00.png",
                           "clay": "pair_clay_y+000_e+00.png"},
            "y+180_e+00": {"twin": "pair_twin_y+180_e+00.png",
                           "clay": "pair_clay_y+180_e+00.png"},
            "y+270_e+00": {"twin": "pair_twin_y+270_e+00.png",
                           "clay": "pair_clay_y+270_e+00.png"},
        },
        "prov_atlas_encoding": "indexed",
        "owner_channel": False,             # honestly absent — never synthesized
        "run_json": "x2_run.json",
        "class_palette": [("background", (0, 0, 0)), ("reference", (60, 200, 110)),
                          ("brush", (70, 170, 255)), ("dilation", (235, 120, 40))],
    },
}
SUBJECTS["w3"]["copies"]["provenance_atlas.png"] = J(
    SUBJECTS["w3"]["tree"], "provenance_atlas_indexed.png")

# ── the dragon: dataset asset #3, and the first manifest born DECLARING ──────
# Schema 1.3.0 (E11 addenda 4). Four blocks the prior two subjects' manifests
# could not carry: identity.subject_name, asset.style, asset.tone_transform and
# asset.render_derivation. All four are OPTIONAL inputs to this tool — a subject
# that does not supply one emits nothing for it, which is what keeps the galleon
# and W3 manifests byte-identical through this change.
#
# There is NO staged 3-render manifest for this subject (the first two inherited
# source/acceptance/palette/captions from one), so those blocks are supplied
# directly — the palette READ FROM CANON at runtime rather than transcribed.

DRAGON_ROOT = r"E:\AI\training\facet_next\E13_stroke"
DRAGON_RUN = J(DRAGON_ROOT, "run")
DRAGON_TWINS = r"E:\AI\training\facet_next\E13_twins"
DRAGON_CLAY = r"E:\AI\training\facet_next\E12_pair\clay"
FACET_REPO = r"E:\AI\facet"

# THE RULED PROJECTION INPUT SET (E12 Ruling 23f), read off the recorded
# invocation E13_stage1\run_stage1.ps1 rather than from memory: v9 x6 + view 3's
# 770701 CURE + view 4-A, all harmonized toward reference view 1. Seven rows live
# in harmonize\operands.json; view 3's cure lives in harmonize\operands_v3r.json,
# because 23f adopted the 770701 artifact after the first harmonization ran.
# Declaring either file alone would describe a transform that did not produce
# these projection sources, so the two are ASSEMBLED (build_tone_operands below)
# with every row carried verbatim and proved against the file it came from.
DRAGON_HARM = [
    # view, source operands file, row key, the harmonized PNG A0 consumed
    (0, "operands.json",     "v0",  "dragonclay_0_twin_v9_harm.png"),
    (1, "operands.json",     "v1",  "dragonclay_1_twin_v9_harm.png"),
    (2, "operands.json",     "v2",  "dragonclay_2_twin_v9_harm.png"),
    (3, "operands_v3r.json", "v3r", "dragonclay_3_twin_v9_s770701_harm.png"),
    (4, "operands.json",     "v4",  "dragonclay_4_twin_v8_harm.png"),
    (5, "operands.json",     "v5",  "dragonclay_5_twin_v9_harm.png"),
    (6, "operands.json",     "v6",  "dragonclay_6_twin_v9_harm.png"),
    (7, "operands.json",     "v7",  "dragonclay_7_twin_v9_harm.png"),
]
DRAGON_REF_VIEW = 1          # verified against E12_gate0\frame_00003.json at emit


def dragon_palette():
    """The palette block, READ from canon and translated at the boundary.

    canon/E12-beast-palette.json suspends BOTH gate bounds on purpose. The lane
    schema allows null for the percentage and requires an integer for the blob
    bound, so the suspension is translated into the whole-atlas sentinel — a
    value no connected component can reach, gating nothing, and unmistakable for
    a measured threshold (the E04 Ruling 29 pattern, third application)."""
    src = J(FACET_REPO, "canon", "E12-beast-palette.json")
    c = json.load(open(src, encoding="utf-8"))
    gate = c["gate"]
    assert gate["max_offpalette_blob_px"] is None, (
        "ANDON: canon now carries a measured blob bound — the suspension "
        "translation below would silently overwrite it")
    return {
        "source": "E:/AI/facet/canon/E12-beast-palette.json",
        "min_chroma": c["min_chroma"],
        "allowed_bands": [{"name": b["name"], "hue_deg": list(b["hue_deg"])}
                          for b in c["allowed_bands"]],
        "gate": {"max_offpalette_pct": gate["max_offpalette_pct"],
                 "max_offpalette_blob_px": 16777216},
        "_max_offpalette_blob_px_IS_A_SUSPENSION_ENCODING":
            "NOT A DERIVED BOUND AND NOT A THRESHOLD. canon/E12-beast-palette.json "
            "declares BOTH bounds null on purpose (E12 Ruling 15: this subject had "
            "no clean twin baseline when its bands were derived, and inventing one "
            "while looking at the artifacts it would judge is the move this repo has "
            "paid for three times). The sdlab schema requires an integer here while "
            "allowing null for max_offpalette_pct, so this tool TRANSLATES the "
            "suspension at the boundary into 16777216 - the whole 4096x4096 atlas, a "
            "value no connected component can reach - so the consumer receives a "
            "bound that gates nothing and cannot be mistaken for a measured "
            "threshold. Canon keeps its nulls. Third application of the E04 Ruling "
            "29 pattern.",
        "_the_blue_violet_stratum_is_NOT_a_band":
            "canon records a suspended blue-violet stratum (273.4-293.4, pair-realised "
            "D3) in a key palette_gate.py does not read, so a suspended band can never "
            "be silently armed. It is not exported as an allowed band here for the same "
            "reason (E12 Ruling 15c).",
    }


def build_tone_operands(tree, no_copy=False):
    """Assemble the per-view harmonization operands the RULED projection consumed.

    Two recorded files, eight rows, every row carried VERBATIM from its source and
    proved three ways: the row exists under its recorded key; the harmonized PNG it
    names is on disk; and that PNG's sha256 equals the row's own sha256_out — so the
    operands demonstrably describe the file that was projected, not a namesake.
    Both source files are also copied into the tree undeclared, so a ruling that
    prefers a different declaration has them in hand with no re-run.

    no_copy=True is the READ-ONLY mode the anchor comparison needs (E14 handoff 10
    P2b): a prior subject's committed tree must not be opened for writing to
    re-emit its manifest, and this function otherwise writes three files into it
    unconditionally. In that mode nothing is written — the sidecar and both sources
    already on disk are VERIFIED instead, which is strictly more checking than the
    write path does."""
    hz = J(DRAGON_TWINS, "harmonize")
    srcs, rows = {}, {}
    for name in ("operands.json", "operands_v3r.json"):
        srcs[name] = {"path": f"_operands_sources/{name}", "sha256": sha256(J(hz, name)),
                      "content": json.load(open(J(hz, name), encoding="utf-8"))}
    refs = {n: s["content"]["_reference"]["sha256"] for n, s in srcs.items()}
    assert len(set(refs.values())) == 1, \
        f"ANDON: the two operands files name different reference twins: {refs}"

    for view, fname, key, png in DRAGON_HARM:
        row = srcs[fname]["content"]["views"].get(key)
        assert row is not None, f"ANDON: {fname} has no row '{key}'"
        p = J(hz, png)
        assert os.path.exists(p), f"ANDON: harmonized source {p} is missing"
        got = sha256(p)
        assert got == row["sha256_out"], (
            f"ANDON: {png} hashes {got[:12]} but row {key} of {fname} records "
            f"{row['sha256_out'][:12]} — the operands do not describe this file")
        assert os.path.basename(row["output"].replace("\\", "/")) == png, \
            f"ANDON: row {key} names output {row['output']}, not {png}"
        rows[f"view_{view}"] = dict(row, _source_file=fname, _source_key=key)

    ref_row = rows[f"view_{DRAGON_REF_VIEW}"]
    assert ref_row["is_reference"] is True, \
        f"ANDON: view {DRAGON_REF_VIEW} is not flagged is_reference in its own row"
    assert ref_row["sha256_out"] == list(refs.values())[0], \
        "ANDON: the reference row's output does not hash to the declared reference twin"

    out = {
        "_what":
            "The per-view operands of the Lab colour-statistics harmonization "
            "(E12 Ruling 22e, ADOPTED at 23f) that produced the eight projection "
            "sources stage 1 consumed. ASSEMBLED, not original: the ruled input set "
            "is v9 x6 + view 3's 770701 cure + view 4-A, and the cure was harmonized "
            "in a second pass, so its row lives in a second file. Every row below is "
            "carried verbatim from the file named in its _source_file, and both "
            "source files ride beside this one under _operands_sources/ unchanged.",
        "_assembled_from": {n: {"path": s["path"], "sha256": s["sha256"]}
                            for n, s in srcs.items()},
        "_the_recorded_invocation":
            "E:/AI/training/facet_next/E13_stage1/run_stage1.ps1 (the A0 run, ruled "
            "as stage 1 by E12 Ruling 24) names these eight files by view index.",
        "_reference": dict(list(srcs.values())[0]["content"]["_reference"],
                           view_index=DRAGON_REF_VIEW),
        "_limit": list(srcs.values())[0]["content"]["_limit"],
        "views": rows,
    }
    dest_dir = J(tree, "_operands_sources")
    path = J(tree, "tone_transform_operands.json")
    if no_copy:
        for name in srcs:
            p = J(dest_dir, name)
            assert os.path.exists(p), f"ANDON: --no-copy but {p} is missing"
            assert sha256(p) == srcs[name]["sha256"], \
                f"ANDON: {p} no longer matches its source {J(hz, name)}"
        assert os.path.exists(path), f"ANDON: --no-copy but {path} is missing"
        have = open(path, encoding="utf-8").read()
        if have != json.dumps(out, indent=1):
            raise SystemExit(
                f"ANDON: {path} differs from what this tool would assemble — "
                f"the operands sidecar in the tree is not this code's output")
        print(f"[manifest] tone operands VERIFIED in place (read-only): "
              f"{len(rows)} views, sidecar content identical, "
              f"{len(srcs)} sources sha-matched; nothing written")
        return "tone_transform_operands.json"
    os.makedirs(dest_dir, exist_ok=True)
    for name in srcs:
        shutil.copyfile(J(hz, name), J(dest_dir, name))
        assert sha256(J(dest_dir, name)) == srcs[name]["sha256"], \
            f"ANDON: copy of {name} changed bytes"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(f"[manifest] tone operands assembled: {len(rows)} views from "
          f"{len(srcs)} recorded files, every row hash-proved against its PNG")
    return "tone_transform_operands.json"


SUBJECTS["dragon"] = {
    "tree": J(DRAGON_ROOT, "export", "turnaround"),
    "staged_manifest": None,       # no staged manifest exists for this subject
    "asset_id": "e12_dragon_dense",
    "schema_version": "1.3.0",
    "identity": {"subject_name": "dragon"},
    # E12 Ruling 10b, earned at Ruling 14. The terms are canon/DRAGON-IDENTITY.md's
    # STYLE-SUPPLIED row verbatim; lora NONE is beast.json's lora-w 0.0 expressed as
    # the positive declaration the lane requires (no card may ride beside it).
    "style": {
        "register": {
            "terms": ["ultra-realistic", "menacing"],
            "ruling": "E12 Ruling 10b",
            "record": "E:/AI/facet/canon/DRAGON-IDENTITY.md STYLE-SUPPLIED; "
                      "E:/AI/facet/docs/style-registers.md",
        },
        "lora": {"declared": "none"},
    },
    "tone_transform": {
        "kind": "lab-stats-transfer",
        "space": "CIELAB",
        "scope": "figure-mask",
        "reversible": True,
        "record": "E:/AI/facet/docs/experiments/E12-ruling.md Rulings 22e (the "
                  "instrument), 23f (adopted - projection consumes the harmonized "
                  "set). First and second moments only, inside the exact figure "
                  "mask, toward reference view 1; sdlab records this claim and "
                  "verifies neither application nor reversibility, which is the seam.",
    },
    "render_derivation": {"kind": "emit", "generated": False,
                          "record": "E11 Ruling 2"},
    "blocks": {
        "source": "facet/E12",
        "acceptance": {
            "gate": "gate-1",
            "verdict": "accepted",
            "date": "2026-08-07",
            "record": "E:/AI/facet/docs/experiments/E12-ruling.md Ruling 28 "
                      "(\"Fantastic!! This is really good!\") - judged artifact: "
                      "E13_stroke/run/dragon_hero.glb at the Director's own zoom in "
                      "Blender, three views returned with the verdict "
                      "(three-quarter front, left profile, top-down rear over the "
                      "wings - that last one mostly surface no eye-level camera "
                      "reaches). Three items were named before his eye and none was "
                      "named back.",
            "by": "director",
        },
        "captions": {
            "subject": "a winged quadruped dragon with deep moss-green scaled hide, "
                       "pale olive-tan banded ventral plates, leathery storm-grey "
                       "wing membranes, bone-ivory back-swept horns, a bone-ivory "
                       "crown and cheek spike ring, charcoal neck dorsal and tail "
                       "spines, charcoal claws, ember-orange eyes, a dark wine-red "
                       "tongue, pale ivory fangs and tooth rows, and a dark slate "
                       "mouth interior",
            "style_trigger": None,
            "domain_tag": "3d asset",
        },
    },
    "copies": {
        "mesh.glb": J(DRAGON_RUN, "dragon_hero.glb"),
        "atlas.png": J(DRAGON_RUN, "dragon_final.png"),
        "provenance_atlas.png": None,   # filled below: the X3-proven indexed file
        "view_owner.npy": J(r"E:\AI\training\facet_next\E13_stage1",
                            "A0_stage1_owner.npy"),
        "styled_mask.npy": J(DRAGON_RUN, "state", "styled_mask.npy"),
        # item 6: the eight clay <-> styled-twin pairs. The twin side is the
        # HARMONIZED image - the ruled projection source (23f), the one this asset's
        # paint actually came from. The raw twins stay in the E13 record.
        **{f"pair_clay_y+{i*45:03d}_e+00.png": J(DRAGON_CLAY, f"dragonclay_{i}.png")
           for i in range(8)},
        **{f"pair_twin_y+{v*45:03d}_e+00.png": J(DRAGON_TWINS, "harmonize", png)
           for v, _f, _k, png in DRAGON_HARM},
    },
    "pairs": {f"y+{i*45:03d}_e+00": {"clay": f"pair_clay_y+{i*45:03d}_e+00.png",
                                     "twin": f"pair_twin_y+{i*45:03d}_e+00.png"}
              for i in range(8)},
    "prov_atlas_encoding": "indexed",
    "owner_channel": True,
    # third configuration: the NUMERIC owner channel is native to this subject, but
    # no owner DISPLAY atlas was ever built for it, so the owner_view render channel
    # is honestly absent rather than synthesized (galleon: both; W3: neither).
    "owner_display": False,
    "run_json": "x3_run.json",
    "class_palette": [("background", (16, 16, 18)), ("reference", (118, 146, 110)),
                      ("brush", (240, 176, 48)), ("dilation", (150, 90, 150))],
    "palette_fn": dragon_palette,
    "tone_ops_fn": build_tone_operands,
    "ref_view": DRAGON_REF_VIEW,
    "ref_view_table": J(r"E:\AI\training\facet_next\E12_gate0", "frame_00003.json"),
}
SUBJECTS["dragon"]["copies"]["provenance_atlas.png"] = J(
    SUBJECTS["dragon"]["tree"], "provenance_atlas_indexed.png")
for _s in ("ship", "w3"):
    SUBJECTS[_s]["owner_display"] = SUBJECTS[_s]["owner_channel"]


# ── the longsword: dataset asset #4, the route's fourth subject CLASS ────────
# Schema 1.3.0. Two things are new here and both are the subject's, not the
# contract's: the provenance atlas carries FIVE non-background classes (the stone
# kept as its own sub-class, Rulings 30/31b), and the tone transform is a MASKED
# PER-VIEW HUE ROTATION on four of eight generation views rather than the dragon's
# whole-figure Lab statistics transfer. The contract's fields take honest values
# for it (E14 handoff 10 P8, registered before this was written).

LS_ROOT = r"E:\AI\training\facet_next\E14_strokes"
LS_FINAL = J(LS_ROOT, "run", "final")
LS_GARNET = J(LS_ROOT, "garnet")
LS_PREP = r"E:\AI\training\facet_next\E14_prep"
LS_TWINS = J(LS_PREP, "twins", "out")
LS_CLAY = J(LS_PREP, "renders")

# Views 2 and 6 have NO accepted twin (E14 Ruling 20 — the Director's own overrule
# excluded view 6; view 2 was never accepted), so six pairs, not eight.
LS_VIEWS = [0, 1, 3, 4, 5, 7]
# THE APPLIED SET (E14 Ruling 26c/5): the four DRIFTED twins go in corrected at the
# ruled rotations; the garnet pair (0/4) goes in UNROTATED — "the *original* files,
# not my corrected copies" (E14-handoff7-garnet-reprojection-report.md §2). The
# corrected 0/4 artifacts exist as the derivation's NEAR-NO-OP CONTROLS and are
# recorded as computed-not-applied, never as projection sources.
LS_ROTATED = {1: 51.80, 3: 34.47, 5: 55.45, 7: 48.01}
LS_CONTROLS = [0, 4]
LS_REF_VIEW = 0        # verified against E14_prep/masks/silhouettes.json at emit


def longsword_palette():
    """The palette block, READ from canon and translated at the boundary.

    canon/E14-longsword-palette.json suspends BOTH gate bounds (E14 Ruling 17d:
    report-only, no clean baseline until this subject's own twins existed). Fourth
    application of the E04 Ruling 29 pattern."""
    src = J(FACET_REPO, "canon", "E14-longsword-palette.json")
    c = json.load(open(src, encoding="utf-8"))
    gate = c["gate"]
    assert gate["max_offpalette_blob_px"] is None and gate["max_offpalette_pct"] is None, (
        "ANDON: canon now carries a measured bound — the suspension translation "
        "below would silently overwrite it")
    lav = [b for b in c["allowed_bands"] if b["name"] == "lavender-rim"]
    assert len(lav) == 1, "ANDON: the lavender-rim admission is not in canon's allowed_bands"
    return {
        "source": "E:/AI/facet/canon/E14-longsword-palette.json",
        "min_chroma": c["min_chroma"],
        "allowed_bands": [{"name": b["name"], "hue_deg": list(b["hue_deg"])}
                          for b in c["allowed_bands"]],
        "gate": {"max_offpalette_pct": gate["max_offpalette_pct"],
                 "max_offpalette_blob_px": 16777216},
        "_max_offpalette_blob_px_IS_A_SUSPENSION_ENCODING":
            "NOT A DERIVED BOUND AND NOT A THRESHOLD. canon/E14-longsword-palette.json "
            "declares BOTH bounds null on purpose (E14 Ruling 17d: this subject had no "
            "clean twin baseline when its bands were derived, and its only known-bad "
            "artifact fails by OCCUPANCY - gold on the blackened-iron crossguard - which "
            "a colour-not-placement gate is structurally blind to). The sdlab schema "
            "requires an integer here while allowing null for max_offpalette_pct, so this "
            "tool TRANSLATES the suspension at the boundary into 16777216 - the whole "
            "4096x4096 atlas, a value no connected component can reach - so the consumer "
            "receives a bound that gates nothing and cannot be mistaken for a measured "
            "threshold. Canon keeps its nulls. Fourth application of the E04 Ruling 29 "
            "pattern.",
        "_the_lavender_rim_band_is_a_RIM_ADMISSION_not_a_material":
            "It IS exported (canon puts it in allowed_bands, which palette_gate.py reads - "
            "unlike the dragon's suspended blue-violet stratum, which canon deliberately "
            "keeps in a key the gate does not read). E14 Ruling 17c admitted it so the "
            "gate's numbers mean something on accepted work: the realised backdrop sits at "
            "C* 32.6-37.1, far above the floor, so its antialiased rim mixing is a real "
            "above-floor hue population INSIDE the silhouette. It covers NO declared "
            "material - 92.8% of its support is rim pixels at median depth 1.00 px, against "
            "wine at 8.0% and gold at 0.3%. The blindness it buys (interior backdrop-family "
            "arrivals, and a DRIFTED declared material - the gem did exactly that at seed "
            "770701) is watched by the standing DEPTH diagnostic, not by hue.",
        "_the_perimeter_law": c["_the_perimeter_law_bites_hardest_here"]
            if "_the_perimeter_law_bites_hardest_here" in c else None,
    }


def build_ls_tone_operands(tree, no_copy=False):
    """Assemble the operands of the GARNET RE-PROJECTION's hue rotation.

    Two recorded files hold the same operand and the assembly ASSERTS they agree:
    garnet_operands_final.json's per-view rows and T3_rotations.npy's array. Every
    row is carried verbatim; the four APPLIED rows are separated from the two
    COMPUTED-NOT-APPLIED controls, because the ruled disposition (Ruling 26c/5) is
    that the garnet pair went in unrotated and a reader must not count six.

    The claims the manifest makes about this transform are checked here against the
    file rather than asserted: C* and L identical before and after in every row is
    what makes `space: CIELAB` (a rotation about the achromatic axis) and
    `reversible: true` sourced statements rather than adjectives."""
    src = J(LS_GARNET, "garnet_operands_final.json")
    ops = json.load(open(src, encoding="utf-8"))
    rot = np.load(J(LS_GARNET, "T3_rotations.npy"))
    rot_by_view = {int(v): float(d) for v, d in rot}

    rows, controls = {}, {}
    for view in LS_VIEWS:
        key = f"T3|{view}"
        row = ops["T3_hue_rotation"].get(key)
        assert row is not None, f"ANDON: garnet_operands_final.json has no row '{key}'"
        assert row["view"] == view, f"ANDON: row {key} carries view {row['view']}"
        assert view in rot_by_view, f"ANDON: T3_rotations.npy has no row for view {view}"
        assert abs(row["rotation_deg"] - rot_by_view[view]) < 1e-9, (
            f"ANDON: view {view} rotation is {row['rotation_deg']} in the operands JSON "
            f"and {rot_by_view[view]} in T3_rotations.npy — two records of one operand "
            f"disagree")
        assert row["C_before"] == row["C_after"] and row["L_before"] == row["L_after"], (
            f"ANDON: view {view} moved C* or L ({row['C_before']}->{row['C_after']}, "
            f"{row['L_before']}->{row['L_after']}) — the transform is not the "
            f"hue-only rotation the manifest declares")
        tagged = dict(row, _source_file="garnet_operands_final.json", _source_key=key)
        if view in LS_ROTATED:
            assert abs(row["rotation_deg"] - LS_ROTATED[view]) < 1e-9, (
                f"ANDON: view {view} rotation {row['rotation_deg']} is not the ruled "
                f"{LS_ROTATED[view]} (E14 Ruling 26c/5)")
            png = f"TWIN_swordclay_{view}_garnet.png"
            p = J(LS_GARNET, "corrected", png)
            assert os.path.exists(p), f"ANDON: corrected twin {p} is missing"
            tagged.update(_applied=True, _projection_source=f"_operands_sources/{png}",
                          _projection_source_sha256=sha256(p))
            rows[f"view_{view}"] = tagged
        else:
            tagged.update(_applied=False, _why=(
                "COMPUTED AS A NEAR-NO-OP CONTROL AND DELIBERATELY NOT APPLIED. E14 "
                "Ruling 26c/5: the garnet pair's stones are the identity family "
                "already, and rotating accepted-family paint toward the reference's "
                "exact mean would 'correct' the medium's own roll variance (the "
                "measured ~25 deg same-seed floor), which is not a defect. The "
                "re-projection consumed the ORIGINAL files for these two views "
                "(E14-handoff7-garnet-reprojection-report.md section 2)."))
            controls[f"view_{view}"] = tagged
    assert sorted(rows) == [f"view_{v}" for v in sorted(LS_ROTATED)], \
        f"ANDON: applied set is {sorted(rows)}, not the four ruled views"
    worst_control = max(controls[k]["median_dE_stone"] for k in controls)
    best_applied = min(rows[k]["median_dE_stone"] for k in rows)
    assert worst_control < best_applied, (
        f"ANDON: a not-applied control moved the stone more ({worst_control}) than the "
        f"smallest applied rotation ({best_applied}) — 'near-no-op' is not what these "
        f"rows describe")

    ref = dict(ops["reference"], view_index=LS_REF_VIEW)
    assert os.path.basename(ref["path"].replace("\\", "/")) == \
        f"PAIR_swordclay_{LS_REF_VIEW}.png", \
        f"ANDON: the reference path {ref['path']} is not the pair's view {LS_REF_VIEW}"

    sources = {"garnet_operands_final.json": J(LS_GARNET, "garnet_operands_final.json"),
               "T3_rotations.npy": J(LS_GARNET, "T3_rotations.npy"),
               "garnet_derivation.json": J(LS_GARNET, "garnet_derivation.json")}
    sources.update({f"TWIN_swordclay_{v}_garnet.png":
                    J(LS_GARNET, "corrected", f"TWIN_swordclay_{v}_garnet.png")
                    for v in LS_ROTATED})
    shas = {n: sha256(p) for n, p in sources.items()}

    out = {
        "_what":
            "The per-view operands of THE GARNET RE-PROJECTION's hue rotation (E14 "
            "Ruling 25d, operands RULED at 26c) — the deterministic, generation-free "
            "colour operation that produced four of the six projection sources the "
            "stone territory's paint came from. T3: a per-view rotation of hue about "
            "the achromatic axis with C* and L preserved exactly, computed over each "
            "twin's stone mask above the C* 12.0 chroma floor, toward the accepted "
            "pair's view-0 stone as reference, by the UNWEIGHTED CIRCULAR MEAN of the "
            "unit chromatic vector (an arithmetic median of hues reported +49.1 deg "
            "where the true direction was -8.4 — garnet straddles the 0/360 wrap).",
        "_scope_stated_exactly":
            "FOUR of eight generation views (1/3/5/7 — the drifted twins), inside the "
            "stone mask only, reaching 67,904 atlas texels = 1.854% of valid. Views "
            "0 and 4 carry COMPUTED rotations in _computed_not_applied below and went "
            "into the projection UNROTATED. Views 2 and 6 have no accepted twin at "
            "all. This is NOT a whole-figure transform.",
        "_assembled_from": {n: {"path": f"_operands_sources/{n}", "sha256": shas[n]}
                            for n in sources},
        "_the_recorded_invocation":
            "E:/AI/facet/docs/experiments/E14-handoff7-garnet-reprojection-report.md "
            "(the corrected M2 run, RATIFIED at E14 Ruling 27) — the restricted write "
            "whose set was territory AND holes exactly, 0 styled texels touched, "
            "16,709,312 outside texels byte-identical.",
        "_chroma_floor": ops["chroma_floor"],
        "_hue_statistic": ops["hue_statistic"],
        "_reference": ref,
        "views": rows,
        "_computed_not_applied": controls,
        "_rim": ops.get("rim"),
    }

    dest_dir = J(tree, "_operands_sources")
    path = J(tree, "tone_transform_operands.json")
    if no_copy:
        for name in sources:
            p = J(dest_dir, name)
            assert os.path.exists(p), f"ANDON: --no-copy but {p} is missing"
            assert sha256(p) == shas[name], f"ANDON: {p} no longer matches its source"
        assert os.path.exists(path), f"ANDON: --no-copy but {path} is missing"
        assert open(path, encoding="utf-8").read() == json.dumps(out, indent=1), \
            f"ANDON: {path} differs from what this tool would assemble"
        print(f"[manifest] tone operands VERIFIED in place (read-only)")
        return "tone_transform_operands.json"
    os.makedirs(dest_dir, exist_ok=True)
    for name, p in sources.items():
        shutil.copyfile(p, J(dest_dir, name))
        assert sha256(J(dest_dir, name)) == shas[name], \
            f"ANDON: copy of {name} changed bytes"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print(f"[manifest] tone operands assembled: {len(rows)} APPLIED rotations "
          f"(views {sorted(LS_ROTATED)}), {len(controls)} computed-not-applied "
          f"controls, both records of every rotation agreeing, C* and L identical "
          f"before/after in every row")
    return "tone_transform_operands.json"


SUBJECTS["longsword"] = {
    "tree": J(LS_ROOT, "export", "turnaround"),
    "staged_manifest": None,
    "asset_id": "e14_longsword_dense",
    "schema_version": "1.3.0",
    "identity": {"subject_name": "longsword"},
    # E12 Ruling 10b's law on this subject's own register: the Director's sentence
    # at designation day one ("Ultra-realistic, no LoRA" — E14 Ruling 5a), EARNED at
    # Ruling 32a. The terms are prop.json's own prompt tail, verbatim.
    "style": {
        "register": {
            "terms": ["ultra-realistic", "worn metal", "harsh directional light"],
            "ruling": "E14 Ruling 5a; EARNED at E14 Ruling 32a",
            "record": "E:/AI/facet/canon/LONGSWORD-IDENTITY.md STYLE-SUPPLIED; "
                      "E:/AI/facet/profiles/prop.json restylize_views.py.prompt tail; "
                      "E:/AI/facet/docs/style-registers.md",
        },
        "lora": {"declared": "none"},
    },
    "tone_transform": {
        "kind": "hue-rotation",
        "space": "CIELAB",
        "scope": "stone-mask on four of eight generation views (1/3/5/7), above the "
                 "C* 12.0 chroma floor; 67,904 atlas texels = 1.854% of valid",
        "reversible": True,
        "record": "E:/AI/facet/docs/experiments/E14-ruling.md Rulings 25d (the "
                  "mechanism — the stone leaves the generation path), 26c (the five "
                  "operands decisions: treatment T3, whole-mask population, no chroma "
                  "operand, unweighted circular mean, six twins with the garnet pair "
                  "UNROTATED), 27 (the run ratified). A per-view rotation of hue about "
                  "the achromatic axis with C* and L preserved exactly — NOT the "
                  "dragon's whole-figure lab-stats-transfer. sdlab records this claim "
                  "and verifies neither application nor reversibility, which is the "
                  "seam.",
    },
    "render_derivation": {"kind": "emit", "generated": False,
                          "record": "E11 Ruling 2"},
    "owner_note":
        "Stage 1b's per-texel view-owner sidecar. OWNER VALUES ARE POSITIONAL INDICES "
        "INTO THE SIX-VIEW INPUT LIST [0,1,3,4,5,7], NOT route view indices — id 2 is "
        "view 3 and id 5 is view 7; views 2 and 6 have no accepted twin (E14 Ruling "
        "20). Verified positionally against stage1b_provenance_legend.json's own "
        "per-view committed counts, every count exact. It owns exactly the 1,656,847 "
        "reference-class texels (stage-1b projection + garnet re-projection + collar "
        "repair) with zero owned outside them.",
    "blocks": {
        "source": "facet/E14",
        "acceptance": {
            "gate": "gate-1",
            "verdict": "accepted",
            "date": "2026-08-08",
            "record": "E:/AI/facet/docs/experiments/E14-ruling.md Ruling 32 "
                      "(\"Fantastic! I accept\") - judged artifact: "
                      "E14_strokes/run/final/longsword_hero.glb at the Director's own "
                      "zoom in Blender, three screenshots returned with the verdict "
                      "(the hero diagonal; near edge-on from the pommel down - the "
                      "ribbon the whole stroke lane existed for, continuous steel to "
                      "the tip at his own zoom; the hilt from above at the fixture's "
                      "five elements). The route's FOURTH accepted asset and its "
                      "fourth subject class - character, ship, beast, prop - at zero "
                      "credits across the entire arc.",
            "by": "director",
        },
        "captions": {
            "subject": "a tip-standing longsword with a battle-worn steel blade and a "
                       "raised central ridge, a blackened iron crossguard, a gold "
                       "diamond boss at the crossing, gold collar rings, an oxblood "
                       "leather grip wrap, and a dark garnet gem pommel",
            "style_trigger": None,
            "domain_tag": "3d asset",
        },
    },
    "copies": {
        "mesh.glb": J(LS_FINAL, "longsword_hero.glb"),
        "atlas.png": J(LS_FINAL, "atlas_final.png"),
        "provenance_atlas.png": None,   # filled below: the X4-proven indexed file
        "view_owner.npy": J(LS_PREP, "stage1", "stage1b_atlas_owner.npy"),
        "styled_mask.npy": J(LS_FINAL, "styled_mask.npy"),
        # item 6: six clay <-> styled-twin pairs. The twin side is the ACCEPTED twin
        # AS GENERATED — what stage 1b projected, and the source of 1,588,943 of the
        # 1,656,847 reference texels. The four hue-corrected twins are the tone
        # transform's OUTPUTS and ride in _operands_sources/ with their shas.
        **{f"pair_clay_y+{v*45:03d}_e+00.png": J(LS_CLAY, f"swordclay_{v}.png")
           for v in LS_VIEWS},
        **{f"pair_twin_y+{v*45:03d}_e+00.png": J(LS_TWINS, f"TWIN_swordclay_{v}.png")
           for v in LS_VIEWS},
    },
    "pairs": {f"y+{v*45:03d}_e+00": {"clay": f"pair_clay_y+{v*45:03d}_e+00.png",
                                     "twin": f"pair_twin_y+{v*45:03d}_e+00.png"}
              for v in LS_VIEWS},
    "prov_atlas_encoding": "indexed",
    "owner_channel": True,
    "owner_display": False,   # no owner display atlas was ever built for this subject
    "run_json": "x4_run.json",
    # FIVE non-background classes: Rulings 30/31b keep the stone as its own
    # provenance sub-class, never blended into the brush's numbers.
    "class_palette": [("background", (16, 16, 18)),
                      ("stage1b_projection", (118, 146, 110)),
                      ("garnet_reprojection", (220, 60, 220)),
                      ("collar_repair", (40, 230, 230)),
                      ("brush", (240, 176, 48)),
                      ("dilation", (150, 90, 150))],
    "palette_fn": longsword_palette,
    "tone_ops_fn": build_ls_tone_operands,
    "ref_view": LS_REF_VIEW,
    "ref_view_table": J(LS_PREP, "masks", "silhouettes.json"),
}
SUBJECTS["longsword"]["copies"]["provenance_atlas.png"] = J(
    SUBJECTS["longsword"]["tree"], "provenance_atlas_indexed.png")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_id(job_key):
    return job_key.replace("+", "")


def verify_ref_view(table_path, ref_view):
    """The tone transform's reference VIEW INDEX -> yaw, checked against the
    recorded frame table rather than asserted from memory (E11 addenda 4's explicit
    instruction: a reference pointing at the wrong camera is a false provenance
    claim). Returns the verified yaw; the render id is then DERIVED from it through
    the same construction the render ids come from."""
    t = json.load(open(table_path, encoding="utf-8"))
    step = float(t["step"])
    views = t["views"]
    if isinstance(views, dict):
        row = views[str(ref_view)]
        yaw = float(row["yaw"] if isinstance(row, dict) else row)
    else:
        assert ref_view in views, f"ANDON: {table_path} records no view {ref_view}"
        yaw = ref_view * step
    assert abs(yaw - ref_view * step) < 1e-9, (
        f"ANDON: {table_path} puts view {ref_view} at yaw {yaw}, not {ref_view*step} "
        f"(step {step}) — do not re-derive, halt")
    print(f"[manifest] reference view {ref_view} = yaw {yaw:g}, verified against "
          f"{os.path.basename(table_path)} (step {step:g})")
    return yaw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", choices=list(SUBJECTS), required=True)
    ap.add_argument("--out", help="write the manifest here instead of into the tree. "
                                  "The anchor comparison uses this so a prior subject's "
                                  "committed manifest is never opened for writing.")
    ap.add_argument("--no-copy", action="store_true",
                    help="do not write into the tree: VERIFY each declared copy already "
                         "there against its source by sha256 instead. Read-only mode for "
                         "re-emitting an existing subject's manifest.")
    args = ap.parse_args()
    S = SUBJECTS[args.subject]
    tree = S["tree"]
    # subjects with a staged 3-render manifest inherit its blocks; the dragon has
    # none and supplies them directly (its palette read from canon at runtime).
    if S["staged_manifest"]:
        staged = json.load(open(S["staged_manifest"], encoding="utf-8"))
    else:
        b = S["blocks"]
        staged = {"asset": {"source": b["source"]}, "acceptance": b["acceptance"],
                  "palette": S["palette_fn"](), "captions": b["captions"]}
    run = json.load(open(J(tree, S["run_json"]), encoding="utf-8"))

    ledger = {}
    for name, src in S["copies"].items():
        dst = J(tree, name)
        if args.no_copy:
            # read-only: the copy must already be there and must match its source.
            assert os.path.exists(dst), f"ANDON: --no-copy but {dst} is missing"
            got = sha256(dst)
            if os.path.abspath(src) != os.path.abspath(dst):
                assert sha256(src) == got, \
                    f"ANDON: {dst} no longer matches its source {src}"
            ledger[name] = got
        elif os.path.abspath(src) != os.path.abspath(dst):
            want = sha256(src)
            shutil.copyfile(src, dst)
            got = sha256(dst)
            assert want == got, f"ANDON: copy of {src} changed bytes"
            ledger[name] = got
        else:
            ledger[name] = sha256(dst)
        print(f"[manifest] {name}  {ledger[name][:12]}...")

    channels = [
        {"id": "provenance_atlas", "space": "texture", "encoding": "indexed",
         "categorical": True, "filter": "nearest",
         "path": "provenance_atlas.png",
         "palette": [{"name": n, "rgb": list(rgb)} for n, rgb in S["class_palette"]],
         "note": "Indexed per E09 Amendment 1; conversion proven pixel-identical "
                 "(the run json's leg for this subject)."},
        {"id": "styled_mask", "space": "texture", "encoding": "npy",
         "categorical": False, "path": "styled_mask.npy",
         "dtype": "|b1", "shape": [4096, 4096],
         "note": "Styled/unstyled coverage before the finalize flood."},
        {"id": "provenance_view", "space": "render", "encoding": "rgb",
         "categorical": False,
         "note": "emit's flat readout of the provenance atlas — antialiased, display "
                 "form; the exact per-pixel classes are prov_class."},
        {"id": "prov_class", "space": "render", "encoding": "indexed",
         "categorical": True, "filter": "nearest",
         "palette": [{"name": n, "rgb": list(rgb)} for n, rgb in S["class_palette"]],
         "note": "EXACT per-pixel class map by texel-id raycast — born indexed, no "
                 "antialiasing, PLTE == this palette. The admission-mask source."},
    ]
    if S["owner_channel"]:
        channels.insert(2, {
            "id": "view_owner", "space": "texture", "encoding": "npy",
            "categorical": False, "path": "view_owner.npy",
            "dtype": "|i1", "shape": [4096, 4096],
            "note": S.get("owner_note") or (
                staged["channels"][1]["note"] if len(staged.get("channels", [])) > 1
                else "the native stage-1 view-owner sidecar")})
    if S["owner_display"]:
        channels.append({
            "id": "owner_view", "space": "render", "encoding": "rgb",
            "categorical": False,
            "note": "the owner display atlas at each camera; numeric truth is "
                    "view_owner.npy and the per-view owner_id_*.npy files (undeclared "
                    "— render-space npy is not in lane schema 1.x; schema item filed "
                    "per the Ruling 29 pattern)."})

    renders = []
    for row in run["renders"]:
        vid = row["id"]
        rid = safe_id(vid)
        entry = {
            "id": rid,
            "path": f"views/{vid}/asset.png",
            "camera": {"yaw_deg": row["yaw"], "elevation_deg": row["el"]},
            "light": "flat",
            "silhouette_mask": f"views/{vid}/silhouette.png",
            "channels": {"provenance_view": f"views/{vid}/prov.png",
                         "prov_class": f"views/{vid}/prov_class_{vid}.png"},
        }
        if S["owner_display"]:
            entry["channels"]["owner_view"] = f"views/{vid}/owner.png"
        if S["owner_channel"]:
            entry["loss_mask"] = f"views/{vid}/loss_mask_{vid}.png"
        if vid in S["pairs"]:
            entry["pair"] = dict(S["pairs"][vid])
        renders.append(entry)

    # ── the 1.3.0 declarations (E11 addenda 4). Every one is OPTIONAL: a subject
    # that supplies none emits none, which is what holds the galleon and W3
    # manifests byte-identical through this change (the anchor proves it).
    asset = {
        "id": S["asset_id"],
        "source": staged["asset"]["source"],
        "mesh": {"path": "mesh.glb"},
        "atlas": {"path": "atlas.png"},
    }
    if S.get("style"):
        asset["style"] = S["style"]
    if S.get("tone_transform"):
        tt = dict(S["tone_transform"])
        # the reference must resolve to a render id THIS manifest declares, or the
        # provenance dangles. Derived from the ruled reference VIEW INDEX through
        # the same key_of/safe_id construction the render ids come from — never
        # typed as a literal.
        ref_yaw = verify_ref_view(S["ref_view_table"], S["ref_view"])
        ref_vid = f"y+{int(round(ref_yaw)):03d}_e+00"
        tt["reference"] = safe_id(ref_vid)
        assert tt["reference"] in {r["id"] for r in renders}, (
            f"ANDON: the tone transform's reference {tt['reference']} is not a render "
            f"id this manifest declares — dangling provenance")
        tt["operands"] = S["tone_ops_fn"](tree, no_copy=args.no_copy)
        asset["tone_transform"] = tt
    if S.get("render_derivation"):
        asset["render_derivation"] = S["render_derivation"]

    manifest = {
        "schema_version": S.get("schema_version", "1.0.0"),
        "_authored": "E11 dense-turnaround exporter, 2026-08-05. Self-contained tree: "
                     "every referenced file lives under this directory, copies "
                     "sha256-verified from the accepted artifacts. The subject root's "
                     "staged 3-render manifest is untouched; which one the Director "
                     "pastes into the lane is his call. Per-view owner_id_*.npy and "
                     "admission_*.json ride undeclared beside the declared channels "
                     "(render-space npy/json are not lane schema 1.x concepts).",
        "asset": asset,
        "acceptance": staged["acceptance"],
        # E11 Ruling 3: the verdict covers the ASSET; renders are derivations.
        "renders_are": "post-verdict derivations of the accepted asset by the "
                       "anchored emit path — the Gate-1 verdict covers the asset "
                       "(mesh + atlas), and these renders derive from it by the "
                       "route's own anchored readout (E11 Ruling 3).",
        "palette": staged["palette"],
        "channels": channels,
        "renders": renders,
        "captions": staged["captions"],
    }
    if S.get("identity"):
        # top-level, and inserted rather than appended so the block reads beside
        # the asset it identifies. Rebuilt in order: dicts keep insertion order and
        # the byte anchor is sensitive to it.
        manifest = {k: v for pair in
                    ([("schema_version", manifest["schema_version"]),
                      ("_authored", manifest["_authored"]),
                      ("identity", S["identity"])]
                     + [(k2, v2) for k2, v2 in manifest.items()
                        if k2 not in ("schema_version", "_authored")])
                    for k, v in [pair]}
    out = args.out or J(tree, "asset-source.json")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    print(f"[manifest] wrote {out}  ({len(renders)} renders, "
          f"{len(channels)} channel declarations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
