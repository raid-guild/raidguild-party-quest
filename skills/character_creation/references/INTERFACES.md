# Interfaces

## Downstream Export

The Campaign Manager expects a concise markdown file compatible with its `state/inputs/known_characters.md` contract.

Write the export to:

- `state/handoffs/known_characters.md`

This path is local to the character-creation skill folder.

Do not move the canonical draft or handoff to a repo-level shared state directory.

Recommended shape:

```md
# Known Characters

## Party
- Rowan Vale | quiet scout | find where the whispers begin | never misses a hidden route

## Character Sheets

### CHAR-001 - Rowan Vale
- Concept: Careful pathfinder who trusts patterns more than people.
- Role: scout
- Drive: Trace the source of a recurring signal.
- Fear: Becoming part of the phenomenon they are tracking.
- Edge: Reads unstable environments quickly.
- Flaw: Keeps too much to themself.
```

The first `## Party` section is the critical one. Keep entries concise and pipe-delimited.

## Upstream Inputs

`campaign_brief.md` and `player_preferences.md` are freeform. The skill should extract:
- tone
- setting hints
- role preferences
- desired complexity
- any red lines or no-go themes
