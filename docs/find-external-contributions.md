## Find External Contributions

Find public GitHub pull requests and issues created by users who are **not** members of a specified organization.

### Parameters

- **Organization** (required): The GitHub organization to search (default: `probelabs`)
- **Days** (required): Number of days to look back (default: `7`)

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

- **If results found**: List each PR/issue with its title, repo, author, and URL. Group by type (PRs vs Issues).
- **If no results**: Report that no external contributions were found for the specified timeframe.
- Always state the organization name, timeframe searched, and number of members excluded.

### Notes

- The `--paginate` flag on the GraphQL call handles organizations with more than 100 members.
- The `gh search` commands may hit GitHub's search query length limits for organizations with very many members. If this happens, report the limitation to the user.
- Bot accounts (like `dependabot[bot]`) are not org members and will appear in results. Mention this if bot-authored items are present.
