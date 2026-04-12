#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def write_json(path: Path, payload: object, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return True


def write_text(path: Path, text: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize shared encounter state.")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--scene-id", default="scene-001")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    ts = now_iso()
    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    active_root = campaign_root / "active"
    written: list[str] = []

    files = {
        active_root / "encounter_request.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "scene_id": args.scene_id,
            "encounter_type": "narrative",
            "objective": "",
            "difficulty": "normal",
            "players": [],
            "npcs": [],
            "environment": {"tags": []},
        },
        active_root / "optional_rolls.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "rolls": {},
        },
        active_root / "scene.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "scene_id": args.scene_id,
            "objective": "",
            "status": "setup",
            "beat_count": 0,
            "beat_cap": 5,
            "must_escalate_at": 4,
            "must_resolve_by": 5,
            "spotlight_next": None,
            "tension": "rising",
            "updated_at": ts,
        },
        active_root / "normalized_actions.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "scene_id": args.scene_id,
            "resolution_mode": "group",
            "actions": [],
        },
    }

    for path, payload in files.items():
        if write_json(path, payload, args.force):
            written.append(str(path.relative_to(repo_root())))

    if write_text(active_root / "raw_player_messages.md", "# Raw Player Messages\n", args.force):
        written.append(str((active_root / "raw_player_messages.md").relative_to(repo_root())))

    print("Initialized shared encounter state:")
    for item in written:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
