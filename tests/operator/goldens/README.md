# Golden corpus — constitution

This directory is the compliance boundary for the **operator ABI family**.

```
goldens/
├── MANIFEST.json              Wilson–Dirac suite list + frozen seeds
├── L2/ L4/                   Wilson–Dirac v1 meta (and optional npz)
├── reduction_v1/             Reduction ABI v1   (when committed)
├── plaquette_v1/             Plaquette ABI v1   (when committed)
└── gauge_force_v1/           Gauge-force ABI v1 (when committed)
```

Seeds are shared across the family. Changing them is an ABI bump for every
operator that uses them.

## What is committed today

| Artifact | Role |
|----------|------|
| `MANIFEST.json` | Wilson–Dirac suite list + frozen seeds |
| `L2/*/golden.meta.json` | params, γ₅ / Q-hermiticity metrics, CG trajectories |
| (after `generate_goldens.py`) | `golden.npz` full complex128 inputs+outputs |

Family trees (`reduction_v1/`, `plaquette_v1/`, `gauge_force_v1/`) use the
same L × kind table. Identity tests in `tests/operator/test_*_abi.py` do not
wait on those files. Tensor replay does.

## Produce Wilson–Dirac tensors

```bash
PYTHONPATH=. python scripts/generate_goldens.py
git add tests/operator/goldens
git commit -m "Wilson–Dirac v1 golden tensors (inputs+outputs)"
```

## Compliance

A backend claiming a frozen ABI passes iff, for every suite of that ABI:

**Wilson–Dirac v1**

1. `Dψ` matches within `tolerances.json`
2. γ₅-hermiticity residual gate
3. `Q`-hermiticity residual gate
4. CG residual trajectory / final residual gate

**Reduction v1** — `dot` conjugate symmetry, `norm` vs `sqrt(dot)`, `axpy` affine + oracle match

**Plaquette v1** — unit-gauge `S_G = 0`, `P̄ = 1`; action / mean match oracle

**Gauge-force v1** — `F† = −F`, `Tr F = 0`, unit-gauge `F = 0`; staple force matches oracle

Internal architecture (streamed stencil, systolic PE, SRAM tiling, mixed precision, …) is **irrelevant** to MetaField. Only the gates matter.

## Next move (do not expand architecture first)

```
wilson_dirac(ψ, U) → Dψ   on FPGA
L2 cold / random / boundary must pass
then L4
then profile → that profile designs the next hardware layer
```
