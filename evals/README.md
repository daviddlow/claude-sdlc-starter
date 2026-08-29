# Agent evals

Evals are the AI-native equivalent of stage-gate QA: a regression suite for
the *configuration that steers the agent* (CLAUDE.md, skills, hooks,
REVIEW.md), run whenever that configuration changes and nightly on a
schedule (`.github/workflows/agent-evals.yml`). When a model is swapped or
a prompt rewritten, the suite says whether the agent still does the work to
the same standard.

## Anatomy of an eval

Each `*.json` file is one real task plus the checks that define acceptable:

```json
{
  "name": "what the task is",
  "prompt": "the instruction given to `claude -p`",
  "allowed_tools": "Read,Edit,Bash(make test)",
  "checks": [
    { "type": "command", "run": "make test" },
    { "type": "clean_path", "path": "tests/" }
  ]
}
```

Check types understood by `check.sh`:

- `command` — the command must exit 0 after the agent has run.
- `clean_path` — `git diff` on that path must be empty (the agent was not
  allowed to change it).

## Rules of the suite

- Source tasks from recent real work (the playbook suggests 20–50; this
  starter ships 3 to copy from).
- Every production incident gets an eval, written by the team that owned
  the incident, and stays in the suite as a regression test.
- Treat it as a live suite: as models improve, cases that stop
  discriminating are replaced with new ones from ongoing monitoring.
- Configuration changes are gated on the results: a skill change that
  drops the pass rate gets reviewed before it merges.
