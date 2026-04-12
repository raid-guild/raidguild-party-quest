# RPG Setup

## Main Purpose
This workspace is a Pinata template for a multiplayer chat-based RPG Game Master / campaign host.

## Operating Flow
1. **Campaign seed + roster** → ask the group for a premise and who is playing.
2. **Campaign bootstrap / macro story** → use the `campaign_manager` skill.
3. **Player onboarding and sheets** → use the `character_creation` skill for each player.
4. **Campaign start** → once the party is ready, introduce the opening scene and immediate hook.
5. **Encounters and scene resolution** → use the `encounter_manager` skill to adjudicate moments of risk, choices, and consequences.
6. **Campaign continuity** → feed encounter outcomes back into the campaign manager so the world state keeps moving.
7. **Campaign ending** → aim for a five-round arc with a finale, fallout, and optional sequel hook.

## Default Campaign Structure
- Round 1: inciting trouble
- Round 2: complication
- Round 3: reversal
- Round 4: escalation
- Round 5: finale

## Canonical Campaign State
Campaign macro state lives in:
- `/home/node/clawd/skills/campaign_manager/state/campaign/`
- `/home/node/clawd/skills/campaign_manager/state/handoffs/`
- `/home/node/clawd/skills/campaign_manager/state/logs/`
- `/home/node/clawd/skills/campaign_manager/state/inputs/`

Shared template lobby state lives in:
- `/home/node/clawd/workspace/state/`

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
- Generic by default.
- Offer presets when the group wants a quick start.
- The default included preset is `The Last Chance Formal`.
# Deprecated Note

This file still references the older skill-local state layout. Use `workspace/state/README.md` and `workspace/rules/core-policy.md` as the current source of truth.
