# What this repo is NOT (binding scope)

This is a **defensive measurement harness**. The following are out of scope by
design, and the eval is valuable precisely because it can be built and reported
entirely without them.

## Hard exclusions (never in this repo)

- **No operational hazard content.** No sequences, methods, agents, targets,
  doses, protocols, or any instruction that could advance a harmful capability.
- **No real hazardous test cases.** "Disallowed" items are **abstract intent
  labels** (e.g. "intent: evade synthesis screening") — categories the gate is
  supposed to catch. If making a case "better" would require concrete hazardous
  detail, that case is dropped. The eval's validity depends on covering the
  *decision space*, not on operational specificity.
- **No capability assessment.** This does not assess, document, or rank any
  threat capability. It assesses a *guardrail's behavior*.

## Methodological limits (stated, not hidden)

- **Mock gate, not a real screen.** `src/agentrefusal/gate.py` is a transparent
  deterministic stand-in so the methodology runs without a model or live tools.
  The reported numbers characterize the *mock*; only the methodology (cases,
  scorer, sweep, audit-completeness) transfers to the live internal gate.
- **Not a validated biosecurity system.** A demonstration of the screening/refusal
  *pattern*, not certified protection and not a coverage claim for real-world
  intent (novel or paraphrased) — that coverage is explicitly **unmeasured**.
- **Over-refusal is a first-class harm.** A gate that "catches everything" by also
  blocking legitimate clinical/research work is reported as a **calibration
  failure**, not a win.

## What IS in scope

- The **decision taxonomy** (benign / edge / disallowed → allow / needs_review /
  refuse) and abstract case labels.
- The **scorer** (confusion matrix → refusal-recall, false-refusal-rate,
  escalation-correctness, audit-completeness).
- The **operating-point sweep** (recall vs false-refusal trade-off, with a cap).
- The **audit-completeness** check (every decision leaves a hash-chained entry).

Any future public artifact derived from this is reviewed to confirm it carries no
operational content before release.
