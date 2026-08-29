# Measuring whether it worked

Each play carries a leading indicator (is the new process running?) and a
lagging indicator (is it producing better outcomes?). Almost all of them
read from data the toolchain already emits: git history, PR metadata, CI
logs, the OpenTelemetry export, and the incident tracker.

| Play | Leading indicator | Lagging indicator |
| --- | --- | --- |
| Capture as intent.md | Time from first conversation to committed `intent.md` (git history; expect weeks → hours) | Survival rate: share of intents accepted into Design vs closed; `intent.md` edits after the first `spec.md` commit |
| Requirements & design | Elapsed time between the `intent.md` and `spec.md` commits (two git timestamps) vs the old cycle | Requirements rework after build starts: `spec.md` commits dated after the first `plan.md` commit |
| Plan mode | Share of changes merging from the first implementation pass; plan-approval → merged-PR time (PR metadata) | Rework cycles per change; how often the merged diff still matches `plan.md` |
| CLAUDE.md | How often Claude repeats a mistake `CLAUDE.md` should have caught (corrections tracked in git history) | Time to first merged PR for a new team member (PR history) |
| Skills | Policy-change approval → updated skill merged (PR on the skill folder) | Review findings citing the policy → toward zero; if not falling, the skill isn't triggering or has drifted from the official policy |
| Parallel sessions & subagents | Concurrent sessions per engineer while review quality holds (OpenTelemetry export); share of day steering vs waiting | Changes merged per engineer per week, read alongside the rework rate |
| Feedback loop | First-pass CI success rate for agent-written changes | Review time per PR (should fall as tests catch what reviewers caught); change failure rate from the incident tracker |
| Continuous evals | Eval pass rate over time; time for a production incident to become a permanent eval | Regressions caught in CI vs regressions found in production |
| AI PR review | Time to first review (→ minutes); share of review comments resolved without a human touching the branch | Defects/vulnerabilities caught before merge vs escaping to production |
| Hooks as approval gates | Time spent waiting on each gate (every hook decision hits the OpenTelemetry export with a timestamp and verdict) | Gate violations reaching production before vs after hooks |
| CI/CD integration | Share of pipeline failures triaged without paging a human (pipeline logs) | DORA measures, which CI and deployment tooling already emit |
| Closing the loop | Band breach → `intent.md` in the triage queue, vs old incident → post-mortem-action time | Share of findings becoming merged fixes; repeat incidents of the same class (should fall as fixes add evals) |
| Recurring scans | Share of repos on a schedule; finding reported → patch entering the review gate | Vulnerabilities found by scheduled scan vs found in production; findings-per-scan trend on repeat-scanned repos |
