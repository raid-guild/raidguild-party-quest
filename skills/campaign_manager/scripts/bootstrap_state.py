#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path


PRESETS = {
    "last-chance-formal": {
        "title": "The Last Chance Formal",
        "seed": "A group of thirty-somethings returns to their fading hometown for an adult prom fundraiser at a once-grand ballroom. What begins as awkward nostalgia turns into missing money, old grudges, social blackmail, and terrible decisions in formalwear.",
        "style": "dark comedy, social noir, ensemble awkwardness, small-town pressure",
        "setting": "A once-grand ballroom in a fading hometown, half dressed for glamour and half collapsing under old resentments.",
        "trouble": "Money is missing, old history is surfacing, and the fundraiser is about to go public in front of exactly the wrong witnesses.",
        "scene": "The players arrive as the fundraiser lurches toward its first public embarrassment and a missing ledger threatens to expose who has been skimming from the event.",
        "intro": "Tonight was supposed to be an awkward charity reunion in borrowed formalwear. Instead, the ballroom is full of old grudges, a fundraiser on the brink, and one missing ledger that could blow the whole night open.",
    }
}

STYLE_PROFILES = {
    "noir": {
        "aliases": ["noir", "crime", "neo-noir", "detective"],
        "texture": "rain-slick streets, private leverage, late-night deals, and everyone pretending they are less desperate than they are",
        "trouble": "missing money and the wrong people asking the right questions",
        "location": "a dockside back room near the waterline",
        "pressure": "a creditor's runner and a dirty official closing in before the players can get their story straight",
    },
    "fantasy": {
        "aliases": ["fantasy", "sword", "magic", "adventure"],
        "texture": "guild politics, old oaths, market rumors, and the feeling that the world is older and more dangerous than it first appears",
        "trouble": "a missing relic and faction panic spreading through town",
        "location": "a crowded market square under the shadow of walls, banners, or temple stone",
        "pressure": "a priest and a local captain demanding action before panic spreads",
    },
    "sci-fi": {
        "aliases": ["sci-fi", "science fiction", "scifi", "space", "cyberpunk"],
        "texture": "fluorescent corridors, surveillance, contract pressure, and machines that keep working just long enough to become someone else's problem",
        "trouble": "missing cargo and a system fault around one compromised asset",
        "location": "a transit hub, docking bay, or control level where too many cameras have line of sight",
        "pressure": "security and a corporate handler forcing the players to act before the station locks down",
    },
    "sports": {
        "aliases": ["sports", "sports drama", "locker room", "team drama"],
        "texture": "locker-room tension, crowd noise, contract pressure, and rivalries that matter before anyone steps into the light",
        "trouble": "a sabotage scare and a media leak that could split the team before the next match",
        "location": "a tunnel, practice floor, or sideline access corridor moments before public pressure peaks",
        "pressure": "a coach and a reporter forcing an answer before game time",
    },
    "workplace": {
        "aliases": ["work sim", "workplace", "office", "corporate", "job"],
        "texture": "calendar panic, bad process, office alliances, and the quiet knowledge that one failure will become everyone's problem by lunch",
        "trouble": "a broken rollout and leadership conflict that lands directly on the players",
        "location": "a conference room, operations floor, or emergency call where nobody has enough time and everyone has an opinion",
        "pressure": "a boss and an internal rival demanding a fix before the damage becomes public",
    },
    "mystery": {
        "aliases": ["mystery", "investigation", "whodunit"],
        "texture": "contradictory stories, careful observation, and the sense that one overlooked detail is holding the whole thing together",
        "trouble": "a disappearance and evidence that is about to vanish",
        "location": "a scene that has already been disturbed by fear, gossip, or official interference",
        "pressure": "someone with local authority wants the truth buried before the players can test what really happened",
    },
    "horror": {
        "aliases": ["horror", "survival horror", "occult"],
        "texture": "uneasy silence, frayed nerves, bad light, and the certainty that the situation is already worse than anyone admits",
        "trouble": "something newly awake is pressing into the edges of ordinary life",
        "location": "a place that should feel safe but clearly is not anymore",
        "pressure": "time and isolation closing in before the players are ready",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def write_json(path: Path, payload: object, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return True


def write_text(path: Path, text: str, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n")
    return True


def normalize_style(style: str) -> str:
    lowered = style.lower()
    for key, profile in STYLE_PROFILES.items():
        if any(alias in lowered for alias in profile["aliases"]):
            return key
    return "noir" if "debt" in lowered or "crime" in lowered else "mystery" if "mystery" in lowered else "workplace" if "office" in lowered else "fantasy" if "magic" in lowered else "sci-fi" if "station" in lowered or "space" in lowered else "noir"


def build_opening_context(title: str, seed: str, style: str, preset: str) -> dict[str, str]:
    if preset:
        preset_data = PRESETS.get(preset)
        if not preset_data:
            raise SystemExit(f"unknown preset: {preset}")
        return preset_data

    safe_title = title or "Uninitialized Campaign"
    safe_seed = seed or f"{safe_title} follows a group pulled into trouble before they have time to get comfortable."
    safe_style = style or "noir"
    style_key = normalize_style(safe_style)
    profile = STYLE_PROFILES[style_key]
    location = profile["location"].replace(", or ", ", ")
    setting = f"{safe_title} opens in a world of {profile['texture']}. The players step into {location}, where the atmosphere already feels like it could turn costly with one bad answer."
    trouble = f"The immediate problem is {profile['trouble']}, and the players hit it at the exact moment {profile['pressure']}."
    scene = f"The opening scene begins at {location}, with the players forced to decide whether they protect their position, chase the truth, or make the situation worse before anyone else can control the narrative."
    intro = f"{safe_seed} Tonight starts in {location}, under pressure from {profile['trouble']}, and the players arrive one move before the situation stops being manageable."
    return {
        "title": safe_title,
        "seed": safe_seed,
        "style": safe_style,
        "style_key": style_key,
        "setting": setting,
        "trouble": trouble,
        "scene": scene,
        "intro": intro,
    }


def opening_brief(title: str, campaign_id: str, session_id: str, ts: str, seed: str, style: str, preset: str) -> str:
    context = build_opening_context(title, seed, style, preset)
    return f"""# Opening Brief

- Campaign ID: {campaign_id}
- Session ID: {session_id}
- Generated At: {ts}
- Title: {context["title"]}
- Preset: {preset or "custom"}

## Premise

{context["seed"]}

## Style

{context["style"]}

## Setting Snapshot

{context["setting"]}

## Current Trouble

{context["trouble"]}

## Opening Scene

{context["scene"]}

## Player-Facing Intro

{context["intro"]}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize shared campaign state.")
    parser.add_argument("--campaign-id", default="campaign-001")
    parser.add_argument("--session-id", default="session-001")
    parser.add_argument("--title", default="Uninitialized Campaign")
    parser.add_argument("--seed", default="")
    parser.add_argument("--style", default="")
    parser.add_argument("--preset", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    ts = now_iso()
    campaign_root = repo_root() / "workspace/state/campaigns" / args.campaign_id
    written: list[str] = []

    files = {
        campaign_root / "campaign.json": {
            "campaign_id": args.campaign_id,
            "title": args.title,
            "seed": args.seed,
            "style": args.style,
            "preset": args.preset or None,
            "status": "setup",
            "current_round": 0,
            "active_scene": None,
            "beat_count": 0,
            "beat_cap": 5,
            "must_escalate_at": 4,
            "must_resolve_by": 5,
            "canon_status": "provisional",
            "state_integrity": "partial",
            "created_at": ts,
            "updated_at": ts,
        },
        campaign_root / "players.json": {
            "campaign_id": args.campaign_id,
            "players": [],
            "start_short_handed_allowed": False,
            "updated_at": ts,
        },
        campaign_root / "npcs.json": {
            "campaign_id": args.campaign_id,
            "npcs": [],
            "updated_at": ts,
        },
        campaign_root / "clocks.json": {
            "campaign_id": args.campaign_id,
            "clocks": [],
            "updated_at": ts,
        },
        campaign_root / "active/scene.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "scene_id": None,
            "objective": "",
            "status": "idle",
            "beat_count": 0,
            "beat_cap": 5,
            "must_escalate_at": 4,
            "must_resolve_by": 5,
            "spotlight_next": None,
            "updated_at": ts,
        },
        campaign_root / "active/encounter_request.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "scene_id": None,
            "encounter_type": "narrative",
            "objective": "",
            "difficulty": "normal",
            "players": [],
            "npcs": [],
            "environment": {"tags": []},
        },
        campaign_root / "active/normalized_actions.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "scene_id": None,
            "resolution_mode": "group",
            "actions": [],
        },
        campaign_root / "active/optional_rolls.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "rolls": {},
        },
        campaign_root / "sessions" / f"{args.session_id}.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "status": "open",
            "started_at": ts,
            "current_round": 0,
            "open_loops": [],
            "canon_notes": [],
            "state_integrity": "partial",
        },
        campaign_root / "handoffs/latest-session.json": {
            "campaign_id": args.campaign_id,
            "session_id": args.session_id,
            "status": "open",
            "ended_at": None,
            "current_round": 0,
            "next_scene_seed": "",
            "opening_brief_ready": True,
            "open_loops": [],
            "canon_notes": [],
            "canon_status": "provisional",
            "state_integrity": "partial",
        },
        campaign_root / "readiness.json": {
            "campaign_id": args.campaign_id,
            "opening_brief_ready": True,
            "roster_confirmed": False,
            "required_players": [],
            "players_ready": [],
            "players_missing_characters": [],
            "start_short_handed_allowed": False,
            "round_1_ready": False,
            "updated_at": ts,
        },
    }

    for path, payload in files.items():
        if write_json(path, payload, args.force):
            written.append(str(path.relative_to(repo_root())))

    if write_text(campaign_root / "logs/event-log.jsonl", "", args.force):
        written.append(str((campaign_root / "logs/event-log.jsonl").relative_to(repo_root())))
    if write_text(campaign_root / "logs/gm-notes.md", "# GM Notes\n", args.force):
        written.append(str((campaign_root / "logs/gm-notes.md").relative_to(repo_root())))
    if write_text(
        campaign_root / "opening_brief.md",
        opening_brief(args.title, args.campaign_id, args.session_id, ts, args.seed, args.style, args.preset),
        args.force,
    ):
        written.append(str((campaign_root / "opening_brief.md").relative_to(repo_root())))
    if write_text(campaign_root / "rounds/round-00-summary.md", "# Round 0 Summary\n\n- Campaign scaffolded.\n", args.force):
        written.append(str((campaign_root / "rounds/round-00-summary.md").relative_to(repo_root())))

    print("Initialized shared campaign state:")
    for item in written:
        print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
