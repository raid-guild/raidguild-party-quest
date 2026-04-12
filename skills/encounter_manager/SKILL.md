---
name: encounter_manager
description: Resolves one encounter beat with strict state-update and append-only logging discipline.
---

# Encounter Manager

## Purpose

Own the active scene loop for one campaign beat.

This skill handles:
- scene preparation
- roll resolution
- consequence application
- beat pacing
- append-only event logging

This skill does not handle:
- long-term campaign planning
- character creation
- round summaries
- session handoff ownership

## Canonical State

Use shared campaign state, not skill-local state.

Required files:
- `workspace/state/campaigns/<campaign_id>/active/encounter_request.json`
- `workspace/state/campaigns/<campaign_id>/active/raw_player_messages.md`
- `workspace/state/campaigns/<campaign_id>/active/optional_rolls.json`
- `workspace/state/campaigns/<campaign_id>/active/scene.json`
- `workspace/state/campaigns/<campaign_id>/active/normalized_actions.json`
- `workspace/state/campaigns/<campaign_id>/logs/event-log.jsonl`

Read policy from `workspace/rules/core-policy.md`.

## Required Workflow

Every uncertain turn must follow:

1. `STATE READ`
2. `ROLL`
3. `STATE UPDATE`
4. `EVENT LOG APPEND`
5. `CHAT OUTPUT`

If step 3 or step 4 fails, the beat is not resolved.

## Required Per-Beat Fields

Each beat must identify:
- scene objective
- acting character
- intent
- risk
- roll trigger
- roll result
- consequence
- updated pressure or clocks
- next spotlight

Before normalization, classify each message as:

- `ooc_chat`
- `ooc_command`
- `ic_action`

Only `ic_action` becomes a normalized encounter action.

## Pacing Rules

Track:
- `beat_count`
- `beat_cap`
- `must_escalate_at`
- `must_resolve_by`

If beat cap is exceeded, force a resolution or cliffhanger.

## Failure Behavior

- If `campaign_id` is ambiguous, stop and ask.
- If active scene state is missing, scaffold it before continuing.
- If append-only logging fails, do not narrate a finalized outcome.
- If rules conflict with prompt prose, follow `workspace/rules/core-policy.md`.
- If a message is OOC, do not treat it as an in-fiction action.

## Bundled Helpers

- `scripts/bootstrap_state.py`
  Initializes shared active encounter files.
- `scripts/validate_state.py`
  Validates shared active encounter files.
- `scripts/prepare_encounter.py`
  Normalizes actions and refreshes active scene state.
- `scripts/resolve_encounter.py`
  Resolves one beat and appends event records.
