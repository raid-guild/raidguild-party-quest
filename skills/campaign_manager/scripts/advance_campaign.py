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


def extract_line(text: str, pattern: str, fallback: str) -> str:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def escalate(level: str) -> str:
    order = ["low", "medium", "high", "critical"]
    try:
        return order[min(order.index(level.lower()) + 1, len(order) - 1)]
    except ValueError:
        return "medium"


def append_after_heading(text: str, heading: str, bullet: str) -> str:
    pattern = rf"(^## {re.escape(heading)}\n)"
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        suffix = "" if text.endswith("\n") else "\n"
        return f"{text}{suffix}\n## {heading}\n\n{bullet}\n"
    insert_at = match.end()
    return f"{text[:insert_at]}\n{bullet}{text[insert_at:]}"


def active_loops(text: str) -> list[tuple[str, str, str]]:
    loops = []
    pattern = re.compile(r"^- \[open\] (LOOP-\d+) \| ([^|]+?)(?: \|.*? next: ([^\n]+))?$", re.MULTILINE)
    for loop_id, summary, next_step in pattern.findall(text):
        loops.append((loop_id.strip(), summary.strip(), next_step.strip() if next_step else "follow the freshest lead"))
    return loops


def main() -> int:
    parser = argparse.ArgumentParser(description="Advance the campaign one macro beat.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    overview_path = args.root / "state/campaign/overview.md"
    current_arc_path = args.root / "state/campaign/current_arc.md"
    world_state_path = args.root / "state/campaign/world_state.md"
    open_loops_path = args.root / "state/campaign/open_loops.md"
    timeline_path = args.root / "state/campaign/timeline.md"
    queue_path = args.root / "state/campaign/encounter_queue.md"
    handoff_path = args.root / "state/handoffs/next_encounter.md"
    change_log_path = args.root / "state/logs/change_log.md"

    overview = read(overview_path)
    current_arc = read(current_arc_path)
    world_state = read(world_state_path)
    open_loops_text = read(open_loops_path)
    timeline = read(timeline_path)
    queue = read(queue_path)
    change_log = read(change_log_path)

    if "Status: scaffold" in queue or "Uninitialized" in overview:
        raise SystemExit("state appears uninitialized; run scripts/bootstrap_state.py first")

    timestamp = now_iso()
    arc_id = extract_line(current_arc, r"^- Arc ID: (ARC-\d+)\b", "ARC-001")
    arc_title = extract_line(current_arc, r"^- Title: (.+)$", "Current Arc")
    pressure = extract_line(overview, r"^- Level: ([a-zA-Z]+)$", "low")
    next_pressure = escalate(pressure)
    loop_items = active_loops(open_loops_text)
    loop_id, loop_summary, loop_next = loop_items[0] if loop_items else ("LOOP-999", "Unknown pressure point", "find a new lead")
    touchpoint_id = next_numeric_id("TP", queue)
    title = f"Pressure On {loop_summary}".replace("  ", " ")

    touchpoint = f"""## {touchpoint_id} - {title}
- Arc ID: {arc_id}
- Type: escalation
- Trigger: Time passes and the active pressure around {loop_id} starts narrowing the party's options.
- Location: LOC-001
- Involved Characters: party, FACTION-001, FACTION-002
- Premise: The world reacts to delay and forces the party to move on the current loop.
- Narrative Purpose: Advance {arc_title} through consequence-bearing pressure.
- Stakes: Lose initiative, secrecy, or a useful relationship if the party hesitates.
- Opposition: Agents acting with incomplete but dangerous information
- Recommended Difficulty: {next_pressure}
- Twist or Reveal: The opposition understands more about the party than expected.
- Reward or Consequence: Progress the loop or let the pressure network harden.
- Aftermath Hooks: {loop_next}
- Handoff Notes: Emphasize urgency and the cost of inaction.
"""

    queue = queue.rstrip() + "\n\n" + touchpoint + "\n"
    handoff = f"""# Next Encounter Handoff

- Generated: {timestamp}
- Selected Touchpoint ID: {touchpoint_id}
- Arc ID: {arc_id}
- Priority: primary

## Scene Frame

- Title: {title}
- Trigger: Time passes and the active pressure around {loop_id} starts narrowing the party's options.
- Location: LOC-001
- Involved Characters: party, FACTION-001, FACTION-002

## Run This Scene For

- Pressure the active loop: {loop_summary}
- Reveal what delay now costs.
- Set up the next hard choice.

## Stakes

- The party can lose initiative, secrecy, or goodwill.

## Opposition

- Agents acting with incomplete but dangerous information.

## On Success

- The party gains momentum and sharper insight into the pressure network.

## On Failure

- The opposition consolidates, and future scenes start under heavier scrutiny.

## Aftermath Hooks

- {loop_next}
"""

    overview = re.sub(r"(^- Level: ).+$", rf"\g<1>{next_pressure}", overview, flags=re.MULTILINE)
    overview = re.sub(r"(^- Updated: ).+$", rf"\g<1>{timestamp}", overview, flags=re.MULTILINE)
    current_arc = append_after_heading(current_arc, "Recent Developments", f"- {timestamp}: Pressure advanced on {loop_id} through {touchpoint_id}.")
    world_state = append_after_heading(world_state, "Recent Changes", f"- {timestamp}: Public pressure increased from {pressure} to {next_pressure}.")
    timeline = timeline.rstrip() + f"\n- {timestamp} | {touchpoint_id} | Campaign advanced around {loop_id}: {loop_summary}.\n"
    change_log = change_log.rstrip() + f"\n\n## {timestamp}\n\n- Advanced campaign pressure from {pressure} to {next_pressure}.\n- Added touchpoint {touchpoint_id} for {loop_id}.\n- Refreshed next encounter handoff.\n"

    write(overview_path, overview)
    write(current_arc_path, current_arc)
    write(world_state_path, world_state)
    write(timeline_path, timeline)
    write(queue_path, queue)
    write(handoff_path, handoff)
    write(change_log_path, change_log)

    print(f"Advanced campaign at {timestamp}")
    print(f"- New touchpoint: {touchpoint_id}")
    print(f"- Pressure: {pressure} -> {next_pressure}")
    print(f"- Focus loop: {loop_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
