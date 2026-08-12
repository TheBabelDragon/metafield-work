# Foundation lock — Wilson–Dirac ABI v1

```
                 MetaField
                    │
             mathematical layer
                    │
        ┌───────────▼───────────┐
        │ Operator ABI family   │
        │                       │
        │ Wilson–Dirac v1  🔒   │
        │ Reduction        …    │
        │ Plaquette        …    │
        │ Gauge force      …    │
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

- Mathematical meaning of Wilson–Dirac
- Golden corpus requirements (inputs **and** outputs)
- Seed table
- Tolerance gates
- PyTorch as oracle

## What is deliberately ugly / replaceable

Everything under the operator ABI: DMA, PE layout, precision tricks, transport, `OperatorBackend` method names.

## Permission

Hardware may be experimental, incomplete, and wrong **until** it passes the goldens.
Once it passes, MetaField does not care how.

## Explicit non-goals until after first device pass

- More architecture documents
- ASIC selection
- HMC on device
- Clever backend APIs

**Implement `wilson_dirac` only. Pass L2. Profile. Then decide.**
