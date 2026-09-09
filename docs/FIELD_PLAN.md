# Field plan — stop expanding, pass the goldens

## North star

```text
PyTorch lattice sim → Zynq/Arty accelerator → repurposed silicon → purpose-built ASIC
```

without rewriting the physics.

A second, non-blocking north star lives in [`DUCK.md`](DUCK.md): the same
operator world can host a hypothesis machine. That track is not allowed to
move Wilson–Dirac, goldens, or device milestones.

## What is locked now

1. **Wilson–Dirac ABI v1** — immutable mathematical contract  
2. **Golden corpus** — L2/L4 × cold/random/boundary with inputs *and* outputs  
3. **Operator language framing** — Wilson–Dirac is the first instruction, not the only one  
4. **Empty FPGA/ASIC slots** — no speculative hardware API  
5. **Duck constitution** — claims die unless a checker and an attacker both fail to kill them  

## What is deliberately not locked

`OperatorBackend` surface · DMA · memory ownership · sync · batching · transport.
Duck bodies · Duck memory · which playground a Duck inhabits.

The first FPGA implementation answers: *what does Wilson–Dirac actually want from hardware?*  
That answer designs the accelerator interface — not the reverse.

## Phases

### A — Constitution (now)

- [x] Wilson–Dirac ABI v1 frozen
- [x] Golden corpus committed
- [x] Reference replay tests
- [x] Backend surface marked provisional
- [x] Duck documented as adjacent, non-ABI experimenter

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

### F — Duck (parallel, never blocking B–E)

- [x] Write the constitution: no self-certified theorems
- [ ] Point a YM body at *this* repo’s plaquette / Wilson operators
- [ ] Admit only finite, recomputed, attack-surviving claims
- [ ] Do not open a Millennium claim file

## Review rule

PRs that touch operator **math** must update ABI version + goldens together.  
PRs that only touch backend transport should not claim ABI changes.  
PRs that only touch Duck bodies should not claim operator progress.
