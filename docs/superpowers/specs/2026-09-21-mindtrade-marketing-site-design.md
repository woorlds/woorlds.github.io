# MindTrade Marketing Site Design

## Purpose

Create a polished, mobile-first marketing site for MindTrade at
`https://woorlds.github.io/mindtrade/`. The page will be suitable for the App
Store Connect Marketing URL field and will explain the product clearly to
prospective users without making investment-performance claims.

The default page is English. A complete Korean version is available at
`https://woorlds.github.io/mindtrade/ko/`.

## Audience and Message

MindTrade is for traders who want to understand how emotion and cognitive bias
affect their decisions. The site presents MindTrade as a private journal and
self-awareness tool, not as an investment advisor, brokerage, or profit
guarantee.

The English hero message is **“Know why you trade.”** The Korean equivalent is
**“내가 왜 매매하는지 알아보세요.”** Supporting copy emphasizes fast trade
logging, personal pattern discovery, and calm review of the user's own data.

## Visual Direction

Use the approved **Calm Product Gallery** direction:

- A warm, light neutral background with restrained violet accents matching the
  app's interface.
- A centered hero with concise copy, the MindTrade app icon, and a prominent
  App Store download action.
- Three real simulator captures arranged as a product gallery in the hero.
- Generous white space, soft borders, and minimal shadows.
- A calm and credible tone instead of a high-pressure finance aesthetic.

The site must use actual simulator captures from:

- `/Users/woorlds/Development/swift/MindTrade/appstore-previews/en/simulator/`
- `/Users/woorlds/Development/swift/MindTrade/appstore-previews/ko/simulator/`

The source PNG files remain unchanged. The site will contain optimized WebP
derivatives generated from those files. Each locale uses screenshots captured
in that locale; text is not overlaid or synthesized onto screenshots.

## Information Architecture

The page is a single, focused landing page with these sections:

1. **Header** — app icon and name, language switcher, and support link.
2. **Hero** — approved headline, short value proposition, App Store CTA, and a
   three-screen gallery using real captures.
3. **Product flow** — four steps: log a trade in about 30 seconds, recognize
   emotion and bias patterns, find time-based patterns, and review reports.
4. **Feature evidence** — screenshots paired with concise descriptions of the
   quick log, mental pattern profile, time analysis, and reports.
5. **Privacy and trust** — no account required, data stays on device, and no
   user data is collected. Mention iCloud Drive backup only as a user-controlled
   feature; do not claim that the app has no cloud capability.
6. **Closing CTA** — download MindTrade from the App Store.
7. **Footer** — privacy policy, email support, App Store link, language switch,
   and iPhone/iOS compatibility note.

## Localization and URLs

The site uses separate static documents rather than runtime JavaScript
translation:

- `/mindtrade/index.html` — English and canonical default
- `/mindtrade/ko/index.html` — Korean

Both documents include canonical metadata, `hreflang` links for `en`, `ko`, and
`x-default`, localized titles and descriptions, and locale-appropriate image
alternative text. The language switch preserves the page's top-level location.

External links:

- App Store: `https://apps.apple.com/app/mindtrade/id6767873530`
- Privacy: `https://woorlds.github.io/mindtrade-privacy/`
- Support: `mailto:woorlds@gmail.com`

External links must remain usable without JavaScript.

## Technical Structure

The implementation is a dependency-free static site that works on GitHub
Pages:

- `mindtrade/index.html`
- `mindtrade/ko/index.html`
- `mindtrade/style.css`
- `mindtrade/assets/icon.png`
- `mindtrade/assets/en/*.webp`
- `mindtrade/assets/ko/*.webp`
- `mindtrade/README.md`
- `mindtrade/verify.py`

HTML provides all meaningful content and navigation. CSS owns layout, color,
responsive behavior, light/dark presentation, focus states, and reduced-motion
behavior. No client-side framework or product JavaScript is needed.

The app icon is copied from the MindTrade asset catalog. Screenshot derivatives
retain their native aspect ratio and intrinsic dimensions to avoid layout shift.
Below-the-fold screenshots are lazy-loaded; hero imagery is prioritized.

## Responsive and Accessible Behavior

- Support 320, 375, 390, and 430 CSS-pixel mobile widths plus tablet and desktop.
- On mobile, hero screenshots overlap or stack without horizontal scrolling and
  feature sections become a single readable column.
- On wider screens, the hero becomes a balanced gallery and feature sections
  alternate copy and imagery.
- Provide a skip link, semantic headings, landmark elements, descriptive image
  alternatives, visible keyboard focus, and touch targets of at least 44 points.
- Respect `prefers-reduced-motion` and avoid motion required for comprehension.
- Maintain readable contrast in both light and dark color schemes.

## Content Constraints

- Do not claim guaranteed returns, loss prevention, brokerage integration, or
  individualized investment advice.
- Do not describe rule-based insights as AI.
- Describe privacy consistently with the current App Store listing: user data
  is not collected, core records stay on device, and iCloud Drive backup is
  user-controlled.
- Use concise language that scans well on a phone.
- English and Korean pages must communicate the same feature scope even when
  phrasing is adapted naturally for each language.

## Verification

The implementation is complete only after all of the following pass:

1. Run the local verifier to check required files, localized metadata,
   reciprocal locale links, image references, image dimensions, alternative
   text, and external URLs.
2. Serve the repository locally and inspect both locales at mobile widths of
   320, 375, 390, and 430 pixels and at one desktop width.
3. Check light mode, dark mode, keyboard navigation, visible focus, reduced
   motion, and absence of horizontal overflow.
4. Confirm every visible App Store, privacy, support, and language link.
5. Confirm all displayed product images are derivatives of the provided real
   simulator captures.
6. After deployment, confirm the English and Korean GitHub Pages URLs return
   successful responses and render their localized content.

## Out of Scope

- Hosting changes outside the existing GitHub Pages repository
- Analytics, cookies, tracking, or contact forms
- Additional languages beyond English and Korean
- App code changes
- Generated or composited fake app screens
