#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")
HTML_LINK = re.compile(
    r"""(?:href|src)=["']([^"']+)["']""",
    re.IGNORECASE,
)

IGNORED_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "data:",
    "javascript:",
)


def extract_target(raw_target: str) -> str:
    target = raw_target.strip()

    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(" ", 1)[0]

    return unquote(target.strip())


def resolve_target(source: Path, target: str) -> Path | None:
    if not target or target.startswith("#"):
        return None

    lowered = target.lower()
    if lowered.startswith(IGNORED_PREFIXES):
        return None

    parsed = urlparse(target)
    path_text = parsed.path
    if not path_text:
        return None

    if path_text.startswith("/"):
        resolved = ROOT / path_text.lstrip("/")
    else:
        resolved = source.parent / path_text

    try:
        resolved = resolved.resolve()
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return resolved

    return resolved


def main() -> int:
    errors: list[str] = []

    markdown_files = sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
        and "__pycache__" not in path.parts
    )

    for source in markdown_files:
        text = source.read_text(encoding="utf-8", errors="ignore")

        for line_number, line in enumerate(text.splitlines(), start=1):
            targets = [
                *MARKDOWN_LINK.findall(line),
                *HTML_LINK.findall(line),
            ]

            for raw_target in targets:
                target = extract_target(raw_target)
                resolved = resolve_target(source, target)

                if resolved is None:
                    continue

                if not resolved.exists():
                    relative_source = source.relative_to(ROOT)
                    errors.append(
                        f"{relative_source}:{line_number}: "
                        f"missing internal target `{target}`"
                    )

    if errors:
        print("[internal-links] broken internal links:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(
        f"[internal-links] checked {len(markdown_files)} Markdown files: OK"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())