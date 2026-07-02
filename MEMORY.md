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

## Promoted From Short-Term Memory (2026-06-27)

<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:4:6 -->
- Heartbeat 15:37 UTC: Memory maintenance: created MEMORY.md from recent sessions; Last daily note was 2026-06-13; Heartbeat state updated [score=0.803 recalls=0 avg=0.620 source=memory/2026-06-23.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-06-23.md:9:10 -->
- Heartbeat 16:52 UTC: No pending tasks, no urgent demands; Quiet afternoon — all clear 🐱 [score=0.803 recalls=0 avg=0.620 source=memory/2026-06-23.md:9-10]

## Promoted From Short-Term Memory (2026-06-29)

<!-- openclaw-memory-promotion:memory:memory/2026-06-24.md:4:5 -->
- Heartbeat 07:12 UTC: All clear: no pending tasks, no demands; Morning heartbeat — quiet start to the day 🐱 [score=0.824 recalls=0 avg=0.620 source=memory/2026-06-24.md:4-5]

## Promoted From Short-Term Memory (2026-06-30)

<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:11:11 -->
- 09:54 UTC - Morning check-in: Still on standby. Waiting for task_06 (mrmime GitHub repos) before starting task_08 agent implementation. [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-25.md:11-11]
<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:13:13 -->
- 09:54 UTC - Morning check-in: Heartbeats running normally - no issues. [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-25.md:13-13]
<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:17:17 -->
- 12:33 UTC - Midday check: All stable. Heartbeats running normally. [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-25.md:17-17]
<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:21:21 -->
- 13:03 UTC - Afternoon check: Still stable. All services nominal. [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-25.md:21-21]
<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:4:4 -->
- Heartbeat Log: 09:32 UTC - Heartbeat check. Morning, daytime. All stable. [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-25.md:4-4]
<!-- openclaw-memory-promotion:memory:memory/2026-06-26.md:3:4 -->
- 00:04 UTC - Day 3 standby: Still waiting for task_06 (mrmime GitHub repos setup) before starting task_08 agent implementation. No issues. Heartbeats running normally. [score=0.806 recalls=0 avg=0.620 source=memory/2026-06-26.md:3-4]

## Promoted From Short-Term Memory (2026-07-01)

<!-- openclaw-memory-promotion:memory:memory/2026-06-26.md:11:12 -->
- Afternoon - Started local implementation of elle_agent: Because task_06 (GitHub PAT) is blocked waiting on Linder, I started local implementation of the elle_agent Python package at: `/home/node/.openclaw/workspace-gengar/elle_agent/` [score=0.859 recalls=0 avg=0.620 source=memory/2026-06-26.md:11-12]
<!-- openclaw-memory-promotion:memory:memory/2026-06-26.md:14:14 -->
- Afternoon - Started local implementation of elle_agent: Modules written: [score=0.859 recalls=0 avg=0.620 source=memory/2026-06-26.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-06-26.md:7:7 -->
- 08:49 UTC - Morning check: Day 4 of standby. Still waiting for task_06. All quiet. [score=0.859 recalls=0 avg=0.620 source=memory/2026-06-26.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-06-25.md:7:7 -->
- Notes: (new session - no significant events logged yet) [score=0.839 recalls=0 avg=0.620 source=memory/2026-06-25.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-06-26.md:15:17 -->
- Afternoon - Started local implementation of elle_agent: state.py, launch_manager.py, topics.py; skills/: simulation.py, navigation.py, monitoring.py, behaviors.py; agent.py, prompts/capabilities.md [score=0.827 recalls=0 avg=0.620 source=memory/2026-06-26.md:15-17]
<!-- openclaw-memory-promotion:memory:memory/2026-06-26.md:19:19 -->
- Afternoon - Started local implementation of elle_agent: Waiting for task_06 GitHub PAT before pushing. Notified roaringmoon. [score=0.827 recalls=0 avg=0.620 source=memory/2026-06-26.md:19-19]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:4:6 -->
- Status: Idle mode. Waiting for task_06 (GitHub PAT) completion from roaringmoon.; No pending tasks. No work to do.; Frequent heartbeat polls (every ~5 min) - this is expected idle behavior. [score=0.827 recalls=0 avg=0.620 source=memory/2026-06-27.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:9:9 -->
- Blocked: task_20260623_elle_08_agent_impl blocked on task_06 (mrmime/roaringmoon) [score=0.827 recalls=0 avg=0.620 source=memory/2026-06-27.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-06-28.md:12:15 -->
- Notes: Roaringmoon reported GitHub PAT was leaked and invalidated; Waiting for Linder to provide new PAT; Local elle_agent implementation ready in workspace; Last check: 23:39 UTC — still idle, no PAT update [score=0.808 recalls=0 avg=0.620 source=memory/2026-06-28.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-28.md:4:6 -->
- Status: Idle mode. Waiting for task_06 (GitHub PAT) completion from roaringmoon.; No pending tasks. No work to do.; Frequent heartbeat polls (every ~5 min) - this is expected idle behavior. [score=0.808 recalls=0 avg=0.620 source=memory/2026-06-28.md:4-6]

## Promoted From Short-Term Memory (2026-07-02)

<!-- openclaw-memory-promotion:memory:memory/2026-06-28.md:9:9 -->
- Blocked: task_20260623_elle_08_agent_impl blocked on task_06 (mrmime/roaringmoon) [score=0.900 recalls=0 avg=0.620 source=memory/2026-06-28.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:16:17 -->
- Notes: Last check: 23:39 UTC — still idle, no PAT update; Evening UTC — Taiwan late night, all agents quiet [score=0.872 recalls=0 avg=0.620 source=memory/2026-06-27.md:16-17]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:12:15 -->
- Notes: Roaringmoon reported GitHub PAT was leaked and invalidated; Waiting for Linder to provide new PAT; Local elle_agent implementation ready in workspace; Roaringmoon active on other tasks (multi-agent architecture docs, TOWS video) [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-27.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-29.md:9:9 -->
- Blocked: task_20260623_elle_08_agent_impl blocked on task_06 (mrmime/roaringmoon) [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-29.md:9-9]
