"""Layer 1–2 — mathematical operator contract + backend interface.

Physics and algorithms depend on this module only.
Backends implement OperatorBackend. They do not redefine Wilson–Dirac.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from metafield.lattice.types import BoundaryCondition, LatticeGeometry, PrecisionPolicy


@dataclass(frozen=True)
class WilsonParams:
    mass: float = 0.1
    wilson_r: float = 1.0
    color_dim: int = 3
    spinor_dim: int = 4


@runtime_checkable
class OperatorBackend(Protocol):
    """Plug-and-play executor. All methods are pure math operators."""

    name: str

    def wilson_dirac(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        """Return D_W ψ. Layout: ψ[x, spin, color], U[x, μ, color, color]."""
        ...

    def wilson_dirac_dagger(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        """Return D_W† ψ. Reference uses γ₅ D γ₅."""
        ...

    def normal_operator(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        """Return (D† D) ψ."""
        ...

    def plaquette_action(self, U: Any, beta: float) -> Any:
        """Scalar Wilson gauge action."""
        ...

    def gauge_force(self, U: Any, beta: float) -> Any:
        """su(N)-valued force from Wilson action."""
        ...

    def complex_dot(self, a: Any, b: Any) -> Any:
        """Hermitian inner product ⟨a,b⟩ = Σ conj(a)·b (complex scalar)."""
        ...

    def complex_norm(self, a: Any) -> Any:
        """‖a‖ = √⟨a,a⟩ as a real scalar."""
        ...

    def synchronize(self) -> None:
        """Device barrier (no-op on CPU)."""
        ...


@dataclass
class OperatorContext:
    """Geometry + precision shared by a simulation handle."""

    geometry: LatticeGeometry
    boundary: BoundaryCondition
    precision: PrecisionPolicy
    backend: OperatorBackend
