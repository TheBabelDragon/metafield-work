# Plaquette ABI v1 — IMMUTABLE

**Status: FROZEN.**
Changes require a new ABI version (`v2`), new goldens, and an explicit migration note.

This is the Wilson gauge action as MetaField means it. Backends may tile,
stream, or fuse traces. They may not change the summand.

Canonical oracle: `backends/reference/torch_backend.py`
Constitutional tests: `tests/operator/goldens/plaquette_v1/` + `tests/operator/test_plaquette_abi.py`.

---

## Operator

Oriented plaquette at site `x` in the `(μ, ν)` plane, `μ < ν`:

```text
P_{μν}(x) = U_μ(x)  U_ν(x+μ)  U_μ(x+ν)†  U_ν(x)†
```

Wilson gauge action (frozen normalization):

```text
S_G[U] = β  Σ_{x} Σ_{μ < ν}  ( 1 − Re Tr P_{μν}(x) / N )
```

Mean plaquette (observables, not the action):

```text
P̄ = (1 / (V · n_planes))  Σ_{x, μ<ν}  Re Tr P_{μν}(x) / N
```

where `n_planes = n_dims (n_dims − 1) / 2` and `V = L^{n_dims}`.

| Symbol | Meaning | Freeze |
|--------|---------|--------|
| `β` | inverse gauge coupling | parameter (oracle default **5.5**) |
| `N` | color dim = `U.shape[-1]` | default **3** |
| `n_dims` | spacetime dims | **4** |
| `U_μ(x)` | SU(N) link | `U[x, μ, a, b]` |
| BC | periodic | v1 default |

**Identities (frozen):**

```text
unit gauge  ⇒  P_{μν}(x) = I  ⇒  S_G = 0  and  P̄ = 1
S_G is real
S_G ≥ 0 for β ≥ 0 on SU(N) (up to rounding)
```

---

## Input / output contract

```text
IN:
  U                 GaugeField
  LatticeGeometry   L, n_dims, BC
  beta
  PrecisionPolicy

OUT:
  plaquette_action  real scalar S_G
  mean_plaquette    real scalar P̄   (optional helper; goldens store both)
```

Trace is over color only. The real part is taken *after* the trace.

---

## Frozen conventions

- Same lattice indexing and `shift` semantics as Wilson–Dirac ABI v1.
- Forward hop uses `U_μ(x)`; the closing links are daggers of the
  shifted partners above.
- Planes are unordered pairs `μ < ν`. Counting a plane twice is a
  compliance failure, not an "optimization."
- `β` multiplies the *sum*, not the mean.

---

## Golden suite requirements

| Check | What |
|-------|------|
| `S_G` | absolute/relative error vs oracle |
| `P̄` | absolute error vs oracle |
| unit-gauge zero action | `‖S_G‖` on cold configs |
| cold / random | L=2 and L=4, same seeds as Wilson goldens |

---

## Explicitly not frozen here

- Rectangle / clover / Symanzik improvements → later operators
- Spatially resolved plaquette field (v1 returns scalars)
- Gauge-force (see `docs/GAUGE_FORCE_ABI.md`)
