# Data Model

The encounter manager reads and writes shared active scene state under `workspace/state/campaigns/<campaign_id>/`.

## `active/encounter_request.json`

Recommended shape:

```json
{
  "campaign_id": "ash-market",
  "session_id": "telegram-01",
  "scene_id": "auction-floor",
  "encounter_type": "social",
  "objective": "Get the ledger before bids close",
  "difficulty": "normal",
  "players": [
    {
      "id": "CHAR-001",
      "name": "Mara"
    }
  ],
  "npcs": [],
  "environment": {
    "tags": ["crowd", "cover"]
  },
  "prior_state_refs": []
}
```

Required fields:

- `campaign_id`
- `session_id`
- `scene_id`
- `encounter_type`
- `objective`
- `difficulty`

## `active/scene.json`

Keep:

- `campaign_id`
- `session_id`
- `scene_id`
- `objective`
- `status`
- `beat_count`
- `beat_cap`
- `must_escalate_at`
- `must_resolve_by`
- `spotlight_next`
- `tension`

## `active/normalized_actions.json`

Each action should include:

- `player_id`
- `actor_name`
- `approach`
- `intent`
- `risk_level`
- `roll_trigger`

Only `ic_action` messages should appear here.

## Message Classification

Before action normalization, classify raw chat into:

- `ooc_chat`
- `ooc_command`
- `ic_action`

`ooc_chat` should be excluded from beat resolution.
`ooc_command` may produce admin events, but not action resolution records.

## `logs/event-log.jsonl`

Append these event types during resolution:

- `scene_prepared`
- `roll_resolved`
- `consequence_applied`
- `beat_closed`

No finalized narration should happen before the append succeeds.
