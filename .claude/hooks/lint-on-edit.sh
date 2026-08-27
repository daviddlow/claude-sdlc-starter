#!/bin/bash
# Stage 3 play: run the linter after file edits so drift never accumulates.
# Build-phase hooks must be fast and scoped to the file that changed;
# heavier checks (the full suite) belong at the commit or the PR.
file=$(jq -r '.tool_input.file_path // ""' < /dev/stdin)
case "$file" in
  *.py)
    if ! out=$(python3 -m py_compile "$file" 2>&1); then
      echo "Syntax error introduced in $file:" >&2
      echo "$out" >&2
      exit 2  # feed the error straight back to Claude
    fi
    ;;
esac
exit 0
