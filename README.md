# metafield-work

**MetaField defines the mathematics. Backends implement the operators.**

Wilson–Dirac was the first frozen instruction. Reduction, Plaquette, and
Gauge-force are now frozen the same way — later was right now.

```
MetaField Operator ABI family
│
├── Wilson–Dirac ABI v1     🔒 IMMUTABLE
├── Reduction ABI v1        🔒 IMMUTABLE
├── Plaquette ABI v1        🔒 IMMUTABLE
└── Gauge-force ABI v1      🔒 IMMUTABLE
```

See [`docs/FOUNDATION.md`](docs/FOUNDATION.md).

| ABI | Contract |
|-----|----------|
| [Wilson–Dirac](docs/WILSON_DIRAC_ABI.md) | `D_W ψ`, `D† = γ₅ D γ₅`, `Q = D†D` |
| [Reduction](docs/REDUCTION_ABI.md) | `⟨a,b⟩`, `‖a‖`, `axpy` |
| [Plaquette](docs/PLAQUETTE_ABI.md) | `S_G = β Σ (1 − ReTr P / N)` |
| [Gauge-force](docs/GAUGE_FORCE_ABI.md) | `F = −(β/N) proj_su(N)(U V)` |

## Quick start

```bash
pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/operator -q
```

## Constitution

`tests/operator/goldens/` is the compliance boundary.

```bash
# Wilson–Dirac tensors (existing)
PYTHONPATH=. python scripts/generate_goldens.py
# Reduction / Plaquette / Gauge-force tensors
PYTHONPATH=. python scripts/generate_family_goldens.py
# then: git add tests/operator/goldens && commit
```

| Check | Gate |
|-------|------|
| `Dψ` | relative error vs oracle |
| γ₅-hermiticity | residual |
| `Q = D†D` hermiticity | residual |
| CG trajectory | residual history |
| `⟨a,b⟩` / `‖a‖` / `axpy` | scalar / field error vs oracle |
| `S_G`, mean plaquette | absolute error vs oracle |
| gauge force `F` | su(N) identities + relative error |

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
