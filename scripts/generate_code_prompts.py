#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Example:
    python3 scripts/generate_code_prompts.py /content/awesome-generative-models
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable, List, Set

DEFAULT_OUTPUT = Path("/content/ai_code_temp.txt")


def iter_code_files_in_dir(dir_path: Path, extensions: Set[str] | None = None) -> Iterable[Path]:
    if extensions is None:
        extensions = {".py", ".yaml", ".yml", ".md", ".jsonl"}

    skip_dirs = {
        ".git",
        ".hg",
        ".svn",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "00-surveys-and-foundations",
        "10-image-2d",
        "20-video",
        "30-3d-object-asset",
        "40-3d-scene",
        "50-4d-dynamic-scene-world",
        "90-topics",
        "91-organizations",
    }

    for root, dirs, files in os.walk(dir_path, topdown=True, followlinks=False):
        dirs[:] = [d for d in dirs if d not in skip_dirs and (d == ".github" or not d.startswith("."))]
        for name in files:
            file_path = Path(name)
            if file_path.suffix.lower() in extensions:
                yield Path(root) / name


def collect_files(inputs: List[str], extensions: Set[str] | None = None) -> List[Path]:
    if extensions is None:
        extensions = {".py", ".yaml", ".yml", ".md", ".jsonl"}

    seen: Set[Path] = set()
    result: List[Path] = []

    for raw in inputs:
        path = Path(raw)
        if not path.exists():
            print(f"[warning] path does not exist: {raw}", file=sys.stderr)
            continue

        if path.is_dir():
            for file_path in iter_code_files_in_dir(path, extensions):
                try:
                    abs_path = file_path.resolve(strict=True)
                except Exception:
                    continue
                if abs_path not in seen:
                    seen.add(abs_path)
                    result.append(abs_path)
        else:
            try:
                abs_path = path.resolve(strict=True)
            except Exception:
                print(f"[warning] failed to resolve file: {path}", file=sys.stderr)
                continue
            if abs_path not in seen:
                seen.add(abs_path)
                result.append(abs_path)

    result.sort(key=lambda x: str(x))
    return result


def read_text_best_effort(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8", "gb18030", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def write_prompts(file_paths: List[Path], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with output_path.open("w", encoding="utf-8", newline="\n") as out:
        first_block = True
        for path in file_paths:
            try:
                content = read_text_best_effort(path)
            except Exception as exc:
                print(f"[skip] failed to read: {path} ({exc})", file=sys.stderr)
                continue

            if not first_block:
                out.write("\n")
            first_block = False

            out.write(f"{str(path)} code content:\n")
            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")
            count += 1

    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a plain-text prompt bundle from selected repository files."
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more file or directory paths.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output file path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="*",
        default=[".py", ".yaml", ".yml", ".md", ".jsonl"],
        help="File extensions to include when traversing directories.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    extensions = set(ext if ext.startswith(".") else f".{ext}" for ext in args.extensions)
    files = collect_files(args.paths, extensions)

    if not files:
        print("[info] no matching files found.", file=sys.stderr)
        sys.exit(1)

    print(f"[info] found {len(files)} files:", file=sys.stderr)
    for file_path in files:
        print(f"  - {file_path}", file=sys.stderr)

    written = write_prompts(files, args.output)
    print(f"[done] wrote {written} prompt blocks -> {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
