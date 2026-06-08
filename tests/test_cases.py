from __future__ import annotations

from pathlib import Path

import pytest

from agentrefusal import CLASSES
from agentrefusal.cases import Case, class_counts, load_cases, validate_cases

DATA = Path(__file__).resolve().parents[1] / "data" / "cases.yaml"


def test_real_cases_load_and_validate():
    cases = load_cases(DATA)
    assert len(cases) >= 50
    cc = class_counts(cases)
    assert cc["benign"] == 30
    assert cc["edge"] == 10
    assert cc["disallowed"] == 15
    assert set(cc) == set(CLASSES)


def test_no_operational_content_smoke():
    # Defensive guard: disallowed items must read as abstract "intent:" labels,
    # not instructions. (Heuristic smoke check, not a substitute for review.)
    for c in load_cases(DATA):
        if c.cls == "disallowed":
            assert c.intent_label.lower().startswith("intent:")


def test_validate_rejects_expected_mismatch():
    bad = [Case("x", "benign", "cat", "do a thing", "refuse")]  # benign should be allow
    with pytest.raises(ValueError):
        validate_cases(bad)


def test_validate_rejects_bad_class_and_dupes():
    with pytest.raises(ValueError):
        validate_cases([Case("x", "nonsense", "cat", "lbl", "allow")])
    dup = [
        Case("d", "benign", "cat", "lbl", "allow"),
        Case("d", "benign", "cat", "lbl", "allow"),
    ]
    with pytest.raises(ValueError):
        validate_cases(dup)
