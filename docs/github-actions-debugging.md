# GitHub Actions Debugging Guide

You have access to bash commands for debugging GitHub Actions workflows using the `gh` CLI.

## Quick Reference Commands

### List Recent Workflow Runs
```bash
gh run list --repo probelabs/<repo> --limit 10
```

### View Workflow Run Details
```bash
gh run view <run_id> --repo probelabs/<repo>
```

### View Failed Job Logs (Most Useful)
```bash
gh run view <run_id> --repo probelabs/<repo> --log-failed
```

### View Specific Job Logs
```bash
gh run view <run_id> --repo probelabs/<repo> --job <job_id> --log
```

### List Workflow Files
```bash
gh workflow list --repo probelabs/<repo>
```

### View Workflow Definition
```bash
gh workflow view <workflow_name> --repo probelabs/<repo>
```

## Debugging Process

### Step 1: Identify the Failure
- Get the workflow run ID, repo from the user's message, PR link, or commit
- **CRUCIAL**: Always use the exact `job_id` provided in the user's message
- If they shared a PR, use: `gh pr checks <pr_number> --repo probelabs/<repo>`

### Step 2: Get Overview
```bash
gh run view <run_id> --repo probelabs/<repo>
```
This shows which jobs passed/failed and their duration.

### Step 3: Get Logs and Grep for Errors
```bash
gh api "repos/probelabs/<repo>/actions/jobs/<job_id>/logs" | \
  grep -nE -C 50 '(##\[error\]|::error|^Error:|Process completed with exit code|Exited with code|Traceback|Exception|fatal:|panic:|FAILED)'
```

### Step 4: Analyze the Error
Common failure patterns by project:

**Probe (Rust)**:
- Build failures: `cargo build` errors, missing crate features
- Test failures: `test result: FAILED`, assertion panics
- Clippy warnings treated as errors

**Visor / Visor-EE (TypeScript)**:
- Build: `tsc` compilation errors, missing types
- Tests: Jest/Vitest failures
- Lint: ESLint errors

**GoReplay (Go)**:
- Build: `go build` errors
- Tests: `--- FAIL:` markers

**General patterns**:
- **Timeout**: Job exceeded time limit
- **Dependency issues**: npm/cargo resolution failures
- **Docker**: Image build or registry errors
- **Permissions**: Token or access issues

### Step 5: Investigate Code (if needed)
Use the `code-explorer` tool to explore:
- `.github/workflows/` directory for workflow definitions
- Check recent commits that could be responsible for breaking tests
- Test files if a specific test is failing
- Source code if it's a build/compilation error

## Key ProbeLabs CI Workflows

| Repository | Common Workflows |
|------------|------------------|
| probe | `ci.yml`, `release.yml` (Rust build + test) |
| visor | `ci.yml`, `release.yml` (TypeScript build + test) |
| visor-ee | `ci.yml` (TypeScript) |
| goreplay | `ci.yml`, `release.yml` (Go build + test) |
| logoscope | `ci.yml` (TypeScript + npm publish) |
| maid | `ci.yml` (TypeScript) |

## Tips

1. **Start with `--log-failed`** - filters out noise from passing steps
2. **Check the job name** - different jobs test different things
3. **Look at the timestamp** - recent failures might be related to recent commits
4. **Compare with main branch** - is main also failing or just this PR?
5. **Handle large logs** - pipe to `tail -n 200` for the most recent lines
6. **Compare with previous successful runs** - `gh run list --repo probelabs/<repo> --status success --limit 5`
