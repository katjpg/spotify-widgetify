# Spotify Widgetify

Display your currently playing Spotify track with a customizable widget for GitHub README profiles and websites.

## Table of Contents
1. [Introduction](#1-introduction)
2. [Features](#2-features)
3. [Quick Start](#3-quick-start)
4. [Prerequisites](#4-prerequisites)
5. [Setup Guide](#5-setup-guide)
6. [GitHub README Integration](#6-github-readme-integration)
7. [Theme Showcase](#7-theme-showcase)
8. [Customization Options](#8-customization-options)
9. [Troubleshooting](#9-troubleshooting)
10. [License](#10-license)
11. [Credits](#11-credits)

## 1. Introduction

Spotify Widgetify is a web widget that displays your currently playing Spotify track, designed to be embedded in GitHub profile READMEs and websites. It automatically updates to reflect your currently playing or recently played tracks on Spotify.

![Spotify Widgetify Demo](https://spotify-widgetify.vercel.app/github?theme=default&style=dark)

## 2. Features

- Real-time display of your current or recently played Spotify tracks
- Multiple theme options: Default, Vinyl, iPod, Retro, Windows XP
- Light and dark mode support for most themes
- Customizable colors for select themes
- Responsive design that works in GitHub READMEs and websites
- Automatic updates when your music changes

## 3. Quick Start

1. Set up your Spotify application credentials
2. Deploy the application or use the hosted version
3. Add the widget to your GitHub README using the embed code
4. Customize the appearance with theme, style, and color parameters

## 4. Prerequisites

- Spotify account
- Spotify Developer application with API credentials
- GitHub account (for README embedding)
- Vercel account (optional, for deployment)

## 5. Setup Guide

### 5.1. Create a Spotify Developer Application

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Log in with your Spotify account
3. Click "Create App"
4. Fill in the required information:
   - App name: "Spotify Widgetify" (or your preferred name)
   - App description: Brief description of your widget
   - Redirect URI: The URL where your application will be hosted (e.g., `https://your-app-name.vercel.app/callback`)
5. Save your `Client ID` and `Client Secret` for the next steps

### 5.2. Set Up Environment Variables

Create a `.env` file with the following variables:
```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REFRESH_TOKEN=your_spotify_refresh_token
```

To obtain a `REFRESH_TOKEN`:
1. Create an authorization URL with your client ID:
```
https://accounts.spotify.com/authorize?client_id=YOUR_CLIENT_ID&response_type=code&scope=user-read-currently-playing,user-read-recently-played&redirect_uri=YOUR_REDIRECT_URI
```
2. Visit the URL and authorize the application
3. You'll be redirected to your redirect URI with a code parameter
4. Exchange this code for a refresh token using the Spotify API's token endpoint

### 5.3. Deploy the Application

#### Option A: Deploy to Vercel

1. Fork this repository
2. Connect your fork to Vercel
3. Configure the environment variables in the Vercel dashboard
4. Deploy the application

#### Option B: Run Locally

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `uvicorn app.main:app --reload`

## 6. GitHub README Integration

Add the widget to your GitHub profile README using the following Markdown:

```markdown
<div align="center">
  <a href="https://your-app-url.vercel.app/link">
    <img src="https://your-app-url.vercel.app/github?theme=default&style=dark" alt="Spotify Now Playing" width="400" />
  </a>
</div>
```

Replace `your-app-url.vercel.app` with your actual deployed application URL.

## 7. Theme Showcase

Below are all available themes with their corresponding embed codes:

| Theme | Preview |
|-------|---------|
| **Default (Light)** | <div align="center"><a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=default&style=light" alt="Default Light Theme" width="400" /></a></div> |
| **Default (Dark)** | <div align="center"><a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=default&style=dark" alt="Default Dark Theme" width="400" /></a></div> |
| **Vinyl** | <div align="center"><a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=vinyl&style=dark" alt="Vinyl Theme" width="400" /></a></div> |
| **iPod** | <div align="center"><a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=ipod&style=light" alt="iPod Theme" width="400" /></a></div> |
| **Retro** | <div align="center"><a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=retro&style=dark" alt="Retro Theme" width="400" /></a></div> |
| **Windows XP** | <div align="center"><a href="https://spotify-widgetify.vercel.app/link"><img src="https://spotify-widgetify.vercel.app/github?theme=windowsxp" alt="Windows XP Theme" width="400" /></a></div> |

### TODO: Future Themes
The following themes are planned for future implementation:
- Windows 98
- Frutiger Aero
- Macintosh

## 8. Customization Options

The widget can be customized using URL parameters:

### 8.1. Common Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `theme` | Widget theme | `default` | `default`, `vinyl`, `ipod`, `retro`, `windowsxp` |
| `style` | Color scheme | `light` | `light`, `dark` (Note: not all themes support both styles) |
| `color` | Custom color | Theme default | Any hex color code without # (e.g., `1DB954`) |
| `eq_color` | Equalizer color | `1ED760` | Any hex color code without # or `rainbow` or `none` |
| `spin` | Enable spinning for album art | `false` | `true`, `false` (Only works with compatible themes) |

### 8.2. Theme-Specific Notes

- **Default**: Supports light/dark modes and custom colors
- **Vinyl**: Spinning record player with album art as the vinyl
- **iPod**: Classic iPod-inspired design with click wheel
- **Retro**: Pixelated retro music player with scan lines
- **Windows XP**: Windows Media Player 11 inspired look

### 8.3. Example with Custom Parameters

```markdown
<div align="center">
  <a href="https://your-app-url.vercel.app/link">
    <img src="https://your-app-url.vercel.app/github?theme=ipod&style=light&color=609dbd" alt="Spotify Now Playing" width="400" />
  </a>
</div>
```

## 9. Troubleshooting

### 9.1. Widget Shows "Not Playing"

- Ensure you're actively playing music on Spotify
- Check that your Spotify API credentials are correct
- Verify that your refresh token is valid and has the correct scopes

### 9.2. Widget Not Updating

- The widget may cache for a short period
- Refresh your GitHub profile page
- Add a query parameter to force a refresh: `?cache_bust=123`

### 9.3. Authentication Issues

- Double-check your CLIENT_ID, CLIENT_SECRET, and REFRESH_TOKEN
- Ensure your Spotify Developer App has the correct redirect URI
- Verify that you've granted the necessary permissions during authorization

## 10. License

[MIT License](LICENSE)

## 11. Credits

- Spotify API for providing track data
- FastAPI for the web framework
- Vercel for hosting capabilities
