# Foundation lock — Wilson–Dirac ABI v1

```
                 MetaField
                    │
             mathematical layer
                    │
        ┌───────────┴───────────┐
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
        ↓           ↓           ↓
      Torch       FPGA        ASIC
      oracle    experiment   future
                    │
                    ↓
              Duck (adjacent)
         conjecture · experiment
         checker · attacker
```

## What is locked

- Mathematical meaning of Wilson–Dirac
- Golden corpus requirements (inputs **and** outputs)
- Seed table
- Tolerance gates
- PyTorch as oracle
- Duck does not own the verifier and cannot freeze a theorem

## What is deliberately ugly / replaceable

Everything under the operator ABI: DMA, PE layout, precision tricks, transport, `OperatorBackend` method names.
Everything inside a Duck body: which playground, which finite claim, which attack list.

## Permission

Hardware may be experimental, incomplete, and wrong **until** it passes the goldens.
Once it passes, MetaField does not care how.

A Duck claim may be experimental, incomplete, and wrong **until** the checker
recomputes it and the attacker fails to kill it. Once it is admitted, the
statement is still only as large as its named bound.

## Explicit non-goals until after first device pass

- ASIC selection
- HMC on device
- Clever backend APIs
- Treating Duck output as operator ABI
- Opening a “Millennium solved” file

**Implement `wilson_dirac` only. Pass L2. Profile. Then decide.**

Duck work, if any, happens *beside* that sentence, never instead of it.
