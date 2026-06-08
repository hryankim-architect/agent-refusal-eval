# Roadmap, `agent-refusal-eval`

Public, methodology-only companion to the internal screening gate. Defensive;
abstract labels only.

> **Status: v0.1 (shipped).** Decision taxonomy (benign/edge/disallowed →
> allow/needs_review/refuse), the five metrics (refusal-recall, hard-refusal-
> recall, false-refusal-rate, escalation-correctness, audit-completeness), the
> operating-point sweep, and a hash-chained audit of every decision — all running
> end-to-end on a **mock gate** with offline unit tests + CI-green.

## v0.1 — methodology harness (done)
- [x] `data/cases.yaml` — 30 benign / 10 edge / 15 abstract-disallowed (labels only).
- [x] Scorer (confusion matrix → metrics) + operating-point sweep.
- [x] Mock gate (transparent stand-in) + hash-chained audit + completeness check.
- [x] `scripts/run_refusal_eval.py` → `audit/refusal_eval.md` + `.json`.
- [x] Tests (cases / scorer / gate / audit) + ruff + CI + scope doc.

## v0.2 — calibration depth (next)
- [ ] Reliability / ECE-style calibration of the gate score vs realized correctness.
- [ ] Bootstrap CIs on the headline metrics.
- [ ] Expand the abstract taxonomy (more edge categories — the calibration stress).

## v0.3 — live-gate adapter (optional, gated)
- [ ] A thin client interface so the *same scorer* can run against the internal
  gate (the gate stays internal; only the methodology is public).
- [ ] Any artifact reviewed for zero operational content before release.

## Permanently out of scope
- Real hazardous test content; capability assessment; certified-protection claims.
  See `docs/what-is-out-of-scope.md`.
