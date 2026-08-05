---
name: robotics-radar
description: Self-maintenance sweep for this robotics skill collection — finds what changed in the field and writes it back into the skills. Use when the user asks to update/refresh the robotics skills, check whether the snapshots are stale, sweep for new robot concepts, platforms, theories or tooling, add coverage for a robot type the collection is missing, or runs this on a schedule. Also use before relying on the collection after a long gap. Orchestrates parallel research agents, verifies every claim against live sources, and commits the diff.
allowed_tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - WebSearch
  - WebFetch
  - AskUserQuestion
---

# Robotics Radar

Keep this collection from rotting. Robotics moves fast enough that a six-month-old snapshot misleads: repos get archived, standards get revised, platforms ship and die, and whole method families appear. This skill is the maintenance loop that finds those changes and writes them back in.

Collection root: the repo containing `skills/` (typically `~/claude-robotics-skills`). Work there, not in the symlinked copies.

## What a sweep does

### 1. Triage — what is actually stale

Read the `**Verified:**` date at the top of every `skills/*/references/landscape.md`. Anything older than ~3 months is a candidate; older than 6 months is due. Run `scripts/check_sources.py` to find dead links before spending any search budget — a 404 is a guaranteed edit, a stale date is only a maybe.

### 2. Fan out — one research agent per stale domain

Spawn agents in parallel (`Agent` tool, or a `Workflow` when the user has opted into orchestration), one per domain. Each agent gets: the domain's current `landscape.md`, the file format rules, and instructions to search live (including Chinese-language queries — a large share of new hardware ships there first) and rewrite the file with only source-verified entries.

Ask each agent for three things beyond the file: **what disappeared** (archived, abandoned, superseded), **what is new**, and **what surprised them**. The third is where genuinely new concepts show up.

### 3. Verify adversarially — never trust the author agent

For each rewritten file, spawn a second agent that tries to *disprove* it: fetch the load-bearing source URLs, check the page actually supports the claim, and delete anything unverifiable. Authors over-claim; verifiers are the reason the collection is trustworthy. A claim that survives an agent trying to kill it is worth keeping.

### 4. Detect coverage gaps — new robot concepts

Separately from updating existing files, ask: **has a robot type, paradigm, or theory appeared that no skill covers?** Search for emerging categories rather than known names. When something real and durable turns up, propose a new skill (same house structure: decision sequence, Loop modes, Modern scan, 5+ Gotchas) and add it — a collection that only refreshes what it already knows goes blind to whatever is actually new.

Be strict about durability: one impressive demo is not a domain. Look for a category with multiple independent groups, real hardware or maintained software, and decisions a practitioner must actually make.

### 5. Write it back

Update files in place, bump each `**Verified:**` date to today, bump `plugin.json` version (minor for new skills, patch for refreshes), and summarize the diff for the user: what changed, what died, what is new, what a reader should re-check. Commit in English. Never push without being asked.

## Loop modes

Offer the user how they want to run the sweep, then honor it:

- **Guided** (default) — triage first, show what is stale, confirm scope, then sweep.
- **Fast-forward** — sweep everything stale without asking, report the diff at the end. This is the mode for `/loop` and scheduled runs.
- **Audit** — read-only. Report staleness, dead links, and suspected gaps; change nothing.

When invoked inside a `/loop` or on a schedule, default to Fast-forward and keep each run scoped to the stalest 2-3 domains rather than all of them — small frequent sweeps beat one giant rewrite.

## Gotchas

- **Refreshing only what exists makes the collection go blind.** The valuable finding is usually a category nobody in the collection named yet. Budget a real share of the sweep for open-ended "what is new in robotics" searching, not just re-checking known entries.
- **The author agent will confidently invent a plausible repo.** Names that sound right (`awesome-<domain>`, `<vendor>_ros2_driver`) are exactly what a language model fabricates. The adversarial verify pass is not optional ceremony — it is the mechanism that keeps entries real.
- **Archived is worse than missing.** A dead repo that still ranks well in search sends users down a path that ended years ago. Explicitly hunt for archive/deprecation banners and record the successor — that is the single most useful thing a snapshot can carry.
- **Vendor pages overstate specs.** Marketing DOF counts, payloads, and runtimes are best-case. Record what the page says and cite it; do not launder it into a recommendation.
- **A sweep that rewrites every file every time destroys signal.** If nothing changed in a domain, leave the file alone and say so — a churning git history hides the real changes.
- **Standards need their revision year.** "ISO 13849" without an edition ages badly and can mislead a safety case. Carry the revision and re-verify it rather than copying it forward.
- **China-market coverage decays fastest.** New hardware there often appears in Chinese-language sources months before English ones. Skipping those queries means the snapshot lags the field, not just the language.
