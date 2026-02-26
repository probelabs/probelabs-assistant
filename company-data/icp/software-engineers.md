# ICP: Software Engineers & Developers

## Tagline

Stop Reading Code You Didn't Write.

## Profile

Individual software engineers and developers who spend significant time understanding unfamiliar codebases, performing code reviews, debugging issues across services, and navigating complex systems. They need fast, accurate code intelligence to be productive without relying on teammates who "know how this works."

## Core Pain Points

- **The Onboarding Wall** -- New repo, no documentation, outdated README. First week spent figuring out where things live and who to ask. First real PR takes 10 days instead of 2.
- **The Hidden Dependency** -- Changing a function signature passes tests locally, but breaks a service you've never heard of in production because it depends on the exact return format.
- **The Context Switch Tax** -- Deep in a debugging session, you need to understand the auth middleware. It calls three modules, which import shared utilities. An hour later, 15 files read, original thread lost.

## What Changes with Probe

1. **Full architecture context in seconds** -- Ask questions about architecture, patterns, and dependencies and get accurate answers immediately.
2. **Self-serve answers from the actual source code** -- No more waiting on Slack for "who knows this?" Get answers from the codebase itself, any time.
3. **Know every dependency before you push** -- See the dependencies, side effects, and blast radius before pushing. Fewer production incidents, fewer rollbacks.

## Key Value Propositions

- **Instant Codebase Understanding** -- Ask questions about architecture, patterns, and dependencies; get accurate answers in seconds (not grep-and-pray).
- **Faster Code Reviews** -- Automated first-pass review catches security issues, style violations, and breaking changes before human review.
- **Ship Without Fear** -- Know dependencies, side effects, and blast radius before pushing.
- **Zero Interruptions** -- Stop waiting on teammates; get answers from the source code itself, any time.

## Core Capabilities

### 1. Instant Codebase Understanding
- Semantic code reading (functions, classes, dependencies, call graphs) -- not just text search.
- Multi-repo awareness: query across microservices, shared libraries, and infrastructure code.
- AST-aware search: understands functions, types, and call graphs.
- Historical context: learn why code was written from past PRs and tickets.

### 2. AI-Powered Code Reviews
- Team-specific rules configurable per repo, per team, per language.
- Breaking change detection: catch API changes that will break consumers.
- Security & performance checks: OWASP vulnerabilities, N+1 queries, missing timeouts.
- Learns the team's patterns and applies them consistently to every PR.

### 3. Full System Intelligence
- Maps the entire system: service boundaries, data flows, event subscriptions, API contracts.
- Dependency mapping: see every consumer of changed code across all repositories.
- Impact analysis: know the blast radius of a change before pushing.
- Regression tracing: find which change introduced a bug by comparing versions.

## Example Use Cases

- **Auth flow walkthrough** -- Trace authentication from login request to session creation, with exact file paths.
- **Nil pointer debugging** -- Trace data flow in an order processing pipeline, identify all sources of nil.
- **Safe model changes** -- Identify all migrations, serializers, tests, and downstream consumers when adding a field.
- **Performance regression** -- Correlate response time spikes with merged PRs to find the culprit.
- **Event system mapping** -- Map all event types, publishers, and subscribers across the system.
- **External HTTP call audit** -- Find every external HTTP call, check timeouts and retry logic.
- **Dependency license/CVE check** -- On every PR, verify new dependencies for license compatibility and known vulnerabilities.
- **Pre-commit test analysis** -- Run tests, analyze failures, suggest fixes, confirm before applying.
- **Ticket-to-code mapping** -- Read a Jira ticket, find relevant code, understand the problem, produce a plan of attack.
- **Error handling audit** -- Identify inconsistent error handling patterns and locate files that need updating.
- **Test plan generation** -- Generate comprehensive test plans covering happy path, edge cases, and failure modes.
- **Refactoring impact analysis** -- Identify everything that would break when changing a struct or API contract.

## Workflow Packs

- **Automated Code Review** (Every PR) -- Security vulnerability scan, performance regression check, breaking API change detection, style/pattern enforcement.
- **Codebase Onboarding** (New Project) -- Architecture overview, service dependency map, key abstractions guide, common task walkthroughs.
- **Root Cause Analysis** (Debugging) -- Code path trace from symptom, recent change correlation, related issue history, suggested fix with context.
- **Impact Analysis** (Before Push) -- Cross-repo dependency trace, consumer impact report, test coverage gaps, migration requirements.

## Trust & Enterprise Readiness

- **Runs Locally** -- Code never leaves the developer's environment.
- **Any LLM Provider** -- Claude, GPT, open-source, or self-hosted. No vendor lock-in.
- **Full Audit Trail** -- OpenTelemetry instrumentation on every query and workflow run.
- **Open Source Core** -- The core engine is open source and auditable.

## Open Source vs Enterprise

- **Open Source (Free)** -- Single-repo code understanding, semantic search, no indexing, MCP integration, any LLM, privacy-first.
- **Enterprise** -- Multi-repo architecture, cross-service dependency mapping, AI-powered code reviews, Jira/Zendesk integration, version comparison, workflow automation, intelligent routing, Slack/Teams integration, on-prem deployment.
