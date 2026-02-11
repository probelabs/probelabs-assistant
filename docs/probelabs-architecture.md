# ProbeLabs Architecture

ProbeLabs builds developer tools focused on AI-assisted software development. The product ecosystem centers around two core platforms: **Probe** (semantic code search) and **Visor** (code review and workflow automation).

## Core Products

### Probe - Semantic Code Search
- **Repo**: `probelabs/probe` (Rust)
- **Purpose**: AI-friendly, fully local code search engine for large codebases
- **Tech**: ripgrep for fast file search + tree-sitter for AST-aware code extraction
- **Key Features**: ElasticSearch-style query syntax, MCP server mode, code block extraction
- **Used By**: Visor code-talk workflows, docs-mcp, developer tooling

### Visor - AI Code Review
- **Repo**: `probelabs/visor` (TypeScript)
- **Purpose**: Automated PR code review via GitHub Action and CLI
- **Tech**: TypeScript, GitHub API, multi-model AI (Claude, GPT)
- **Key Features**: Security analysis, performance review, style checking, architecture analysis
- **Distribution**: GitHub Action, npm CLI

### Visor Enterprise (visor-ee)
- **Repo**: `probelabs/visor-ee` (TypeScript)
- **Purpose**: Workflow engine for building AI assistants (like this one)
- **Tech**: TypeScript, Slack SDK, MCP protocol
- **Key Features**: Intent routing, skill classification, code-talk workflows, engineer workflows
- **Used By**: Tyk Oel assistant, ProbeLabs assistant

## Developer Tools

### GoReplay
- **Repo**: `probelabs/goreplay` (Go)
- **Purpose**: HTTP traffic capture and replay for testing
- **History**: Mature OSS project, widely used in production environments

### Logoscope
- **Repo**: `probelabs/logoscope` (TypeScript)
- **Purpose**: AI-optimized log analysis with pattern detection
- **Distribution**: npm package, MCP server

### Maid
- **Repo**: `probelabs/maid` (TypeScript)
- **Purpose**: Mermaid diagram linter for humans and AI

## AI Agent Tools

### Memaris
- **Repo**: `probelabs/memaris`
- **Purpose**: Convert Claude Code sessions into persistent memory

### AFK
- **Repo**: `probelabs/afk` (Node.js)
- **Purpose**: Remote control and approval for Claude Code via Telegram

### BigBrain
- **Repo**: `probelabs/big-brain`
- **Purpose**: MCP server for getting fresh AI insights when stuck

### Vow
- **Repo**: `probelabs/vow`
- **Purpose**: Accountability gates for autonomous AI agents

### Docs MCP
- **Repo**: `probelabs/docs-mcp`
- **Purpose**: Turn any GitHub repo into an MCP server for chatting with code/docs

### SandboxJS
- **Repo**: `probelabs/SandboxJS` (fork)
- **Purpose**: Safe JavaScript eval runtime, used by Visor

## Project Relationships

```
Probe (search engine)
  └── Used by: visor-ee code-talk, docs-mcp, probe-quickstart

Visor (code review)
  ├── Uses: GitHub API, AI models
  └── SandboxJS (safe eval)

Visor-EE (workflow engine)
  ├── Uses: Probe (via code-talk), Slack SDK, MCP protocol
  ├── Hosts: ProbeLabs assistant, Tyk Oel assistant
  └── Imports: assistant.yaml, code-talk workflow

AI Tools (memaris, afk, big-brain, vow)
  └── Standalone CLIs / MCP servers for AI development workflows

GoReplay (traffic replay)
  └── Standalone Go application

probelabs.com (website)
  └── Marketing site for all products
```

## Internal Knowledge

### Company Data
- **Repo**: `probelabs/company-data` (private)
- **Purpose**: Internal knowledge base — commercial docs, ideas, strategy, business context
- **Note**: Not code — use `analyze_all` for comprehensive document analysis

## Tech Stack Summary

| Language | Projects |
|----------|----------|
| Rust | probe |
| TypeScript | visor, visor-ee, logoscope, maid, docs-mcp, big-brain |
| Go | goreplay |
| Node.js | afk, memaris |
| JavaScript | SandboxJS, vow |
