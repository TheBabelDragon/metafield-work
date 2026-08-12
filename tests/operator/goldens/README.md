# Golden corpus — constitution

**Wilson–Dirac ABI v1** is frozen. This directory is the compliance boundary.

## What is committed

| Artifact | Role |
|----------|------|
| `MANIFEST.json` | suite list + frozen seeds |
| `L2/*/golden.meta.json` | params, γ₅ / Q-hermiticity metrics, CG residual trajectories |
| (after `generate_goldens.py`) | `golden.npz` full complex128 inputs+outputs |

## Produce the full tensor tree

```bash
PYTHONPATH=. python scripts/generate_goldens.py
git add tests/operator/goldens
git commit -m "Wilson–Dirac v1 golden tensors (inputs+outputs)"
```

Seeds are immutable. Changing them is an ABI bump.

## Compliance

A backend passes iff, for every suite:

1. `Dψ` matches within `tolerances.json`
2. γ₅-hermiticity residual gate
3. `Q`-hermiticity residual gate
4. CG residual trajectory / final residual gate

Internal architecture (streamed stencil, systolic PE, SRAM tiling, mixed precision, …) is **irrelevant** to MetaField. Only the gates matter.

## Next move (do not expand architecture first)

```
wilson_dirac(ψ, U) → Dψ   on FPGA
L2 cold / random / boundary must pass
then L4
then profile → that profile designs the next hardware layer
```
