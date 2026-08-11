"""E33 Gate 0 - the register sheet: concept | clay | control | one column per CANDIDATE register.

WHY A NEW SHEET AND NOT AN EXISTING ONE. Enumerated before commissioning, per CLAUDE.md's own
law, and each existing sheet is missing a different column this ruling needs:

  verify/gate0_sheet.py     concept beside N clay views. No styled column at all, so it cannot
                            put a candidate register next to the thing it is a register FOR.
  diagnostics/e12_pair_sheet.py   clay | control | styled, one row per view - the right three
                            panels, but exactly ONE styled per row and no concept panel. A
                            register ruling compares candidates to EACH OTHER, side by side,
                            at one camera; across three files it is not a comparison.
  diagnostics/e14_pair_sheet.py   reference | control | asset, single view, hilt zoom. Same
                            one-asset limit, and its zoom rows are a sword's.
  diagnostics/e13_gate1_sheet.py  reference | asset | provenance | error | clay - needs a
                            FINISHED atlas and a texel-provenance map. Neither exists before
                            projection, which is where this experiment stops.

WHAT THE COLUMNS ARE FOR, left to right, and what a defect in each one means:

  concept    the Director's own plate - the identity that is supposed to survive the route.
             It is a different frame and a different scale from everything right of it, and
             it is labelled so nobody reads a size difference as a proportion finding.
  clay       what the GEOMETRY actually is (Workbench --clay: texture hides geometry).
  control    what the generator was TOLD about that geometry - canny + the mask's
             morphological contour. E07's lesson: a number says a region is wrong, the
             provenance panel says what it was supposed to be.
  R*         one column per candidate register, in the order given, each labelled with its
             register clause. A difference visible across these columns and absent from
             `control` is the register doing its job; a difference present in `control` is
             ours.

IT RANKS NOTHING AND EMITS NO NUMBER. Which register is canon is the Director's call and no
statistic approaches it - this repo graded material identity with high-pass statistics once
and character identity with silhouette IoU once, and both were the wrong question with a
number attached.

THE ONE ANDON, and why it is on THIS direction. Every candidate must be pixel-identical in
SIZE to the clay render of the view it belongs to. A styled twin is projected through the
camera that made its render, so a twin one pixel off its control breaks every downstream
pairing - measured, E04 Ruling 15, where a width not divisible by 8 decoded 1066 -> 1064 and
put every twin 2 px off. A sheet that quietly LANCZOS-resizes a mismatched twin into a tidy
column would hide exactly that, and the resize is the only place this tool could hide it. So
the check lives here, `raise`s (never `assert`: `python -O` deletes those - E21 Ruling 2),
and has no skip flag.

  e33_register_sheet.py --concept P.png --clay DIR --control DIR --tag armclay --views 0,4
                        --candidate R1:0=a.png --candidate R1:4=b.png ...
                        --register R1="ultra-realistic, matte fired clay"
                        --out SHEET.png [--width 700]

Standards compliance:
  PIN_PER_STEP - every input path is an explicit flag and the sheet prints the full column
    order it built, so the artifact's composition replays from the recorded command.
  ANDON_AUTHORITY - the size check above raises inside the tool that writes the file; a
    missing candidate for a named (register, view) pair raises too, because a silently short
    row would read as "that register produced nothing" when it means "nobody passed it".
  NAMED_COMPENSATORS - writes only --out; undo = delete it. Every input is opened read-only.
  DECOMPOSE_BY_SECRETS - knows nothing about what a register IS; the clause is a label
    string supplied by the caller and the candidate is a file. Subject content stays out.
  UNCERTAINTY_GATED_HUMANS - this file exists to put an undecided canon question in front of
    the Director as an artifact rather than resolve it with a metric.
  EXTERNAL_VERIFIER - emits no number and adopts nothing.

Source is ASCII bytes (the repo's law).
"""
import argparse
import os

from PIL import Image, ImageDraw


def build(concept, clay_dir, control_dir, tag, views, candidates, registers, width):
    """Return the composed sheet. Raises on any size or completeness violation.

    `candidates` maps (register, view) -> path; `registers` is the ordered register list
    and `registers_label` its clause text, both supplied by the caller.
    """
    reg_order = [r for r, _ in registers]
    rows = []
    for v in views:
        clay_p = os.path.join(clay_dir, "%s_%s.png" % (tag, v))
        ctrl_p = os.path.join(control_dir, "%s_%s_control.png" % (tag, v))
        clay = Image.open(clay_p).convert("RGB")
        ctrl = Image.open(ctrl_p).convert("RGB")
        tiles = [("clay  (Workbench --clay: geometry, no texture)", clay),
                 ("control  (canny + morphological contour)", ctrl)]
        for r in reg_order:
            p = candidates.get((r, v))
            if p is None:
                raise SystemExit(
                    "ANDON: no candidate given for register %r at view %s. A short row would "
                    "read as 'this register produced nothing' when it means nobody passed "
                    "it. No file written." % (r, v))
            im = Image.open(p).convert("RGB")
            if im.size != clay.size:
                raise SystemExit(
                    "ANDON: candidate %s (register %s, view %s) is %dx%d against its clay "
                    "render's %dx%d. A twin is projected through the camera that made its "
                    "render, so a size mismatch breaks every downstream pairing (E04 Ruling "
                    "15). Resizing it into the column here would hide that. No file written."
                    % (p, r, v, im.size[0], im.size[1], clay.size[0], clay.size[1]))
            tiles.append(("%s  %s" % (r, dict(registers)[r]), im))
        rows.append((v, tiles))

    cw = width
    ch = int(round(cw * rows[0][1][0][1].height / rows[0][1][0][1].width))
    hdr, cap, gap, pad = 30, 34, 10, 12
    # the concept panel spans the full sheet height on the left, at its own aspect
    con = Image.open(concept).convert("RGB")
    con_w = cw
    con_h = int(round(con_w * con.height / con.width))
    ncol = len(rows[0][1])
    body_w = ncol * cw + (ncol - 1) * gap
    row_h = ch + hdr + cap
    sheet_w = con_w + gap * 2 + body_w + pad * 2
    sheet_h = max(len(rows) * row_h, con_h + cap) + pad * 2
    sheet = Image.new("RGB", (sheet_w, sheet_h), (14, 14, 16))
    d = ImageDraw.Draw(sheet)

    d.text((pad + 4, pad + 6),
           "concept  (the Director's plate - DIFFERENT frame and scale; do not read a size "
           "difference here as a proportion finding)", fill=(255, 210, 90))
    sheet.paste(con.resize((con_w, con_h), Image.LANCZOS), (pad, pad + cap))

    x0 = pad + con_w + gap * 2
    for i, (v, tiles) in enumerate(rows):
        y = pad + i * row_h
        d.text((x0 + 4, y + 6), "view %s" % v, fill=(120, 220, 255))
        for j, (lab, im) in enumerate(tiles):
            x = x0 + j * (cw + gap)
            d.text((x + 4, y + cap - 14), lab, fill=(255, 210, 90))
            sheet.paste(im.resize((cw, ch), Image.LANCZOS), (x, y + cap + hdr - 14))
    return sheet, [t[0] for t in rows[0][1]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--concept", required=True)
    ap.add_argument("--clay", required=True, help="dir holding <tag>_<view>.png")
    ap.add_argument("--control", required=True, help="dir holding <tag>_<view>_control.png")
    ap.add_argument("--tag", default="armclay")
    ap.add_argument("--views", default="0,4")
    ap.add_argument("--candidate", action="append", required=True,
                    help="REGISTER:VIEW=PATH, repeatable")
    ap.add_argument("--register", action="append", required=True,
                    help="REGISTER=CLAUSE, repeatable; ORDER SETS COLUMN ORDER")
    ap.add_argument("--width", type=int, default=700, help="per-panel width in the sheet")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    views = [v.strip() for v in a.views.split(",") if v.strip()]
    registers = []
    for spec in a.register:
        k, _, txt = spec.partition("=")
        registers.append((k.strip(), txt))
    cands = {}
    for spec in a.candidate:
        key, _, path = spec.partition("=")
        r, _, v = key.partition(":")
        cands[(r.strip(), v.strip())] = path
    d = os.path.dirname(os.path.abspath(a.out))
    if d and not os.path.isdir(d):
        os.makedirs(d)  # scripts create their own output directories
    sheet, cols = build(a.concept, a.clay, a.control, a.tag, views, cands, registers, a.width)
    sheet.save(a.out)
    print("[e33sheet] %d views x %d panels + concept -> %s  (%dx%d)"
          % (len(views), len(cols), a.out, sheet.width, sheet.height))
    print("[e33sheet] column order: concept | %s" % " | ".join(c.split("  ")[0] for c in cols))


if __name__ == "__main__":
    main()
