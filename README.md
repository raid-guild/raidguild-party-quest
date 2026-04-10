# Party Quest

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

It is **generic by default**.

It also includes an optional quick-start preset:
- **The Last Chance Formal** — a Coen-ish adult-prom social noir setup

## Best fit

This template is best for:
- Discord servers
- Telegram group chats
- short campaign arcs
- friend groups who want a guided story without heavy prep
- story-first play with light d20 resolution

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

The default ending preference is a **cliffhanger**, but the agent can also land a cleaner ending or explicitly seed a follow-up campaign.

## How a game starts

When added to a group chat, the agent should:
1. ask what kind of campaign the group wants
2. offer quick-start presets if the group is undecided
3. ask who is playing
4. confirm the roster
5. onboard characters one player at a time
6. wait until all listed players are marked ready
7. launch the opening scene
8. keep the campaign moving toward a fifth-round finale

## Workspace guide

Key files:
- `workspace/CAMPAIGN_HOST.md` — operating rules and onboarding flow
- `workspace/CAMPAIGN_PRESETS.md` — optional starter premises, including the prom preset
- `workspace/FINALE_CHECKLIST.md` — ending guidance for round 5 and epilogues
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

## Design philosophy

This template favors compact, consequence-driven campaigns over endless sandbox drift.
It works best when the group wants momentum, clear turns, and an ending worth remembering.
