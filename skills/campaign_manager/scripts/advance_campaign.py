#!/usr/bin/env python3

from __future__ import annotations


def main() -> int:
    raise SystemExit(
        "advance_campaign.py is deprecated. Campaign state has moved to workspace/state/campaigns/<campaign_id>/. "
        "Use bootstrap_state.py plus shared campaign snapshots until this helper is rewritten for the new model."
    )


if __name__ == "__main__":
    raise SystemExit(main())
