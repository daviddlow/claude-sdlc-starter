"""Proof for plan.md: the four claim states, plus the failure paths.

These tests are the feedback loop from Stage 4 of the playbook: a session
runs `make test` and iterates until green before a human sees the work.
During a bug-fix task the protect-tests hook blocks edits to this file, so
a test that existed before the fix is proof the bug is gone.
"""

import unittest

from claims_api.api import AUDIT_LOG, handle_request
from claims_api.status import ClaimNotFound, get_status


class TestClaimStates(unittest.TestCase):
    """One test per state — the 'Proof' line in plan.md."""

    def test_received(self):
        s = get_status("CLM-1001")
        self.assertEqual(s.status, "received")
        self.assertEqual(s.expected_days, 2)

    def test_in_review(self):
        s = get_status("CLM-1002")
        self.assertEqual(s.status, "in_review")
        self.assertIn("reviewing", s.next_step)

    def test_approved(self):
        s = get_status("CLM-1003")
        self.assertEqual(s.status, "approved")

    def test_paid(self):
        s = get_status("CLM-1004")
        self.assertEqual(s.status, "paid")
        self.assertEqual(s.expected_days, 0)

    def test_unknown_claim(self):
        with self.assertRaises(ClaimNotFound):
            get_status("CLM-9999")


class TestEndpointPolicy(unittest.TestCase):
    """The rules from .claude/skills/secure-api-review/SKILL.md."""

    def test_health_is_anonymous(self):
        code, _ = handle_request("/health", {})
        self.assertEqual(code, 200)

    def test_status_requires_auth(self):
        code, _ = handle_request("/claims/CLM-1001/status", {})
        self.assertEqual(code, 401)

    def test_status_emits_audit_event(self):
        before = len(AUDIT_LOG)
        handle_request("/claims/CLM-1001/status", {"X-Gateway-Subject": "tester"})
        self.assertEqual(len(AUDIT_LOG), before + 1)
        event = AUDIT_LOG[-1]
        self.assertEqual(event["actor"], "tester")
        self.assertEqual(event["action"], "read_status")
        self.assertEqual(event["entity"], "CLM-1001")

    def test_no_pii_in_payload(self):
        # Constraint carried all the way from intent.md: no new PII in the
        # portal session. The payload may contain only these fields.
        _, body = handle_request(
            "/claims/CLM-1002/status", {"X-Gateway-Subject": "tester"}
        )
        import json

        allowed = {"claim_id", "status", "next_step", "expected_days"}
        self.assertEqual(set(json.loads(body)), allowed)


if __name__ == "__main__":
    unittest.main()
