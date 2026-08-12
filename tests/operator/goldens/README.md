# Golden corpus — constitution of metafield-work

**Wilson–Dirac ABI v1** compliance boundary.

Each suite directory contains:

| File | Role |
|------|------|
| `golden.meta.json` | params, seeds, metrics (γ₅, Q-hermiticity, CG trajectory) |
| `golden.npz.b64` | base64 of compressed NPZ: inputs ψ,U,η,φ + outputs Dψ, D†ψ, Qψ, cg_x |

```bash
PYTHONPATH=. python scripts/generate_goldens.py   # regenerate from oracle
PYTHONPATH=. python -m pytest tests/operator -q
```

A backend is compliant iff it reproduces outputs within `tolerances.json` for all suites.

Internal FPGA architecture is irrelevant to MetaField.
