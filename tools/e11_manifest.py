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


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_id(job_key):
    return job_key.replace("+", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", choices=list(SUBJECTS), required=True)
    args = ap.parse_args()
    S = SUBJECTS[args.subject]
    tree = S["tree"]
    staged = json.load(open(S["staged_manifest"], encoding="utf-8"))
    run = json.load(open(J(tree, S["run_json"]), encoding="utf-8"))

    ledger = {}
    for name, src in S["copies"].items():
        dst = J(tree, name)
        if os.path.abspath(src) != os.path.abspath(dst):
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
            "note": staged["channels"][1]["note"] if len(staged.get("channels", [])) > 1
                    else "the native stage-1 view-owner sidecar"})
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
        if S["owner_channel"]:
            entry["channels"]["owner_view"] = f"views/{vid}/owner.png"
            entry["loss_mask"] = f"views/{vid}/loss_mask_{vid}.png"
        if vid in S["pairs"]:
            entry["pair"] = dict(S["pairs"][vid])
        renders.append(entry)

    manifest = {
        "schema_version": "1.0.0",
        "_authored": "E11 dense-turnaround exporter, 2026-08-05. Self-contained tree: "
                     "every referenced file lives under this directory, copies "
                     "sha256-verified from the accepted artifacts. The subject root's "
                     "staged 3-render manifest is untouched; which one the Director "
                     "pastes into the lane is his call. Per-view owner_id_*.npy and "
                     "admission_*.json ride undeclared beside the declared channels "
                     "(render-space npy/json are not lane schema 1.x concepts).",
        "asset": {
            "id": S["asset_id"],
            "source": staged["asset"]["source"],
            "mesh": {"path": "mesh.glb"},
            "atlas": {"path": "atlas.png"},
        },
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
    out = J(tree, "asset-source.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    print(f"[manifest] wrote {out}  ({len(renders)} renders, "
          f"{len(channels)} channel declarations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
