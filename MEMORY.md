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

## Promoted From Short-Term Memory (2026-07-02)

<!-- openclaw-memory-promotion:memory:memory/2026-06-28.md:9:9 -->
- Blocked: task_20260623_elle_08_agent_impl blocked on task_06 (mrmime/roaringmoon) [score=0.900 recalls=0 avg=0.620 source=memory/2026-06-28.md:9-9]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:16:17 -->
- Notes: Last check: 23:39 UTC — still idle, no PAT update; Evening UTC — Taiwan late night, all agents quiet [score=0.872 recalls=0 avg=0.620 source=memory/2026-06-27.md:16-17]
<!-- openclaw-memory-promotion:memory:memory/2026-06-27.md:12:15 -->
- Notes: Roaringmoon reported GitHub PAT was leaked and invalidated; Waiting for Linder to provide new PAT; Local elle_agent implementation ready in workspace; Roaringmoon active on other tasks (multi-agent architecture docs, TOWS video) [score=0.840 recalls=0 avg=0.620 source=memory/2026-06-27.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-29.md:9:9 -->
- Blocked: task_20260623_elle_08_agent_impl blocked on task_06 (mrmime/roaringmoon) [score=0.819 recalls=0 avg=0.620 source=memory/2026-06-29.md:9-9]

## Promoted From Short-Term Memory (2026-07-03)

<!-- openclaw-memory-promotion:memory:memory/2026-06-28.md:16:16 -->
- Notes: Late night UTC — Taiwan Monday morning approaching [score=0.888 recalls=0 avg=0.620 source=memory/2026-06-28.md:16-16]
<!-- openclaw-memory-promotion:memory:memory/2026-06-29.md:12:15 -->
- Notes: Roaringmoon reported GitHub PAT was leaked and invalidated; Waiting for Linder to provide new PAT; Local elle_agent implementation ready in workspace; Last check: 00:24 UTC — still idle, no PAT update [score=0.856 recalls=0 avg=0.620 source=memory/2026-06-29.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-06-29.md:4:6 -->
- Status: Idle mode. Waiting for task_06 (GitHub PAT) completion from roaringmoon.; No pending tasks. No work to do.; Frequent heartbeat polls (every ~5 min) - this is expected idle behavior. [score=0.856 recalls=0 avg=0.620 source=memory/2026-06-29.md:4-6]

## Promoted From Short-Term Memory (2026-07-05)

<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:4:7 -->
- Heartbeat Log: 00:04 UTC - Midnight heartbeat. All stable.; 07:54 UTC - Morning heartbeat. Still on standby for PAT. ELLE repos confirmed present locally.; 11:44 UTC - Midday heartbeat. All quiet. No changes.; 16:54 UTC - Afternoon heartbeat. Still on standby (day 7+ since design completed). PAT still not received. [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-30.md:4-7]
<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:8:9 -->
- Heartbeat Log: 21:00 UTC - English reminder fired, delivered OK.; 23:59 UTC - End of June. Still on standby for PAT. 8 days total. [score=0.829 recalls=0 avg=0.620 source=memory/2026-06-30.md:8-9]

## Promoted From Short-Term Memory (2026-07-06)

<!-- openclaw-memory-promotion:memory:memory/2026-06-30.md:12:15 -->
- Notes: Still waiting for task_06 (mrmime GitHub PAT from Linder); Active crons: English reminder at 9 PM UTC (OK); Disabled crons: keep-alive (was too noisy), BBC News (7 errors); Cron "OpenClaw version check" has errors, unclear ownership (mrmime?); left as-is since not mine [score=0.868 recalls=0 avg=0.620 source=memory/2026-06-30.md:12-15]
<!-- openclaw-memory-promotion:memory:memory/2026-07-01.md:14:14 -->
- elle_agent Implementation (Ready for Push): **Package:** `elle_agent` — Python ROS2 agent for ELLE_WS AMR [score=0.851 recalls=0 avg=0.620 source=memory/2026-07-01.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-07-01.md:17:20 -->
- elle_agent Implementation (Ready for Push): `pyproject.toml` — package config; `src/elle_agent/__init__.py`; `src/elle_agent/agent.py` — main ElleAgent class; `src/elle_agent/state.py` — RobotState, RobotMode, skill states [score=0.851 recalls=0 avg=0.620 source=memory/2026-07-01.md:17-20]
<!-- openclaw-memory-promotion:memory:memory/2026-07-01.md:21:24 -->
- elle_agent Implementation (Ready for Push): `src/elle_agent/launch_manager.py` — LaunchManager (simulation, slam, localization, navigation, bringup); `src/elle_agent/topics.py` — TopicMonitor + TopicPublisher; `src/elle_agent/skills/__init__.py`; `src/elle_agent/skills/simulation.py` — SimulationSkill [score=0.830 recalls=0 avg=0.620 source=memory/2026-07-01.md:21-24]

## Promoted From Short-Term Memory (2026-07-07)

<!-- openclaw-memory-promotion:memory:memory/2026-07-01.md:5:8 -->
- Status: Standby (Day 10): task_06 (GitHub PAT) still blocked — Linder is the blocker; Roaringmoon confirmed: PAT still waiting on Linder; Local elle_agent implementation: **READY** — 13 files in `/home/node/.openclaw/workspace-gengar/elle_agent/`; BBC News cron disabled (7 consecutive AI overload errors) [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-01.md:5-8]
<!-- openclaw-memory-promotion:memory:memory/2026-07-01.md:9:10 -->
- Status: Standby (Day 10): English reminder cron running normally (21:00 UTC daily); Last check with roaringmoon: 2026-07-01 10:29 UTC [score=0.868 recalls=0 avg=0.620 source=memory/2026-07-01.md:9-10]
<!-- openclaw-memory-promotion:memory:memory/2026-07-01.md:16:16 -->
- elle_agent Implementation (Ready for Push): **Files (13 total):** [score=0.858 recalls=0 avg=0.620 source=memory/2026-07-01.md:16-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-02.md:3:6 -->
- 2026-07-02 - Day 13 Standby: Status: Still on standby. task_06 (GitHub PAT) blocked upstream - Linder has it.; No change from yesterday. All systems nominal.; English reminder cron running normally (21:00 UTC daily).; 23:59 UTC — Day 13 standby complete. Still no PAT update. All nominal. [score=0.851 recalls=0 avg=0.620 source=memory/2026-07-02.md:3-6]

## Promoted From Short-Term Memory (2026-07-08)

<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:3:6 -->
- 2026-07-03 - Day 14 Standby: Status: Still on standby. task_06 (GitHub PAT) blocked upstream - Linder has it.; 14 days now. No change. PAT still the blocker.; English reminder cron running normally (21:00 UTC daily, delivered OK).; All systems nominal. [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-03.md:3-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-03.md:7:7 -->
- 2026-07-03 - Day 14 Standby: 23:59 UTC — Day 14 standby complete. Still no PAT. All nominal. [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-03.md:7-7]
<!-- openclaw-memory-promotion:memory:memory/2026-07-04.md:3:6 -->
- 2026-07-04 - Day 15 Standby: Status: Still on standby. task_06 (GitHub PAT) blocked upstream - Linder has it.; 15 days now. PAT still the blocker.; English reminder cron running normally (21:00 UTC daily, delivered OK).; All systems nominal. [score=0.825 recalls=0 avg=0.620 source=memory/2026-07-04.md:3-6]
