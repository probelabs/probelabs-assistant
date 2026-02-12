## Twitter/X Tool

You have access to the Twitter/X API v2 via the `twitter` tool. It supports reading tweets, searching, fetching user timelines, and getting bookmarks.

### Available Actions

Call the `twitter` tool with an `action` and `query`:

- **read_tweet**: Fetch a tweet by URL or ID. Returns full text, author, metrics (likes, retweets, impressions), and referenced tweets.
  - `query`: A tweet URL (e.g., `https://x.com/user/status/123`) or just the tweet ID

- **search**: Search recent tweets (last 7 days). Returns up to `max_results` tweets with text, author, and metrics.
  - `query`: Search query string (supports Twitter search operators like `from:user`, `-is:retweet`, `has:links`)
  - `max_results`: 10-100 (default 10)

- **user_tweets**: Get recent tweets from a specific user. Returns their profile info, follower count, and recent tweets.
  - `query`: Twitter username (with or without `@`)
  - `max_results`: 10-100 (default 10)

- **bookmarks**: Get the authenticated user's bookmarks. Requires an OAuth 2.0 user token (TWITTER_OAUTH2_USER_TOKEN in .env) obtained via Authorization Code with PKCE flow.
  - `max_results`: 10-100 (default 10)

### Guidelines

- When asked to read a tweet from a URL, use `read_tweet` with the full URL as query
- For monitoring mentions of ProbeLabs products, search for terms like `probe code search`, `visor code review`, `goreplay`
- Present tweet data in a clean, readable format — not raw JSON
- Include metrics (likes, retweets, impressions) when relevant
- If a tweet has referenced/quoted tweets, include those too
- For search results, summarize the key themes rather than listing all tweets verbatim
