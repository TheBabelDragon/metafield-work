"""Layer 1–2 — mathematical operators + *provisional* backend surface.

Frozen mathematical ABIs (docs/):
  Wilson–Dirac v1, Reduction v1, Plaquette v1, Gauge-force v1.

This Protocol is EXPERIMENTAL software glue — method names, handles, and
sync semantics may change as the first FPGA implementation teaches us
what the operators actually want from hardware.

Physics should depend on the mathematical meaning and the golden corpora,
not on this surface being eternal.
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


@dataclass(frozen=True)
class GaugeParams:
    beta: float = 5.5
    color_dim: int = 3


@runtime_checkable
class OperatorBackend(Protocol):
    """Provisional executor surface. Not a frozen hardware ABI.

    Implement enough to pass tests/operator/goldens/. Prefer matching
    the oracle on wilson_dirac first; reductions, plaquettes, and the
    gauge force have their own frozen goldens.
    """

    name: str

    def wilson_dirac(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        """Return D_W ψ. Layout: ψ[x, spin, color], U[x, μ, color, color]."""
        ...

    def wilson_dirac_dagger(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        """Return D_W† ψ. Oracle uses γ5 D γ5."""
        ...

    def normal_operator(self, psi: Any, U: Any, params: WilsonParams) -> Any:
        """Return (D† D) ψ."""
        ...

    def plaquette_action(self, U: Any, beta: float) -> Any:
        """Scalar Wilson gauge action S_G (Plaquette ABI v1)."""
        ...

    def mean_plaquette(self, U: Any) -> Any:
        """Mean ReTr(P)/N over sites and planes (Plaquette ABI v1)."""
        ...

    def gauge_force(self, U: Any, beta: float) -> Any:
        """Left-trivialized su(N) force of S_G (Gauge-force ABI v1)."""
        ...

    def complex_dot(self, a: Any, b: Any) -> Any:
        """Hermitian inner product ⟨a,b⟩ = Σ conj(a)·b (Reduction ABI v1)."""
        ...

    def complex_norm(self, a: Any) -> Any:
        """‖a‖ = √⟨a,a⟩ as a real scalar (Reduction ABI v1)."""
        ...

    def axpy(self, alpha: Any, x: Any, y: Any) -> Any:
        """Return α x + y (Reduction ABI v1)."""
        ...

    def synchronize(self) -> None:
        """Device barrier (no-op on CPU). Mechanism is experimental."""
        ...


@dataclass
class OperatorContext:
    geometry: LatticeGeometry
    boundary: BoundaryCondition
    precision: PrecisionPolicy
    backend: OperatorBackend
