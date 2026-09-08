"""Golden-path tests for Reduction ABI v1."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from backends.reference.torch_backend import TorchReferenceBackend
from metafield.lattice.types import LatticeGeometry, PrecisionPolicy
from metafield.operators.protocol import WilsonParams

GOLDEN_ROOT = Path(__file__).parent / "goldens" / "reduction_v1"
TOL = json.loads((Path(__file__).parent / "tolerances.json").read_text())["complex128"]


def _backend(L: int = 2) -> TorchReferenceBackend:
    return TorchReferenceBackend(LatticeGeometry(L=L, n_dims=4), PrecisionPolicy())


def test_dot_conjugate_symmetry():
    be = _backend()
    params = WilsonParams()
    g = torch.Generator().manual_seed(3)
    a = be.random_fermion(params, g)
    b = be.random_fermion(params, g)
    lhs = complex(be.complex_dot(a, b))
    rhs = complex(be.complex_dot(b, a)).conjugate()
    assert abs(lhs - rhs) < TOL["reduction_dot_abs"]


def test_norm_matches_dot():
    be = _backend()
    params = WilsonParams()
    g = torch.Generator().manual_seed(5)
    a = be.random_fermion(params, g)
    n = float(be.complex_norm(a))
    from_dot = float(be.complex_dot(a, a).real) ** 0.5
    assert abs(n - from_dot) < TOL["reduction_norm_abs"]


def test_axpy_affine():
    be = _backend()
    params = WilsonParams()
    g = torch.Generator().manual_seed(9)
    x = be.random_fermion(params, g)
    y = be.random_fermion(params, g)
    alpha = 0.25 + 0.5j
    out = be.axpy(alpha, x, y)
    err = float(be.complex_norm(out - (alpha * x + y)))
    assert err < TOL["reduction_axpy_abs"]


def _suites():
    man = GOLDEN_ROOT / "MANIFEST.json"
    if not man.exists():
        return []
    manifest = json.loads(man.read_text())
    return [Path(__file__).parent / "goldens" / s["path"] for s in manifest["suites"]]


@pytest.mark.parametrize("d", _suites() or [None], ids=lambda p: p.as_posix() if p else "none")
def test_reduction_replay(d):
    if d is None:
        pytest.skip("no reduction goldens")
    meta = json.loads((d / "golden.meta.json").read_text())
    assert meta["abi"] == "reduction_v1"
    assert meta["metrics"]["dot_conj_err"] < TOL["reduction_dot_abs"]
    npz_path = d / "golden.npz"
    if not npz_path.exists():
        pytest.skip("npz not materialized")
    npz = np.load(npz_path)
    p = meta["params"]
    params = WilsonParams(color_dim=p["color_dim"], spinor_dim=p["spinor_dim"])
    be = TorchReferenceBackend(LatticeGeometry(L=meta["L"], n_dims=p["n_dims"]), PrecisionPolicy())
    psi = torch.from_numpy(npz["inputs__psi"])
    phi = torch.from_numpy(npz["inputs__phi"])
    alpha = complex(meta["metrics"]["axpy_alpha_real"], meta["metrics"]["axpy_alpha_imag"])
    dot = complex(be.complex_dot(psi, phi))
    exp = complex(meta["metrics"]["dot_real"], meta["metrics"]["dot_imag"])
    assert abs(dot - exp) < TOL["reduction_dot_abs"]
    assert abs(float(be.complex_norm(psi)) - meta["metrics"]["norm"]) < TOL["reduction_norm_abs"]
    got = be.axpy(alpha, psi, phi)
    exp_y = torch.from_numpy(npz["outputs__axpy"])
    rel = float(
        torch.linalg.vector_norm((got - exp_y).reshape(-1))
        / torch.linalg.vector_norm(exp_y.reshape(-1)).clamp_min(1e-30)
    )
    assert rel < TOL["reduction_axpy_rel"]
