#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


BASE_TARGETS = {"easy": 8, "normal": 12, "hard": 16, "deadly": 18}
TWISTS = {
    "social": "hidden witness",
    "hazard": "secondary collapse",
    "combat": "exposed weakness",
    "mystery": "clue reveal",
    "narrative": "reality shift",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def append_event(path: Path, payload: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload) + "\n")


def deterministic_roll(seed: str) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return (int(digest[:8], 16) % 20) + 1


def target_number(request: dict, action: dict, scene_state: dict) -> int:
    base = BASE_TARGETS.get(request.get("difficulty", "normal"), 12)
    if action["approach"] == "support":
        base -= 1
    if scene_state.get("tension") in {"high", "critical"}:
        base += 1
    if action["risk_level"] == "cautious":
        base -= 1
    if action["risk_level"] == "reckless":
        base += 1
    return max(8, min(18, base))


def modifier(action: dict) -> int:
    if action["approach"] == "support":
        return 1
    if action["risk_level"] == "bold":
        return 1
    if action["risk_level"] == "reckless":
        return 2
    return 0


def outcome_band(roll_value: int, final_value: int, target: int) -> str:
    if roll_value == 1:
        return "critical_failure"
    if roll_value == 20:
        return "critical_success"
    if final_value < target:
        return "mixed_success" if target - final_value <= 2 else "failure"
    return "critical_success" if final_value - target >= 4 else "success"


def status_from(resolutions: list[dict]) -> str:
    if all(item["outcome_band"] in {"success", "critical_success"} for item in resolutions):
        return "resolved"
    if all(item["outcome_band"] in {"failure", "critical_failure"} for item in resolutions):
        return "failed"
    return "ongoing"


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve one encounter beat in the shared campaign tree.")
    parser.add_argument("--campaign-id", required=True)
    args = parser.parse_args()

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    active_root = campaign_root / "active"
    request = load_json(active_root / "encounter_request.json")
    scene_state = load_json(active_root / "scene.json")
    normalized = load_json(active_root / "normalized_actions.json")
    optional_rolls = load_json(active_root / "optional_rolls.json").get("rolls", {})
    event_log_path = campaign_root / "logs/event-log.jsonl"

    resolutions = []
    next_beat = int(scene_state.get("beat_count", 0)) + 1

    for index, action in enumerate(normalized.get("actions", []), start=1):
        seed = f"{request.get('scene_id')}:{action['player_id']}:{action['intent']}"
        roll_value = optional_rolls.get(action["player_id"], deterministic_roll(seed))
        mod = modifier(action)
        target = target_number(request, action, scene_state)
        final = roll_value + mod
        band = outcome_band(roll_value, final, target)
        twist = band in {"critical_failure", "critical_success"} or scene_state.get("tension") in {"high", "critical"}
        resolution = {
            "action_id": f"ACTION-{index:03d}",
            "actor_id": action["player_id"],
            "roll_type": "d20",
            "roll_value": roll_value,
            "modifier": mod,
            "final_value": final,
            "target_number": target,
            "outcome_band": band,
            "twist_triggered": twist,
            "twist_type": TWISTS.get(request.get("encounter_type"), "unexpected turn") if twist else None,
        }
        resolutions.append(resolution)
        append_event(
            event_log_path,
            {
                "ts": now_iso(),
                "campaign_id": request.get("campaign_id"),
                "session_id": request.get("session_id"),
                "scene_id": request.get("scene_id"),
                "type": "roll_resolved",
                "beat_count": next_beat,
                "actor": action["player_id"],
                "intent": action["intent"],
                "risk": action["risk_level"],
                "target_number": target,
                "roll_value": roll_value,
                "modifier": mod,
                "final_value": final,
                "outcome_band": band,
            },
        )

    status = status_from(resolutions)
    if next_beat >= int(scene_state.get("must_resolve_by", 5)) and status == "ongoing":
        status = "cliffhanger"

    scene_state["status"] = "aftermath" if status in {"resolved", "failed", "cliffhanger"} else "active"
    scene_state["beat_count"] = next_beat
    scene_state["updated_at"] = now_iso()
    if any(item["outcome_band"] == "critical_success" for item in resolutions):
        scene_state["tension"] = "high"
    elif any(item["outcome_band"] == "critical_failure" for item in resolutions):
        scene_state["tension"] = "critical"

    summary = f"{request.get('encounter_type', 'narrative').capitalize()} scene {request.get('scene_id')} resolved as {status}."
    added_hazards = ["heightened pressure"] if status in {"failed", "cliffhanger"} else []
    added_opportunities = ["momentum"] if status == "resolved" else []

    write_json(active_root / "scene.json", scene_state)
    write_json(
        campaign_root / "sessions" / f"{request.get('session_id')}.json",
        {
            "campaign_id": request.get("campaign_id"),
            "session_id": request.get("session_id"),
            "status": "open" if status == "ongoing" else "closing",
            "last_scene_id": request.get("scene_id"),
            "last_summary": summary,
            "open_loops": [],
            "canon_notes": [],
            "state_integrity": "partial",
        },
    )

    append_event(
        event_log_path,
        {
            "ts": now_iso(),
            "campaign_id": request.get("campaign_id"),
            "session_id": request.get("session_id"),
            "scene_id": request.get("scene_id"),
            "type": "consequence_applied",
            "beat_count": next_beat,
            "status": status,
            "added_hazards": added_hazards,
            "added_opportunities": added_opportunities,
        },
    )
    append_event(
        event_log_path,
        {
            "ts": now_iso(),
            "campaign_id": request.get("campaign_id"),
            "session_id": request.get("session_id"),
            "scene_id": request.get("scene_id"),
            "type": "beat_closed",
            "beat_count": next_beat,
            "status": status,
            "summary": summary,
            "spotlight_next": scene_state.get("spotlight_next"),
        },
    )

    print(f"Resolved scene {request.get('scene_id')} as {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
