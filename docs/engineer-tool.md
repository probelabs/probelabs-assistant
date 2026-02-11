## Engineer Tool

The `engineer` tool uses Claude Code to make actual code changes and create pull requests.

### CRITICAL RULES

1. **ALWAYS explore first** - Use `code-explorer` before calling `engineer` to understand the codebase
2. **Never call engineer more than once** for the same task
3. **Pass context from code-explorer** to avoid redundant code exploration
4. **Preserve PR URLs** - always use exact URLs from tool output, never construct them

### When to Use

- User explicitly asks to "create a PR", "fix this", "implement this"
- User wants code changes made in a ProbeLabs repository
- User wants a bug fixed or feature implemented

### How to Use

1. First, call `code-explorer` with a detailed question about the relevant code
2. Then call `engineer` with:
   - `task`: Clear description of what to implement
   - `context`: The answer from code-explorer (so engineer doesn't re-explore)
   - `projects`: List of project directory paths from code-explorer's `checkout_projects`

### Multi-Repo Changes

If changes span multiple ProbeLabs repos (e.g., changes in both `probe` and `visor`):
- Include all relevant project paths
- The engineer tool will handle multi-repo changes with sub-agents
- All repos must have PRs created before the task is considered complete
