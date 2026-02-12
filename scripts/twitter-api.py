#!/usr/bin/env python3
"""
Twitter/X API v2 helper script.

Usage:
  twitter-api.py read_tweet <tweet_url_or_id>
  twitter-api.py search <query> [--max_results=10]
  twitter-api.py bookmarks [--max_results=10]
  twitter-api.py user_tweets <username> [--max_results=10]

Environment variables:
  TWITTER_BEARER_TOKEN       - Required for read_tweet, search, user_tweets
  TWITTER_CONSUMER_KEY       - Required for bookmarks (OAuth 1.0a)
  TWITTER_SECRET_KEY         - Required for bookmarks (OAuth 1.0a)
  TWITTER_ACCESS_TOKEN       - Required for bookmarks (OAuth 1.0a)
  TWITTER_ACCESS_TOKEN_SECRET - Required for bookmarks (OAuth 1.0a)
"""

import sys
import os
import json
import re
import time
import hmac
import hashlib
import base64
import uuid
import urllib.parse
import urllib.request
import urllib.error


def oauth1_header(method, url, query_params, consumer_key, consumer_secret, access_token, access_token_secret):
    """Generate OAuth 1.0a Authorization header."""
    oauth_params = {
        'oauth_consumer_key': consumer_key,
        'oauth_nonce': uuid.uuid4().hex,
        'oauth_signature_method': 'HMAC-SHA1',
        'oauth_timestamp': str(int(time.time())),
        'oauth_token': access_token,
        'oauth_version': '1.0',
    }

    all_params = {**oauth_params, **query_params}
    sorted_params = '&'.join(
        f'{urllib.parse.quote(k, safe="")}'
        f'={urllib.parse.quote(str(v), safe="")}'
        for k, v in sorted(all_params.items())
    )

    base_string = (
        f'{method.upper()}'
        f'&{urllib.parse.quote(url, safe="")}'
        f'&{urllib.parse.quote(sorted_params, safe="")}'
    )

    signing_key = (
        f'{urllib.parse.quote(consumer_secret, safe="")}'
        f'&{urllib.parse.quote(access_token_secret, safe="")}'
    )

    signature = base64.b64encode(
        hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1).digest()
    ).decode()

    oauth_params['oauth_signature'] = signature
    auth_header = 'OAuth ' + ', '.join(
        f'{k}="{urllib.parse.quote(v, safe="")}"'
        for k, v in sorted(oauth_params.items())
    )
    return auth_header


def api_get(url, headers):
    """Make a GET request and return parsed JSON."""
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return {"error": json.loads(body), "status": e.code}
        except json.JSONDecodeError:
            return {"error": body, "status": e.code}


def get_bearer():
    token = os.environ.get('TWITTER_BEARER_TOKEN', '')
    if not token:
        print(json.dumps({"error": "TWITTER_BEARER_TOKEN not set"}))
        sys.exit(1)
    return token


def get_oauth1_creds():
    keys = ['TWITTER_CONSUMER_KEY', 'TWITTER_SECRET_KEY',
            'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET']
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        print(json.dumps({
            "error": f"OAuth 1.0a credentials missing: {', '.join(missing)}. "
                     f"Add them to .env for bookmarks support."
        }))
        sys.exit(1)
    return tuple(os.environ[k] for k in keys)


def extract_tweet_id(input_str):
    """Extract tweet ID from URL or return as-is."""
    match = re.search(r'(?:status|statuses)/(\d+)', input_str)
    if match:
        return match.group(1)
    if input_str.isdigit():
        return input_str
    return input_str


def format_tweet(tweet, users_map):
    """Format a tweet for readable output."""
    author = users_map.get(tweet.get('author_id', ''), {})
    metrics = tweet.get('public_metrics', {})
    result = {
        'id': tweet['id'],
        'author': f"@{author.get('username', '?')} ({author.get('name', '?')})",
        'text': tweet['text'],
        'created_at': tweet.get('created_at', ''),
    }
    if metrics:
        result['metrics'] = {
            'likes': metrics.get('like_count', 0),
            'retweets': metrics.get('retweet_count', 0),
            'replies': metrics.get('reply_count', 0),
            'impressions': metrics.get('impression_count', 0),
            'bookmarks': metrics.get('bookmark_count', 0),
        }
    # Expand URLs in entities
    entities = tweet.get('entities', {})
    if entities.get('urls'):
        result['links'] = [
            {'url': u.get('expanded_url', u.get('url', '')), 'display': u.get('display_url', '')}
            for u in entities['urls']
        ]
    return result


def build_users_map(includes):
    """Build a user ID -> user info map from API includes."""
    users = {}
    for u in (includes or {}).get('users', []):
        users[u['id']] = u
    return users


def cmd_read_tweet(args):
    if not args:
        print(json.dumps({"error": "Usage: read_tweet <tweet_url_or_id>"}))
        sys.exit(1)

    tweet_id = extract_tweet_id(args[0])
    bearer = get_bearer()

    url = (
        f"https://api.twitter.com/2/tweets/{tweet_id}"
        f"?tweet.fields=text,author_id,created_at,public_metrics,entities,conversation_id,in_reply_to_user_id"
        f"&expansions=author_id,referenced_tweets.id,referenced_tweets.id.author_id"
        f"&user.fields=name,username,description"
    )

    data = api_get(url, {"Authorization": f"Bearer {bearer}"})

    if 'errors' in data and 'data' not in data:
        print(json.dumps({"error": data['errors']}, indent=2))
        sys.exit(1)

    if 'data' not in data:
        print(json.dumps(data, indent=2))
        sys.exit(1)

    users_map = build_users_map(data.get('includes'))
    result = format_tweet(data['data'], users_map)

    # Include referenced tweets (quoted, replied to)
    if data.get('includes', {}).get('tweets'):
        result['referenced_tweets'] = [
            format_tweet(t, users_map) for t in data['includes']['tweets']
        ]

    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_search(args):
    if not args:
        print(json.dumps({"error": "Usage: search <query> [--max_results=10]"}))
        sys.exit(1)

    query = args[0]
    max_results = 10
    for a in args[1:]:
        if a.startswith('--max_results='):
            max_results = max(10, min(100, int(a.split('=')[1])))

    bearer = get_bearer()
    encoded_query = urllib.parse.quote(query, safe='')

    url = (
        f"https://api.twitter.com/2/tweets/search/recent"
        f"?query={encoded_query}"
        f"&tweet.fields=text,author_id,created_at,public_metrics,entities"
        f"&expansions=author_id"
        f"&user.fields=name,username"
        f"&max_results={max_results}"
    )

    data = api_get(url, {"Authorization": f"Bearer {bearer}"})

    if 'errors' in data and 'data' not in data:
        print(json.dumps({"error": data['errors']}, indent=2))
        sys.exit(1)

    users_map = build_users_map(data.get('includes'))
    tweets = [format_tweet(t, users_map) for t in data.get('data', [])]

    result = {
        "query": query,
        "count": len(tweets),
        "tweets": tweets,
    }
    if data.get('meta', {}).get('next_token'):
        result['has_more'] = True

    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_bookmarks(args):
    max_results = 10
    for a in args:
        if a.startswith('--max_results='):
            max_results = int(a.split('=')[1])

    consumer_key, consumer_secret, access_token, access_token_secret = get_oauth1_creds()

    # First get authenticated user ID
    me_url = "https://api.twitter.com/2/users/me"
    auth = oauth1_header('GET', me_url, {}, consumer_key, consumer_secret, access_token, access_token_secret)
    me_data = api_get(me_url, {"Authorization": auth})

    if 'data' not in me_data:
        print(json.dumps({"error": "Failed to get user info", "details": me_data}, indent=2))
        sys.exit(1)

    user_id = me_data['data']['id']

    # Get bookmarks
    base_url = f"https://api.twitter.com/2/users/{user_id}/bookmarks"
    query_params = {
        'tweet.fields': 'text,author_id,created_at,public_metrics,entities',
        'expansions': 'author_id',
        'user.fields': 'name,username',
        'max_results': str(max_results),
    }

    full_url = base_url + '?' + urllib.parse.urlencode(query_params)
    auth = oauth1_header('GET', base_url, query_params, consumer_key, consumer_secret, access_token, access_token_secret)
    data = api_get(full_url, {"Authorization": auth})

    if 'errors' in data and 'data' not in data:
        print(json.dumps({"error": data['errors']}, indent=2))
        sys.exit(1)

    users_map = build_users_map(data.get('includes'))
    tweets = [format_tweet(t, users_map) for t in data.get('data', [])]

    result = {
        "bookmarks_count": len(tweets),
        "bookmarks": tweets,
    }
    if data.get('meta', {}).get('next_token'):
        result['has_more'] = True

    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_user_tweets(args):
    if not args:
        print(json.dumps({"error": "Usage: user_tweets <username> [--max_results=10]"}))
        sys.exit(1)

    username = args[0].lstrip('@')
    max_results = 10
    for a in args[1:]:
        if a.startswith('--max_results='):
            max_results = int(a.split('=')[1])

    bearer = get_bearer()

    # First resolve username to user ID
    user_url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=name,description,public_metrics"
    user_data = api_get(user_url, {"Authorization": f"Bearer {bearer}"})

    if 'data' not in user_data:
        print(json.dumps({"error": f"User @{username} not found", "details": user_data}, indent=2))
        sys.exit(1)

    user_id = user_data['data']['id']
    user_info = user_data['data']

    # Get their tweets
    tweets_url = (
        f"https://api.twitter.com/2/users/{user_id}/tweets"
        f"?tweet.fields=text,created_at,public_metrics,entities"
        f"&max_results={max_results}"
    )

    tweets_data = api_get(tweets_url, {"Authorization": f"Bearer {bearer}"})
    users_map = {user_id: user_info}
    tweets = [format_tweet(t, users_map) for t in tweets_data.get('data', [])]

    result = {
        "user": f"@{username} ({user_info.get('name', '')})",
        "description": user_info.get('description', ''),
        "followers": user_info.get('public_metrics', {}).get('followers_count', 0),
        "count": len(tweets),
        "tweets": tweets,
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))


def load_env_file():
    """Load .env file from script directory or parent, without overwriting existing env."""
    for candidate in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'),
        os.path.join(os.getcwd(), '.env'),
    ]:
        path = os.path.normpath(candidate)
        if os.path.isfile(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    # Strip 'export ' prefix
                    if line.startswith('export '):
                        line = line[7:]
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            return


COMMANDS = {
    'read_tweet': cmd_read_tweet,
    'search': cmd_search,
    'bookmarks': cmd_bookmarks,
    'user_tweets': cmd_user_tweets,
}

if __name__ == '__main__':
    load_env_file()

    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(json.dumps({
            "error": f"Usage: {sys.argv[0]} <{'|'.join(COMMANDS.keys())}> [args...]"
        }))
        sys.exit(1)

    COMMANDS[sys.argv[1]](sys.argv[2:])
