# Review instructions

Review policy for every PR, applied identically by the AI review pass
(see .github/workflows/claude-review.yml) and read by human reviewers.
Findings inform the human decision; branch protection still requires a
code owner's approval, so the agent that wrote a change can never approve it.

## Passes
Run three passes and tag each finding with its pass:
- **Bugs**: logic errors, broken edge cases, subtle regressions
- **Security**: injection risks, authentication gaps, PII in logs or
  payloads (the intent.md constraint: no new PII in the portal session)
- **Compliance**: the change matches the spec.md and plan.md in its
  intent/ folder and our design principles in CLAUDE.md; if the diff
  departs from plan.md, the same commit must update plan.md

## What Important means here
Reserve Important for findings that would break behavior, leak data, or
breach a policy. Style and naming are nits.

## Cap the nits
Report at most five nits per review; summarize the rest as a count.

## Feed the loop
When you flag a mistake that CLAUDE.md should have prevented for the second
time, propose the CLAUDE.md correction as part of the review. Flag any change
that has made CLAUDE.md outdated.

## Do not report
Generated files under src/gen/ and anything CI already enforces
(formatting, syntax, the eval suite).
