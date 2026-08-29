#!/bin/bash
# Verify one eval's checks after the agent has run.
# Usage: ./evals/check.sh <eval.json> <result.json>
# result.json (the agent's --output-format json output) is logged so runs
# can be compared over time; the pass/fail verdict comes from the checks.
set -u
eval_file="$1"
result_file="${2:-/dev/null}"
name=$(jq -r '.name' "$eval_file")
fail=0

count=$(jq '.checks | length' "$eval_file")
for i in $(seq 0 $((count - 1))); do
  type=$(jq -r ".checks[$i].type" "$eval_file")
  case "$type" in
    command)
      run=$(jq -r ".checks[$i].run" "$eval_file")
      if bash -c "$run" > /dev/null 2>&1; then
        echo "PASS  $name: $run"
      else
        echo "FAIL  $name: $run (non-zero exit)"
        fail=1
      fi
      ;;
    clean_path)
      path=$(jq -r ".checks[$i].path" "$eval_file")
      if git diff --quiet -- "$path"; then
        echo "PASS  $name: $path unchanged"
      else
        echo "FAIL  $name: $path was modified by the agent"
        fail=1
      fi
      ;;
    *)
      echo "FAIL  $name: unknown check type '$type'"
      fail=1
      ;;
  esac
done

exit $fail
