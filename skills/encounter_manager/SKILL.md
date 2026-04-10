---
name: encounter_manager
description: Resolve a single narrative encounter in a multiplayer chat-based campaign using lightweight d20 mechanics and structured consequences.
---

# Encounter Manager

## Purpose

Resolve one encounter beat inside a live campaign.

This skill receives scene context, player actions, and stakes from upstream context, then returns:
- structured outcomes
- scene changes
- condition changes
- narrative consequences
- suggested next prompts

This is a story-forward encounter engine, not a full tactical combat simulator.

---

## What This Skill Handles

Supported encounter types:
- social
- hazard
- combat
- mystery
- narrative

Use it when something meaningful is uncertain and the story needs a clean resolution cycle.

---

## What This Skill Does Not Handle

- long-term campaign planning
- player onboarding
- character creation
- full inventory simulation
- tactical grid combat
- deep class or spell systems
- persistent world canon outside the encounter result

---

## Design Goals

- Keep encounter resolution narrow and reliable
- Support multiple players in chat rooms
- Use lightweight d20-based outcomes
- Favor consequences and twists over dead ends
- Return structured data the Campaign Manager can continue from
- Stay setting-agnostic

---

## Canonical State Files

Maintain these files:

- `state/inputs/encounter_request.json`
- `state/inputs/raw_player_messages.md`
- `state/inputs/optional_rolls.json`
- `state/encounters/scene_state.json`
- `state/encounters/normalized_actions.json`
- `state/outputs/encounter_result.json`
- `state/outputs/encounter_results.md`
- `state/logs/change_log.md`

All state for this skill is self-contained inside this skill folder under `state/`.

Do not assume a repo-level shared `state/` directory.

If another skill needs the encounter result, it should read or copy the export from this skill folder.

If files are missing, initialize them instead of failing.

---

## Resolution Philosophy

Use a narrow mechanical band:
- one action per player per resolution cycle
- one d20 roll per action
- simple target numbers
- five outcome bands
- lightweight conditions
- concise scene state

Prefer:
- success with cost
- failure with new pressure
- critical outcomes that shift the story

Avoid:
- complex math
- long tactical exchanges
- over-simulation

---

## Required Workflow Modes

### 1) Bootstrap Encounter State
Initialize the encounter input, scene state, and output files from templates.

### 2) Prepare Encounter
Use when a fresh encounter request and player chat messages arrive.

Steps:
1. Read `encounter_request.json`
2. Read `raw_player_messages.md`
3. Build or refresh local `scene_state.json`
4. Normalize player messages into `normalized_actions.json`
5. Log the preparation step

### 3) Resolve Encounter Beat
Use when actions are ready to resolve.

Steps:
1. Read the encounter request, scene state, normalized actions, and optional rolls
2. Set target numbers within the narrow allowed band
3. Roll or use provided rolls
4. Assign outcome bands
5. Apply consequences, twists, and scene updates
6. Write both structured JSON and campaign-manager-compatible markdown
7. Log the transition

### 4) Recap
Return:
- current scene state
- action resolutions
- encounter status
- next likely prompts

---

## Operating Rules

- Normalize every player message into one primary intent and one broad approach.
- Use these approaches only:
  - `force`
  - `finesse`
  - `charm`
  - `insight`
  - `weird`
  - `support`
- Keep target numbers in the practical range from `8` to `18`.
- Use exactly these outcome bands:
  - `critical_failure`
  - `failure`
  - `mixed_success`
  - `success`
  - `critical_success`
- Every resolution cycle should change the scene in some way.

---

## Output Contracts

Write a structured result object to:
- `state/outputs/encounter_result.json`

Write a Campaign Manager import packet to:
- `state/outputs/encounter_results.md`

The markdown export must remain compatible with the Campaign Manager expectation for:
- `Encounter ID`
- `Session ID`
- `Timestamp`
- `Outcome`
- `Summary`
- `Resolved Loops`
- `New Loops`
- `World Changes`
- `Rewards`
- `Consequences`
- `Suggested Follow-Up`

---

## Bundled Helpers

- `scripts/bootstrap_state.py`
  Initializes encounter manager state from templates.
- `scripts/validate_state.py`
  Validates required files and key identifiers.
- `scripts/prepare_encounter.py`
  Builds scene state and normalized action objects from inputs.
- `scripts/resolve_encounter.py`
  Resolves actions into a structured result and markdown export.

---

## Reference Files

Load these as needed:

- `references/DATA_MODEL.md`
- `references/RESOLUTION_RULES.md`
- `references/TWIST_GUIDELINES.md`
- `references/TRANSCRIPT_EXAMPLE.md`
