---
name: campaign_manager
description: Manages durable campaign state, round progression, and session handoffs for a multiplayer chat RPG.
---

# Campaign Manager Skill

## Purpose

Own the campaign layer, not the beat layer.

Own:
- `campaign.json`
- `players.json`
- `readiness.json`
- `npcs.json`
- `clocks.json`
- `opening_brief.md`
- round summaries
- session handoffs

Do not own:
- character creation
- per-beat resolution
- per-turn roll adjudication
- append-only beat logging

## Canonical State

Canonical state lives under `workspace/state/campaigns/<campaign_id>/`.

Read policy from `workspace/rules/core-policy.md` before making game-law decisions.

Required files:
- `workspace/state/campaigns/<campaign_id>/campaign.json`
- `workspace/state/campaigns/<campaign_id>/players.json`
- `workspace/state/campaigns/<campaign_id>/readiness.json`
- `workspace/state/campaigns/<campaign_id>/npcs.json`
- `workspace/state/campaigns/<campaign_id>/clocks.json`
- `workspace/state/campaigns/<campaign_id>/opening_brief.md`
- `workspace/state/campaigns/<campaign_id>/rounds/round-XX-summary.md`
- `workspace/state/campaigns/<campaign_id>/sessions/<session_id>.json`
- `workspace/state/campaigns/<campaign_id>/handoffs/latest-session.json`

Inputs:
- `workspace/state/campaigns/<campaign_id>/characters/*.json`
- `workspace/state/campaigns/<campaign_id>/logs/event-log.jsonl`
- `workspace/state/campaigns/<campaign_id>/active/scene.json`

## Workflow Modes

### 1) Bootstrap Campaign

1. Identify `campaign_id`
2. Scaffold missing campaign files
3. Generate `opening_brief.md`
4. Evaluate readiness for Round 1
5. Seed current round, pressure, and handoff state
6. Mark `canon_status` and `state_integrity`

### 2) Advance Campaign

1. Read campaign snapshot and recent event log entries
2. Advance round state or world pressure
3. Update snapshots
4. Write or refresh the next handoff

### 3) Absorb Encounter Outcome

1. Read recent appended events
2. Update snapshots, loops, and clocks
3. Produce or refresh the round summary
4. Refresh the session handoff

## Failure Behavior

- If `campaign_id` is ambiguous, stop and ask.
- If event log and snapshot disagree, prefer the event log and mark integrity accordingly.
- If a required file is missing, scaffold it before continuing.
- Do not start Round 1 without `opening_brief.md`.
- Do not start Round 1 unless `readiness.json` says `round_1_ready: true`, unless the group explicitly starts short-handed.
- Do not invent rules outside `workspace/rules/core-policy.md`.

## Bundled Helpers

- `scripts/bootstrap_state.py`
  Initializes the shared campaign tree.
- `scripts/validate_state.py`
  Validates the shared campaign tree.
- `scripts/summarize_round.py`
  Builds `rounds/round-XX-summary.md` and refreshes `handoffs/latest-session.json` from shared state and append-only events.
- `scripts/apply_lifecycle.py`
  Applies pause, resume, close, abandon, or supersede transitions from OOC admin events into shared campaign/session state.
- `scripts/evaluate_readiness.py`
  Compares roster state, canonical character exports, and opening-brief state to decide whether Round 1 may start.
- `scripts/manage_players.py`
  Registers or updates player rows in `players.json`, including handle, status, and linked character IDs.
