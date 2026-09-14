# StepCue Marketing Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a mobile-first English, Korean, and Japanese StepCue marketing site at `https://woorlds.github.io/stepcue/`.

**Architecture:** Build three semantic static HTML documents with stable localized URLs, one shared mobile-first stylesheet, and locale-specific optimized screenshot assets copied from the StepCue project. Add a dependency-free Python verifier so link, asset, language, naming, and excluded-content contracts can be checked before and after deployment.

**Tech Stack:** HTML5, CSS, Python 3 standard library, GitHub Pages

**Spec:** `docs/superpowers/specs/2026-09-14-stepcue-marketing-site-design.md`

## Global Constraints

- English is served from `/stepcue/`; Korean from `/stepcue/ko/`; Japanese from `/stepcue/ja/`.
- Design from 320 CSS pixels upward and keep touch targets at least 44 by 44 CSS pixels.
- Use the StepCue CalmSystem light and dark color tokens exactly as documented in the spec.
- Source screenshots only from `/Users/woorlds/Development/swift/StepCue/appstore-previews/{en,ko,ja}/simulator/`.
- The hero uses the current locale-specific `03_timer.png`.
- Do not show an App Store badge, download action, release date, or pre-release availability message.
- Do not add analytics, forms, cookies, accounts, or runtime data requests.
- Spell `woorlds` entirely in lowercase in StepCue page content and metadata.
- Do not link to other apps from the StepCue page.
- StepCue is an iPhone-only app.

---

### Task 1: Localized Static Site and Assets

**Files:**
- Create: `stepcue/index.html`
- Create: `stepcue/ko/index.html`
- Create: `stepcue/ja/index.html`
- Create: `stepcue/style.css`
- Create: `stepcue/assets/icon.png`
- Create: `stepcue/assets/en/routines.webp`
- Create: `stepcue/assets/en/timer.webp`
- Create: `stepcue/assets/en/editor.webp`
- Create: `stepcue/assets/en/rhythm.webp`
- Create: `stepcue/assets/ko/routines.webp`
- Create: `stepcue/assets/ko/timer.webp`
- Create: `stepcue/assets/ko/editor.webp`
- Create: `stepcue/assets/ko/rhythm.webp`
- Create: `stepcue/assets/ja/routines.webp`
- Create: `stepcue/assets/ja/timer.webp`
- Create: `stepcue/assets/ja/editor.webp`
- Create: `stepcue/assets/ja/rhythm.webp`
- Create: `stepcue/verify.py`

**Interfaces:**
- Consumes: StepCue app icon and locale-specific simulator PNGs from the StepCue repository.
- Produces: Three localized static pages that share `stepcue/style.css` and refer only to files under `stepcue/assets/`.

- [ ] **Step 1: Write the dependency-free contract verifier**

Implement `stepcue/verify.py` with `html.parser.HTMLParser` and `pathlib.Path`. For all three localized pages, assert:

```python
EXPECTED = {
    "index.html": ("en", "assets/en/timer.webp"),
    "ko/index.html": ("ko", "../assets/ko/timer.webp"),
    "ja/index.html": ("ja", "../assets/ja/timer.webp"),
}
FORBIDDEN = ("Coming soon", "More apps", "다른 앱", "その他のアプリ", "Woorlds")
```

The verifier must parse and check the root `lang`, exactly one H1, canonical URL, all four alternate-language declarations, required privacy/support URLs, local stylesheet and image existence, nonempty `alt` text, hero image eager priority, below-the-fold `loading="lazy"`, and absence of forbidden phrases. Print every failure and exit 1; print `StepCue site verification passed.` and exit 0 otherwise.

- [ ] **Step 2: Run the verifier before implementation**

Run before creating the site:

```bash
python3 stepcue/verify.py
```

Expected: FAIL because the localized pages do not exist.

- [ ] **Step 3: Optimize the approved localized screenshots**

Use the already-installed Pillow runtime to copy the icon and convert each locale’s selected simulator PNGs to WebP without modifying the StepCue sources:

```bash
mkdir -p stepcue/assets/{en,ko,ja}
cp /Users/woorlds/Development/swift/StepCue/StepCue/Assets.xcassets/AppIcon.appiconset/stepcue.png stepcue/assets/icon.png
python3 - <<'PY'
from pathlib import Path
from PIL import Image

source = Path("/Users/woorlds/Development/swift/StepCue/appstore-previews")
target = Path("stepcue/assets")
names = {
    "02_morning_pinned.png": "routines.webp",
    "03_timer.png": "timer.webp",
    "04_editor.png": "editor.webp",
    "06_rhythm.png": "rhythm.webp",
}
for locale in ("en", "ko", "ja"):
    for input_name, output_name in names.items():
        with Image.open(source / locale / "simulator" / input_name) as image:
            image.save(target / locale / output_name, "WEBP", quality=88, method=6)
PY
```

- [ ] **Step 4: Implement the shared mobile-first stylesheet**

Create `stepcue/style.css` with the documented CalmSystem variables, single-column default layout, the first wide-layout breakpoint at 760 pixels, explicit 44-pixel target minimums, `prefers-color-scheme: dark`, and `prefers-reduced-motion: reduce`. Reproduce the approved mockup’s header, hero, screenshot, feature flow, trust cards, and two-link footer.

Required CSS contract:

```css
:root {
  color-scheme: light dark;
  --background: #F5F2E9;
  --card: #FFFDF8;
  --surface: #EFEAE0;
  --action: #367865;
  --action-strong: #285F50;
  --action-soft: #DCECE5;
  --text: #1C2823;
  --secondary-text: #6D756F;
  --border: #D9D2C5;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #111612;
    --card: #1B211D;
    --surface: #202820;
    --action: #72B49E;
    --action-strong: #9BD6C3;
    --action-soft: #23352F;
    --text: #F2F6F3;
    --secondary-text: #C7D1CB;
    --border: #344139;
  }
}
```

- [ ] **Step 5: Implement the three semantic localized pages**

Each page must contain a skip link, compact brand header, real language URLs, localized support label, localized hero copy and timer screenshot, the three-feature flow, three trust cards, and a footer with only privacy and support. Add localized `<title>`, description, canonical URL, and reciprocal `hreflang` links for `en`, `ko`, `ja`, and `x-default`.

Use these link targets exactly:

```html
<a href="https://woorlds.github.io/app-legal/stepcue/privacy/">Privacy</a>
<a href="https://woorlds.github.io/app-legal/stepcue/support/">Support</a>
```

The Korean and Japanese documents localize those visible labels while retaining the same targets. The English page uses `./style.css` and `./assets/en/...`; Korean and Japanese use `../style.css` and `../assets/<locale>/...`.

- [ ] **Step 6: Run the verifier and fix each reported contract failure**

```bash
python3 stepcue/verify.py
```

Expected: `StepCue site verification passed.` with exit code 0.

- [ ] **Step 7: Commit the localized site and verifier**

```bash
git add stepcue/index.html stepcue/ko/index.html stepcue/ja/index.html stepcue/style.css stepcue/assets stepcue/verify.py
git commit -m "feat: add StepCue marketing pages"
```

### Task 2: Site Contract Verification and Documentation

**Files:**
- Create: `stepcue/README.md`

**Interfaces:**
- Consumes: Static pages and assets from Task 1.
- Produces: Source and deployment documentation plus browser verification evidence for the Task 1 site contract.

- [ ] **Step 1: Re-run the verifier before documenting the site**

```bash
python3 stepcue/verify.py
```

Expected: `StepCue site verification passed.` with exit code 0.

- [ ] **Step 2: Document sources and commands**

Create `stepcue/README.md` listing the three public URLs, exact StepCue source paths, chosen source filenames, image conversion command, local server command, verifier command, and deployment verification commands.

- [ ] **Step 3: Verify markup, links, and responsive rendering locally**

```bash
python3 -m http.server 8000
```

Inspect `/stepcue/`, `/stepcue/ko/`, and `/stepcue/ja/` at widths 320, 375, 390, 430, and 1024 pixels. Check light mode, dark mode, reduced motion, keyboard focus, language navigation, feature anchor, privacy, and support. Confirm no horizontal overflow and capture console errors; expected: none.

- [ ] **Step 4: Commit documentation**

```bash
git add stepcue/README.md
git commit -m "docs: document StepCue marketing site"
```

### Task 3: Final Audit and GitHub Pages Deployment

**Files:**
- Verify: `stepcue/`
- Verify: `docs/superpowers/specs/2026-09-14-stepcue-marketing-site-design.md`
- Verify: `docs/superpowers/plans/2026-09-14-stepcue-marketing-site.md`

**Interfaces:**
- Consumes: Completed site, verifier, and repository GitHub Pages configuration.
- Produces: Public English, Korean, and Japanese StepCue marketing URLs.

- [ ] **Step 1: Run the complete local audit**

```bash
python3 stepcue/verify.py
git diff --check
git status --short
```

Expected: verifier passes, `git diff --check` emits no output, and status contains only an intentional plan-document change if it has not yet been committed.

- [ ] **Step 2: Commit the implementation plan**

```bash
git add docs/superpowers/plans/2026-09-14-stepcue-marketing-site.md
git commit -m "docs: plan StepCue marketing site"
```

- [ ] **Step 3: Push the verified commits to GitHub Pages**

```bash
git push origin main
```

Expected: the remote `main` branch advances to the local verified commit.

- [ ] **Step 4: Verify public deployment**

Poll GitHub Pages without fixed sleeps until each URL returns HTTP 200 or a bounded deployment timeout is reached:

```bash
curl --fail --location https://woorlds.github.io/stepcue/
curl --fail --location https://woorlds.github.io/stepcue/ko/
curl --fail --location https://woorlds.github.io/stepcue/ja/
curl --fail --location https://woorlds.github.io/app-legal/stepcue/privacy/
curl --fail --location https://woorlds.github.io/app-legal/stepcue/support/
```

Inspect the public English page and switch to Korean and Japanese through its visible language links. Confirm localized copy and images load, privacy/support links resolve, `woorlds` is lowercase, and no other-app or pre-release availability link appears.
