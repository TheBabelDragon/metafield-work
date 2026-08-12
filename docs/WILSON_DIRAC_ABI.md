# Wilson–Dirac ABI v1 — IMMUTABLE

**Status: FROZEN.**  
Changes require a new ABI version (`v2`), new goldens, and an explicit migration note.
This is the first operator in the MetaField operator language — not the whole language.

Treat this as a **mathematical ABI**. Backends that disagree on any frozen
convention produce a spectacularly convincing wrong simulation.

Canonical oracle: `backends/reference/torch_backend.py`  
(aligned with `TheBabelDragon/metafield` → `meta_field_sim_torch.py`).

Constitutional tests: `tests/operator/goldens/` + `tests/operator/test_goldens.py`.

---

## Operator

```text
(D ψ)(x) = (m + n_dims · r) ψ(x)
         − (1/2) Σ_μ [
               (r I − γ_μ) U_μ(x)       ψ(x+μ)
             + (r I + γ_μ) U_μ(x−μ)†    ψ(x−μ)
           ]
```

| Symbol | Meaning | Freeze |
|--------|---------|--------|
| `m` | bare mass | parameter (oracle default 0.1) |
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

- Axes `0 .. n_dims-1` ↔ μ = 0 .. n_dims−1.
- Dense hypercube extent `L` per axis (v1).
- `shift(f, μ, +1)(x) = f(x + e_μ)`
- `shift(f, μ, −1)(x) = f(x − e_μ)`
- Periodic BC default.

### Gauge links

- Layout: `U[x, μ, a, b]` color indices last.
- Forward hop: `U_μ(x)` transports ψ(x+μ) → x.
- Backward hop: `U_μ(x−μ)†`.

### Spin / color

- Spinor dim = **4**.
- Color dim = **N** (default 3).
- Layout: `ψ[x, spin, color]` — spin **before** color.

### Gamma matrices (Degrand–DeTar Euclidean)

Hermitian, `{γ_μ, γ_ν} = 2 δ_{μν} I`.

```
γ1 = [[0,0,0,-i],[0,0,-i,0],[0,i,0,0],[i,0,0,0]]
γ2 = [[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]]
γ3 = [[0,0,-i,0],[0,0,0,i],[i,0,0,0],[0,-i,0,0]]
γ4 = [[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]]
γ5 = γ1 γ2 γ3 γ4
```

μ = 0..3 ↔ γ1..γ4 in that order.

### Complex representation

- Interleaved vs planar is a **backend choice** (experimental transport).
- Goldens compare in canonical complex planar form from the oracle.
- Default storage: complex128.

### Reductions

```text
⟨a,b⟩ = Σ conj(a) · b
‖a‖   = √⟨a,a⟩
```

---

## Golden suite requirements (constitution)

Every backend claiming Wilson–Dirac ABI v1 compliance must pass:

| Check | What |
|-------|------|
| `Dψ` | relative error vs oracle output |
| γ₅-hermiticity | `‖D†ψ − γ₅ D γ₅ ψ‖` |
| `D†D` hermiticity | `⟨φ,Qψ⟩ ≈ ⟨Qφ,ψ⟩` |
| `Qψ` | relative error vs oracle |
| CG trajectory | residual history on fixed RHS |
| cold / random / boundary | L=2 and L=4 suites |

Inputs **and** outputs are stored under `tests/operator/goldens/`.

---

## Explicitly not frozen here

- Backend method names (`OperatorBackend` is provisional software glue)
- DMA, device handles, streaming, batching
- FPGA/ASIC transport
- Plaquette / gauge-force (future ABIs in the same operator language)

---

## Non-goals of v1

RHMC · clover · domain wall / overlap · multi-grid preconditioners  
→ later operators, separate ABIs.
