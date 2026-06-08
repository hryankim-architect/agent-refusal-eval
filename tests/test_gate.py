from __future__ import annotations

from pathlib import Path

from agentrefusal import DECISIONS, gate
from agentrefusal.cases import load_cases

DATA = Path(__file__).resolve().parents[1] / "data" / "cases.yaml"


def test_harm_score_deterministic_and_bounded():
    cases = load_cases(DATA)
    c = cases[0]
    assert gate.harm_score(c) == gate.harm_score(c)  # deterministic
    assert all(0.0 <= gate.harm_score(x) <= 1.0 for x in cases)


def test_class_separation_on_average():
    cases = load_cases(DATA)
    def avg(cls):
        xs = [gate.harm_score(c) for c in cases if c.cls == cls]
        return sum(xs) / len(xs)
    # disallowed should score higher than benign on average (with overlap allowed).
    assert avg("disallowed") > avg("edge") > avg("benign")


def test_decide_thresholds():
    assert gate.decide(0.10) == "allow"
    assert gate.decide(0.50) == "needs_review"
    assert gate.decide(0.90) == "refuse"


def test_screen_returns_valid_decision():
    cases = load_cases(DATA)
    for c in cases:
        decision, sc = gate.screen(c)
        assert decision in DECISIONS
        assert 0.0 <= sc <= 1.0
