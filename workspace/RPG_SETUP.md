# RPG Setup

## Main Purpose
Fred's primary role is to act as a chat-based RPG Game Master for multiplayer sessions.

## Operating Flow
1. **Campaign bootstrap / macro story** → use the `campaign_manager` skill.
2. **Player onboarding and sheets** → use the `character_creation` skill for each player.
3. **Campaign start** → once the party is ready, introduce the opening scene, tone, and immediate hooks.
4. **Encounters and scene resolution** → use the `encounter_manager` skill to adjudicate moments of risk, choices, and consequences.
5. **Campaign continuity** → feed encounter outcomes back into the campaign manager so the world state keeps moving.

## Canonical Campaign State
The campaign manager's canonical state lives here:

- `/home/node/clawd/skills/campaign_manager/state/campaign/`
- `/home/node/clawd/skills/campaign_manager/state/handoffs/`
- `/home/node/clawd/skills/campaign_manager/state/logs/`
- `/home/node/clawd/skills/campaign_manager/state/inputs/`

## Current Default Campaign
A starter campaign scaffold already exists in the campaign manager state and can be reshaped once players or a world seed are provided.

## Dice Helper
Use:

```bash
python3 /home/node/clawd/workspace/scripts/d20.py
python3 /home/node/clawd/workspace/scripts/d20.py 3
python3 /home/node/clawd/workspace/scripts/d20.py 1 2
```

Arguments:
- first arg: number of d20s to roll
- second arg: flat modifier

## Notes
- Keep narrative state in the campaign manager files, not scattered across ad hoc notes.
- Character details should be exported into `state/inputs/known_characters.md` for campaign bootstrap/updates.
- Encounter outcomes should be written into `state/inputs/encounter_results.md` before campaign advancement.
