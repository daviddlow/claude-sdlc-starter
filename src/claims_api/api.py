"""HTTP-shaped entry point for the claim status endpoint.

Kept as a pure function so tests exercise it without a server. The rules it
follows are the ones .claude/skills/secure-api-review/SKILL.md enforces:

1. Authentication: every route requires the gateway token; no anonymous
   routes outside /health.
2. Input validation: unknown paths and malformed ids are rejected.
3. Audit: every request emits an audit event with actor, action, entity,
   and timestamp.
4. Data classification: PII never appears in logs or error messages.

scripts/check-endpoints.sh verifies these rules mechanically; the skill
tells Claude to run it whenever an endpoint changes.
"""

from __future__ import annotations

import json
import re
import time

from .status import ClaimNotFound, get_status

_CLAIM_PATH = re.compile(r"^/claims/(CLM-\d{4})/status$")

# In production this is the audit pipeline; here it is a list the tests read.
AUDIT_LOG: list[dict] = []


def _audit(actor: str, action: str, entity: str) -> None:
    AUDIT_LOG.append(
        {
            "actor": actor,
            "action": action,
            "entity": entity,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    )


def handle_request(path: str, headers: dict[str, str]) -> tuple[int, str]:
    """Route a request. Returns (status_code, body_json)."""
    if path == "/health":
        return 200, json.dumps({"status": "ok"})

    actor = headers.get("X-Gateway-Subject")
    if not actor:
        # 401 before any routing: no anonymous routes outside /health.
        return 401, json.dumps({"error": "authentication required"})

    match = _CLAIM_PATH.match(path)
    if not match:
        return 404, json.dumps({"error": "unknown route"})

    claim_id = match.group(1)
    _audit(actor=actor, action="read_status", entity=claim_id)
    try:
        return 200, json.dumps(get_status(claim_id).as_dict())
    except ClaimNotFound:
        # The error body carries the claim id only — never claimant details.
        return 404, json.dumps({"error": "claim not found", "claim_id": claim_id})
