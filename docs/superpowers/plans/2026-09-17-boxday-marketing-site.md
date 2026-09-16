# Boxday Marketing Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, verify, and publish an iPhone-first Boxday marketing site in English, Korean, and Japanese at `/boxday/`.

**Architecture:** Add three semantic static HTML documents backed by one shared responsive stylesheet and locale-specific web-optimized screenshots. A Python verifier enforces the cross-locale URL, metadata, asset, link, accessibility, and screenshot-crop contracts before browser review and deployment.

**Tech Stack:** Static HTML5, CSS, Python 3 standard library, Pillow for image conversion if available, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-09-17-boxday-marketing-site-design.md`

## Global Constraints

- English is served at `/boxday/`, Korean at `/boxday/ko/`, and Japanese at `/boxday/ja/`.
- The default experience is optimized for iPhone widths from 320 CSS pixels upward, with no horizontal overflow and at least 44-by-44-pixel interactive targets.
- Use only implemented Boxday capabilities and standard local notifications; never claim push notifications or Critical Alerts.
- Do not show an App Store badge, download action, release promise, analytics, forms, or unrelated-app links.
- Feature 3 uses the upper notification-settings area of `04_notifications.png`; DEBUG-only Developer, test-data, data-management, and iCloud rows must not be visible.
- Privacy and support link to the existing `https://woorlds.github.io/app-legal/boxday/` pages.
- Implementation review is local first. Push to `main` only after verification passes.

---

### Task 1: Static Site Contract Verifier

**Files:**
- Create: `boxday/verify.py`
- Test: `boxday/verify.py` run against the initially missing pages

**Interfaces:**
- Consumes: `boxday/index.html`, `boxday/ko/index.html`, `boxday/ja/index.html`, `boxday/style.css`, and referenced local assets.
- Produces: command-line exit code `0` with `Boxday site verification passed.` or one-or-more human-readable failures with exit code `1`.

- [ ] **Step 1: Write the verifier before the pages exist**

Create a Python standard-library script modeled on `stepcue/verify.py`. Define locale records for `en`, `ko`, and `ja`; parse each document with `html.parser.HTMLParser`; verify `lang`, canonical URL, all four alternate links (`en`, `ko`, `ja`, `x-default`), local stylesheet and image existence, unique heading IDs, non-empty localized image `alt`, the language navigation URLs, feature anchor, privacy URL, support URL, lazy loading on below-fold images, and `notification-crop` on the third feature image container. Reject the strings `DEVELOPER`, `Seed 200 Test Boxes`, and `Delete Test Data` in HTML.

- [ ] **Step 2: Run the verifier and confirm it fails for missing pages**

Run: `python3 boxday/verify.py`

Expected: exit code `1` with missing-file failures for the three localized documents and shared stylesheet.

- [ ] **Step 3: Commit the failing contract**

```bash
git add boxday/verify.py
git commit -m "test: define Boxday site contract"
```

---

### Task 2: Localized Assets and Semantic Pages

**Files:**
- Create: `boxday/index.html`
- Create: `boxday/ko/index.html`
- Create: `boxday/ja/index.html`
- Create: `boxday/assets/icon.png`
- Create: `boxday/assets/en/today.webp`
- Create: `boxday/assets/en/editor.webp`
- Create: `boxday/assets/en/notifications.webp`
- Create: `boxday/assets/en/stats.webp`
- Create: `boxday/assets/ko/today.webp`
- Create: `boxday/assets/ko/editor.webp`
- Create: `boxday/assets/ko/notifications.webp`
- Create: `boxday/assets/ko/stats.webp`
- Create: `boxday/assets/ja/today.webp`
- Create: `boxday/assets/ja/editor.webp`
- Create: `boxday/assets/ja/notifications.webp`
- Create: `boxday/assets/ja/stats.webp`
- Create: `boxday/README.md`

**Interfaces:**
- Consumes: Boxday icon and locale captures in `/Users/woorlds/Development/swift/Boxday/Boxday/Boxday/Assets.xcassets/AppIcon.appiconset/` and `/Users/woorlds/Development/swift/Boxday/Boxday/appstore-previews/<locale>/simulator/`.
- Produces: the complete semantic content tree and stable CSS class contract consumed by `boxday/style.css`: `site-header`, `hero`, `features`, `flow`, `shot-wrap`, `notification-crop`, `trust`, and `site-footer`.

- [ ] **Step 1: Create web derivatives of the approved captures**

Copy the 1024-pixel app icon and convert each locale's `01_today.png`, `02_editor.png`, `04_notifications.png`, and `05_stats.png` to WebP without changing the source files. Use quality `88`, preserve the 1320-by-2868 dimensions, and name them according to the file list above.

- [ ] **Step 2: Create the English document**

Implement `/boxday/index.html` with `lang="en"`, complete canonical/alternate metadata, the headline `Plan in one line. Start on time.`, the four headings `See today clearly`, `Plan in one line`, `Let reminders do the rest`, and `See your focus`, localized image alternatives, `Explore features` anchor, and `Support` link. Wrap the third feature image in `<div class="shot-wrap notification-crop">`.

- [ ] **Step 3: Create the Korean document**

Implement `/boxday/ko/index.html` with `lang="ko"`, corrected relative asset paths, the approved Korean hero and feature copy from the spec, localized alternatives, and the same semantic section order. Mark `한국어` with `aria-current="page"`.

- [ ] **Step 4: Create the Japanese document**

Implement `/boxday/ja/index.html` with `lang="ja"`, corrected relative asset paths, the headline `一行で予定して、時間どおりに始める。`, concise natural Japanese body copy, localized alternatives, and the same semantic section order. Mark `日本語` with `aria-current="page"`.

- [ ] **Step 5: Document sources and local verification**

Create `boxday/README.md` listing the three URLs, source screenshot directories, selected source filenames, notification CSS-crop rationale, `python3 boxday/verify.py`, and a local server command `python3 -m http.server 8000` from the repository root.

- [ ] **Step 6: Run the verifier and confirm only stylesheet-dependent checks remain**

Run: `python3 boxday/verify.py`

Expected: documents and assets pass; stylesheet is the only missing implementation artifact.

- [ ] **Step 7: Commit localized content and assets**

```bash
git add boxday/index.html boxday/ko/index.html boxday/ja/index.html boxday/assets boxday/README.md
git commit -m "feat: add Boxday marketing content"
```

---

### Task 3: iPhone-First Responsive Visual System

**Files:**
- Create: `boxday/style.css`
- Test: `boxday/verify.py`

**Interfaces:**
- Consumes: the semantic CSS class contract from Task 2.
- Produces: warm-editorial light/dark presentation, 320-pixel-safe mobile layout, 760-pixel desktop expansion, and the non-destructive notification crop.

- [ ] **Step 1: Implement design tokens and base accessibility**

Define the approved light colors as CSS custom properties, dark-mode overrides under `@media (prefers-color-scheme: dark)`, `box-sizing`, Apple system font stack, visible `:focus-visible`, a keyboard skip link, and readable default line height. Set `.wrap` to `width: min(calc(100% - 36px), 1060px)` and all navigation links to a minimum 44-pixel size.

- [ ] **Step 2: Implement the mobile hierarchy**

Build the compact header, single-column hero, large localized headline, pill action, centered screenshot with soft orange backdrop, sequential feature cards, trust cards, and wrapping footer. Use fluid type with `clamp()` and ensure long Japanese copy wraps without fixed widths.

- [ ] **Step 3: Implement notification cropping and image behavior**

Use an overflow-hidden `.notification-crop` container with a stable aspect ratio and `.notification-crop img { height: 100%; object-fit: cover; object-position: top; }`. The crop must retain the notification-default rows while excluding the DEBUG Developer section at all tested widths. Provide explicit HTML image dimensions and native lazy loading below the hero.

- [ ] **Step 4: Implement wide-screen expansion and motion preferences**

At `min-width: 760px`, change the hero to two columns and alternate feature copy/images while preserving DOM order. Under `prefers-reduced-motion: reduce`, disable smooth scrolling and transitions.

- [ ] **Step 5: Run the complete verifier**

Run: `python3 boxday/verify.py`

Expected: `Boxday site verification passed.`

- [ ] **Step 6: Commit the visual system**

```bash
git add boxday/style.css
git commit -m "feat: style Boxday marketing site"
```

---

### Task 4: Homepage Link and Browser Verification

**Files:**
- Modify: `index.html`
- Test: `boxday/verify.py`

**Interfaces:**
- Consumes: the completed `/boxday/` site.
- Produces: discoverability from the developer homepage and browser evidence at required viewports.

- [ ] **Step 1: Link Boxday from the root homepage**

Change the existing plain `<strong>Boxday</strong>` label to `<strong><a href="/boxday/">Boxday</a></strong>` without changing its privacy or support links.

- [ ] **Step 2: Extend the verifier for the root link**

Add a check that root `index.html` contains an anchor with `href="/boxday/"` and visible text `Boxday`.

- [ ] **Step 3: Run static verification**

Run: `python3 boxday/verify.py`

Expected: `Boxday site verification passed.`

- [ ] **Step 4: Serve and inspect all locales**

Start `python3 -m http.server 8000` at the repository root. Inspect `/boxday/`, `/boxday/ko/`, and `/boxday/ja/` at 320, 375, 390, and 430 CSS pixels plus one desktop viewport. Verify language links, feature anchor, privacy/support links, no horizontal overflow, dark mode, visible keyboard focus, and that the third screenshot never exposes the Developer section.

- [ ] **Step 5: Commit homepage integration**

```bash
git add index.html boxday/verify.py
git commit -m "feat: link Boxday marketing site"
```

---

### Task 5: Deployment and Public Verification

**Files:**
- No new source files

**Interfaces:**
- Consumes: verified local `main` commits.
- Produces: public English, Korean, and Japanese Boxday pages on GitHub Pages.

- [ ] **Step 1: Confirm the worktree is clean except ignored design-session artifacts**

Run: `git status --short`

Expected: no tracked modifications and no uncommitted Boxday implementation files.

- [ ] **Step 2: Push `main`**

Run: `git push origin main`

Expected: the remote `main` branch advances to the local implementation commit.

- [ ] **Step 3: Verify public URLs**

After GitHub Pages finishes, verify HTTP 200 and expected localized titles for:

```text
https://woorlds.github.io/boxday/
https://woorlds.github.io/boxday/ko/
https://woorlds.github.io/boxday/ja/
https://woorlds.github.io/app-legal/boxday/privacy/
https://woorlds.github.io/app-legal/boxday/support/
```

- [ ] **Step 4: Perform final public mobile smoke test**

Open the Korean public page at an iPhone-sized viewport, follow each language link, confirm assets load, and verify the third feature crop hides all DEBUG-only content.
