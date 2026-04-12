# State Model

Canonical campaign state is campaign-first.

## Root

All canonical campaign continuity lives under:

- `workspace/state/campaigns/<campaign_id>/`

## Canonical Files

- `campaign.json`
  Campaign identity, current round, active scene, pacing defaults, canon confidence, and state integrity.
- `players.json`
  Roster, readiness, and player status for this campaign.
- `readiness.json`
  Campaign-level gate for opening brief readiness, roster confirmation, character completion, and whether Round 1 may start.
- `npcs.json`
  Important NPCs, agendas, and current status.
- `clocks.json`
  Pressure trackers and thresholds.
- `opening_brief.md`
  Required player-facing setting and scenario intro to be summarized before Round 1 starts.
- `characters/<character_id>.json`
  Canonical character sheets exported from `character_creation`.
- `active/scene.json`
  Live scene snapshot for the current beat loop.
- `active/encounter_request.json`
  Current scene request payload for `encounter_manager`.
- `active/normalized_actions.json`
  Parsed player actions for the current beat.
- `active/optional_rolls.json`
  Approved player-supplied rolls for the current beat.
- `sessions/<session_id>.json`
  Current or last known session snapshot.
- `rounds/round-XX-summary.md`
  End-of-round artifact.
- `logs/event-log.jsonl`
  Append-only source of truth for actual play.
- `logs/gm-notes.md`
  Non-canonical GM scratchpad.
- `handoffs/latest-session.json`
  Resume-ready summary for the next session.

## File Conventions

- Every file must align on `campaign_id`.
- Use stable slugs for campaigns and scenes.
- Use ISO-8601 UTC timestamps in script-written fields.
- Treat `event-log.jsonl` as truth when snapshots drift.

## Scene Pacing Fields

`campaign.json` and `active/scene.json` should carry:

- `beat_count`
- `beat_cap`
- `must_escalate_at`
- `must_resolve_by`

These fields are enforceable state, not style guidance.

## Confidence Fields

Track:

- `canon_status`: `canon`, `provisional`, `disputed`
- `state_integrity`: `clean`, `partial`, `messy`
