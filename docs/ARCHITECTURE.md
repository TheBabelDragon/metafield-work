# MetaField operator architecture (frozen plan)

## One principle

> **MetaField defines the mathematics; backends implement the operators.**

The Wilson–Dirac operator is the first stable plug-and-play contract.
FPGA and ASIC layers implement it. They do not redefine it.

---

## System diagram

```
                    ┌───────────────────────────┐
                    │       MetaField Model      │
                    │ Gauge · Fermion · HMC      │
                    │ Observables · BC           │
                    └─────────────┬─────────────┘
                                  │ Physics API
                    ┌─────────────▼─────────────┐
                    │     Operator Interface     │
                    │ D_W · D†D · Plaquette      │
                    │ Gauge force · Dot · Norm   │
                    └─────────────┬─────────────┘
                                  │ Backend dispatcher
              ┌───────────────────┼──────────────────┐
        ┌─────▼─────┐       ┌─────▼─────┐      ┌─────▼─────┐
        │ PyTorch   │       │ FPGA      │      │ ASIC      │
        │ Reference │       │ Backend   │      │ Backend   │
        └───────────┘       └───────────┘      └───────────┘
```

---

## Five layers

### Layer 0 — Representation (pure data)

- `GaugeField`
- `FermionField`
- `LatticeGeometry`
- `BoundaryCondition`
- `SimulationState`
- `PrecisionPolicy`

No CUDA / FPGA / ASIC assumptions. No PyTorch types leaking upward into the
contract (backends may use tensors internally).

### Layer 1 — Mathematical operators

These define **what MetaField means**:

| Operator | Meaning |
|----------|---------|
| `wilson_dirac(ψ, U)` | `D_W ψ` |
| `wilson_dirac_dagger(ψ, U)` | `D_W† ψ` (= γ₅ D γ₅ for Wilson) |
| `normal_operator(ψ, U)` | `D† D ψ` |
| `plaquette_action(U)` | Wilson gauge action |
| `gauge_force(U)` | su(N)-valued force |
| `complex_dot(a, b)` | Hermitian inner product |
| `complex_norm(a)` | √⟨a,a⟩ |
| `axpy` / `reduce` | linear algebra primitives |

### Layer 2 — Backend interface

```text
OperatorBackend
    wilson_dirac(...)
    wilson_dirac_dagger(...)
    normal_operator(...)
    plaquette(...)
    gauge_force(...)
    dot(...)
    norm(...)
    synchronize(...)
```

Implementations: `TorchBackend` (oracle), `CudaBackend`, `FPGADeviceBackend`,
`ASICBackend`.

### Layer 3 — Algorithms

CG, HMC, leapfrog, observables, calibration consume **operators**, not
implementations. CG only sees `A(x)`.

### Layer 4 — Orchestration

Device placement, batching, DMA, PCIe, CAN, multi-card, physical MetaField
nodes. Physics stays clean above this layer.

---

## Hardware exposes atoms, not physics

**Do expose**

`WILSON_DIRAC` · `PLAQUETTE` · `GAUGE_FORCE` · `DOT` · `NORM` · `AXPY` · `REDUCE`

**Do not expose (initially)**

`RUN_HMC()`

The host composes trajectories. Silicon only understands the operator vocabulary.
That is what makes repurposed accelerators viable.

---

## Precision policy

Do not hard-code `complex128` into the ABI.

```text
PrecisionPolicy
    storage_precision
    compute_precision
    accumulation_precision
```

Reference defaults: all complex128. Hardware may use complex64 / mixed /
fixed-point storage with higher-precision residual accumulation for CG.

---

## Milestone order

1. Freeze Wilson–Dirac ABI + golden vectors
2. Backend implements `D_W ψ` only
3. CG on `D†D` matches reference trajectory residuals
4. Plaquette + gauge force
5. Host-orchestrated HMC using accelerated operators
6. Optional: push more of the leapfrog onto device

CG is the first serious accelerator benchmark — not full HMC.

---

## Conceptual accelerator datapath (non-frozen)

```
Lattice memory → neighborhood gather → gauge transport (Uμ ψ)
  → spin/color arithmetic → Wilson stencil → reduce/store
```

Memory movement is first-class. Arithmetic alone is not the bottleneck.

---

## Plug-and-play target UX

```python
mf = MetaField(...)
mf.backend = "reference"
r0 = mf.solve(...)
mf.backend = "fpga"
r1 = mf.solve(...)
# same physics code; different executor
```

Silicon is replaceable. FPGA is replaceable. The MetaField operator language is not.
