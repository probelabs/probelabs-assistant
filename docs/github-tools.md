## GitHub Tools

You have access to the `gh` CLI for browsing and managing GitHub resources across all ProbeLabs repositories.

### ProbeLabs Repositories

| Repo | Language | Description |
|------|----------|-------------|
| `probelabs/probe` | Rust | Semantic code search engine |
| `probelabs/visor` | TypeScript | AI code review tool (GitHub Action + CLI) |
| `probelabs/visor-ee` | TypeScript | Visor Enterprise - workflow engine for AI assistants |
| `probelabs/probelabs.com` | Web | Official website |
| `probelabs/probe-quickstart` | YAML | Quickstart template for AI assistants |
| `probelabs/maid` | TypeScript | Mermaid diagram linter |
| `probelabs/goreplay` | Go | HTTP traffic capture and replay |
| `probelabs/logoscope` | TypeScript | AI log analysis CLI + MCP server |
| `probelabs/docs-mcp` | TypeScript | Turn GitHub repos into MCP servers |
| `probelabs/memaris` | TypeScript | Claude Code session memory |
| `probelabs/afk` | Node.js | Remote control for Claude Code via Telegram |
| `probelabs/big-brain` | TypeScript | MCP Server for AI insights |
| `probelabs/vow` | TypeScript | Accountability gates for AI agents |
| `probelabs/SandboxJS` | JavaScript | Safe eval runtime (fork) |
| `probelabs/ground-control` | - | AI chat interface (private) |

### Quick Reference Commands

#### Browse Issues
```bash
# List open issues for a repo
gh issue list --repo probelabs/<repo> --limit 20

# View a specific issue
gh issue view <number> --repo probelabs/<repo>

# Search issues across repos
gh search issues --owner probelabs "<query>"
```

#### Browse Pull Requests
```bash
# List open PRs
gh pr list --repo probelabs/<repo>

# View a specific PR with details
gh pr view <number> --repo probelabs/<repo>

# View PR diff
gh pr diff <number> --repo probelabs/<repo>

# View PR checks/CI status
gh pr checks <number> --repo probelabs/<repo>

# List merged PRs (recent)
gh pr list --repo probelabs/<repo> --state merged --limit 10
```

#### Browse Releases
```bash
# List releases
gh release list --repo probelabs/<repo>

# View latest release
gh release view --repo probelabs/<repo>

# View specific release
gh release view <tag> --repo probelabs/<repo>
```

#### Repository Info
```bash
# View repo details
gh repo view probelabs/<repo>

# List all ProbeLabs repos
gh repo list probelabs --limit 50

# View repo README
gh repo view probelabs/<repo> --web
```

#### Cross-Repo Search
```bash
# Search code across ProbeLabs
gh search code --owner probelabs "<query>"

# Search issues across all repos
gh search issues --owner probelabs "<query>"

# Search PRs across all repos
gh search prs --owner probelabs "<query>"
```

#### Branch and Commit Info
```bash
# List branches
gh api repos/probelabs/<repo>/branches --jq '.[].name'

# View recent commits
gh api repos/probelabs/<repo>/commits --jq '.[:10] | .[] | "\(.sha[:7]) \(.commit.message | split("\n")[0])"'

# Compare branches
gh api repos/probelabs/<repo>/compare/<base>...<head> --jq '.commits[] | "\(.sha[:7]) \(.commit.message | split("\n")[0])"'
```

### Multi-Repo Overview

When asked about the overall state of ProbeLabs projects, gather info from multiple repos:

```bash
# Recent activity across key repos
for repo in probe visor visor-ee logoscope maid; do
  echo "=== probelabs/$repo ==="
  gh pr list --repo probelabs/$repo --limit 3
  echo ""
done
```

### Tips

1. **Always specify `--repo probelabs/<name>`** - never assume a default repo
2. **Use `--json` flag** for structured output when processing data
3. **Use `gh api`** for advanced queries not covered by standard commands
4. **Check both issues and PRs** - some teams use issues for tracking, others use PR descriptions
5. **For private repos** (ground-control) - access depends on authentication scope
