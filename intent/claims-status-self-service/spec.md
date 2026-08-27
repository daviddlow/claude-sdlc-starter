# Spec: claims status self-service (from intent.md 2026-06-02)
Status: accepted. Product owner: A. Devi (portal).

## Summary
A status view in the customer portal backed by a new read-only endpoint on
the claims API. A customer sees their claim's current status, what happens
next, and the expected number of days to the next step — removing the
status-only calls that consume a third of handler call time.

## Requirements
1. An authenticated customer can retrieve status, next step, and expected
   days for a claim they hold (traces: Proposed outcome).
2. The four claim states are shown: received, in_review, approved, paid
   (traces: claims-core state model).
3. The response contains no PII: claim_id, status, next_step, expected_days
   only (traces: Constraints — "no new PII in the portal session").
4. Access uses the existing gateway authentication; no new auth flows
   (traces: Constraints — "existing authentication only").
5. Every status read is audited with actor, action, entity, timestamp
   (policy: secure-api-review skill).
6. Status messages follow the UX writing rules: direct address, plain
   words, always a next step (policy: brand-voice skill).

## Design
- New endpoint `GET /claims/{id}/status` on the claims API
  (`src/claims_api/api.py`), behind the gateway subject header.
- Domain logic in `src/claims_api/status.py`, mapping claims-core state to
  the customer-facing view.
- The portal panel calls the endpoint and renders the three fields. The
  claims-core API rate-limits at 50 rps, so the panel must cache responses
  per session.
- `/health` remains the only anonymous route.

## Policies applied
- secure-api-review (auth, validation, audit, data classification)
- brand-voice (customer-facing next_step and error copy)

## Areas of concern
1. **Rate limit vs freshness.** claims-core allows 50 rps; caching per
   session may show a status up to a few minutes stale. Resolved with
   claims operations: staleness under 5 minutes is acceptable.
2. **Expected date wording.** A hard date risks breaching the fair-communication
   guideline if missed; the spec uses expected *days to next step* instead.
   Resolved with the brand owner.

## Open questions carried forward
- Third-party loss adjuster access: out of scope for this change; owned by
  A. Devi, to be raised as its own intent if wanted.
