# Governance in the AI-native SDLC

The AI-native SDLC keeps the old control objectives and changes the
enforcement: governance runs *as the agent acts*, not in weekly review
cycles. Humans remain accountable for every decision that requires
judgment; their attention moves to the gates.

## The audit trail is the artifact chain

Each stage ends by committing an artifact to version control, and the next
stage begins by reading it. Together the chain **is** the audit record —
who asked for what, what the agent produced, and who approved it:

| Artifact | Evidence it provides | Who approves |
| --- | --- | --- |
| `intent.md` | Author, timestamp, full revision history in the intent home | Product owner (merge = accept, closed review = reject) |
| `spec.md` | The prompt that produced it, the skill versions in force, flagged concerns and their resolutions | Product owner signs off; concerns routed to named policy owners |
| `plan.md` | Design review evidence *before any code is generated*; revisions and who accepted them | Engineer for routine changes; tech lead or architect for higher risk |
| Diff + tests | The literal output of `make test`, the build log, the screenshot diff — evidence from the toolchain | Code owner in PR review |
| Reviewed PR | Findings, fixes, ratings and the human approval, in PR history | Human code owner via branch protection |
| Incident record | Breach timestamp, tier, diagnosis-as-intent.md, triage decision | Service owner triages; changes go through the normal review gate |

## Control layers, weakest to strongest

1. **CLAUDE.md** — working knowledge; reviewable and version controlled,
   but advisory.
2. **Skills** — advisory controls: they make Claude likely to apply policy
   while the code is written; nothing forces a session to comply. Skill
   invocations are logged in session traces; the policy owner reviews
   skill changes like code.
3. **Hooks** — the deterministic layer behind skills. A policy that must
   always hold gets a hook that allows, asks, or blocks: the skill makes
   violations rare, the hook makes them close to impossible. Team hooks
   live in `.claude/settings.json` in git; non-negotiable hooks live in
   managed settings where engineers cannot switch them off.
4. **Managed settings + sandbox** — organization-owned: permission rules
   no flag can widen, OS-level network and credential isolation, an
   approved-marketplace-only plugin surface. See `managed-settings/`.
5. **Branch protection** — separation of duties: the agent that wrote the
   code has no way to approve it, and anything the agent writes arrives as
   a PR with no route to main.
6. **The production gate** — the agent may act up to the gate and cannot
   pass it: a named release manager authorizes production deploys
   (`.claude/hooks/production-gate.sh`), per-environment tiers set what the
   agent may do on the way there.

## Legacy systems and the source of truth

Existing processes already track artifacts — in Jira, a requirements tool,
Figma, a change board. Those systems are hard to displace because auditors
already accept them, so the AI-native SDLC fits around what exists. For
every artifact, name one system as the source of truth:

- **The repo as source of truth** — markdown artifacts are authoritative;
  the legacy system references commits. Cleanest for engineering-led
  organizations: one tool, one timestamp authority.
- **The legacy system as source of truth** — Jira/ServiceNow holds the
  record; the markdown artifacts are working copies. Claude reads the
  record at session start and writes the outcome back through an MCP
  connector in the same session.
- **Linkage as the minimum bar** — artifacts note the record ID; records
  carry the commit SHA. A good transitional state, accepting two sources
  of truth.

## Where the evidence lands

- Hook decisions (allow/block, timestamp) and session transcripts flow to
  the organization's observability stack via the OpenTelemetry export.
- Test/build output is attached to the PR's check run, visible to the
  reviewer and any later auditor.
- Eval runs are logged so results compare over time; the pass-rate
  threshold is a merge check.
- Monitor invocations, findings, and triage decisions are logged with
  timestamps; dismissals carry reasons so they tune the bands.
