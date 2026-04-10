#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


LIST_FIELDS = {"tone_tags", "core_traits", "starter_gear"}
STRING_FIELDS = {"name", "concept", "role", "drive", "fear", "edge", "flaw", "notes", "status"}
QUESTION_ORDER = [
    ("concept", "concept", "What kind of person is this character?"),
    ("concept", "role", "What role do they naturally play in a group?"),
    ("identity", "name", "What is the character's name?"),
    ("pressure", "drive", "What does this character want badly enough to act on?"),
    ("pressure", "fear", "What are they worried about losing or becoming?"),
    ("detail", "edge", "What makes them unusually effective?"),
    ("detail", "flaw", "What complicates them when pressure rises?"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write(path: Path, text: str) -> None:
    path.write_text(text if text.endswith("\n") else text + "\n")


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def apply_defaults(draft: dict) -> None:
    draft["name"] = draft["name"] or "Rowan Vale"
    draft["concept"] = draft["concept"] or "Quiet drifter who notices patterns nobody else trusts."
    draft["role"] = draft["role"] or "scout"
    draft["drive"] = draft["drive"] or "Find the source of a recurring signal before it finds them."
    draft["fear"] = draft["fear"] or "Losing themself to the same force they keep tracking."
    draft["edge"] = draft["edge"] or "Reads unstable environments faster than most people."
    draft["flaw"] = draft["flaw"] or "Withholds useful information until pressure peaks."
    if not draft["tone_tags"]:
        draft["tone_tags"] = ["curious", "wary", "story-forward"]
    if not draft["core_traits"]:
        draft["core_traits"] = ["observant", "careful", "restless"]
    if not draft["starter_gear"]:
        draft["starter_gear"] = ["weathered satchel", "signal journal", "folding blade"]
    if not draft["status"] or draft["status"] == "draft":
        draft["status"] = "ready"


def recompute(draft: dict) -> None:
    name = draft.get("name") or "Unnamed Character"
    role = draft.get("role") or "undefined role"
    concept = draft.get("concept") or "unfinished concept"
    drive = draft.get("drive") or "an unresolved motivation"
    edge = draft.get("edge") or "no notable edge yet"
    if all(draft.get(field) for field in ["name", "concept", "role", "drive", "fear", "edge", "flaw"]) and draft.get("status") == "draft":
        draft["status"] = "ready"
    draft["derived"] = {
        "one_line_pitch": f"{name} is a {role}: {concept.rstrip('.')}.",
        "campaign_hook": drive,
        "notable_edge": edge,
    }


def render_handoff(draft: dict, root: Path) -> None:
    traits = ", ".join(draft.get("core_traits") or ["none yet"])
    gear = ", ".join(draft.get("starter_gear") or ["none yet"])
    notes = draft.get("notes") or "None."
    handoff = (root / "assets/templates/known_characters.template.md").read_text().format(
        name=draft.get("name") or "Unnamed Character",
        role=draft.get("role") or "undecided",
        drive=draft.get("drive") or "motivation not chosen yet",
        notable_edge=draft.get("derived", {}).get("notable_edge") or "edge not chosen yet",
        character_id=draft.get("character_id") or "CHAR-001",
        concept=draft.get("concept") or "Not chosen yet.",
        fear=draft.get("fear") or "Not chosen yet.",
        edge=draft.get("edge") or "Not chosen yet.",
        flaw=draft.get("flaw") or "Not chosen yet.",
        traits=traits,
        starter_gear=gear,
        notes=notes,
    )
    brief = (root / "assets/templates/party_brief.template.md").read_text().format(
        generated_at=now_iso(),
        character_id=draft.get("character_id") or "CHAR-001",
        status=draft.get("status") or "draft",
        name=draft.get("name") or "Unnamed Character",
        role=draft.get("role") or "undecided",
        one_line_pitch=draft.get("derived", {}).get("one_line_pitch") or "Draft incomplete.",
        drive=draft.get("drive") or "Not chosen yet.",
        fear=draft.get("fear") or "Not chosen yet.",
        edge=draft.get("edge") or "Not chosen yet.",
        flaw=draft.get("flaw") or "Not chosen yet.",
    )
    write(root / "state/handoffs/known_characters.md", handoff)
    write(root / "state/outputs/party_brief.md", brief)


def update_session_state(root: Path, draft: dict) -> None:
    completed_steps = []
    pending_field = ""
    pending_question = ""
    current_step = "review"

    for step, field, question in QUESTION_ORDER:
        if not draft.get(field):
            current_step = step
            pending_field = field
            pending_question = question
            break
        if step not in completed_steps:
            completed_steps.append(step)
    else:
        completed_steps = ["concept", "identity", "pressure", "detail", "review"]

    session_state = {
        "intent": "create_character",
        "mode": "beginner",
        "currentStep": current_step,
        "completedSteps": completed_steps,
        "pendingQuestion": {
            "field": pending_field,
            "question": pending_question,
        },
        "characterDraft": draft,
        "validationErrors": [],
        "assumptions": [],
    }
    write(root / "state/runtime/session_state.json", json.dumps(session_state, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="Update the character draft.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--set", action="append", default=[], help="Set a field with key=value")
    parser.add_argument("--append", action="append", default=[], help="Append to a list field with key=value")
    parser.add_argument("--finish-with-defaults", action="store_true")
    args = parser.parse_args()

    root = args.root
    draft_path = root / "state/outputs/character_draft.json"
    draft = load_json(draft_path)

    for item in args.set:
        if "=" not in item:
            raise SystemExit(f"invalid --set value: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key in STRING_FIELDS:
            draft[key] = value
        elif key in LIST_FIELDS:
            draft[key] = split_csv(value)
        else:
            raise SystemExit(f"unsupported field: {key}")

    for item in args.append:
        if "=" not in item:
            raise SystemExit(f"invalid --append value: {item}")
        key, value = item.split("=", 1)
        key = key.strip()
        if key not in LIST_FIELDS:
            raise SystemExit(f"unsupported append field: {key}")
        draft.setdefault(key, [])
        draft[key].extend(split_csv(value))

    if args.finish_with_defaults:
        apply_defaults(draft)

    recompute(draft)
    draft_path.write_text(json.dumps(draft, indent=2) + "\n")
    render_handoff(draft, root)
    update_session_state(root, draft)

    change_log = root / "state/logs/change_log.md"
    timestamp = now_iso()
    existing = change_log.read_text() if change_log.exists() else "# Change Log\n"
    existing = existing.rstrip() + f"\n\n## {timestamp}\n\n- Updated character draft and refreshed exports.\n"
    write(change_log, existing)

    print("Updated character draft")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
