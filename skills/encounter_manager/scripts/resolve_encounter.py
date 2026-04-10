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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


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


def status_from(resolutions: list[dict], request: dict) -> str:
    if any(item["twist_triggered"] and item["outcome_band"] == "critical_success" for item in resolutions):
        return "transformed"
    if all(item["outcome_band"] in {"success", "critical_success"} for item in resolutions):
        return "resolved"
    if all(item["outcome_band"] in {"failure", "critical_failure"} for item in resolutions):
        return "failed"
    return "ongoing"


def bullet_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a narrative encounter beat.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = args.root
    request = load_json(root / "state/inputs/encounter_request.json")
    scene_state = load_json(root / "state/encounters/scene_state.json")
    normalized = load_json(root / "state/encounters/normalized_actions.json")
    optional_rolls = load_json(root / "state/inputs/optional_rolls.json").get("rolls", {})

    resolutions = []
    for index, action in enumerate(normalized.get("actions", []), start=1):
        action_id = f"ACTION-{index:03d}"
        seed = f"{request.get('encounter_id')}:{action['player_id']}:{action['intent']}"
        roll_value = optional_rolls.get(action["player_id"], deterministic_roll(seed))
        mod = modifier(action)
        target = target_number(request, action, scene_state)
        final = roll_value + mod
        band = outcome_band(roll_value, final, target)
        twist = band in {"critical_failure", "critical_success"} or scene_state.get("tension") in {"high", "critical"}
        resolutions.append(
            {
                "action_id": action_id,
                "actor_id": action["player_id"],
                "roll_type": "d20",
                "roll_value": roll_value,
                "modifier": mod,
                "final_value": final,
                "target_number": target,
                "outcome_band": band,
                "reasoning": f"{action['approach']} action resolved against a narrow difficulty band.",
                "twist_triggered": twist,
                "twist_type": TWISTS.get(request.get("encounter_type"), "unexpected turn") if twist else None,
            }
        )

    status = status_from(resolutions, request)
    scene_state["phase"] = "aftermath" if status in {"resolved", "failed", "transformed"} else "resolution"
    if status == "ongoing":
        scene_state["round"] = int(scene_state.get("round", 1)) + 1
    if any(item["outcome_band"] == "critical_success" for item in resolutions):
        scene_state["tension"] = "high"
    elif any(item["outcome_band"] == "critical_failure" for item in resolutions):
        scene_state["tension"] = "critical"

    added_hazards = []
    added_opportunities = []
    environment_changes = []
    hooks = []
    gm_notes = []

    if status == "resolved":
        added_opportunities.append("momentum")
        hooks.append("Push immediately into the next reveal before resistance regroups.")
        gm_notes.append("The scene bent in the players' favor. Offer a strong follow-through choice.")
    elif status == "failed":
        added_hazards.append("heightened pressure")
        hooks.append("Let failure redirect the scene instead of dead-ending it.")
        gm_notes.append("Escalate pressure, but keep the next choice legible.")
    elif status == "transformed":
        added_hazards.append("encounter transformed")
        environment_changes.append("The scene shifts into a new mode under fresh pressure.")
        hooks.append("Ask who reacts first to the transformed scene.")
        gm_notes.append("A critical result changed the shape of the encounter. Reframe quickly.")
    else:
        environment_changes.append("The scene remains in motion and pressure keeps building.")
        hooks.append("Prompt the players to commit to the next beat before the scene cools.")
        gm_notes.append("Use the next beat to sharpen stakes or expose a new angle.")

    summary = f"{request.get('encounter_type', 'narrative').capitalize()} encounter resolved as {status} across {len(resolutions)} action(s)."
    consequences = {
        "narrative_update": summary,
        "state_changes": {"players": [], "npcs": [], "monsters": []},
        "scene_changes": {
            "added_hazards": added_hazards,
            "removed_hazards": [],
            "added_opportunities": added_opportunities,
            "removed_opportunities": [],
            "environment_changes": environment_changes,
        },
        "new_story_hooks": hooks,
        "escalation": "high" if status in {"failed", "transformed"} else "low" if status == "ongoing" else "none",
    }

    result = {
        "encounter_id": request.get("encounter_id"),
        "status": status,
        "summary": summary,
        "updated_scene_state": scene_state,
        "action_resolutions": resolutions,
        "consequences": consequences,
        "gm_notes": gm_notes,
        "suggested_next_prompts": hooks[:3],
    }
    write_json(root / "state/outputs/encounter_result.json", result)
    write_json(root / "state/encounters/scene_state.json", scene_state)

    timestamp = now_iso()
    session_id = request.get("scene_id", "SCENE-001").replace("SCENE", "SESSION")
    markdown = (root / "assets/templates/encounter_results.template.md").read_text().format(
        encounter_id=request.get("encounter_id"),
        session_id=session_id,
        timestamp=timestamp,
        outcome=status,
        summary=summary,
        resolved_loops="",
        new_loops=bullet_lines(hooks[:1]),
        world_changes=bullet_lines(environment_changes or ["Encounter pressure changed the scene state."]),
        rewards=bullet_lines(added_opportunities or ["No clean reward. The value is narrative position."]),
        consequences=bullet_lines(added_hazards or ["Pressure remains active and unresolved."]),
        suggested_follow_up=bullet_lines(hooks[:3] or ["Ask the players what they do next."]),
    )
    (root / "state/outputs/encounter_results.md").write_text(markdown if markdown.endswith("\n") else markdown + "\n")

    change_log_path = root / "state/logs/change_log.md"
    existing = change_log_path.read_text() if change_log_path.exists() else "# Change Log\n"
    existing = existing.rstrip() + f"\n\n## {timestamp}\n\n- Resolved encounter {request.get('encounter_id')} as {status}.\n"
    change_log_path.write_text(existing + "\n")

    print(f"Resolved encounter {request.get('encounter_id')} as {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
