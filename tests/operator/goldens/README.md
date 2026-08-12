# Golden corpus (constitution)

**Wilson–Dirac ABI v1** inputs **and** outputs live here after generation.

```bash
PYTHONPATH=. python scripts/generate_goldens.py
```

Produces:

```
L2/{cold,random,boundary}/golden.json
L4/{cold,random,boundary}/golden.json
MANIFEST.json
```

Each file stores ψ, U, η, φ **and** Dψ, D†ψ, Qψ, CG trajectory metrics.

Frozen seeds (do not change without ABI bump):

| L | kind | seed |
|---|------|------|
| 2 | cold | 1001 |
| 2 | random | 1002 |
| 2 | boundary | 1003 |
| 4 | cold | 2001 |
| 4 | random | 2002 |
| 4 | boundary | 2003 |

Commit the generated tree before a non-reference backend claims compliance.
