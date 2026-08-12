# MetaField operator language

MetaField has an **operator language**. Individual operators get their own ABIs.

```
MetaField Operator ABI family
│
├── Wilson–Dirac ABI v1       ← FIRST FROZEN (immutable)
│
├── Reduction ABI v1            (provisional)
│
├── Plaquette ABI v1            (later)
│
├── Gauge-force ABI v1          (later)
│
└── …
```

Wilson–Dirac is the first standardized instruction — not the whole language.
Plaquette and gauge force will freeze the same way when their golden corpora exist.

---

## Frozen vs experimental

### FROZEN (do not casual-change)

| Item |
|------|
| MetaField mathematical meaning of Wilson–Dirac |
| Wilson form, mass/r conventions |
| Degrand–DeTar Euclidean γ matrices |
| Field layouts `ψ[x,spin,color]`, `U[x,μ,a,b]` |
| Lattice indexing + shift semantics |
| Boundary semantics (periodic default) |
| Link orientation in hops |
| γ₅-hermiticity identity |
| `Q = D†D` as CG normal operator |
| Precision semantics (policy object; tolerances per policy) |
| **Golden-vector requirements** (inputs + outputs under `tests/operator/goldens/`) |

### EXPERIMENTAL (must not pretend to be ABI)

| Item |
|------|
| `OperatorBackend` method names / Protocol surface |
| Device handles |
| DMA API / memory ownership |
| Synchronization mechanism |
| Batching / streaming |
| FPGA transport |
| ASIC transport |

The Protocol in `metafield/operators/protocol.py` is a **software convenience**,
not a frozen hardware ABI. The golden corpus is the constitution.

---

## Constitution: golden corpus

```
tests/operator/goldens/
  MANIFEST.json
  L2/
    cold/golden.json
    random/golden.json
    boundary/golden.json
  L4/
    cold/golden.json
    random/golden.json
    boundary/golden.json
```

Each suite stores **inputs and outputs**:

1. `Dψ`
2. γ₅-hermiticity residual
3. `D†D` hermiticity residual
4. `Qψ`
5. CG residual trajectory + final residual
6. Pathological / boundary sanity configs

Regenerate only deliberately:

```bash
PYTHONPATH=. python scripts/generate_goldens.py
```

Hardware that cannot pass these gates is not yet a MetaField backend.

---

## Progression (locked)

```
PyTorch oracle
      ↓
golden corpus          ← constitution
      ↓
software backend contract (provisional)
      ↓
FPGA D_W
      ↓
FPGA Q = D†D
      ↓
CG
      ↓
measure bottleneck
      ↓
design specialized datapath
      ↓
then investigate ASIC candidates
```

Do not choose an ASIC until MetaField has told us which primitive is worth accelerating.

FPGA and ASIC package slots stay empty until a boring `wilson_dirac` implementation
exists that passes the goldens.
