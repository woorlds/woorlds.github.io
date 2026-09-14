# StepCue Marketing Site Design

**Date:** 2026-09-14  
**Status:** Approved for implementation  
**Target:** `https://woorlds.github.io/stepcue/`

## Objective

Create an app-specific marketing page for StepCue that explains its core value to iPhone visitors and supplies the App Store Connect Marketing URL. The page must reflect the shipping iPhone app rather than describe unimplemented features.

The site does not show an App Store badge, download action, or “Coming soon” message until a public App Store URL exists.

## Audience and Language URLs

The majority of visitors are expected to view the page on an iPhone. The design is mobile-first, with desktop presentation treated as an expanded version of the same reading flow.

English is the default language:

- English: `/stepcue/`
- Korean: `/stepcue/ko/`
- Japanese: `/stepcue/ja/`

Each language has a real static URL and matching `lang`, title, description, canonical URL, alternate-language metadata, visible copy, alternative text, and localized StepCue simulator screenshots. The header provides `EN`, `한국어`, and `日本語` links that navigate between these pages. The production pages do not depend on JavaScript for language access or core content.

## Page Structure

Each localized page uses this order:

1. Compact header with the StepCue icon and name, language navigation, and localized support link label.
2. Hero with the product promise, short explanation, “Explore features” anchor, support link, and the localized timer screenshot.
3. Feature flow showing routine selection, routine editing, and rhythm/history with localized screenshots.
4. Trust section describing local-first storage, reliable return after interruption, and accessibility support.
5. Footer containing `StepCue by woorlds · iPhone only` in the page language plus only the StepCue privacy and support links.

The page excludes links to other apps.

## Visual System

The site reuses the app’s CalmSystem palette:

| Role | Light | Dark |
| --- | --- | --- |
| Background | `#F5F2E9` | `#111612` |
| Card | `#FFFDF8` | `#1B211D` |
| Surface | `#EFEAE0` | `#202820` |
| Action | `#367865` | `#72B49E` |
| Strong action | `#285F50` | `#9BD6C3` |
| Soft action | `#DCECE5` | `#23352F` |
| Primary text | `#1C2823` | `#F2F6F3` |
| Secondary text | `#6D756F` | `#C7D1CB` |
| Border | `#D9D2C5` | `#344139` |

The app icon’s navy background and colored bars remain a compact brand mark. They do not replace the app’s cream-and-green page theme. The site uses Apple system fonts, restrained shadows, rounded screenshot containers, and no decorative animation. `prefers-color-scheme` controls dark mode and `prefers-reduced-motion` disables smooth scrolling.

## Responsive Behavior

The default layout is a single vertical flow designed from 320-point-wide iPhone viewports upward. It must not create horizontal scrolling at 320 CSS pixels. Interactive targets are at least 44 by 44 CSS pixels, text remains readable without zoom, and the language controls wrap or compress safely on narrow screens.

The hero uses a single-column order on iPhone: copy, actions, then timer screenshot. At wider breakpoints it becomes a balanced two-column layout. Feature sections remain sequential on iPhone and may alternate copy and images on wider screens. Desktop does not introduce different information architecture.

## Image Sources and Delivery

Use actual localized simulator captures from the StepCue repository:

- `appstore-previews/en/simulator/`
- `appstore-previews/ko/simulator/`
- `appstore-previews/ja/simulator/`

The hero uses each locale’s current `03_timer.png`. The feature flow uses `02_morning_pinned.png`, `04_editor.png`, and `06_rhythm.png`. Copy the selected assets into `stepcue/assets/<locale>/` in the website repository; do not reference files across repositories at runtime.

Preserve the original StepCue screenshots. Produce web-optimized derivatives for the site without overwriting source PNGs. The hero image loads eagerly with explicit dimensions; below-the-fold images use native lazy loading. Image alternative text describes the purpose of each visible app screen in the page language.

## Content Contract

Marketing copy communicates only the implemented shared flow: create or select a routine, follow named timed steps, see current and nearby steps and expected finish time, return after interruption, and review rhythm/history. Trust copy may mention on-device routine storage, ordinary local notifications, and supported accessibility modes.

Copy must not claim account sync, app-operated cloud backup, Live Activities, subscriptions, in-app purchase, an App Store release date, or availability for iPad, Mac, or Android. StepCue remains an iPhone-only app. The footer and metadata spell `woorlds` entirely in lowercase.

## Links and Failure Behavior

The feature action is an in-page anchor and remains useful without JavaScript. Privacy and support links point to:

- `https://woorlds.github.io/app-legal/stepcue/privacy/`
- `https://woorlds.github.io/app-legal/stepcue/support/`

There are no forms, accounts, cookies, analytics, or application data requests. If an image fails to load, localized copy and alternative text still communicate the feature. If CSS fails, the semantic document order remains readable and all links remain usable.

## Files

Implementation adds:

- `stepcue/index.html`
- `stepcue/ko/index.html`
- `stepcue/ja/index.html`
- `stepcue/style.css`
- `stepcue/assets/icon.png`
- `stepcue/assets/en/*`
- `stepcue/assets/ko/*`
- `stepcue/assets/ja/*`
- `stepcue/README.md`

The implementation does not change the root developer homepage. The approved StepCue page contains no “other apps” link.

## Verification

Before publication:

- Validate all three documents as semantic HTML and confirm there are no missing local assets.
- Confirm every internal and external link resolves to its intended URL.
- Verify English, Korean, and Japanese content and screenshots match on each localized URL.
- Check 320, 375, 390, and 430 CSS-pixel mobile widths for overflow, readable hierarchy, and 44-pixel targets.
- Check one desktop width only as a responsive expansion sanity test.
- Check light mode, dark mode, reduced motion, keyboard focus, and useful alternative text.
- Confirm no pre-release availability message, App Store badge, other-app link, or non-lowercase `woorlds` brand spelling remains.
- Serve the site locally and inspect it in a browser before committing implementation.
- After an explicitly authorized push, verify the three public StepCue URLs and the existing privacy and support URLs return HTTP 200.

## Approved Reference

The approved visual reference is the mobile-first StepCue mockup produced during the 2026-09-14 design session. It uses the current localized `03_timer.png` images, working language switching for review, the CalmSystem light/dark palette, actual simulator captures, and a footer limited to privacy and support.
