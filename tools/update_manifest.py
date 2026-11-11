#!/usr/bin/env python3
"""Regenerate SHA-256 for the static archive, excluding the manifest itself."""
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "hash" / "SHA256SUMS.txt"
IGNORED = {".git", "__pycache__", ".venv", "node_modules"}


def archive_files():
    return sorted(p for p in ROOT.rglob("*") if p.is_file()
                  and not any(part in IGNORED for part in p.relative_to(ROOT).parts)
                  and p != MANIFEST)


if __name__ == "__main__":
    lines = [f"{sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}\n"
             for p in archive_files()]
    MANIFEST.parent.mkdir(exist_ok=True)
    MANIFEST.write_text("".join(lines), encoding="utf-8")
    print(f"Recorded {len(lines)} files in hash/SHA256SUMS.txt")
