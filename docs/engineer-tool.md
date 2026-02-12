## Engineer Tool

The `engineer` tool uses Claude Code to make actual code changes and create pull requests.

### CRITICAL RULES

1. **ALWAYS explore first** - Use `code-explorer` before calling `engineer` to understand the codebase
2. **Never call engineer more than once** for the same task
3. **Pass context from code-explorer** to avoid redundant code exploration
4. **Preserve PR URLs** - always use exact URLs from tool output, never construct them

### Communication Protocol

When using the `engineer` tool, you MUST follow this two-step communication protocol to ensure clarity:

1. **State Your Plan:** Before calling the `engineer` tool, inform the user of your plan.
   - Example: "I have analyzed the code. I will now use the engineer tool to create a pull request that fixes the issue."

2. **Report the Outcome:** After the `engineer` tool has executed, report the outcome with relevant details such as a PR link.
   - Example: "I have successfully created the pull request. You can review it here: https://github.com/probelabs/visor/pull/123"

This protocol prevents confusion and makes it clear when you are *about to take* an action vs. having *already completed* it.

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
