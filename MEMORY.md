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
