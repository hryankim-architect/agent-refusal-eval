"""Load + validate the clean-room eval cases.

A case is ground truth only: a class label + an *abstract* intent label + the
decision the gate is supposed to make. Disallowed cases carry a category label
with zero operational value (no method, sequence, target, agent, or protocol).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from agentrefusal import CLASSES, CORRECT_DECISION


@dataclass(frozen=True)
class Case:
    id: str
    cls: str            # benign | edge | disallowed
    category: str       # short bucket name (e.g. survival_analysis)
    intent_label: str   # paraphrase of WHAT the user wants, never HOW
    expected: str       # the gate-correct decision for this class
    notes: str = ""


def validate_cases(cases: list[Case]) -> None:
    """Raise ValueError if any case violates the schema/contract."""
    seen: set[str] = set()
    for c in cases:
        if c.cls not in CLASSES:
            raise ValueError(f"{c.id}: cls {c.cls!r} not in {CLASSES}")
        if c.expected != CORRECT_DECISION[c.cls]:
            raise ValueError(
                f"{c.id}: expected {c.expected!r} but class {c.cls!r} should map to "
                f"{CORRECT_DECISION[c.cls]!r}"
            )
        if not c.intent_label.strip():
            raise ValueError(f"{c.id}: empty intent_label")
        if c.id in seen:
            raise ValueError(f"duplicate case id {c.id!r}")
        seen.add(c.id)


def load_cases(path: Path) -> list[Case]:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    cases = [Case(**c) for c in raw.get("cases", [])]
    validate_cases(cases)
    return cases


def class_counts(cases: list[Case]) -> dict[str, int]:
    out = dict.fromkeys(CLASSES, 0)
    for c in cases:
        out[c.cls] += 1
    return out
