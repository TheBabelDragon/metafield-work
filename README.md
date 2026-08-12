# metafield-work

**MetaField defines the mathematics. Backends implement the operators.**

Wilson–Dirac is the **first frozen instruction** in the MetaField operator language —
not the whole language, and not a frozen hardware API.

```
MetaField Operator ABI family
│
├── Wilson–Dirac ABI v1     ← IMMUTABLE
├── Reduction ABI           ← later
├── Plaquette ABI           ← later
└── Gauge-force ABI         ← later
```

## Constitution

`tests/operator/goldens/` is the law.

| Suite | Content |
|-------|---------|
| L2/L4 × cold/random/boundary | **inputs + outputs** |
| checks | Dψ · γ₅-hermiticity · Q-hermiticity · Qψ · CG trajectory |

```bash
pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/operator -q
```

Regenerate goldens only when intentionally changing the oracle:

```bash
PYTHONPATH=. python scripts/generate_goldens.py
```

## Frozen vs experimental

**Frozen:** Wilson form, Degrand–DeTar γ, layouts, indexing, shifts, γ₅-hermiticity,
`Q=D†D`, precision semantics, golden corpus.

**Experimental:** `OperatorBackend` method names, DMA, device handles, sync, batching,
FPGA/ASIC transport.

See `docs/OPERATOR_LANGUAGE.md` and `docs/WILSON_DIRAC_ABI.md`.

## Progression

```
PyTorch oracle → golden corpus → (provisional software contract)
  → FPGA D_W → FPGA Q → CG → measure bottleneck
  → specialized datapath → only then ASIC candidates
```

`backends/fpga` and `backends/asic` stay empty until a boring implementation
passes the goldens. That is intentional.

## Layout

```
metafield/     pure math + algorithms
backends/      reference oracle · empty fpga/asic slots
tests/         operator + goldens (constitution)
scripts/       generate_goldens.py
docs/          ABI + field plan
```

Oracle lineage: [`TheBabelDragon/metafield`](https://github.com/TheBabelDragon/metafield)
`meta_field_sim_torch.py`.
