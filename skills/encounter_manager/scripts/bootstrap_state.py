#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


TEXT_TEMPLATES = {
    "assets/templates/raw_player_messages.template.md": "state/inputs/raw_player_messages.md",
    "assets/templates/encounter_results.template.md": "state/outputs/encounter_results.md",
    "assets/templates/change_log.template.md": "state/logs/change_log.md",
}

JSON_TEMPLATES = {
    "assets/templates/encounter_request.template.json": "state/inputs/encounter_request.json",
    "assets/templates/optional_rolls.template.json": "state/inputs/optional_rolls.json",
    "assets/templates/scene_state.template.json": "state/encounters/scene_state.json",
    "assets/templates/normalized_actions.template.json": "state/encounters/normalized_actions.json",
    "assets/templates/encounter_result.template.json": "state/outputs/encounter_result.json",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize encounter manager state.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = args.root
    timestamp = now_iso()

    for src, dest in JSON_TEMPLATES.items():
        src_path = root / src
        dest_path = root / dest
        if args.force or not dest_path.exists():
            write(dest_path, src_path.read_text())

    for src, dest in TEXT_TEMPLATES.items():
        dest_path = root / dest
        if not args.force and dest_path.exists():
            continue
        template = (root / src).read_text()
        if dest.endswith("encounter_results.md"):
            text = template.format(
                encounter_id="TP-001",
                session_id="SESSION-001",
                timestamp=timestamp,
                outcome="pending",
                summary="Encounter output has not been generated yet.",
                resolved_loops="",
                new_loops="",
                world_changes="",
                rewards="",
                consequences="",
                suggested_follow_up="",
            )
        elif dest.endswith("change_log.md"):
            text = template.format(generated_at=timestamp)
        else:
            text = template
        write(dest_path, text)

    print("Initialized encounter manager state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
