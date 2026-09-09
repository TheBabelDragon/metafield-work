# metafield-work

**MetaField defines the mathematics. Backends implement the operators.**
**The Duck proposes hypotheses. The verifier admits results.**

Wilson–Dirac is the first frozen instruction in the MetaField operator language.
The Duck is not an instruction. It is a bounded experimenter that lives *beside*
the operator ABI and is forbidden to redefine it.

```
MetaField Operator ABI family
│
├── Wilson–Dirac ABI v1     🔒 IMMUTABLE
├── Reduction ABI             later
├── Plaquette ABI             later
└── Gauge-force ABI           later

Duck (experimental, above the ABI)
│
├── observe → conjecture → experiment
├── draft proof object
├── independent checker
└── adversarial attack → SURVIVE | DIE
```

See [`docs/FOUNDATION.md`](docs/FOUNDATION.md) and [`docs/DUCK.md`](docs/DUCK.md).

## Quick start

```bash
pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/operator -q
```

## Constitution

`tests/operator/goldens/` is the operator compliance boundary.

```bash
# regenerate full input/output tensors from the oracle (seed-locked)
PYTHONPATH=. python scripts/generate_goldens.py
# then: git add tests/operator/goldens && commit
```

| Check | Gate |
|-------|------|
| `Dψ` | relative error vs oracle |
| γ5-hermiticity | residual |
| `Q = D†D` hermiticity | residual |
| CG trajectory | residual history |

A Duck claim has a different gate. Beauty is not it.

| Check | Gate |
|-------|------|
| finite experiment | the statement has a bound the body can run |
| proof object | every step names a body rule |
| independent checker | the body recomputes every step |
| adversarial attack | at least three attacks; one hit kills the claim |

There is no status called “Duck says theorem proven.”
The only promotion is `ADMITTED`, and only after the checker and the attacker
both fail to kill the claim.

## Frozen vs experimental

**Frozen:** Wilson math, layouts, γ matrices, seeds, golden requirements, PyTorch oracle.

**Experimental:** `OperatorBackend` surface, DMA, device handles, FPGA/ASIC transport,
Duck bodies, Duck memory, Millennium playgrounds.

Duck code must not:

- edit Wilson–Dirac math
- edit goldens
- edit the verifier
- treat a numerical experiment as a Millennium proof
- claim success without a survived verdict

## Two tracks

### Track A — operator isolation (blocking)

```
wilson_dirac(ψ, U) → Dψ on device
L2 cold → random → boundary → L4 → profile
```

No further *operator* architecture until that profile exists.

### Track B — Duck experimenter (non-blocking)

Same creature, many mathematical bodies. Navier–Stokes is one gym.
Yang–Mills on this repo’s lattice operators is the gym that belongs here.
Unbounded prize statements die at the experiment gate on purpose.

```
observe → represent → conjecture → construct experiment
       → search for invariant → attempt proof
       → attack its own proof → retain only verified results
```

Details: [`docs/DUCK.md`](docs/DUCK.md).

Oracle lineage: [TheBabelDragon/metafield](https://github.com/TheBabelDragon/metafield) `meta_field_sim_torch.py`.
