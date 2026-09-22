"""T102 - the prop library's size contract.

Every reconstruction this route makes is normalised to ~1.002 on its longest axis, so a
prop mesh carries NO true scale. The contract is that a prop's real size is declared,
stored in the file, and CHECKED rather than trusted. These legs pin the checking.

THE CAN-FAIL LEGS COME FIRST, and one of them is the whole point: an unscaled
reconstruction wearing a prop's sidecar must be refused. That is the exact mistake the
contract exists to prevent - a file that looks like a prop, declares a sensible size, and
is actually 1.8 m tall.

Everything printed here is ASCII (the repo's law).
"""
import json
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
import trimesh

TOOL = pathlib.Path(__file__).resolve().parents[1] / "tools" / "prop_scale.py"
METRES_PER_UNIT = 1.8


def _normalised_box(longest=1.002, ratios=(0.70, 1.0, 0.20)):
    """A stand-in for a reconstruction: a box normalised to ~1.002 on its longest axis."""
    e = np.array(ratios) * longest
    return trimesh.creation.box(extents=e)


def _write(mesh, path):
    path.write_bytes(trimesh.exchange.gltf.export_glb(trimesh.Scene({"body": mesh})))
    return path


def _run(*args):
    p = subprocess.run([sys.executable, str(TOOL), *[str(a) for a in args]],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    return p.returncode, p.stdout + p.stderr


def test_t102_an_unscaled_reconstruction_wearing_a_sidecar_is_refused():
    """CAN-FAIL LEG, and the one the contract exists for."""
    with tempfile.TemporaryDirectory() as d:
        dd = pathlib.Path(d)
        raw = _write(_normalised_box(), dd / "raw.glb")
        rc, log = _run("--glb", raw, "--out", dd / "p.glb", "--name", "x",
                       "--real-mm", 758, "--axis", "height")
        assert rc == 0, log
        # now swap the good prop's mesh for the unscaled one, keeping the sidecar
        (dd / "p.glb").write_bytes(raw.read_bytes())
        rc, log = _run("--verify", dd / "p.glb")
        assert rc == 2, "a 1.8 m prop passed verification\n%s" % log
        assert "UNSCALED reconstruction" in log, log
        assert "1803" in log, "the refusal did not report the real size in mm\n%s" % log


def test_t102_a_prop_with_no_sidecar_is_refused():
    with tempfile.TemporaryDirectory() as d:
        dd = pathlib.Path(d)
        p = _write(_normalised_box(), dd / "lonely.glb")
        rc, log = _run("--verify", p)
        assert rc != 0 and "no sidecar" in log, log


def test_t102_the_declared_size_lands_in_the_file():
    with tempfile.TemporaryDirectory() as d:
        dd = pathlib.Path(d)
        raw = _write(_normalised_box(), dd / "raw.glb")
        rc, log = _run("--glb", raw, "--out", dd / "p.glb", "--name", "shield",
                       "--real-mm", 758, "--axis", "height", "--attach", "forearm_l")
        assert rc == 0, log
        meta = json.loads((dd / "p.prop.json").read_text())
        assert meta["real_mm"] == 758 and meta["attach"] == "forearm_l", meta
        g = trimesh.load(dd / "p.glb", process=False)
        g = g.to_geometry() if hasattr(g, "to_geometry") else g
        size = g.bounds[1] - g.bounds[0]
        assert abs(size[1] - 758 / 1000.0 / METRES_PER_UNIT) < 1e-6, size
        # and the OTHER axes must scale with it - a prop is not stretched to fit
        assert abs(size[0] / size[1] - 0.70) < 1e-3, (
            "the aspect ratio moved; scaling must be uniform: %s" % size)


def test_t102_verify_round_trips_what_build_wrote():
    with tempfile.TemporaryDirectory() as d:
        dd = pathlib.Path(d)
        raw = _write(_normalised_box(), dd / "raw.glb")
        _run("--glb", raw, "--out", dd / "p.glb", "--name", "s", "--real-mm", 600)
        rc, log = _run("--verify", dd / "p.glb")
        assert rc == 0 and "PROP OK" in log, log
        assert "600" in log


def test_t102_a_zero_extent_axis_is_refused_rather_than_divided_by():
    with tempfile.TemporaryDirectory() as d:
        dd = pathlib.Path(d)
        flat = trimesh.Trimesh(vertices=[[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                               faces=[[0, 1, 2]], process=False)
        raw = _write(flat, dd / "flat.glb")
        rc, log = _run("--glb", raw, "--out", dd / "p.glb", "--name", "f",
                       "--real-mm", 100, "--axis", "z")
        assert rc != 0 and "zero extent" in log, log


def test_t102_the_unit_system_is_stated_in_the_source():
    """A tool that silently assumes a scale is the thing being fixed."""
    src = TOOL.read_text(encoding="utf-8")
    assert "METRES_PER_UNIT = 1.8" in src
    assert "1.0 unit = 1.8 m" in src, (
        "the unit system is no longer stated in the tool's own docstring")
