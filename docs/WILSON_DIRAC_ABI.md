# Wilson–Dirac operator ABI (hard freeze)

Treat this as a **mathematical ABI**. Backends that disagree on any frozen
convention produce a spectacularly convincing wrong simulation.

Canonical reference: `TheBabelDragon/metafield` → `meta_field_sim_torch.py`
(`WilsonDiracOperator`).

---

## Operator

```text
(D ψ)(x) = (m + n_dims · r) ψ(x)
         − (1/2) Σ_μ [
               (r I − γ_μ) U_μ(x)       ψ(x+μ)
             + (r I + γ_μ) U_μ(x−μ)†    ψ(x−μ)
           ]
```

| Symbol | Meaning | Default / freeze |
|--------|---------|------------------|
| `m` | bare mass | config (ref: 0.1) |
| `r` | Wilson parameter | **1.0** standard |
| `n_dims` | spacetime dims | **4** |
| `γ_μ` | Euclidean gamma | Degrand–DeTar (below) |
| `U_μ(x)` | SU(N) gauge link | shape `… × μ × N × N` |
| `ψ(x)` | spinor-color field | shape `… × spin × color` |

**Adjoint identity (frozen):**

```text
D† ψ = γ₅ D (γ₅ ψ)
```

**Normal operator for CG:**

```text
Q = D† D
```

---

## Input / output contract

```text
IN:
  ψ                 FermionField
  U                 GaugeField
  LatticeGeometry   L, n_dims, BC
  mass, wilson_r
  PrecisionPolicy

OUT:
  D_W ψ             same layout as ψ
```

---

## Frozen conventions

### Lattice indexing

- Axes `0 .. n_dims-1` correspond to μ = 0 .. n_dims−1.
- Sites are a dense hypercube of extent `L` per axis (rectangular later; not required for v1).
- `shift(f, μ, +1)(x) = f(x + e_μ)`
- `shift(f, μ, −1)(x) = f(x − e_μ)`
- Periodic BC default (other BC must be explicit in `BoundaryCondition`).

### Gauge links

- Layout: `U[x, μ, a, b]` with `a,b` color indices.
- `U_μ(x)` parallel-transports **from** `x+μ` **to** `x` in the forward hop
  (matches reference `einsum('...ij,...sj->...si', U_mu, psi_fwd)`).
- Backward hop uses `U_μ(x−μ)†`.

### Spin / color ordering

- Spinor dim = **4** (Euclidean Dirac).
- Color dim = **N** (default 3).
- Field layout: `ψ[x, spin, color]` — spin **before** color.

### Gamma matrices (Degrand–DeTar Euclidean)

Hermitian, `{γ_μ, γ_ν} = 2 δ_{μν} I`.

```
γ1 = [[0,0,0,-i],[0,0,-i,0],[0,i,0,0],[i,0,0,0]]
γ2 = [[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]
γ3 = [[0,0,-i,0],[0,0,0,i],[i,0,0,0],[0,-i,0,0]]
γ4 = [[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
γ5 = γ1 γ2 γ3 γ4
```

Direction order in the sum is μ = 0,1,2,3 ↔ γ1..γ4 as above.

### Complex representation

- Interleaved or planar is a **backend choice**.
- ABI tests compare against reference in a canonical planar form:
  `real/imag` separated only at the boundary if needed.
- Reference storage: native complex (`complex128` default).

### Precision semantics

- Equivalence tolerances are **explicit** per precision policy (see tests).
- Default reference: `complex128` throughout.
- Mixed-precision backends must still pass residual gates on `Q`-solves within
  published bounds.

### Reductions

```text
⟨a,b⟩ = Σ conj(a) · b     (Hermitian inner product, real part taken where required)
‖a‖   = √⟨a,a⟩
```

---

## Golden vectors

Every backend must reproduce reference outputs for fixed seeds:

| Suite | Content |
|-------|---------|
| `D_on_noise` | random ψ, cold/hot U → `Dψ` |
| `Ddag_identity` | `‖D†ψ − γ₅ D γ₅ ψ‖ < tol` |
| `Q_hermitian` | `⟨φ, Qψ⟩ ≈ ⟨Qφ, ψ⟩` |
| `CG_path` | fixed RHS, same `Q`, residual history |

Tolerance tables live under `tests/operator/tolerances.json`.

---

## Non-goals of this ABI

- RHMC / fractional powers
- Clover improvement
- Domain wall / overlap
- Multi-grid preconditioners

Those are later operators with their own contracts.
