# Party Quest

*Multiplayer chat RPGs for Discord and Telegram.*

A Pinata agent template for running compact multiplayer chat-based RPG campaigns in Discord or Telegram.

## What it does

This template gives you an agent that can:
- start a campaign in a group chat
- ask the group what kind of story they want
- confirm who is playing
- guide each player through character creation
- wait until the roster is ready
- run a five-round story arc with rising pressure
- deliver a finale, fallout, and optional sequel hook

It is generic by default.

## Included skills

- `campaign_manager`
- `character_creation`
- `encounter_manager`

## Workspace guide

Key files:
- `workspace/CAMPAIGN_HOST.md` — operating rules and onboarding flow
- `workspace/CAMPAIGN_PRESETS.md` — optional starter premises
- `workspace/FINALE_CHECKLIST.md` — finale guidance
- `workspace/rules/core-policy.md` — canonical dice, NPC, pacing, and ending rules
- `workspace/state/README.md` — campaign-first state layout
- `workspace/state/lobby.md` — lobby and campaign selection state
- `workspace/state/campaigns/` — canonical multi-campaign state tree
- `workspace/scripts/d20.py` — tiny dice helper

## Design philosophy

This template should keep narration loose and bookkeeping rigid.
State, logs, and handoffs should be harder to violate than prompt prose alone.
