# Field plan — stop expanding, pass the goldens

## North star

```text
PyTorch lattice sim → Zynq/Arty accelerator → repurposed silicon → purpose-built ASIC
```

without rewriting the physics.

## What is locked now

1. **Wilson–Dirac ABI v1** — immutable mathematical contract  
2. **Golden corpus** — L2/L4 × cold/random/boundary with inputs *and* outputs  
3. **Operator language framing** — Wilson–Dirac is the first instruction, not the only one  
4. **Empty FPGA/ASIC slots** — no speculative hardware API  

## What is deliberately not locked

`OperatorBackend` surface · DMA · memory ownership · sync · batching · transport.

The first FPGA implementation answers: *what does Wilson–Dirac actually want from hardware?*  
That answer designs the accelerator interface — not the reverse.

## Phases

### A — Constitution (now)

- [x] Wilson–Dirac ABI v1 frozen
- [x] Golden corpus committed
- [x] Reference replay tests
- [x] Backend surface marked provisional

### B — First FPGA (next)

- [ ] Implement only `wilson_dirac` on device
- [ ] Pass L2 goldens, then L4
- [ ] No HMC, no clever API

### C — Q and CG

- [ ] `D†D` on device or host-composed
- [ ] CG residual trajectory within tolerance
- [ ] Measure bandwidth vs arithmetic bottleneck

### D — Host-composed HMC

Host remains conductor. Device is orchestra.

### E — ASIC only after measurement

Choose candidates from measured primitives, not speculation.

## Review rule

PRs that touch operator **math** must update ABI version + goldens together.  
PRs that only touch backend transport should not claim ABI changes.
