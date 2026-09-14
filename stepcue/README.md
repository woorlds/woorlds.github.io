# StepCue marketing site

Mobile-first, localized marketing pages for the iPhone-only StepCue app.

## URLs

- English: https://woorlds.github.io/stepcue/
- Korean: https://woorlds.github.io/stepcue/ko/
- Japanese: https://woorlds.github.io/stepcue/ja/
- Privacy: https://woorlds.github.io/app-legal/stepcue/privacy/
- Support: https://woorlds.github.io/app-legal/stepcue/support/

## Image sources

The app icon is copied from:

```text
/Users/woorlds/Development/swift/StepCue/StepCue/Assets.xcassets/AppIcon.appiconset/stepcue.png
```

Localized simulator screenshots come from:

```text
/Users/woorlds/Development/swift/StepCue/appstore-previews/{en,ko,ja}/simulator/
```

The site uses these source files for each locale:

- `02_morning_pinned.png` → `routines.webp`
- `03_timer.png` → `timer.webp`
- `04_editor.png` → `editor.webp`
- `06_rhythm.png` → `rhythm.webp`

The source PNG files remain unchanged. Web derivatives were generated with the already-installed Pillow runtime:

```bash
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

## Local verification

From the repository root:

```bash
python3 stepcue/verify.py
python3 -m http.server 8000
```

Open these local pages:

- http://localhost:8000/stepcue/
- http://localhost:8000/stepcue/ko/
- http://localhost:8000/stepcue/ja/

Check 320, 375, 390, and 430 CSS-pixel widths, plus one desktop width. Also check light mode, dark mode, reduced motion, keyboard focus, and every visible link.

## Deployment verification

GitHub Pages publishes `main` from the repository root. After pushing verified changes, confirm:

```bash
curl --fail --location https://woorlds.github.io/stepcue/
curl --fail --location https://woorlds.github.io/stepcue/ko/
curl --fail --location https://woorlds.github.io/stepcue/ja/
curl --fail --location https://woorlds.github.io/app-legal/stepcue/privacy/
curl --fail --location https://woorlds.github.io/app-legal/stepcue/support/
```
