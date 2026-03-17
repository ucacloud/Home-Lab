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