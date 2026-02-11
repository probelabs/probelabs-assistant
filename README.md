# ProbeLabs Assistant

AI-powered assistant for the ProbeLabs engineering team. Explores code, browses GitHub, debugs CI/CD, makes changes, and creates PRs across all ProbeLabs repositories — all from Slack.

Built on [Visor](https://github.com/probelabs/visor) workflow engine with the unified skills architecture.

> **New to Visor assistants?** Start with [probe-quickstart](https://github.com/probelabs/probe-quickstart) for a minimal working example, then come back here to see how a production assistant is structured.

## What It Can Do

- **Code Exploration** — search and understand code across all 15 ProbeLabs repos (Probe, Visor, GoReplay, Logoscope, etc.) using semantic code-talk
- **GitHub Access** — browse PRs, issues, releases, branches, and activity across the entire `probelabs` org
- **CI/CD Debugging** — investigate GitHub Actions failures, view logs, identify root causes
- **Engineering Tasks** — make code changes, create PRs, implement features and bug fixes via Claude Code
- **Thread Summaries** — summarize Slack conversation threads
- **General Chat** — answer questions about ProbeLabs products and architecture

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/probelabs/probelabs-assistant.git
cd probelabs-assistant
cp .env.example .env
# Edit .env with your Slack tokens and API keys
```

### 2. Try it locally (CLI)

```bash
npx -y @probelabs/visor@latest run probelabs-assistant.yaml \
  --message "What can you help me with?"
```

Or use the interactive TUI:

```bash
npx -y @probelabs/visor@latest run probelabs-assistant.yaml --tui
```

### 3. Run as Slack bot

```bash
npx -y @probelabs/visor@latest run probelabs-assistant.yaml --slack
```

Mention the bot in any Slack thread and it will respond.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_APP_TOKEN` | For Slack | App-level token (`xapp-...`) for Socket Mode |
| `SLACK_BOT_TOKEN` | For Slack | Bot token (`xoxb-...`) for messages and API |
| `SLACK_SIGNING_SECRET` | For Slack | Webhook verification |
| `GOOGLE_API_KEY` | Yes | Google AI API key (Gemini) |

### Slack App Setup

Create a Slack app at [api.slack.com/apps](https://api.slack.com/apps):

1. Enable **Socket Mode** (Settings > Socket Mode > Enable)
2. Add **Bot Token Scopes**: `app_mentions:read`, `channels:history`, `groups:history`, `im:history`, `mpim:history`, `chat:write`, `reactions:read`, `reactions:write`
3. Subscribe to **Bot Events**: `app_mention`, `message.channels`, `message.groups`, `message.im`
4. Install to workspace, copy tokens to `.env`

## Architecture

```
probelabs-assistant.yaml          ← Main config: Slack, scheduler, system prompt
│
├── config/
│   ├── intents.yaml              ← Intent routing (chat, code_help)
│   └── skills.yaml               ← 8 skills with knowledge + tools
│
├── docs/                         ← Knowledge files injected into skills
│   ├── probelabs-architecture.md ← Product ecosystem overview
│   ├── github-tools.md           ← gh CLI reference for all repos
│   ├── github-actions-debugging.md
│   ├── code-exploration-tool.md
│   ├── code-help-mode.md
│   ├── engineer-tool.md
│   └── capabilities.md
│
└── workflows/
    └── engineer.yaml             ← Code changes + PR creation via Claude Code
```

### How It Works

When a message arrives, the assistant runs this pipeline:

1. **Intent classification** — determines if it's `chat` or `code_help`
2. **Skill selection** — matches skills by their `description` fields
3. **Dependency expansion** — skills with `requires` pull in other skills (e.g., `engineer` activates `code-explorer`)
4. **Knowledge + tool injection** — activated skills inject docs and tools into the AI context
5. **Response** — the AI answers, calling tools like code-talk or `gh` CLI as needed

### Skills

| Skill | Activates When | Tools |
|-------|---------------|-------|
| `github` | References PRs, issues, releases, branches | `gh` CLI |
| `github-actions` | CI/CD failures, pipeline debugging | `gh` CLI |
| `code-explorer` | Needs code search or implementation details | code-talk workflow |
| `code-help` | Code questions, debugging | Knowledge only |
| `engineer` | Wants code changes or PRs created | engineer workflow + Claude Code |
| `capabilities` | Asks what the assistant can do | Knowledge only |
| `thread-summary` | Asks to summarize a thread | Knowledge only |

### Repositories Covered

The code-explorer skill has all 15 ProbeLabs projects configured with smart routing overrides:

| Repo | Language | What It Is |
|------|----------|------------|
| [probe](https://github.com/probelabs/probe) | Rust | Semantic code search engine |
| [visor](https://github.com/probelabs/visor) | TypeScript | AI code review (GitHub Action + CLI) |
| [visor-ee](https://github.com/probelabs/visor-ee) | TypeScript | Workflow engine for AI assistants |
| [goreplay](https://github.com/probelabs/goreplay) | Go | HTTP traffic capture and replay |
| [logoscope](https://github.com/probelabs/logoscope) | TypeScript | AI log analysis CLI + MCP server |
| [maid](https://github.com/probelabs/maid) | TypeScript | Mermaid diagram linter |
| [docs-mcp](https://github.com/probelabs/docs-mcp) | TypeScript | Turn GitHub repos into MCP servers |
| [memaris](https://github.com/probelabs/memaris) | TypeScript | Claude Code session memory |
| [afk](https://github.com/probelabs/afk) | Node.js | Remote control for Claude Code via Telegram |
| [big-brain](https://github.com/probelabs/big-brain) | TypeScript | MCP server for fresh AI insights |
| [vow](https://github.com/probelabs/vow) | TypeScript | Accountability gates for AI agents |
| [SandboxJS](https://github.com/probelabs/SandboxJS) | JavaScript | Safe eval runtime |
| [probelabs.com](https://github.com/probelabs/probelabs.com) | Web | Official website |
| [probe-quickstart](https://github.com/probelabs/probe-quickstart) | YAML | Quickstart template |
| [ground-control](https://github.com/probelabs/ground-control) | - | AI chat interface (private) |

## Example Interactions

```
User: "How does Probe's tree-sitter integration work?"
→ Activates: code-explorer
→ Searches probelabs/probe for AST parsing code, returns file paths and explanation

User: "Show me recent PRs on visor"
→ Activates: github
→ Runs: gh pr list --repo probelabs/visor

User: "Why is the CI failing on probe PR #42?"
→ Activates: github-actions
→ Runs: gh pr checks, fetches logs, greps for errors

User: "Add a --verbose flag to the probe CLI"
→ Activates: engineer (+ code-explorer)
→ Explores code first, then makes changes and creates a PR
```

## Running Tests

```bash
npx -y @probelabs/visor@latest test
```

Tests verify workflow execution (engineer prompt building, task execution steps).

## Adding New Skills

Add a new entry to `config/skills.yaml`:

```yaml
- id: my-new-skill
  description: when this skill should activate (used by AI classifier)
  knowledge: |
    {% readfile "docs/my-skill-guide.md" %}
```

For skills with external tools (MCP servers):

```yaml
- id: my-tool-skill
  description: user needs access to some external service
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

See the [probe-quickstart](https://github.com/probelabs/probe-quickstart) README for a gentler introduction to skills, intents, and tools.

## Related Projects

- [probe-quickstart](https://github.com/probelabs/probe-quickstart) — Minimal starter template for building your own assistant
- [visor](https://github.com/probelabs/visor) — The workflow engine powering this assistant
- [visor-ee](https://github.com/probelabs/visor-ee) — Enterprise workflows (assistant pipeline, code-talk, engineer)
- [probe](https://github.com/probelabs/probe) — Semantic code search engine used by code-talk

## License

MIT
