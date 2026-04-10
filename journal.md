# Journal
 
A running log of what I built, what broke, and what I learned.
 
---
 
## [March 2026] Getting the Bee online
 
**What I was trying to do:**
Get Ubuntu Server installed and SSH working so I could manage everything remotely from my Windows desktop.
 
**What happened:**
First attempt at flashing the USB was with Rufus 4.63 - had issues. Switched to balenaEtcher and that worked.
 
Bigger problem was the network. The Bee had no WiFi or ethernet drivers out of the box which created a dependency loop. I needed internet to install drivers but needed drivers to get internet. Plugging in an ethernet cable didn't work either because the driver wasn't there yet.
 
Fix: connected my phone via USB-C and used it as a hotspot to give the Bee internet access. That broke the loop. I was able to download and install the network drivers, finish the Ubuntu Server setup, and get everything configured.
 
**SSH issue:**
Plain `ssh` wasn't working initially. Had to run:
`ssh -o StrictHostKeyChecking=accept-new`
This tells SSH to automatically trust and save the Bee's fingerprint on first connection. Works normally after that first handshake.
 
**What I learned:**
- Always have an ethernet cable ready before starting a server install - WiFi only creates a dependency loop
- balenaEtcher over Rufus for USB flashing
- StrictHostKeyChecking=accept-new is the fix when SSH refuses first connection
 
---
 
## [March 2026] Setting up the repo and dev environment
 
**What I was trying to do:**
Get a GitHub repo created, cloned onto the Bee, and VS Code on Windows connected so I could work in a familiar environment.
 
**What happened:**
Repo creation was straightforward. Cloning onto the Bee was simple. VS Code Remote SSH extension connects directly into the Bee - the file explorer and terminal in VS Code are actually running on the Bee, not on Windows. Nothing needs to be installed on the Windows machine except VS Code itself.
 
**Git credentials issue:**
Pushing from the bash terminal kept failing with invalid token errors even with the correct token. VS Code terminal worked because it inherited Windows credentials automatically. Fixed it by embedding the token directly in the remote URL:
`git remote set-url origin https://<username>:<token>@github.com/<username>/<repo>.git`
 
**What I learned:**
- VS Code Remote SSH is just a window into the Bee - everything runs on the Bee, Windows is just the screen
- GitHub no longer accepts passwords for git operations - Personal Access Token required
- When token auth keeps failing, embed it directly in the remote URL
- `git config --global user.email` and `git config --global user.name` need to be set before first commit on a fresh machine
 
---
 
## [March 2026] Installed Podman
 
**What I did:**
Installed Podman 4.9.3 via apt. Verified with hello-world container.
 
**What I learned:**
- `sudo apt install podman -y` broken down: sudo = run as admin, apt = package manager, install = action, podman = package name, -y = auto confirm
- Podman runs Docker images natively - the whole Docker Hub library works out of the box
- "Hello from Docker" in the output is just hardcoded text inside the image itself, not an error. Podman pulled and ran it correctly.
 
---
 
## [March 2026] Purged Podman / Installed Docker
 
**What I did:**
Purged Podman / installed Docker 29.3.0. Verified with hello-world container.
 
**What I learned:**
- When I attempted to create a new Podman connection in Portainer, there was a note that mentioned "Rootless mode + Ubuntu not officially supported".
- I tried to do a permission fix and system reboot but it didn't resolve the issue.
- Decided to move forward with the project and use Docker instead since the 'risk' is almost negligible.
 
---
 
## [March 2026] Installed and setup Portainer
 
**What I was trying to do:**
Get Portainer linked to Docker so that I can monitor it.
 
**What I did:**
Installed Portainer, connected it to my local machine and was able to view my Docker from the Portainer dashboard.
 
**What I learned:**
- Portainer can allow me to start and stop containers, read logs, inspect what's happening inside containers and deploy new stacks.
 
---
 
## [March 2026] Created a simple bot
 
**What I was trying to do:**
Get a foundational understanding of how to make a simple Claude bot.
 
**What I did:**
Got an API key from Anthropic, built a simple bot that acts on a loop to answer any questions and exits when the user types 'quit'.
 
**What I learned:**
- How to designate which model to use
- Set a usage rate limit
- Save the conversation history to an array
- Store API keys in .env and reference with os.getenv() - never hardcode credentials
 
---
 
## [March 2026] Installed DBeaver / Connected Postgres
 
**What I was trying to do:**
Get access to my Postgres database.
 
**What I did:**
Installed DBeaver and connected it to my Postgres database.
 
**What I learned:**
- How to connect my database to DBeaver and what credentials were needed.
 
---
 
## [March 2026] Built the personal finance bot
 
**What I was trying to do:**
Build a dedicated financial advisor bot that keeps conversations in PostgreSQL and coaches toward financial freedom.
 
**What I did:**
Built the finance bot using Claude Sonnet with PostgreSQL-backed persistent memory. Tuned the system prompt for financial coaching. Added a 20-message sliding window to manage token costs. Full history stays in PostgreSQL but only the recent window goes to the API.
 
**What I learned:**
- How to connect Python to PostgreSQL via psycopg2
- The sliding window pattern for token management - save everything, send only what's needed
- System prompt design matters - specific principles produce better coaching than generic instructions
- Conversation history needs to be in chronological order for the API, even when you query in reverse
 
---
 
## [April 2026] Installed Hermes Agent and got Herman running
 
**What I was trying to do:**
Set up an always-on AI agent accessible from my phone that could eventually run overnight jobs, manage projects, and coordinate other bots.
 
**What I did:**
Decided between OpenClaw and Hermes. Chose Hermes - created a SOUL.md with the Chief of Staff role, communication rules, full project context, and cost management instructions. Tested on Telegram, follows the SOUL.md personality, and is reachable from my phone.
 
**What I learned:**
- Hermes Agent is a full platform
- SOUL.md loads fresh every message
- `/reset` clears the session context but Honcho memory persists across resets
- System-level systemd service needs `sudo $(which hermes)` because sudo doesn't inherit the user's PATH
 
---
 
## [April 2026] Set up Ollama on Windows desktop for local inference
 
**What I was trying to do:**
Get a local model running on my Windows PC's GPU so background tasks and cron jobs can run for free instead of burning API credits.
 
**What I did:**
Installed Ollama on Windows, pulled Qwen3 8B (~5.2GB). Tested in command prompt the model runs and responds. Set the OLLAMA_HOST environment variable so it accepts connections from the LAN. Verified from The Bee that it can see the model. Registered it as a custom endpoint in Hermes. Both providers work - Claude Sonnet for interactive, Ollama for background.
 
**What I learned:**
- Ollama exposes an OpenAI-compatible API at port 11434 by default
- By default it only listens on localhost - need the OLLAMA_HOST environment variable set to 0.0.0.0 to accept LAN connections
- Qwen3 8B fits in 8GB VRAM at Q4 quantization
- Windows sleep must be set to Never or Ollama becomes unreachable from the network
- Local model quality is noticeably lower than Claude Sonnet
- If the Windows PC is off, Hermes falls back to Anthropic automatically
 
---
 
## [April 2026] Built the market bot and trading copilot
 
**What I was trying to do:**
Get daily trading signals delivered to Telegram automatically, and build a dashboard I can use during market hours to manage positions.
 
**What I did:**
Built `market_bot.py` to generate morning picks for a small Robinhood cash account. Signals include entry price, target, stop loss, confidence score, and specific option contract recommendations with premiums affordable on a small account. Set up systemd timers to run analysis at 6am CST and deliver the morning brief to Telegram at 7:50am CST.
 
Built the trading copilot as a single-file frontend (`trading_copilot.html`) on port 3000 with a Flask API backend (`market_advisor_api.py`) on port 5000. The copilot pulls morning picks from the `market_plays` Postgres table, runs checkpoint alerts at 11am/1pm/2:30pm/3:45pm ET, and has time-weighted stop losses that tighten as the day goes on (40% before 1pm, 25% 1-2pm, 15% after 2pm). Added a Hold/Fold advisor that calls Haiku via the Flask proxy to give a quick read on whether to stay in a position.
 
Set up two Telegram channels - one for morning picks, one for intraday alerts.
 
**Core rules I coded in as non-negotiable:**
- Hard stop at 40-50% drawdown, no exceptions
- Take profit at 50-75% gain - at least half off the table
- Everything closes by 2:30-3pm ET
- No entries after 2:30pm ET
- Max $20-30 per play, max 2-3 positions at once
 
**What I learned:**
- Flask + CORS is the right pattern for a single-file HTML frontend calling a local API
- Time-weighted risk rules actually encode real trading discipline - the closer to close, the less time for a loser to recover
- Checkpoint alerts are more useful than a continuous feed - they force a structured decision at set times instead of constant noise
- Storing picks in Postgres makes them available to multiple services (the frontend, Herman, future analytics)
 
---
 
## [April 2026] Discovered market bot was calling Anthropic API instead of Ollama
 
**What happened:**
Found out the market bot was hitting the Anthropic API during its automated 6am run instead of routing to Ollama. This was burning tokens every morning without me realizing it - directly violating the hard rule that automated tasks must never touch the API.
 
**What I did:**
Tasked Herman with diagnosing and fixing the routing bug before touching anything else. The issue was in how the provider was configured for the cron/systemd context vs. interactive context.
 
**What I learned:**
- Model routing bugs are silent - they don't throw errors, they just cost money
- The hard rule (Ollama for all automated tasks) needs to be enforced at the code level, not just the config level
- Always verify which provider is actually being called in automated runs, not just in interactive testing
- Systemd service environments don't inherit the same environment variables as a normal shell session - this can silently break provider selection
 
---
 
## [April 2026] Installed Hindsight memory system
 
**What I was trying to do:**
Replace flat Postgres memory storage with something that actually understands context and can retrieve relevant information intelligently.
 
**What I did:**
Installed Hindsight (by Vectorize) as a Docker container on The Bee. Configured it against the `hindsight` Postgres database with pgvector enabled. Installed the `hindsight-hermes` plugin to hook into Hermes Agent. Auto-recall injects relevant memories before every LLM call; auto-retain stores conversations after every response.
 
Configured the bank with Herman's mission, directives, and disposition (Skepticism 3, Literalism 3, Empathy 3).
 
Hit an async event loop conflict in Hermes gateway mode - the Hindsight client library was using `asyncio.run_until_complete` which conflicts with the running event loop. Fixed it by patching the sync hooks to use raw HTTP via `requests` instead of the client library.
 
The GPU contention issue came up immediately: Hindsight consolidation locks the GPU and causes Ollama inference timeouts during the market bot window. Solved with systemd timers - Hindsight pauses at 5:22am CST and resumes at 8:00am CST on weekdays.
 
**Current state at install:** 131+ nodes, 1,875+ links, 55+ synthesized observations.
 
**What I learned:**
- Hindsight's four-tier hierarchy (Mental Models → Observations → World Facts → Experience Facts) is a real improvement over flat key-value memory - retrieval is context-aware, not just keyword matching
- TEMPR search (semantic similarity + BM25 + knowledge graph + temporal filtering) running in parallel means it finds relevant memories even when the wording doesn't match
- Async conflicts in Python are subtle - when a library internally calls `asyncio.run_until_complete`, it fails if there's already a running loop. Raw HTTP is the escape hatch.
- GPU contention between inference and memory consolidation is a real scheduling problem, not just a theoretical one. Systemd timers are the right tool for hard time-based resource handoffs.
- A dedicated database for the memory system (`hindsight`) is the right call - keeps it isolated from the application database
 
---
 
## [April 2026] Upgraded Hermes to v0.8.0, confirmed Hindsight docker run command
 
**What I did:**
Upgraded Hermes Agent to v0.8.0. Locked in the confirmed working docker run command for Hindsight with all the key env vars:
 
- `DB=postgresql://<user>:<password>@host.docker.internal:5432/hindsight`
- `LLM_BASE_URL=http://[desktop-ip]:11434/v1`
- `MODEL=qwen3:8b`
- `CONSOLIDATION_MAX_SLOTS=0` - disables the buggy consolidation behavior in v0.4.22
 
Hindsight v0.5.0 upgrade is on the radar but deferred until the market bot routing fix is confirmed stable.
 
**What I learned:**
- `CONSOLIDATION_MAX_SLOTS=0` is the workaround for the v0.4.22 consolidation bug - without it, consolidation runs in a broken state
- `host.docker.internal` is the right hostname for a Docker container to reach services on the host machine (or the Windows desktop via LAN routing)
- Always save the working docker run command somewhere permanent before iterating - losing a confirmed working config is expensive to reconstruct