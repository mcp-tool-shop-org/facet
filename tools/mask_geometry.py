"""Mask geometry shared by the tools that peel a figure's edge.

Extracted for E16-10 (E14 Ruling 24c), which ports the A3 local-half-width bound
to `texpass_iter`'s commit — the fix's missing consumer, found four experiments
late. `project_twins` already carried this function, and the alternative to
extracting it was a second copy: the thing this repo keeps paying for is two
implementations of one model drifting apart, so there is one.

The body is `project_twins.local_thickness` moved verbatim. Nothing in the
projector's arithmetic changes, and the twin-projection anchor is re-run across
the extraction to prove it.
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
