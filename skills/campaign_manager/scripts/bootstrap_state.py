#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import re


TEMPLATES = {
    "assets/templates/overview.template.md": "state/campaign/overview.md",
    "assets/templates/current_arc.template.md": "state/campaign/current_arc.md",
    "assets/templates/world_state.template.md": "state/campaign/world_state.md",
    "assets/templates/factions.template.md": "state/campaign/factions.md",
    "assets/templates/locations.template.md": "state/campaign/locations.md",
    "assets/templates/open_loops.template.md": "state/campaign/open_loops.md",
    "assets/templates/timeline.template.md": "state/campaign/timeline.md",
    "assets/templates/encounter_queue.template.md": "state/campaign/encounter_queue.md",
    "assets/templates/next_encounter.template.md": "state/handoffs/next_encounter.md",
    "assets/templates/session_log.template.md": "state/logs/session_log.md",
    "assets/templates/change_log.template.md": "state/logs/change_log.md",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def first_heading(text: str) -> str | None:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def first_paragraph(text: str) -> str | None:
    lines = []
    ignored_prefixes = (
        "Use this file as upstream",
        "Describe the campaign premise here",
        "Suggested starter prompts:",
        "Replace this with",
    )
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            if lines:
                break
            continue
        if stripped.startswith(ignored_prefixes):
            continue
        if stripped.startswith("- "):
            continue
        lines.append(stripped)
    return " ".join(lines) if lines else None


def normalize_title(value: str | None, fallback: str) -> str:
    if not value:
        return fallback
    cleaned = re.sub(r"[^A-Za-z0-9 '\-:]", "", value).strip()
    if cleaned.lower() in {"world seed", "known characters"}:
        return fallback
    return cleaned[:80] or fallback


def extract_party_summary(text: str) -> str:
    lines = []
    in_party_section = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("## "):
            in_party_section = stripped == "## Party"
            continue
        if not in_party_section:
            continue
        if not stripped.startswith("- "):
            continue
        if "|" not in stripped or "Name | role" in stripped:
            continue
        lines.append(stripped)
    if not lines:
        return "- No party details provided yet."
    return "\n".join(lines[:4])


def summarize_input(text: str, fallback: str) -> str:
    paragraph = first_paragraph(text)
    return paragraph[:220] if paragraph else fallback


def needs_initialization(path: Path) -> bool:
    if not path.exists():
        return True
    text = path.read_text()
    markers = ("Status: scaffold", "Uninitialized Campaign", "Uninitialized Arc")
    return any(marker in text for marker in markers)


def render(root: Path) -> dict[str, str]:
    generated_at = now_iso()
    known_characters = read_text(root / "state/inputs/known_characters.md")
    world_seed = read_text(root / "state/inputs/world_seed.md")

    campaign_title = normalize_title(first_heading(world_seed), "Shadows At The Threshold")
    premise = summarize_input(
        world_seed,
        "A quiet power struggle is hardening around a contested route, and the party is close enough to disturb it.",
    )
    party_summary = extract_party_summary(known_characters)
    known_characters_summary = summarize_input(known_characters, "No character roster has been supplied yet.")

    return {
        "generated_at": generated_at,
        "campaign_id": "CAMPAIGN-001",
        "campaign_title": campaign_title,
        "campaign_premise": premise,
        "party_summary": party_summary,
        "pressure_label": "low",
        "world_seed_summary": summarize_input(world_seed, "No world seed supplied yet."),
        "known_characters_summary": known_characters_summary,
        "arc_id": "ARC-001",
        "arc_title": f"Arc One: {campaign_title}",
        "arc_objective": "Map the hidden pressure network before it closes around the party.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize campaign state from bundled templates.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--force", action="store_true", help="Overwrite already initialized canonical files.")
    args = parser.parse_args()

    context = render(args.root)
    written = []
    skipped = []

    for template_rel, target_rel in TEMPLATES.items():
        template_path = args.root / template_rel
        target_path = args.root / target_rel
        if not args.force and not needs_initialization(target_path):
            skipped.append(target_rel)
            continue
        content = template_path.read_text().format(**context)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content + ("\n" if not content.endswith("\n") else ""))
        written.append(target_rel)

    print("Initialized files:")
    for item in written:
        print(f"- {item}")
    if skipped:
        print("Skipped existing initialized files:")
        for item in skipped:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
