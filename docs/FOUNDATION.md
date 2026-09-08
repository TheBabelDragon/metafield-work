# Foundation lock — operator ABI family v1

```
                 MetaField
                    │
             mathematical layer
                    │
        ┌───────────▼───────────┐
        │ Operator ABI family   │
        │                       │
        │ Wilson–Dirac v1  🔒   │
        │ Reduction v1     🔒   │
        │ Plaquette v1     🔒   │
        │ Gauge force v1   🔒   │
        └───────────┬───────────┘
                    │
             provisional glue
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
      Torch       FPGA        ASIC
      oracle    experiment   future
```

## What is locked

- Mathematical meaning of Wilson–Dirac, reductions, Wilson plaquette, gauge force
- Golden corpus requirements (inputs **and** outputs)
- Seed table (shared across the family)
- Tolerance gates
- PyTorch as oracle

## What is deliberately ugly / replaceable

Everything under the operator ABI: DMA, PE layout, precision tricks, transport, `OperatorBackend` method names.

## Permission

Hardware may be experimental, incomplete, and wrong **until** it passes the goldens.
Once it passes, MetaField does not care how.

## Explicit non-goals until after first device pass

- ASIC selection
- HMC on device
- Clever backend APIs
- Clover / Symanzik / fermion force ABIs

**Implement the frozen operators. Pass L2. Profile. Then decide.**
