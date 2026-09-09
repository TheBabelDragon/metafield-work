# Backend equivalence

Every non-reference backend must pass the **same frozen operators** as the
PyTorch oracle. The protocol surface may change; the goldens may not.

1. Load the seed-locked inputs under `tests/operator/goldens/`.
2. Run the operator family the backend claims:
   - `wilson_dirac` / `wilson_dirac_dagger` / `normal_operator` / CG
   - `complex_dot` / `complex_norm` / `axpy`
   - `plaquette_action` / `mean_plaquette`
   - `gauge_force`
3. Compare against `TorchReferenceBackend` within `tests/operator/tolerances.json`.

Wilson–Dirac is the first device target. Reductions, plaquettes, and the
gauge force are already frozen math — implement them after `D_W` passes L2.

Until FPGA/ASIC land, this directory holds the policy only.
