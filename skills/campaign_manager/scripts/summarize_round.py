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


def read_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        events.append(json.loads(stripped))
    return events


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")


def unique_ordered(items: list[str]) -> list[str]:
    seen = set()
    ordered = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def latest_with_key(events: list[dict], key: str):
    for event in reversed(events):
        value = event.get(key)
        if value not in (None, "", []):
            return value
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a round summary and latest session handoff from shared campaign state.")
    parser.add_argument("--campaign-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--round", type=int, required=True)
    args = parser.parse_args()

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    campaign = load_json(campaign_root / "campaign.json")
    scene = load_json(campaign_root / "active/scene.json")
    session = load_json(campaign_root / "sessions" / f"{args.session_id}.json")
    players = load_json(campaign_root / "players.json")
    npcs = load_json(campaign_root / "npcs.json")
    clocks = load_json(campaign_root / "clocks.json")
    events = [event for event in read_events(campaign_root / "logs/event-log.jsonl") if event.get("session_id") == args.session_id]

    beat_events = [event for event in events if event.get("type") == "beat_closed"]
    consequence_events = [event for event in events if event.get("type") == "consequence_applied"]
    roll_events = [event for event in events if event.get("type") == "roll_resolved"]

    summaries = unique_ordered([event.get("summary", "") for event in beat_events])
    open_loops = unique_ordered(
        [item for event in consequence_events for item in event.get("added_hazards", [])]
        + session.get("open_loops", [])
    )
    canon_notes = unique_ordered(session.get("canon_notes", []))
    npc_changes = [npc.get("name") or npc.get("id") for npc in npcs.get("npcs", [])[:5]]
    last_scene_id = latest_with_key(events, "scene_id") or scene.get("scene_id") or "unassigned"
    derived_beat_count = latest_with_key(events, "beat_count")
    beat_count = derived_beat_count if derived_beat_count is not None else scene.get("beat_count", 0)
    spotlight_next = (
        latest_with_key(beat_events, "spotlight_next")
        or scene.get("spotlight_next")
        or (players.get("players", [{}])[0].get("handle") if players.get("players") else "unassigned")
    )
    derived_status = latest_with_key(beat_events, "status") or latest_with_key(consequence_events, "status")
    session_status = "closed" if derived_status in {"resolved", "failed", "cliffhanger"} else session.get("status", "open")
    last_summary = summaries[-1] if summaries else session.get("last_summary", "No resolved beat summary recorded.")
    next_scene_seed = (
        "Escalate unresolved pressure from the last beat."
        if open_loops
        else "Frame the next scene around the strongest unresolved player objective."
    )

    round_summary = f"""# Round {args.round} Summary

- Campaign ID: {args.campaign_id}
- Session ID: {args.session_id}
- Generated At: {now_iso()}
- Beat Count: {beat_count}
- Last Scene: {last_scene_id}

## Summary

- {last_summary}

## Unresolved Threads
{chr(10).join(f"- {item}" for item in open_loops) if open_loops else "- None recorded."}

## Clocks
{chr(10).join(f"- {clock.get('name', clock.get('id', 'clock'))}: {clock.get('value', 0)}/{clock.get('max', '?')}" for clock in clocks.get('clocks', [])) if clocks.get('clocks') else "- No clocks recorded."}

## NPC Status Changes
{chr(10).join(f"- {item}" for item in npc_changes) if npc_changes else "- No NPC changes recorded."}

## Spotlight Next

- {spotlight_next}

## Canon Notes
{chr(10).join(f"- {item}" for item in canon_notes) if canon_notes else "- None."}

## Roll Activity

- Resolved Rolls: {len(roll_events)}
- Closed Beats: {len(beat_events)}
"""

    handoff = {
        "campaign_id": args.campaign_id,
        "session_id": args.session_id,
        "status": session_status,
        "ended_at": now_iso(),
        "current_round": args.round,
        "next_scene_seed": next_scene_seed,
        "open_loops": open_loops,
        "canon_notes": canon_notes,
        "canon_status": campaign.get("canon_status", "provisional"),
        "state_integrity": campaign.get("state_integrity", "partial"),
    }

    campaign["current_round"] = args.round
    campaign["active_scene"] = last_scene_id
    campaign["beat_count"] = beat_count
    campaign["updated_at"] = now_iso()
    session["current_round"] = args.round
    session["status"] = session_status
    session["last_summary"] = last_summary
    session["open_loops"] = open_loops
    session["canon_notes"] = canon_notes

    write_text(campaign_root / "rounds" / f"round-{args.round:02d}-summary.md", round_summary)
    write_json(campaign_root / "handoffs/latest-session.json", handoff)
    write_json(campaign_root / "campaign.json", campaign)
    write_json(campaign_root / "sessions" / f"{args.session_id}.json", session)

    print(f"Wrote round summary and session handoff for {args.campaign_id} round {args.round}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
