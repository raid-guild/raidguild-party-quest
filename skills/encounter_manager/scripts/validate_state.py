#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "active/encounter_request.json",
    "active/raw_player_messages.md",
    "active/optional_rolls.json",
    "active/scene.json",
    "active/normalized_actions.json",
    "logs/event-log.jsonl",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate shared encounter state.")
    parser.add_argument("--campaign-id", required=True)
    args = parser.parse_args()

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    errors = []

    for rel in REQUIRED_FILES:
        path = campaign_root / rel
        if not path.exists():
            errors.append(f"missing: {rel}")

    request_path = campaign_root / "active/encounter_request.json"
    if request_path.exists():
        request = json.loads(request_path.read_text())
        for field in ["campaign_id", "session_id", "scene_id", "encounter_type", "difficulty", "objective"]:
            if field not in request:
                errors.append(f"encounter_request missing: {field}")
        if request.get("campaign_id") != args.campaign_id:
            errors.append("encounter_request campaign_id mismatch")

    scene_path = campaign_root / "active/scene.json"
    if scene_path.exists():
        scene = json.loads(scene_path.read_text())
        for field in ["campaign_id", "session_id", "scene_id", "beat_count", "beat_cap"]:
            if field not in scene:
                errors.append(f"scene missing: {field}")

    print("Validation report")
    print(f"- Campaign root: {campaign_root}")
    if errors:
        print("- Errors:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("- Status: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
