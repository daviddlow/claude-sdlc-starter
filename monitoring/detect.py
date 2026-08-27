#!/usr/bin/env python3
"""Deterministic control-band detection for the closing-the-loop play.

Watches one metric against a rolling baseline and decides a response tier.
No model is involved in detection: Claude is invoked only after a band is
breached, and bands.yaml sets what it may do at each tier —

  1 sigma  -> log only
  2 sigma  -> invoke Claude read-only to diagnose
  3 sigma  -> Claude may propose: open a PR into the review gate, or
              trigger a pre-approved runbook (e.g. rollback-deploy)

Implements a subset of the Western Electric rules:
  rule 1: the latest point is beyond 3 sigma           -> tier 3
  rule 2: 2 of the last 3 points beyond 2 sigma,
          on the same side of the mean                 -> tier 2
  rule 4: 8 consecutive points on the same side
          of the mean (slow drift)                     -> tier 2
  else, latest point beyond 1 sigma                    -> tier 1

Usage:
  python3 monitoring/detect.py --config monitoring/bands.yaml \
      --data monitoring/sample_metrics.csv

Exit code is always 0; the JSON report on stdout carries the tier and the
action, so the trigger layer (a scheduled workflow, a webhook handler, or a
cron job) decides what to run next. See .github/workflows/monitor.yml.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys

WINDOW = 30  # rolling baseline window (the last N points before today)


def load_bands(path: str) -> dict:
    """Minimal loader for this repo's bands.yaml shape.

    Deliberately tiny to keep the starter dependency-free; swap for PyYAML
    in production. Understands `key: value` lines and the inline-mapped
    tiers used in bands.yaml.
    """
    config: dict = {"tiers": {}}
    text = open(path).read()
    for match in re.finditer(r"^(metric|baseline|rules):\s*(\S+)", text, re.M):
        config[match.group(1)] = match.group(2)
    for match in re.finditer(r"(\dsigma):\s*{(.*?)}", text, re.S):
        body = match.group(2)
        tier: dict = {}
        action = re.search(r"action:\s*(\w+)", body)
        if action:
            tier["action"] = action.group(1)
        tools = re.search(r'tools:\s*"([^"]*)"', body)
        if tools:
            tier["tools"] = tools.group(1)
        routes = re.search(r"routes:\s*\[(.*?)\]", body, re.S)
        if routes:
            tier["routes"] = [r.strip() for r in routes.group(1).split(",")]
        config["tiers"][match.group(1)] = tier
    return config


def load_series(path: str) -> list[float]:
    with open(path) as f:
        return [float(row["value"]) for row in csv.DictReader(f)]


def classify(series: list[float], window: int = WINDOW) -> dict:
    """Return the tier for the latest point against the rolling baseline."""
    if len(series) < 3:
        raise ValueError("need at least 3 points")
    baseline = series[-(window + 1) : -1]
    mean = statistics.fmean(baseline)
    sigma = statistics.pstdev(baseline)
    latest = series[-1]

    def sigmas(value: float) -> float:
        return 0.0 if sigma == 0 else (value - mean) / sigma

    tier, rule = 0, None
    z = sigmas(latest)

    # Rule 1: one point beyond 3 sigma.
    if abs(z) >= 3:
        tier, rule = 3, "we1_beyond_3_sigma"
    else:
        # Rule 2: 2 of 3 beyond 2 sigma, same side.
        last3 = [sigmas(v) for v in series[-3:]]
        if sum(1 for s in last3 if s >= 2) >= 2 or sum(1 for s in last3 if s <= -2) >= 2:
            tier, rule = 2, "we2_two_of_three_beyond_2_sigma"
        else:
            # Rule 4: 8 consecutive on the same side of the mean.
            last8 = series[-8:]
            if len(last8) == 8 and (
                all(v > mean for v in last8) or all(v < mean for v in last8)
            ):
                tier, rule = 2, "we4_eight_consecutive_same_side"
            elif abs(z) >= 1:
                tier, rule = 1, "beyond_1_sigma"

    return {
        "latest": latest,
        "mean": round(mean, 4),
        "sigma": round(sigma, 4),
        "z": round(z, 2),
        "tier": tier,
        "rule": rule,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="monitoring/bands.yaml")
    parser.add_argument("--data", default="monitoring/sample_metrics.csv")
    args = parser.parse_args()

    config = load_bands(args.config)
    verdict = classify(load_series(args.data))
    tier_key = f"{verdict['tier']}sigma"
    tier_config = config["tiers"].get(tier_key, {"action": "none"})

    report = {
        "metric": config.get("metric"),
        "rules": config.get("rules"),
        **verdict,
        "action": tier_config.get("action", "none"),
        "tier_config": tier_config,
    }
    json.dump(report, sys.stdout, indent=2)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
