#!/bin/bash
# Stage 3 play: hooks as build-time guardrails.
# Block edits to protected paths: generated code and the frozen v1 package.
# This is the deterministic layer behind the conventions in CLAUDE.md —
# the skill makes violations rare, the hook makes them close to impossible.
file=$(jq -r '.tool_input.file_path // ""' < /dev/stdin)
case "$file" in
  *"/src/gen/"*|src/gen/*)
    echo "Blocked: $file is generated. Change the generator, not its output." >&2
    exit 2
    ;;
  *"/claims_api/v1/"*)
    echo "Blocked: the legacy v1/ package is frozen. Changes go in v2/." >&2
    exit 2
    ;;
esac
exit 0
