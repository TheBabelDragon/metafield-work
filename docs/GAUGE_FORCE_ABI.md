# Gauge-force ABI v1 — IMMUTABLE

**Status: FROZEN.**
Changes require a new ABI version (`v2`), new goldens, and an explicit migration note.

This is the su(N)-valued force of the Wilson gauge action in
`docs/PLAQUETTE_ABI.md`. Silicon should implement staples. The PyTorch
oracle may use staples or autograd; both must match the goldens.

Canonical oracle: `backends/reference/torch_backend.py`
Constitutional tests: `tests/operator/goldens/gauge_force_v1/` + `tests/operator/test_gauge_force_abi.py`.

---

## Operator

Staple sum at link `(x, μ)`:

```text
V_μ(x) = Σ_{ν ≠ μ} [
            U_ν(x+μ)   U_μ(x+ν)†   U_ν(x)†
          + U_ν(x−ν+μ)† U_μ(x−ν)†  U_ν(x−ν)
        ]
```

Left-trivialized, traceless anti-Hermitian force (frozen):

```text
W_μ(x)     = U_μ(x) V_μ(x)
A_μ(x)     = (1/2) ( W_μ(x) − W_μ(x)† )
F_μ(x)     = − (β / N)  [ A_μ(x) − (Tr A_μ(x) / N) I ]
```

`F` has the same layout as `U`: `F[x, μ, a, b]`.

| Symbol | Meaning | Freeze |
|--------|---------|--------|
| `β` | same coupling as Plaquette ABI | default **5.5** |
| `N` | color dim | default **3** |
| projection | traceless anti-Hermitian | above formula |

This is the derivative of

```text
S_G = β Σ_{x, μ<ν} (1 − Re Tr P_{μν} / N)
```

under left multiplication `U → e^{ω} U` with `ω ∈ su(N)`.
Sign is part of the ABI: HMC that integrates `p-dot = −F` with the opposite
sign will heat instead of sample.

**Identities (frozen):**

```text
F† = −F                         (anti-Hermitian)
Tr F = 0                        (traceless)
unit gauge  ⇒  F = 0
```

---

## Input / output contract

```text
IN:
  U                 GaugeField
  LatticeGeometry
  beta
  PrecisionPolicy

OUT:
  F                 same layout as U, values in su(N)
```

---

## Frozen conventions

- Same `U` layout, `shift`, and periodic BC as Wilson–Dirac / Plaquette v1.
- Both forward and backward staples are required. Dropping the backward
  staple is a different (wrong) action.
- Projection happens **after** forming `U V`, not on `V` alone.

---

## Golden suite requirements

| Check | What |
|-------|------|
| `F` | relative error vs oracle |
| anti-Hermitian residual | `‖F + F†‖ / ‖F‖` (or abs on cold) |
| traceless residual | `‖Tr F‖` |
| unit-gauge zero force | cold configs |
| cold / random | L=2 and L=4, same seeds as Wilson goldens |

---

## Explicitly not frozen here

- How the staple is scheduled (gather vs streaming)
- Autograd vs explicit staples (must agree with goldens)
- Fermion force / pseudofermion force → later operator
- Right-trivialized vs left-trivialized variants — v1 is **left**
