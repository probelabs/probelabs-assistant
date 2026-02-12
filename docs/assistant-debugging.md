## Debugging the ProbeLabs Assistant

The ProbeLabs Assistant is built on the Visor workflow engine. When something goes wrong — a skill doesn't activate,
a tool call fails, or a response is unexpected — you can use the techniques below to diagnose the issue.

### CRITICAL: When Given a Trace ID

**If the user provides a trace ID, you MUST fetch it from Jaeger FIRST before doing anything else:**

```bash
curl -s "http://localhost:8001/api/traces/{trace_id}" | jq
```

Replace `{trace_id}` with the actual trace ID. This returns the full trace data including all spans,
tags, and logs. Analyze this data to understand what happened - do NOT try to answer by reading
code files alone.

### Jaeger Traces

Every assistant request is instrumented with OpenTelemetry and exported to a local Jaeger instance.
Traces give you full visibility into the execution flow: which skills were activated, which tools
were called, how long each step took, and where errors occurred.

**Accessing Jaeger UI:**
- Local Jaeger UI: `http://localhost:16686`
- Jaeger API (used internally): `http://localhost:8001/api`

**Fetching a trace by ID:**
```bash
curl -s "http://localhost:8001/api/traces/{trace_id}" | jq
```

**Searching for recent traces:**
```bash
# Find traces for the visor service in the last hour
curl -s "http://localhost:8001/api/traces?service=visor&limit=20" | jq
```

**Key spans to look for:**
- `visor.run` — The top-level span for the entire workflow execution. Contains tags like
  `slack.user_id`, `slack.channel`, and `workflow.name`.
- `visor.check.*` — Individual check/step executions (e.g., `visor.check.chat`,
  `visor.check.route-intent`). These show the execution of each step in the workflow.
- `ai.chat` — AI model calls. Look at duration to identify slow LLM responses.
- `mcp.*` — MCP tool invocations (code-explorer, engineer, etc.).

**Analyzing a trace:**
1. Identify all spans and their parent/child relationships to understand execution flow.
2. Check for error tags (`error=true`, `otel.status_code=ERROR`) on any span.
3. Examine span durations to find performance bottlenecks.
4. Look at span tags and logs for context (e.g., which skill was activated, what prompt was used).
5. Follow the dependency chain: `visor.run` → `route-intent` → `chat-answer` → tool calls.

**Common issues visible in traces:**
- Skill not activated: Check the `route-intent` span for classification output.
- Tool call failed: Look for error spans under `mcp.*` with error messages in tags.
- Slow responses: Compare durations across spans to find the bottleneck (usually AI or MCP calls).
- Missing context: Check if the expected knowledge was injected by examining prompt-related tags.

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/probelabs/probelabs-assistant.git
   cd probelabs-assistant
   ```

2. **Set environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your tokens and API keys
   ```

3. **Run the assistant locally:**
   ```bash
   npx -y @probelabs/visor@latest run probelabs-assistant.yaml
   ```

4. **Enable verbose logging:**
   ```bash
   npx -y @probelabs/visor@latest run probelabs-assistant.yaml -v
   ```

### Debugging Tips

- **Skill classification issues:** If the wrong skill is activated (or none at all), check the
  skill `description` fields in `config/skills.yaml`. The description is what the intent router
  uses to match user requests to skills.
- **Knowledge not injected:** Verify that the skill's `knowledge` field references the correct
  doc file path and that the file exists in `docs/`.
- **MCP tool failures:** Check that the required environment variables are set and that the
  MCP server process can start.
- **Workflow errors:** Use `visor test` to check for YAML issues before running.
