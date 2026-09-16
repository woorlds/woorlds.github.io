# Boxday Marketing Site Design

**Date:** 2026-09-17  
**Status:** Design approved; written-spec review pending  
**Target:** `https://woorlds.github.io/boxday/`

## Objective

Create an app-specific marketing page for Boxday that explains its zero-friction timeboxing flow to iPhone visitors and supplies the App Store Connect Marketing URL. The page must use the shipping app's real localized screens and describe only implemented behavior.

The site does not show an App Store badge, download action, or release promise until a public App Store URL exists. Its primary actions are an in-page feature link and the existing Boxday support page.

## Repository and Deployment Boundary

Marketing-site source belongs in the `woorlds/woorlds.github.io` repository under `boxday/`. GitHub Pages publishes that repository's `main` branch from `/`, so `boxday/index.html` maps to `https://woorlds.github.io/boxday/`.

Privacy and support remain in the separate `woorlds/app-legal` repository. This work links to those pages but does not move or rewrite them. Implementation and local review happen before any deployment; pushing to `main` requires a separate final approval.

## Audience and Language URLs

Most visitors are expected to use an iPhone. The design is mobile-first, with desktop treated as an expanded presentation of the same vertical reading flow.

English is the default language:

- English: `/boxday/`
- Korean: `/boxday/ko/`
- Japanese: `/boxday/ja/`

Each language uses a real static URL and matching `lang`, localized title and description, canonical URL, `hreflang` metadata, visible copy, image alternative text, and localized Boxday screenshots. The header contains `EN`, `한국어`, and `日本語` links. Language navigation and core content require no JavaScript.

## Page Structure

Each localized page uses this order:

1. Compact header with the Boxday icon and name, language navigation, and localized support label.
2. Hero with the localized promise, short explanation, feature anchor, support link, and localized Today screenshot.
3. Four-part feature flow:
   - Today timeline.
   - One-line time-box creation.
   - Default local-notification controls.
   - Weekly focus statistics.
4. Trust section explaining on-device storage, standard local notifications, and optional personal iCloud Drive backup.
5. Footer containing localized `Boxday by woorlds · iPhone only` copy plus Boxday privacy and support links.

The page excludes links to unrelated apps and excludes pricing or Premium comparison content.

## Approved Korean Copy Direction

The Korean hero leads with:

- Kicker: `간편한 타임박싱`
- Headline: `한 줄 적고, 제때 시작하세요.`
- Explanation: `할 일을 적고 시작 시간을 고르세요. 복잡한 계획 없이, Boxday가 시작할 순간을 알려드립니다.`
- Actions: `기능 살펴보기` and `지원`

The feature section leads with `준비는 짧게. 시작은 제시간에.` and the four headings `오늘을 한눈에`, `한 줄이면 계획 끝`, `시작할 순간을 알림으로`, and `집중한 시간을 한눈에`.

English and Japanese preserve the meaning and hierarchy rather than translating word-for-word. Copy must remain concise enough for narrow iPhone layouts.

## Visual System

The approved direction is “Warm editorial”: a cream background, warm orange action color, dark warm-gray text, rounded cards, restrained shadows, and generous vertical spacing. It follows StepCue's proven marketing-page structure without copying StepCue's green identity.

Initial implementation tokens:

| Role | Value |
| --- | --- |
| Background | `#F9F2E8` |
| Card | `#FFFAF4` |
| Surface | `#F1E5D8` |
| Action | `#EF6848` |
| Strong action | `#C94D34` |
| Primary text | `#302B27` |
| Secondary text | `#756C63` |
| Border | `#DFD1C3` |

Use Apple system fonts only. The app icon supplies the compact brand mark. Decorative motion is unnecessary; reduced-motion users must not receive smooth scrolling or nonessential transitions. Dark mode may derive a warm charcoal palette while retaining the orange brand accent and WCAG-readable contrast.

## Responsive and iPhone Behavior

The default layout is a single vertical flow designed from 320 CSS pixels upward. It must not scroll horizontally at 320 pixels. Controls and links provide at least 44 by 44 CSS-pixel targets, the language navigation remains usable without clipping, and text remains readable without zoom.

On iPhone, the hero order is copy, actions, then Today screenshot. Each feature shows copy immediately before its screenshot so the relationship survives a long vertical scroll. The header may use a translucent background while scrolling, but must not consume excessive vertical space or obscure content near the safe area.

At wider breakpoints, the hero becomes two columns and feature copy/images alternate left and right. Desktop introduces no additional sections or different navigation.

## Image Sources and Presentation

Use the existing localized simulator captures from the Boxday repository:

- `appstore-previews/en/simulator/`
- `appstore-previews/ko/simulator/`
- `appstore-previews/ja/simulator/`

For each locale:

- Hero and feature 1: `01_today.png`
- Feature 2: `02_editor.png`
- Feature 3: `04_notifications.png`, cropped non-destructively in CSS to its upper notification-settings area
- Feature 4: `05_stats.png`

Do not use `03_recurrence.png` for feature 3 because its upper content is nearly identical to `02_editor.png` and appears duplicated in the marketing flow. Do not expose the DEBUG-only Developer section present near the bottom of `04_notifications.png`. The website crop must show only the notification-default controls and must exclude Developer, test-data, data-management, and iCloud sections.

Copy selected assets into `boxday/assets/<locale>/`; do not reference the Boxday application repository at runtime. Preserve source PNGs and create web-optimized derivatives without overwriting them. The hero image loads eagerly with explicit dimensions; below-the-fold images use native lazy loading. Every image has meaningful localized alternative text.

## Content Contract

The page may describe one-line time-box entry, start time and duration selection, the Today timeline, recurrence, standard local start/5-minute/end notifications, completion and focus statistics, on-device storage, and optional iCloud Drive backup.

The page must not claim push notifications, Critical Alerts, cross-device live sync, team collaboration, Android/iPad/Mac availability, an App Store release date, or an unimplemented automation feature. Backup copy must make clear that it is optional and stored in the user's personal iCloud Drive rather than on a Boxday-operated server.

## Links and Failure Behavior

The feature action is an in-page anchor and works without JavaScript. Privacy and support point to:

- `https://woorlds.github.io/app-legal/boxday/privacy/`
- `https://woorlds.github.io/app-legal/boxday/support/`

There are no forms, cookies, analytics, accounts, or collection of visitor data. If an image fails, semantic copy and localized alternative text still explain the feature. If CSS fails, the source order remains readable and all links remain usable.

## Files

Implementation adds:

- `boxday/index.html`
- `boxday/ko/index.html`
- `boxday/ja/index.html`
- `boxday/style.css`
- `boxday/assets/icon.png`
- `boxday/assets/en/*`
- `boxday/assets/ko/*`
- `boxday/assets/ja/*`
- `boxday/README.md`
- A small static verification script if needed to check links, metadata, and assets consistently across locales

Implementation also updates the root developer homepage so the existing Boxday label links to `/boxday/` while its privacy and support links remain unchanged.

## Verification

Before requesting deployment approval:

- Validate all three documents as semantic HTML and confirm every local asset exists.
- Verify canonical and alternate-language metadata for English, Korean, Japanese, and `x-default`.
- Confirm visible copy, screenshots, and alternative text match each locale.
- Verify the notification screenshot crop at 320, 375, 390, and 430 CSS-pixel widths and confirm no DEBUG-only Developer content is visible.
- Check all mobile widths for horizontal overflow, readable hierarchy, and 44-pixel targets.
- Check one desktop width as a responsive expansion sanity test.
- Check light mode, dark mode, reduced motion, keyboard focus, and useful alternative text.
- Confirm no App Store badge, release promise, unrelated-app link, or unsupported product claim appears.
- Serve the site locally and inspect all three language pages in a browser.
- Confirm the root homepage's Boxday link resolves to the local marketing page.
- Do not deploy during implementation review. After explicit deployment approval, push and verify the three public Boxday URLs plus privacy and support return HTTP 200.

## Approved Reference

The approved visual reference is the Korean mobile-first v3 mockup produced during the 2026-09-17 design session. It uses the Warm editorial direction, actual Boxday captures, the CSS-cropped notification settings screenshot, and a footer limited to privacy and support.
