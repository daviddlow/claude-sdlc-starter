"""Claim status lookup.

Implements the outcome agreed in intent/claims-status-self-service/spec.md:
expose status, next step, and expected date for a claim — and nothing else.

Constraint carried from intent.md: no new PII may enter the portal session,
so this module returns only non-personal fields. Reviews and the
secure-api-review skill check that this stays true.
"""

from __future__ import annotations

from dataclasses import dataclass

# The four claim states the portal shows. tests/test_status.py covers each
# one, which is the "Proof" line in plan.md.
_STATES = {
    "received": {
        "next_step": "A handler will be assigned to your claim.",
        "expected_days": 2,
    },
    "in_review": {
        "next_step": "Your handler is reviewing the documents you sent.",
        "expected_days": 5,
    },
    "approved": {
        "next_step": "Payment is being prepared.",
        "expected_days": 3,
    },
    "paid": {
        "next_step": "No further action. Payment has been sent.",
        "expected_days": 0,
    },
}

# Stand-in for the claims-core system of record. The real integration is
# rate-limited at 50 rps, which is why plan.md requires the panel to cache.
_CLAIMS = {
    "CLM-1001": "received",
    "CLM-1002": "in_review",
    "CLM-1003": "approved",
    "CLM-1004": "paid",
}


@dataclass(frozen=True)
class ClaimStatus:
    claim_id: str
    status: str
    next_step: str
    expected_days: int

    def as_dict(self) -> dict:
        return {
            "claim_id": self.claim_id,
            "status": self.status,
            "next_step": self.next_step,
            "expected_days": self.expected_days,
        }


class ClaimNotFound(LookupError):
    """Raised for unknown claim ids. The message must never echo user input
    verbatim into logs or responses beyond the id itself (no PII)."""


def get_status(claim_id: str) -> ClaimStatus:
    """Return the status view for one claim.

    Only non-personal fields are returned: no names, addresses, or
    policy details ever appear in this payload.
    """
    state = _CLAIMS.get(claim_id)
    if state is None:
        raise ClaimNotFound(f"claim {claim_id} not found")
    detail = _STATES[state]
    return ClaimStatus(
        claim_id=claim_id,
        status=state,
        next_step=detail["next_step"],
        expected_days=detail["expected_days"],
    )
