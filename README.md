# metafield-work

**MetaField defines the mathematics. Backends implement the operators.**

Wilson–Dirac was the first frozen instruction. Reduction, Plaquette, and
Gauge-force are frozen the same way.

```
MetaField Operator ABI family
│
├── Wilson–Dirac ABI v1     🔒 IMMUTABLE   docs/WILSON_DIRAC_ABI.md
├── Reduction ABI v1        🔒 IMMUTABLE   docs/REDUCTION_ABI.md
├── Plaquette ABI v1        🔒 IMMUTABLE   docs/PLAQUETTE_ABI.md
└── Gauge-force ABI v1      🔒 IMMUTABLE   docs/GAUGE_FORCE_ABI.md
```

Map: [`docs/FOUNDATION.md`](docs/FOUNDATION.md) · language: [`docs/OPERATOR_LANGUAGE.md`](docs/OPERATOR_LANGUAGE.md) · plan: [`docs/FIELD_PLAN.md`](docs/FIELD_PLAN.md)

| ABI | Contract | Tests |
|-----|----------|-------|
| Wilson–Dirac | `D_W ψ`, `D† = γ₅ D γ₅`, `Q = D†D` | `tests/operator/test_wilson_abi.py`, `test_goldens.py` |
| Reduction | `⟨a,b⟩`, `‖a‖`, `axpy` | `tests/operator/test_reduction_abi.py` |
| Plaquette | `S_G = β Σ (1 − ReTr P / N)` | `tests/operator/test_plaquette_abi.py` |
| Gauge-force | `F = −(β/N) proj_su(N)(U V)` | `tests/operator/test_gauge_force_abi.py` |

## Quick start

```bash
pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/operator -q
```

## Constitution

`tests/operator/goldens/` is the compliance boundary. See that folder's [README](tests/operator/goldens/README.md).

```bash
# Wilson–Dirac tensors (seed-locked)
PYTHONPATH=. python scripts/generate_goldens.py
git add tests/operator/goldens && git commit
```

Family goldens (Reduction / Plaquette / Gauge-force) reuse the same L2/L4 ×
cold/random/boundary seeds. Identity tests already run without those npz
files; tensor replay starts once the family corpora are committed under
`tests/operator/goldens/{reduction,plaquette,gauge_force}_v1/`.

| Check | Gate |
|-------|------|
| `Dψ` | relative error vs oracle |
| γ₅-hermiticity | residual |
| `Q = D†D` hermiticity | residual |
| CG trajectory | residual history |
| `⟨a,b⟩` / `‖a‖` / `axpy` | conjugate symmetry + oracle match |
| `S_G`, mean plaquette | unit-gauge zero action; oracle match |
| gauge force `F` | su(N) identities; staple ≡ autograd |

Tolerances: [`tests/operator/tolerances.json`](tests/operator/tolerances.json).

## Frozen vs experimental

**Frozen:** Wilson math, layouts, γ matrices, seeds, golden requirements,
PyTorch oracle, reduction identities, Wilson gauge action, left-trivialized
staple force.

**Experimental:** `OperatorBackend` surface, DMA, device handles, FPGA/ASIC transport.

## Next

FPGA implements the frozen vocabulary one instruction at a time:

```
wilson_dirac → complex_dot / axpy → plaquette_action → gauge_force
L2 cold → random → boundary → L4 → profile
```

Oracle lineage: [TheBabelDragon/metafield](https://github.com/TheBabelDragon/metafield) `meta_field_sim_torch.py`.
