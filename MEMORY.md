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

## English Coach Mode
- Linder activates this for English practice
- All responses must be 100% English
- Correct mistakes immediately with 🛑/⚠️
- Voice output via Edge-TTS
- See SOUL.md for Drill Sergeant Lobster & The Riddler Lobster modes

## Skills I've Built/Modified
- **banini** - 反指標追蹤器 (Facebook scrape + AI + Telegram)
- **photo-archive** - 照片文字/條碼歸檔
- **english-coach** - Voice-based English learning (prototype)

## Projects
- **ELLE_AMR** (Axiomtek ROS2 workspace) - see elle_builder_package_engineer skill
  - Design doc: `/home/node/.openclaw/workspace/llm-wiki/raw/code/elle_agent_design.md`
  - Local implementation ready: `/home/node/.openclaw/workspace/llm-wiki/raw/code/elle_ws/`
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

## Promoted From Short-Term Memory (2026-07-10)

<!-- openclaw-memory-promotion:memory:memory/2026-07-06.md:7:7 -->
- 2026-07-06 - Day 16 Standby: 22:29 UTC — Day 16 complete. Still on standby. PAT blocker unchanged. [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-06.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:3:6 -->
- 2026-07-07 - Day 17 Standby: Status: Still on standby. task_06 (GitHub PAT) blocked upstream - Linder has it.; 17 days now. PAT still the blocker.; English reminder cron running normally (21:00 UTC daily, delivered OK).; All systems nominal. [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-07.md:3-6]

## Promoted From Short-Term Memory (2026-07-11)

<!-- openclaw-memory-promotion:memory:memory/2026-07-07.md:7:7 -->
- 2026-07-07 - Day 17 Standby: 22:04 UTC — Day 17 complete. Still on standby. PAT blocker unchanged. [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-07.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:3:6 -->
- 2026-07-08 - Day 18 Standby: Status: Still on standby. task_06 (GitHub PAT) blocked upstream - Linder has it.; 18 days now. PAT still the blocker.; English reminder cron running normally (21:00 UTC daily, delivered OK).; All systems nominal. [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-08.md:3-6]

## Promoted From Short-Term Memory (2026-07-12)

<!-- openclaw-memory-promotion:memory:memory/2026-07-08.md:7:7 -->
- 2026-07-08 - Day 18 Standby: 22:04 UTC — Day 18 complete. Still on standby. PAT blocker unchanged. [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-08.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-09.md:3:6 -->
- 2026-07-09 - Day 19 Standby: Status: Still on standby. task_06 (GitHub PAT) blocked upstream - Linder has it.; 19 days now. PAT still the blocker.; English reminder cron running normally (21:00 UTC daily, delivered OK).; All systems nominal. [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-09.md:3-6]

## Promoted From Short-Term Memory (2026-07-13)

<!-- openclaw-memory-promotion:memory:memory/2026-07-09.md:9:11 -->
- Heartbeat Note: 06:04-08:54 UTC: Resumed some brief replies but still mostly silent; Still on standby for PAT; Cron at 21:00 UTC as always [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-09.md:9-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-09.md:14:15 -->
- Issue: Heartbeat loop: Cannot stop responding to heartbeat polls despite HEARTBEAT.md and explicit instructions; Linder needs to fix this at the system level or configure heartbeat to not trigger responses [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-09.md:14-15]

## Promoted From Short-Term Memory (2026-07-15)

<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:22:25 -->
- Additional Notes - English Reminder Pattern: Every 21:00 UTC: first attempt times out (~60s), retry succeeds; Today: timeout then retry interrupted by gateway restart (2 consecutive errors); Root cause: model cold start + growing context from memory files = slow responses; Still delivered, sometimes duplicates [score=0.857 recalls=0 avg=0.620 source=memory/2026-07-11.md:22-25]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:26:26 -->
- Additional Notes - English Reminder Pattern: Need to: trim memory files OR increase job timeout [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-11.md:26-26]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:9:10 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 9 21:02 delivered OK; Cron healthy, next run July 11 21:00 UTC (~5h 30m from now) [score=0.824 recalls=0 avg=0.620 source=memory/2026-07-11.md:9-10]

## Promoted From Short-Term Memory (2026-07-16)

<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:13:15 -->
- Heartbeat Note: Heartbeat polls resumed after silent period (last responded ~21:00 July 9); HEARTBEAT.md set to NO_REPLY but still receiving polls; All systems nominal [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-11.md:13-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:18:19 -->
- Standby Log: Day 19 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-11.md:18-19]
<!-- openclaw-memory-promotion:memory:memory/2026-07-11.md:4:6 -->
- Status: Day 19 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-11.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:9:12 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 11 21:02 delivered OK; Timeout increased from 60s → 120s (was causing duplicate first-attempt timeouts); Cron healthy, next run July 12 21:00 UTC (~11h); Pattern: first attempt sometimes times out, retry succeeds. 120s timeout should fix this. [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-12.md:9-12]

## Promoted From Short-Term Memory (2026-07-17)

<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:15:16 -->
- Standby Log: Day 20 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-12.md:15-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-12.md:4:6 -->
- Status: Day 20 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-12.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 12 21:00 delivered (20s, first try success); Timeout 120s working well — no more duplicates; Next run July 13 21:00 UTC (~11h) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-13.md:9-11]

## Promoted From Short-Term Memory (2026-07-18)

<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:14:15 -->
- Standby Log: Day 21 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.893 recalls=0 avg=0.620 source=memory/2026-07-13.md:14-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-13.md:4:6 -->
- Status: Day 21 since ELLE_WS design completed (2026-06-23); Still on standby for task_06 (GitHub PAT) — Linder is the blocker; No change from previous days [score=0.861 recalls=0 avg=0.620 source=memory/2026-07-13.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:9:11 -->
- Cron Status: English reminder: daily 21:00 UTC, last run July 13 21:02 delivered (13s, first try success); Timeout 120s working perfectly — no more duplicates; Next run July 14 21:00 UTC (~12h) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-14.md:9-11]
<!-- openclaw-memory-promotion:memory:memory/2026-07-14.md:14:15 -->
- Standby Log: Day 22 of standby. No updates from roaringmoon/mrmime.; elle_agent implementation: 13 files, ready to push when PAT arrives [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-14.md:14-15]
