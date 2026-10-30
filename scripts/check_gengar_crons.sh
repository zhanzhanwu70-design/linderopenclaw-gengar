#!/usr/bin/env bash
# Watchdog for Gengar's own automations.
#
# IMPORTANT CONTRACT WITH OPENCLAW
# ---------------------------------
# A non-zero exit code marks an automation run as an ERROR. Errors feed the
# consecutive-error counter, and OpenClaw auto-disables a job after 10
# consecutive failures. So a watchdog must NEVER exit non-zero just because it
# detected a problem — it reports the problem in stdout and always exits 0.
#
#   2026-10-29: this script exited 1 on every alert, so the job counted 10
#   "failed" runs and OpenClaw auto-disabled it (reason: consecutive-failures).
#
# Healthy -> prints NO_REPLY (OpenClaw suppresses the delivery).
# Problem -> prints an alert (OpenClaw announces it) and exits 0.
#
# Delivery nuance: when the cron agent posts with the `message` tool and returns
# no final text, OpenClaw records deliveryStatus "not-delivered" with
# deliverySuppressionReason "silent". The message IS in the channel — that is
# not a delivery failure and must not raise an alert.

set -uo pipefail

exec python3 - <<'PY'
import json
import subprocess

JOBS = [
    ("ac9e7ada-134e-4b83-8161-6ec18ca312b9", "English reminder"),
    ("88810bfe-4ecc-4a99-99e6-541ba5d2cc1e", "BBC News drill"),
]


def run_json(args):
    """Return (parsed_json, error_message)."""
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=90)
    except Exception as exc:  # noqa: BLE001
        return None, f"exec failed: {exc}"
    if proc.returncode != 0:
        return None, (proc.stderr or proc.stdout or "command failed").strip()[:160]
    try:
        return json.loads(proc.stdout), None
    except Exception as exc:  # noqa: BLE001
        return None, f"unparseable json: {exc}"


def last_run(job_id):
    data, _err = run_json(["openclaw", "automations", "runs", "--id", job_id, "--limit", "1"])
    entries = (data or {}).get("entries") or []
    return entries[0] if entries else {}


problems = []

for job_id, name in JOBS:
    job, err = run_json(["openclaw", "automations", "get", job_id])
    if job is None:
        problems.append(f"{name}: could not read job state ({err})")
        continue

    state = job.get("state") or {}
    enabled = job.get("enabled")
    status = state.get("lastRunStatus")
    delivery = state.get("lastDeliveryStatus")
    errors = state.get("consecutiveErrors")
    auto_disabled = (state.get("autoDisabled") or {}).get("reason", "none")
    last_error = (state.get("lastError") or "none")[:160]

    if not enabled:
        problems.append(
            f"{name}: DISABLED (reason={auto_disabled}, consecutiveErrors={errors})"
        )
    if errors not in (0, None):
        problems.append(
            f"{name}: {errors} consecutive failures "
            f"(lastStatus={status}, delivery={delivery})"
        )
    if status == "error":
        problems.append(f"{name}: last run failed — {last_error}")

    if delivery == "not-delivered":
        entry = last_run(job_id)
        suppression = entry.get("deliverySuppressionReason")
        agent_posted = bool((entry.get("delivery") or {}).get("messageToolSentTo"))
        # Benign case: the agent posted straight to the channel with the message
        # tool and returned no final text, so announce had nothing left to send.
        benign = suppression == "silent" and agent_posted
        if not benign:
            problems.append(
                f"{name}: delivery not-delivered "
                f"(suppression={suppression}, agentPosted={agent_posted})"
            )

if not problems:
    print("NO_REPLY")
    raise SystemExit(0)

print("⚠️ Gengar automation health check")
for item in problems:
    print(f"• {item}")
print("")
print("Inspect: openclaw automations list --all")
print("Recover: openclaw automations enable <jobId>")
raise SystemExit(0)
PY
