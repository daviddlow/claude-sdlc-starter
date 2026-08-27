---
name: secure-api-review
description: Apply the API security standard. Use whenever creating or
  modifying an external-facing endpoint, reviewing API code, or
  generating an OpenAPI spec.
---
# Secure API review

When you create or change an API endpoint:

1. Authentication: every endpoint requires the gateway subject header
   (`X-Gateway-Subject` in this codebase); no anonymous routes outside
   `/health`.
2. Input validation: validate the path and request body against the schema
   and reject unknown fields and malformed ids.
3. Audit: every state-changing or data-reading endpoint emits an audit
   event with actor, action, entity, and timestamp.
4. Data classification: fields classed as PII must never appear in logs,
   payloads, or error messages. In this repo the status payload is limited
   to claim_id, status, next_step, expected_days.

Run `scripts/check-endpoints.sh` and include its output in your summary.

This skill is advisory; the deterministic layer behind it is the test suite
(tests/test_status.py policy tests) and the review pass in REVIEW.md that
re-checks the policy at the PR.
