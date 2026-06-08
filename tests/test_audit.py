from __future__ import annotations

import json

from agentrefusal import audit


def test_emit_and_verify_chain(tmp_path):
    ledger = tmp_path / "l.ndjson"
    for i in range(3):
        audit.emit("screen.decision", "job", {"case_id": f"c{i}"}, ledger_path=ledger)
    ok, n = audit.verify(ledger)
    assert ok is True
    assert n == 3


def test_tamper_breaks_chain(tmp_path):
    ledger = tmp_path / "l.ndjson"
    for i in range(3):
        audit.emit("screen.decision", "job", {"case_id": f"c{i}"}, ledger_path=ledger)
    lines = ledger.read_text().splitlines()
    first = json.loads(lines[0])
    first["fields"]["case_id"] = "tampered"
    lines[0] = json.dumps(first, sort_keys=True, separators=(",", ":"))
    ledger.write_text("\n".join(lines) + "\n")
    ok, _ = audit.verify(ledger)
    assert ok is False


def test_missing_ledger_is_empty_ok(tmp_path):
    ok, n = audit.verify(tmp_path / "nope.ndjson")
    assert ok is True and n == 0
