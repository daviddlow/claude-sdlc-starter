#!/bin/bash
# Deterministic companion to the secure-api-review skill: the skill tells
# Claude to run this and include the output in its summary. The same checks
# run in CI, so the advisory control has a mechanical backstop.
set -u
api_files=$(grep -rl "def handle_request" src/ --include="*.py" | grep -v __pycache__ || true)
fail=0

for f in $api_files; do
  echo "checking $f"
  if ! grep -q "X-Gateway-Subject" "$f"; then
    echo "  FAIL: no gateway authentication check found"
    fail=1
  else
    echo "  ok: gateway authentication present"
  fi
  if ! grep -q "_audit(" "$f"; then
    echo "  FAIL: no audit event emitted"
    fail=1
  else
    echo "  ok: audit event emitted"
  fi
done

# Data classification: the status payload must stay within the approved
# field set (the intent.md constraint — no new PII in the portal session).
if PYTHONPATH=src python3 - <<'EOF'
from claims_api.status import get_status
allowed = {"claim_id", "status", "next_step", "expected_days"}
extra = set(get_status("CLM-1001").as_dict()) - allowed
raise SystemExit(1 if extra else 0)
EOF
then
  echo "  ok: status payload within approved fields (no PII)"
else
  echo "  FAIL: status payload carries fields outside the approved set"
  fail=1
fi

exit $fail
