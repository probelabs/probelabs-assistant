## Find External Contributions

Find public GitHub pull requests and issues created by users who are *not* members of a specified organization.

### Parameters

- *Organization* (required): The GitHub organization to search (default: `probelabs`)
- *Days* (required): Number of days to look back (default: `7`)

### Execution Steps

Follow these steps in order. Run commands using `gh` CLI.

#### Step 1: Calculate the start date

Compute the date `N` days ago from today in `YYYY-MM-DD` format. Use this as the `created:>=` filter.

#### Step 2: Fetch organization members

Retrieve all member logins for the organization using the GraphQL API:

```bash
gh api graphql --paginate -f query='
query($org: String!, $cursor: String) {
  organization(login: $org) {
    membersWithRole(first: 100, after: $cursor) {
      nodes { login }
      pageInfo { hasNextPage endCursor }
    }
  }
}' -f org='<ORG>'
```

Extract the list of logins from the response. If there are multiple pages, collect all of them.

#### Step 3: Build the exclusion query

Construct a search query string that:
- Filters to items created on or after the start date: `created:>=YYYY-MM-DD`
- Excludes each organization member: `-author:member1 -author:member2 ...`

The full query string looks like:
```
is:public created:>=2026-02-04 -author:member1 -author:member2 -author:memberN
```

#### Step 4: Search for external pull requests

```bash
gh search prs --org <ORG> "<query_string>" --limit 100
```

#### Step 5: Search for external issues

```bash
gh search issues --org <ORG> "<query_string>" --limit 100
```

#### Step 6: Report findings

Present the results clearly:

- *If results found*: List each PR/issue with its title, repo, author, and URL. Group by type (PRs vs Issues).
- *If no results*: Report that no external contributions were found for the specified timeframe.
- Always state the organization name, timeframe searched, and number of members excluded.

### Notes

- The `--paginate` flag on the GraphQL call handles organizations with more than 100 members.
- The `gh search` commands may hit GitHub's search query length limits for organizations with very many members. If this happens, report the limitation to the user.
- Bot accounts (like `dependabot[bot]`) are not org members and will appear in results. Mention this if bot-authored items are present.

### Advanced Usage: Creating a Scheduled Report

This skill can be combined with other skills like `scheduler` and `github` to create powerful, automated reports.

*Example Scenario:* "set a daily morning reminder to show me currently opened OSS external contributions for last 7 days... Also give a brief on stars changed in last 24 hours"

*Execution Analysis (from trace `bd8080deedef1f005acf70152c034d36`):*

1.  *Decomposition*: The assistant correctly identified that this request required three separate skills:
    *   `scheduler`: To handle the "daily morning reminder" part.
    *   `find_external_contributions`: To perform the core task of finding PRs and issues from non-members.
    *   `github`: To fetch repository star statistics.

2.  *Orchestration*: The assistant chained these skills together:
    *   It first used the `scheduler` to set up the recurring task.
    *   The task's *action* was then defined by the combined logic of the `find_external_contributions` and `github` skills.
    *   The `find_external_contributions` logic was executed exactly as described in the steps above (fetch members, build exclusion query, search).
    *   The `github` skill was then used to gather star counts.
    *   Finally, the results from both were formatted into a single, coherent report to be delivered by the scheduler.

*Tips & Tricks for Complex Reporting:*

*   *Combine Skills*: Don't be afraid to activate multiple skills to fulfill a complex request. The assistant is designed to orchestrate them.
*   *Be Specific*: The more specific the user's request (e.g., "daily morning", "last 7 days"), the better the assistant can select and configure the right tools.
*   *Leverage Scheduling*: For any recurring reporting need, always combine the reporting skill (like this one) with the `scheduler` skill.
