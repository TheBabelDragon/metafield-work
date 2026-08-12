# Backend equivalence

Every non-reference backend must:

1. Load the same seed-locked golden inputs under `tests/operator/goldens/` (to be committed).
2. Run `wilson_dirac` / `normal_operator` / CG.
3. Compare against `TorchReferenceBackend` within `tests/operator/tolerances.json`.

Until FPGA/ASIC land, this directory holds the policy only.
