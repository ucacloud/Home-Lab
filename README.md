# Home Lab - AI Agent Organization
 
## Overview
 
A self-hosted, always-on AI agent organization running on a dedicated mini PC ("The Bee"). One agent - Herman - talks to me via Telegram, manages the infrastructure, runs a trading copilot, delegates background work to local models, and learns over time through structured memory.
 
This is simultaneously a personal productivity system, an AI-assisted trading operation, and a hands-on DevOps/Platform Engineering training environment. The north star goal is financial independence for the household.
 
Everything runs on The Bee or the local network. All data stays at home.
 
-----
 
## Current Status
 
| Milestone | Status |
|-----------|--------|
| Hardware acquired and set up | ✅ Done |
| Ubuntu Server 24.04 LTS installed | ✅ Done |
| SSH access from Windows desktop | ✅ Done |
| Docker + Portainer running | ✅ Done |
| PostgreSQL with pgvector | ✅ Done |
| Hermes Agent (Herman) deployed | ✅ Done |
| Telegram bot connected | ✅ Done |
| Market bot + trading copilot | ✅ Done |
| Hindsight memory system | ✅ Done |
| Ollama local inference | ✅ Done |
| GPU scheduling (Hindsight/market bot) | ✅ Done |
| Market bot Ollama routing fix | 🔧 In progress |
| Multi-agent supervisor architecture | 🔲 Planned (needs 2nd GPU) |
| Land deal sourcing pipeline | 🔲 Planned |
| K3s Kubernetes migration | 🔲 Planned |
 
-----
 
## Hardware
 
| Component | Details |
|-----------|---------|
| **Server ("The Bee")** | Beelink SER5 MAX Mini PC |
| **CPU** | AMD Ryzen 7 7735HS (8C/16T, up to 4.75GHz, Zen 3+) |
| **RAM** | 24GB LPDDR5 6300MHz |
| **Storage** | 500GB M.2 PCIe 4.0 SSD (466GB usable, ~21GB used) |
| **Network** | 2.5G LAN - wired ethernet in use |
| **OS** | Ubuntu Server 24.04 LTS |
| **UPS** | APC Back-UPS 600 |
| **GPU (Desktop)** | NVIDIA RTX 2070 SUPER (8GB VRAM) via Ollama |
| **Desktop PSU** | EVGA 650 GS |
 
The Bee handles all services, containers, and agent orchestration. The Windows desktop provides GPU inference via Ollama over the LAN. Auto Power On is enabled so The Bee boots automatically after power loss.
 
-----
 
## Herman - The Agent
 
Herman is the Chief of Staff. I talk to him on Telegram. He manages infrastructure, runs trading operations, coordinates tasks, and has broad autonomy over infrastructure decisions while requiring explicit approval for financial decisions and new project builds.
 
```
Owner (Telegram)
        │
        ▼
┌─────────────────────────┐
│        Herman           │  ← The only agent I talk to.
│    Chief of Staff       │    Manages infrastructure, trading,
│                         │    and agent coordination.
│  Hermes Agent (v0.6.0)  │
└────────────┬────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐   ┌──────────────┐
│ Haiku   │   │   Ollama     │
│ Sonnet  │   │  qwen3:8b    │
│ (API)   │   │  (local GPU) │
└─────────┘   └──────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│          Shared infrastructure layer            │
│  PostgreSQL (pgvector) · Hindsight Memory       │
│  Docker · Telegram · systemd timers             │
└─────────────────────────────────────────────────┘
```
 
### Model Routing
 
| Task | Model | Reason |
|------|-------|--------|
| Direct conversation | Claude Haiku | Fast, conversational |
| Deep reasoning | Claude Sonnet | Complex analysis, money decisions |
| Automated/background tasks | Ollama qwen3:8b | Zero API cost |
| Memory processing | Ollama qwen3:8b | Fact extraction, consolidation |
 
**Hard rule:** Automated tasks must never hit the Anthropic API. Ollama handles all background work to prevent unintended token burns.
 
-----
 
## Memory System - Hindsight
 
Herman's memory runs on Hindsight (by Vectorize), a biomimetic agent memory system. Installed April 7, 2026 to replace flat Postgres memory storage.
 
**How it works:** Hindsight organizes knowledge into a four-tier hierarchy with clear priority during retrieval: Mental Models → Observations → World Facts → Experience Facts. Each tier tracks evidence chains so Herman knows *why* he believes something, not just *what* he believes.
 
**Retrieval** uses TEMPR - four search strategies running in parallel: semantic similarity, BM25 keyword matching, knowledge graph traversal, and temporal filtering.
 
**Current state:** 131+ nodes, 1,875+ links, 55+ synthesized observations. Runs as a Docker container on The Bee, backed by PostgreSQL with pgvector. Uses Ollama/qwen3:8b for all memory processing (fact extraction, entity resolution, consolidation). Zero cloud dependency for the memory layer.
 
**Integration:** The `hindsight-hermes` plugin hooks into Hermes Agent. Auto-recall injects relevant memories before every LLM call. Auto-retain stores conversations after every response. The plugin required a local patch to fix async event loop conflicts in Hermes gateway mode (sync hooks wrapped with raw HTTP via `requests` to bypass the client library's `asyncio.run_until_complete` issue).
 
**Bank configuration:**
- **Mission:** Chief of Staff for the home lab infrastructure and AI agent organization
- **Directives:** No trades without approval, route automated tasks to Ollama, log decisions to DECISIONS.md, strip sensitive details before GitHub pushes, no production changes without confirmation
- **Disposition:** Skepticism 3, Literalism 3, Empathy 3
 
-----
 
## Trading System
 
### Market Bot
 
A Python script (`market_bot.py`) that generates daily trading signals for a small options account.
 
**Schedule (automated via systemd timers):**
- 5:22am CST - Hindsight container pauses (frees GPU)
- 6:00am CST - Market bot runs analysis via Ollama
- 7:50am CST - Morning brief delivers picks to Telegram
- 8:00am CST - Hindsight container resumes
 
**Signal format:** Entry price, target, stop loss, confidence score, and specific option contract recommendations sized for a small account.
 
### Trading Copilot
 
A single-file frontend (`trading_copilot.html`) served on port 3000 with a Flask API backend (`market_advisor_api.py`) on port 5000.
 
**Features:**
- Time-weighted stop losses: 40% before 1pm ET, 25% 1-2pm, 15% after 2pm
- Checkpoint alerts at 11am, 1pm, 2:30pm, 3:45pm ET
- Hold/Fold advisor calling Haiku via Flask proxy
- Pulls morning picks from `market_plays` Postgres table
 
**Core trading rules (non-negotiable):**
- Hard stop loss at 40-50% drawdown - no exceptions
- Take profit at 50-75% gain - at least half off
- Everything closes by 2:30-3pm ET - no holding into close
- Expired worthless = hard failure state
- No entries after 2:30pm ET
- Max $20-30 per play, max 2-3 simultaneous positions
 
### Telegram Channels
 
- Market Bot Picks (morning signals)
- Trading Copilot Alerts (checkpoint notifications)
 
-----
 
## Deployed Services
 
| Service | Description | Schedule/Port |
|---------|-------------|---------------|
| `hermes-gateway` | Herman's Telegram bot (systemd service) | Always on |
| `market_bot.py` | Morning market analysis | 6:00am CST (systemd timer) |
| Morning brief delivery | Sends picks to Telegram | 7:50am CST (systemd timer) |
| `market_advisor_api.py` | Flask API for trading copilot | Port 5000 |
| `trading_copilot.html` | Trading copilot frontend | Port 3000 |
| `token_tracker.py` | API token usage tracking | Daily midnight (cron) |
| `api_usage_poller.py` | Hourly API usage polling | Hourly (cron) |
| Hindsight pause/resume | Frees GPU for market bot | 5:22am / 8:00am CST (systemd timers) |
 
-----
 
## Tech Stack
 
| Layer | Technology |
|-------|------------|
| OS | Ubuntu Server 24.04 LTS |
| Containers | Docker + Portainer |
| Agent framework | Hermes Agent v0.6.0 (NousResearch) |
| Agent memory | Hindsight v0.4.22 (Vectorize) |
| AI API | Anthropic Claude (Haiku + Sonnet, pay-as-you-go) |
| Local inference | Ollama + qwen3:8b (RTX 2070 SUPER) |
| Database | PostgreSQL 18.3 (pgvector/pgvector:pg18) |
| Remote access | SSH + VS Code Remote |
| DB management | DBeaver (from Windows desktop) |
| Version control | GitHub |
| Messaging | Telegram |
 
-----
 
## Database
 
Single PostgreSQL instance running in Docker (`pgvector/pgvector:pg18`) with persistent volume storage.
 
**Databases:**
- `homelab` - primary database, all Herman and trading tables
- `hindsight` - Hindsight memory system (pgvector enabled)
- `hermes` - legacy, stale (candidate for removal)
 
**Key tables (homelab):**
`herman_memory`, `herman_conversations`, `herman_decisions`, `herman_tasks`, `market_plays`, `trades`, `account_stats`, `telegram_channels`, `closed_trades`, `api_token_usage`, `daily_spend_alerts`, `conversation_archives`
 
**Access:** Dedicated application role for agent access, superuser for administration.
 
-----
 
## GPU Resource Management
 
The RTX 2070 SUPER (8GB VRAM) is shared between Hindsight memory processing and the market bot. These cannot run simultaneously - Hindsight consolidation locks the GPU and causes Ollama inference timeouts for other callers.
 
**Solution:** Systemd timers pause the Hindsight container during the market bot window (5:22am-8:00am CST Mon-Fri). Outside this window, Hindsight has full GPU access for memory consolidation.
 
**Future fix:** A second GPU (targeting RTX 3090, 24GB VRAM) would eliminate contention entirely and enable running Gemma 4 26B MoE for near-Sonnet quality at zero API cost. This requires a PSU upgrade from the current EVGA 650 GS to 850W+.
 
-----
 
## Documentation Pattern
 
Three files, all written in first person:
 
- **README.md** - current state only (this file)
- **DECISIONS.md** - architectural decisions with reasoning and what was ruled out
- **journal.md** - running build/break/learn log
 
Sensitive details (IPs, usernames, bot names, identifiers) are stripped before GitHub pushes. Internal configs managed via `.env` and systemd overrides.
 
-----
 
## Security
 
- SSH key authentication only - password login disabled
- All data processed locally; Anthropic API does not train on API data
- Hindsight memory stored on-machine in PostgreSQL
- Hard API spending cap set in Anthropic console
- Each agent and database role operates with minimum required permissions
- Sensitive config in systemd overrides and `.env` files, not in code
 
-----
 
## Cost
 
| Item | Cost |
|------|------|
| Beelink SER5 MAX | $460 |
| APC Back-UPS 600 | ~$70 |
| **Hardware total** | **~$530** |
| Hermes Agent | Free (open source) |
| Hindsight | Free (open source, self-hosted) |
| Ollama | Free (open source) |
| Anthropic API (monthly) | ~$10-20/month |
 
-----
 
## Career Context
 
This project builds the exact skills that Platform Engineering, DevOps, and analyst roles require - while producing something real and demonstrable.
 
**Primary target:** Analyst role in the energy sector (power grid operations / market settlements).
 
**Fallback path:** Platform Engineering / DevOps.
 
**Skills this project directly builds:** Linux server administration, containerization (Docker), remote system management via SSH, database administration (PostgreSQL + pgvector), API integration and cost management, multi-agent system design, AI memory architecture, GPU resource scheduling, and trading system design.
 
**Certifications roadmap:** AWS Cloud Practitioner → AWS Solutions Architect Associate → Docker Certified Associate → Certified Kubernetes Administrator (CKA).
 
**Kubernetes path (when ready):** K3s on The Bee once core stack is stable.
 
-----
 
## On the Horizon
 
- Verify market bot generates real picks with correct Ollama routing
- Build 2-3 week trading track record with logged results
- Weekly research cron (Herman analyzes sectors/macro during off-hours)
- Daily system health monitoring script
- Evaluate Gemma 4 26B MoE when GPU upgrade happens
- Land deal sourcing pipeline (scraper agents, analyst agent, Telegram alerts, buyer CRM)
- Multi-agent supervisor architecture (needs 2nd GPU)
- Hermes Agent update (deferred until memory system stable)
- Self-hosted Honcho replacement (complete - Hindsight replaces this)
- K3s Kubernetes migration
 
-----
 
## Resources
 
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - agent framework
- [Hindsight](https://github.com/vectorize-io/hindsight) - agent memory system
- [Ollama](https://ollama.com) - local model inference
- [Anthropic API Console](https://platform.anthropic.com) - model access and spending caps
- [Docker Documentation](https://docs.docker.com)
- [pgvector](https://github.com/pgvector/pgvector) - vector similarity for PostgreSQL
 
-----
 
*Started February 2026. Hindsight memory upgrade April 7, 2026.*