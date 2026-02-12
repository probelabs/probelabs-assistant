#!/usr/bin/env python3
"""
OAuth 2.0 PKCE token generator for Twitter/X API.

Usage:
  twitter-oauth2.py          # Start full flow (opens browser, runs callback server)
  twitter-oauth2.py refresh   # Refresh an expired token using TWITTER_OAUTH2_REFRESH_TOKEN

Generates a user access token with scopes: tweet.read, users.read, bookmark.read
"""

import sys
import os
import json
import secrets
import hashlib
import base64
import urllib.parse
import urllib.request
import webbrowser
import http.server
import threading


def load_env():
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
                    if line.startswith('export '):
                        line = line[7:]
                    key, _, value = line.partition('=')
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            return


def exchange_code(code, code_verifier, client_id, client_secret, redirect_uri):
    """Exchange authorization code for access token."""
    url = 'https://api.twitter.com/2/oauth2/token'
    data = urllib.parse.urlencode({
        'code': code,
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier,
    }).encode()

    # Use Basic auth with client_id:client_secret
    credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded',
    })

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Token exchange failed ({e.code}): {body}", file=sys.stderr)
        sys.exit(1)


def refresh_token(refresh_tok, client_id, client_secret):
    """Refresh an expired access token."""
    url = 'https://api.twitter.com/2/oauth2/token'
    data = urllib.parse.urlencode({
        'refresh_token': refresh_tok,
        'grant_type': 'refresh_token',
        'client_id': client_id,
    }).encode()

    credentials = base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded',
    })

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Token refresh failed ({e.code}): {body}", file=sys.stderr)
        sys.exit(1)


def update_env_file(key, value):
    """Add or update a key in the .env file."""
    env_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
    if not os.path.isfile(env_path):
        env_path = os.path.join(os.getcwd(), '.env')

    lines = []
    found = False
    if os.path.isfile(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip().startswith(f'{key}=') or line.strip().startswith(f'export {key}='):
                    lines.append(f'{key}={value}\n')
                    found = True
                else:
                    lines.append(line)

    if not found:
        lines.append(f'{key}={value}\n')

    with open(env_path, 'w') as f:
        f.writelines(lines)


def get_oauth2_client_creds():
    """Get OAuth 2.0 client credentials, preferring TWITTER_CLIENT_ID/SECRET."""
    client_id = os.environ.get('TWITTER_CLIENT_ID', '') or os.environ.get('TWITTER_CONSUMER_KEY', '')
    client_secret = os.environ.get('TWITTER_CLIENT_SECRET', '') or os.environ.get('TWITTER_SECRET_KEY', '')
    if not client_id or not client_secret:
        print("Error: TWITTER_CLIENT_ID and TWITTER_CLIENT_SECRET must be set in .env")
        sys.exit(1)
    return client_id, client_secret


def full_flow():
    """Run the full OAuth 2.0 PKCE flow with a local callback server."""
    client_id, client_secret = get_oauth2_client_creds()

    redirect_uri = 'http://localhost:3000/callback'

    # Generate PKCE
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip('=')
    state = secrets.token_urlsafe(16)

    auth_url = (
        f'https://x.com/i/oauth2/authorize'
        f'?response_type=code'
        f'&client_id={urllib.parse.quote(client_id)}'
        f'&redirect_uri={urllib.parse.quote(redirect_uri)}'
        f'&scope=tweet.read%20users.read%20bookmark.read'
        f'&state={state}'
        f'&code_challenge={code_challenge}'
        f'&code_challenge_method=S256'
    )

    # Set up callback server
    auth_code = [None]
    server_done = threading.Event()

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            if 'code' in params:
                received_state = params.get('state', [''])[0]
                if received_state != state:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'State mismatch!')
                    return

                auth_code[0] = params['code'][0]
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<h1>Authorization successful!</h1><p>You can close this tab.</p>')
                server_done.set()
            else:
                self.send_response(400)
                self.end_headers()
                error = params.get('error', ['unknown'])[0]
                self.wfile.write(f'Error: {error}'.encode())
                server_done.set()

        def log_message(self, format, *args):
            pass  # Suppress server logs

    server = http.server.HTTPServer(('localhost', 3000), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("Opening browser for Twitter authorization...")
    print(f"If browser doesn't open, visit:\n{auth_url}\n")
    webbrowser.open(auth_url)

    print("Waiting for callback on http://localhost:3000/callback ...")
    server_done.wait(timeout=120)
    server.shutdown()

    if not auth_code[0]:
        print("Error: No authorization code received (timeout or user denied)")
        sys.exit(1)

    print("Got authorization code, exchanging for token...")
    token_data = exchange_code(auth_code[0], code_verifier, client_id, client_secret, redirect_uri)

    access_token = token_data.get('access_token', '')
    refresh_tok = token_data.get('refresh_token', '')
    expires_in = token_data.get('expires_in', 0)
    scope = token_data.get('scope', '')

    print(f"\nSuccess!")
    print(f"  Scopes: {scope}")
    print(f"  Expires in: {expires_in}s ({expires_in // 3600}h)")

    # Save to .env
    update_env_file('TWITTER_OAUTH2_USER_TOKEN', access_token)
    print(f"  Saved TWITTER_OAUTH2_USER_TOKEN to .env")

    if refresh_tok:
        update_env_file('TWITTER_OAUTH2_REFRESH_TOKEN', refresh_tok)
        print(f"  Saved TWITTER_OAUTH2_REFRESH_TOKEN to .env")
        print(f"\n  When token expires, run: python3 scripts/twitter-oauth2.py refresh")


def do_refresh():
    """Refresh an expired token."""
    client_id, client_secret = get_oauth2_client_creds()
    refresh_tok = os.environ.get('TWITTER_OAUTH2_REFRESH_TOKEN', '')

    if not refresh_tok:
        print("Error: TWITTER_OAUTH2_REFRESH_TOKEN not set. Run full flow first.")
        sys.exit(1)

    print("Refreshing token...")
    token_data = refresh_token(refresh_tok, client_id, client_secret)

    access_token = token_data.get('access_token', '')
    new_refresh = token_data.get('refresh_token', '')
    expires_in = token_data.get('expires_in', 0)

    update_env_file('TWITTER_OAUTH2_USER_TOKEN', access_token)
    print(f"  Saved new TWITTER_OAUTH2_USER_TOKEN (expires in {expires_in // 3600}h)")

    if new_refresh:
        update_env_file('TWITTER_OAUTH2_REFRESH_TOKEN', new_refresh)
        print(f"  Saved new TWITTER_OAUTH2_REFRESH_TOKEN")


if __name__ == '__main__':
    load_env()

    if len(sys.argv) > 1 and sys.argv[1] == 'refresh':
        do_refresh()
    else:
        full_flow()
