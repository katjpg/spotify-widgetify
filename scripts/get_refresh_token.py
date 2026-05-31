#!/usr/bin/env python3
# Create a Spotify refresh token for the app (one-time, run locally).
#
# Prerequisites:
# - Add http://127.0.0.1:8888/callback to the app's Redirect URIs
#   (dashboard: https://developer.spotify.com/dashboard -> select app -> Redirect URIs)
# - .env must contain SPOTIFY_CLIENT_ID (the client secret is not used here)
#
# Run:
#   uv run python scripts/get_refresh_token.py
#
# NOTE: this script, in order:
# 1. opens the Spotify consent page
# 2. captures the redirect on 127.0.0.1:8888
# 3. exchanges the code via Authorization Code + PKCE
# 4. confirms the token can be refreshed
# 5. writes SPOTIFY_REFRESH_TOKEN to .env

import base64
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"

# verify via: dashboard -> app -> redirect uris
REDIRECT_URI = "http://127.0.0.1:8888/callback"
CALLBACK_HOST = "127.0.0.1"
CALLBACK_PORT = 8888

# default scopes; but these can be adjusted
SCOPES = "user-read-currently-playing user-read-recently-played"

CALLBACK_TIMEOUT_SECONDS = 180


def _read_env_file(path: Path) -> dict[str, str]:
    """Read KEY=VALUE pairs from a .env file.

    Minimal parser for this setup script: skips comments and blank lines and
    strips one layer of surrounding quotes. It does not handle multiline values
    or the `export` prefix.
    """
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value
    return values


def _get_required_setting(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value

    env_values = _read_env_file(ENV_PATH)
    value = env_values.get(name)
    if value:
        return value

    sys.exit(f"Missing required setting: {name}")


def _generate_code_verifier(length: int = 64) -> str:
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def _mask(value: str, prefix: int = 6, suffix: int = 4) -> str:
    if len(value) <= prefix + suffix:
        return "*" * len(value)
    return f"{value[:prefix]}...{value[-suffix:]}"


def _upsert_env_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text().splitlines() if path.exists() else []
    updated: list[str] = []
    replaced = False

    for line in lines:
        if line.startswith(f"{key}="):
            updated.append(f"{key}={value}")
            replaced = True
        else:
            updated.append(line)

    if not replaced:
        updated.append(f"{key}={value}")

    path.write_text("\n".join(updated).rstrip() + "\n")

    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


class _CallbackHandler(BaseHTTPRequestHandler):
    result: dict[str, list[str]] | None = None

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)

        # NOTE: the browser may request /favicon.ico before /callback;
        # ignore non-callback paths so the loop keeps serving until /callback arrives.
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return

        _CallbackHandler.result = urllib.parse.parse_qs(
            parsed.query, keep_blank_values=True
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h1>Authorization received.</h1><p>You can close this tab.</p></body></html>"
        )

    def log_message(self, format: str, *args) -> None:
        return


def _build_authorize_url(client_id: str, state: str, code_challenge: str) -> str:
    params = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
            "state": state,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
            "show_dialog": "true",
        }
    )
    return f"{AUTH_URL}?{params}"


def _start_callback_server() -> HTTPServer:
    """Return a server listening on the loopback callback address.

    Call before opening the browser: if the redirect arrives before the socket
    is listening, the browser reports connection refused and the flow stalls.
    """
    _CallbackHandler.result = None
    try:
        server = HTTPServer((CALLBACK_HOST, CALLBACK_PORT), _CallbackHandler)
    except OSError as exc:
        sys.exit(f"Cannot bind {CALLBACK_HOST}:{CALLBACK_PORT} for the callback: {exc}")
    server.timeout = 1
    return server


def _capture_code(server: HTTPServer, expected_state: str) -> str:
    started = time.monotonic()
    while _CallbackHandler.result is None:
        if time.monotonic() - started > CALLBACK_TIMEOUT_SECONDS:
            server.server_close()
            sys.exit("Timed out waiting for Spotify callback.")
        server.handle_request()

    server.server_close()
    params = _CallbackHandler.result or {}

    if "error" in params:
        sys.exit(f"Authorization denied: {params['error'][0]}")

    if params.get("state", [""])[0] != expected_state:
        sys.exit("State mismatch; aborting.")

    code = params.get("code", [""])[0]
    if not code:
        sys.exit("Missing authorization code in callback.")

    return code


def _post_form(url: str, data: dict[str, str]) -> dict:
    body = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")[:500]
        sys.exit(f"HTTP {exc.code} from Spotify: {details}")


def _exchange_code_for_tokens(client_id: str, code: str, code_verifier: str) -> dict:
    return _post_form(
        TOKEN_URL,
        {
            "client_id": client_id,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": code_verifier,
        },
    )


def _verify_refresh_token(client_id: str, refresh_token: str) -> None:
    response = _post_form(
        TOKEN_URL,
        {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )

    if not response.get("access_token"):
        sys.exit("Refresh token verification failed: no access_token returned.")


def main() -> None:
    client_id = _get_required_setting("SPOTIFY_CLIENT_ID")

    code_verifier = _generate_code_verifier()
    code_challenge = _generate_code_challenge(code_verifier)
    state = secrets.token_urlsafe(24)
    authorize_url = _build_authorize_url(client_id, state, code_challenge)

    # bind the callback server before opening the browser to avoid a race
    server = _start_callback_server()

    print(f"Using SPOTIFY_CLIENT_ID {_mask(client_id)} from {ENV_PATH}")
    print("Opening Spotify authorization in your browser...")
    print(f"If it does not open, visit:\n{authorize_url}\n")

    webbrowser.open(authorize_url, new=1, autoraise=True)

    code = _capture_code(server, state)
    tokens = _exchange_code_for_tokens(client_id, code, code_verifier)

    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        sys.exit(
            "No refresh_token returned. Revoke the app in Spotify, then run again."
        )

    _verify_refresh_token(client_id, refresh_token)
    _upsert_env_value(ENV_PATH, "SPOTIFY_REFRESH_TOKEN", refresh_token)

    print("Success. Verified and wrote SPOTIFY_REFRESH_TOKEN to .env.")
    print(f"Stored token: {_mask(refresh_token)}")
    print("Copy the full value from .env into your deployment secret manager.")


if __name__ == "__main__":
    main()
