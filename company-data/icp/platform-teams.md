# ICP: Platform & Infrastructure Teams

## Tagline

Stop Being the Bottleneck for Every Codebase Question.

## Profile

Platform engineers, infrastructure teams, and DevOps/SRE teams responsible for maintaining shared infrastructure, deployment pipelines, and internal developer platforms. They are overwhelmed by support requests from application teams and need to make platform knowledge self-serve while maintaining quality and compliance.

## Core Pain Points

- **The Support Tax** -- 40% of time spent answering questions already answered in code: "How does the deploy pipeline work?" "Which env vars does service X need?" "Why does this Terraform module exist?" Answers exist, nobody can find them.
- **The Documentation Treadmill** -- Docs written, infrastructure changes, docs go stale. App teams follow outdated runbooks and break things. Fix what they broke, update docs they won't read. Repeats every sprint.
- **The Scaling Wall** -- Org adds 3 new teams, each needs onboarding. Different tech stacks and requirements. A 4-person platform team now supports 12 app teams, and Jira is full of "help me deploy" tickets.

## What Changes with Probe

1. **Engineers self-serve from the actual source code** -- App teams query the codebase directly instead of filing tickets against the platform team.
2. **Platform knowledge lives in code, not wikis** -- Infrastructure-as-code is the documentation; Probe reads it directly so it never goes stale.
3. **Full service dependency context in seconds** -- Map dependencies across all repos and services instantly; know what breaks before pushing changes.

## Key Value Propositions

- **Cross-Service Visibility** -- Map dependencies across all repos and services. Know what breaks when you change something before you push.
- **Automated Quality Gates** -- Enforce platform standards on every PR. Catch Terraform misconfigurations, missing health checks, and security issues automatically.
- **Reduce Support Load** -- App teams query the codebase directly instead of filing tickets against the platform team.
- **Incident Intelligence** -- Correlate alerts with recent deploys, config changes, and dependency updates. Cut MTTR by giving on-call real context.

## Core Capabilities

### 1. Infrastructure-Aware Code Intelligence
- Ask any question about any service, Terraform module, or Helm chart and get answers grounded in actual code.
- Reads Terraform resources, Kubernetes manifests, Helm values, Docker compose files, and CI/CD pipelines.
- Connects application code with the infrastructure that runs it.
- Multi-repo architecture: query across app repos, infra repos, and shared libraries in one request.
- IaC-aware: understands Terraform, YAML, Dockerfiles natively.
- Dependency graphing: maps service-to-service, service-to-infrastructure, and shared resource dependencies.

### 2. Automated Platform Compliance
- Every PR reviewed against platform standards; every new service validated against golden path.
- Custom platform rules for infra, Dockerfiles, Helm charts, and CI configs.
- Security scanning: catch overly permissive IAM policies, open security groups, unencrypted resources.
- Breaking change detection: know when a shared module change affects downstream consumers.

### 3. Operational Intelligence
- Correlate incidents with code changes, config drifts, and dependency updates across the entire stack.
- Change correlation: link incidents to recent deploys, config changes, and dependency updates.
- Blast radius analysis: map which services are affected when a shared dependency fails.
- Runbook automation: surface and execute relevant runbooks based on incident context.

## Example Use Cases

- **Deployment pipeline walkthrough** -- Trace from git push to production for any namespace, including canary rollout and auto-rollback.
- **Connection pool investigation** -- Identify all services sharing a database connection pool and correlate with recent changes causing exhaustion.
- **Service dependency mapping** -- List all consumers of a service; identify breaking changes when upgrading versions.
- **Resource optimization** -- Scan Kubernetes resource limits across prod, identify over/under-provisioned services and waste.
- **Latency investigation** -- Trace the full request path, identify new synchronous calls or missing connection pooling causing spikes.
- **Terraform module audit** -- List all modules, their consumers, and which ones are stale (6+ months without update).
- **Health check audit** -- Morning check for services missing readiness/liveness probes; create tickets for gaps.
- **Infrastructure PR review** -- Validate Terraform plans for security group changes, overly broad IAM policies, state drift.
- **New service validation** -- Audit new repos against golden path (Dockerfile, health check, structured logging, graceful shutdown, Helm chart).
- **CVE scanning** -- Nightly scan of all Dockerfiles for base images with known CVEs; auto-open PRs to bump images.
- **Incident correlation** -- Correlate 503 errors with recent config changes, deploys, and infrastructure events.
- **Platform adoption reporting** -- Track which teams use standard Helm charts vs custom deployments, SDK version adoption.

## Workflow Packs

- **Infrastructure Review** (Every PR) -- Terraform plan validation, security policy compliance, downstream consumer impact analysis, cost estimation.
- **Incident Context Assembly** (On Incident) -- Recent change timeline, service dependency map, related past incidents, relevant runbook links.
- **Service Onboarding** (New Service) -- Golden path compliance audit, auto-generated issues for gaps, template links, platform SDK setup guide.
- **Infrastructure Hygiene** (Nightly) -- CVE scan with auto-bump PRs, resource waste report, state drift detection, module staleness audit.

## Trust & Enterprise Readiness

- **On-Premises Deployment** -- Runs entirely inside the customer's infrastructure. Meets SOC 2, HIPAA, and FedRAMP requirements.
- **Any LLM Provider** -- Use the org's preferred model (Claude, GPT, open-source, or self-hosted behind firewall).
- **Full Audit Trail** -- OpenTelemetry instrumentation on every query and workflow execution. Exports to Datadog, Grafana, or Splunk.
- **Open Source Core** -- Security team can audit exactly how code is processed.

## Open Source vs Enterprise

- **Open Source (Free)** -- Single-repo code intelligence, semantic code search (understands Terraform, YAML, Dockerfiles), no indexing, MCP integration, any LLM, privacy-first.
- **Enterprise** -- Multi-repo architecture, cross-service dependency mapping, AI-powered infrastructure review, Jira integration, Datadog/Grafana integration, incident correlation, workflow automation, intelligent routing, Slack/Teams integration, on-prem deployment.
