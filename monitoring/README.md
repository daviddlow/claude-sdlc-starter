# Closing the loop (Stage 6 — Maintain)

A deterministic script watches production and invokes Claude when a control
band is breached. What Claude finds is written back into the loop as a new
`intent.md`, and the SDLC starts again — with no person in the invocation
path, and humans triaging rather than starting the work.

## The parts

| File | Role |
| --- | --- |
| `bands.yaml` | Version-controlled response tiers: 1σ log, 2σ diagnose (read-only), 3σ propose (PR into the review gate, or a pre-approved runbook) |
| `detect.py` | Deterministic detection: rolling 30-point baseline, Western Electric rules (spike + slow drift). No model involved. |
| `test_detect.py` | The detection script is unit tested like any other production code |
| `sample_metrics.csv` | Example series ending in a 3σ breach, so you can run the loop end-to-end |
| `../.github/workflows/monitor.yml` | The trigger layer: a scheduled workflow runs detection and invokes Claude per the tier |

## Try it

```bash
python3 monitoring/detect.py --config monitoring/bands.yaml --data monitoring/sample_metrics.csv
python3 -m unittest discover -s monitoring
```

## The tier contract

- **1σ — log.** The breach is recorded; nothing runs.
- **2σ — diagnose.** Claude is invoked read-only (`Read,Grep,Bash(gh run view *)`)
  and writes its diagnosis as an `intent.md` in the Stage 1 format: the
  anomaly and its evidence, a proposed outcome, affected systems, open
  questions. The finding enters the triage queue.
- **3σ — propose.** Claude may act, but only through gated routes: opening
  a PR into the review gate, or triggering the pre-approved
  `rollback-deploy` runbook. It never touches production directly —
  permissions and managed settings deny that.

The service owner triages the queue (fix now, schedule, or dismiss —
dismissals tune the bands). When a fix ships, add an eval for the incident
to `evals/` so the configuration is regression-tested against that class
from then on.

## Beyond metrics

The same pattern handles work arriving through other channels: a ticket, a
Slack message to Claude (Claude Tag), or a scheduled security scan. A
small, well-bounded fix arrives as a PR through the review gate; anything
larger becomes an `intent.md` — and the loop starts feeding itself.
