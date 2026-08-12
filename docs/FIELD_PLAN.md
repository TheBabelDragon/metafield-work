# Field plan — ASIC / FPGA isolation path

## North star

Ship a path:

```text
PyTorch lattice sim  →  Zynq/Arty accelerator  →  repurposed silicon  →  purpose-built MetaField ASIC
```

without rewriting the physics at each step.

---

## Phase A — Contract (now)

- [x] Architecture freeze document
- [x] Wilson–Dirac ABI freeze
- [x] `OperatorBackend` protocol in-repo
- [x] Reference backend scaffold + equivalence test harness
- [ ] Golden vectors committed for L=2 and L=4 (seed-locked)

## Phase B — Software isolation

- [ ] Extract pure operator calls out of monolithic `meta_field_sim_torch.py`
      into `metafield/operators/*` (this repo) while metafield remains oracle
- [ ] CG only talks to `OperatorBackend.normal_operator`
- [ ] HMC force path uses `gauge_force` + fermion force via same interface

## Phase C — CG on device

First **hardware** milestone is not HMC.

1. Host sends ψ, U (or streams tiles)
2. Device returns `Dψ`
3. Host runs CG using device matvecs
4. Residuals match reference within tolerance

Exposes: throughput, bandwidth, complex arithmetic, reductions, stability, sync.

## Phase D — Host-composed HMC

```text
plaquette → gauge action → D_W → CG → force → leapfrog → Metropolis
```

Host remains conductor. Accelerator is the orchestra.

## Phase E — Optional device orchestration

Only after C+D are boringly correct: pack multi-matvec sequences, on-device
leapfrog fragments, multi-card domain decomposition.

---

## Repo boundary vs `metafield`

| Repo | Role |
|------|------|
| `metafield` | Living sim, physical bodies, FO schemas, Aurora mods |
| `metafield-work` | Operator isolation, ABI, backends, hardware benches |

Do not let FPGA code import FO / optical stubs. Do not let operator math import
bitstreams.

---

## Review checklist (every PR that touches operators)

1. Does this change the **math** or only an **implementation**?
2. If math: update ABI doc + golden vectors in the same PR.
3. Does any algorithm import a backend symbol? (reject)
4. New backend: passes `tests/backend_equivalence` against reference.
