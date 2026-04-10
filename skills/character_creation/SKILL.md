---
name: character_creation
description: Create and revise a setting-agnostic player character draft through focused conversation, maintain a structured JSON object, and export a campaign-manager-compatible known characters handoff.
---

# Character Creation Skill

## Purpose

Guide the user through creating a minimal but playable character draft for a story-first multiplayer campaign.

Own:
- character concept intake
- draft JSON state
- core identity, motivation, and friction
- concise handoff exports for downstream skills

Do not own:
- long-term campaign planning
- encounter resolution
- world canon outside the character draft
- deep rules simulation

This skill is setting-agnostic and should not assume fantasy, sci-fi, or any specific game system unless the user provides one.

---

## Core Behavior

- Ask one focused question at a time unless the user already supplied several details.
- Parse compact answers and fill as many fields as possible.
- Keep language clear and beginner-friendly.
- Offer short recommendations when the user is unsure.
- Keep optional flavor details for later.
- Recompute derived summary fields after every meaningful update.
- Support:
  - `show summary`
  - `show json`
  - `change X to Y`
  - `skip this`
  - `finish with defaults`

---

## Canonical State Files

Maintain these files as the source of truth:

- `state/outputs/character_draft.json`
- `state/outputs/party_brief.md`
- `state/handoffs/known_characters.md`
- `state/logs/change_log.md`
- `state/runtime/session_state.json`

Input files:
- `state/inputs/campaign_brief.md`
- `state/inputs/player_preferences.md`

All state for this skill is self-contained inside this skill folder under `state/`.

Do not assume a repo-level shared `state/` directory.

If another skill needs this output, it should read or copy the exported handoff from this skill folder.

If state files are missing, initialize them instead of failing.

---

## Required Workflow Modes

### 1) Bootstrap Character Draft
Use when the skill has not been initialized yet.

Steps:
1. Read `campaign_brief.md` if present
2. Read `player_preferences.md` if present
3. Create the JSON draft and starter markdown files
4. Export `state/handoffs/known_characters.md`
5. Log initialization

### 2) Build Or Update Character
Use whenever the user provides character details or changes an earlier choice.

Steps:
1. Read the current JSON draft
2. Update the relevant fields
3. Recompute derived summary fields
4. Flag downstream inconsistencies if any appear
5. Refresh the handoff markdown
6. Log changes if the draft materially changed

### 3) Finish With Defaults
Use when the user wants a quick playable draft.

Steps:
1. Fill missing core fields with conservative defaults
2. Keep the concept coherent with provided tone and preferences
3. Recompute derived fields
4. Export the refreshed handoff

### 4) Recap
Return:
- a short summary
- missing fields if any remain
- the current JSON if requested

---

## Data Model

The canonical JSON draft should keep these fields:

- `character_id`
- `status`
- `name`
- `concept`
- `role`
- `tone_tags`
- `core_traits`
- `drive`
- `fear`
- `edge`
- `flaw`
- `relationships`
- `starter_gear`
- `notes`
- `derived`

Derived fields should include:
- `one_line_pitch`
- `campaign_hook`
- `notable_edge`

Keep the JSON compact and readable.

---

## Handoff Contract

The handoff for the Campaign Manager should be written to:

- `state/handoffs/known_characters.md`

Include:
- one `## Party` section with concise pipe-delimited party entries
- a short `## Character Sheets` section with richer detail
- optional `## Important NPCs` notes only if the user explicitly created them

The downstream Campaign Manager only needs a clean, concise summary of who the party is and what tension they bring into the story.

---

## Writing Style

When guiding the user:
- be warm and direct
- avoid jargon unless the user is already using it
- keep questions short

When writing canonical state:
- prefer compact JSON and bullet summaries
- avoid ornamental prose
- optimize for downstream agent readability

---

## Bundled Helpers

- `scripts/bootstrap_state.py`
  Initializes the starter state files from templates.
- `scripts/update_character.py`
  Updates the JSON draft, recomputes derived fields, and refreshes exports.
- `scripts/validate_character.py`
  Validates the draft shape and required fields.
- `scripts/render_handoff.py`
  Renders markdown exports from the canonical JSON draft.

Use the scripts when repetitive state maintenance is easier to keep deterministic than doing it manually.

---

## Reference Files

Use these only when needed:

- `references/STATE_MODEL.md`
- `references/INTERFACES.md`
- `references/JSON_SCHEMA.md`
- `references/CONVERSATION_GUIDELINES.md`
- `references/STEP_FLOW.json`
- `references/SESSION_STATE_SCHEMA.json`
