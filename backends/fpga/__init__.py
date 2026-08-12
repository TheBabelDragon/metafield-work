"""FPGA backend placeholder — implement OperatorBackend against the ABI."""


class FPGABackend:
    name = "fpga"

    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "FPGABackend is a slot for Zynq/Arty operators. "
            "Implement wilson_dirac first; see docs/FIELD_PLAN.md Phase C."
        )
