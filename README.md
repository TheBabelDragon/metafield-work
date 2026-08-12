# metafield-work

**MetaField defines the mathematics. Backends implement the operators.**

Wilson–Dirac is the first frozen instruction in the MetaField operator language.

```
MetaField Operator ABI family
│
├── Wilson–Dirac ABI v1     🔒 IMMUTABLE
├── Reduction ABI             later
├── Plaquette ABI             later
└── Gauge-force ABI           later
```

See [`docs/FOUNDATION.md`](docs/FOUNDATION.md).

## Quick start

```bash
pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/operator -q
```

## Constitution

`tests/operator/goldens/` is the compliance boundary.

```bash
# regenerate full input/output tensors from the oracle (seed-locked)
PYTHONPATH=. python scripts/generate_goldens.py
# then: git add tests/operator/goldens && commit
```

| Check | Gate |
|-------|------|
| `Dψ` | relative error vs oracle |
| γ₅-hermiticity | residual |
| `Q = D†D` hermiticity | residual |
| CG trajectory | residual history |

## Frozen vs experimental

**Frozen:** Wilson math, layouts, γ matrices, seeds, golden requirements, PyTorch oracle.

**Experimental:** `OperatorBackend` surface, DMA, device handles, FPGA/ASIC transport.

## Next (and only next)

```
wilson_dirac(ψ, U) → Dψ on device
L2 cold → random → boundary → L4 → profile
```

No further architecture until that profile exists.

Oracle lineage: [TheBabelDragon/metafield](https://github.com/TheBabelDragon/metafield) `meta_field_sim_torch.py`.
