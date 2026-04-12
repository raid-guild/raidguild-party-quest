#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize character creation state.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--campaign-id")
    parser.add_argument("--player-handle")
    parser.add_argument("--character-id", default="CHAR-001")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    generated_at = now_iso()
    root = args.root

    draft_path = root / "state/outputs/character_draft.json"
    if args.force or not draft_path.exists():
        draft = json.loads((root / "assets/templates/character_draft.template.json").read_text())
        draft["character_id"] = args.character_id
        draft_path.write_text(json.dumps(draft, indent=2) + "\n")

    session_state_path = root / "state/runtime/session_state.json"
    if args.force or not session_state_path.exists():
        session_state = json.loads((root / "assets/templates/session_state.template.json").read_text())
        session_state["characterDraft"] = json.loads(draft_path.read_text())
        session_state["campaignContext"] = {
            "campaign_id": args.campaign_id,
            "player_handle": args.player_handle,
        }
        session_state_path.write_text(json.dumps(session_state, indent=2) + "\n")

    campaign_brief_path = root / "state/inputs/campaign_brief.md"
    if args.force or not campaign_brief_path.exists():
        write(campaign_brief_path, (root / "assets/templates/campaign_brief.template.md").read_text())

    preferences_path = root / "state/inputs/player_preferences.md"
    if args.force or not preferences_path.exists():
        write(preferences_path, (root / "assets/templates/player_preferences.template.md").read_text())

    brief_text = (root / "assets/templates/party_brief.template.md").read_text().format(
        generated_at=generated_at,
        character_id=args.character_id,
        status="draft",
        name="Unnamed Character",
        role="undecided",
        one_line_pitch="A character draft has been initialized but not filled in yet.",
        drive="Not chosen yet.",
        fear="Not chosen yet.",
        edge="Not chosen yet.",
        flaw="Not chosen yet.",
    )
    handoff_text = (root / "assets/templates/known_characters.template.md").read_text().format(
        name="Unnamed Character",
        role="undecided",
        drive="motivation not chosen yet",
        notable_edge="edge not chosen yet",
        character_id=args.character_id,
        concept="Draft not initialized beyond the starter template.",
        fear="Not chosen yet.",
        edge="Not chosen yet.",
        flaw="Not chosen yet.",
        traits="none yet",
        starter_gear="none yet",
        notes="Use update_character.py or the skill conversation to fill this in.",
    )
    change_log_text = (root / "assets/templates/change_log.template.md").read_text().format(generated_at=generated_at)

    write(root / "state/outputs/party_brief.md", brief_text)
    write(root / "state/handoffs/known_characters.md", handoff_text)
    write(root / "state/logs/change_log.md", change_log_text)

    if args.campaign_id:
        shared_character_path = repo_root() / "workspace/state/campaigns" / args.campaign_id / "characters" / f"{args.character_id}.json"
        shared_character_path.parent.mkdir(parents=True, exist_ok=True)
        shared_character_path.write_text(draft_path.read_text())

    print("Initialized character creation state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
