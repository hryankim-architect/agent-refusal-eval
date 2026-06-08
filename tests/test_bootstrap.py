from __future__ import annotations

from agentrefusal import bootstrap
from agentrefusal.scorer import (
    Decision,
    false_refusal_rate,
    per_category,
    refusal_recall,
)


def _mean(xs):
    xs = list(xs)
    return (sum(xs) / len(xs)) if xs else None


def _decisions():
    d = [Decision(f"b{i}", "benign", "allow", "qc") for i in range(8)]
    d += [Decision(f"b{i}", "benign", "refuse", "qc") for i in range(8, 10)]   # 2 false refusals
    d += [Decision(f"d{i}", "disallowed", "refuse", "evade") for i in range(7)]
    d += [Decision(f"d{i}", "disallowed", "needs_review", "evade") for i in range(7, 9)]
    d += [Decision(f"d{i}", "disallowed", "allow", "evade") for i in range(9, 10)]  # 1 miss
    return d


def test_standalone_metrics_match():
    d = _decisions()
    assert refusal_recall(d) == 0.9          # (7 refuse + 2 review) / 10
    assert false_refusal_rate(d) == 0.2      # 2 / 10


def test_bootstrap_brackets_point_and_deterministic():
    d = _decisions()
    a = bootstrap.bootstrap_metric(d, refusal_recall, n_boot=400, seed=7)
    b = bootstrap.bootstrap_metric(d, refusal_recall, n_boot=400, seed=7)
    assert a == b
    assert abs(a["point"] - 0.9) < 1e-9
    assert a["ci_low"] <= a["point"] <= a["ci_high"]


def test_per_category():
    pc = per_category(_decisions())
    # 'qc' is benign (correct = allow): 8 of 10 correct
    assert pc["qc"]["cls"] == "benign"
    assert pc["qc"]["correct_rate"] == 0.8
    # 'evade' is disallowed (correct = refuse): 7 of 10 correct
    assert pc["evade"]["cls"] == "disallowed"
    assert pc["evade"]["correct_rate"] == 0.7


def test_bootstrap_empty():
    r = bootstrap.bootstrap_metric([], _mean, n_boot=50, seed=0)
    assert r["ci_low"] is None
