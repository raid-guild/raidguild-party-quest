# Core Policy

This file is the single source of truth for dice, NPC authority, pacing, and ending rules.

## Required Identifiers

- Every write must include `campaign_id`.
- Encounter and session writes must also include `session_id`.
- Scene writes must also include `scene_id`.
- If `campaign_id` is ambiguous, stop and ask.

## Canonical State Rules

- Canonical state lives under `workspace/state/campaigns/<campaign_id>/`.
- Append-only logs are source of truth for actual play.
- Snapshot files summarize current state and may be rebuilt from logs.
- Skill-local `state/` folders are working areas, not canonical campaign history.

## Campaign And Session Lifecycle

Allowed lifecycle states:

- `active`
- `paused`
- `closed`
- `abandoned`
- `superseded`

Use them this way:

- `active`: the current campaign or session is in play
- `paused`: the group intends to resume later
- `closed`: the campaign or session ended cleanly
- `abandoned`: the group stopped and does not appear to intend to resume
- `superseded`: the group started another campaign and the old one is no longer current

Lifecycle control rules:

- If players explicitly say they want to stop for now, mark `paused`.
- If players explicitly end the campaign, mark `closed`.
- If players clearly move on and do not intend to resume, mark `abandoned`.
- If a new campaign replaces the old active one, mark the old one `superseded`.
- Do not leave an inactive campaign pretending to be the active one.

## Encounter Order

Every uncertain turn must follow this order:

1. `STATE READ`
2. `ROLL`
3. `STATE UPDATE`
4. `EVENT LOG APPEND`
5. `CHAT OUTPUT`

If step 3 or 4 fails, the turn is not resolved.

## Message Classification

Classify chat into exactly one of:

- `ooc_chat`
- `ooc_command`
- `ic_action`

Rules:

- `ooc_chat` is side chatter, jokes, planning, or reactions. Do not resolve it as an in-fiction action.
- `ooc_command` is direct table or GM control such as pause, resume, recap, switch campaign, or end campaign.
- `ic_action` is in-fiction intent that may trigger scene or encounter handling.

OOC detection cues:

- messages beginning with `OOC:`
- messages beginning with `(OOC)`
- messages wrapped in `[[ ... ]]`
- direct table-talk like "pause here", "can we resume tomorrow", "what campaign are we in", or "let's start a different one"

Only `ic_action` should enter encounter normalization and roll handling.
`ooc_command` may create admin events such as `session_paused`, `session_closed`, or `campaign_switched`.
Plain `ooc_chat` should not create beat-resolution events.

## Dice Policy

- Roll when an action is risky, opposed, time-sensitive, or consequence-bearing.
- Do not free-narrate a risky success or failure when policy requires a roll.
- Use approved player rolls when present.
- Otherwise use the approved script method.
- One primary action maps to one primary roll unless a move explicitly says otherwise.

## NPC Authority

- Major NPC actions must update structured state first.
- Offscreen NPC moves are allowed only when logged.
- Do not invent a major reversal without a state update.

## Scene Pacing

Each active scene must track:

- `objective`
- `beat_count`
- `beat_cap`
- `must_escalate_at`
- `must_resolve_by`
- `spotlight_next`

Default pacing:

- Beat 1-2: establish and complicate
- Beat 3-4: escalate or reverse
- Beat 5: resolve or cliffhanger

If `beat_count` exceeds `beat_cap`, force a resolution or cliffhanger.

## Round Summaries

Every round must produce:

- round summary
- unresolved threads
- updated clocks
- NPC status changes
- spotlight-next
- canon ambiguity notes

## Ending Thresholds

Trigger finale pressure when one of these becomes true:

- current round reaches the finale round
- a critical clock caps out
- cumulative failures make delay no longer credible

Allowed endings:

- costly win
- clear loss
- unstable truce
- cliffhanger

## Canon And Confidence

Track:

- `canon_status`: `canon`, `provisional`, `disputed`
- `state_integrity`: `clean`, `partial`, `messy`

## Failure Behavior

- If `campaign_id` is missing or ambiguous, stop.
- If the roster is unclear, stop.
- If a required file is missing, scaffold it before continuing.
- If append-only logging fails, do not claim the beat resolved.
- If prompt prose conflicts with this file, follow this file.
- If chat is OOC, do not treat it as fiction.
