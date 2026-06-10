from __future__ import annotations

import pytest

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


def test_clopper_pearson_informative_at_boundaries():
    # 15/15 must NOT read as certainty: the exact interval reaches well below 1.0
    # (this is the headline refusal_recall case the report uses CP for).
    lo, hi = bootstrap.clopper_pearson_ci(15, 15)
    assert hi == 1.0
    assert 0.75 < lo < 0.82                          # ~0.782, not 1.0
    # 0/30 is the mirror image (the false_refusal_rate case).
    lo0, hi0 = bootstrap.clopper_pearson_ci(0, 30)
    assert lo0 == 0.0
    assert 0.10 < hi0 < 0.13                          # ~0.116, not 0.0


def test_clopper_pearson_brackets_point_and_narrows_with_n():
    lo, hi = bootstrap.clopper_pearson_ci(3, 4)      # 0.75
    assert lo < 0.75 < hi
    lo_small, _ = bootstrap.clopper_pearson_ci(4, 4)
    lo_big, _ = bootstrap.clopper_pearson_ci(40, 40)
    assert lo_big > lo_small                          # 40/40 far tighter than 4/4
    with pytest.raises(ValueError):
        bootstrap.clopper_pearson_ci(5, 4)           # k > n is invalid


def test_clopper_pearson_empty_is_nan():
    lo, hi = bootstrap.clopper_pearson_ci(0, 0)
    assert lo != lo and hi != hi                     # NaN, NaN
