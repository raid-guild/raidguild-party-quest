#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "state/inputs/encounter_request.json",
    "state/inputs/raw_player_messages.md",
    "state/inputs/optional_rolls.json",
    "state/encounters/scene_state.json",
    "state/encounters/normalized_actions.json",
    "state/outputs/encounter_result.json",
    "state/outputs/encounter_results.md",
    "state/logs/change_log.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate encounter manager state.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = args.root
    errors = []

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            errors.append(f"missing: {rel}")

    request_path = root / "state/inputs/encounter_request.json"
    if request_path.exists():
        request = json.loads(request_path.read_text())
        for field in ["encounter_id", "campaign_id", "scene_id", "encounter_type", "difficulty", "objective"]:
            if field not in request:
                errors.append(f"encounter_request missing: {field}")

    result_path = root / "state/outputs/encounter_result.json"
    if result_path.exists():
        result = json.loads(result_path.read_text())
        if "encounter_id" not in result:
            errors.append("encounter_result missing encounter_id")

    print("Validation report")
    print(f"- Root: {root}")
    if errors:
        print("- Errors:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("- Status: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
