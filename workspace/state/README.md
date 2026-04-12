# State Layout

Canonical state is campaign-first.

## Rules

- One chat can host many campaigns over time.
- One campaign can span many sessions.
- Every write must name `campaign_id`.
- Event logs are source of truth.
- Snapshots are derived state.

## Layout

```text
workspace/state/
  lobby.md
  campaigns/
    <campaign_id>/
      campaign.json
      players.json
      npcs.json
      clocks.json
      characters/
        <character_id>.json
      active/
        encounter_request.json
        normalized_actions.json
        optional_rolls.json
        raw_player_messages.md
        scene.json
      sessions/
        <session_id>.json
      rounds/
        round-01-summary.md
      logs/
        event-log.jsonl
        gm-notes.md
      handoffs/
        latest-session.json
```
