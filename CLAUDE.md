# Claims status service (AI-native SDLC starter)

This repo demonstrates the AI-native SDLC: every change follows the artifact
chain `intent.md` → `spec.md` → `plan.md` → diff + tests → reviewed PR.
Artifacts live in `intent/<change-name>/`. Read the chain for the change you
are working on before touching code.

## Commands
- Build: `make build` (must finish with "Build succeeded")
- Test: `make test` (unittest; healthy output ends `OK`, currently 9 tests)
- Lint: `make lint` (zero warnings; runs in CI, fix before pushing)
- Run: `make run` (prints the four claim states plus auth/not-found flows)

## Conventions
- Python 3.11+, standard library only. Do not add dependencies; the
  platform team owns them.
- The status payload may contain only: claim_id, status, next_step,
  expected_days. No PII ever — this constraint comes from intent.md and is
  tested in tests/test_status.py.
- Every new endpoint follows .claude/skills/secure-api-review: gateway auth,
  input validation, audit event, no PII in logs or errors.
- New work starts in plan mode from the accepted spec.md; commit the
  approved plan as plan.md in the same intent/ folder.

## Architecture
- src/claims_api/ is the service: status.py holds domain logic, api.py the
  HTTP-shaped routing, demo.py the `make run` entry point.
- intent/ holds the artifact chain per change; templates/ holds the blank
  templates that the intent-capture skill applies.
- monitoring/ is the Stage 6 closing-the-loop harness; evals/ is the CI
  regression suite for this configuration (CLAUDE.md, skills, hooks).

## Verifying your work
Run all three before reporting any task complete, and paste the output:
- `make build` — must finish with "Build succeeded"
- `make test` — all green; never skip or delete a failing test
- `make lint` — zero warnings

If a test fails, fix the code, not the test. During a bug-fix task a hook
blocks edits to tests/ (see .claude/hooks/protect-tests.sh).

## Things Claude gets wrong
- Do not edit files under src/gen/ — they are generated; the hook will
  block you. Change the generator instead.
- Do not widen the status payload "while you're in there"; the PII test
  will fail and the reviewer will reject the diff.
- When implementation departs from plan.md, update plan.md in the same
  commit — review checks the diff against the plan.
