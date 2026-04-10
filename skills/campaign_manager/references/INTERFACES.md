# Interfaces

This skill exchanges data with sibling skills through markdown files in `state/inputs/` and `state/handoffs/`.

## Inputs

### `state/inputs/known_characters.md`

Expected from a character creation skill or the user.

Recommended format:

```md
# Known Characters

## Party
- Name | role | drive | notable edge

## Important NPCs
- NPC-001 | name | role | motive | relationship
```

### `state/inputs/world_seed.md`

Freeform campaign seed. The bootstrap script uses the first heading and the first paragraph as the initial premise when possible.

### `state/inputs/encounter_results.md`

Expected from the encounter manager after a scene resolves.

Recommended format:

```md
# Encounter Results

- Encounter ID: TP-003
- Session ID: SESSION-002
- Timestamp: 2026-04-10T18:00:00Z
- Outcome: success
- Summary: The party exposed the smuggler but alerted the harbor watch.

## Resolved Loops
- LOOP-001 | Smuggler identified

## New Loops
- LOOP-003 | Harbor watch now wants payment for silence | pressure: high | next: secure leverage before dawn

## World Changes
- The harbor watch is alert and suspicious.

## Rewards
- A coded ledger naming two buyers.

## Consequences
- The smugglers know the party interfered.

## Suggested Follow-Up
- Push the party toward the buyers before the ledger is destroyed.
```

The import script reads these sections by heading name. Keep them exact.

## Outputs

### `state/handoffs/next_encounter.md`

The campaign manager should produce one primary touchpoint packet for the encounter manager. It should include:

- the selected touchpoint ID
- the narrative purpose
- the immediate trigger
- the location
- involved characters or factions
- stakes and likely opposition
- aftermath hooks if the scene succeeds or fails
