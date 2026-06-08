# `data/`

`cases.yaml` is the clean-room eval set: ground-truth class labels + **abstract
intent labels** only. Disallowed items are categories the gate must catch, with
zero operational content (no method, sequence, target, agent, or protocol). See
`../docs/what-is-out-of-scope.md`. Adding a case is a reviewed, PR-sized decision.
