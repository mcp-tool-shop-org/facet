"""Mask geometry shared by the tools that peel a figure's edge.

Extracted for E16-10 (E14 Ruling 24c), which ports the A3 local-half-width bound
to `texpass_iter`'s commit — the fix's missing consumer, found four experiments
late. `project_twins` already carried this function, and the alternative to
extracting it was a second copy: the thing this repo keeps paying for is two
implementations of one model drifting apart, so there is one.

The body is `project_twins.local_thickness` moved verbatim. Nothing in the
projector's arithmetic changes, and the twin-projection anchor is re-run across
the extraction to prove it.

`fit_background` joined it for E32, and the reason is the same one, one step
worse: FIVE copies of that model already exist (`project_twins:349`,
`e12_twin_readout:106`, `e14_twin_registration:48`, `gained_bg_check:94`,
`e08_registration:86`), because `project_twins` calls `ap.parse_args` at module
level (line 220) and therefore CANNOT BE IMPORTED - so every consumer that wanted
the route's background model had to retype it. This copy is ADDITIVE ONLY: it
adds a name that nothing previously imported, changes no existing function, and
leaves all five in place. The drift it does not fix is reported rather than
silently extended, and T64 asserts this copy is bit-identical to
`project_twins`' by extracting that file's own source, so the two cannot part
company unnoticed.
"""
import numpy as np
from scipy.ndimage import distance_transform_edt


def local_thickness(dist):
    """Half-width of the structure each pixel belongs to.

    `dist` is the distance transform of the figure mask, so dist(c) is the radius of
    the largest disc centred at c that fits inside the figure, and a pixel p belongs to
    that disc when ||p - c|| <= dist(c). Taking the largest such disc over all c gives
    the local thickness (Hildebrand & Ruegsegger). Evaluated with one EDT per integer
    radius band rather than an explicit disc dilation, which would be O(r^2) per pixel.
    """
    R = np.zeros_like(dist, dtype=np.float32)
    for r in range(int(np.ceil(dist.max())), 0, -1):
        core = dist >= r
        if not core.any():
            continue
        cover = distance_transform_edt(~core) <= r
        R[cover & (R == 0)] = r
    return R


def fit_background(img, b=24):
    """The route's background model: a per-channel quadratic surface, least-squares
    over a border ring the figure cannot reach.

    Body moved verbatim from `project_twins.fit_background` (E32). Corner-median
    keying is retired here after three independent failures - painted concept art
    has a gradient and a cast shadow, a Workbench clay is grey on grey, and a
    diffusion model paints a lit studio backdrop - and a quadratic REDUCES to the
    corner median on a genuinely flat field, so nothing measured under the old
    model loses comparability.

    Returns the fitted surface in float64, deliberately: `figure_mask` subtracts it
    channel-by-channel into a float32 residual, and returning float64 keeps that
    arithmetic bit-identical to the pre-factoring code.
    """
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    ring = np.zeros((H, W), dtype=bool)
    ring[:b, :] = ring[-b:, :] = ring[:, :b] = ring[:, -b:] = True
    cols = [np.ones(H * W), xx.ravel() / W, yy.ravel() / H,
            (xx.ravel() / W) ** 2, (yy.ravel() / H) ** 2,
            (xx.ravel() / W) * (yy.ravel() / H)]
    A = np.stack(cols, axis=1)
    Xr = A.reshape(H, W, -1)[ring]
    out = np.zeros((H, W, 3), dtype=np.float64)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(Xr, img[..., c][ring], rcond=None)
        out[..., c] = (A @ coef).reshape(H, W)
    return out
