---
name: "openclaw-automation-triage"
description: "Triage failing OpenClaw crons/heartbeats and lane health: read run table, classify provider vs local cause, recover without auto-disable."
---

# OpenClaw Automation Triage

Diagnose a failing automation, fix what is fixable in config, and report the true cause.
Every step is grounded in observed OpenClaw behaviour.

## Step 1 — Read the run table before any explanation

```
openclaw automations runs --id <jobId> --limit 25
```

Quote the raw rows (timestamp, status, durationMs, error) when reporting; the duration
classifies the failure before you look anywhere else:

| duration | meaning |
|---|---|
| ~15 s, `error` | provider rejected every candidate fast (HTTP 4xx on the first call) |
| ~260 ms, `skipped` | `heartbeat skipped: no-route` — route unresolved, benign |
| exactly 600004–600005 ms | heartbeat hard cap reached (see Step 8) |
| `timeout (last phase: model-call-started)` | job `timeoutSeconds` too low for the model call |
| `timeout (last phase: tool-execution-started)` | job `timeoutSeconds` too low for the tool phase |

## Step 2 — Read job state, never `enabled` alone

```
openclaw automations get <jobId>
```

Read `state.lastRunStatus`, `state.lastDeliveryStatus`, `state.consecutiveErrors`,
`state.lastError`, `state.autoDisabled.reason`. `enabled: true` proves nothing: OpenClaw
auto-disables after **10 consecutive failures** (`autoDisabled.reason: consecutive-failures`).

## Step 3 — See which candidates were actually tried

```
journalctl --since "<run window>" --no-pager | grep -E 'model-fetch|agent end'
```

Each `model-fetch ... provider=<p> model=<m> status=<code>` line is one candidate attempt —
this separates "the fallback chain worked" from "every candidate hit the same wall".

## Step 4 — Classify the provider error code

- `429 rate_limit_error` + `"Token Plan usage limit reached"` (code 2056) → **account plan
  cap**. The portal credential and the API key are the *same plan*, so an in-vendor fallback
  cannot help; only credits/plan upgrade or a second vendor fixes it.
- `429 overloaded_error` + `"server is busy, please retry later"` → transient capacity; a
  later attempt often succeeds.
- `400 invalid_request_error` + `"invalid params, context window exceeds limit"` (2013) →
  that candidate's context window is smaller than the session prompt (observed: a 1M-ctx model
  accepted a 1.37 MB prompt that a 200k-ctx model rejected).
- `400` on a large request body while small probes succeed → the plan cap is **token-budget
  based**: a big session prompt burns the allowance, a 10-word probe does not.

## Step 5 — Probe the provider directly to separate "exhausted now" from "transient"

Run the provider call yourself, reading the key **inside the process** (never echoed, never
in a command line): `POST https://<provider>/anthropic/v1/messages` with `x-api-key`, then the
same with `Authorization: Bearer`. Probe with a small prompt AND with a payload sized like the
failing job's session. A 200 on the small probe while the job 429s means the cap is
token-budget based, not a dead credential.

## Step 6 — Fix ladder (smallest change first)

1. `timeout (last phase: model-call-started)` → raise `timeoutSeconds` (120 s is the old default
   that killed a job for weeks; 600 s is a sane floor).
2. Long isolated agent job → set `lightContext: true` (a one-line job otherwise loads ~74K
   bootstrap tokens per run and trips shared rate limits).
3. Plan cap → **not a config fix**: owner action (plan/credits top-up, second provider). Do not
   add more in-vendor fallbacks; they share the plan.
4. Context-window 400 → remove that candidate from the chain or shrink the session prompt.

## Step 7 — Recover and confirm

```
openclaw automations run <jobId> --wait          # or without --wait to enqueue
```

Check the receipt (`cron_run_receipts` in `~/.openclaw/state/openclaw.sqlite`) turned `ok`. A
successful run resets `consecutiveErrors`; if the job was auto-disabled, also run
`openclaw automations enable <jobId>` (clears the streak and the autoDisabled flag).

## Step 8 — Report from evidence, and correct yourself when corrected

Quote the run table and the per-candidate status codes; for any "is my lane healthy" claim,
quote the watchdog script output verbatim. If a peer agent contradicts your report, re-derive
both numbers from the same source before replying and rewrite the stored note — a wrong
conclusion left in memory gets reused next round. (A partial read saying "no consecutive
errors" was contradicted by the watchdog's own "4 consecutive failures".)

**Heartbeat-specific:** the cap is a hard constant — `timeout = min(600, ceil(intervalMs/1000))`
— so it can only get *smaller* with a shorter interval, never larger, and `--timeout-seconds`
is rejected for heartbeat jobs. The only lever is turn length: **one bounded check per
heartbeat turn, then reply.** A killed turn counts as a failure toward auto-disable at 10
consecutive failures.

## Step 9 — Verify what already landed, and how to judge inbound

**A failed job that posts to a channel may already have delivered:**

```
openclaw automations runs --id <jobId> --limit 2      # delivery.messageToolSentTo
sessions_history --sessionKey <run.sessionKey>         # primaryPlatformMessageId
```

`status: error` **and** `delivery.delivered: true` **and** a non-empty
`delivery.messageToolSentTo` means the send succeeded before the model call died — re-running
puts a second copy in the channel. Re-run only when no message id exists.

**Discord inbound:** compare the *same clock window* day over day in `channel_ingress_events`
(`/home/amr/.openclaw/state/openclaw.sqlite`, `received_at` in epoch ms): yesterday 03:00–07:00
vs today 03:00–07:00. A rolling window can be satisfied entirely by pre-incident rows and
proves nothing. Cross-check the journal: a monotonic climb in the reconnect "attempt" number
means the websocket never reached READY (a successful READY resets it), and no MESSAGE_CREATE
lines means no inbound. `openclaw status` reporting "Discord ON / OK" only means the plugin is
configured, and outbound REST can keep delivering while the inbound websocket is black.

**Gateway restart:** verify it landed before reporting recovery — a restart can be deferred or
never fire. Check the running pid and its uptime, then in `~/.openclaw/state/openclaw.sqlite`
`gateway_restart_intent` (intent consumed) and `gateway_boot_lifecycle` (boot row
`completed_at_ms` set for the new pid). Observed 2026-11-17: a 07:22 restart had not fired by
10:05 — same pid, uptime unchanged, intent table empty, boot row still NULL — while the fault
it was meant to fix persisted. Re-check inbound only after the restart lands.

## Step 10 — Read the state DB safely (WAL) and report without noise

`~/.openclaw/state/openclaw.sqlite` runs in **WAL mode**: a read-only connection sees only
checkpointed data, so a freshly written row (new `operator_approvals` ticket, new ingress
event) is invisible until the WAL is checkpointed. Copy all three files before querying:

```
cp ~/.openclaw/state/openclaw.sqlite        /tmp/db.sqlite
cp ~/.openclaw/state/openclaw.sqlite-wal    /tmp/db.sqlite-wal   # when present
cp ~/.openclaw/state/openclaw.sqlite-shm    /tmp/db.sqlite-shm   # when present
python3 -c "import sqlite3; con=sqlite3.connect('file:/tmp/db.sqlite?mode=ro',uri=True); ..."
```

Copying only the `.sqlite` file makes a just-created approval look nonexistent — always verify
a fresh row with the full WAL copy before reporting it as missing.

**Embedded helper rules:** see `references/measurement-and-state-db.md` — parameterize SQL, pass
the DB path via `argv`, never `%`-format a script containing `strftime('%m-%d %H:%M')`, print
failures to **stderr**, and verify a helper by running it twice and diffing output.

**Standing faults must be de-duplicated**: announce only when the state *changes*, otherwise
at most every few hours. Key the signature on stable facts (newest row, counts), never on a
value that drifts each cycle (e.g. "age in hours") — a drifting key makes the notice repeat
every run. Keep the signature plus a timestamp in a small state file.

**Gateway-restart approval tickets are 10-minute windows**: report each as its own line with
its expiry so the owner sees the open window, and suppress an *expired* ticket once the Gateway
has restarted since it was raised (compare Gateway process start time with ticket creation
time) — otherwise a stale ticket re-alerts forever.

**When the restart lands**, verify recovery by the **first ingress row after the Gateway
start**, not by the restart log. Observed 2026-11-17: Gateway restarted 13:19:32, first ingress
row 13:20:48 — inbound back 76 s later, hourly ingress immediately in its normal band. Outbound
REST was never the broken half, so a successful cron delivery is not evidence that inbound
recovered.

## Step 11 — Lane report fields

Enumerate jobs with `openclaw automations list --all --json`; the default listing omits
disabled jobs and undercounts. Report per job: id, name, enabled, lastStatus,
consecutiveErrors, last run, nextRun. When grepping logs for `401|403`, exclude PIDs — a
crash-looping service prints its pid on every line (matched a 401 scan with no auth error).
