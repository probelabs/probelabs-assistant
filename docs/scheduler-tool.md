# Scheduler Tool

The scheduler tool allows you to schedule reminders and workflow executions at specific times or recurring intervals.

## Capabilities

- **Create schedules**: Set up one-time or recurring reminders or workflow runs
- **List schedules**: View your active schedules
- **Cancel schedules**: Remove a scheduled task
- **Pause/Resume**: Temporarily disable or re-enable a schedule

## Scheduling a Reminder

To schedule a simple text reminder, just describe what you want to be reminded of and when. Any request without a `%` prefix is treated as a text reminder.

**Examples:**
- "remind me to check the build status in 1 hour"
- "remind me every morning at 9am to review open PRs"
- "schedule a reminder for tomorrow at 3pm to deploy to production"

## Scheduling a Workflow (Advanced)

To schedule a specific workflow, you **MUST** prefix the workflow name with a `%` symbol. This tells the scheduler that you want to execute a named workflow instead of creating a simple text reminder.

If you do not use the `%` prefix, your entire request will be treated as the text for a reminder.

**Correct Usage:**
- `schedule %daily-report every day at 8am` (Schedules the `daily-report` workflow)
- `schedule %run-security-scan every Friday at 5pm` (Schedules the `run-security-scan` workflow)

**Incorrect Usage (will create a text reminder instead of running a workflow):**
- `schedule daily-report every day at 8am`

## Managing Schedules

- **To see your active schedules:** "list my schedules"
- **To cancel a schedule:** "cancel schedule abc123"
- **To pause a schedule:** "pause schedule abc123"
- **To resume a schedule:** "resume schedule abc123"

## Context-Based Restrictions

The scheduler respects your current context:
- From a **DM**: You can only create/manage personal schedules
- From a **channel**: You can only create/manage channel schedules
- From a **group DM**: You can only create/manage group schedules

## Notes

- Schedule IDs are shown as 8-character codes
- You can only see and manage your own schedules
- Recurring schedules automatically calculate the next run time
