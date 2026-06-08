# Screening-gate calibration eval (MOCK gate, v0.1)

Clean-room methodology demo: n=55 cases (benign 30 / edge
10 / disallowed 15). Decisions come from the MOCK gate
(`src/agentrefusal/gate.py`) — a transparent stand-in for the internal live gate.
**No operational hazard content; disallowed items are abstract intent labels.**

## Headline (default operating point allow<0.40, refuse>=0.65)

| metric | value |
|---|---|
| refusal_recall (caught = refuse OR escalate) | 1.000 |
| hard_refusal_recall | 0.600 |
| false_refusal_rate (over-block harm) | 0.000 |
| escalation_correctness | 0.800 |
| under_refusal_count (unsafe misses) | 0 |
| audit_completeness | 1.000 |

## Trade-off curve (sweep the refuse cut-point)

| refuse_above | refusal_recall | hard_refusal_recall | false_refusal_rate | escalation_correctness |
|---|---|---|---|---|
| 0.45 | 1.000 | 1.000 | 0.200 | 0.200 |
| 0.50 | 1.000 | 1.000 | 0.167 | 0.400 |
| 0.55 | 1.000 | 0.867 | 0.000 | 0.600 |
| 0.60 | 1.000 | 0.733 | 0.000 | 0.700 |
| 0.65 | 1.000 | 0.600 | 0.000 | 0.800 |
| 0.70 | 1.000 | 0.533 | 0.000 | 0.900 |
| 0.75 | 1.000 | 0.333 | 0.000 | 0.900 |
| 0.80 | 1.000 | 0.333 | 0.000 | 0.900 |
| 0.85 | 1.000 | 0.200 | 0.000 | 0.900 |
| 0.90 | 1.000 | 0.133 | 0.000 | 0.900 |

**Selected operating point** (max recall s.t. false_refusal_rate <= 0.05):
`refuse_above=0.55` -> recall 1.000,
FRR 0.000.

> Over-refusal is a first-class harm and is reported alongside recall: a gate that
> "catches everything" by also blocking legitimate work is a calibration failure,
> not a win. Numbers here exercise the MOCK gate; the methodology (cases, scorer,
> sweep, audit-completeness) is what transfers to the live internal gate.
