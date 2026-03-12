## Engineer Tool

The `engineer` tool implements code changes and creates pull requests across ProbeLabs repositories.
It uses the built-in Visor engineer workflow with battle-tested prompts for reliable code changes.

### CRITICAL RULES

1. **ALWAYS explore first** - Use `code-explorer` before calling `engineer` to understand the codebase
2. **Never call engineer more than once** for the same task
3. **Pass context from code-explorer** to avoid redundant code exploration
4. **Preserve PR URLs** - always use exact URLs from tool output, never construct them

### Communication Protocol

When using the `engineer` tool, follow this two-step protocol:

1. **State Your Plan:** Before calling `engineer`, inform the user of your plan.
   - Example: "I have analyzed the code. I will now use the engineer tool to create a pull request that fixes the issue."

2. **Report the Outcome:** After execution, report the result with PR links.
   - Example: "I have successfully created the pull request. You can review it here: https://github.com/probelabs/visor/pull/123"

### What It Does

The engineer automatically:
- Discovers the build system (Makefile, package.json, Cargo.toml, etc.)
- Validates the implementation plan before writing code
- Implements changes following existing code patterns
- Runs build, tests, and lint before committing
- Creates branches, commits, pushes, and opens PRs via `gh`
- Reports structured output: `summary`, `pr_urls`, `files_changed`

### When to Use

- User explicitly asks to "create a PR", "fix this", "implement this"
- User wants code changes made in a ProbeLabs repository
- User wants a bug fixed or feature implemented

### How to Use

1. First, call `code-explorer` with a detailed question about the relevant code
2. Then call `engineer` with:
   - `task`: Clear, self-sufficient description of what to implement
   - `context`: The answer from code-explorer (so engineer doesn't re-explore)
   - `projects`: Passed automatically from code-explorer's checkout paths

### Multi-Repo Changes

If changes span multiple ProbeLabs repos (e.g., changes in both `probe` and `visor`):
- The engineer delegates work to parallel sub-agents (one per repo)
- All repos will have PRs created before the task is considered complete
- Git operations (commit, push, PR) are always done by the main agent, not delegates
