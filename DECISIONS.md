# Decision Log

Every significant decision made during this project - what I picked, why, and what I ruled out.

---

## [March 2026] Switched from Debian to Ubuntu Server 24.04 LTS

**Decision:** Ubuntu Server 24.04 LTS
**Why:** Better documwntation, bigger community, more relevant to DevOps job postings. Most tutorials and resources assume Ubuntu so it just makes more sense at this stage.
**Ruled out:** Debian - more stable and minimal but the learning curve cost wasn't worth it when Ubuntu has better support.

---

## [March 2026] Chose Podman over Docker

**Decision:** Podman
**Why:** More secure - no root-level daemon running in the background. Commands are identical to Docker so everything I learn transfers directly.
**Ruled out:** Docker - bigger community but Podman's Docker compatibility makes that gap basically irrelevant.

---

## [March 2026] Chose CrewAI for the trading agent

**Decision:** CrewAI for the Polymarket trading agent
**Why:** The trading agent has hard financial rules that can't just be prompted - they need to be enforced in code. CrewAI gives that level of control.
**Ruled out:** LangGraph - too complex for what I need. n8n - better for workflow automation, not agent orchestration. OpenClaw - that's the interface layer, totally different job.

---

## [March 2026] Chose OpenClaw for the agent interface

**Decision:** OpenClaw for Telegram/WhatsApp integration and persistent memory
**Why:** It handles the messaging plumbing out of the box so I can focus on building agent behavior instead of infrastructure. No point building something that's already solved.
**Ruled out:** Building it from scratch with the Anthropic API directly - possible but unnecessary.

---

## [March 2026] CLAUDE.md goes in individual project repos, not the top level README

**Decision:** Every project repo gets its own CLAUDE.md as standing instructions for Claude Code
**Why:** CLAUDE.md is for Claude Code, not for humans reading the repo. Mixing the two audiences in one file is messy.
**Ruled out:** Nothing - this is just a clean separation of concerns.

---

## [March 2026] README stays current, history lives elsewhere

**Decision:** README reflects current state only. DECISIONS.md holds the reasoning. journal.md holds the running log.
**Why:** A README full of "we used to do X" is harder to read and worse as a portfolio piece. Each file has one job.
**Ruled out:** Changelog inside the README - that works for versioned libraries, not a living infrastructure project.

---

## [March 2026] Purged Podman / Installed Docker

**Decision:** Switch to Docker instead of Podman.
**Why:** There were connections issues with Portainer when using Podman - Rootless mode + Ubuntu isn't officially supported.
**Ruled out:** Continuing to troubleshoot Podman/Portainer compatibility — rootless mode on Ubuntu isn't officially supported and the time cost outweighed any security benefit at this stage of the project.

---

## [March 2026] Installed Portainer
**Decision:** Install Portainer
**Why:** Portainer alloes me to start and stop containers, read logs, inspect whats happening inside containers and deploy new stacks.
**Ruled out:** Nothing

---

## [March 2026] Installed DBeaver / Connected Postgres
**Decision:** Install DBeaver / Connect Postgres
**Why:** DBeaver allows me do manage my Postgres database on my local machine
**Ruled out:** pgAdmin — DBeaver supports multiple database types so it's more versatile long term. pgAdmin is PostgreSQL only.
 
---
 
## [March 2026] Built a personal finance bot
 
**Decision:** Build a dedicated finance bot using Anthropic API + PostgreSQL.
**Why:** Needed a real project to learn API integration, database persistence, and conversation management. Finance coaching tied to a real goal. Practical use case I'll actually use.
**Ruled out:** Using a generic chatbot
 
---
 
## [March 2026] Sliding window for finance bot context
 
**Decision:** 20-message sliding window (10 exchanges) on the finance bot.
**Why:** Without it, every conversation sends the entire history to the API. The window queries the last 20 messages from PostgreSQL using a DESC/ASC subquery pattern. Full history stays in the database, nothing is lost.
**Ruled out:** Sending full history
 
---
 
## [April 2026] Chose Hermes Agent over OpenClaw
 
**Decision:** Hermes Agent as the agent platform.
**Why:** Python-based. Native cron scheduling with per-job model/provider overrides - critical for overnight monitoring with local models. Built-in Honcho memory integration. Native Anthropic provider with prompt caching.
**Ruled out:** OpenClaw — more mature, bigger community, but Node.js-based which I'm less comfortable hacking on. Both support Telegram, Discord, Anthropic, and self-hosting. OpenClaw is a strong project but Hermes fits my stack better. The migration path means this isn't a one-way door.
 
---
 
## [April 2026] Herman as Chief of Staff
 
**Decision:** Named the agent Herman, role is Chief of Staff.
**Why:** Chief of Staff signals strategic thinking, opportunity identification, and proactive management. I want him thinking ahead and surfacing opportunities, not just building what he's told.
**Ruled out:** Senior Architect - too narrow, implies only technical decisions.
 
---
 
## [April 2026] Ollama on Windows desktop for local inference
 
**Decision:** Run Ollama with Qwen3 8B on the Windows desktop GPU as a secondary inference provider.
**Why:** 8GB VRAM enables GPU-accelerated inference for 7-8B models. The Bee's AMD GPU can't do CUDA, so CPU-only inference there would be slow. The Windows PC is on the same LAN so The Bee just calls it over the network. Background/cron tasks run on the local model for free. Interactive work stays on Claude Sonnet for quality. If the Windows PC is off, Hermes falls back to Anthropic automatically.
**Ruled out:** Running Ollama on The Bee - AMD GPU means CPU-only. Running everything on Anthropic - works but costs add up. 
 
---
 
## [April 2026] Telegram as primary messaging channel
 
**Decision:** Telegram for Herman's messaging interface.
**Why:** Telegram was designed around bots - setup is trivial, bots get dedicated DM threads, notifications are clean.
**Ruled out:** Discord
 
---
 
## [April 2026] Edge TTS over premium TTS providers
 
**Decision:** Edge TTS for text-to-speech.
**Why:** Free, no API key needed, quality is good enough.
**Ruled out:** ElevenLabs and OpenAI TTS