#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


VALID_STATUSES = {"invited", "building", "ready", "absent", "dropped"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Register or update a player in shared campaign state.")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--handle", required=True)
    parser.add_argument("--display-name")
    parser.add_argument("--status", default="invited")
    parser.add_argument("--character-id")
    parser.add_argument("--character-name")
    parser.add_argument("--notes", default="")
    parser.add_argument("--allow-short", action="store_true")
    args = parser.parse_args()

    if args.status not in VALID_STATUSES:
        raise SystemExit(f"invalid status: {args.status}")

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    players_path = campaign_root / "players.json"
    players = load_json(players_path)
    rows = players.get("players", [])

    match = None
    for player in rows:
        if player.get("handle") == args.handle:
            match = player
            break

    if match is None:
        match = {
            "handle": args.handle,
            "display_name": args.display_name or args.handle,
            "status": args.status,
            "character_id": args.character_id,
            "character_name": args.character_name,
            "notes": args.notes,
        }
        rows.append(match)
    else:
        match["display_name"] = args.display_name or match.get("display_name") or args.handle
        match["status"] = args.status or match.get("status", "invited")
        if args.character_id:
            match["character_id"] = args.character_id
        if args.character_name:
            match["character_name"] = args.character_name
        if args.notes:
            match["notes"] = args.notes

    players["players"] = rows
    if args.allow_short:
        players["start_short_handed_allowed"] = True
    players["updated_at"] = now_iso()
    write_json(players_path, players)

    print(f"Updated player {args.handle} in {args.campaign_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
