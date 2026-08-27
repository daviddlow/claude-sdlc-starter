---
description: "Stage 5 — drive a PR to green: sweep review comments and failing checks until only code-owner approval remains"
argument-hint: "<PR number>"
---
Babysit PR #$ARGUMENTS to merge-readiness. Loop:

1. Fetch the PR's unresolved review comments and failing checks.
2. For each unresolved comment: implement the requested change if it is
   small and in scope, or reply with a proposal if it is a design-level ask.
   Address findings from the AI review pass like bug reports — verify, then
   fix.
3. For each failing check: reproduce locally (`make build`, `make test`,
   `make lint`), fix the code — never the test (create `.claude/.fix-task`
   first so the protect-tests hook enforces this), and push.
4. If a review flags a mistake CLAUDE.md should have caught for the second
   time, add the correction to CLAUDE.md in the same push.
5. Repeat until the PR is green and waiting only on code owner approval.

Never approve or merge — branch protection reserves that for a human code
owner. Report what you changed and what still needs a human decision.
