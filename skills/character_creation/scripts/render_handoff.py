#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from update_character import load_json, recompute, render_handoff


def main() -> int:
    parser = argparse.ArgumentParser(description="Render handoff markdown from the character draft.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    draft = load_json(args.root / "state/outputs/character_draft.json")
    recompute(draft)
    render_handoff(draft, args.root)
    print("Rendered character handoff")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
