"""Protection manifests for the read-only trees: verify one, or emit a new one.

WHY THIS FILE EXISTS. E33/E34/E35 each gate their tree with a sha256 manifest at arc open
and close, and until now the verifier was written inline in whichever session needed it.
That is how a gate's own repair gets re-derived every arc: E35's open session rebuilt it,
fired a FALSE halt on `E34_manifest.json` (which declares `excludes_self: true` and is
absent from its own file list by construction), repaired the walk, and the repair went
nowhere. This is that walk, committed, with its can-fail fixture riding beside it.

`excludes_self` IS PART OF THE CONTRACT, not a special case. A manifest that lists its own
hash cannot be written - the hash changes when it is written - so the flag is how a tree
declares that exactly one file, its own manifest, is outside the census. The walk honours
the flag and nothing else: any OTHER new file is still `added`, which is what the fixture
proves.

  tree_manifest.py --verify PATH_TO_MANIFEST [--verify ...]
  tree_manifest.py --emit ROOT --out PATH --occasion TEXT [--exclude NAME ...]
  tree_manifest.py --selftest        <- the can-fail fixture, no real tree touched

ASCII prints. Read-only on every tree it verifies. It renders no verdict beyond
HELD / FIRED, which is a fact about bytes.
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
import tempfile


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                return h.hexdigest()
            h.update(b)


def walk(root, exclude=()):
    """Every file under root, relative-path keyed, sorted. `exclude` is matched on the
    relative path so a self-exclusion cannot accidentally hide a same-named file deeper
    in the tree."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if rel in exclude:
                continue
            out[rel] = full
    return out


def normalise(m):
    """TWO ENCODINGS OF ONE CONTRACT, and neither is wrong. E34 keys `root` with `files`
    as a dict and declares `excludes_self`; E33 keys `_root` with `files` as a list of
    {path,bytes,sha256} and LISTS ITSELF. Both are saying the same thing about the same
    hazard - a manifest cannot record its own hash, because writing the hash changes the
    file - so the walk accepts both and handles the self-entry explicitly either way."""
    root = m.get("root") or m["_root"]
    files = m["files"]
    if isinstance(files, list):
        files = {f["path"]: {"sha256": f["sha256"], "bytes": f["bytes"]} for f in files}
    return root, files


def verify(manifest_path, quiet=False):
    m = json.load(open(manifest_path, encoding="utf-8"))
    root, declared = normalise(m)
    me = os.path.basename(manifest_path).replace(os.sep, "/")
    excl = set()
    if m.get("excludes_self"):
        excl.add(me)
    present = walk(root, excl)
    # THE SELF-ENTRY, when a manifest lists itself: its recorded hash is stale BY
    # CONSTRUCTION and is reported on its own line rather than counted as a change.
    # Reported, never silent - a silent carve-out is how a real delta hides.
    self_stale = None
    if me in declared and me in present:
        if sha256(present[me]) != declared[me]["sha256"]:
            self_stale = me
            declared = {k: v for k, v in declared.items() if k != me}
            present = {k: v for k, v in present.items() if k != me}
    added = sorted(set(present) - set(declared))
    removed = sorted(set(declared) - set(present))
    changed = []
    total = 0
    for rel in sorted(set(declared) & set(present)):
        b = os.path.getsize(present[rel])
        total += b
        if b != declared[rel]["bytes"] or sha256(present[rel]) != declared[rel]["sha256"]:
            changed.append(rel)
    held = not (added or removed or changed)
    if not quiet:
        print("[manifest] %s" % os.path.basename(manifest_path))
        print("           root %s" % root)
        print("           declared %d / present %d   total_bytes %d (declared %d)"
              % (len(declared), len(present), total, m.get("total_bytes", -1)))
        if self_stale:
            print("           self-reference %s: hash stale BY CONSTRUCTION, reported "
                  "and not counted" % self_stale)
        print("           added %d  removed %d  changed %d   -> %s"
              % (len(added), len(removed), len(changed), "HELD" if held else "FIRED"))
        for label, xs in (("added", added), ("removed", removed), ("changed", changed)):
            for x in xs[:10]:
                print("             %s: %s" % (label, x))
    return held, dict(manifest=os.path.basename(manifest_path), root=root,
                      declared=len(declared), present=len(present), total_bytes=total,
                      added=added, removed=removed, changed=changed, held=held,
                      self_reference_stale=self_stale)


def emit(root, out, occasion, exclude=()):
    excl = set(exclude) | {os.path.basename(out).replace(os.sep, "/")}
    present = walk(root, excl)
    files, total = {}, 0
    for rel in sorted(present):
        b = os.path.getsize(present[rel])
        files[rel] = {"sha256": sha256(present[rel]), "bytes": b}
        total += b
    doc = {"root": root,
           "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "occasion": occasion, "excludes_self": True,
           "count": len(files), "total_bytes": total, "files": files}
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
    print("[manifest] emitted %s" % out)
    print("           %d files, %d bytes, excludes_self true" % (len(files), total))
    return doc


def selftest():
    """THE CAN-FAIL FIXTURE. A gate that has only ever been seen to pass is not evidence.
    Four cases on a synthetic tree: clean HELDs, and each of the three delta kinds FIRES.
    The self-exclusion case is the one E35's open session got wrong, so it is first."""
    ok = True
    with tempfile.TemporaryDirectory() as d:
        root = os.path.join(d, "tree")
        os.makedirs(root)
        for n, body in (("a.txt", b"alpha"), ("sub/b.bin", b"\x00\x01\x02")):
            p = os.path.join(root, n.replace("/", os.sep))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "wb").write(body)
        mpath = os.path.join(root, "M_manifest.json")
        emit(root, mpath, "selftest")
        cases = []
        held, _ = verify(mpath, quiet=True)
        cases.append(("clean tree, manifest self-excluded", held, True))
        p = os.path.join(root, "intruder.txt"); open(p, "wb").write(b"x")
        held, _ = verify(mpath, quiet=True); os.remove(p)
        cases.append(("an intruder file", held, False))
        p = os.path.join(root, "a.txt"); old = open(p, "rb").read()
        open(p, "wb").write(b"alphb")
        held, _ = verify(mpath, quiet=True); open(p, "wb").write(old)
        cases.append(("one changed byte", held, False))
        p = os.path.join(root, "sub", "b.bin"); old = open(p, "rb").read(); os.remove(p)
        held, _ = verify(mpath, quiet=True); open(p, "wb").write(old)
        cases.append(("a removed file", held, False))
        held, _ = verify(mpath, quiet=True)
        cases.append(("restored tree", held, True))
        # the E33 encoding: _root, files as a LIST, manifest listed with a stale hash
        e33 = json.load(open(mpath, encoding="utf-8"))
        lst = [{"path": k, "bytes": v["bytes"], "sha256": v["sha256"]}
               for k, v in e33["files"].items()]
        lst.append({"path": "M33_manifest.json", "bytes": 1,
                    "sha256": "0" * 64})          # stale by construction
        # the E34-form manifest is a real file in this tree and this encoding excludes
        # nothing, so it must be declared - otherwise the leg fires on the fixture's own
        # omission rather than on anything about the walk. (It did, first run.)
        lst.append({"path": "M_manifest.json", "bytes": os.path.getsize(mpath),
                    "sha256": sha256(mpath)})
        p33 = os.path.join(root, "M33_manifest.json")
        with open(p33, "w", encoding="utf-8") as fh:
            json.dump({"_root": root, "_files": len(lst), "files": lst}, fh)
        held, row = verify(p33, quiet=True)
        cases.append(("E33 form: self-listed, hash stale", held, True))
        cases.append(("  ... and the staleness is REPORTED",
                      row["self_reference_stale"] == "M33_manifest.json", True))
        pi = os.path.join(root, "intruder2.txt"); open(pi, "wb").write(b"y")
        held, _ = verify(p33, quiet=True); os.remove(pi)
        cases.append(("E33 form still catches an intruder", held, False))
        os.remove(p33)
        print()
        for name, got, want in cases:
            good = got == want
            ok &= good
            print("  %-38s HELD=%-5s expected %-5s  %s"
                  % (name, got, want, "ok" if good else "WRONG"))
    print("\nSELFTEST %s" % ("PASSED" if ok else "FAILED"))
    if not ok:
        raise SystemExit("ANDON: the manifest walk does not behave as specified")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="append", default=[])
    ap.add_argument("--emit")
    ap.add_argument("--out")
    ap.add_argument("--occasion", default="")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out-json")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        sys.exit(0)
    if a.emit:
        if not (a.out and a.occasion):
            raise SystemExit("ANDON: --emit needs --out and --occasion")
        emit(a.emit, a.out, a.occasion, a.exclude)
    rows, all_held = [], True
    for mp in a.verify:
        held, row = verify(mp)
        rows.append(row)
        all_held &= held
        print()
    if a.verify:
        print("MANIFEST GATE: %s" % ("HELD" if all_held else "FIRED"))
        if a.out_json:
            json.dump(rows, open(a.out_json, "w"), indent=1)
        if not all_held:
            raise SystemExit("ANDON: a protected tree has changed - halt and report")
