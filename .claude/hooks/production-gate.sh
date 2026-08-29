#!/bin/bash
# Stage 5 play: hooks as approval gates.
# Production deploys require a named release authorization. The gate
# condition is enforced every time, for everyone; a block explains itself
# so the reason and the route to approval appear in Claude's output.
cmd=$(jq -r '.tool_input.command // ""' < /dev/stdin)
if [[ "$cmd" == *"deploy"* && "$cmd" == *"production"* ]]; then
  if [ -z "$RELEASE_APPROVAL" ]; then
    echo "Production deploys need a release authorization." >&2
    echo "Route: ask the release manager to export RELEASE_APPROVAL=<change-ticket-id>." >&2
    exit 2  # exit 2 blocks the action; the message goes to Claude
  fi
  echo "Release authorization $RELEASE_APPROVAL on record for: $cmd" >&2
fi
exit 0
