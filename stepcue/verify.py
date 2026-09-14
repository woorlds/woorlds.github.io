#!/usr/bin/env python3

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import struct
from urllib.parse import urlparse
import sys


ROOT = Path(__file__).resolve().parent
PRIVACY_URL = "https://woorlds.github.io/app-legal/stepcue/privacy/"
SUPPORT_URL = "https://woorlds.github.io/app-legal/stepcue/support/"
EXPECTED = {
    "index.html": {
        "lang": "en",
        "canonical": "https://woorlds.github.io/stepcue/",
        "title": "StepCue — A calmer routine timer for iPhone",
        "description": "Turn everyday routines into clear, timed steps. StepCue keeps the current step, remaining time, nearby steps, and expected finish time visible on iPhone.",
        "hero": "./assets/en/timer.webp",
        "icon": "./assets/icon.png",
        "images": ("./assets/icon.png", "./assets/en/timer.webp", "./assets/en/routines.webp", "./assets/en/editor.webp", "./assets/en/rhythm.webp"),
        "stylesheet": "./style.css",
    },
    "ko/index.html": {
        "lang": "ko",
        "canonical": "https://woorlds.github.io/stepcue/ko/",
        "title": "StepCue — iPhone을 위한 차분한 루틴 타이머",
        "description": "매일의 루틴을 명확한 시간 단계로 만드세요. StepCue는 현재 단계, 남은 시간, 주변 단계와 예상 종료 시각을 iPhone에서 한눈에 보여줍니다.",
        "hero": "../assets/ko/timer.webp",
        "icon": "../assets/icon.png",
        "images": ("../assets/icon.png", "../assets/ko/timer.webp", "../assets/ko/routines.webp", "../assets/ko/editor.webp", "../assets/ko/rhythm.webp"),
        "stylesheet": "../style.css",
    },
    "ja/index.html": {
        "lang": "ja",
        "canonical": "https://woorlds.github.io/stepcue/ja/",
        "title": "StepCue — iPhoneのための穏やかなルーティンタイマー",
        "description": "毎日のルーティンをわかりやすい時間付きステップに。StepCueは現在のステップ、残り時間、前後のステップ、終了予定時刻をiPhoneで見やすく表示します。",
        "hero": "../assets/ja/timer.webp",
        "icon": "../assets/icon.png",
        "images": ("../assets/icon.png", "../assets/ja/timer.webp", "../assets/ja/routines.webp", "../assets/ja/editor.webp", "../assets/ja/rhythm.webp"),
        "stylesheet": "../style.css",
    },
}
ALTERNATES = {
    "en": "https://woorlds.github.io/stepcue/",
    "ko": "https://woorlds.github.io/stepcue/ko/",
    "ja": "https://woorlds.github.io/stepcue/ja/",
    "x-default": "https://woorlds.github.io/stepcue/",
}
FORBIDDEN = (
    "Coming soon",
    "More apps",
    "다른 앱",
    "その他のアプリ",
    "Woorlds",
    "복원 루틴",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.h1_count = 0
        self.title = ""
        self.in_title = False
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.meta: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.html_lang = values.get("lang", "")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.in_title = True
        elif tag in {"a", "link"}:
            self.links.append(values)
        elif tag == "img":
            self.images.append(values)
        elif tag == "meta":
            self.meta.append(values)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def local_path(page: Path, value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or value.startswith("#"):
        return None
    return (page.parent / parsed.path).resolve()


def verify_page(relative_path: str, contract: dict[str, str]) -> list[str]:
    failures: list[str] = []
    page = ROOT / relative_path
    if not page.is_file():
        return [f"{relative_path}: page is missing"]

    source = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)

    if parser.html_lang != contract["lang"]:
        failures.append(f"{relative_path}: expected lang={contract['lang']!r}")
    if parser.h1_count != 1:
        failures.append(f"{relative_path}: expected exactly one h1, found {parser.h1_count}")
    if parser.title.strip() != contract["title"]:
        failures.append(f"{relative_path}: localized title is incorrect")
    descriptions = [meta.get("content", "") for meta in parser.meta if meta.get("name") == "description"]
    if descriptions != [contract["description"]]:
        failures.append(f"{relative_path}: localized description is incorrect")
    theme_colors = {
        meta.get("media", "default"): meta.get("content", "")
        for meta in parser.meta
        if meta.get("name") == "theme-color"
    }
    expected_theme_colors = {
        "(prefers-color-scheme: light)": "#F5F2E9",
        "(prefers-color-scheme: dark)": "#111612",
    }
    if theme_colors != expected_theme_colors:
        failures.append(f"{relative_path}: light and dark theme colors are incomplete")

    canonicals = [link.get("href") for link in parser.links if link.get("rel") == "canonical"]
    if canonicals != [contract["canonical"]]:
        failures.append(f"{relative_path}: canonical URL is incorrect")

    alternate_links = [link for link in parser.links if link.get("rel") == "alternate"]
    alternates = {
        link.get("hreflang", ""): link.get("href", "")
        for link in alternate_links
    }
    if len(alternate_links) != 4 or alternates != ALTERNATES:
        failures.append(f"{relative_path}: alternate language URLs are incomplete")

    hrefs = {link.get("href", "") for link in parser.links}
    for required in (PRIVACY_URL, SUPPORT_URL):
        if required not in hrefs:
            failures.append(f"{relative_path}: missing required link {required}")

    stylesheets = [
        link.get("href", "")
        for link in parser.links
        if link.get("rel") == "stylesheet"
    ]
    if stylesheets != [contract["stylesheet"]]:
        failures.append(f"{relative_path}: stylesheet path is incorrect")
    icons = [link.get("href", "") for link in parser.links if link.get("rel") == "icon"]
    if icons != [contract["icon"]]:
        failures.append(f"{relative_path}: app icon favicon is missing")

    for link in parser.links:
        path = local_path(page, link.get("href", ""))
        if path is not None and not path.is_file() and not path.is_dir():
            failures.append(f"{relative_path}: missing local link target {link.get('href', '')}")

    if len(parser.images) != 5:
        failures.append(f"{relative_path}: expected five images, found {len(parser.images)}")
    image_sources = tuple(image.get("src", "") for image in parser.images)
    if image_sources != contract["images"]:
        failures.append(f"{relative_path}: localized image paths are incorrect")
    for image in parser.images:
        src = image.get("src", "")
        if not image.get("alt", "").strip():
            failures.append(f"{relative_path}: image {src!r} needs nonempty alt text")
        path = local_path(page, src)
        if path is None or not path.is_file():
            failures.append(f"{relative_path}: missing image {src!r}")

    hero = next((image for image in parser.images if image.get("class") == "screen"), None)
    if hero is None or hero.get("src") != contract["hero"]:
        failures.append(f"{relative_path}: hero image path is incorrect")
    elif hero.get("fetchpriority") != "high" or hero.get("loading") == "lazy":
        failures.append(f"{relative_path}: hero image must load eagerly at high priority")

    below_fold = [image for image in parser.images if image is not hero and image.get("class") != "app-icon"]
    if any(image.get("loading") != "lazy" for image in below_fold):
        failures.append(f"{relative_path}: below-the-fold images must use loading=lazy")

    for phrase in FORBIDDEN:
        if phrase in source:
            failures.append(f"{relative_path}: forbidden phrase {phrase!r}")

    return failures


def main() -> int:
    failures = [
        failure
        for relative_path, contract in EXPECTED.items()
        for failure in verify_page(relative_path, contract)
    ]
    stylesheet = (ROOT / "style.css").read_text(encoding="utf-8") if (ROOT / "style.css").is_file() else ""
    brand_rule = re.search(r"\.brand\s*\{(?P<body>.*?)\}", stylesheet, re.DOTALL)
    if brand_rule is None or "min-width: 44px;" not in brand_rule.group("body"):
        failures.append("style.css: .brand must keep a 44px minimum touch width")
    if "min-width: 42px;" in stylesheet:
        failures.append("style.css: narrow layouts must not reduce targets below 44px")
    if "clip: rect(0 0 0 0);" in stylesheet:
        failures.append("style.css: narrow layouts must keep the StepCue name visible")
    if "--secondary-on-background: #626a65;" not in stylesheet:
        failures.append("style.css: accessible light background secondary text token is missing")
    if "color: var(--background);" not in stylesheet:
        failures.append("style.css: action foreground must adapt to the page color scheme")

    icon_path = ROOT / "assets/icon.png"
    if icon_path.is_file():
        with icon_path.open("rb") as icon_file:
            signature = icon_file.read(24)
        dimensions = struct.unpack(">II", signature[16:24]) if signature[:8] == b"\x89PNG\r\n\x1a\n" else (0, 0)
        if dimensions != (128, 128) or icon_path.stat().st_size > 100_000:
            failures.append("assets/icon.png: expected an optimized 128px PNG under 100KB")
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        return 1
    print("StepCue site verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
