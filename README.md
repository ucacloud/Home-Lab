# Home Lab — AI Agent Organization

## Overview

A self-hosted, always-on AI agent organization running on a dedicated mini PC. The goal is to run a small AI company from a single box — a senior architect agent that talks to me, delegates to specialized worker agents, spawns new agents when needed, and manages a live dashboard so I can see exactly what the org is doing at any moment.

This is simultaneously a personal productivity system, an autonomous trading agent with strict guardrails, and a hands-on DevOps/Platform Engineering training environment aimed at a career transition into a $200k+ remote role.

Everything runs on the Beelink. Nothing is farmed out to SaaS. All data stays at home.

-----

## Current Status

| Milestone | Status |
|-----------|--------|
| Hardware acquired and set up | ✅ Done |
| Ubuntu Server 24.04 LTS installed | ✅ Done |
| SSH access from Windows desktop | ✅ Done |
| Docker installed | ✅ Done |
| Portainer running | ✅ Done |
| PostgreSQL container | 🔲 Planned |
| Financial advisor bot | 🔲 Planned |
| Polymarket trading agent | 🔲 Planned |
| Agent dashboard website | 🔲 Planned |

-----

## Documentation Approach

This repo is maintained as a live record of the project — not a retrospective writeup.

- **README** — always reflects current state. No history, no "we used to do X."
- **DECISIONS.md** — every significant pivot or architectural choice is logged here with the reasoning and tradeoffs considered.
- **journal.md** — running log of what was built, what broke, and what was learned.
- **Git history** — commit messages are written to tell the story. Each pivot is committed before and after with context.

-----

## Hardware

|Component   |Details                                                 |
|------------|--------------------------------------------------------|
|**Device**  |Beelink SER5 MAX Mini PC                                |
|**CPU**     |AMD Ryzen 7 7735HS (8C/16T, up to 4.75GHz, Zen 3+)      |
|**RAM**     |24GB LPDDR5 6300MHz                                     |
|**Storage** |500GB M.2 PCIe 4.0 SSD (2x M.2 slots, expandable to 4TB)|
|**Network** |WiFi 6 / 2.5G LAN — wired ethernet in use               |
|**OS**      |Ubuntu Server 24.04 LTS                                 |
|**UPS**     |APC Back-UPS 600                                        |
|**Location**|Home network                        |

**Physical setup notes:**

- Beelink is managed remotely via SSH.
- Ethernet is the primary connection. WiFi is available but not relied on.
- Auto Power On enabled — machine boots automatically after any power loss.

**Current status:** Ubuntu Server 24.04 LTS installed. SSH access from Windows desktop confirmed working.

-----

## The Agent Organization

The core concept is a multi-agent hierarchy that operates like a small company. I talk to one agent. That agent runs the rest.

```
You (Telegram / WhatsApp)
        │
        ▼
┌─────────────────────────┐
│     Senior Architect    │  ← The only agent you talk to directly.
│                         │    Understands goals, makes plans,
│   Claude Sonnet         │    delegates work, hires new agents
└────────────┬────────────┘    when needed.
             │
             ▼
┌─────────────────────────┐
│    Organizer / PM       │  ← Breaks tasks into pieces,
│                         │    assigns workers, tracks progress,
│   Claude Haiku          │    reports back to architect.
└──────┬──────────────────┘
       │
  ┌────┴──────────────────────────────────────┐
  │           Worker agents (spawned on demand) │
  │                                             │
  │  Researcher  Analyst  Writer  Coder  +New  │
  │  (web/data)  (numbers) (drafts) (scripts)  │
  └─────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│          Shared memory + tools layer            │
│  PostgreSQL · filesystem · email · Telegram     │
│  Anthropic API · Polymarket API                 │
└─────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│         Agent dashboard — the office            │
│  Live website showing every agent, their        │
│  current task, and new hires spawning in        │
└─────────────────────────────────────────────────┘
```

**How hiring works:** The architect recognizes when a task requires a capability that doesn’t exist yet, defines a new agent role with specific tools and instructions, and spawns it dynamically via CrewAI. The dashboard shows the new hire appearing in the office. When the task is done, temporary agents can be stood down.

**How CLAUDE.md fits in:** Each project repo contains a CLAUDE.md file — a standing order document that tells Claude Code how to behave when working in that repo. The architect’s CLAUDE.md enforces: plan before acting, use subagents, verify before marking complete, capture lessons from mistakes. The trading agent’s CLAUDE.md adds hard rules around financial guardrails.

-----

## Use Cases

### 1. Personal AI organization (OpenClaw)

OpenClaw is the interface layer — it handles the Telegram/WhatsApp connection, persistent memory across conversations, and the always-on presence that makes the architect feel like a coworker rather than a chatbot.

The org can be tasked with anything: research, writing, analysis, automation, scheduling. The architect figures out what’s needed and routes it. No SaaS subscriptions required — the org replaces most of them.

### 2. Personal financial advisor bot

A dedicated agent receives financial documents. The analyst agent reads and builds up a picture of spending patterns, income, recurring bills, and trends over time. On demand via Telegram: “how much did I spend on food last month?” or “what bills are coming up?” — answered from real data, not generic advice.

Constraints: read and analyze only, no financial transactions, no external cloud storage. All documents stay on the Beelink.

### 3. Polymarket Bitcoin trading agent

Monitors 5-minute Bitcoin markets on Polymarket. Uses Claude Haiku every 5 minutes for price monitoring (cheap, fast). Escalates to Claude Sonnet for actual bid decisions. Places autonomous bids within strict guardrails.

**Guardrails (non-negotiable):**

- Bitcoin price markets only — no political or unrelated markets
- Maximum bet size per position: TBD before going live
- Maximum total simultaneous exposure: TBD before going live
- Daily and weekly spending cap: TBD before going live
- No doubling down after losses
- Hard spending cap set in Anthropic console before any autonomous trading begins

Built with custom Python + CrewAI for precise control over guardrail logic. This is not a use case for an opinionated framework — the rules need to be exact.

### 4. Small business PostgreSQL database

Hosts a database for a small business. Future migration from Google Sheets. Managed remotely via DBeaver from the Windows desktop. Nightly automated backups to external drive.

### 5. Agent dashboard website

A live website showing the agent org in action. Built as a React frontend that polls the Beelink for agent status data. The pixel art office UI shows each agent as a character — typing when writing, reading when searching, speech bubble when waiting, matrix animation when a new hire spawns. Served via Caddy with SSL. Accessible from anywhere.

This is also a portfolio piece — a live demonstration of the entire stack working together.

### 6. Eryndor (game project)

A solo-developed game. Separate project, tracked in its own repo. Hosted on the Beelink eventually. AI tools are a core part of the solo dev workflow — art, content, and code generation collapse the cost of building alone.

-----

## Tech Stack

|Layer              |Technology                                               |
|-------------------|---------------------------------------------------------|
|OS                 |Ubuntu Server 24.04 LTS                                  |
|Containers         |Docker + Docker Compose                                  |
|Container UI       |Portainer                                                |
|Agent interface    |OpenClaw (openclaw.ai)                                   |
|Agent orchestration|CrewAI (open source, self-hosted)                        |
|Workflow automation|n8n (open source, self-hosted, free)                     |
|AI API             |Anthropic Claude (pay-as-you-go)                         |
|Database           |PostgreSQL                                               |
|Web / SSL          |Caddy + Let’s Encrypt                                    |
|Dashboard frontend |React                                                    |
|Remote access      |SSH from Windows Command Prompt                          |
|DB management      |DBeaver (from Windows desktop)                           |
|Disk encryption    |LUKS (future)                                            |
|IaC                |Ansible (future — document everything as you build)      |
|Kubernetes         |K3s on this Beelink (future — after core stack is stable)|

-----

## AI Model Routing

|Task                       |Model        |Reason                                 |
|---------------------------|-------------|---------------------------------------|
|Senior architect           |Claude Sonnet|Complex reasoning, planning, delegation|
|Organizer / PM             |Claude Haiku |Task routing, fast coordination        |
|Worker agents              |Claude Haiku |Most tasks are simple and high-volume  |
|Bid decisions (Polymarket) |Claude Sonnet|Needs real reasoning, money on the line|
|Financial document analysis|Claude Sonnet|Complex multi-document analysis        |

**API:** Anthropic pay-as-you-go — not a subscription.
**Estimated monthly cost:** $10–20 depending on agent activity.
**Hard rule:** Set a spending cap in the Anthropic console before enabling any autonomous features.

-----

## Network

|Detail            |Value                        |
|------------------|-----------------------------|
|Connection        |Wired ethernet to router     |

-----

## Security

- SSH key authentication only — password login disabled
- All financial data processed locally where possible; Anthropic API does not train on API data
- OpenClaw memory and context stored on-machine — not in any cloud
- Hard API spending cap set before enabling autonomous agents
- Caddy + Let’s Encrypt for SSL on any externally exposed service
- LUKS disk encryption planned once core stack is stable
- Each agent operates with minimum required permissions — no agent has broader access than its role needs

-----

## Cost

|Item                   |Cost              |
|-----------------------|------------------|
|Beelink SER5 MAX       |$460              |
|APC Back-UPS 600       |~$70              |
|External backup drive  |Already owned     |
|**Hardware total**     |**~$530**         |
|n8n (self-hosted)      |Free              |
|CrewAI (open source)   |Free              |
|OpenClaw               |Free (self-hosted)|
|Anthropic API (monthly)|~$10–20/month     |

-----

## Career context

This project is intentional. Not just a personal tool — a home lab for building the exact skills that Platform Engineering and DevOps roles require, while producing something real and demonstrable.

The people making serious money in the AI era aren’t the ones who learned to use AI tools — they’re the ones who learned to architect, evaluate, and ship systems that involve AI. Platform Engineering sits at exactly that intersection.

**Skills this project directly builds:**

Linux server administration, containerization (Docker), remote system management via SSH, database administration (PostgreSQL), API integration and cost management, multi-agent system design, observability and dashboards, SSL/TLS and reverse proxy configuration, infrastructure as code (Ansible), and eventually Kubernetes cluster management.

**What this project teaches that most courses don’t:**

Thinking in systems rather than tasks. Designing what an agent does, when, with what guardrails, connected to what data. Building observable infrastructure — knowing what your system is doing at all times. The agent dashboard is literally production observability dressed up beautifully.

**Certifications roadmap:**

1. AWS Cloud Practitioner
2. AWS Solutions Architect Associate
3. Docker Certified Associate
4. Certified Kubernetes Administrator

**Kubernetes path (when ready):**

- K3s — lightweight Kubernetes running directly on this Beelink
- K9s — best Kubernetes management UI
- Minikube — for local experimentation inside containers

-----

## Resources

- [OpenClaw](https://openclaw.ai) — agent interface and Telegram/WhatsApp integration
- [CrewAI](https://crewai.com) — multi-agent orchestration framework
- [n8n](https://n8n.io) — workflow automation
- [Anthropic API Console](https://platform.anthropic.com) — model access and spending caps
- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Documentation](https://docs.docker.com/compose)
- [Portainer Documentation](https://docs.portainer.io)
- [DECISIONS.md](DECISIONS.md) — architectural decisions and reasoning
- [journal.md](journal.md) — running log of what was built and what broke

-----

*Started February 2026*