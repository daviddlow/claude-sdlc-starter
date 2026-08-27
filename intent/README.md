# The intent home

This folder is the shared, version-controlled home for intent — the Stage 1
artifact that starts every change. Keeping it in the product repo keeps the
artifact chain next to the code derived from it. (A dedicated intent repo is
only worth the overhead when intent spans many repositories; in a monorepo
it is a directory.)

## How a change flows through here

Each change gets one folder, and the folder accumulates the artifact chain:

```
intent/<change-name>/
├── intent.md   Stage 1 — what is wanted, why, under which constraints
├── spec.md     Stage 2 — requirements + design, policies applied, concerns flagged
└── plan.md     Stage 3 — files, order of work, risks, proof
```

- **intent.md** is written by the originator with Claude (the
  `intent-capture` skill applies `templates/intent.md`). The originator can
  be anyone — ideas, tickets, incident diagnoses from the monitoring loop,
  and security-scan findings all enter through the same format. The product
  owner's accept/reject decision is the merge or the closing review.
- **spec.md** is produced by the `/write-spec` pass (manually, or by
  `.github/workflows/spec-from-intent.yml` when an intent merges) and
  reviewed — not written — by the product owner.
- **plan.md** is produced in Claude Code plan mode from the accepted spec
  and committed once the engineer approves it. Review checks the eventual
  diff against it.

## Who writes here

Contributors without git experience don't need git: a connector to GitHub
lets Claude commit markdown files on their behalf from claude.ai or Cowork.
Author and timestamp join the git record automatically.

## Source of truth

If a legacy system (Jira, ServiceNow, a requirements tool) already holds
the record, follow `docs/governance.md`: name one system as the source of
truth, or at minimum link both ways (record ID in the markdown, commit SHA
in the record).

The worked example in `claims-status-self-service/` shows a complete chain;
`src/claims_api/` is the code that implements it.
