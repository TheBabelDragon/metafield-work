# Duck — hypothesis machine above the ABI

The Duck is not an LLM bolted onto the lattice. It is a bounded scientific
organism. It never mutates the substrate. It never redefines Wilson–Dirac.
It only proposes claims, and only memory of claims that survive attack.

```
                    DUCK
                      │
             mathematical world
                      │
       ┌───────────────┼───────────────┐
       ↓              ↓              ↓
   experiment      conjecture      proof
       │              │              │
       └───────────────┼───────────────┘
                      ↓
                 adversarial
                   verifier
                      │
                ┌─────┼─────┐
                ↓           ↓
              FAIL        SURVIVE
                │           │
                └─────→ MEMORY
                           │
                           ↓
                     next hypothesis
```

## Relation to the operator ABI

```
                 METAFIELD
                     │
       ┌────────────┼──────────────┐
       ↓             ↓              ↓
    Operators     Observer       Memory
    (frozen)      (Duck)         (episodes)
       │             │              │
       └────────────┼──────────────┘
                     ↓
              candidate claim
                     ↓
                 VERIFIER
             checker + attacker
                     │
             ┌──────┼───────┐
             ↓               ↓
           reject           admit
```

Layer 0–4 in [`ARCHITECTURE.md`](ARCHITECTURE.md) do not change.
The Duck is adjacent to Layer 4. It may *request* an operator application
the same way CG does: by calling a backend through the frozen contract.
It may not ship a new `D_W`.

## Loop

```
OBSERVE → REPRESENT → CONJECTURE → EXPERIMENT
       → DRAFT PROOF OBJECT → CHECKER RECOMPUTES
       → ATTACKER TRIES TO KILL IT
       → ADMIT | REJECT
       → UPDATE MEMORY
```

Reward is survival under attack, not how pretty the writeup looks.

## Constitution

Duck cannot:

- mutate state outside a declared delta / claim object
- modify history
- modify its own verifier
- bypass conservation or golden checks
- introduce NaNs into a field body
- violate boundary conditions
- retroactively alter a committed tick
- declare a theorem without a survived verdict
- hide a landed attack
- treat numerical evidence as existence of a proof

Duck may:

- observe a body
- form a conjecture
- construct a finite experiment
- search for an invariant
- draft a proof object
- request verification and attack
- retain only survived claims

## Mathematical bodies

Each prize problem (and Collatz, which is a gym, not a Clay problem)
gets its own executable body. The hunt is the open question. A surviving
claim is always smaller than the hunt.

| Body | Playground | What a surviving claim is allowed to be |
|------|------------|------------------------------------------|
| Riemann | zeros of a windowed Hardy Z / η | sign changes / no small off-line |η| in a named box |
| Yang–Mills | gauge configurations; later this repo’s Wilson operators | finite correlator / gap *proxy* on a named lattice |
| Navier–Stokes | velocity / vorticity field | regularity or blow-up on a named IC and horizon |
| P vs NP | Boolean circuits / SAT batches | a named solver decides a named batch |
| Birch–Swinnerton-Dyer | elliptic curves + truncated L | search-rank matches a named curve and height |
| Hodge | varieties / cohomology of Pⁿ | Hodge numbers / NS rank of a named space |
| Collatz | integer transition graph | termination / no foreign cycle up to a named N |

Unbounded statements (“RH is true”, “4D YM has a mass gap”, “every smooth
3D NS field stays smooth”) die at the experiment gate. That is the point.

Yang–Mills is the body that should eventually consume *this* repository:
plaquette, Wilson–Dirac, correlators, goldens. Until a device profile
exists, the YM body is allowed to be a tiny lattice gym. It is not
allowed to pretend it froze a new operator.

## Verifier

Two vetoes, neither owned by the Duck.

1. **Independent checker.** Every proof step names a rule in the body’s
   table. The body recomputes the step. Unknown rules fail. Missing
   premises fail. Unreproducible evidence fails.
2. **Adversarial attacker.** At least three attacks. A different lattice,
   a larger N, a denser grid, a planted counterexample. One hit kills
   the claim. Changing the theorem and calling it a refutation is not
   a hit — scope is part of the claim.

Final step if anything ever looks like a theorem:

```
Duck produces proof
    → independent checker verifies every step
    → separate system tries to falsify it
    → only then does MetaField admit the result
```

## Memory

Do not store `prompt → answer`.

Store:

```
Observation → Hypothesis → Candidate Δ / claim
           → Invariant / checker results
           → Attacks
           → Outcome
           → Fitness
```

That library *is* the policy. A flock of Ducks can share a field and keep
private memories; scored outcomes decide what is copied forward.

## What this is not

- Not a solver for the Millennium problems.
- Not permission to expand the Wilson–Dirac ABI.
- Not an excuse to skip goldens.
- Not “MetaField + LLM = Duck.”

The engine becomes a scientific environment. Duck-like behavior is the
consequence of: observe, hypothesize, perturb, measure, reject, remember,
try again — inside a world where mathematics is executable and every
claimed discovery has to survive reality.
