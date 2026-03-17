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