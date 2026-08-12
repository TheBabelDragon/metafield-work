# metafield-work

**MetaField defines the mathematics. Backends implement the operators.**

Work repo for isolating lattice operators (Wilson–Dirac first) so CPU / CUDA /
FPGA / ASIC can plug in without redefining the physics.

The existing PyTorch simulation in [`TheBabelDragon/metafield`](https://github.com/TheBabelDragon/metafield)
(`meta_field_sim_torch.py`) is the **reference oracle**. This repo hardens the
contract around it.

```
                  METAFIELD
                     │
              mathematical truth
                     │
             ┌───────▼───────┐
             │   OPERATORS   │
             │ Wilson–Dirac  │
             │ Plaquette     │
             │ Force         │
             │ Reduction     │
             └───────┬───────┘
                     │
              stable contract
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
      CPU          FPGA          ASIC
```

## Hard freezes

| # | Freeze |
|---|--------|
| 1 | Wilson–Dirac mathematical convention (see `docs/WILSON_DIRAC_ABI.md`) |
| 2 | Field memory / indexing semantics |
| 3 | Backend / operator separation — physics never imports silicon details |
| 4 | PyTorch reference backend as permanent correctness oracle |
| 5 | Operator-level hardware interface (not `RUN_HMC`) |
| 6 | Precision policy (storage / compute / accumulate) |
| 7 | Golden-vector equivalence tests for every backend |

## Keep experimental

FPGA microarchitecture · fixed vs float · ASIC candidate · PCIe/DMA · PE count ·
lattice size · distributed topology · CAN · custom silicon.

## Layout

```
metafield/          # pure math + algorithms (no device imports upward)
backends/           # reference · cuda · fpga · asic stubs
hardware/           # bitstreams, interfaces (later)
tests/              # operator · equivalence · numerical · regression
benchmarks/         # CG first, then HMC
docs/               # architecture + ABI
```

## Quick start

```bash
pip install torch   # reference backend
python -m pytest tests/operator -q
```

Point `METAFIELD_ORACLE` at a checkout of `TheBabelDragon/metafield` if you want
the live `WilsonDiracOperator` as the oracle (optional; a self-contained
reference is included).

## Milestones

1. **Operator ABI frozen** ← you are here
2. Golden vectors for `D_W ψ` on small lattices
3. CG against reference on same vectors
4. FPGA backend implements `wilson_dirac` only
5. Equivalence gates green
6. Host-composed HMC (still software orchestration)
