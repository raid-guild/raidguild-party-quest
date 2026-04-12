#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


APPROACH_KEYWORDS = {
    "force": ["attack", "break", "threaten", "push", "strike", "intimidate", "fight"],
    "finesse": ["sneak", "slip", "pick", "precise", "careful", "quiet", "stealth"],
    "charm": ["convince", "persuade", "reassure", "bluff", "talk", "trust"],
    "insight": ["read", "study", "observe", "inspect", "notice", "analyze"],
    "weird": ["whisper", "magic", "strange", "ritual", "improvise", "weird"],
    "support": ["help", "assist", "cover", "protect", "back up", "support"],
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


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


def classify_message(message: str) -> str:
    stripped = message.strip()
    lower = stripped.lower()
    if stripped.startswith("[[") and stripped.endswith("]]"):
        return "ooc_chat"
    if lower.startswith("ooc:") or lower.startswith("(ooc)"):
        return "ooc_chat"
    if re.search(r"\b(pause|resume|recap|switch campaign|start another|end campaign|stop here)\b", lower):
        return "ooc_command"
    return "ic_action"


def append_event(path: Path, payload: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare encounter state in the shared campaign tree.")
    parser.add_argument("--campaign-id", required=True)
    args = parser.parse_args()

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    active_root = campaign_root / "active"
    request = load_json(active_root / "encounter_request.json")
    scene = load_json(active_root / "scene.json")
    messages = parse_messages((active_root / "raw_player_messages.md").read_text())

    players = request.get("players", [])
    player_lookup = {player["name"]: player for player in players if "name" in player}

    scene_state = {
        "campaign_id": request.get("campaign_id"),
        "session_id": request.get("session_id"),
        "scene_id": request.get("scene_id"),
        "objective": request.get("objective", ""),
        "status": "ready",
        "beat_count": scene.get("beat_count", 0),
        "beat_cap": scene.get("beat_cap", 5),
        "must_escalate_at": scene.get("must_escalate_at", 4),
        "must_resolve_by": scene.get("must_resolve_by", 5),
        "spotlight_next": scene.get("spotlight_next"),
        "tension": derive_tension(request.get("difficulty", "normal")),
        "active_hazards": [tag for tag in request.get("environment", {}).get("tags", []) if tag in {"unstable", "fire", "water", "mist", "crowd"}],
        "active_opportunities": [tag for tag in request.get("environment", {}).get("tags", []) if tag in {"only-route-forward", "cover", "witness", "high-ground"}],
        "environment_changes": [],
        "unresolved_threads": request.get("prior_state_refs", []),
        "spotlight_order": [player.get("id") for player in players],
    }

    actions = []
    ooc_messages = []
    admin_commands = []
    for name, message in messages:
        classification = classify_message(message)
        if classification == "ooc_chat":
            ooc_messages.append({"actor_name": name, "message": message})
            continue
        if classification == "ooc_command":
            admin_commands.append({"actor_name": name, "message": message})
            continue
        player = player_lookup.get(name, {})
        actions.append(
            {
                "player_id": player.get("id", name.upper().replace(" ", "-")),
                "actor_name": name,
                "message_class": classification,
                "approach": detect_approach(message),
                "intent": message,
                "risk_level": detect_risk(message),
                "roll_trigger": "risky_action",
            }
        )

    normalized = {
        "campaign_id": request.get("campaign_id"),
        "session_id": request.get("session_id"),
        "scene_id": request.get("scene_id"),
        "resolution_mode": "group" if len(actions) > 1 else "individual",
        "actions": actions,
        "ignored_ooc_chat": ooc_messages,
        "admin_commands": admin_commands,
    }

    write_json(active_root / "scene.json", scene_state)
    write_json(active_root / "normalized_actions.json", normalized)

    append_event(
        campaign_root / "logs/event-log.jsonl",
        {
            "ts": request.get("session_id"),
            "campaign_id": request.get("campaign_id"),
            "session_id": request.get("session_id"),
            "scene_id": request.get("scene_id"),
            "type": "scene_prepared",
            "beat_count": scene_state["beat_count"],
            "objective": scene_state["objective"],
            "action_count": len(actions),
            "ignored_ooc_count": len(ooc_messages),
            "admin_command_count": len(admin_commands),
        },
    )

    for command in admin_commands:
        append_event(
            campaign_root / "logs/event-log.jsonl",
            {
                "ts": request.get("session_id"),
                "campaign_id": request.get("campaign_id"),
                "session_id": request.get("session_id"),
                "scene_id": request.get("scene_id"),
                "type": "ooc_command_detected",
                "beat_count": scene_state["beat_count"],
                "actor_name": command["actor_name"],
                "message": command["message"],
            },
        )

    print("Prepared encounter inputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
