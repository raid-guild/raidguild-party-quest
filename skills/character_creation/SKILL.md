---
name: character_creation
description: Creates a canonical character sheet and exports it into the shared campaign tree.
---

# Character Creation Skill

## Purpose

Own character intake and canonical character sheet format.

Own:
- local draft flow
- canonical character JSON export
- concise handoff exports

Do not own:
- campaign arc state
- encounter resolution
- world progression

## Canonical State

Canonical character state lives at:

- `workspace/state/campaigns/<campaign_id>/characters/<character_id>.json`

These character exports are used by campaign readiness gating before Round 1 starts.

Working files may still live in this skill's local `state/` folder, but they are not the source of truth for campaign continuity.

## Workflow

1. Build or update the local draft
2. Recompute derived fields
3. Refresh local handoffs
4. Export canonical character JSON to the shared campaign tree when `campaign_id` is known

## Failure Behavior

- If `campaign_id` is ambiguous at export time, stop and ask.
- If the shared campaign folder is missing, scaffold it before export.
- Do not mutate campaign arc or active scene state.

## Bundled Helpers

- `scripts/bootstrap_state.py`
  Initializes the local draft and optional shared export target.
- `scripts/update_character.py`
  Updates the draft and writes the shared character export when campaign context is known.
- `scripts/validate_character.py`
  Validates local draft shape and shared export presence.
