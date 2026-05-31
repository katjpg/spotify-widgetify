# Spotify Widgetify

Displays your currently playing Spotify track as an embeddable and customizable SVG widget for GitHub READMEs and
websites.

<div align="center">
  <a href="https://spotify-widgetify.vercel.app/link">
    <img src="https://spotify-widgetify.vercel.app/github?theme=default&style=dark" alt="Spotify Now Playing" width="440" />
  </a>
</div>

## Table of Contents

- [Spotify Widgetify](#spotify-widgetify)
  - [Table of Contents](#table-of-contents)
  - [1. How it works](#1-how-it-works)
  - [2. Features](#2-features)
  - [3. Themes](#3-themes)
  - [4. Embedding in a README](#4-embedding-in-a-readme)
  - [5. Customization](#5-customization)
  - [6. Self-hosting](#6-self-hosting)
    - [Prerequisites](#prerequisites)
    - [6.1. Create a Spotify application](#61-create-a-spotify-application)
    - [6.2. Configure credentials](#62-configure-credentials)
    - [6.3. Get a refresh token](#63-get-a-refresh-token)
    - [6.4. Run locally](#64-run-locally)
    - [6.5. Deploy to Vercel](#65-deploy-to-vercel)
  - [7. Architecture](#7-architecture)
  - [8. Troubleshooting](#8-troubleshooting)
    - [**Shows "Not Playing".**](#shows-not-playing)
    - [**Stuck on an old track.**](#stuck-on-an-old-track)
    - [**Token script cannot capture the redirect.**](#token-script-cannot-capture-the-redirect)
  - [9. License](#9-license)
  - [10. Credits](#10-credits)

## 1. How it works

Spotify Widgetify is a web widget that displays your currently playing Spotify track, designed to be embedded in GitHub profile READMEs and websites. It automatically updates to reflect your currently playing or recently played tracks on Spotify. 

1. Refresh a Spotify access token, cached until it expires.
2. Fetch the currently playing track, falling back to the most recently played, then to a
   "Not Playing" state.
3. Map the Spotify response to a `Track` model and derive a color palette from the album art.
4. Apply the requested theme and render a Jinja2 SVG template.

The rendered SVG inlines its assets as base64 and carries its CSS in a `<style>` block. It runs no
JavaScript and makes no external requests, so it renders the same in a README or offline.

GitHub serves widget images through a caching proxy, so a profile can show the previous track for a
minute or two after playback changes.

## 2. Features

- Eight themes inspired by defining GUI eras, including iPod (skeuomorphic design), Windows 98 (Windows Classic), Macintosh (Platinum), and more.
- Current track, or the most recently played when nothing is on.
- `light` and `dark` styles on the themes that support both.
- Custom accent color via `?color=`.

## 3. Themes

| Theme | `theme=` | `style` | `color` | Preview |
|-------|----------|---------|---------|---------|
| **Default** | `default` | light / dark | yes | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=default&style=dark" alt="Default theme" width="360" /></a> |
| **Vinyl** | `vinyl` | light / dark | yes | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=vinyl&style=dark" alt="Vinyl theme" width="360" /></a> |
| **iPod** | `ipod` | light / dark | yes | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=ipod" alt="iPod theme" width="360" /></a> |
| **Retro** | `retro` | light / dark | — | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=retro&style=dark" alt="Retro theme" width="360" /></a> |
| **Windows 98** | `windows98` | fixed (light) | — | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=windows98" alt="Windows 98 theme" width="360" /></a> |
| **Windows XP** | `windowsxp` | fixed | — | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=windowsxp" alt="Windows XP theme" width="360" /></a> |
| **Frutiger Aero** | `frutiger_aero` | fixed | — | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=frutiger_aero" alt="Frutiger Aero theme" width="360" /></a> |
| **Macintosh** | `macintosh` | fixed | — | <a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=macintosh" alt="Macintosh theme" width="360" /></a> |

> Previews show the track currently playing on the hosted demo account.

## 4. Embedding in a README

Embed the widget using `/github` as the `<img>` source and linking it via `/link`, which opens an embedded Spotify player for the track you're currently playing.

```markdown
<div align="center">
  <a href="https://spotify-widgetify.vercel.app/link">
    <img src="https://spotify-widgetify.vercel.app/github?theme=ipod" alt="Spotify Now Playing" width="440" />
  </a>
</div>
```

NOTE: Replace `spotify-widgetify.vercel.app` with a self-hosted deployment if needed.

| Endpoint | Returns |
|----------|---------|
| `/github` | The widget as `image/svg+xml`, for use in an `<img>`. |
| `/` | The widget as an HTML page, for previewing in a browser. |
| `/link` | An HTML page embedding the current track's Spotify player. |

## 5. Customization

Options are query parameters on `/github` and `/`:

| Parameter | Default | Values | Notes |
|-----------|---------|--------|-------|
| `theme` | `default` | any `theme=` value in [§3](#3-themes) | Unknown values fall back to `default`. |
| `style` | `light` | `light`, `dark` | Effective on `default`, `vinyl`, `ipod`, `retro`. Other themes render one fixed look. |
| `color` | — | hex digits, no `#` (e.g. `609dbd`) | Custom accent for `default`, `vinyl`, `ipod`. Ignored by other themes. |
| `eq_color` | `1ED760` | hex digits, `rainbow`, `none` | Equalizer color on themes that show one. |

Example with a custom iPod body color and no equalizer:

```markdown
<img src="https://spotify-widgetify.vercel.app/github?theme=ipod&color=609dbd&eq_color=none" alt="Spotify Now Playing" width="440" />
```

## 6. Self-hosting

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- A Spotify account and a Spotify Developer application

### 6.1. Create a Spotify application

1. Open the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and create an app.
2. Record the **Client ID** and **Client Secret**.
3. Add `http://127.0.0.1:8888/callback` to the app's Redirect URIs. The token script in step 6.3
   uses it.

### 6.2. Configure credentials

Create a `.env` file in the project root:

```bash
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REFRESH_TOKEN=        # filled in by step 6.3
```

### 6.3. Get a refresh token

Run the helper script to complete the Authorization Code + PKCE flow and save `SPOTIFY_REFRESH_TOKEN` to `.env`. Make sure `SPOTIFY_CLIENT_ID` is set and the redirect URI from step 6.1 is registered.

```bash
uv run python scripts/get_refresh_token.py
```

The script opens Spotify’s consent page, captures the redirect at `127.0.0.1:8888`, exchanges the authorization code, and saves the refresh token.



### 6.4. Run locally

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000/?theme=ipod> for the preview, or
<http://127.0.0.1:8000/github?theme=ipod> for the raw SVG.

### 6.5. Deploy to Vercel

The repository includes `vercel.json`. Import the project in Vercel, set `SPOTIFY_CLIENT_ID`,
`SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REFRESH_TOKEN` in the project environment, and deploy. The
widget is then served at `https://<app>.vercel.app/github`.

## 7. Architecture

Server-rendered SVG. No build step.

```bash

app/
├── api/          # web requests
├── schemas/      # URL query parameters
├── domain/       # track + theme models
├── services/     # builds widget UI via colors + rendering
├── providers/    # Spotify client
├── themes/       # theme styling
├── templates/    # SVG layouts
├── assets/       # logos/images encoded into the SVG
└── static/       # source SVG files

```

## 8. Troubleshooting

### **Shows "Not Playing".** 
- Confirm music is playing and that `SPOTIFY_CLIENT_ID`,
`SPOTIFY_CLIENT_SECRET`, and `SPOTIFY_REFRESH_TOKEN` are set. An invalid or unscoped refresh token yields an empty access token and the fallback state. 
- The token needs the `user-read-currently-playing` and `user-read-recently-played` scopes (which the script requests).

### **Stuck on an old track.** 
- GitHub caches the image through its proxy. Append a parameter
such as `&cb=1` to fix the cache.

### **Token script cannot capture the redirect.** 
- Confirm `http://127.0.0.1:8888/callback` is registered
exactly in the app's Redirect URIs and that port 8888 is free.

## 9. License

[MIT](LICENSE)

## 10. Credits

- [Spotify Web API](https://developer.spotify.com/documentation/web-api) for track data
- [FastAPI](https://fastapi.tiangolo.com/) and [Jinja2](https://jinja.palletsprojects.com/)
- [Pillow](https://python-pillow.org/) for album-art color extraction
- [Vercel](https://vercel.com/) for hosting