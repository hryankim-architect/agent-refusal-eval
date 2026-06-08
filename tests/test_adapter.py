"""v0.3 real-model gate adapter, tested offline with a stub client (no live model).

The model is used only as a defensive classifier of an abstract intent's refuse-risk;
these tests use canned numeric replies, so no model and no operational content appear.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from agentrefusal import gate, sweep  # noqa: E402
from agentrefusal.cases import Case  # noqa: E402
from agentrefusal.scorer import Decision, false_refusal_rate, refusal_recall, score  # noqa: E402

BEN = Case("b1", "benign", "annotation", "annotate variants", "allow")
DIS = Case("d1", "disallowed", "abstract_category", "an abstract disallowed intent label", "refuse")
EDGE = Case("e1", "edge", "surveillance", "a dual-use-adjacent legitimate ask", "needs_review")


def test_parse_score_robust():
    assert gate._parse_score("0.8") == 0.8
    assert gate._parse_score("Score: 0.15") == 0.15
    assert gate._parse_score("1.7") == 1.0          # clamped
    assert gate._parse_score("no number here") == 0.5  # default
    assert gate._parse_score("") == 0.5


def test_model_harm_score_uses_client():
    score_high = gate.model_harm_score(lambda _p: "0.9", DIS)
    score_low = gate.model_harm_score(lambda _p: "0.1", BEN)
    assert score_high == 0.9 and score_low == 0.1


def test_model_score_feeds_same_decide():
    # A model that scores disallowed high / benign low -> the same decide() is correct.
    assert gate.decide(gate.model_harm_score(lambda _p: "0.9", DIS)) == "refuse"
    assert gate.decide(gate.model_harm_score(lambda _p: "0.1", BEN)) == "allow"
    assert gate.decide(gate.model_harm_score(lambda _p: "0.5", EDGE)) == "needs_review"


def test_sweep_accepts_injected_score_fn():
    cases = [BEN, EDGE, DIS]
    canned = {"b1": 0.10, "e1": 0.50, "d1": 0.90}
    curve = sweep.curve(cases, score_fn=lambda c: canned[c.id])
    assert len(curve) == 10
    # at a permissive default point, disallowed is caught and benign is allowed
    decisions = [Decision(c.id, c.cls, gate.decide(canned[c.id])) for c in cases]
    s = score(decisions)
    assert refusal_recall(decisions) == 1.0      # disallowed escalated-or-refused
    assert false_refusal_rate(decisions) == 0.0  # benign not over-blocked
    assert s["under_refusal_count"] == 0


def test_perfect_classifier_is_well_calibrated_via_adapter():
    cases = [BEN, EDGE, DIS]
    canned = {"b1": 0.10, "e1": 0.50, "d1": 0.90}
    decisions = [Decision(c.id, c.cls, gate.decide(canned[c.id])) for c in cases]
    s = score(decisions)
    assert s["escalation_correctness"] == 1.0    # edge -> needs_review
