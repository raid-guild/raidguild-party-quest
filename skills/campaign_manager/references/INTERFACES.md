# Interfaces

The campaign manager exchanges state through the shared campaign tree under `workspace/state/campaigns/<campaign_id>/`.

## Inputs

### `characters/<character_id>.json`

Expected from `character_creation`.

Recommended shape:

```json
{
  "character_id": "CHAR-001",
  "name": "Mara",
  "concept": "Streetwise courier with too many debts",
  "role": "scout",
  "drive": "Stay ahead of the people she owes",
  "fear": "Being trapped where everyone can find her",
  "edge": "Reads crowds and exits quickly",
  "flaw": "Bails before trust fully lands",
  "derived": {
    "one_line_pitch": "Mara is a scout: Streetwise courier with too many debts.",
    "campaign_hook": "Stay ahead of the people she owes",
    "notable_edge": "Reads crowds and exits quickly"
  }
}
```

### `logs/event-log.jsonl`

Expected from `encounter_manager`.

Recommended event types:

- `scene_prepared`
- `roll_resolved`
- `consequence_applied`
- `beat_closed`

Example:

```json
{"ts":"2026-04-12T16:10:00Z","campaign_id":"ash-market","session_id":"telegram-01","scene_id":"auction-floor","type":"scene_prepared","beat_count":1,"objective":"Steal the ledger before bids close","action_count":3}
{"ts":"2026-04-12T16:12:10Z","campaign_id":"ash-market","session_id":"telegram-01","scene_id":"auction-floor","type":"roll_resolved","beat_count":1,"actor":"Mara","intent":"Slip behind the clerk and lift the ledger","risk":"cautious","target_number":12,"roll_value":14,"modifier":0,"final_value":14,"outcome_band":"success"}
{"ts":"2026-04-12T16:13:42Z","campaign_id":"ash-market","session_id":"telegram-01","scene_id":"auction-floor","type":"consequence_applied","beat_count":1,"status":"ongoing","added_hazards":["heightened pressure"],"added_opportunities":[]}
```

### `active/scene.json`

Live scene snapshot shared with `encounter_manager`.

Use it to read:

- current objective
- beat pacing fields
- spotlight-next
- active pressure markers

## Outputs

### `rounds/round-XX-summary.md`

Required round artifact.

Include:

- round number
- summary of meaningful changes
- unresolved threads
- clocks changed
- NPC changes
- spotlight-next
- canon ambiguity notes

### `handoffs/latest-session.json`

Required session handoff.

Include:

- `campaign_id`
- `session_id`
- `status`
- `ended_at`
- `current_round`
- `next_scene_seed`
- `open_loops`
- `canon_notes`
- `canon_status`
- `state_integrity`
