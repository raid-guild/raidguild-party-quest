# State Model

This skill stores campaign state in markdown files under `state/`.

## Canonical Files

- `state/campaign/overview.md`
  Campaign identity, premise, party summary, and current pressure.
- `state/campaign/current_arc.md`
  The single active arc, objective, antagonistic force, and next beats.
- `state/campaign/world_state.md`
  Facts about the world that have materially changed.
- `state/campaign/factions.md`
  Active factions, goals, leverage, and posture.
- `state/campaign/locations.md`
  Important places, status, and unresolved opportunities.
- `state/campaign/open_loops.md`
  Open, resolved, and dormant loops. Use stable loop IDs.
- `state/campaign/timeline.md`
  Timestamped macro events in campaign order.
- `state/campaign/encounter_queue.md`
  A queue of touchpoints for the encounter manager.
- `state/handoffs/next_encounter.md`
  The single encounter packet to hand to the encounter manager now.
- `state/logs/session_log.md`
  Session-level summaries and imported encounter notes.
- `state/logs/change_log.md`
  Audit trail for campaign-level edits.

## File Conventions

- Use markdown headings with short bullet lists underneath.
- Keep stable IDs in uppercase form like `ARC-001`, `TP-004`, `LOOP-002`.
- Append dated entries instead of silently deleting old information.
- Mark superseded material explicitly with `Superseded by:` or `Status: resolved`.
- Use ISO-8601 UTC timestamps when scripts write to files.

## Open Loop Format

Use one bullet per loop in `state/campaign/open_loops.md`:

```md
- [open] LOOP-001 | Recover the missing sigil | owner: party | pressure: medium | next: inspect the river shrine
- [resolved] LOOP-002 | Learn who hired the bandits | resolved: 2026-04-10T18:00:00Z
```

The scripts expect:
- a status in square brackets
- a stable loop ID
- a short summary

## Touchpoint Format

Each touchpoint in `state/campaign/encounter_queue.md` is a `## TP-...` section with fields described in `references/TOUCHPOINT_SCHEMA.md`.
