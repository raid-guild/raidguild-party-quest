#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


APPROACH_KEYWORDS = {
    "force": ["attack", "break", "threaten", "push", "strike", "intimidate", "fight"],
    "finesse": ["sneak", "slip", "pick", "precise", "careful", "quiet", "stealth"],
    "charm": ["convince", "persuade", "reassure", "bluff", "talk", "trust"],
    "insight": ["read", "study", "observe", "inspect", "notice", "analyze"],
    "weird": ["whisper", "magic", "strange", "ritual", "improvise", "weird"],
    "support": ["help", "assist", "cover", "protect", "back up", "support"],
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def detect_approach(message: str) -> str:
    lower = message.lower()
    for approach, keywords in APPROACH_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return approach
    return "insight"


def detect_risk(message: str) -> str:
    lower = message.lower()
    if any(word in lower for word in ["reckless", "charge", "all in", "risk everything"]):
        return "reckless"
    if any(word in lower for word in ["bold", "push hard", "force it"]):
        return "bold"
    if any(word in lower for word in ["careful", "slowly", "quietly", "cautious"]):
        return "cautious"
    return "standard"


def derive_tension(difficulty: str) -> str:
    return {
        "easy": "low",
        "normal": "rising",
        "hard": "high",
        "deadly": "critical",
    }.get(difficulty, "rising")


def parse_messages(text: str) -> list[tuple[str, str]]:
    messages = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ") or ":" not in stripped:
            continue
        name, message = stripped[2:].split(":", 1)
        messages.append((name.strip(), message.strip()))
    return messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare encounter scene state and normalized actions.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = args.root
    request = load_json(root / "state/inputs/encounter_request.json")
    messages = parse_messages((root / "state/inputs/raw_player_messages.md").read_text())

    players = request.get("players", [])
    player_lookup = {player["name"]: player for player in players}

    scene_state = {
        "round": 1,
        "phase": "setup",
        "tension": derive_tension(request.get("difficulty", "normal")),
        "active_hazards": [tag for tag in request.get("environment", {}).get("tags", []) if tag in {"unstable", "fire", "water", "mist", "crowd"}],
        "active_opportunities": [tag for tag in request.get("environment", {}).get("tags", []) if tag in {"only-route-forward", "cover", "witness", "high-ground"}],
        "environment_changes": [],
        "unresolved_threads": request.get("prior_state_refs", []),
        "spotlight_order": [player.get("id") for player in players],
    }

    actions = []
    for name, message in messages:
        player = player_lookup.get(name, {})
        actions.append(
            {
                "player_id": player.get("id", name.upper().replace(" ", "-")),
                "approach": detect_approach(message),
                "intent": message,
                "target_id": request.get("npcs", [{}])[0].get("id") if request.get("npcs") else None,
                "uses_item_tag": None,
                "risk_level": detect_risk(message),
                "aiding_player_id": None,
            }
        )

    normalized = {
        "resolution_mode": "group" if len(actions) > 1 else "individual",
        "actions": actions,
    }

    write_json(root / "state/encounters/scene_state.json", scene_state)
    write_json(root / "state/encounters/normalized_actions.json", normalized)

    change_log_path = root / "state/logs/change_log.md"
    existing = change_log_path.read_text() if change_log_path.exists() else "# Change Log\n"
    existing = existing.rstrip() + "\n\n## prepare\n\n- Prepared scene state and normalized player actions.\n"
    change_log_path.write_text(existing + "\n")

    print("Prepared encounter inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
