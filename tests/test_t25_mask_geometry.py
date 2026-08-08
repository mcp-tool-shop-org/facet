"""T25 (E20 U2) - mask_geometry.local_thickness, and the A3 bound as a property.

WHY THIS FILE EXISTS. `local_thickness` is the shared model behind the A3 bound
in BOTH consumers (project_twins:392 aliases it; texpass_iter:435 calls it for
the E16-10 port), it was extracted precisely so there would not be two copies -
and it had no test of its own. It is also one of only two units in E20's list
that is genuinely importable: project_twins, texpass_finalize and mesh_stats run
their pipelines at module level, so they cannot be imported at all (reported in
E20-coverage-report.md).

THE ORACLE IS INDEPENDENT, not a re-run of the implementation. local_thickness's
own docstring names the alternative it avoided - "an explicit disc dilation,
which would be O(r^2) per pixel" - so this file WRITES that slow version and
asserts the fast one equals it on small grids. A test that recomputed the banded
EDT would be the same implementation checking itself.

THE A3 SAFETY PROPERTY is the point of the second half. The bound is
`e <= edge_frac * local half-width` with edge_frac = 1/3 (E08 A3, ported by
E16-10). local_thickness is INTEGER-QUANTIZED and therefore OVERESTIMATES a true
half-width - measured here, R = ceil(W/2) against a true W/2 - so the property
that matters is not that R is exact but that the erosion it authorizes still
cannot consume the structure it is protecting. That is asserted per width, with
the margin printed.

Source is ASCII bytes (the repo's law).
"""
import importlib.util
import math

import numpy as np
import pytest
from scipy.ndimage import distance_transform_edt

from conftest import tool

EDGE_FRAC = 1.0 / 3.0        # project_twins' --edge-frac default; E08 A3's third


@pytest.fixture(scope="module")
def mg():
    """mask_geometry imported in-process.

    It is 33 lines of pure numpy/scipy with no module-level execution, so import
    has no side effects - checked by reading it, and it is the shortest tool in
    the repo. Imported here rather than through a conftest fixture because
    E20-ruling 2 reserves conftest's fixture plumbing to E18's lane.
    """
    spec = importlib.util.spec_from_file_location(
        "mask_geometry", tool("mask_geometry.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# the independent oracle
# ---------------------------------------------------------------------------

def brute_local_thickness(dist):
    """The O(r^2) explicit-disc version local_thickness's docstring avoided.

    R(p) = the largest integer r such that some centre c has dist(c) >= r and
    ||p - c|| <= r. Written with explicit loops over every (p, c) pair, so it is
    obviously the definition and obviously too slow for a real atlas - which is
    exactly what makes it a usable oracle on a 15x15 grid.
    """
    H, W = dist.shape
    rmax = int(math.ceil(dist.max())) if dist.size else 0
    out = np.zeros((H, W), dtype=np.float32)
    centres = [(cy, cx, dist[cy, cx]) for cy in range(H) for cx in range(W)
               if dist[cy, cx] > 0]
    for py in range(H):
        for px in range(W):
            best = 0
            for r in range(rmax, 0, -1):
                if r <= best:
                    break
                for (cy, cx, dc) in centres:
                    if dc >= r and (py - cy) ** 2 + (px - cx) ** 2 <= r * r:
                        best = r
                        break
            out[py, px] = best
    return out


def edt(mask):
    return distance_transform_edt(mask)


# ---------------------------------------------------------------------------
# shape builders - deterministic, tiny, no fixture files needed
# ---------------------------------------------------------------------------

def bar(width, n=15):
    """A horizontal bar of exactly `width` rows, spanning the full grid."""
    m = np.zeros((n, n), dtype=bool)
    lo = (n - width) // 2
    m[lo:lo + width, :] = True
    return m


def square(width, n=15):
    m = np.zeros((n, n), dtype=bool)
    lo = (n - width) // 2
    m[lo:lo + width, lo:lo + width] = True
    return m


def thin_beside_wide(n=21):
    """A 2px stalk and a 10px block in one mask - the mixed case the A3 bound
    exists for (a fixed peel costs a thin structure everything and a torso 4%)."""
    m = np.zeros((n, n), dtype=bool)
    m[3:18, 2:4] = True
    m[3:18, 8:18] = True
    return m


# ---------------------------------------------------------------------------
# equality with the oracle
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("mask,label", [
    (bar(1), "bar w=1"),
    (bar(2), "bar w=2"),
    (bar(3), "bar w=3"),
    (bar(5), "bar w=5"),
    (square(1), "square 1x1"),
    (square(3), "square 3x3"),
    (square(5), "square 5x5"),
    (thin_beside_wide(), "thin beside wide"),
])
def test_t25_matches_the_explicit_disc_oracle(mg, mask, label):
    """The fast banded implementation equals the slow definition, everywhere."""
    d = edt(mask)
    fast = mg.local_thickness(d)
    slow = brute_local_thickness(d)
    bad = int((fast != slow).sum())
    assert bad == 0, (
        "%s: %d of %d pixels disagree with the explicit-disc definition; "
        "first few fast=%s slow=%s"
        % (label, bad, fast.size, fast[fast != slow][:5], slow[fast != slow][:5]))


def test_t25_returns_float32_over_the_whole_grid(mg):
    d = edt(bar(3))
    R = mg.local_thickness(d)
    assert R.dtype == np.float32
    assert R.shape == d.shape


def test_t25_an_empty_mask_yields_all_zeros(mg):
    """dist.max() is 0, so the radius loop never runs. It must return zeros
    rather than raise - the degenerate input a caller can genuinely hand it."""
    R = mg.local_thickness(edt(np.zeros((9, 9), dtype=bool)))
    assert R.shape == (9, 9)
    assert not R.any()


# ---------------------------------------------------------------------------
# what R actually is, measured
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("width", [1, 2, 3, 4, 5, 6, 7, 9])
def test_t25_bar_thickness_is_ceil_half_width(mg, width):
    """MEASURED, then pinned: on a bar of width W, R = ceil(W/2) on every pixel
    of the bar. Odd and even widths one apart share a value (w=1 and w=2 both
    give 1), which is the integer quantization and is where the overestimate in
    the next test comes from.
    """
    m = bar(width)
    R = mg.local_thickness(edt(m))
    on = R[m]
    expected = math.ceil(width / 2.0)
    assert on.min() == on.max() == expected, (
        "bar w=%d: R ranged %.1f..%.1f, expected a flat %d"
        % (width, on.min(), on.max(), expected))


def test_t25_thickness_is_monotone_in_width(mg):
    """A wider structure never reports a smaller half-width."""
    prev = 0.0
    for w in (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13):
        R = mg.local_thickness(edt(bar(w, n=31)))
        val = float(R[bar(w, n=31)].max())
        assert val >= prev, "w=%d reported %.1f after %.1f" % (w, val, prev)
        prev = val


def test_t25_thin_and_wide_are_measured_separately_in_one_mask(mg):
    """The whole reason the bound is local: one mask, two structures, two
    half-widths. A global constant cannot do this and that is the E08 A3
    finding."""
    m = thin_beside_wide()
    R = mg.local_thickness(edt(m))
    thin = R[3:18, 2:4]
    wide = R[3:18, 8:18]
    assert thin.max() < wide.max(), (
        "thin stalk reported %.1f, wide block %.1f - the local model is not "
        "separating them" % (thin.max(), wide.max()))
    assert thin.max() == 1.0, thin.max()


def test_t25_r_is_nonzero_off_the_mask_so_membership_is_a_separate_question(mg):
    """CHARACTERIZED, because a consumer has already been bitten by it.

    `cover` is every pixel within r of a core, INCLUDING background - so R is
    positive on background near the figure. texpass_iter:437 carries the
    consequence in its own words: mask membership "IS REQUIRED SEPARATELY, and
    leaving it implicit was a real defect in the first cut of this port ...
    Measured before the fix: 38,041 texels committed against 4,344."

    This test pins the property that makes that separate check necessary. It
    does not call the property wrong: the function is documented as taking a
    distance transform and returning a thickness field, and both live consumers
    now gate membership explicitly (project_twins:743, texpass_iter:435-443).
    """
    m = bar(3)
    R = mg.local_thickness(edt(m))
    off = R[~m]
    assert off.max() > 0, (
        "R is zero everywhere off the mask - then texpass_iter's explicit "
        "membership check would be guarding nothing, and its recorded 38,041 "
        "vs 4,344 measurement would need re-reading")


# ---------------------------------------------------------------------------
# the A3 safety property
# ---------------------------------------------------------------------------
# ANCHOR: E08 A3 as ported by E16-10 - `e <= edge_frac * local half-width`,
# edge_frac = 1/3. E16-10 measured ZERO violations on real structures; this is
# the same invariant as a property over constructed ones, including the widths
# where the quantization is worst.

@pytest.mark.parametrize("width", [1, 2, 3, 4, 5, 6, 7, 9, 11, 15])
def test_t25_a3_erosion_cannot_consume_the_structure(mg, width, capsys):
    """The property that matters, given R overestimates.

    R = ceil(W/2) against a TRUE half-width of W/2, so `edge_frac * R` is a
    bound derived from an overestimate - worst at W=1, where R is 2x the truth.
    The invariant is still safe iff the authorized peel stays strictly inside
    the structure's own true half-width. Asserted per width, with the margin
    reported so a future change that eats the margin is visible rather than
    merely passing.
    """
    m = bar(width, n=31)
    R = mg.local_thickness(edt(m))
    r_on = float(R[m].max())
    e = EDGE_FRAC * r_on
    true_half = width / 2.0
    assert e < true_half, (
        "w=%d: A3 authorizes a peel of %.3f px against a true half-width of "
        "%.3f px - the erosion would reach past the structure's centre line, "
        "which is the over-erosion direction the invariant exists to bound"
        % (width, e, true_half))
    print("A3 w=%2d: R=%.0f  e=%.3f  true half-width=%.3f  margin x%.2f"
          % (width, r_on, e, true_half, true_half / e))


def test_t25_a3_bound_never_exceeds_the_reported_half_width(mg):
    """The trivial leg, stated because its absence is what a proxy gate looks
    like: whatever R says, one third of it is less than it, everywhere, on a
    mask with two very different structures in it."""
    m = thin_beside_wide()
    R = mg.local_thickness(edt(m))
    e = EDGE_FRAC * R
    viol = int((e[m] > R[m]).sum())
    assert viol == 0, "%d pixels where the peel exceeds the half-width" % viol


def test_t25_a3_is_tightest_on_the_thinnest_structure(mg):
    """Direction check: the bound must SHRINK as the structure thins, or it is
    not local. E08's cost analysis - "the cost of a fixed peel runs inversely
    with local feature width" - is the anchor."""
    peels = []
    for w in (1, 3, 7, 15):
        R = mg.local_thickness(edt(bar(w, n=31)))
        peels.append(EDGE_FRAC * float(R[bar(w, n=31)].max()))
    assert peels == sorted(peels), peels
    assert peels[0] < peels[-1]
