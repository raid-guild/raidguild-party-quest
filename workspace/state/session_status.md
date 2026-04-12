# Legacy Session Status

- Updated: 2026-04-10T19:42:51Z
- Campaign Status: onboarding
- Current Round: 0
- Pressure: 1
- Finale Triggered: no
- Ending Mode: cliffhanger
- Default Arc Length: 5

## Round Framework

- 0 = onboarding / character creation
- 1 = inciting trouble
- 2 = complication
- 3 = reversal
- 4 = escalation
- 5 = finale

## Current Goal

- Migrate active play into `workspace/state/campaigns/<campaign_id>/campaign.json`.

## Transition Rules

- Move to round 1 only when the roster is confirmed and all active players are ready.
- Trigger the finale when current round reaches 5 or pressure reaches 5.

## Ending Checklist Pointer

- Use `workspace/FINALE_CHECKLIST.md` when entering round 5 or epilogue framing.

## Migration Note

- This file is now a lobby-era summary only.
- Canonical round and pressure state belong inside each campaign folder.
