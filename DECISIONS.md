# Decision Log
 
Every significant decision made during this project - what I picked, why, and what I ruled out.
 
---
 
## [March 2026] Switched from Debian to Ubuntu Server 24.04 LTS
 
**Decision:** Ubuntu Server 24.04 LTS
**Why:** Better documentation, bigger community, more relevant to DevOps job postings. Most tutorials and resources assume Ubuntu so it just makes more sense at this stage.
**Ruled out:** Debian - more stable and minimal but the learning curve cost wasn't worth it when Ubuntu has better support.
 
---
 
## [March 2026] Chose Podman over Docker
 
**Decision:** Podman
**Why:** More secure - no root-level daemon running in the background. Commands are identical to Docker so everything I learn transfers directly.
**Ruled out:** Docker - bigger community but Podman's Docker compatibility makes that gap basically irrelevant.
 
---
 
## [March 2026] Purged Podman / Installed Docker
 
**Decision:** Switch to Docker instead of Podman.
**Why:** Connection issues with Portainer when using Podman - rootless mode + Ubuntu isn't officially supported.
**Ruled out:** Continuing to troubleshoot Podman/Portainer compatibility - the time cost outweighed any security benefit at this stage of the project.
 
---
 
## [March 2026] Installed Portainer
 
**Decision:** Portainer for container management UI.
**Why:** Allows me to start and stop containers, read logs, inspect what's happening inside containers, and deploy new stacks - all without touching the CLI every time.
**Ruled out:** CLI-only management - fine for simple tasks but harder to get a quick overview of what's running.
 
---
 
## [March 2026] Installed DBeaver / Connected Postgres
 
**Decision:** DBeaver as the database management tool.
**Why:** Allows me to manage my Postgres database from my local machine with a full GUI.
**Ruled out:** pgAdmin - DBeaver supports multiple database types so it's more versatile long term. pgAdmin is PostgreSQL only.
 
---
 
## [March 2026] CLAUDE.md goes in individual project repos, not the top level README
 
**Decision:** Every project repo gets its own CLAUDE.md as standing instructions for Claude Code.
**Why:** CLAUDE.md is for Claude Code, not for humans reading the repo. Mixing the two audiences in one file is messy.
**Ruled out:** Nothing - this is just a clean separation of concerns.
 
---
 
## [March 2026] README stays current, history lives elsewhere
 
**Decision:** README reflects current state only. DECISIONS.md holds the reasoning. journal.md holds the running log.
**Why:** A README full of "we used to do X" is harder to read and worse as a portfolio piece. Each file has one job.
**Ruled out:** Changelog inside the README - that works for versioned libraries, not a living infrastructure project.
 
---
 
## [March 2026] Built a personal finance bot
 
**Decision:** Build a dedicated finance bot using Anthropic API + PostgreSQL.
**Why:** Needed a real project to learn API integration, database persistence, and conversation management. Finance coaching tied to a real goal and a practical use case I'll actually use.
**Ruled out:** Using a generic chatbot - no persistence, no project-specific learning.
 
---
 
## [March 2026] Sliding window for finance bot context
 
**Decision:** 20-message sliding window (10 exchanges) on the finance bot.
**Why:** Without it, every conversation sends the entire history to the API. The window queries the last 20 messages from PostgreSQL using a DESC/ASC subquery pattern. Full history stays in the database, nothing is lost.
**Ruled out:** Sending full history - token costs compound fast with long conversations.
 
---
 
## [April 2026] Chose Hermes Agent over OpenClaw
 
**Decision:** Hermes Agent as the agent platform.
**Why:** Python-based. Native cron scheduling with per-job model/provider overrides - critical for overnight monitoring with local models. Built-in Honcho memory integration. Native Anthropic provider with prompt caching.
**Ruled out:** OpenClaw - more mature, bigger community, but Node.js-based which I'm less comfortable hacking on. Both support Telegram, Discord, Anthropic, and self-hosting. OpenClaw is a strong project but Hermes fits my stack better. The migration path means this isn't a one-way door.
 
---
 
## [April 2026] Herman as Chief of Staff
 
**Decision:** Named the agent Herman, role is Chief of Staff.
**Why:** Chief of Staff signals strategic thinking, opportunity identification, and proactive management. I want him thinking ahead and surfacing opportunities, not just executing tasks.
**Ruled out:** Senior Architect - too narrow, implies only technical decisions.
 
---
 
## [April 2026] Ollama on Windows desktop for local inference
 
**Decision:** Run Ollama with Qwen3 8B on the Windows desktop GPU as a secondary inference provider.
**Why:** 8GB VRAM enables GPU-accelerated inference for 7-8B models. The Bee's AMD GPU can't do CUDA, so CPU-only inference there would be slow. The Windows PC is on the same LAN so The Bee just calls it over the network. Background and cron tasks run on the local model for free. Interactive work stays on Claude Sonnet for quality. If the Windows PC is off, Hermes falls back to Anthropic automatically.
**Ruled out:** Running Ollama on The Bee - AMD GPU means CPU-only inference, too slow. Running everything on Anthropic - works but costs add up for automated tasks.
 
---
 
## [April 2026] Telegram as primary messaging channel
 
**Decision:** Telegram for Herman's messaging interface.
**Why:** Telegram was designed around bots - setup is trivial, bots get dedicated DM threads, notifications are clean.
**Ruled out:** Discord - more overhead to set up, noisier notification model, primarily designed for communities not personal bots.
 
---
 
## [April 2026] Edge TTS over premium TTS providers
 
**Decision:** Edge TTS for text-to-speech.
**Why:** Free, no API key needed, quality is good enough for the use case.
**Ruled out:** ElevenLabs and OpenAI TTS - both cost money and quality difference doesn't justify it.
 
---
 
## [April 2026] Model routing strategy
 
**Decision:** Three-tier model routing - Claude Haiku for conversation, Claude Sonnet for deep reasoning, Ollama/qwen3:8b for all automated and background tasks.
**Why:** Automated tasks running on the Anthropic API would burn tokens silently around the clock. Local inference is free once the hardware is running. Haiku handles conversational back-and-forth cheaply. Sonnet is reserved for decisions that warrant it - market analysis, complex reasoning, anything touching money.
**Ruled out:** Using Sonnet for everything - quality is great but cost is unsustainable for high-frequency automated work. Using Ollama for everything - local model quality isn't good enough for nuanced reasoning or financial decisions.
 
---
 
## [April 2026] Hindsight over flat Postgres memory
 
**Decision:** Hindsight (Vectorize) as Herman's memory system, replacing flat Postgres storage.
**Why:** Flat key-value memory in Postgres has no retrieval intelligence - you either load everything or search by exact match. Hindsight uses a four-tier knowledge hierarchy (Mental Models → Observations → World Facts → Experience Facts) with TEMPR retrieval (semantic similarity + BM25 + knowledge graph + temporal filtering) running in parallel. It knows *why* Herman believes something, not just *what* he believes. Zero cloud dependency - runs on The Bee, backed by the local Postgres instance with pgvector.
**Ruled out:** Continuing with flat Postgres memory - works at small scale but doesn't improve with use. Self-hosted Honcho - considered it but Hindsight is a more complete solution and already integrates with Hermes via the `hindsight-hermes` plugin.
 
---
 
## [April 2026] Systemd timers for GPU scheduling
 
**Decision:** Systemd timers to pause the Hindsight container during the market bot window (5:22am–8:00am CST weekdays).
**Why:** The RTX 2070 SUPER is shared between Hindsight memory consolidation and Ollama inference for the market bot. Hindsight consolidation locks the GPU and causes Ollama timeouts. A second GPU would solve this permanently but isn't worth the hardware cost right now. Systemd timers are reliable, composable with other service dependencies, and the pause/resume is a clean handoff.
**Ruled out:** Running both simultaneously - causes inference timeouts. Disabling Hindsight consolidation entirely - defeats the purpose of the memory system. Cron - systemd timers integrate better with service management and have proper dependency handling.
 
---
 
## [April 2026] CONSOLIDATION_MAX_SLOTS=0 workaround for Hindsight v0.4.22
 
**Decision:** Set `CONSOLIDATION_MAX_SLOTS=0` in the Hindsight container config.
**Why:** Hindsight v0.4.22 has a bug where consolidation runs in a broken state when slots are available. Setting this to 0 disables consolidation entirely until upgrading to v0.5.0, which has the fix.
**Ruled out:** Upgrading to v0.5.0 immediately - deferred until the market bot Ollama routing fix is confirmed stable. Don't want two moving parts changing at once.