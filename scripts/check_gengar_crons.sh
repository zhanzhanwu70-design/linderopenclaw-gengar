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
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile

STATE_DB = os.path.expanduser("~/.openclaw/state/openclaw.sqlite")
# Where the standing-fault notice state is kept (de-duplication between cycles).
NOTICE_STATE = os.path.expanduser(
    "~/.openclaw/workspace-gengar/.state/watchdog-inbound-notice.json")

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

def sqlite_snapshot():
    """Copy openclaw.sqlite plus its WAL sidecars so a read-only query sees
    un-checkpointed rows. openclaw.sqlite runs in WAL mode: copying only the
    .sqlite file hides freshly written rows (e.g. a new operator_approvals
    ticket). Returns (db_path, tmpdir) or (None, None).
    """
    if not os.path.exists(STATE_DB):
        return None, None
    tmp = tempfile.mkdtemp(prefix="opappr-")
    db = os.path.join(tmp, "db.sqlite")
    shutil.copyfile(STATE_DB, db)
    for suffix in ("-wal", "-shm"):
        side = STATE_DB + suffix
        if os.path.exists(side):
            shutil.copyfile(side, db + suffix)
    return db, tmp


def run_sqlite_script(script, db):
    """Run a python snippet against a copied DB; returns parsed JSON or None.

    Rules for every sqlite helper used here:
      * SQL is always parameterized; the DB path arrives via argv, never
        interpolated into the script text.
      * No %-formatting of the script (it contains strftime('%m-%d %H:%M')).
      * Errors go to stderr instead of failing silently into an empty result.
    """
    try:
        proc = subprocess.run(
            ["python3", "-c", script, db], capture_output=True, text=True, timeout=60)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write("sqlite helper failed: %s\n" % exc)
        return None
    if proc.returncode != 0:
        sys.stderr.write("sqlite helper failed: " + (proc.stderr or "").strip()[:300] + "\n")
        return None
    try:
        return json.loads(proc.stdout or "null")
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write("sqlite helper returned non-JSON: %s\n" % exc)
        return None


def gateway_restart_approvals():
    """Report gateway-restart approval tickets as their own line.

    A pending ticket means Linder has a 10-minute approval window open RIGHT
    NOW — that must be visible as such, not folded into "restart never
    happened".

    IMPORTANT: openclaw.sqlite runs in WAL mode. A read-only connection sees
    only checkpointed data, so a freshly created approval is invisible unless
    the -wal and -shm sidecars are copied next to the .sqlite file first.
    """
    db, tmp = sqlite_snapshot()
    if db is None:
        return []
    try:
        script = r"""
import json, sqlite3, sys, datetime
con = sqlite3.connect('file:' + sys.argv[1] + '?mode=ro', uri=True)
tz = datetime.timezone(datetime.timedelta(hours=8))
rows = list(con.execute(
    "select approval_id, status, created_at_ms, expires_at_ms, presentation_json "
    "from operator_approvals where kind='system-agent' order by created_at_ms desc limit 20"))
out = []
for approval_id, status, created, expires, presentation in rows:
    try:
        desc = (json.loads(presentation or '{}') or {}).get('description', '')
    except Exception:
        desc = ''
    if 'restart the Gateway' not in desc:
        continue
    def fmt(ms):
        try:
            return datetime.datetime.fromtimestamp(ms / 1000, tz).strftime('%m-%d %H:%M')
        except Exception:
            return '?'
    out.append({
        'id': approval_id,
        'status': status,
        'created': fmt(created),
        'created_ms': created,
        'expires': fmt(expires),
        'expires_ms': expires,
    })
print(json.dumps(out))
"""
        return run_sqlite_script(script, db) or []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def discord_inbound_state():
    """Detect a Discord inbound cliff by comparing SAME clock windows.

    Rolling windows mislead (a 6 h window can contain only pre-cliff rows), so
    compare the last 3 h against the same 3 clock hours yesterday and report the
    age of the newest ingress row.
    """
    db, tmp = sqlite_snapshot()
    if db is None:
        return None
    try:
        script = r"""
import json, sqlite3, sys, time, datetime
con = sqlite3.connect('file:' + sys.argv[1] + '?mode=ro', uri=True)
tz = datetime.timezone(datetime.timedelta(hours=8))
now = int(time.time() * 1000)
now_dt = datetime.datetime.fromtimestamp(now / 1000, tz)
def window(minutes):
    # Rolling window, compared against the SAME clock window on previous days.
    # Yesterday alone is not a reliable baseline when yesterday was broken the same
    # way - use the max over the last 7 days instead.
    a1, a2 = now - minutes * 60 * 1000, now
    cur = list(con.execute(
        'select count(*) from channel_ingress_events where received_at>=? and received_at<?', (a1, a2)))[0][0]
    baseline = []
    for day in range(1, 8):
        b1, b2 = a1 - day * 24 * 3600 * 1000, a2 - day * 24 * 3600 * 1000
        baseline.append(list(con.execute(
            'select count(*) from channel_ingress_events where received_at>=? and received_at<?',
            (b1, b2)))[0][0])
    return cur, max(baseline) if baseline else 0, baseline
cur3, yest3, _ = window(180)
cur1, yest1, _ = window(60)
cur45, yest45, _ = window(45)
newest = list(con.execute('select max(received_at) from channel_ingress_events'))[0][0]
def fmt(ms):
    try:
        return datetime.datetime.fromtimestamp(ms / 1000, tz).strftime('%m-%d %H:%M')
    except Exception:
        return '?'
print(json.dumps({'current': cur3, 'yesterday': yest3, 'current_1h': cur1,
                  'yesterday_1h': yest1, 'current_45m': cur45, 'yesterday_45m': yest45,
                  'newest_ms': newest, 'newest': fmt(newest)}))
"""
        return run_sqlite_script(script, db)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def notice_suppressed(signature):
    """Rate-limit a standing fault: report on change, else at most every 6 h."""
    try:
        with open(NOTICE_STATE, "r", encoding="utf-8") as fh:
            prev = json.load(fh)
    except Exception:
        prev = {}
    now = int(datetime.datetime.now().timestamp() * 1000)
    if prev.get("signature") == signature and now - int(prev.get("ts", 0)) < 6 * 3600 * 1000:
        return True
    try:
        os.makedirs(os.path.dirname(NOTICE_STATE), exist_ok=True)
        with open(NOTICE_STATE, "w", encoding="utf-8") as fh:
            json.dump({"signature": signature, "ts": now}, fh)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write("notice state write failed: %s\n" % exc)
    return False


def fmt_ms(ms):
    try:
        return datetime.datetime.fromtimestamp(ms / 1000).strftime("%m-%d %H:%M")
    except Exception:
        return "?"


def discord_runtime_state():
    """Runtime layer of the Discord accounts.

    `openclaw status` only reports the CONFIG layer ("Discord ON / OK / accounts
    9/9") - that stays green while every bot is actually disconnected. The
    runtime truth is `openclaw channels status`, which reports per-account
    "error:startup-not-ready, running, disconnected".
    """
    try:
        proc = subprocess.run(
            ["openclaw", "channels", "status"], capture_output=True, text=True, timeout=120)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write("channels status failed: %s\n" % exc)
        return None
    if proc.returncode != 0:
        sys.stderr.write("channels status failed: " + (proc.stderr or "").strip()[:200] + "\n")
        return None
    broken = []
    enabled = 0
    for line in (proc.stdout or "").splitlines():
        if not line.strip().startswith("- Discord"):
            continue
        if "enabled," not in line and "disabled," not in line:
            continue
        name = line.split(":", 1)[0].replace("- Discord", "").strip()
        if "disabled" in line:
            continue
        enabled += 1
        if "disconnected" in line or "startup-not-ready" in line or "error:" in line:
            broken.append(name)
    return {"enabled": enabled, "broken": broken}


def gateway_start_ms():
    """Epoch ms when the current Gateway process started, or None."""
    try:
        proc = subprocess.run(
            ["pgrep", "-f", "openclaw/dist/index.js"], capture_output=True, text=True, timeout=15)
        pids = [p for p in proc.stdout.split() if p.strip()]
        if not pids:
            return None
        ps = subprocess.run(
            ["ps", "-o", "lstart=", "-p", pids[0]], capture_output=True, text=True, timeout=15)
        raw = ps.stdout.strip()
        if not raw:
            return None
        dt = datetime.datetime.strptime(raw, "%a %b %d %H:%M:%S %Y")
        return int(dt.timestamp() * 1000)
    except Exception:
        return None


for ticket in gateway_restart_approvals():
    if ticket.get("status") == "pending":
        problems.append(
            "Gateway restart approval PENDING (id %s) - Linder has a ~10 min approval "
            "window open now, expires %s" % (ticket["id"], ticket["expires"]))
    elif ticket.get("status") == "expired":
        # Only report an expiry while the Gateway has NOT been restarted since the
        # ticket was raised - once a restart happened, the stale ticket is noise.
        started = gateway_start_ms()
        created = ticket.get("created_ms")
        if started is not None and created is not None and started > created:
            continue
        problems.append(
            "Gateway restart approval EXPIRED without a decision (id %s, expired %s) - "
            "a new approval must be created" % (ticket["id"], ticket["expires"]))
        break

inbound = discord_inbound_state()
if inbound:
    age_min = None
    if inbound.get("newest_ms"):
        age_min = round((datetime.datetime.now().timestamp() * 1000 - inbound["newest_ms"]) / 60000)
    # A rolling 3 h window dilutes a fresh cliff, so compare the last hour too.
    fresh_cliff = (inbound.get("current_45m") == 0 and int(inbound.get("yesterday_45m") or 0) > 0)
    # Staleness: the newest row can still be inside the last hour while traffic
    # already died (that is exactly the 03:32 case) - treat "nothing newer than
    # 30 min" as a cliff too, as long as the same clock window had traffic on
    # one of the previous 7 days.
    stale = (age_min is not None and age_min > 30 and int(inbound.get("yesterday_45m") or 0) > 0)
    wide_cliff = (inbound.get("current") == 0 and int(inbound.get("yesterday") or 0) > 0)
    if fresh_cliff or stale or wide_cliff:
        signature = "inbound_black|%s|%s|%s|%s|%s" % (
            inbound.get("newest"), inbound.get("current_45m"), inbound.get("yesterday_45m"),
            inbound.get("current_1h"), inbound.get("current"))
        if not notice_suppressed(signature):
            problems.append(
                "Discord INBOUND looks black: %s ingress rows in the last 45 min (3 h window: %s) "
                "vs a %s-row baseline for the same clock window on previous days; newest ingress "
                "row %s (~%s min ago). Websocket clients stuck in READY-timeout backoff - "
                "outbound REST still works"
                % (inbound.get("current_45m"), inbound.get("current"), inbound.get("yesterday_45m"),
                   inbound.get("newest"), age_min))

runtime = discord_runtime_state()
if runtime and runtime.get("broken"):
    signature = "discord_runtime|%s|%s" % (
        len(runtime["broken"]), runtime.get("enabled"))
    if not notice_suppressed(signature):
        problems.append(
            "Discord RUNTIME layer broken: %s of %s enabled accounts disconnected "
            "(error:startup-not-ready) per `openclaw channels status` - `openclaw status` "
            "still shows Discord ON/OK because that is the config layer only"
            % (len(runtime["broken"]), runtime.get("enabled")))

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
