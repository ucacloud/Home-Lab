# Home Lab — AI Agent Infrastructure

## Overview

A self-hosted, always-on AI agent infrastructure running on a dedicated mini PC. A Chief of Staff agent (Herman) handles direct communication, delegates to specialized worker agents, runs scheduled jobs, and manages a growing portfolio of income-generating projects.

This is simultaneously a personal productivity system, an autonomous analysis platform with strict guardrails, and a hands-on DevOps/Platform Engineering training environment.

Everything runs on The Bee. All data stays at home.

-----

## Current Status

| Milestone | Status |
|-----------|--------|
| Hardware acquired and set up | ✅ Done |
| Ubuntu Server 24.04 LTS installed | ✅ Done |
| SSH access from Windows desktop | ✅ Done |
| Docker + Portainer running | ✅ Done |
| PostgreSQL container (connected via DBeaver) | ✅ Done |
| Financial advisor bot (Python + PostgreSQL) | ✅ Done |
| Hermes Agent installed (systemd service) | ✅ Done |
| Telegram bot (Herman) connected | ✅ Done |
| SOUL.md configured (Chief of Staff role) | ✅ Done |
| Ollama on Windows desktop (GPU inference) | ✅ Done |
| Hybrid model routing (Claude + Ollama) | ✅ Done |
| Overnight market analysis agent | 🔲 Next |
| Polymarket signal generator | 🔲 Planned |
| Land wholesaling pipeline | 🔲 Planned |
| Self-hosted Honcho (memory layer) | 🔲 Planned |
| Agent dashboard website | 🔲 Planned |

-----

## Hardware

### The Bee (Beelink SER5 MAX) - Always-On Server

| Component | Details |
|-----------|---------|
| **CPU** | AMD Ryzen 7 7735HS (8C/16T, up to 4.75GHz, Zen 3+) |
| **RAM** | 24GB LPDDR5 6300MHz |
| **Storage** | 500GB M.2 PCIe 4.0 SSD (2x M.2 slots, expandable to 4TB) |
| **Network** | WiFi 6 / 2.5G LAN — wired ethernet in use |
| **OS** | Ubuntu Server 24.04 LTS |

Managed remotely via SSH. Ethernet is the primary connection. Auto Power On enabled — boots automatically after power loss.

### Windows Desktop - GPU Inference Machine

| Component | Details |
|-----------|---------|
| **CPU** | AMD Ryzen 7 3700X (8C/16T) |
| **RAM** | 16GB |
| **GPU** | NVIDIA GeForce RTX 2070 SUPER (8GB VRAM) |

Runs Ollama for local GPU-accelerated inference. Accessible from The Bee over LAN. Shared daily-use machine - inference scheduled for off-hours or lightweight tasks.

-----

## The Agent - Herman

Herman is a Hermes Agent (NousResearch) running as a systemd service on The Bee. He operates as Chief of Staff - the only agent I talk to directly. He oversees all projects, coordinates future worker agents, and runs scheduled jobs.

Accessible via Telegram and CLI. Personality and operating rules defined in SOUL.md. Memory persists across sessions via Honcho (currently cloud-hosted, self-hosted migration planned).

-----

## AI Model Routing

| Task | Model | Provider | Cost |
|------|-------|----------|------|
| Interactive conversation | Claude Sonnet | Anthropic API | Pay-per-use |
| Background/cron jobs | Qwen3 8B | Ollama (local GPU) | Free |
| Complex analysis | Claude Sonnet | Anthropic API | Pay-per-use |

Long-term goal: route as much as possible through Ollama to minimize API costs.

-----

## Tech Stack

| Layer | Technology |
|-------|-----------|
| OS | Ubuntu Server 24.04 LTS |
| Containers | Docker |
| Container UI | Portainer |
| Agent platform | Hermes Agent (NousResearch) |
| Agent interface | Telegram (primary), CLI (local) |
| Local inference | Ollama + Qwen3 8B (RTX 2070 SUPER) |
| AI API | Anthropic Claude Sonnet (pay-as-you-go) |
| Database | PostgreSQL (Docker) |
| DB management | DBeaver |
| Remote access | SSH + VS Code Remote SSH |

-----

## Projects

### 1. Agent Infrastructure
Herman as Chief of Staff on The Bee. Hybrid model routing between Anthropic API and local Ollama. Future: self-hosted Honcho memory, additional worker agents.

### 2. Personal Finance Bot
Python bot using Anthropic API + PostgreSQL. 20-message sliding window for token management. Tracks spending, income, and bills. Coaches toward financial freedom.

### 3. Overnight Market Analysis Agent
Cron job that monitors market data, news, and sentiment overnight. Delivers brief analysis via Telegram each morning - actionable plays with confidence levels. Analysis only, no autonomous execution.

### 4. Polymarket Trading Agent
Event-based prediction markets. Focus on detecting mispriced real-world events. Phased: signal generator > paper trading > controlled execution with strict guardrails.

### 5. Land Wholesaling Pipeline
Find underpriced parcels, get them under contract, assign to cash buyers. Scraper agents, analyst for pricing comps, alerts, PostgreSQL buyer CRM, deal scoring, due diligence automation.

### 6. AI Agent Automation Services
Building AI bots for small businesses (trade verticals).

### 7. Personal Trainer / Nutritionist Bot
Meal logging, exercise guidance. Lower priority than income-generating projects.

### 8. Furniture Flipping / Coffee Tables
Physical-world business. Fastest feedback loop for income.

-----

## Security

- SSH key authentication only - password login disabled
- Telegram bot restricted to owner only
- All data processed locally where possible
- Anthropic API does not train on API data
- Hard API spending cap set before enabling any autonomous features

-----

## Cost

| Item | Cost |
|------|------|
| Beelink SER5 MAX | $460 |
| **Hardware total** | **$460** |
| Hermes Agent | Free (open source) |
| Ollama | Free (open source) |
| Anthropic API (monthly) | ~$10-20/month |

-----

*Started February 2026*