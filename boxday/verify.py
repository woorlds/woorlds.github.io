#!/usr/bin/env python3

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
PRIVACY_URL = "https://woorlds.github.io/app-legal/boxday/privacy/"
SUPPORT_URL = "https://woorlds.github.io/app-legal/boxday/support/"
ALTERNATES = {
    "en": "https://woorlds.github.io/boxday/",
    "ko": "https://woorlds.github.io/boxday/ko/",
    "ja": "https://woorlds.github.io/boxday/ja/",
    "x-default": "https://woorlds.github.io/boxday/",
}
EXPECTED = {
    "index.html": {
        "lang": "en",
        "canonical": ALTERNATES["en"],
        "stylesheet": "./style.css",
        "icon": "./assets/icon.png",
        "images": ("./assets/icon.png", "./assets/en/today.webp", "./assets/en/today.webp", "./assets/en/editor.webp", "./assets/en/notifications.webp", "./assets/en/stats.webp"),
    },
    "ko/index.html": {
        "lang": "ko",
        "canonical": ALTERNATES["ko"],
        "stylesheet": "../style.css",
        "icon": "../assets/icon.png",
        "images": ("../assets/icon.png", "../assets/ko/today.webp", "../assets/ko/today.webp", "../assets/ko/editor.webp", "../assets/ko/notifications.webp", "../assets/ko/stats.webp"),
    },
    "ja/index.html": {
        "lang": "ja",
        "canonical": ALTERNATES["ja"],
        "stylesheet": "../style.css",
        "icon": "../assets/icon.png",
        "images": ("../assets/icon.png", "../assets/ja/today.webp", "../assets/ja/today.webp", "../assets/ja/editor.webp", "../assets/ja/notifications.webp", "../assets/ja/stats.webp"),
    },
}
FORBIDDEN = ("DEVELOPER", "Seed 200 Test Boxes", "Delete Test Data", "Critical Alerts", "Coming soon")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang = ""
        self.h1_count = 0
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.ids: list[str] = []
        self.notification_crop_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "html":
            self.html_lang = values.get("lang", "")
        elif tag == "h1":
            self.h1_count += 1
        elif tag in {"a", "link"}:
            self.links.append(values)
        elif tag == "img":
            self.images.append(values)
        if "notification-crop" in values.get("class", "").split():
            self.notification_crop_count += 1


def local_path(page: Path, value: str) -> Path | None:
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc or value.startswith("#") or value.startswith("/"):
        return None
    return (page.parent / parsed.path).resolve()


def verify_page(relative_path: str, contract: dict[str, object]) -> list[str]:
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
        failures.append(f"{relative_path}: expected exactly one h1")
    if len(parser.ids) != len(set(parser.ids)):
        failures.append(f"{relative_path}: element IDs must be unique")

    canonicals = [link.get("href") for link in parser.links if link.get("rel") == "canonical"]
    if canonicals != [contract["canonical"]]:
        failures.append(f"{relative_path}: canonical URL is incorrect")
    alternate_links = [link for link in parser.links if link.get("rel") == "alternate"]
    alternates = {link.get("hreflang", ""): link.get("href", "") for link in alternate_links}
    if len(alternate_links) != 4 or alternates != ALTERNATES:
        failures.append(f"{relative_path}: alternate language URLs are incomplete")

    hrefs = {link.get("href", "") for link in parser.links}
    for required in ("#features", PRIVACY_URL, SUPPORT_URL):
        if required not in hrefs:
            failures.append(f"{relative_path}: missing required link {required}")
    stylesheets = [link.get("href", "") for link in parser.links if link.get("rel") == "stylesheet"]
    if stylesheets != [contract["stylesheet"]]:
        failures.append(f"{relative_path}: stylesheet path is incorrect")
    icons = [link.get("href", "") for link in parser.links if link.get("rel") == "icon"]
    if icons != [contract["icon"]]:
        failures.append(f"{relative_path}: favicon path is incorrect")

    image_sources = tuple(image.get("src", "") for image in parser.images)
    if image_sources != contract["images"]:
        failures.append(f"{relative_path}: localized image paths are incorrect")
    for image in parser.images:
        src = image.get("src", "")
        if not image.get("alt", "").strip():
            failures.append(f"{relative_path}: image {src!r} needs alt text")
        path = local_path(page, src)
        if path is None or not path.is_file():
            failures.append(f"{relative_path}: missing image {src!r}")
        if not image.get("width") or not image.get("height"):
            failures.append(f"{relative_path}: image {src!r} needs explicit dimensions")
    hero = next((image for image in parser.images if "screen" in image.get("class", "").split()), None)
    if hero is None or hero.get("fetchpriority") != "high" or hero.get("loading") == "lazy":
        failures.append(f"{relative_path}: hero image loading policy is incorrect")
    below_fold = [image for image in parser.images if image is not hero and "app-icon" not in image.get("class", "").split()]
    if any(image.get("loading") != "lazy" for image in below_fold):
        failures.append(f"{relative_path}: below-fold images must use loading=lazy")
    if parser.notification_crop_count != 1:
        failures.append(f"{relative_path}: expected one notification-crop container")
    for phrase in FORBIDDEN:
        if phrase in source:
            failures.append(f"{relative_path}: forbidden phrase {phrase!r}")
    return failures


def main() -> int:
    failures = [failure for path, contract in EXPECTED.items() for failure in verify_page(path, contract)]
    stylesheet = ROOT / "style.css"
    if not stylesheet.is_file():
        failures.append("style.css: stylesheet is missing")
    else:
        css = stylesheet.read_text(encoding="utf-8")
        for required in ("notification-crop", "prefers-color-scheme: dark", "prefers-reduced-motion", "min-width: 44px"):
            if required not in css:
                failures.append(f"style.css: missing {required!r}")
        if re.search(r"min-(?:width|height):\s*(?:4[0-3]|[0-3]?\d)px", css):
            failures.append("style.css: interactive targets must not shrink below 44px")
    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        return 1
    print("Boxday site verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
