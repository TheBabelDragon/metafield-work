"""Duck protocol — experimental, adjacent to the operator ABI.

The Duck may request operators the way CG does. It may not version them.
This module is a software convenience, not a frozen hardware ABI and not
a theorem prover.
"""

from __future__ import annotations

from typing import Any, Protocol


class DuckCannot:
    EDIT_WILSON_DIRAC = "edit Wilson–Dirac math"
    EDIT_GOLDENS = "edit operator goldens"
    EDIT_VERIFIER = "modify its own verifier"
    SELF_CERTIFY = "declare a theorem without a survived verdict"
    HIDE_ATTACK = "hide a landed attack"
    UNBOUNDED_CLAIM = "treat an unbounded prize statement as an experiment"


class MathBody(Protocol):
    name: str
    hunt: str

    def observe(self) -> dict[str, float]: ...
    def conjectures(self, features: dict[str, float]) -> list[Any]: ...
    def experiment(self, conjecture: Any) -> Any: ...
    def proof_attempt(self, conjecture: Any, result: Any) -> Any: ...
    def attacks(self, conjecture: Any) -> list[Any]: ...
    def execute_attack(self, conjecture: Any, attack: Any) -> tuple[bool, str]: ...
    def recompute(self, step: Any) -> tuple[bool, str]: ...


class Verifier(Protocol):
    """Owned by MetaField, not by the Duck."""

    def check_proof(self, body: MathBody, proof: Any) -> tuple[bool, tuple[str, ...]]: ...
    def attack(self, body: MathBody, conjecture: Any) -> tuple[int, int, tuple[str, ...]]: ...
    def judge(self, body: MathBody, claim: Any) -> Any: ...
