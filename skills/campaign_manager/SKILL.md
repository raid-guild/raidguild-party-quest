---
name: campaign_manager
description: Manages long-form agentic RPG campaign state, narrative arcs, open loops, and encounter touchpoints. Use when bootstrapping a campaign, advancing story state, absorbing encounter results, or preparing a handoff for the encounter manager.
---

# Campaign Manager Skill

## Purpose

Manage the macro-level campaign layer for an agentic roleplaying game.

Own:
- campaign state
- narrative progression
- world state
- open story loops
- encounter touchpoints
- handoff packets for the encounter manager

Do not own:
- character creation
- encounter resolution
- tactical combat adjudication
- deterministic dice logic
- final canonical character sheets if another skill owns them

This skill works with external skills:
1. Character Creation
2. Encounter Manager

---

## Core Mental Model

Treat the game as three layers:

1. **Characters**  
   Provided by the Character Creation skill. Treat them as inputs.

2. **Campaign / Narrative Road**  
   Owned by this skill. Maintain the road, pacing, stakes, progression, and continuity.

3. **Encounters / Tall Grass**  
   Owned by the Encounter Manager. Create encounter touchpoints, but do not resolve them here.

---

## State Rules

Store canonical campaign state in markdown files.

All canonical state for this skill lives inside this skill folder under `state/`.

Do not assume a repo-level shared `state/` directory.

If another skill needs data from this one, exchange it through explicit handoff files or copied exports between skill folders.

Prefer:
- append-only logs
- derived summaries
- stable IDs
- explicit supersession instead of silent deletion

Use stable IDs such as:
- `CAMPAIGN-001`
- `ARC-001`
- `TP-001`
- `NPC-001`
- `FACTION-001`
- `LOC-001`
- `SESSION-001`

Use ISO timestamps where possible.

If state files are missing, initialize them rather than failing.

---

## Canonical State Files

Maintain these files as the source of truth:

- `state/campaign/overview.md`
- `state/campaign/current_arc.md`
- `state/campaign/world_state.md`
- `state/campaign/factions.md`
- `state/campaign/locations.md`
- `state/campaign/open_loops.md`
- `state/campaign/timeline.md`
- `state/campaign/encounter_queue.md`
- `state/handoffs/next_encounter.md`
- `state/logs/session_log.md`
- `state/logs/change_log.md`

Input files from other skills:
- `state/inputs/known_characters.md`
- `state/inputs/world_seed.md`
- `state/inputs/encounter_results.md`

---

## Required Workflow Modes

### 1) Bootstrap Campaign
Use when the campaign does not yet exist.

Steps:
1. Read `known_characters.md` if present
2. Read `world_seed.md` if present
3. Create campaign overview, arc, world state, factions, locations, open loops, timeline, and encounter queue
4. Seed 3-5 viable encounter touchpoints
5. Write `state/handoffs/next_encounter.md`
6. Log initialization in `state/logs/change_log.md`

### 2) Advance Narrative
Use when the user wants “what happens next” or the campaign needs progression.

Steps:
1. Read overview, current arc, open loops, encounter queue, and latest session log
2. Advance the current arc
3. Update world pressure if appropriate
4. Refresh encounter queue
5. Write the next handoff packet
6. Log changes

### 3) Absorb Encounter Outcome
Use after the encounter manager returns a result.

Steps:
1. Read `state/inputs/encounter_results.md`
2. Update timeline, logs, arc, world state, and open loops
3. Close resolved loops
4. Create new loops caused by consequences
5. Refresh the next encounter handoff
6. Log the transition

### 4) Recap / Briefing
Use when a concise summary is needed.

Return:
- current campaign status
- active arc
- unresolved loops
- current encounter queue
- next likely scene

---

## Encounter Touchpoint Contract

A touchpoint is not a full encounter.

It is a structured opportunity that the encounter manager can turn into a scene.

Each touchpoint should include:
- `id`
- `title`
- `arc_id`
- `type`
- `trigger`
- `location`
- `involved_characters`
- `premise`
- `narrative_purpose`
- `stakes`
- `opposition`
- `recommended_difficulty`
- `twist_or_reveal` if relevant
- `reward_or_consequence`
- `aftermath_hooks`
- `handoff_notes`

Good touchpoints:
- connect to an existing thread
- create a meaningful choice
- are concrete enough to run
- do not pre-resolve the outcome

---

## Narrative Heuristics

Follow these rules unless the user says otherwise:

- Keep 1 primary arc active
- Keep 2-4 open loops alive
- Escalate pressure gradually
- Tie new beats back to prior events
- Favor consequence-bearing choices over random filler
- Avoid disconnected encounters unless the campaign explicitly wants that feel
- Preserve continuity across sessions

When appropriate:
- foreshadow later scenes
- reuse names, places, and unresolved tensions
- make the world feel reactive to player actions

---

## Writing Style

When writing canonical state:
- be concise
- be concrete
- use bullets and clear headings
- avoid ornamental prose
- optimize for agent readability

When writing player-facing narrative:
- be vivid enough to feel alive
- but keep the underlying state precise

---

## Reference Files

Keep supporting detail one level deep from this file.

Suggested references:
- `references/STATE_MODEL.md`
- `references/INTERFACES.md`
- `references/TOUCHPOINT_SCHEMA.md`
- `references/NARRATIVE_GUIDELINES.md`

Keep these files focused and easy to scan.

---

## Bundled Helpers

Use scripts when they reduce token use or make a repetitive file update deterministic.

- `scripts/bootstrap_state.py`
  Initializes the canonical state tree from the bundled templates.
- `scripts/validate_state.py`
  Checks that required files exist and that key IDs line up.
- `scripts/advance_campaign.py`
  Advances the campaign one macro beat, refreshes the encounter queue, and rewrites the next handoff.
- `scripts/import_encounter_results.py`
  Absorbs a structured encounter result packet into campaign state.

Prefer the scripts for routine state maintenance. If the user needs a bespoke narrative direction, reason in-context and then update the canonical files directly.

---

## Input Contracts

When input files use the bundled starter format, follow it exactly.

- For canonical file structure and section names, read `references/STATE_MODEL.md`.
- For file-to-file contracts with other skills, read `references/INTERFACES.md`.
- For touchpoint fields and required IDs, read `references/TOUCHPOINT_SCHEMA.md`.
- For pacing, escalation, and continuity guidance, read `references/NARRATIVE_GUIDELINES.md`.

---

## File Update Policy

When this skill changes state:
1. Update the relevant canonical markdown files
2. Append a short note to `state/logs/change_log.md`
3. Append session-level progress to `state/logs/session_log.md` if the campaign advanced
4. Refresh `state/handoffs/next_encounter.md` if the next scene changed

Do not leave the handoff packet stale after a material story change.

---

## First Action on Invocation

On every invocation:
1. Determine the mode: bootstrap, advance, absorb-result, or recap
2. Read the minimum relevant state files
3. Update only what is necessary
4. Return a concise summary of:
   - what changed
   - current narrative status
   - next likely encounter touchpoint

If state is missing, initialize it.
