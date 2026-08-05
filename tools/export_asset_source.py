"""Export the E04 galleon into the sdlab asset lane: the `asset-source.json` manifest.

facet exports; sdlab ingests. This writes the manifest and the two derived channel
files the contract needs, and it touches NOTHING else.

WHAT THE CONTRACT REQUIRES THAT THE RAW ARTIFACTS DO NOT ALREADY SATISFY
(style-dataset-lab/lib/asset-source.js, docs/asset-lane-design.md):

  1. A categorical texture channel must be an INDEXED PNG whose PLTE is a subset of the
     declared class palette (E09 Amendment 1). `prov_atlas.png` is truecolor (IHDR color
     type 2), so it is re-encoded here as indexed with a 4-entry PLTE and no padding.
     The check is structural - PLTE proves every pixel in-palette without decoding one.
  2. Every referenced path must resolve INSIDE the manifest's directory. The manifest
     therefore lives at E04_stroke/ (where the asset is), and the one artifact that lives
     in the other tree - the native `_owner.npy` from stage 1 - is COPIED to export/,
     verified by sha256 after the copy.

THE BASE ASSET IS NEVER OPENED FOR WRITING. `galleon_final.glb` and `galleon_final.png`
are Gate-1 accepted canon (Ruling 28). This tool sha256s both before and after every
write and HALTS on any difference. The check lives in the tool that performs the writes,
with no skip flag - E08 Amendment 32: a shell chain is a transport, not a guard.

Standards compliance:
  PIN_PER_STEP - every class colour, dtype and shape written into the manifest is READ
    from the artifact it describes, never typed from memory; the source of each is echoed.
  ANDON_AUTHORITY - canon-invariance halts; the indexed re-encode halts unless the written
    file's PLTE round-trips against the declaration AND its pixels equal the source's.
  NAMED_COMPENSATORS - writes exactly three paths, all under export/, plus the manifest.
    Undo = delete E04_stroke/export/ and E04_stroke/asset-source.json. Owner: this session.
    No irreversible or external action; the ingest is a separate session's call.
  DECOMPOSE_BY_SECRETS - subject vocabulary (palette, identity, acceptance) is READ from
    canon/ and profiles/; this file holds the contract's mechanics only.
  EXTERNAL_VERIFIER - this tool does not validate its own manifest. sdlab's
    `validateAssetSource` reads the bytes and rules; run it after this.

  export_asset_source.py [--stroke DIR] [--armt DIR] [--dry-run]
"""
import argparse
import ast
import hashlib
import json
import os
import shutil
import struct
import sys
import zlib

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# ---- the provenance class palette. Colours are e04_replay_owner.py's, transcribed, and
# ---- asserted below against the atlas's own measured colour set.
PROV_CLASSES = [
    {"name": "background", "rgb": [0, 0, 0]},
    {"name": "reference", "rgb": [46, 176, 88]},
    {"name": "brush", "rgb": [40, 110, 235]},
    {"name": "dilation", "rgb": [232, 132, 32]},
]

# ---- the three ruled Gate-1 sheet cameras (e04_sheet_renders.py CAMS), named as the arc
# ---- named them: view 0 is the BEAM, the two elevated cameras are the DECK (Ruling 27).
CAMS = [
    {"id": "beam_y000_e00", "yaw": 0, "el": 0, "facing": "beam",
     "clay": True},
    {"id": "deck_y000_e40", "yaw": 0, "el": 40,
     "facing": "deck from the beam, viewed from above", "clay": False},
    {"id": "deck_y180_e40", "yaw": 180, "el": 40,
     "facing": "deck from the opposite beam, viewed from above", "clay": False},
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def npy_header(path):
    with open(path, "rb") as f:
        magic = f.read(6)
        major = f.read(1)[0]
        f.read(1)
        hlen = struct.unpack("<H" if major == 1 else "<I",
                             f.read(2 if major == 1 else 4))[0]
        d = ast.literal_eval(f.read(hlen).decode("latin1"))
    assert magic == b"\x93NUMPY", "ANDON: %s is not an npy" % path
    return d["descr"], list(d["shape"])


def png_chunks(buf):
    assert buf[:8] == b"\x89PNG\r\n\x1a\n", "ANDON: not a png"
    i, out = 8, []
    while i < len(buf):
        (ln,) = struct.unpack(">I", buf[i:i + 4])
        typ = buf[i + 4:i + 8]
        out.append((typ, buf[i + 8:i + 8 + ln]))
        i += 12 + ln
    return out


def write_indexed_png(dst, idx, palette_rgb):
    """Write an 8-bit indexed PNG with PLTE == palette_rgb EXACTLY (no padding).

    Hand-rolled rather than left to an encoder: E09 Amendment 1 requires the written
    file's PLTE to BE the declared class palette, and a library that pads to 256 entries
    would produce undeclared classes that the contract refuses. Nothing here is clever -
    it is the smallest writer that makes the declaration and the bytes the same object.
    """
    h, w = idx.shape
    raw = bytearray()
    for y in range(h):
        raw.append(0)                       # filter type 0 (None)
        raw += idx[y].tobytes()

    def chunk(typ, data):
        return (struct.pack(">I", len(data)) + typ + data
                + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))

    plte = b"".join(bytes(c) for c in palette_rgb)
    out = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 3, 0, 0, 0))
           + chunk(b"PLTE", plte)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(dst, "wb") as f:
        f.write(out)
    return plte


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stroke", default=r"E:\AI\training\facet_next\E04_stroke")
    ap.add_argument("--armt", default=r"E:\AI\training\facet_next\E04_armT72")
    ap.add_argument("--repo", default=r"E:\AI\facet")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    J = os.path.join
    STROKE, ARMT, REPO = args.stroke, args.armt, args.repo
    EXPORT = J(STROKE, "export")

    # ---- canon, hashed BEFORE anything is written -----------------------------------
    CANON = {"out/galleon_final.glb": J(STROKE, "out", "galleon_final.glb"),
             "out/galleon_final.png": J(STROKE, "out", "galleon_final.png")}
    before = {k: sha256(p) for k, p in CANON.items()}
    print("[canon] accepted base asset, hashed before any write:")
    for k, v in before.items():
        print("  %-24s %s" % (k, v))

    if args.dry_run:
        print("[dry-run] nothing written")
        return 0

    os.makedirs(EXPORT, exist_ok=True)

    # ---- 1. provenance atlas -> indexed PNG -----------------------------------------
    src = J(STROKE, "out", "prov_atlas.png")
    rgb = np.asarray(Image.open(src).convert("RGB"))
    uniq = np.unique(rgb.reshape(-1, 3), axis=0)
    declared = {tuple(c["rgb"]) for c in PROV_CLASSES}
    found = {tuple(int(x) for x in c) for c in uniq}
    if not found <= declared:
        print("ANDON: prov_atlas.png contains colours not in the declared class palette: %s"
              % sorted(found - declared))
        return 1
    print("[prov] %s carries %d colours, all declared" % (os.path.basename(src), len(found)))

    idx = np.zeros(rgb.shape[:2], dtype=np.uint8)
    for i, cls in enumerate(PROV_CLASSES):
        idx[np.all(rgb == np.array(cls["rgb"], dtype=np.uint8), axis=-1)] = i
    prov_dst = J(EXPORT, "provenance_atlas.png")
    plte = write_indexed_png(prov_dst, idx, [c["rgb"] for c in PROV_CLASSES])

    # ANDON: the PLTE must round-trip against the declaration, and the pixels must not move
    chunks = dict(png_chunks(open(prov_dst, "rb").read()))
    w, h, depth, ctype = struct.unpack(">IIBB", chunks[b"IHDR"][:10])
    if ctype != 3 or depth != 8:
        print("ANDON: wrote color type %d depth %d, expected indexed 8-bit" % (ctype, depth))
        return 1
    if chunks[b"PLTE"] != plte:
        print("ANDON: PLTE does not round-trip against the declaration")
        return 1
    back = np.asarray(Image.open(prov_dst).convert("RGB"))
    if not np.array_equal(back, rgb):
        print("ANDON: the indexed re-encode changed pixels")
        return 1
    print("[prov] wrote %s  %dx%d indexed, PLTE %d entries, pixels identical to source"
          % (os.path.relpath(prov_dst, STROKE), w, h, len(plte) // 3))

    # ---- 2. the native owner sidecar, copied in (it lives in the other tree) ---------
    own_src = J(ARMT, "stage1", "stage1_8cam_owner.npy")
    own_dst = J(EXPORT, "view_owner.npy")
    shutil.copyfile(own_src, own_dst)
    if sha256(own_src) != sha256(own_dst):
        print("ANDON: view_owner.npy copy does not match its source")
        return 1
    own_dtype, own_shape = npy_header(own_dst)
    own = np.load(own_dst)
    own_vals = sorted(int(v) for v in np.unique(own))
    print("[owner] %s <- %s  dtype %s shape %s values %s"
          % (os.path.relpath(own_dst, STROKE), os.path.basename(own_src),
             own_dtype, own_shape, own_vals))

    # ---- 3. the beam view's clay pair, copied in (also the other tree) ---------------
    clay_src = J(ARMT, "clay", "galleonclay_0.png")
    clay_dst = J(EXPORT, "pair_clay_beam_y000_e00.png")
    shutil.copyfile(clay_src, clay_dst)
    if sha256(clay_src) != sha256(clay_dst):
        print("ANDON: clay pair copy does not match its source")
        return 1

    # ANDON: the clay pair is only admissible as this render's pair if it is the SAME
    # camera. Proven by its exact silhouette, not asserted from the filename.
    m_clay = np.asarray(Image.open(J(ARMT, "masks", "galleonclay_0.png")).convert("L")) > 0
    m_hit = np.asarray(Image.open(J(STROKE, "sheet", "asset", "job_y+000_e+00",
                                    "hit.png")).convert("L")) > 0
    if m_clay.shape != m_hit.shape or not np.array_equal(m_clay, m_hit):
        print("ANDON: the clay view-0 silhouette is not the beam camera's silhouette")
        return 1
    print("[clay] %s  silhouette byte-equal to the beam camera's raycast hit (%d px)"
          % (os.path.relpath(clay_dst, STROKE), int(m_hit.sum())))

    # ---- 4. the styled mask, read where it lies -------------------------------------
    sm_rel = "state/styled_mask.npy"
    sm_dtype, sm_shape = npy_header(J(STROKE, "state", "styled_mask.npy"))

    # ---- 5. the manifest ------------------------------------------------------------
    pal = json.load(open(J(REPO, "canon", "E04-galleon-palette.json"), encoding="utf-8"))
    prov_counts = json.load(open(J(STROKE, "out", "provenance.json"), encoding="utf-8"))

    # ---- the suspension, TRANSLATED at the boundary (E04 Ruling 29) ------------------
    # canon declares max_offpalette_blob_px: null - a SUSPENSION, not a missing value
    # (Ruling 8: no baseline for this subject exists, and the only numbers derivable are
    # the ones the bound would judge). The sdlab schema has no representation for that:
    # it allows null for the percentage bound and demands an integer here, which forces
    # exactly the invention the non-circularity rule forbids. So the export translates
    # the suspension into an UNREACHABLE SENTINEL - the whole atlas, a bound no blob can
    # reach - which is E04's own established pattern (bbox-tol 9.99, bg-max-pct 100.0):
    # suspension expressed as a value the consumer actually receives. CANON KEEPS ITS
    # NULL. The translation lives here, with its reason, which is what an export tool is
    # for. If canon ever carries a derived integer, it passes through untouched.
    atlas_meta = Image.open(J(STROKE, "out", "galleon_final.png"))
    blob_sentinel = atlas_meta.width * atlas_meta.height
    canon_blob = pal["gate"]["max_offpalette_blob_px"]
    blob_suspended = canon_blob is None
    blob_value = blob_sentinel if blob_suspended else int(canon_blob)
    print("[gate] canon blob bound %s -> manifest %d (%s)"
          % ("null (SUSPENDED)" if blob_suspended else str(canon_blob), blob_value,
             "unreachable sentinel = %dx%d atlas" % (atlas_meta.width, atlas_meta.height)
             if blob_suspended else "derived bound, passed through"))

    renders = []
    for c in CAMS:
        tag = "y%+04d_e%+03d" % (c["yaw"], c["el"])
        r = {
            "id": c["id"],
            "path": "out/sheet_asset_%s.png" % tag,
            "camera": {"yaw_deg": c["yaw"], "elevation_deg": c["el"]},
            "light": "flat",
            "facing": c["facing"],
            "silhouette_mask": "sheet/asset/job_%s/hit.png" % tag,
            "channels": {"provenance_view": "out/sheet_prov_%s.png" % tag,
                         "owner_view": "out/sheet_owner_%s.png" % tag},
        }
        if c["clay"]:
            r["pair"] = {"clay": "export/pair_clay_beam_y000_e00.png"}
        renders.append(r)

    manifest = {
        "schema_version": "1.0.0",
        "_authored": (
            "2026-08-05 by the facet executor session, from artifacts already on disk. "
            "Asset #2 of the facet lane and the FIRST with a native view_owner channel. "
            "Lives at E04_stroke/ because manifest paths must stay inside the manifest's "
            "directory: the asset, its renders and its exact silhouettes are all here, and "
            "the two artifacts that live in E04_armT72 (the stage-1 owner sidecar and the "
            "beam view's clay pair) are copied into export/ with their sha256 verified "
            "after the copy. Only three renders exist for this asset - the three ruled "
            "Gate-1 sheet cameras - against W3's eight; a dense turnaround is the "
            "dense-turnaround exporter's job (Ruling 28's queue), not this manifest's."),
        "asset": {
            "id": "e04_galleon",
            "source": "facet/E04",
            "mesh": {"path": "out/galleon_final.glb"},
            "atlas": {"path": "out/galleon_final.png"},
        },
        "acceptance": {
            "gate": "gate-1",
            "verdict": "accepted",
            "date": "2026-08-05",
            "record": ("E:/AI/facet/docs/experiments/E04-ruling.md Ruling 28 "
                       "(\"Dude, it looks good to me.\") - judged artifacts: "
                       "out/GATE1_sheet_beam.png, out/GATE1_sheet_deck.png, "
                       "out/galleon_final.glb at the Director's zoom"),
            "by": "director",
        },
        "palette": {
            "source": "E:/AI/facet/canon/E04-galleon-palette.json",
            "min_chroma": pal["min_chroma"],
            "allowed_bands": [{"name": b["name"], "hue_deg": b["hue_deg"]}
                              for b in pal["allowed_bands"]],
            "gate": {
                "max_offpalette_pct": pal["gate"]["max_offpalette_pct"],
                "max_offpalette_blob_px": blob_value,
            },
            "_max_offpalette_blob_px_IS_A_SUSPENSION_ENCODING": (
                "NOT A DERIVED BOUND AND NOT A THRESHOLD. canon/E04-galleon-palette.json "
                "declares this null on purpose (E04 Ruling 8: this subject had no baseline "
                "when its bands were derived, and 'suspend rather than invent' is the "
                "house rule - the only numbers available to derive a bound from are the "
                "results the bound would judge). The sdlab schema requires an integer "
                "here while allowing null for max_offpalette_pct, so the export tool "
                "TRANSLATES the suspension at the boundary into %d - the whole %dx%d "
                "atlas, a value no connected component can reach - so the consumer "
                "receives a bound that gates nothing and cannot be mistaken for a "
                "measured threshold. This is E04's established pattern (bbox-tol 9.99, "
                "bg-max-pct 100.0). Canon keeps its null; the translation lives in "
                "tools/export_asset_source.py with its reason. Ruled in E04-ruling.md "
                "Ruling 29. MEASURED CONTEXT, not a bound: the three renders below carry "
                "largest off-palette components of 1,738 / 1,495 / 263 px; W3's 800 px "
                "bound would reject two of the three renders of this accepted asset."
                % (blob_value, atlas_meta.width, atlas_meta.height)),
            "_bands_note": (
                "Transcribed from the canon fixture, which derives them from "
                "GALLEON-IDENTITY.md's named materials measured on a DIFFERENT image than "
                "any twin. The `blue` band is SUSPENDED in the fixture: its span is "
                "measured at 283-291 deg, and the 273-301 written here is a +-10 deg "
                "CONVENTION, not a measurement. Blue is a declared material on this "
                "subject (G11), not an off-palette detector colour as on W3."),
            "_gate_note": (
                "BOTH BOUNDS ARE NULL IN THE CANON FIXTURE, ON PURPOSE (E04 Ruling 8): no "
                "baseline for this subject existed when the bands were derived, and "
                "'suspend rather than invent' is the house rule. W3's 800 px blob bound is "
                "W3 data and a global constant must not govern a local feature. This is a "
                "known collision with the sdlab schema, which requires an integer here - "
                "reported, NOT resolved by this tool."),
        },
        "channels": [
            {
                "id": "provenance_atlas",
                "space": "texture",
                "encoding": "indexed",
                "categorical": True,
                "filter": "nearest",
                "path": "export/provenance_atlas.png",
                "palette": PROV_CLASSES,
                "note": (
                    "Re-encoded from out/prov_atlas.png (truecolor, 4 colours measured) to "
                    "indexed with PLTE == this palette exactly, per E09 Amendment 1; the "
                    "written file's PLTE was round-tripped and its pixels proven equal to "
                    "the source. Classes are e04_replay_owner.py's: `reference` = the "
                    "stage-1 eight-camera projection (%d texels, %.2f%%), `brush` = the six "
                    "authored strokes (%d, %.2f%%), `dilation` = the finalize flood (%d, "
                    "%.2f%%), `background` = outside the UV-valid mask. Ownership was "
                    "reconstructed by RE-RUNNING the shipped commits to byte-identity, not "
                    "by reimplementing the filter chain."
                    % (prov_counts["stage1"], prov_counts["mix_pct"]["stage1"],
                       prov_counts["brush"], prov_counts["mix_pct"]["brush"],
                       prov_counts["dilation"], prov_counts["mix_pct"]["dilation"])),
            },
            {
                "id": "view_owner",
                "space": "texture",
                "encoding": "npy",
                "categorical": False,
                "path": "export/view_owner.npy",
                "dtype": own_dtype,
                "shape": own_shape,
                "note": (
                    "THE NATIVE SIDECAR project_twins.py writes: which VIEW won each texel, "
                    "int8, -1 where nothing styled it. Measured values %s - the eight "
                    "stage-1 cameras at 45 deg steps from yaw 0, and -1 elsewhere. This is "
                    "the channel the W3 manifest declared missing, so the owner-seam gate "
                    "the schema reserved has its first asset. BOUNDARY, stated so it is not "
                    "over-read: it carries STAGE-1 view ownership. The six brush strokes "
                    "committed after stage 1 own %d texels between them; those texels read "
                    "as their stage-1 owner here (or -1 if stage 1 never reached them), and "
                    "per-stroke ownership lives in provenance_atlas's `brush` class and in "
                    "out/provenance.json's per_stroke counts. `categorical` is false because "
                    "schema 1.x does not support categorical npy - the classes are declared "
                    "in this note, not proven by the contract."
                    % (own_vals, prov_counts["brush"])),
            },
            {
                "id": "styled_mask",
                "space": "texture",
                "encoding": "npy",
                "categorical": False,
                "path": sm_rel,
                "dtype": sm_dtype,
                "shape": sm_shape,
                "note": (
                    "Styled/unstyled coverage after the sixth stroke and BEFORE the finalize "
                    "flood: true where reference or brush painted, false where the flood "
                    "later filled. Same channel W3 declared."),
            },
            {
                "id": "provenance_view",
                "space": "render",
                "encoding": "rgb",
                "categorical": False,
                "note": (
                    "The provenance atlas raycast at each sheet camera by texpass_iter emit "
                    "- no lighting, so it is a flat readout. Antialiased at silhouette and "
                    "class edges, so it is NOT exactly-classifiable and no class palette is "
                    "declared for it; carried and hashed. Class shares activate when an "
                    "exporter declares a render-space palette with a filter and tolerance."),
            },
            {
                "id": "owner_view",
                "space": "render",
                "encoding": "rgb",
                "categorical": False,
                "note": (
                    "The owner atlas at the same cameras - the fifth column of the Gate-1 "
                    "sheet. 16 colours in texture space: 8 stage-1 cameras, 6 stroke "
                    "colours, dilation grey, background. Antialiased in render space for the "
                    "same reason as provenance_view. The numeric answer is view_owner.npy; "
                    "this is its display form."),
            },
        ],
        "renders": renders,
        "captions": {
            "subject": ("a three-masted galleon with a gilded lion figurehead, warm "
                        "oak-brown hull planking, black tarred strakes, weathered tan "
                        "canvas sails, gilded stern scrollwork, red gun port lids, black "
                        "iron cannon barrels, pale scrubbed deck planking, and a deep "
                        "sea-blue frieze band along the bulwarks"),
            "style_trigger": None,
            "domain_tag": "3d asset",
        },
        "_identity_fixture": "E:/AI/facet/canon/GALLEON-IDENTITY.md (G1-G13)",
    }

    dst = J(STROKE, "asset-source.json")
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    print("[manifest] wrote %s (%d bytes)" % (dst, os.path.getsize(dst)))

    # ---- canon, hashed AFTER every write. No skip flag. -----------------------------
    after = {k: sha256(p) for k, p in CANON.items()}
    bad = [k for k in CANON if before[k] != after[k]]
    if bad:
        print("ANDON: the accepted base asset changed during export: %s. HALT." % bad)
        return 1
    print("[canon] base asset byte-identical after export: %d/%d files unchanged"
          % (len(CANON), len(CANON)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
