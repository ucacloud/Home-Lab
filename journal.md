# Journal

A running log of what I built, what broke, and what I learned.

---

## [March 2026] Getting the Bee online

**What I was trying to do:**
Get Ubuntu Server installed and SSH working so I could manage everything remotely from my Windows desktop.

**What happened:**
First attempt at flashing the USB was with Rufus 4.63 — had issues. Switched to balenaEtcher and that worked. 

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
`git remote set-url origin https://username:TOKEN@github.com/username/Home-Lab.git`

**What I learned:**
- VS Code Remote SSH is just a window into the Bee - everything runs on the Bee, Windows is just the screen
- GitHub no longer accepts passwords for git operations - Personal Access Token required
- When token auth keeps failing, embed it directly in the remote URL
- `git config --global user.email` and `git config --global user.name` need to be set before first commit on a fresh machine

## [March 2026] Installed Podman

**What I did:**
Installed Podman 4.9.3 via apt. Verified with hello-world container.

**What I learned:**
- `sudo apt install podman -y` broken down: sudo = run as admin, apt = package manager, install = action, podman = package name, -y = auto confirm
- Podman runs Docker images natively - the whole Docker Hub library works out of the box
- "Hello from Docker" in the output is just hardcoded text inside the image itself, not an error. Podman pulled and ran it correctly.

## [March 2026] Purged Podman / Installed Docker

**What I did:**
Purged Podman / installed Docker 29.3.0. Verified with hello-world container.

**What I learned:**
- When I attempted to create a new Podman connection in Portainer, there was a note that mentioned "Rootless mode + Ubuntu not officially supported".
- I tried to do a permission fix and system reboot but it didn't resolve the issue.
- Decided to move forward with the project and use Docker instead since the 'risk' is almost negligible.

## [March 2026] Installed and setup Portainer

**What I was trying to do:**
Get Portainer linked to Docker to that I can monitor it.

**What I did:**
Installed Portainer, connected it to my local machine and was able to view my Docker from the Portainer dashboard.

**What I learned:**
- Portainer can allow me to start and stop containers, read logs, inspect whats happening inside containers and deploy new stacks.

## [March 2026] Created a simple bot

**What I was trying to do:**
Get a foundational understanding of how to make a simple Claude bot.

**What I did:**
Got an API key from Anthropic, built a somple bot that acts on a loop to answer any questions and exits when the user types 'quit'.

**What I learned:**
- How to designate which model to use
- Set a usage rate limit
- Save the conversation history to an array
- Store API keys in .env and reference with os.getenv() — never hardcode credentials