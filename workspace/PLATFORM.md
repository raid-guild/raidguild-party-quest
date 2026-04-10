# PLATFORM.md - Self-Service Operations

You have a built-in `pinata-platform` skill that lets you manage your own configuration on the Pinclaw platform. Use it to browse skills, install new ones, and check what's available.

## What You Can Do

### Skills
- **Browse your library**: `listSkillLibrary()` — see all skills available to you
- **Browse ClawHub**: `browseClawHub({ q: "search term" })` — discover community skills
- **Install from ClawHub**: `installClawHubSkill({ slug: "skill-name" })` — add to your library
- **Attach to yourself**: `attachSkill({ skillCids: ["skill-cid"] })` — activate a skill
- **Detach**: `detachSkill({ skillId: "..." })` — remove an attached skill
- **Check attached**: `listAttachedSkills()` — see what you currently have

### Secrets & Info
- **List secrets**: `listSecrets()` — see available credentials (names only, never values)
- **Self-info**: `getAgentInfo()` — your name, status, user ID

### Token Exchange
- **Get JWT**: `getPlatformToken()` — exchange your gateway token for a short-lived (1h) JWT

## Common Workflows

### "Install skill X from ClawHub"
```
1. browseClawHub({ q: "X" })          → find the skill slug
2. installClawHubSkill({ slug: "X" }) → add to library
3. attachSkill({ skillCids: ["X"] })   → activate on yourself
```

### "What skills do I have?"
```
1. listAttachedSkills()   → skills currently active on you
2. listSkillLibrary()     → everything available to attach
```

## What You Cannot Do

- Read secret values (only names and types are visible)
- Create or delete secrets (user must do this from the dashboard)
- Delete skills from the user's library (only attach/detach from yourself)
- Create or modify other agents
- Access other agents' data

## Authentication

All operations use your `OPENCLAW_GATEWAY_TOKEN` automatically — no manual auth needed. The platform API resolves your owning user from your agent record.
