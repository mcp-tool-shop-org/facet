"""T84 - silence callieri_border inf-inf subtract. Warning repair, not a
behaviour change.

THE LIVE MODULE IS NOT EDITED WHILE E46 IS MID-CHAIN. The authorized
patch sits at tools/callieri_border_repair.diff. t76 is not edited.
Public arrays must stay byte-identical to HEAD 1.0.0.

Derivation of the recorded hashes (2026-08-16):
  git rev-parse HEAD:tools/callieri_border.py
    -> ecdcbacb6e6ec51f5baf5afbd9ebd285a993aa50
  last edit: 2d883d5 (TOOL_VERSION 1.0.0)
  sha256 of np.ascontiguousarray(arr).tobytes()
  fixture: fixture_inf_bg_step() below
  real:    E:/AI/training/facet_E45/aov/view_0/{depth,sil,normal_world}.npy

CALIBRATION CLAIM (this file's named leg):
  fixture depth_edge_mask sha256 ==
  1d8d77359854a915472da8296da7806be8c53219062a6c77a88d553e611959c1
  A behaviour change, a different fixture, or a hash of a view instead
  of the array, misses this. The repaired form must land the same hash.

  python -m pytest tests/test_t84_callieri_border_repair.py::test_t84_calibration_fixture_edge_hash -q
"""
import ast
import hashlib
import importlib.util
import os
import subprocess
import sys
import warnings

import numpy as np
import pytest

from conftest import REPO, need

sys.path.insert(0, os.path.join(str(REPO), "tools"))
import callieri_border as CB  # noqa: E402


# ---------------------------------------------------------------------------
# HEAD 1.0.0 public-surface hashes. Computed against blob ecdcbac, not
# against this working tree. Do not regenerate from a repaired module.
# ---------------------------------------------------------------------------
HEAD_BLOB = "ecdcbacb6e6ec51f5baf5afbd9ebd285a993aa50"

FIXTURE_SHA = {
    "depth_edge_mask":
        "1d8d77359854a915472da8296da7806be8c53219062a6c77a88d553e611959c1",
    "mixed_depth_reject":
        "0161ca4cc9170775963efba8a2bb6a35937bbed4395349f6cd00d7dfc6ab9e9a",
    "border_weight":
        "fe958feecd6e0dac3261c7c29f529f7838ea80cb6e1716590d56c07c48466f2c",
    "facing_weight":
        "8df5ae96512f6ccf45d0eb9cb529000d9eb05535bf1573d9b90379f0f28a38ad",
}

REAL_SHA = {
    "depth_edge_mask":
        "f65bf08815c603c785eacc2dfb478ac470093b29b5d3360b48e364e9230937fc",
    "mixed_depth_reject":
        "4437c81f0e6a9c4804c5c9358e60cb9148834632d5a3e58658301f5edff29638",
    "border_weight":
        "ea7cf5e0ec7a236c65fcd54bf26f177189e2feabfcfc5ec6491f5b4636460548",
    "facing_weight":
        "e9b68eb0335424e53122b2b29ae96b0227e2ccada255c679284d0af353fea5b2",
}

CALIBRATION_EDGE_SHA = FIXTURE_SHA["depth_edge_mask"]
DIFF_PATH = os.path.join(str(REPO), "tools", "callieri_border_repair.diff")
E46_REPORT = os.path.join(
    str(REPO), "docs", "experiments", "E46-s3-run-report.md")


def sha256_array(arr):
    return hashlib.sha256(np.ascontiguousarray(arr).tobytes()).hexdigest()


def fixture_inf_bg_step():
    """+inf background, interior step so IQR>0 and thr>0.

    The T76 thin-bar is constant-Z, so thr==0 and _finite_neighbour_jump
    returns zeros without subtracting. This fixture is the one that
    actually reaches the two warning sites.
    """
    depth = np.full((32, 32), np.inf, dtype=np.float64)
    sil = np.zeros((32, 32), dtype=bool)
    sil[8:24, 8:24] = True
    depth[sil] = 1.0
    depth[8:24, 16:24] = 2.0
    nrm = np.zeros((32, 32, 3), dtype=np.float64)
    nrm[sil, 2] = 1.0
    return depth, sil, nrm


def pre_repair_jump(depth, thr):
    """Verbatim HEAD 1.0.0 :194-218. The form that warns."""
    if thr <= 0.0:
        return np.zeros(depth.shape, dtype=bool)
    fin = CB._finite(depth)
    edge = np.zeros(depth.shape, dtype=bool)
    pair = fin[:, :-1] & fin[:, 1:]
    jump = np.abs(depth[:, :-1] - depth[:, 1:]) > thr
    hit = pair & jump
    edge[:, :-1] |= hit
    edge[:, 1:] |= hit
    pair = fin[:-1, :] & fin[1:, :]
    jump = np.abs(depth[:-1, :] - depth[1:, :]) > thr
    hit = pair & jump
    edge[:-1, :] |= hit
    edge[1:, :] |= hit
    return edge


def repaired_jump(depth, thr):
    """v1.0.1 form. Masked indexing, same as _typical_neighbour_abs."""
    if thr <= 0.0:
        return np.zeros(depth.shape, dtype=bool)
    fin = CB._finite(depth)
    edge = np.zeros(depth.shape, dtype=bool)
    pair = fin[:, :-1] & fin[:, 1:]
    jump = np.zeros(pair.shape, dtype=bool)
    if pair.any():
        jump[pair] = np.abs(depth[:, :-1][pair] - depth[:, 1:][pair]) > thr
    hit = pair & jump
    edge[:, :-1] |= hit
    edge[:, 1:] |= hit
    pair = fin[:-1, :] & fin[1:, :]
    jump = np.zeros(pair.shape, dtype=bool)
    if pair.any():
        jump[pair] = np.abs(depth[:-1, :][pair] - depth[1:, :][pair]) > thr
    hit = pair & jump
    edge[:-1, :] |= hit
    edge[1:, :] |= hit
    return edge


def public_surface(depth, sil, nrm, jump_fn):
    prev = CB._finite_neighbour_jump
    CB._finite_neighbour_jump = jump_fn
    try:
        return {
            "depth_edge_mask": CB.depth_edge_mask(depth, silhouette=sil),
            "mixed_depth_reject": CB.mixed_depth_reject(depth, silhouette=sil),
            "border_weight": CB.border_weight(depth, sil),
            "facing_weight": CB.facing_weight(nrm, 6.0),
        }
    finally:
        CB._finite_neighbour_jump = prev


def subtract_warnings(recorded):
    out = []
    for w in recorded:
        if issubclass(w.category, RuntimeWarning) and "subtract" in str(w.message):
            out.append(w)
    return out


def test_t84_calibration_fixture_edge_hash():
    depth, sil, nrm = fixture_inf_bg_step()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        surf = public_surface(depth, sil, nrm, pre_repair_jump)
    got = sha256_array(surf["depth_edge_mask"])
    assert got == CALIBRATION_EDGE_SHA, (
        "CALIBRATION: fixture depth_edge_mask sha256 is %s, not %s "
        "(HEAD blob %s)"
        % (got, CALIBRATION_EDGE_SHA, HEAD_BLOB))


def test_t84_fixture_public_surface_byte_identical():
    depth, sil, nrm = fixture_inf_bg_step()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        before = public_surface(depth, sil, nrm, pre_repair_jump)
    after = public_surface(depth, sil, nrm, repaired_jump)
    for name in FIXTURE_SHA:
        b = sha256_array(before[name])
        a = sha256_array(after[name])
        assert b == FIXTURE_SHA[name], (
            "HEAD hash moved for %s: %s (want %s)"
            % (name, b, FIXTURE_SHA[name]))
        assert a == b, (
            "repair changed %s: after %s before %s" % (name, a, b))


def test_t84_pre_repair_form_warns():
    """The sibling: this fixture DID provoke the warning on HEAD."""
    depth, sil, nrm = fixture_inf_bg_step()
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always", RuntimeWarning)
        public_surface(depth, sil, nrm, pre_repair_jump)
    hits = subtract_warnings(rec)
    assert hits, (
        "inf-bg fixture produced no subtract RuntimeWarning against the "
        "pre-repair form; the silence leg then cannot fail")


def test_t84_repaired_form_is_silent():
    depth, sil, nrm = fixture_inf_bg_step()
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always", RuntimeWarning)
        public_surface(depth, sil, nrm, repaired_jump)
    hits = subtract_warnings(rec)
    assert hits == [], (
        "repaired form still warned: %s"
        % [str(h.message) for h in hits])
    if CB.TOOL_VERSION == "1.0.1":
        with warnings.catch_warnings(record=True) as rec:
            warnings.simplefilter("always", RuntimeWarning)
            CB.depth_edge_mask(depth, silhouette=sil)
            CB.border_weight(depth, sil)
        hits = subtract_warnings(rec)
        assert hits == [], (
            "live 1.0.1 module still warned: %s"
            % [str(h.message) for h in hits])


def test_t84_t76_pin_still_holds():
    """T76 file is not edited. The number still has to be 2/3."""
    depth, sil = CB.fixture_thin_bar()
    w = CB.border_weight(depth, sil)
    got = float(w[CB.CALIBRATION_RC, CB.CALIBRATION_CC])
    assert got == pytest.approx(CB.CALIBRATION_WEIGHT, abs=1e-6), got


def test_t84_timing_gate():
    """An instrument does not change under the session using it."""
    if os.path.isfile(E46_REPORT):
        assert CB.TOOL_VERSION == "1.0.1", (
            "E46 has landed; apply tools/callieri_border_repair.diff "
            "(live TOOL_VERSION is %r)" % CB.TOOL_VERSION)
    else:
        assert CB.TOOL_VERSION == "1.0.0", (
            "E46 is mid-chain; do not edit tools/callieri_border.py "
            "(live TOOL_VERSION is %r)" % CB.TOOL_VERSION)
        assert os.path.isfile(DIFF_PATH), (
            "repair diff missing at %s" % DIFF_PATH)


# The 1.0.0 blob, pinned at the fold (advisor, 2026-08-16). The leg was written
# against a floating HEAD and was correct in the pre-fold tree; the moment the
# repair is committed, HEAD carries 1.0.1 and the diff no longer applies to it.
# The property the leg proves is "the diff is exactly the 1.0.0 -> 1.0.1 delta",
# and 1.0.0 is this blob (the diff's own index line names its short form).
V100_BLOB = "ecdcbacb6e6ec51f5baf5afbd9ebd285a993aa50"


def test_t84_repair_diff_applies_to_the_v100_blob(tmp_path):
    src = subprocess.check_output(
        ["git", "cat-file", "blob", V100_BLOB],
        cwd=str(REPO))
    work = tmp_path / "apply"
    (work / "tools").mkdir(parents=True)
    (work / "tools" / "callieri_border.py").write_bytes(src)
    diff = open(DIFF_PATH, "rb").read()
    (work / "repair.diff").write_bytes(diff)
    p = subprocess.run(
        ["git", "apply", "--check", "repair.diff"],
        cwd=str(work), capture_output=True)
    assert p.returncode == 0, (
        "diff does not apply to HEAD callieri_border.py\n%s\n%s"
        % (p.stdout.decode("ascii", "replace"),
           p.stderr.decode("ascii", "replace")))
    p = subprocess.run(
        ["git", "apply", "repair.diff"],
        cwd=str(work), capture_output=True)
    assert p.returncode == 0, p.stderr.decode("ascii", "replace")
    patched = (work / "tools" / "callieri_border.py").read_text(encoding="utf-8")
    assert 'TOOL_VERSION = "1.0.1"' in patched
    tree = ast.parse(patched)
    bares = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.Assert)]
    assert bares == [], "patched source has bare assert at %s" % bares
    spec = importlib.util.spec_from_file_location(
        "cb_patched", str(work / "tools" / "callieri_border.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    depth, sil, nrm = fixture_inf_bg_step()
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always", RuntimeWarning)
        edge = mod.depth_edge_mask(depth, silhouette=sil)
    assert subtract_warnings(rec) == []
    assert sha256_array(edge) == CALIBRATION_EDGE_SHA


@pytest.mark.artifacts
def test_t84_real_frame_public_surface_byte_identical(assets):
    aov = need(assets, "facet_E45/aov/view_0")
    depth = np.load(str(aov / "depth.npy"))
    sil = np.load(str(aov / "sil.npy")).astype(bool)
    nrm = np.load(str(aov / "normal_world.npy"))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        before = public_surface(depth, sil, nrm, pre_repair_jump)
    after = public_surface(depth, sil, nrm, repaired_jump)
    for name in REAL_SHA:
        b = sha256_array(before[name])
        a = sha256_array(after[name])
        assert b == REAL_SHA[name], (
            "HEAD hash moved for real %s: %s (want %s)"
            % (name, b, REAL_SHA[name]))
        assert a == b, (
            "repair changed real %s: after %s before %s" % (name, a, b))


