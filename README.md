# Chat Campaign Host

A Pinata agent template for running multiplayer chat-based RPG campaigns in Discord or Telegram.

## What it does

This agent can:
- ask a group for a campaign seed
- collect who is playing
- guide each player through character creation
- start play once the roster is ready
- run a compact five-round campaign arc
- end on a finale, fallout, and optional sequel hook

It is **generic by default**.

It also ships with an optional starter tone/preset:
- **The Last Chance Formal** — a Coen-ish adult-prom social noir campaign seed

## Included skills

- `campaign_manager`
- `character_creation`
- `encounter_manager`

Pinned skill CIDs are declared in `manifest.json`.

## Supported channels

- Discord
- Telegram

The deployer must provide the relevant bot token(s) during setup.

## Campaign shape

Default arc:
- Lobby / onboarding
- Round 1: inciting trouble
- Round 2: complication
- Round 3: reversal
- Round 4: escalation
- Round 5: finale
- Epilogue: fallout + cliffhanger / next-campaign seed

## Workspace guide

Key files:
- `workspace/CAMPAIGN_HOST.md` — operating rules for multiplayer campaign hosting
- `workspace/CAMPAIGN_PRESETS.md` — optional starter premises, including the prom preset
- `workspace/state/lobby.md` — lobby and onboarding state
- `workspace/state/players.md` — roster and readiness tracking
- `workspace/state/session_status.md` — round, pressure, and campaign status
- `workspace/scripts/d20.py` — tiny dice helper

## Deploying as a template

Use this repo as a Pinata agent template. The manifest includes:
- agent metadata
- template metadata
- required secrets
- the 3 pinned skill CIDs
- Discord/Telegram channel configuration

## Intended behavior

When added to a group chat, the agent should:
1. ask what kind of campaign the group wants
2. ask who is playing
3. confirm the roster
4. onboard characters one player at a time
5. wait until all players are marked ready
6. launch the opening scene
7. keep the campaign moving toward a fifth-round finale

## Notes

This template favors compact, consequence-driven campaigns over endless sandbox drift.
