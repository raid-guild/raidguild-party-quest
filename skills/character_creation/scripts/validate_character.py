#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = ["character_id", "name", "concept", "role", "drive", "edge", "flaw", "derived"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the character draft.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    draft = json.loads((args.root / "state/outputs/character_draft.json").read_text())
    session_state_path = args.root / "state/runtime/session_state.json"
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in draft:
            errors.append(f"missing field: {field}")

    if "derived" in draft:
        for field in ["one_line_pitch", "campaign_hook", "notable_edge"]:
            if field not in draft["derived"]:
                errors.append(f"missing derived field: {field}")

    if not draft.get("name"):
        errors.append("name is empty")
    if not draft.get("concept"):
        errors.append("concept is empty")
    if not session_state_path.exists():
        errors.append("session_state.json is missing")

    print("Validation report")
    print(f"- Root: {args.root}")
    if errors:
        print("- Errors:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("- Status: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
