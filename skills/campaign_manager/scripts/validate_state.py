#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FILES = [
    "campaign.json",
    "players.json",
    "readiness.json",
    "npcs.json",
    "clocks.json",
    "opening_brief.md",
    "active/scene.json",
    "active/encounter_request.json",
    "active/normalized_actions.json",
    "logs/event-log.jsonl",
    "handoffs/latest-session.json",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate shared campaign state.")
    parser.add_argument("--campaign-id", required=True)
    args = parser.parse_args()

    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    errors = []

    for rel in REQUIRED_FILES:
        path = campaign_root / rel
        if not path.exists():
            errors.append(f"missing: {rel}")

    campaign_path = campaign_root / "campaign.json"
    handoff_path = campaign_root / "handoffs/latest-session.json"
    if campaign_path.exists():
        campaign = json.loads(campaign_path.read_text())
        if campaign.get("campaign_id") != args.campaign_id:
            errors.append("campaign.json campaign_id mismatch")
    if handoff_path.exists():
        handoff = json.loads(handoff_path.read_text())
        if handoff.get("campaign_id") != args.campaign_id:
            errors.append("latest-session.json campaign_id mismatch")
    readiness_path = campaign_root / "readiness.json"
    if readiness_path.exists():
        readiness = json.loads(readiness_path.read_text())
        if readiness.get("campaign_id") != args.campaign_id:
            errors.append("readiness.json campaign_id mismatch")

    print("Validation report")
    print(f"- Campaign root: {campaign_root}")
    if errors:
        print("- Errors:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("- Status: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
