#!/usr/bin/env python3

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import struct
import sys
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent
APP_STORE_URL = "https://apps.apple.com/app/mindtrade/id6767873530"
PRIVACY_URL = "https://woorlds.github.io/mindtrade-privacy/"
SUPPORT_URL = "mailto:woorlds@gmail.com"

ALTERNATES = {
    "en": "https://woorlds.github.io/mindtrade/",
    "ko": "https://woorlds.github.io/mindtrade/ko/",
    "x-default": "https://woorlds.github.io/mindtrade/",
}

EXPECTED: dict[str, dict[str, object]] = {
    "index.html": {
        "lang": "en",
        "canonical": ALTERNATES["en"],
        "title": "MindTrade — Track Your Trading Psychology",
        "description": "Log trades in 30 seconds, understand the emotions behind your decisions, and discover the patterns shaping your results with MindTrade.",
        "stylesheet": "./style.css",
        "icon": "./assets/icon.png",
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
        "description": "30초 만에 매매와 감정을 기록하고, 반복되는 투자 심리 패턴과 감정이 결과에 미치는 영향을 MindTrade에서 확인하세요.",
        "stylesheet": "../style.css",
        "icon": "../assets/icon.png",
        "images": (
            "../assets/icon.png",
            "../assets/ko/quick-log.webp",
            "../assets/ko/insights.webp",
            "../assets/ko/report.webp",
            "../assets/ko/heatmap.webp",
        ),
    },
}

CSS_CONTRACTS = (
    "min-width: 44px",
    "@media (max-width: 374px)",
    "@media (prefers-color-scheme: dark)",
    "@media (prefers-reduced-motion: reduce)",
    "overflow-x: clip",
    ":focus-visible",
    "width: min(100%, 340px)",
)
MOBILE_CSS_CONTRACTS = (
    "scroll-snap-type: x mandatory",
    "scroll-snap-align: center",
    "overscroll-behavior-inline: contain",
    "-webkit-overflow-scrolling: touch",
    "width: calc(100% + 28px)",
    "word-break: keep-all",
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


def verify_page(relative_path: str, contract: dict[str, object]) -> list[str]:
    failures: list[str] = []
    page = ROOT / relative_path
    if not page.is_file():
        return [f"{relative_path}: page is missing"]

    source = page.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)

    if "●" in source:
        failures.append(f"{relative_path}: App Store CTA must not use a generic bullet as its icon")
    if 'class="gallery-hint"' not in source:
        failures.append(f"{relative_path}: mobile gallery needs a localized swipe hint")

    if parser.html_lang != contract["lang"]:
        failures.append(f"{relative_path}: expected lang={contract['lang']!r}")
    if parser.h1_count != 1:
        failures.append(f"{relative_path}: expected exactly one h1, found {parser.h1_count}")
    if parser.title.strip() != contract["title"]:
        failures.append(f"{relative_path}: localized title is incorrect")

    descriptions = [
        meta.get("content", "")
        for meta in parser.meta
        if meta.get("name") == "description"
    ]
    if descriptions != [contract["description"]]:
        failures.append(f"{relative_path}: localized description is incorrect")

    canonicals = [link.get("href", "") for link in parser.links if link.get("rel") == "canonical"]
    if canonicals != [contract["canonical"]]:
        failures.append(f"{relative_path}: canonical URL is incorrect")

    alternate_links = [link for link in parser.links if link.get("rel") == "alternate"]
    alternates = {link.get("hreflang", ""): link.get("href", "") for link in alternate_links}
    if len(alternate_links) != 3 or alternates != ALTERNATES:
        failures.append(f"{relative_path}: alternate language URLs are incomplete")

    hrefs = {link.get("href", "") for link in parser.links}
    for required in (APP_STORE_URL, PRIVACY_URL, SUPPORT_URL):
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
        failures.append(f"{relative_path}: favicon path is incorrect")

    for link in parser.links:
        path = local_path(page, link.get("href", ""))
        if path is not None and not path.is_file() and not path.is_dir():
            failures.append(f"{relative_path}: missing local link target {link.get('href', '')}")

    image_sources = tuple(image.get("src", "") for image in parser.images)
    if image_sources != contract["images"]:
        failures.append(f"{relative_path}: localized image paths are incorrect")
    for image in parser.images:
        src = image.get("src", "")
        if not image.get("alt", "").strip():
            failures.append(f"{relative_path}: image {src!r} needs nonempty alt text")
        try:
            width = int(image.get("width", "0"))
            height = int(image.get("height", "0"))
        except ValueError:
            width = height = 0
        if width <= 0 or height <= 0:
            failures.append(f"{relative_path}: image {src!r} needs numeric intrinsic dimensions")
        path = local_path(page, src)
        if path is None or not path.is_file():
            failures.append(f"{relative_path}: missing image {src!r}")

    hero_images = [image for image in parser.images if "hero-screen" in image.get("class", "").split()]
    if len(hero_images) != 3:
        failures.append(f"{relative_path}: expected three hero screenshots")
    for image in hero_images:
        if image.get("fetchpriority") != "high" or image.get("loading") == "lazy":
            failures.append(f"{relative_path}: hero screenshots must load eagerly at high priority")

    below_fold = [image for image in parser.images if "feature-screen" in image.get("class", "").split()]
    if len(below_fold) != 1 or below_fold[0].get("loading") != "lazy":
        failures.append(f"{relative_path}: heatmap screenshot must load lazily below the fold")

    return failures


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as stream:
        signature = stream.read(24)
    if signature[:8] != b"\x89PNG\r\n\x1a\n":
        return (0, 0)
    return struct.unpack(">II", signature[16:24])


def webp_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()[:30]
    if len(data) < 16 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return (0, 0)
    kind = data[12:16]
    if kind == b"VP8X" and len(data) >= 30:
        return (
            1 + int.from_bytes(data[24:27], "little"),
            1 + int.from_bytes(data[27:30], "little"),
        )
    if kind == b"VP8 " and len(data) >= 30 and data[23:26] == b"\x9d\x01\x2a":
        return (
            int.from_bytes(data[26:28], "little") & 0x3FFF,
            int.from_bytes(data[28:30], "little") & 0x3FFF,
        )
    if kind == b"VP8L" and len(data) >= 25 and data[20] == 0x2F:
        bits = int.from_bytes(data[21:25], "little")
        return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
    return (0, 0)


def verify_assets() -> list[str]:
    failures: list[str] = []
    icon = ROOT / "assets/icon.png"
    if not icon.is_file():
        failures.append("assets/icon.png: file is missing")
    elif png_dimensions(icon) != (128, 128) or icon.stat().st_size > 100_000:
        failures.append("assets/icon.png: expected an optimized 128px PNG under 100KB")

    for locale in ("en", "ko"):
        for name in ("quick-log", "insights", "report", "heatmap"):
            path = ROOT / f"assets/{locale}/{name}.webp"
            label = path.relative_to(ROOT)
            if not path.is_file():
                failures.append(f"{label}: file is missing")
            elif webp_dimensions(path) != (1320, 2868):
                failures.append(f"{label}: expected a readable 1320×2868 WebP")
            elif path.stat().st_size > 500_000:
                failures.append(f"{label}: expected a WebP under 500KB")
    return failures


def main() -> int:
    failures = [
        failure
        for relative_path, contract in EXPECTED.items()
        for failure in verify_page(relative_path, contract)
    ]
    failures.extend(verify_assets())
    if any(ROOT.rglob("__pycache__")):
        failures.append("site tree: Python cache directories must not be deployed")

    stylesheet_path = ROOT / "style.css"
    if not stylesheet_path.is_file():
        failures.append("style.css: file is missing")
    else:
        stylesheet = stylesheet_path.read_text(encoding="utf-8")
        for contract in CSS_CONTRACTS:
            if contract not in stylesheet:
                failures.append(f"style.css: missing contract {contract!r}")
        for contract in MOBILE_CSS_CONTRACTS:
            if contract not in stylesheet:
                failures.append(f"style.css: missing mobile gallery contract {contract!r}")
        if re.search(
            r"^\s*(?:width|min-width):\s*(?:[5-9]|[1-9]\d+)\d{2,}px",
            stylesheet,
            re.MULTILINE,
        ):
            failures.append("style.css: fixed wide layout risks horizontal overflow")

    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        return 1
    print("MindTrade site verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
