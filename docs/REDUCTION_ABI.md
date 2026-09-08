# Reduction ABI v1 — IMMUTABLE

**Status: FROZEN.**
Changes require a new ABI version (`v2`), new goldens, and an explicit migration note.

These are the linear-algebra atoms CG (and later HMC) consume.
They are not "helpers." Hardware that cannot reduce correctly cannot claim
Wilson–Dirac compliance either — CG residuals live or die here.

Canonical oracle: `backends/reference/torch_backend.py`
Constitutional tests: `tests/operator/goldens/reduction_v1/` + `tests/operator/test_reduction_abi.py`.

---

## Operators

```text
⟨a, b⟩  = Σ_i  conj(a_i) · b_i          complex_dot
‖a‖     = √ max(Re ⟨a, a⟩, 0)           complex_norm
y ← α x + y                             axpy
```

Summation is over the entire flattened field (every lattice × spin × color
component for fermions; every lattice × μ × color × color component for
gauge objects when those are passed).

| Symbol | Meaning | Freeze |
|--------|---------|--------|
| `a`, `b`, `x`, `y` | same layout, same dtype policy | layout is the caller’s |
| `α` | complex scalar | full complex |
| accumulation | `PrecisionPolicy.accumulation` | default complex128 |

**Identities (frozen):**

```text
⟨a, b⟩ = conj(⟨b, a⟩)
⟨a, a⟩ is real and ≥ 0 (up to rounding)
‖λ a‖  = |λ| ‖a‖
axpy is affine: axpy(α, x, y) − y = α x
```

---

## Input / output contract

```text
IN (dot / norm):
  a, b            same-shaped fields
  PrecisionPolicy

OUT:
  complex_dot     0-d complex scalar
  complex_norm    0-d real scalar (non-negative)

IN (axpy):
  α               complex scalar
  x, y            same-shaped fields

OUT:
  α x + y         same layout as y
```

Order of summation is a backend choice. Goldens compare the *value*,
not the reduction tree.

---

## Explicitly not frozen here

- Warp / PE / tree-reduce topology
- Kahan vs pairwise vs block accumulation (must still pass tolerances)
- DMA of partial sums
- Fused `norm2` that skips the sqrt — the ABI still *returns* `√⟨a,a⟩`

---

## Golden suite requirements

| Check | What |
|-------|------|
| `dot` | relative error vs oracle scalar |
| conjugate symmetry | `‖⟨a,b⟩ − conj(⟨b,a⟩)‖` |
| `norm` | relative error vs oracle |
| `axpy` | relative error vs oracle field |
| cold / random / boundary | L=2 and L=4 fermion fields, Wilson seeds |
