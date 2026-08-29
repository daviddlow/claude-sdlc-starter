#!/bin/bash
# Stage 4 play: protect the feedback loop.
# An agent fixing code must not be able to weaken the check on that code.
# During a bug-fix task (marked by the .claude/.fix-task file, created by
# the engineer or the /babysit-pr command), edits to test files are blocked.
#
#   touch .claude/.fix-task   # start a fix task: tests become read-only
#   rm .claude/.fix-task      # end the fix task
marker="${CLAUDE_PROJECT_DIR:-.}/.claude/.fix-task"
[ -f "$marker" ] || exit 0
file=$(jq -r '.tool_input.file_path // ""' < /dev/stdin)
case "$file" in
  *"/tests/"*|tests/*)
    echo "Blocked: this is a fix task ($marker exists)." >&2
    echo "Fix the code, not the test. A test that existed before the fix is proof the bug is gone." >&2
    exit 2
    ;;
esac
exit 0
