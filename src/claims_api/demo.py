"""`make run` target: exercise the endpoint the way the verifier subagent does.

Prints the status of each sample claim plus the auth and not-found paths,
so a human (or the verifier agent in .claude/agents/verifier.md) can see
the changed behavior and its nearest neighboring flows in one pass.
"""

from .api import handle_request

if __name__ == "__main__":
    auth = {"X-Gateway-Subject": "portal-user-demo"}
    print("== healthy flows ==")
    for claim in ("CLM-1001", "CLM-1002", "CLM-1003", "CLM-1004"):
        code, body = handle_request(f"/claims/{claim}/status", auth)
        print(f"GET /claims/{claim}/status -> {code} {body}")
    print("== neighboring flows ==")
    code, body = handle_request("/claims/CLM-1001/status", {})
    print(f"no auth              -> {code} {body}")
    code, body = handle_request("/claims/CLM-9999/status", auth)
    print(f"unknown claim        -> {code} {body}")
    print("Run complete.")
