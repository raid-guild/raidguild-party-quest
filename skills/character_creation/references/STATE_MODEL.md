# State Model

This skill keeps one canonical character draft in JSON and two downstream-friendly markdown views.

## Canonical Files

- `state/outputs/character_draft.json`
  The source of truth for the active character draft.
- `state/outputs/party_brief.md`
  A human-readable summary of the draft.
- `state/handoffs/known_characters.md`
  The export that Campaign Manager can consume.
- `state/logs/change_log.md`
  Append-only audit trail.

## Input Files

- `state/inputs/campaign_brief.md`
  Optional campaign framing or tone.
- `state/inputs/player_preferences.md`
  Optional constraints, likes, dislikes, or starter ideas from the player.

## IDs

Use stable IDs like `CHAR-001`.

## Draft Shape

The JSON draft should remain compact:

```json
{
  "character_id": "CHAR-001",
  "status": "draft",
  "name": "",
  "concept": "",
  "role": "",
  "tone_tags": [],
  "core_traits": [],
  "drive": "",
  "fear": "",
  "edge": "",
  "flaw": "",
  "relationships": [],
  "starter_gear": [],
  "notes": "",
  "derived": {
    "one_line_pitch": "",
    "campaign_hook": "",
    "notable_edge": ""
  }
}
```
