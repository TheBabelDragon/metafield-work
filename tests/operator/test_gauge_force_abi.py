"""Golden-path tests for Gauge-force ABI v1."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from backends.reference.torch_backend import TorchReferenceBackend, dagger
from metafield.lattice.types import LatticeGeometry, PrecisionPolicy
from metafield.operators.protocol import WilsonParams

GOLDEN_ROOT = Path(__file__).parent / "goldens" / "gauge_force_v1"
TOL = json.loads((Path(__file__).parent / "tolerances.json").read_text())["complex128"]


def _backend(L: int = 2) -> TorchReferenceBackend:
    return TorchReferenceBackend(LatticeGeometry(L=L, n_dims=4), PrecisionPolicy())


def test_unit_gauge_zero_force():
    be = _backend(2)
    U = be.unit_gauge(WilsonParams())
    F = be.gauge_force(U, beta=5.5)
    assert float(be.complex_norm(F)) < TOL["gauge_force_cold_abs"]


def test_force_is_sun_algebra():
    be = _backend(2)
    params = WilsonParams()
    U = be.unit_gauge(params)
    F = be.gauge_force(U, beta=5.5)
    assert float(be.complex_norm(F + dagger(F))) < TOL["gauge_force_ah_abs"]
    tr = torch.diagonal(F, dim1=-2, dim2=-1).sum(-1)
    assert float(torch.linalg.vector_norm(tr.reshape(-1))) < TOL["gauge_force_tr_abs"]


def _random_sun(be, params, seed: int):
    g = torch.Generator().manual_seed(seed)
    U0 = be.unit_gauge(params)
    shape = U0.shape
    n = params.color_dim
    real = torch.randn(shape, generator=g, dtype=torch.float64)
    imag = torch.randn(shape, generator=g, dtype=torch.float64)
    A = (real + 1j * imag).to(be.dtype) * 0.05
    H = 0.5 * (A + A.conj().transpose(-1, -2))
    tr = torch.diagonal(H, dim1=-2, dim2=-1).sum(-1)
    eye = torch.eye(n, dtype=be.dtype)
    H = H - (tr / n)[..., None, None] * eye
    HH = 1j * (1j * H)
    evals, evecs = torch.linalg.eigh(HH)
    phase = torch.exp(-1j * evals.to(be.dtype))
    Vh = evecs.conj().transpose(-1, -2)
    return (evecs @ (phase[..., :, None] * Vh)) @ U0


def test_staples_match_autograd_on_random():
    be = _backend(2)
    params = WilsonParams()
    U = _random_sun(be, params, seed=1003)
    F = be.gauge_force(U, 5.5)
    F_ag = be.gauge_force_autograd(U, 5.5)
    rel = float(
        torch.linalg.vector_norm((F - F_ag).reshape(-1))
        / torch.linalg.vector_norm(F.reshape(-1)).clamp_min(1e-30)
    )
    assert rel < TOL["gauge_force_rel"]


def _suites():
    man = GOLDEN_ROOT / "MANIFEST.json"
    if not man.exists():
        return []
    manifest = json.loads(man.read_text())
    return [Path(__file__).parent / "goldens" / s["path"] for s in manifest["suites"]]


@pytest.mark.parametrize("d", _suites() or [None], ids=lambda p: p.as_posix() if p else "none")
def test_gauge_force_replay(d):
    if d is None:
        pytest.skip("no gauge-force goldens")
    meta = json.loads((d / "golden.meta.json").read_text())
    assert meta["abi"] == "gauge_force_v1"
    assert meta["metrics"]["anti_hermitian_residual"] < TOL["gauge_force_ah_abs"]
    assert meta["metrics"]["traceless_residual"] < TOL["gauge_force_tr_abs"]
    npz_path = d / "golden.npz"
    if not npz_path.exists():
        pytest.skip("npz not materialized")
    npz = np.load(npz_path)
    p = meta["params"]
    be = TorchReferenceBackend(LatticeGeometry(L=meta["L"], n_dims=p["n_dims"]), PrecisionPolicy())
    U = torch.from_numpy(npz["inputs__U"])
    F = be.gauge_force(U, p["beta"])
    exp = torch.from_numpy(npz["outputs__F"])
    den = torch.linalg.vector_norm(exp.reshape(-1)).clamp_min(1e-30)
    rel = float(torch.linalg.vector_norm((F - exp).reshape(-1)) / den)
    if meta["kind"] in ("cold", "boundary"):
        assert float(be.complex_norm(F)) < TOL["gauge_force_cold_abs"]
    else:
        assert rel < TOL["gauge_force_rel"]
