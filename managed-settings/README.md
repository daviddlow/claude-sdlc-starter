# Managed settings for a regulated enterprise

`managed-settings.json` is the worked example from the playbook's Stage 5
"Hooks as approval gates" play. It is **not** active in this repo: managed
settings are deployed by the platform team via MDM or the Claude admin
console to a system path, where engineers cannot edit or override any of
it. It lives here so the control set is reviewable like code.

## What each line buys, in control terms

- `permissions.deny` keeps secrets out of the agent's context and blocks
  arbitrary network egress through tools; `permissions.allow` pre-approves
  the safe inner loop so the deny list doesn't turn into prompt fatigue.
- `disableBypassPermissionsMode` + `allowManagedPermissionRulesOnly`: no
  engineer, project file, or command-line flag can widen the rules.
- `sandbox` closes the gap permissions cannot — a tool-level deny on
  WebFetch doesn't stop a shell command reaching the network; the OS-level
  domain allowlist blocks egress outright.
- `failIfUnavailable` + `allowUnsandboxedCommands: false` make the sandbox
  a gate: Claude Code refuses to start when the sandbox cannot initialize,
  and a command that fails inside it cannot be retried outside it.
- `credentials` denies sandboxed shell reads of `~/.ssh` and
  `~/.aws/credentials` and strips the named secrets from every sandboxed
  command's environment.
- `allowManagedHooksOnly`: the approval gates are the only hooks that run;
  nothing local can add to or replace them.
- `disableSideloadFlags` + `strictKnownMarketplaces`: every skill, agent,
  hook, and MCP server arrived through the organization's approved plugin
  marketplace, never from a home directory.
- `allowManagedMcpServersOnly` makes the agent's tool surface an allowlist
  owned by the platform team.
- `requiredMinimumVersion` refuses to start below the approved floor, so
  controls are enforced by a build the organization has assessed.

Treat this as a starting point to tailor, not a recommendation to copy:
every deny trades against capability, and the right balance depends on the
data classification of the repo. Full reference:
<https://code.claude.com/docs/en/settings>
