# MindTrade Marketing Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify an English-first, Korean-localized MindTrade marketing site at `/mindtrade/` using real simulator captures and a live App Store download CTA.

**Architecture:** Add a dependency-free GitHub Pages subtree with two static HTML documents sharing one responsive stylesheet. Generate optimized locale-specific WebP assets from the supplied simulator PNGs, then enforce the content, localization, accessibility, image, and link contracts with a self-contained Python verifier modeled on the existing StepCue site.

**Tech Stack:** Semantic HTML5, CSS, Python 3 standard library, Pillow for one-time image conversion, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-09-21-mindtrade-marketing-site-design.md`

## Global Constraints

- The canonical English page is `https://woorlds.github.io/mindtrade/`; Korean is `https://woorlds.github.io/mindtrade/ko/`.
- Use actual localized simulator captures from `/Users/woorlds/Development/swift/MindTrade/appstore-previews/{en,ko}/simulator/`; never synthesize or overlay app UI.
- Keep source PNGs unchanged and commit only optimized derivatives to the website repository.
- App Store CTA: `https://apps.apple.com/app/mindtrade/id6767873530`.
- Privacy URL: `https://woorlds.github.io/mindtrade-privacy/`; support URL: `mailto:woorlds@gmail.com`.
- Do not claim guaranteed returns, loss prevention, brokerage integration, personalized investment advice, or AI-powered insights.
- Describe privacy accurately: no user data is collected, core records stay on device, and iCloud Drive backup is user-controlled.
- No framework, package installation, analytics, cookies, tracking, or product JavaScript.
- English and Korean must have equivalent scope and locale-specific screenshots, metadata, link labels, and image alternative text.

## Review Focus

- A 320px-wide device must show the full header, CTA, and hero gallery without horizontal overflow; Task 3 pins this with CSS and Task 4 checks it in a browser.
- A locale page must never reference screenshots from the other locale; Task 1 verifies exact image paths for both documents.
- An App Store, privacy, support, or language link must not be omitted or replaced with a placeholder; Task 1 verifies exact required targets.
- Below-the-fold images must not delay the hero or cause layout shift; Task 1 checks loading attributes and intrinsic dimensions, while Task 2 records actual dimensions.
- Dark mode and reduced-motion preferences must preserve readable content and visible focus; Task 1 checks required CSS contracts and Task 4 visually verifies them.

---

### Task 1: Add the executable site contract

**Files:**
- Create: `mindtrade/verify.py`
- Test: `mindtrade/verify.py` (self-testing site contract, matching the established `stepcue/verify.py` pattern)

**Interfaces:**
- Consumes: the approved spec and the repository-relative layout under `mindtrade/`
- Produces: `verify_page(relative_path: str, contract: dict[str, object]) -> list[str]` and `main() -> int`; exit code `0` means the complete static-site contract passes

- [ ] **Step 1: Write the verifier with exact locale contracts**

Define constants and contracts before any site files exist:

```python
ROOT = Path(__file__).resolve().parent
APP_STORE_URL = "https://apps.apple.com/app/mindtrade/id6767873530"
PRIVACY_URL = "https://woorlds.github.io/mindtrade-privacy/"
SUPPORT_URL = "mailto:woorlds@gmail.com"

ALTERNATES = {
    "en": "https://woorlds.github.io/mindtrade/",
    "ko": "https://woorlds.github.io/mindtrade/ko/",
    "x-default": "https://woorlds.github.io/mindtrade/",
}

EXPECTED = {
    "index.html": {
        "lang": "en",
        "canonical": ALTERNATES["en"],
        "title": "MindTrade — Track Your Trading Psychology",
        "images": (
            "./assets/icon.png",
            "./assets/en/quick-log.webp",
            "./assets/en/insights.webp",
            "./assets/en/report.webp",
            "./assets/en/heatmap.webp",
        ),
    },
    "ko/index.html": {
        "lang": "ko",
        "canonical": ALTERNATES["ko"],
        "title": "MindTrade — 투자 심리를 기록하고 이해하세요",
        "images": (
            "../assets/icon.png",
            "../assets/ko/quick-log.webp",
            "../assets/ko/insights.webp",
            "../assets/ko/report.webp",
            "../assets/ko/heatmap.webp",
        ),
    },
}
```

Implement an `HTMLParser` subclass that records `<html lang>`, title, meta tags,
links, headings, and images. `verify_page` must report all failures rather than
stop at the first one. Check exactly one `h1`, localized title/description,
canonical and all three alternate URLs, one stylesheet, one favicon, all three
required external links, exact locale image order, nonempty `alt`, numeric
`width`/`height`, existing local targets, eager `fetchpriority="high"` on the
three hero screenshots, and `loading="lazy"` on the heatmap screenshot.

In `main`, validate that `style.css` contains these explicit contracts:

```python
CSS_CONTRACTS = (
    "min-width: 44px",
    "@media (max-width: 374px)",
    "@media (prefers-color-scheme: dark)",
    "@media (prefers-reduced-motion: reduce)",
    "overflow-x: clip",
    ":focus-visible",
)
```

Also verify `assets/icon.png` is a 128×128 PNG under 100 KB and every WebP is
readable, has positive dimensions, and is under 500 KB. Print each error as
`FAIL: ...`; otherwise print `MindTrade site verification passed.`.

- [ ] **Step 2: Run the contract to prove it fails before implementation**

Run: `python3 mindtrade/verify.py`

Expected: nonzero exit with missing-page, missing-stylesheet, and missing-asset failures. The verifier itself must not crash when files are absent.

- [ ] **Step 3: Commit the failing contract**

```bash
git add mindtrade/verify.py
git commit -m "test: define MindTrade marketing site contract"
```

### Task 2: Generate and document authentic web assets

**Files:**
- Create: `mindtrade/assets/icon.png`
- Create: `mindtrade/assets/en/quick-log.webp`
- Create: `mindtrade/assets/en/insights.webp`
- Create: `mindtrade/assets/en/report.webp`
- Create: `mindtrade/assets/en/heatmap.webp`
- Create: `mindtrade/assets/ko/quick-log.webp`
- Create: `mindtrade/assets/ko/insights.webp`
- Create: `mindtrade/assets/ko/report.webp`
- Create: `mindtrade/assets/ko/heatmap.webp`
- Create: `mindtrade/README.md`
- Test: `mindtrade/verify.py`

**Interfaces:**
- Consumes: MindTrade `AppIcon.appiconset/icon.png` and locale simulator PNGs named `02_quick_log.png`, `03_insights.png`, `04_time_heatmap.png`, and `05_report.png`
- Produces: immutable site asset paths and provenance instructions consumed by both locale pages and the verifier

- [ ] **Step 1: Generate optimized derivatives without changing sources**

Use the bundled/current Python environment with Pillow and run from repository root:

```python
from pathlib import Path
from PIL import Image

app = Path("/Users/woorlds/Development/swift/MindTrade/MindTrade/MindTrade")
previews = Path("/Users/woorlds/Development/swift/MindTrade/appstore-previews")
target = Path("mindtrade/assets")
mapping = {
    "02_quick_log.png": "quick-log.webp",
    "03_insights.png": "insights.webp",
    "04_time_heatmap.png": "heatmap.webp",
    "05_report.png": "report.webp",
}

target.mkdir(parents=True, exist_ok=True)
with Image.open(app / "Assets.xcassets/AppIcon.appiconset/icon.png") as image:
    image.convert("RGBA").resize((128, 128), Image.Resampling.LANCZOS).save(
        target / "icon.png", optimize=True
    )
for locale in ("en", "ko"):
    (target / locale).mkdir(parents=True, exist_ok=True)
    for source_name, output_name in mapping.items():
        with Image.open(previews / locale / "simulator" / source_name) as image:
            image.save(target / locale / output_name, "WEBP", quality=86, method=6)
```

- [ ] **Step 2: Run the verifier and isolate the expected remaining failures**

Run: `python3 mindtrade/verify.py`

Expected: asset checks pass; failures remain only for the two HTML pages and `style.css`. If a WebP exceeds 500 KB, lower quality in increments of two without resizing or cropping until it passes.

- [ ] **Step 3: Document provenance, URL map, and local verification**

In `mindtrade/README.md`, record the canonical English and Korean URLs, exact source paths and filename mapping, the conversion script above, the App Store/privacy/support destinations, and these local commands:

```bash
python3 mindtrade/verify.py
python3 -m http.server 8000
```

Include local preview URLs `http://localhost:8000/mindtrade/` and `http://localhost:8000/mindtrade/ko/` plus the required mobile widths and appearance/accessibility checks.

- [ ] **Step 4: Commit the authentic asset set**

```bash
git add mindtrade/assets mindtrade/README.md
git commit -m "assets: add localized MindTrade product captures"
```

### Task 3: Build the localized Calm Product Gallery pages

**Files:**
- Create: `mindtrade/index.html`
- Create: `mindtrade/ko/index.html`
- Create: `mindtrade/style.css`
- Test: `mindtrade/verify.py`

**Interfaces:**
- Consumes: Task 2 asset paths and the URL/locale contracts from Task 1
- Produces: the deployable `/mindtrade/` and `/mindtrade/ko/` marketing pages

- [ ] **Step 1: Build the English semantic document**

Create `mindtrade/index.html` with a skip link; branded header; `EN`/`한국어`
switcher; centered hero headed `Know why you trade.`; short copy describing
emotion, bias, and personal-data review; and a primary `Download on the App
Store` link. Use a `hero-gallery` containing `quick-log.webp`, `insights.webp`,
and `report.webp`, all with real intrinsic dimensions and `fetchpriority="high"`.

Below the hero, add four numbered product-flow articles:

1. `Log the moment` — a trade, emotion, and mental pattern in about 30 seconds.
2. `See the pattern` — compare calm and stressed outcomes and recurring bias.
3. `Find the timing` — review time-of-day patterns with the real heatmap image.
4. `Review and reset` — use reports to reflect and improve the process.

Add three trust cards (`On-device by default`, `No account required`, `Your
backup, your choice`) and explicitly say MindTrade does not provide investment
advice. Finish with the App Store CTA and required footer links.

- [ ] **Step 2: Build the Korean document with equivalent scope**

Create `mindtrade/ko/index.html` with the same semantic structure and section
order, localized naturally. The hero heading is `내가 왜 매매하는지 알아보세요.`
and the four feature headings are `순간을 기록하세요`, `패턴을 발견하세요`,
`시간대를 확인하세요`, and `돌아보고 다시 시작하세요`. Use only
`../assets/ko/*.webp`, localized alternative text, and `aria-current="page"`
on `한국어`.

- [ ] **Step 3: Implement the shared responsive style**

Create a warm off-white palette with violet accents, soft lavender surfaces,
subtle borders, and restrained shadows. Center the hero copy and use a
three-device overlapping gallery at desktop widths. At mobile widths, reduce
the overlap and widths so all devices remain inside the viewport. Alternate
copy/image feature rows above 760px and stack them below it.

Required behavior:

```css
body { overflow-x: clip; }
a:focus-visible { outline: 3px solid var(--accent); outline-offset: 4px; }
@media (max-width: 374px) { /* compact header and gallery, 44px targets remain */ }
@media (prefers-color-scheme: dark) { /* readable neutral/violet dark tokens */ }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
```

Use `clamp()` for headings and gallery width, reserve image space with explicit
dimensions, and never hide the MindTrade brand or language links on narrow
screens.

- [ ] **Step 4: Run the full executable contract**

Run: `python3 mindtrade/verify.py`

Expected: `MindTrade site verification passed.` with exit code 0.

- [ ] **Step 5: Check markup and repository integrity**

Run:

```bash
git diff --check
rg -n "id0000000000|Coming soon|TODO|TBD|guaranteed|AI-powered" mindtrade
```

Expected: `git diff --check` exits 0 and the search returns no matches.

- [ ] **Step 6: Commit the deployable localized site**

```bash
git add mindtrade/index.html mindtrade/ko/index.html mindtrade/style.css
git commit -m "feat: add MindTrade marketing site"
```

### Task 4: Perform visual, accessibility, and live-link QA

**Files:**
- Modify if defects are found: `mindtrade/index.html`
- Modify if defects are found: `mindtrade/ko/index.html`
- Modify if defects are found: `mindtrade/style.css`
- Modify if the contract needs regression coverage: `mindtrade/verify.py`

**Interfaces:**
- Consumes: the complete Task 3 site served from repository root
- Produces: verified release-ready pages with any discovered regression encoded in `verify.py`

- [ ] **Step 1: Start a local server and inspect both locales**

Run: `python3 -m http.server 8000`

Open `/mindtrade/` and `/mindtrade/ko/`. At 320, 375, 390, and 430 CSS pixels,
verify no horizontal scroll; header and language switch remain usable; hero CTA
is visible; screenshot text matches the locale; and each feature image is
uncropped. At 1280px, verify the three-screen hero is balanced and feature rows
do not become excessively wide.

- [ ] **Step 2: Exercise appearance and accessibility conditions**

In both locales, verify light and dark mode, keyboard-only navigation, visible
focus, skip-link behavior, reduced motion, meaningful heading order, readable
alternative text, and minimum 44px interactive targets. Fix every defect and
add a verifier assertion when it can be checked statically.

- [ ] **Step 3: Verify all external destinations**

Run:

```bash
curl --fail --location --head https://apps.apple.com/app/mindtrade/id6767873530
curl --fail --location --head https://woorlds.github.io/mindtrade-privacy/
```

Expected: successful HTTP response after redirects. Manually activate
`mailto:woorlds@gmail.com` and both language links from each locale.

- [ ] **Step 4: Run final automated checks**

Run:

```bash
python3 mindtrade/verify.py
git diff --check
git status --short
```

Expected: verifier passes, no whitespace errors, and the worktree contains no
uncommitted site changes.

- [ ] **Step 5: Commit QA fixes only if the previous steps required changes**

```bash
git add mindtrade
git commit -m "fix: polish MindTrade marketing site"
```

If no files changed, do not create an empty commit.
