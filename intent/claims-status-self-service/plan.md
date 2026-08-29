# Plan: claims status self-service (from spec.md 2026-06-04)
Status: approved by R. Chen (portal team), 2026-06-05.

## Files that change
src/claims_api/status.py (new), src/claims_api/api.py (new),
src/claims_api/demo.py (new), tests/test_status.py (new)

## Order of work
1. Add the status domain logic mapping the four claim states.
2. Add the endpoint behind existing gateway auth, with audit events.
3. Wire the demo entry point (`make run`) so the change is verifiable.

## Risks
- The claims-core API rate-limits at 50 rps; the portal panel must cache
  (accepted staleness: under 5 minutes — see spec.md concern 1).
- Riskiest step: the auth boundary. Mitigated by policy tests asserting
  401-before-routing and audit-on-read.
- Option not taken: proxying claims-core fields straight through. Rejected
  because it would leak fields beyond the approved payload (PII constraint).

## Proof
tests/test_status.py covers the four claim states, the unknown-claim path,
the anonymous-health / authenticated-status split, the audit event, and the
no-PII payload shape. `make test` all green; `make run` shows the four
states plus the two nearest neighboring flows.
