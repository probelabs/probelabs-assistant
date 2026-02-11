# ProbeLabs Assistant

This is the AI assistant that ProbeLabs runs internally. It's how we use [Probe](https://github.com/probelabs/probe) and [Visor](https://github.com/probelabs/visor) ourselves — a real-world, production implementation that covers our entire codebase of 16 repositories spanning Rust, TypeScript, Go, and Node.js.

We open-sourced it so you can see exactly how a Probe-based assistant works at scale: how skills are structured, how code-talk explores multiple repos, how GitHub integration feeds context into conversations, and how the engineer workflow turns questions into pull requests.

> **Want to build your own?** Use [probe-quickstart](https://github.com/probelabs/probe-quickstart) — a minimal template you can clone and customize in minutes. Come back here when you want to see how a full production setup looks.

## What We Use It For

- **Code exploration** — our team asks questions about implementation details across all ProbeLabs projects and gets answers with file paths and line numbers
- **GitHub browsing** — check PRs, issues, releases, and activity across the `probelabs` org without leaving Slack
- **CI/CD debugging** — paste a failed pipeline link and get a root cause analysis with the relevant code context
- **Code changes** — describe what needs to change and the assistant explores the code, implements the fix, and opens a PR
- **Thread summaries** — catch up on long Slack discussions

## Running It

### CLI

```bash
git clone https://github.com/probelabs/probelabs-assistant.git
cd probelabs-assistant
cp .env.example .env
# Edit .env with your API keys

npx -y @probelabs/visor@latest run probelabs-assistant.yaml --tui
```

### Slack

```bash
npx -y @probelabs/visor@latest run probelabs-assistant.yaml --slack
```

Requires Slack tokens in `.env` — see [Environment Variables](#environment-variables) below.

## How It Works

A message goes through this pipeline:

1. **Intent classification** — is this `chat` or `code_help`?
2. **Skill selection** — which skills match the request?
3. **Dependency expansion** — `engineer` requires `code-explorer`, so both activate
4. **Knowledge injection** — each active skill injects its docs and tools into the AI context
5. **Execution** — the AI responds, calling code-talk, `gh` CLI, or Claude Code as needed

Everything is declared in YAML. No application code.

## Project Structure

```
probelabs-assistant.yaml          ← Main config: Slack, scheduler, system prompt
│
├── config/
│   ├── intents.yaml              ← Intent routing (chat, code_help)
│   └── skills.yaml               ← All skills with knowledge + tools
│
├── docs/                         ← Knowledge files injected into skills at runtime
│   ├── probelabs-architecture.md ← How our products fit together
│   ├── github-tools.md           ← gh CLI patterns for all repos
│   ├── github-actions-debugging.md
│   ├── code-exploration-tool.md
│   ├── code-help-mode.md
│   ├── engineer-tool.md
│   └── capabilities.md
│
└── workflows/
    └── engineer.yaml             ← Code changes + PR creation via Claude Code
```

## Skills

| Skill | When It Activates | What It Does |
|-------|-------------------|--------------|
| `github` | PRs, issues, releases, branches | Runs `gh` CLI commands across all ProbeLabs repos |
| `github-actions` | CI/CD failures, pipeline debugging | Fetches logs, greps for errors, identifies root cause |
| `code-explorer` | Code questions, implementation details | Semantic search across 15 repos via code-talk |
| `code-help` | General code Q&A | Injects coding conventions and project context |
| `engineer` | Code changes, PR requests | Explores code, implements changes, opens PRs via Claude Code |
| `capabilities` | "What can you do?" | Describes available skills |
| `thread-summary` | "Summarize this thread" | Condenses Slack conversations |

## Repositories

The code-explorer skill covers all ProbeLabs projects with smart routing — it knows that "search engine" means `probe`, "code review" means `visor`, and "workflow engine" means `visor-ee`.

| Repo | Language | Description |
|------|----------|-------------|
| [probe](https://github.com/probelabs/probe) | Rust | Semantic code search engine (ripgrep + tree-sitter) |
| [visor](https://github.com/probelabs/visor) | TypeScript | AI code review — GitHub Action + CLI |
| [visor-ee](https://github.com/probelabs/visor-ee) | TypeScript | Workflow engine powering this assistant |
| [goreplay](https://github.com/probelabs/goreplay) | Go | HTTP traffic capture and replay |
| [logoscope](https://github.com/probelabs/logoscope) | TypeScript | AI log analysis CLI + MCP server |
| [maid](https://github.com/probelabs/maid) | TypeScript | Mermaid diagram linter |
| [docs-mcp](https://github.com/probelabs/docs-mcp) | TypeScript | Turn any GitHub repo into an MCP server |
| [memaris](https://github.com/probelabs/memaris) | TypeScript | Persistent memory for Claude Code sessions |
| [afk](https://github.com/probelabs/afk) | Node.js | Remote control for Claude Code via Telegram |
| [big-brain](https://github.com/probelabs/big-brain) | TypeScript | MCP server for fresh AI insights when stuck |
| [vow](https://github.com/probelabs/vow) | TypeScript | Accountability gates for AI agents |
| [SandboxJS](https://github.com/probelabs/SandboxJS) | JavaScript | Safe eval runtime |
| [probelabs.com](https://github.com/probelabs/probelabs.com) | Web | Company website |
| [probe-quickstart](https://github.com/probelabs/probe-quickstart) | YAML | Quickstart template for building assistants |
| [company-data](https://github.com/probelabs/company-data) | — | Internal knowledge base — commercial docs, ideas, strategy (private) |
| [ground-control](https://github.com/probelabs/ground-control) | — | AI chat interface (private) |

## Example Conversations

```
"How does Probe's tree-sitter integration work?"
→ code-explorer activates, searches probelabs/probe, returns explanation with file paths

"Show me recent PRs on visor"
→ github activates, runs gh pr list --repo probelabs/visor

"Why is CI failing on probe PR #42?"
→ github-actions activates, fetches logs, identifies the failing test and root cause

"Add a --verbose flag to the probe CLI"
→ engineer + code-explorer activate, explores the code, implements the change, opens a PR
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google AI API key (Gemini) |
| `SLACK_APP_TOKEN` | For Slack | App-level token (`xapp-...`) for Socket Mode |
| `SLACK_BOT_TOKEN` | For Slack | Bot token (`xoxb-...`) for messages and API |
| `SLACK_SIGNING_SECRET` | For Slack | Webhook request verification |

### Slack App Setup

1. Create app at [api.slack.com/apps](https://api.slack.com/apps)
2. Enable **Socket Mode**
3. Add **Bot Token Scopes**: `app_mentions:read`, `channels:history`, `groups:history`, `im:history`, `mpim:history`, `chat:write`, `reactions:read`, `reactions:write`
4. Subscribe to **Bot Events**: `app_mention`, `message.channels`, `message.groups`, `message.im`
5. Install to workspace, copy tokens to `.env`

## Tests

```bash
npx -y @probelabs/visor@latest test
```

## Building Your Own

This repo is our production config. If you want to build something similar for your team:

1. Start with [probe-quickstart](https://github.com/probelabs/probe-quickstart) — a working assistant in one YAML file
2. Add your repos to the `code-explorer` skill's `projects` list
3. Add skills for your tools (Jira, Confluence, etc.) using MCP servers
4. Write knowledge docs in `docs/` and reference them with `{% readfile %}`
5. Use this repo as a reference for how skills, routing, and workflows fit together at scale

## Related

- [probe-quickstart](https://github.com/probelabs/probe-quickstart) — Start here to build your own assistant
- [probe](https://github.com/probelabs/probe) — The semantic code search engine underneath
- [visor](https://github.com/probelabs/visor) — Workflow engine and code review tool
- [visor-ee](https://github.com/probelabs/visor-ee) — Enterprise assistant workflows (code-talk, engineer, intent routing)

## License

MIT
