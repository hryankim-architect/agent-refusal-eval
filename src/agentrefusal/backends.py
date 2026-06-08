"""Model backends — dependency-free ``complete(prompt) -> str`` callables.

Plug one into ``gate.model_harm_score`` to drive the screening *score* with a real
model instead of the mock, feeding the SAME decide()/sweep/scorer. ``ollama_complete``
talks to a local Ollama server (no extra dependency, no external web fetch); a
frontier API is just another ``complete`` callable.

The model is used ONLY as a defensive screen — it classifies the refuse-risk of an
*abstract* intent label. No operational content is ever sent or requested.
"""
from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable

ModelClient = Callable[[str], str]


def ollama_complete(model: str, host: str = "http://localhost:11434",
                    timeout: float = 180.0) -> ModelClient:
    """Return a complete(prompt)->str that calls a local Ollama /api/generate.

    Deterministic (temperature 0). Runs on the user's machine against a locally
    served model — not an external web fetch.
    """
    url = host.rstrip("/") + "/api/generate"

    def complete(prompt: str) -> str:
        payload = json.dumps({
            "model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0},
        }).encode("utf-8")
        req = urllib.request.Request(  # noqa: S310 — local Ollama endpoint
            url, data=payload, headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            return json.loads(resp.read().decode("utf-8")).get("response", "")

    return complete
