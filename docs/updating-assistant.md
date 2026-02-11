# Updating the ProbeLabs Assistant

This guide explains how to update and extend this assistant. The assistant can use this guide to modify itself via PRs to `probelabs/probelabs-assistant`.

## Architecture Overview

- **`probelabs-assistant.yaml`** — Main entry point: Slack config, system prompt, intent and skill loading
- **`config/intents.yaml`** — High-level intent categories (chat, code_help)
- **`config/skills.yaml`** — All skills with descriptions, knowledge, tools, and dependencies
- **`docs/`** — Knowledge files injected into skills at runtime via `{% readfile %}`
- **`workflows/engineer.yaml`** — Code changes and PR creation via Claude Code

## Adding a New Skill

### Step 1: Define the skill in `config/skills.yaml`

```yaml
- id: my-new-skill
  description: when this skill should activate (used by AI classifier)
  knowledge: |
    {% readfile "docs/my-skill-guide.md" %}
```

The `description` field is critical — it tells the classifier when to activate this skill. Be specific and include example phrases.

### Step 2: Create documentation

Create a file in `docs/` with instructions the AI should follow when this skill is active:

```
docs/my-skill-guide.md
```

### Step 3: Add tools (optional)

If the skill needs external tools:

```yaml
- id: my-skill
  description: ...
  tools:
    my-tool:
      command: npx
      args: ["my-mcp-server"]
      env:
        API_KEY: "${MY_API_KEY}"
      allowedMethods:
        - method_one
        - method_two
```

### Step 4: Add dependencies (optional)

If the skill requires another skill to be active:

```yaml
- id: my-skill
  description: ...
  requires: [code-explorer]
```

## Adding a New Repository

### Step 1: Add to `config/skills.yaml` under code-explorer projects

```yaml
projects:
  - id: my-repo
    repo: probelabs/my-repo
    description: |
      What this repo contains:
      - Key functionality
      - When to search it
```

### Step 2: Add routing override (if needed)

Add to the `routing_prompt` in the code-explorer skill:

```yaml
routing_prompt: |
  X. "My topic" questions -> MUST include `my-repo`
     - Specific patterns that require this repo
```

## Adding a New Intent

Edit `config/intents.yaml`:

```yaml
- id: my_intent
  description: |
    When this intent should activate.
    Examples: "do X", "help me with Y"
```

## Self-Update via PR

When a user asks the assistant to "remember" something, learn a new workflow, or extend its capabilities, it should:

1. Identify what needs to change (new skill, updated docs, new routing rule)
2. Use the `engineer` tool to make changes to `probelabs/probelabs-assistant`
3. Create a PR with the changes
4. The PR must be reviewed and merged before changes take effect

Common self-update triggers:
- "Remember how we just did this, add it as a capability"
- "You should know how to do X, update yourself"
- "Add this to your instructions"
- "Create a new skill for Y"

## Testing Changes

```bash
# Run workflow tests
npx -y @probelabs/visor@latest test
```

## File Reference

| File | Purpose |
|------|---------|
| `probelabs-assistant.yaml` | Main config: Slack, scheduler, system prompt |
| `config/intents.yaml` | Intent definitions for routing |
| `config/skills.yaml` | All skills with knowledge, tools, dependencies |
| `workflows/engineer.yaml` | Code changes and PR creation |
| `docs/*.md` | Knowledge files injected into skills |
