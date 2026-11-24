# Boxday 2.1 marketing site

Localized freelancer-focused previews, deployed by GitHub Pages from `main` at the repository root:

- English: https://woorlds.github.io/boxday/
- Korean: https://woorlds.github.io/boxday/ko/
- Japanese: https://woorlds.github.io/boxday/ja/

The page labels 2.1 as an upcoming preview until the app release. It describes today-only allocation, undated backlog, impact preview, completed/remaining work, and planned project allocations. It does not promise measured work hours or recurrence.

## Assets

Localized WebP derivatives of the approved Boxday repository `appstore-previews/{en,ko,ja}/freelancer/captures/{01_today,02_editor,03_impact,04_backlog,05_stats}.png`. Source captures are 1320 × 2868; WebP dimensions are preserved. The previous v1 assets remain in git history and are no longer referenced by the pages.

## Verification

```sh
python3 boxday/verify.py
python3 -m http.server 8874 --bind 127.0.0.1 --directory boxday
```

Check each language, mobile and desktop layout, light/dark colors, and live URLs after the Pages deployment succeeds. Privacy/support and all other app sites retain their existing destinations.
