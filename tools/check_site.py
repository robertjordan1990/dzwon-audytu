#!/usr/bin/env python3
"""Check HTML structure, local links and every recorded archive checksum."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "/dzwon-audytu/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.counts = {tag: 0 for tag in ("html", "head", "body", "main", "h1")}
        self.links, self.ids, self.duplicate_ids = [], set(), []
        self.lang = None
        self.languages = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.counts:
            self.counts[tag] += 1
        if tag == "html":
            self.lang = a.get("lang")
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicate_ids.append(a["id"])
            self.ids.add(a["id"])
        if tag == "link" and a.get("rel") == "alternate":
            self.languages.add(a.get("hreflang"))
        for key in ("href", "src"):
            if a.get(key):
                self.links.append(a[key])


def main():
    errors, pages = [], {}
    for path in sorted(ROOT.rglob("*.html")):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
        if any(count != 1 for count in page.counts.values()):
            errors.append(f"{path.relative_to(ROOT)}: invalid document structure {page.counts}")
        if page.lang not in {"pl", "en"} or page.duplicate_ids:
            errors.append(f"{path.relative_to(ROOT)}: invalid language/duplicate IDs")
        # Full English reading editions pair with the original PDF, not a second HTML translation.
        if "readings" not in path.parts and page.languages != {"pl", "en"}:
            errors.append(f"{path.relative_to(ROOT)}: missing language alternatives")
    checked = 0
    for path, page in pages.items():
        for raw in page.links:
            u = urlsplit(raw)
            if u.scheme or u.netloc:
                continue
            decoded = unquote(u.path)
            if decoded.startswith(BASE):
                target = ROOT / decoded[len(BASE):]
            elif decoded.startswith("/"):
                errors.append(f"{path.relative_to(ROOT)}: unexpected absolute path {raw}")
                continue
            else:
                target = path.parent / decoded if decoded else path
            target = target.resolve()
            if ROOT not in (target, *target.parents):
                errors.append(f"{path.relative_to(ROOT)}: link escapes archive {raw}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"{path.relative_to(ROOT)}: missing {raw}")
            elif u.fragment and target in pages and u.fragment not in pages[target].ids:
                errors.append(f"{path.relative_to(ROOT)}: missing fragment {raw}")
            checked += 1
    hashes, listed = 0, set()
    for line in (ROOT / "hash" / "SHA256SUMS.txt").read_text().splitlines():
        digest, name = line.split("  ", 1)
        if name in listed:
            errors.append(f"Duplicate checksum entry: {name}")
        listed.add(name)
        p = ROOT / name
        if not p.is_file() or sha256(p.read_bytes()).hexdigest() != digest:
            errors.append(f"Checksum mismatch: {name}")
        hashes += 1
    ignored = {".git", "__pycache__", ".venv", "node_modules"}
    expected = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
                if p.is_file() and not any(part in ignored for part in p.relative_to(ROOT).parts)
                and p.relative_to(ROOT).as_posix() != "hash/SHA256SUMS.txt"}
    if expected != listed:
        errors.append(f"Manifest coverage mismatch: missing={sorted(expected-listed)}, extra={sorted(listed-expected)}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(pages)} HTML pages, {checked} local links, {hashes} checksums")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
