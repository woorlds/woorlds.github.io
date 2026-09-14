#!/usr/bin/env python3

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse
import sys


ROOT = Path(__file__).resolve().parent
PRIVACY_URL = "https://woorlds.github.io/app-legal/stepcue/privacy/"
SUPPORT_URL = "https://woorlds.github.io/app-legal/stepcue/support/"
EXPECTED = {
    "index.html": {
        "lang": "en",
        "canonical": "https://woorlds.github.io/stepcue/",
        "hero": "./assets/en/timer.webp",
        "icon": "./assets/icon.png",
        "stylesheet": "./style.css",
    },
    "ko/index.html": {
        "lang": "ko",
        "canonical": "https://woorlds.github.io/stepcue/ko/",
        "hero": "../assets/ko/timer.webp",
        "icon": "../assets/icon.png",
        "stylesheet": "../style.css",
    },
    "ja/index.html": {
        "lang": "ja",
        "canonical": "https://woorlds.github.io/stepcue/ja/",
        "hero": "../assets/ja/timer.webp",
        "icon": "../assets/icon.png",
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
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.h1_count = 0
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "html":
            self.html_lang = values.get("lang", "")
        elif tag == "h1":
            self.h1_count += 1
        elif tag in {"a", "link"}:
            self.links.append(values)
        elif tag == "img":
            self.images.append(values)


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

    canonicals = [link.get("href") for link in parser.links if link.get("rel") == "canonical"]
    if canonicals != [contract["canonical"]]:
        failures.append(f"{relative_path}: canonical URL is incorrect")

    alternates = {
        link.get("hreflang", ""): link.get("href", "")
        for link in parser.links
        if link.get("rel") == "alternate"
    }
    if alternates != ALTERNATES:
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
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        return 1
    print("StepCue site verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
