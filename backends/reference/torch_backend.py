"""PyTorch reference backend — permanent correctness oracle.

Conventions locked to TheBabelDragon/metafield meta_field_sim_torch.py:
  - Euclidean Degrand–DeTar gamma matrices
  - D† = γ5 D γ5
  - ψ layout: lattice + (spin, color)
  - U layout: lattice + (μ, color, color)
  - shift(f, μ, +1)(x) = f(x+e_μ)

Gauge operators follow Plaquette ABI v1 and Gauge-force ABI v1:
  S_G = β Σ_{μ<ν} (1 − ReTr P / N)
  F   = −(β/N) proj_su(N)(U V)   with V the staple sum
"""

from __future__ import annotations

from typing import Any

import torch

from metafield.lattice.types import LatticeGeometry, PrecisionPolicy
from metafield.operators.protocol import WilsonParams


def _dtype(policy: PrecisionPolicy) -> torch.dtype:
    if policy.storage == "complex64":
        return torch.complex64
    return torch.complex128


def euclidean_gamma_matrices(dtype: torch.dtype, device: torch.device) -> torch.Tensor:
    i = 1j
    g1 = torch.tensor(
        [[0, 0, 0, -i], [0, 0, -i, 0], [0, i, 0, 0], [i, 0, 0, 0]], dtype=dtype, device=device
    )
    g2 = torch.tensor(
        [[0, 0, 0, -1], [0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0]], dtype=dtype, device=device
    )
    g3 = torch.tensor(
        [[0, 0, -i, 0], [0, 0, 0, i], [i, 0, 0, 0], [0, -i, 0, 0]], dtype=dtype, device=device
    )
    g4 = torch.tensor(
        [[0, 0, 1, 0], [0, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0]], dtype=dtype, device=device
    )
    return torch.stack([g1, g2, g3, g4], dim=0)


def gamma5(gammas: torch.Tensor) -> torch.Tensor:
    return gammas[0] @ gammas[1] @ gammas[2] @ gammas[3]


def dagger(M: torch.Tensor) -> torch.Tensor:
    return M.conj().transpose(-1, -2)


def project_sun_algebra(M: torch.Tensor) -> torch.Tensor:
    """Traceless anti-Hermitian projection (su(N) algebra element)."""
    n = M.shape[-1]
    A = 0.5 * (M - dagger(M))
    tr = torch.diagonal(A, dim1=-2, dim2=-1).sum(-1)
    eye = torch.eye(n, dtype=M.dtype, device=M.device)
    return A - (tr / n)[..., None, None] * eye


class TorchReferenceBackend:
    name = "reference"

    def __init__(
        self,
        geometry: LatticeGeometry,
        precision: PrecisionPolicy | None = None,
        device: str = "cpu",
    ) -> None:
        self.geometry = geometry
        self.precision = precision or PrecisionPolicy()
        self.device = torch.device(device)
        self.dtype = _dtype(self.precision)
        self.gammas = euclidean_gamma_matrices(self.dtype, self.device)
        self.g5 = gamma5(self.gammas)
        eye4 = torch.eye(4, dtype=self.dtype, device=self.device)
        self._eye4 = eye4

    def _shift(self, field: torch.Tensor, axis: int, direction: int) -> torch.Tensor:
        return torch.roll(field, shifts=-direction, dims=axis)

    def wilson_dirac(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        psi_t = torch.as_tensor(psi, dtype=self.dtype, device=self.device)
        U_t = torch.as_tensor(U, dtype=self.dtype, device=self.device)
        n_dims = self.geometry.n_dims
        r = float(params.wilson_r)
        out = (float(params.mass) + n_dims * r) * psi_t
        for mu in range(n_dims):
            g = self.gammas[mu]
            r_minus = r * self._eye4 - g
            r_plus = r * self._eye4 + g
            U_mu = U_t[..., mu, :, :]
            U_mu_back = self._shift(U_mu, mu, -1)
            psi_fwd = self._shift(psi_t, mu, +1)
            psi_back = self._shift(psi_t, mu, -1)
            transported_fwd = torch.einsum("...ij,...sj->...si", U_mu, psi_fwd)
            transported_back = torch.einsum("...ij,...sj->...si", dagger(U_mu_back), psi_back)
            term_fwd = torch.einsum("st,...ti->...si", r_minus, transported_fwd)
            term_back = torch.einsum("st,...ti->...si", r_plus, transported_back)
            out = out - 0.5 * (term_fwd + term_back)
        return out

    def wilson_dirac_dagger(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        psi_t = torch.as_tensor(psi, dtype=self.dtype, device=self.device)
        g5psi = torch.einsum("st,...ti->...si", self.g5, psi_t)
        Dg5psi = self.wilson_dirac(g5psi, U, params)
        return torch.einsum("st,...ti->...si", self.g5, Dg5psi)

    def normal_operator(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        return self.wilson_dirac_dagger(self.wilson_dirac(psi, U, params), U, params)

    def _plaquettes(self, U: Any) -> torch.Tensor:
        """ReTr(P)/N for every site and every μ<ν plane. Shape: lattice + (n_planes,)."""
        U_t = torch.as_tensor(U, dtype=self.dtype, device=self.device)
        n = U_t.shape[-1]
        traces = []
        for mu in range(self.geometry.n_dims):
            for nu in range(mu + 1, self.geometry.n_dims):
                U_mu = U_t[..., mu, :, :]
                U_nu = U_t[..., nu, :, :]
                U_nu_xpm = self._shift(U_nu, mu, +1)
                U_mu_xpn = self._shift(U_mu, nu, +1)
                plaq = U_mu @ U_nu_xpm @ dagger(U_mu_xpn) @ dagger(U_nu)
                tr = torch.diagonal(plaq, dim1=-2, dim2=-1).sum(-1).real / n
                traces.append(tr)
        return torch.stack(traces, dim=-1)

    def plaquette_action(self, U: Any, beta: float) -> Any:
        stacked = self._plaquettes(U)
        return float(beta) * torch.sum(1.0 - stacked)

    def mean_plaquette(self, U: Any) -> Any:
        stacked = self._plaquettes(U)
        return torch.mean(stacked)

    def staples(self, U: Any) -> torch.Tensor:
        """V_μ(x) staple sum. Same layout as U."""
        U_t = torch.as_tensor(U, dtype=self.dtype, device=self.device)
        n_dims = self.geometry.n_dims
        V = torch.zeros_like(U_t)
        for mu in range(n_dims):
            U_mu = U_t[..., mu, :, :]
            acc = torch.zeros_like(U_mu)
            for nu in range(n_dims):
                if nu == mu:
                    continue
                U_nu = U_t[..., nu, :, :]
                U_nu_xpm = self._shift(U_nu, mu, +1)
                U_mu_xpn = self._shift(U_mu, nu, +1)
                fwd = U_nu_xpm @ dagger(U_mu_xpn) @ dagger(U_nu)
                U_nu_xmn = self._shift(U_nu, nu, -1)
                U_mu_xmn = self._shift(U_mu, nu, -1)
                U_nu_xmn_xpm = self._shift(U_nu_xmn, mu, +1)
                back = dagger(U_nu_xmn_xpm) @ dagger(U_mu_xmn) @ U_nu_xmn
                acc = acc + fwd + back
            V[..., mu, :, :] = acc
        return V

    def gauge_force(self, U: Any, beta: float) -> Any:
        U_t = torch.as_tensor(U, dtype=self.dtype, device=self.device)
        n = U_t.shape[-1]
        V = self.staples(U_t)
        return -(float(beta) / n) * project_sun_algebra(U_t @ V)

    def gauge_force_autograd(self, U: Any, beta: float) -> Any:
        """Oracle cross-check only. Not part of the hardware ABI."""
        U_t = torch.as_tensor(U, dtype=self.dtype, device=self.device).detach().clone().requires_grad_(True)
        S = self.plaquette_action(U_t, beta)
        (grad,) = torch.autograd.grad(S, U_t)
        raw = U_t.detach() @ dagger(grad.detach())
        return project_sun_algebra(raw)

    def complex_dot(self, a: Any, b: Any) -> Any:
        a_t = torch.as_tensor(a, dtype=self.dtype, device=self.device)
        b_t = torch.as_tensor(b, dtype=self.dtype, device=self.device)
        return torch.sum(a_t.conj() * b_t)

    def complex_norm(self, a: Any) -> Any:
        d = self.complex_dot(a, a)
        return torch.sqrt(d.real.clamp_min(0.0))

    def axpy(self, alpha: Any, x: Any, y: Any) -> Any:
        x_t = torch.as_tensor(x, dtype=self.dtype, device=self.device)
        y_t = torch.as_tensor(y, dtype=self.dtype, device=self.device)
        return complex(alpha) * x_t + y_t

    def synchronize(self) -> None:
        return

    def random_fermion(self, params: WilsonParams, generator: torch.Generator | None = None) -> torch.Tensor:
        shape = self.geometry.shape + (params.spinor_dim, params.color_dim)
        g = generator or torch.Generator().manual_seed(0)
        real = torch.randn(shape, generator=g, dtype=torch.float64, device=self.device)
        imag = torch.randn(shape, generator=g, dtype=torch.float64, device=self.device)
        return (real + 1j * imag).to(self.dtype)

    def unit_gauge(self, params: WilsonParams) -> torch.Tensor:
        shape = self.geometry.shape + (self.geometry.n_dims, params.color_dim, params.color_dim)
        eye = torch.eye(params.color_dim, dtype=self.dtype, device=self.device)
        return eye.expand(shape).clone()
