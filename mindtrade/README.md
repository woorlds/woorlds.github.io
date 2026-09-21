# MindTrade marketing site

Mobile-first marketing pages for the iPhone trading-psychology journal MindTrade.

## URLs

- English: https://woorlds.github.io/mindtrade/
- Korean: https://woorlds.github.io/mindtrade/ko/
- App Store: https://apps.apple.com/app/mindtrade/id6767873530
- Privacy: https://woorlds.github.io/mindtrade-privacy/
- Support: mailto:woorlds@gmail.com

## Image sources

The app icon is copied and resized from:

```text
/Users/woorlds/Development/swift/MindTrade/MindTrade/MindTrade/Assets.xcassets/AppIcon.appiconset/icon.png
```

Localized simulator screenshots come from:

```text
/Users/woorlds/Development/swift/MindTrade/appstore-previews/{en,ko}/simulator/
```

The site uses these source files for each locale:

- `02_quick_log.png` → `quick-log.webp`
- `03_insights.png` → `insights.webp`
- `04_time_heatmap.png` → `heatmap.webp`
- `05_report.png` → `report.webp`

The source PNG files remain unchanged. Web derivatives were generated with
Pillow:

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

## Local verification

From the repository root:

```bash
python3 mindtrade/verify.py
python3 -m http.server 8000
```

Open:

- http://localhost:8000/mindtrade/
- http://localhost:8000/mindtrade/ko/

Check 320, 375, 390, and 430 CSS-pixel widths plus one desktop width. Verify
light mode, dark mode, reduced motion, keyboard focus, skip navigation, absence
of horizontal overflow, localized screenshots, and every visible link.
