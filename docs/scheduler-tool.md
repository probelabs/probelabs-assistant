# Scheduler Tool

The scheduler tool allows you to schedule workflow executions at specific times or recurring intervals.

## Capabilities

- **Create schedules**: Set up one-time or recurring workflow runs
- **List schedules**: View your active schedules
- **Cancel schedules**: Remove a scheduled task
- **Pause/Resume**: Temporarily disable or re-enable a schedule

## Usage Examples

### One-time schedules
- "Remind me in 2 hours to check the PR"
- "Schedule a status check for tomorrow at 9am"
- "Run this again next Monday at 3pm"

### Recurring schedules
- "Run the status-check every weekday at 9am"
- "Remind me every Monday at 10am about releases"
- "Schedule a repo health check every Sunday at midnight"

### Managing schedules
- "List my schedules"
- "What schedules do I have?"
- "Cancel schedule abc123"
- "Pause schedule def456"

## Context-Based Restrictions

The scheduler respects your current context:
- From a **DM**: You can only create/manage personal schedules
- From a **channel**: You can only create/manage channel schedules
- From a **group DM**: You can only create/manage group schedules

## Notes

- Schedule IDs are shown as 8-character codes
- You can only see and manage your own schedules
- Recurring schedules automatically calculate the next run time
