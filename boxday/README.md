# Boxday marketing site

Localized static marketing pages for Boxday:

- English: `https://woorlds.github.io/boxday/`
- Korean: `https://woorlds.github.io/boxday/ko/`
- Japanese: `https://woorlds.github.io/boxday/ja/`

## Assets

The app icon comes from `Boxday/Assets.xcassets/AppIcon.appiconset/app-icon-1024.png` in the Boxday repository. Each locale uses web-optimized derivatives of:

- `01_today.png`
- `02_editor.png`
- `04_notifications.png`
- `05_stats.png`

The notification image is cropped non-destructively in CSS to show the notification defaults without exposing DEBUG-only controls lower on the source screen.

## Local verification

From the developer-site repository root:

```sh
python3 boxday/verify.py
python3 -m http.server 8000
```

Then open `http://localhost:8000/boxday/`.
