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


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped:
            events.append(json.loads(stripped))
    return events


def classify_lifecycle(message: str) -> tuple[str | None, str | None]:
    lower = message.lower()
    if "pause" in lower:
        return "paused", "Players requested a pause."
    if "resume" in lower:
        return "active", "Players requested a resume."
    if "end campaign" in lower or "we're done" in lower or "we are done" in lower:
        return "closed", "Players ended the campaign."
    if "start another" in lower or "switch campaign" in lower:
        return "superseded", "Players switched to another campaign."
    if "abandon" in lower:
        return "abandoned", "Campaign marked abandoned."
    return None, None


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply lifecycle transitions from OOC admin events.")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--session-id", required=True)
    args = parser.parse_args()

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    events = [
        event
        for event in read_events(campaign_root / "logs/event-log.jsonl")
        if event.get("session_id") == args.session_id and event.get("type") == "ooc_command_detected"
    ]
    if not events:
        print("No lifecycle admin events found")
        return 0

    last_event = events[-1]
    next_status, note = classify_lifecycle(last_event.get("message", ""))
    if not next_status:
        print("No lifecycle transition recognized")
        return 0

    ts = now_iso()
    campaign = load_json(campaign_root / "campaign.json")
    session_path = campaign_root / "sessions" / f"{args.session_id}.json"
    handoff_path = campaign_root / "handoffs/latest-session.json"
    session = load_json(session_path)
    handoff = load_json(handoff_path)

    session["status"] = next_status
    session["updated_at"] = ts
    handoff["status"] = next_status
    handoff["ended_at"] = ts if next_status in {"closed", "abandoned", "superseded"} else handoff.get("ended_at")
    campaign["status"] = next_status if next_status in {"paused", "closed", "abandoned", "superseded"} else campaign.get("status", "active")
    campaign["updated_at"] = ts

    canon_notes = handoff.get("canon_notes", [])
    if note and note not in canon_notes:
        canon_notes.append(note)
    handoff["canon_notes"] = canon_notes
    session["canon_notes"] = canon_notes

    write_json(session_path, session)
    write_json(handoff_path, handoff)
    write_json(campaign_root / "campaign.json", campaign)

    print(f"Applied lifecycle status {next_status} to {args.campaign_id}/{args.session_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
