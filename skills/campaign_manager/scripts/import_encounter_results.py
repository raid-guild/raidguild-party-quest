#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read(path: Path) -> str:
    return path.read_text()


def write(path: Path, text: str) -> None:
    path.write_text(text if text.endswith("\n") else text + "\n")


def next_numeric_id(prefix: str, text: str) -> str:
    values = [int(match) for match in re.findall(rf"{prefix}-(\d+)", text)]
    return f"{prefix}-{(max(values) if values else 0) + 1:03d}"


def extract_value(text: str, label: str, fallback: str) -> str:
    match = re.search(rf"^- {re.escape(label)}: (.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def extract_section(text: str, heading: str) -> list[str]:
    pattern = rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return []
    lines = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped and stripped.startswith("- "):
            lines.append(stripped)
    return lines


def append_after_heading(text: str, heading: str, bullet: str) -> str:
    pattern = rf"(^## {re.escape(heading)}\n)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        suffix = "" if text.endswith("\n") else "\n"
        return f"{text}{suffix}\n## {heading}\n\n{bullet}\n"
    insert_at = match.end()
    return f"{text[:insert_at]}\n{bullet}{text[insert_at:]}"


def mark_resolved(open_loops_text: str, loop_id: str, timestamp: str) -> str:
    pattern = re.compile(rf"^- \[open\] {re.escape(loop_id)} \| ([^\n]+)$", re.MULTILINE)
    open_loops_text = pattern.sub(
        lambda m: f"- [resolved] {loop_id} | {m.group(1).split('|')[0].strip()} | resolved: {timestamp}",
        open_loops_text,
    )
    if loop_id not in open_loops_text:
        open_loops_text = append_after_heading(open_loops_text, "Resolved", f"- [resolved] {loop_id} | Imported as resolved | resolved: {timestamp}")
    return open_loops_text


def add_new_loop(open_loops_text: str, bullet: str) -> str:
    loop_id = bullet[2:].split("|", 1)[0].strip()
    if loop_id in open_loops_text:
        return open_loops_text
    line = bullet if bullet.startswith("- [open] ") else bullet.replace("- ", "- [open] ", 1)
    return append_after_heading(open_loops_text, "Active", line)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import structured encounter results into campaign state.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    results_path = args.root / "state/inputs/encounter_results.md"
    queue_path = args.root / "state/campaign/encounter_queue.md"
    handoff_path = args.root / "state/handoffs/next_encounter.md"
    open_loops_path = args.root / "state/campaign/open_loops.md"
    timeline_path = args.root / "state/campaign/timeline.md"
    world_state_path = args.root / "state/campaign/world_state.md"
    current_arc_path = args.root / "state/campaign/current_arc.md"
    session_log_path = args.root / "state/logs/session_log.md"
    change_log_path = args.root / "state/logs/change_log.md"

    results = read(results_path)
    queue = read(queue_path)
    open_loops_text = read(open_loops_path)
    timeline = read(timeline_path)
    world_state = read(world_state_path)
    current_arc = read(current_arc_path)
    session_log = read(session_log_path)
    change_log = read(change_log_path)

    encounter_id = extract_value(results, "Encounter ID", "TP-000")
    session_id = extract_value(results, "Session ID", next_numeric_id("SESSION", session_log))
    timestamp = extract_value(results, "Timestamp", now_iso())
    outcome = extract_value(results, "Outcome", "unknown")
    summary = extract_value(results, "Summary", "Encounter results imported.")
    suggested_follow_up = extract_section(results, "Suggested Follow-Up")
    new_loops = extract_section(results, "New Loops")
    resolved_loops = extract_section(results, "Resolved Loops")
    world_changes = extract_section(results, "World Changes")
    rewards = extract_section(results, "Rewards")
    consequences = extract_section(results, "Consequences")

    for item in resolved_loops:
        loop_id = item[2:].split("|", 1)[0].strip()
        if loop_id != "LOOP-000":
            open_loops_text = mark_resolved(open_loops_text, loop_id, timestamp)

    for item in new_loops:
        loop_id = item[2:].split("|", 1)[0].strip()
        if loop_id != "LOOP-000":
            open_loops_text = add_new_loop(open_loops_text, item)

    follow_up_text = suggested_follow_up[0][2:] if suggested_follow_up else summary
    touchpoint_id = next_numeric_id("TP", queue)
    arc_id = extract_value(current_arc, "Arc ID", "ARC-001")
    title = follow_up_text[:72].rstrip(".")
    primary_hook = new_loops[0][2:] if new_loops and "LOOP-000" not in new_loops[0] else follow_up_text

    touchpoint = f"""## {touchpoint_id} - {title}
- Arc ID: {arc_id}
- Type: consequence
- Trigger: The fallout from {encounter_id} creates immediate new motion.
- Location: LOC-001
- Involved Characters: party, FACTION-001
- Premise: Consequences from the last encounter force the next scene into view.
- Narrative Purpose: Convert the encounter outcome into campaign momentum.
- Stakes: The party must capitalize before the opposition adapts.
- Opposition: New pressure, damaged trust, or exposed leverage
- Recommended Difficulty: medium
- Twist or Reveal: The cleanest next lead also carries the clearest risk.
- Reward or Consequence: The party can seize initiative or cede it.
- Aftermath Hooks: {primary_hook}
- Handoff Notes: Carry forward unresolved tension from {encounter_id}.
"""

    handoff = f"""# Next Encounter Handoff

- Generated: {timestamp}
- Selected Touchpoint ID: {touchpoint_id}
- Arc ID: {arc_id}
- Priority: primary

## Scene Frame

- Title: {title}
- Trigger: The fallout from {encounter_id} creates immediate new motion.
- Location: LOC-001
- Involved Characters: party, FACTION-001

## Run This Scene For

- Pay off the consequences of {encounter_id}.
- Pressure the newest open loop or follow-up lead.
- Make the world feel reactive to the prior result.

## Stakes

- Delay gives the opposition time to harden its position.

## Opposition

- New pressure, damaged trust, or exposed leverage.

## On Success

- The party turns fallout into leverage.

## On Failure

- The world closes around the unresolved consequences.

## Aftermath Hooks

- {primary_hook}
"""

    queue = queue.rstrip() + "\n\n" + touchpoint + "\n"
    timeline = timeline.rstrip() + f"\n- {timestamp} | {encounter_id} | {summary}\n"
    current_arc = append_after_heading(current_arc, "Recent Developments", f"- {timestamp}: Imported {encounter_id} with outcome {outcome}.")
    if world_changes:
        for item in world_changes:
            world_state = append_after_heading(world_state, "Recent Changes", f"- {timestamp}: {item[2:]}")
    if consequences:
        for item in consequences:
            world_state = append_after_heading(world_state, "Recent Changes", f"- {timestamp}: consequence - {item[2:]}")

    session_entry = [
        f"## {session_id}",
        "",
        f"- Timestamp: {timestamp}",
        f"- Encounter ID: {encounter_id}",
        f"- Outcome: {outcome}",
        f"- Summary: {summary}",
    ]
    if rewards:
        session_entry.append(f"- Rewards: {'; '.join(item[2:] for item in rewards)}")
    if consequences:
        session_entry.append(f"- Consequences: {'; '.join(item[2:] for item in consequences)}")
    session_log = session_log.rstrip() + "\n\n" + "\n".join(session_entry) + "\n"

    change_log = change_log.rstrip() + (
        f"\n\n## {timestamp}\n\n"
        f"- Imported encounter results from {encounter_id}.\n"
        f"- Updated open loops, timeline, session log, and world state.\n"
        f"- Added follow-up touchpoint {touchpoint_id} and refreshed next encounter handoff.\n"
    )

    write(open_loops_path, open_loops_text)
    write(queue_path, queue)
    write(handoff_path, handoff)
    write(timeline_path, timeline)
    write(world_state_path, world_state)
    write(current_arc_path, current_arc)
    write(session_log_path, session_log)
    write(change_log_path, change_log)

    print(f"Imported {encounter_id} into campaign state")
    print(f"- Session: {session_id}")
    print(f"- New follow-up touchpoint: {touchpoint_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
