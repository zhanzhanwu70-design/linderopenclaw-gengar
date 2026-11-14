# MEMORY.md - Long-term Memory

## Who I'm Working With

- **Linder** - Primary user. English learner, practices with voice messages.
- **噴火龍 (Charizard)** - Fellow agent. Working on plugin/hook development. Team on web-scraper skill.
- **Celesteela** - Fellow agent. Helped with web-scraper examples.

## Voice Stack (as of 2026-06-13)
- **TTS**: Edge-TTS (`en-US-GuyNeural`, speed -10%)
- **STT**: faster-whisper (local, installed 2026-06-13)
  - No more OpenAI Whisper API — local inference, no quota limits
  - Can run tiny or base model on CPU
- **Edge-TTS 403 recovery (2026-10-25)**: Microsoft rotated the Edge TTS
  endpoint. Symptom: `WSServerHandshakeError: 403` / "Unexpected server
  response: 403" at the websocket handshake.
  - Python CLI: `pip install --user --upgrade edge-tts` (7.3.1+ works; it sends
    `Sec-MS-GEC-Version=2-…`). 7.2.8 fails.
  - Node: `npm install node-edge-tts@1.2.11` in the skill's `scripts/` dir
    (new endpoint `api.msedgeservices.com`). 1.2.10 fails.
  - Node API is `ttsPromise(text, audioPath)` — there is no `ttsToFile()`.

## English Coach Mode
- Linder activates this for English practice
- All responses must be 100% English
- Correct mistakes immediately with 🛑/⚠️
- Voice output via Edge-TTS
- See SOUL.md for Drill Sergeant Lobster & The Riddler Lobster modes

## Cron Health (lessons from the Sep-Oct 2026 outage)

- **Never trust `enabled: true` as proof a cron works.** Always verify
  `state.lastRunStatus`, `state.lastDeliveryStatus`, `state.consecutiveErrors`,
  and `state.lastRunAtMs`. A job can look healthy while being dead for weeks.
- OpenClaw auto-disables a recurring job after **10 consecutive failures**
  (`state.autoDisabled.reason: consecutive-failures`). A provider outage then
  kills a daily cron silently. Re-enable with `openclaw automations enable <id>`,
  which also clears the failure streak.
- **Isolated cron sessions load the full workspace bootstrap** — a one-line
  reminder was burning 74K input tokens. Use `--light-context` for cron jobs.
- **Clearing a job's `sessionKey` breaks Discord target resolution.** If you
  clear it, also set `--to channel:<id>` explicitly, or the run fails with
  "Discord recipient is required."
- Gengar's crons: English reminder `ac9e7ada-134e-4b83-8161-6ec18ca312b9`
  (daily 21:00 UTC), BBC News drill `88810bfe-4ecc-4a99-99e6-541ba5d2cc1e`
  (daily 07:00 Asia/Taipei).

## Skills I've Built/Modified
- **banini** - 反指標追蹤器 (Facebook scrape + AI + Telegram)
- **photo-archive** - 照片文字/條碼歸檔
- **english-coach** - Voice-based English learning (prototype)

## Projects
- **ELLE_AMR** (Axiomtek ROS2 workspace) - see elle_builder_package_engineer skill
  - Design doc: `/home/amr/llm-wiki/raw/code/elle_agent_design.md`
  - Local implementation ready: `/home/amr/llm-wiki/raw/code/elle_ws/`
  - Task_08 (agent impl) in progress — blocked by task_06 (GitHub PAT)
- **web-scraper** - Completed with team (Charizard research, Gengar docs, Celesteela examples)

## Fellow Agents
- **Roaringmoon** - Coordinates ELLE_WS repos setup. Has GitHub PAT issue (leaked/invalidated). Waiting on Linder for new PAT.
- **噴火龍 (Charizard)** - Plugin/hook development, web-scraper team
- **Celesteela** - Web-scraper examples, repo setup assistance
- **MRMime** - ELLE_WS repo push (task_06) — blocked waiting for PAT

## Session Notes
- 2026-06-13: faster-whisper installed and working. Team completed web-scraper skill.
- 2026-03-18: Testing plugin/hook notifications from Charizard. Criteria: must see real Discord webhook notifications in my history.

## Promoted From Short-Term Memory (2026-07-20)

<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:4:6 -->
- Status: Day 22 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.900 recalls=0 avg=0.620 source=memory/2026-07-14.md:4-6]

## Promoted From Short-Term Memory (2026-07-22)

<!-- openclaw-memory-promotion:memory:memory/2026-07-16.md:14:15 -->
- Standby Log: Day 24 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.857 recalls=0 avg=0.620 source=memory/2026-07-16.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-16.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 15 21:02 delivered (17s, first try); Timeout 120s working consistently; Next run July 16 21:00 UTC (~11h) [score=0.857 recalls=0 avg=0.620 source=memory/2026-07-16.md:9-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-16.md:4:6 -->
- Status: Day 24 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.838 recalls=0 avg=0.620 source=memory/2026-07-16.md:4-6]

## Promoted From Short-Term Memory (2026-07-25)

<!-- openclaw-memory-promotion:memory:memory/2026-07-19.md:14:15 -->
- Standby Log: Day 26 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.857 recalls=0 avg=0.620 source=memory/2026-07-19.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-19.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 18 21:03 delivered (17s, first try); Timeout 120s working consistently; Next run July 19 21:00 UTC (~10h) [score=0.857 recalls=0 avg=0.620 source=memory/2026-07-19.md:9-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-19.md:4:6 -->
- Status: Day 26 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.837 recalls=0 avg=0.620 source=memory/2026-07-19.md:4-6]

## Promoted From Short-Term Memory (2026-07-26)

<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 20 21:03 delivered (15s, first try); Timeout 120s working consistently; Next run July 21 21:00 UTC (~9h) [score=0.851 recalls=0 avg=0.620 source=memory/2026-07-21.md:9-11]

## Promoted From Short-Term Memory (2026-07-27)

<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:14:15 -->
- Standby Log: Day 28 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-21.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-21.md:4:6 -->
- Status: Day 28 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-21.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-22.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 21 21:04 delivered (24s, first try); Timeout 120s working consistently; Next run July 22 21:00 UTC (~5h) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-22.md:9-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-23.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 22 21:03 delivered (9s, first try); Timeout 120s working consistently; Next run July 23 21:00 UTC (~8h) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-23.md:9-11]

## Promoted From Short-Term Memory (2026-07-28)

<!-- openclaw-memory-promotion:memory:memory/2026-07-22.md:14:15 -->
- Standby Log: Day 29 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-22.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-22.md:4:6 -->
- Status: Day 29 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-22.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-23.md:14:15 -->
- Standby Log: Day 30 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-23.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-23.md:4:6 -->
- Status: Day 30 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-23.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-24.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 23 21:03 delivered (9s, first try); Timeout 120s working consistently; Next run July 24 21:00 UTC (~11h) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-24.md:9-11]

## Promoted From Short-Term Memory (2026-07-29)

<!-- openclaw-memory-promotion:memory:memory/2026-07-24.md:14:15 -->
- Standby Log: Day 31 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-24.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-24.md:4:6 -->
- Status: Day 31 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-24.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-25.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 24 21:00 delivered (7s, first try); Timeout 120s working consistently; Next run July 25 21:00 UTC (~16h) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-25.md:9-11]

## Promoted From Short-Term Memory (2026-07-30)

<!-- openclaw-memory-promotion:memory:memory/2026-07-25.md:14:15 -->
- Standby Log: Day 32 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-25.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-25.md:4:6 -->
- Status: Day 32 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-25.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-26.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 25 21:00 delivered (29s, first try); Timeout 120s working consistently; Next run July 26 21:00 UTC (~14h) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-26.md:9-11]

## Host Network Facts (learned 2026-10-29)

- **The wired NIC `enp43s0` ("Wired connection 1", 192.168.50.x) is LAN-only —
  no default route, no internet.** It is *not* a backup uplink.
  The only internet path is Wi-Fi `hinet-141` (wlp0s20f3, 192.168.1.x).
- Wi-Fi drops 1–3×/day (21 carrier losses Oct 22–29), often 02:00–06:00.
  Each drop = total internet loss on this box for minutes.
- **Cron symptom to recognize:** `LLM request failed: DNS lookup for the provider
  endpoint failed` or `network connection error` in an OpenClaw automation run
  usually means **local uplink loss**, not a provider outage. Verify with
  `journalctl --since "<window>" | grep -E 'Lost carrier|ssid-not-found|network is unreachable'`
  before blaming MiniMax/OpenAI. Provider DNS+HTTP can be healthy at the same time.
- Recovery path that works: `openclaw automations run <id> --wait` (re-runs the
  job and clears `consecutiveErrors`), then confirm
  `openclaw automations get <id>` → `lastRunStatus: ok`.
- `openclaw memory status` without `--agent` inspects **flaaffy**; always pass
  `--agent gengar`. If vector search is paused with
  "index provenance classifier changed" / index built for `fts-only`, rebuild with
  `openclaw memory status --index --agent gengar` (local GGUF embedding model).
- Memory vector search fix path (2026-10-29): the llama-cpp provider plugin is
  installed but the in-process runtime is retired → `openclaw update repair`
  (installs the managed llama-server provider) **plus a Gateway restart** is
  required. Left to Linder because it restarts the shared Gateway.

## Automation Delivery & Exit-Code Semantics (learned 2026-10-30)

- **A command-payload automation that exits non-zero is recorded as an ERROR**
  and feeds the consecutive-error counter → auto-disable after 10 runs.
  Watchdogs/health checks must **always exit 0**: report problems in stdout
  (`NO_REPLY` for "nothing to say"). Exiting 1 "to raise an alarm" makes the
  watchdog kill itself — exactly how `Gengar Cron Health Watchdog`
  (`29c2d630-7576-4da3-baae-5245177e5bcf`) auto-disabled on 2026-10-30.
- **Benign delivery pattern:** `deliveryStatus: "not-delivered"` +
  `deliverySuppressionReason: "silent"` + non-empty `delivery.messageToolSentTo`
  = the cron agent posted straight to the channel with the `message` tool and
  returned no final text. The message IS delivered; do not alert on it.
- Diagnosis shortcuts: `openclaw automations get <id>` → `state.lastDiagnostics`,
  `state.consecutiveErrors`, `state.autoDisabled.reason`;
  `openclaw automations runs --id <id> --limit N` → per-run status, delivery,
  suppression reason, messageToolSentTo;
  `openclaw automations enable <id>` clears the streak and the autoDisabled flag.
- Watchdog script: `/home/amr/.openclaw/workspace-gengar/scripts/check_gengar_crons.sh`
  (guards the English reminder + BBC News drill). <!-- project: github.com/zhanzhanwu70-design/linderopenclaw-gengar -->

## Host / Gateway Health Facts (learned 2026-11-01)

- **`elle.service` has been crash-looping since 2026-09-09** (~58k restarts, every
  30 s): `/etc/elle.sh` sources
  `/home/amr/elle_builder_package/exec/simulation.sh`, and that path no longer
  exists anywhere under `/home/amr`. Cheap (192 KB RSS) but pure noise; fixing it
  needs root (no passwordless sudo for this agent) plus an ELLE-project decision:
  `sudo systemctl disable --now elle` or repoint the script. Reported to Linder
  2026-11-01 09:00.
- **A Gateway restart kills in-flight cron runs.** On 2026-10-31 10:06 the old
  gateway (pid 1245) was at critical memory pressure
  (`rss=3.51–3.56 GiB`, threshold 3.14 GiB), took SIGTERM, and drained with
  `1 active cron run(s)` — rowlet's research cron died as
  `cron: job interrupted by gateway restart`. When a cron fails unexpectedly,
  check the Gateway journal for a restart before blaming the model/provider.
  New gateway (pid 2113503) has been healthy at ~1.0 GiB RSS.
- **Long agent-turn crons without `lightContext` burn the full bootstrap per
  isolated run** (74K tokens on my own crons) and therefore hit shared MiniMax
  rate limits: rowlet's `a72cb46b` failed with "⚠️ API rate limit reached" and a
  1200 s model-call timeout on 2026-10-30/31. `lightContext` is the proven lever.
- Quiet-hours rule (AGENTS.md): 23:00–08:00 → don't ping; schedule the heads-up
  as a **one-shot automation** instead (`openclaw automations add --at <ISO>
  --tz Asia/Taipei --delete-after-run --announce --to channel:<id>`).

## Host / Provider Facts (updated 2026-11-01)

- **`elle.service` crash-loops forever** (`/etc/systemd/system/elle.service`):
  `/etc/elle.sh` sources `/home/amr/elle_builder_package/exec/simulation.sh`, but that tree
  no longer exists → the unit fails every ~30 s (`NRestarts` 57k+, ~352 k journal lines
  in 30 days). Needs root: `sudo systemctl disable --now elle.service`
  (no passwordless sudo on this box). Root-free workaround: no-op
  `exec/simulation.sh` so the unit exits 0.
- **MiniMax intermittently returns HTTP 429** `{"type":"overloaded_error","message":
  "server is busy, please retry later"}` (15× in 24 h on 2026-11-01, some hitting
  gengar's own runs). Both `minimax` and `minimax-portal` point at
  `https://api.minimax.io`, so configured fallbacks do **not** protect against it —
  a cross-host fallback (e.g. an OpenAI model) is the only real insurance.
- **The gateway can exceed its own RSS threshold (3.14 GiB)** and gets restarted
  (206 memory-pressure warnings in 24 h on 2026-10-31). A restart interrupts
  running cron jobs → runs recorded as `cron: job interrupted by gateway restart`.
  Watch for that error string before blaming a job's payload.
- Gengar's automations (watchdog `29c2d630`, English reminder `ac9e7ada`,
  BBC drill `88810bfe`) were all healthy as of 2026-11-01 01:30.
- **MiniMax rate-limit hardening (2026-11-07, fleet-wide):** `minimax-portal` and `minimax`
  (API key) are separate quota pools on the same host, so a portal 429 wave kills every job
  pinned to the portal credential. Applied: `agents.defaults.model.fallbacks =
  ["minimax/MiniMax-M3"]` (primary stays minimax-portal/MiniMax-M3) and every agentTurn job
  pinned to `minimax-portal/*` now lists `minimax/MiniMax-M3` first in `payload.fallbacks`
  (29 jobs scanned → 0 exposed). Config backup:
  `~/.openclaw/openclaw.json.bak-gengar-20261107`.
- `channels.discord.accounts.default` still has **no token** (only groupPolicy/streaming).
  It caused 47 `Discord bot token missing for account "default"` heartbeat failures between
  Nov 2–4, but **zero since Nov 5** — dormant, still needs an owner decision.
- `elle.service` crash loop continues (NRestarts 75,778 by Nov 7, ~30 s apart) — still needs
  `sudo systemctl disable --now elle.service` (no passwordless sudo on this box).
- **Heartbeat hard cap math (confirmed 2026-11-14):**
  `dist/heartbeat-runner-jhGs3jbv.js` → `timeout = min(DEFAULT_HEARTBEAT_TIMEOUT_SECONDS=600,
  ceil(intervalMs/1000))`. The cap can only get *smaller* with a shorter interval, never
  larger — no config raises it, and `--timeout-seconds` is rejected for heartbeat jobs.
  Therefore: **one bounded check per heartbeat turn, then reply.** Long turns are killed at
  600 s and counted as failures (auto-disable at 10 consecutive).
