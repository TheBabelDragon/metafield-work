"""Constitution tests for Wilson–Dirac ABI v1.

- Meta gates always run when golden.meta.json is present.
- Tensor replay runs when golden.npz is present (after generate_goldens.py).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
import torch

from backends.reference.torch_backend import TorchReferenceBackend
from metafield.lattice.types import LatticeGeometry, PrecisionPolicy
from metafield.operators.protocol import WilsonParams

GOLDEN_ROOT = Path(__file__).parent / "goldens"
TOL = json.loads((Path(__file__).parent / "tolerances.json").read_text())["complex128"]


def _suite_dirs():
    man = GOLDEN_ROOT / "MANIFEST.json"
    if not man.exists():
        return []
    manifest = json.loads(man.read_text())
    return [
        GOLDEN_ROOT / s["path"]
        for s in manifest["suites"]
        if (GOLDEN_ROOT / s["path"] / "golden.meta.json").exists()
    ]


def _rel_err(got: torch.Tensor, exp: torch.Tensor) -> float:
    num = torch.linalg.vector_norm((got - exp).reshape(-1))
    den = torch.linalg.vector_norm(exp.reshape(-1)).clamp_min(1e-30)
    return float(num / den)


def _torch_c(a: np.ndarray) -> torch.Tensor:
    return torch.from_numpy(np.ascontiguousarray(a)).to(torch.complex128)


@pytest.mark.parametrize(
    "d",
    _suite_dirs() or [None],
    ids=lambda p: (f"{p.parent.name}/{p.name}" if p else "no-meta"),
)
def test_meta_g5_and_Q_gates(d):
    if d is None:
        pytest.skip("no golden.meta.json yet")
    meta = json.loads((d / "golden.meta.json").read_text())
    assert meta["abi"] == "wilson_dirac_v1"
    assert meta["metrics"]["g5_hermiticity_err"] < TOL["Ddag_identity_abs"]
    assert meta["metrics"]["Q_hermiticity_err"] < TOL["Q_hermitian_abs"]
    traj = meta["metrics"]["cg_residual_trajectory"]
    assert traj and meta["metrics"]["cg_final_resid"] is not None
    assert traj[-1] <= traj[0] * 1.01 + 1e-12


@pytest.mark.parametrize(
    "d",
    _suite_dirs() or [None],
    ids=lambda p: (f"{p.parent.name}/{p.name}" if p else "no-npz"),
)
def test_tensor_replay_if_npz_present(d):
    if d is None:
        pytest.skip("no suites")
    npz_path = d / "golden.npz"
    if not npz_path.exists():
        pytest.skip("run scripts/generate_goldens.py to materialize golden.npz")
    meta = json.loads((d / "golden.meta.json").read_text())
    npz = np.load(npz_path)
    p = meta["params"]
    params = WilsonParams(
        mass=p["mass"],
        wilson_r=p["wilson_r"],
        color_dim=p["color_dim"],
        spinor_dim=p["spinor_dim"],
    )
    be = TorchReferenceBackend(
        LatticeGeometry(L=meta["L"], n_dims=p["n_dims"]), PrecisionPolicy()
    )
    psi = _torch_c(npz["inputs__psi"])
    U = _torch_c(npz["inputs__U"])
    assert (
        _rel_err(be.wilson_dirac(psi, U, params), _torch_c(npz["outputs__Dpsi"]))
        < TOL["D_on_noise_rel"]
    )
    assert (
        _rel_err(
            be.wilson_dirac_dagger(psi, U, params), _torch_c(npz["outputs__Ddag_psi"])
        )
        < TOL["D_on_noise_rel"]
    )
    assert (
        _rel_err(be.normal_operator(psi, U, params), _torch_c(npz["outputs__Qpsi"]))
        < TOL["D_on_noise_rel"]
    )
