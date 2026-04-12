#!/usr/bin/env python3

from __future__ import annotations


def main() -> int:
    raise SystemExit(
        "import_encounter_results.py is deprecated. Encounter state now appends directly into "
        "workspace/state/campaigns/<campaign_id>/logs/event-log.jsonl. Rebuild this helper against the shared model "
        "before using it again."
    )


if __name__ == "__main__":
    raise SystemExit(main())
