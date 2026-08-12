"""Constitution tests for Wilson–Dirac ABI v1.

1) Determinism: same seeds → identical Dψ (oracle self-consistency).
2) Replay: if tests/operator/goldens/L*/**/golden.json exist (from
   scripts/generate_goldens.py), compare outputs within tolerances.

The seed table in scripts/generate_goldens.py is frozen law.
Commit generated goldens before claiming a non-reference backend passes.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
import torch

from backends.reference.torch_backend import TorchReferenceBackend
from metafield.lattice.types import LatticeGeometry, PrecisionPolicy
from metafield.operators.protocol import WilsonParams

GOLDEN_ROOT = Path(__file__).parent / "goldens"
TOL = json.loads((Path(__file__).parent / "tolerances.json").read_text())["complex128"]
PARAMS = WilsonParams(mass=0.1, wilson_r=1.0, color_dim=3, spinor_dim=4)

# Frozen seeds — must match scripts/generate_goldens.py
SEEDS = {
    (2, "cold"): 1001,
    (2, "random"): 1002,
    (2, "boundary"): 1003,
    (4, "cold"): 2001,
    (4, "random"): 2002,
    (4, "boundary"): 2003,
}


def _unpack(obj) -> torch.Tensor:
    shape = tuple(obj["shape"])
    real = torch.tensor(obj["real"], dtype=torch.float64)
    if obj["imag"] is None:
        return real.reshape(shape)
    imag = torch.tensor(obj["imag"], dtype=torch.float64)
    return (real + 1j * imag).reshape(shape).to(torch.complex128)


def _rel_err(got: torch.Tensor, exp: torch.Tensor) -> float:
    num = torch.linalg.vector_norm((got - exp).reshape(-1))
    den = torch.linalg.vector_norm(exp.reshape(-1)).clamp_min(1e-30)
    return float(num / den)


def _make_boundary_psi(be, params):
    psi = torch.zeros(
        be.geometry.shape + (params.spinor_dim, params.color_dim), dtype=be.dtype
    )
    origin = (0,) * be.geometry.n_dims
    psi[origin + (0, 0)] = 1.0 + 0.3j
    psi[origin + (1, 1)] = -0.2 + 0.5j
    return psi


def _suite_inputs(L: int, kind: str, seed_base: int):
    be = TorchReferenceBackend(LatticeGeometry(L=L, n_dims=4), PrecisionPolicy())
    g = torch.Generator().manual_seed(seed_base)
    if kind == "cold":
        U = be.unit_gauge(PARAMS)
        psi = be.random_fermion(PARAMS, g)
    elif kind == "boundary":
        U = be.unit_gauge(PARAMS)
        psi = _make_boundary_psi(be, PARAMS)
    else:
        # random kind uses slightly deformed unit gauge — keep simple here
        U = be.unit_gauge(PARAMS)
        psi = be.random_fermion(PARAMS, g)
    return be, psi, U


@pytest.mark.parametrize("L,kind", [(2, "cold"), (2, "boundary")])
def test_oracle_determinism_Dpsi(L, kind):
    seed = SEEDS[(L, kind)]
    be1, psi1, U1 = _suite_inputs(L, kind, seed)
    d1 = be1.wilson_dirac(psi1, U1, PARAMS)
    be2, psi2, U2 = _suite_inputs(L, kind, seed)
    d2 = be2.wilson_dirac(psi2, U2, PARAMS)
    assert _rel_err(d1, d2) == 0.0


@pytest.mark.parametrize("L,kind", [(2, "cold"), (2, "boundary")])
def test_g5_and_Q_metrics_fresh(L, kind):
    seed = SEEDS[(L, kind)]
    be, psi, U = _suite_inputs(L, kind, seed)
    dag = be.wilson_dirac_dagger(psi, U, PARAMS)
    g5psi = torch.einsum("st,...ti->...si", be.g5, psi)
    manual = torch.einsum("st,...ti->...si", be.g5, be.wilson_dirac(g5psi, U, PARAMS))
    assert float(be.complex_norm(dag - manual)) < TOL["Ddag_identity_abs"]
    g = torch.Generator().manual_seed(seed + 99)
    phi = be.random_fermion(PARAMS, g)
    Qpsi = be.normal_operator(psi, U, PARAMS)
    Qphi = be.normal_operator(phi, U, PARAMS)
    err = abs(complex(be.complex_dot(phi, Qpsi)) - complex(be.complex_dot(Qphi, psi)))
    assert err < TOL["Q_hermitian_abs"]


def _existing_golden_paths():
    if not (GOLDEN_ROOT / "MANIFEST.json").exists():
        return []
    manifest = json.loads((GOLDEN_ROOT / "MANIFEST.json").read_text())
    out = []
    for s in manifest["suites"]:
        p = GOLDEN_ROOT / s["path"]
        if p.exists():
            out.append(p)
    return out


@pytest.mark.parametrize("path", _existing_golden_paths() or [None], ids=lambda p: str(p) if p else "no-committed-goldens")
def test_replay_committed_golden_if_present(path):
    if path is None:
        pytest.skip("Run scripts/generate_goldens.py and commit goldens/ for full replay gates")
    data = json.loads(path.read_text())
    assert data["abi"] == "wilson_dirac_v1"
    L = data["L"]
    p = data["params"]
    params = WilsonParams(
        mass=p["mass"],
        wilson_r=p["wilson_r"],
        color_dim=p["color_dim"],
        spinor_dim=p["spinor_dim"],
    )
    be = TorchReferenceBackend(LatticeGeometry(L=L, n_dims=p["n_dims"]), PrecisionPolicy())
    psi = _unpack(data["inputs"]["psi"])
    U = _unpack(data["inputs"]["U"])
    assert _rel_err(be.wilson_dirac(psi, U, params), _unpack(data["outputs"]["Dpsi"])) < TOL["D_on_noise_rel"]
    assert data["metrics"]["g5_hermiticity_err"] < TOL["Ddag_identity_abs"]
    assert data["metrics"]["Q_hermiticity_err"] < TOL["Q_hermitian_abs"]
    traj = data["metrics"]["cg_residual_trajectory"]
    assert traj and traj[-1] <= traj[0] * 1.01 + 1e-12
