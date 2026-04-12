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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def has_non_placeholder_opening(path: Path) -> bool:
    if not path.exists():
        return False
    text = path.read_text()
    blocked = [
        "The setting should be introduced in 2-3 vivid sentences before live play starts.",
        "Something urgent is already in motion.",
        "Frame the first scene with:",
    ]
    return not any(marker in text for marker in blocked)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate whether a campaign is ready to start Round 1.")
    parser.add_argument("--campaign-id", required=True)
    args = parser.parse_args()

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    players = load_json(campaign_root / "players.json")
    readiness_path = campaign_root / "readiness.json"
    readiness = load_json(readiness_path)

    player_rows = players.get("players", [])
    required_players = [
        player for player in player_rows
        if player.get("status") not in {"absent", "dropped"} and player.get("handle")
    ]
    characters_root = campaign_root / "characters"
    players_ready = []
    missing_characters = []

    for player in required_players:
        character_id = player.get("character_id")
        handle = player.get("handle")
        if character_id and (characters_root / f"{character_id}.json").exists():
            players_ready.append(handle)
        else:
            missing_characters.append(handle)

    roster_confirmed = bool(required_players)
    start_short = bool(players.get("start_short_handed_allowed", False))
    opening_ready = has_non_placeholder_opening(campaign_root / "opening_brief.md")
    round_1_ready = opening_ready and roster_confirmed and (
        not missing_characters or start_short
    )

    readiness.update(
        {
            "campaign_id": args.campaign_id,
            "opening_brief_ready": opening_ready,
            "roster_confirmed": roster_confirmed,
            "required_players": [player.get("handle") for player in required_players],
            "players_ready": players_ready,
            "players_missing_characters": missing_characters,
            "start_short_handed_allowed": start_short,
            "round_1_ready": round_1_ready,
            "updated_at": now_iso(),
        }
    )
    write_json(readiness_path, readiness)
    print(f"Round 1 ready: {'yes' if round_1_ready else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
