# Data Model

## encounter_request

Store the incoming structured request in `state/inputs/encounter_request.json`.

Recommended shape:

```json
{
  "encounter_id": "TP-001",
  "campaign_id": "CAMPAIGN-001",
  "scene_id": "SCENE-001",
  "encounter_type": "social",
  "tone": "tense, strange, low-magic",
  "objective": "Get past the ferryman guarding passage across the river.",
  "difficulty": "normal",
  "narrative_context": "The river crossing is the only obvious way forward.",
  "trigger": "The party reaches the dock at dusk.",
  "stakes": {
    "success": "The party crosses safely.",
    "failure": "The ferryman refuses and alerts nearby patrol.",
    "complication": "The ferryman reveals a hidden price or secret condition."
  },
  "environment": {
    "location_name": "Black River Dock",
    "description": "A narrow ferry platform rocks against the dock in cold mist.",
    "tags": ["water", "mist", "unstable", "only-route-forward"]
  },
  "players": [
    {
      "id": "CHAR-001",
      "name": "Nyra",
      "traits": ["sharp", "intuitive", "calm"],
      "conditions": [],
      "inventory_tags": [],
      "narrative_role": "observer"
    }
  ],
  "npcs": [],
  "monsters": [],
  "prior_state_refs": []
}
```

## scene_state

The local scene state lives in `state/encounters/scene_state.json`.

Keep:
- `round`
- `phase`
- `tension`
- `active_hazards`
- `active_opportunities`
- `environment_changes`
- `unresolved_threads`
- `spotlight_order`

## normalized_actions

The normalized player actions live in `state/encounters/normalized_actions.json`.

Each action should include:
- `player_id`
- `approach`
- `intent`
- `target_id`
- `uses_item_tag`
- `risk_level`
- `aiding_player_id`

## encounter_result

Write the final structured output to `state/outputs/encounter_result.json`.
