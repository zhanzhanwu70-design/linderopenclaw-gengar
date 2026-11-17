---
name: "openclaw-automation-triage"
description: "Triage failing OpenClaw crons/heartbeats: read run table, classify provider vs local cause, recover without auto-disable."
---

# OpenClaw Automation Triage

Diagnose a failing automation, fix what is fixable in config, and report the true cause.
Every step below is grounded in observed OpenClaw behaviour; no step is speculative.

## Step 1 — Read the run table before any explanation

```
openclaw automations runs --id <jobId> --limit 25
```

Quote the raw rows (timestamp, status, durationMs, error) when reporting. The duration
classifies the failure before you look anywhere else:

| duration | meaning |
|---|---|
| ~15 s, `error` | provider rejected every candidate fast (HTTP 4xx on the first call) |
| ~260 ms, `skipped` | `heartbeat skipped: no-route` — route unresolved, benign |
| exactly 600004–600005 ms | heartbeat hard cap reached (see Step 5) |
| `timeout (last phase: model-call-started)` | job `timeoutSeconds` too low for the model call |
| `timeout (last phase: tool-execution-started)` | job `timeoutSeconds` too low for the tool phase |

## Step 2 — Read job state, never `enabled` alone

```
openclaw automations get <jobId>
```

Use `state.lastRunStatus`, `state.lastDeliveryStatus`, `state.consecutiveErrors`,
`state.lastError`, `state.autoDisabled.reason`. `enabled: true` proves nothing: OpenClaw
auto-disables after **10 consecutive failures** (`autoDisabled.reason: consecutive-failures`).

## Step 3 — See which candidates were actually tried

```
journalctl --since "<run window>" --no-pager | grep -E 'model-fetch|agent end'
```

Each `model-fetch ... provider=<p> model=<m> status=<code>` line is one candidate attempt.
This distinguishes "the fallback chain worked" from "every candidate hit the same wall".

## Step 4 — Classify the provider error code

- `429 rate_limit_error` + `"Token Plan usage limit reached"` (code 2056) → **account plan
  cap**. The portal credential and the API key are the *same plan*, so an in-vendor fallback
  cannot help; only credits/plan upgrade or a second vendor fixes it.
- `429 overloaded_error` + `"server is busy, please retry later"` → transient capacity; a
  later attempt often succeeds.
- `400 invalid_request_error` + `"invalid params, context window exceeds limit"` (2013) →
  that candidate's context window is smaller than the session prompt. Observed: MiniMax-M3
  (1M ctx) accepted a 1.37 MB prompt while MiniMax-M2.7 (200k ctx) rejected the same payload.
- `400` on a request whose *body* is large, while small probes succeed → the plan cap is
  **token-budget based**: a big session prompt burns the allowance, a 10-word probe does not.

## Step 5 — Probe the provider directly to separate "exhausted now" from "transient"

Run the provider call yourself, reading the key **inside the process** (never echoed, never
in a command line): `POST https://<provider>/anthropic/v1/messages` with `x-api-key`, and the
same with `Authorization: Bearer`. Probe with a small prompt AND with a payload sized like
the failing job's session. A 200 on the small probe while the job 429s means the cap is
token-budget based, not a dead credential.

## Step 6 — Fix ladder (smallest change first)

1. `timeout (last phase: model-call-started)` → raise `timeoutSeconds` (120 s is the old
   default that killed a job for weeks; 600 s is a sane floor).
2. Long isolated agent job → set `lightContext: true` (a one-line job otherwise loads ~74K
   bootstrap tokens per run and trips shared rate limits).
3. Plan cap → **not a config fix**. Note it as an owner action (plan/credits top-up, second
   provider). Do not add more in-vendor fallbacks; they share the plan.
4. Context-window 400 → remove that candidate from the chain or shrink the session prompt.

## Step 7 — Recover and confirm

```
openclaw automations run <jobId> --wait          # or without --wait to enqueue
```

Check the receipt (`cron_run_receipts` in `~/.openclaw/state/openclaw.sqlite`) turned `ok`.
A successful run resets `consecutiveErrors`; if the job was auto-disabled, also run
`openclaw automations enable <jobId>` (clears the streak and the autoDisabled flag).

## Step 8 — Report from evidence, and correct yourself when corrected

Quote the run table and the per-candidate status codes. If a peer agent contradicts your
report, re-read the run table and the watchdog output before replying — a partial read that
said "no consecutive errors" was contradicted by the watchdog's own "4 consecutive failures".
For any "is my lane healthy" claim, quote the watchdog script output verbatim.

**Heartbeat-specific:** the cap is a hard constant — `timeout = min(600, ceil(intervalMs/1000))`
— so it can only get *smaller* with a shorter interval, never larger, and `--timeout-seconds`
is rejected for heartbeat jobs. The only lever is turn length: **one bounded check per
heartbeat turn, then reply.** A killed turn is recorded as a failure and counts toward
auto-disable at 10 consecutive failures.

## Step 9 — Verify what already landed, and how to judge inbound

**Before re-running a failed job that posts to a channel**, check whether the first attempt
already delivered:

```
openclaw automations runs --id <jobId> --limit 2      # delivery.messageToolSentTo
sessions_history --sessionKey <run.sessionKey>         # primaryPlatformMessageId
```

A run with `status: error` **and** `delivery.delivered: true` **and** a non-empty
`delivery.messageToolSentTo` already posted — the send succeeded before the model call died.
Re-running it puts a second copy in the channel. Re-run only when no message id exists.

**To decide whether Discord inbound is alive**, compare the *same clock window* day over day in
`channel_ingress_events` (`/home/amr/.openclaw/state/openclaw.sqlite`, `received_at` in epoch
ms): yesterday 03:00–07:00 vs today 03:00–07:00. A rolling window can be satisfied entirely by
pre-incident rows and proves nothing. Cross-check the journal: a monotonic climb in the
reconnect "attempt" number means the websocket never reached READY (a successful READY resets
it), and no MESSAGE_CREATE lines means no inbound. `openclaw status` reporting "Discord
ON / OK" only means the plugin is configured, and outbound REST can keep delivering while the
inbound websocket is black.

**When a peer agent contradicts your report**, re-derive both numbers from the same source
before replying, then rewrite the stored note — a wrong conclusion left in memory gets reused
on the next round.

**After scheduling a Gateway restart, verify it landed before reporting recovery.** A restart
can be deferred or never fire. Check the running pid and its uptime, then the restart tables
in `~/.openclaw/state/openclaw.sqlite`: `gateway_restart_intent` should show the intent
consumed, and `gateway_boot_lifecycle` should show a completed boot (`completed_at_ms` set)
for the new pid. Observed 2026-11-17: a restart scheduled for 07:22 had not fired by 10:05 —
same pid, uptime unchanged, `gateway_restart_intent` empty, current boot row still
`completed_at_ms = NULL` — while the Discord inbound fault it was meant to fix persisted.
Re-check inbound only after the restart actually lands.
