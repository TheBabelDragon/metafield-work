"""Golden-path tests for Plaquette ABI v1."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from backends.reference.torch_backend import TorchReferenceBackend
from metafield.lattice.types import LatticeGeometry, PrecisionPolicy
from metafield.operators.protocol import WilsonParams

GOLDEN_ROOT = Path(__file__).parent / "goldens" / "plaquette_v1"
TOL = json.loads((Path(__file__).parent / "tolerances.json").read_text())["complex128"]


def _backend(L: int = 2) -> TorchReferenceBackend:
    return TorchReferenceBackend(LatticeGeometry(L=L, n_dims=4), PrecisionPolicy())


def test_unit_gauge_zero_action_and_unit_mean():
    be = _backend(2)
    U = be.unit_gauge(WilsonParams())
    S = float(be.plaquette_action(U, beta=5.5))
    P = float(be.mean_plaquette(U))
    assert abs(S) < TOL["plaquette_action_abs"]
    assert abs(P - 1.0) < TOL["mean_plaquette_abs"]


def _suites():
    man = GOLDEN_ROOT / "MANIFEST.json"
    if not man.exists():
        return []
    manifest = json.loads(man.read_text())
    return [Path(__file__).parent / "goldens" / s["path"] for s in manifest["suites"]]


@pytest.mark.parametrize("d", _suites() or [None], ids=lambda p: p.as_posix() if p else "none")
def test_plaquette_replay(d):
    if d is None:
        pytest.skip("no plaquette goldens")
    meta = json.loads((d / "golden.meta.json").read_text())
    assert meta["abi"] == "plaquette_v1"
    npz_path = d / "golden.npz"
    if not npz_path.exists():
        pytest.skip("npz not materialized")
    npz = np.load(npz_path)
    p = meta["params"]
    be = TorchReferenceBackend(LatticeGeometry(L=meta["L"], n_dims=p["n_dims"]), PrecisionPolicy())
    U = torch.from_numpy(npz["inputs__U"])
    S = float(be.plaquette_action(U, p["beta"]))
    P = float(be.mean_plaquette(U))
    assert abs(S - meta["metrics"]["plaquette_action"]) < TOL["plaquette_action_abs"]
    assert abs(P - meta["metrics"]["mean_plaquette"]) < TOL["mean_plaquette_abs"]
    if meta["kind"] in ("cold", "boundary"):
        assert abs(S) < TOL["plaquette_action_abs"]
        assert abs(P - 1.0) < TOL["mean_plaquette_abs"]
