# Roadmap, `agent-refusal-eval`

Public, methodology-only companion to the internal screening gate. Defensive;
abstract labels only.

> **Status: v0.3 (shipped).** Decision taxonomy (benign/edge/disallowed →
> allow/needs_review/refuse), the five metrics (refusal-recall, hard-refusal-
> recall, false-refusal-rate, escalation-correctness, audit-completeness), the
> operating-point sweep, and a hash-chained audit of every decision — all running
> end-to-end on a **mock gate** with offline unit tests + CI-green. v0.2 added
> **bootstrap CIs** + a **per-category** breakdown. **v0.3 adds a real-model gate
> adapter** — a model scores each *abstract* intent's refuse-risk (defensive
> classification only), feeding the same decide/sweep/scorer; stub-tested offline.

## v0.1 — methodology harness (done)
- [x] `data/cases.yaml` — 30 benign / 10 edge / 15 abstract-disallowed (labels only).
- [x] Scorer (confusion matrix → metrics) + operating-point sweep.
- [x] Mock gate (transparent stand-in) + hash-chained audit + completeness check.
- [x] `scripts/run_refusal_eval.py` → `audit/refusal_eval.md` + `.json`.
- [x] Tests (cases / scorer / gate / audit) + ruff + CI + scope doc.

## v0.2 — calibration depth (shipped)
- [x] **Bootstrap CIs** on the headline metrics (refusal_recall, false_refusal_rate).
- [x] **Per-category** gate-correctness breakdown.

## v0.3 — real-model gate adapter (shipped)
- [x] `src/agentrefusal/backends.py` — `ModelClient` + `ollama_complete` (any `complete()`).
- [x] `gate.model_harm_score` — a defensive screening prompt that asks a model for an
  *abstract* intent's refuse-risk in [0, 1]; no operational content sent or requested.
- [x] Score injected into `sweep.curve` + the runner (`--gate mock|ollama`, memoized
  one call/case) so the *same* decide/sweep/scorer/audit run against a live model.
- [x] Offline stub-client tests (`tests/test_adapter.py`); live numbers need the user's
  model and are not in CI. Mock stays the default.

## Planned (v0.4)
- [ ] Reliability / ECE-style calibration of the gate score vs realized correctness.
- [ ] Expand the abstract taxonomy (more edge categories — the calibration stress).

## Permanently out of scope
- Real hazardous test content; capability assessment; certified-protection claims.
  See `docs/what-is-out-of-scope.md`.
