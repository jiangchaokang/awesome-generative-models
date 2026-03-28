#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
python3 generate_code_prompts.py /content/awesome-generative-models
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Iterable, List, Set

DEFAULT_OUTPUT = Path("ai_code_temp.txt")


def iter_code_files_in_dir(dir_path: Path, extensions: Set[str] = None) -> Iterable[Path]:
    if extensions is None:
        extensions = {".py", ".yaml", ".yml", ".md", ".jsonl"}  # 默认支持的文件类型
    
    # 需要跳过的目录（不包括 .github）
    skip_dirs = {
        ".git", ".hg", ".svn",
        "__pycache__", ".mypy_cache", ".pytest_cache",
        ".venv", "venv", "env", "node_modules"
    }
    
    for root, dirs, files in os.walk(dir_path, topdown=True, followlinks=False):
        # 过滤掉隐藏/缓存目录，但保留 .github
        dirs[:] = [d for d in dirs if d not in skip_dirs and (d == ".github" or not d.startswith("."))]
        
        for name in files:
            file_path = Path(name)
            if file_path.suffix.lower() in extensions:
                yield Path(root) / name 


def collect_files(inputs: List[str], extensions: Set[str] = None) -> List[Path]:
    if extensions is None:
        extensions = {".py", ".yaml", ".yml", ".md", ".jsonl"}
    
    seen: Set[Path] = set()
    result: List[Path] = []

    for raw in inputs:
        p = Path(raw)
        if not p.exists():
            print(f"[警告] 路径不存在：{raw}", file=sys.stderr)
            continue

        if p.is_dir():
            for fp in iter_code_files_in_dir(p, extensions):
                try:
                    abspath = fp.resolve(strict=True)
                except Exception:
                    continue
                if abspath not in seen:
                    seen.add(abspath)
                    result.append(abspath)
        else:
            try:
                abspath = p.resolve(strict=True)
            except Exception:
                print(f"[警告] 无法解析文件：{p}", file=sys.stderr)
                continue
            if abspath not in seen:
                seen.add(abspath)
                result.append(abspath)
    result.sort(key=lambda x: str(x))
    return result


def read_text_best_effort(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("utf-8", "gb18030", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def write_prompts(file_paths: List[Path], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with output_path.open("w", encoding="utf-8", newline="\n") as out:
        first_block = True
        for p in file_paths:
            try:
                content = read_text_best_effort(p)
            except Exception as e:
                print(f"[跳过] 读取失败：{p} （{e}）", file=sys.stderr)
                continue

            if not first_block:
                out.write("\n")
            first_block = False

            out.write(f"{str(p)} code 内容如下:\n")
            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")
            count += 1

    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从指定文件/目录生成 AI 读取用的代码 prompt 文本"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="文件或目录路径。目录将递归收集指定扩展名的文件；文件将直接纳入（不限制扩展名）。"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"输出文件路径（默认：{DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "-e", "--extensions",
        nargs="*",
        default=[".py", ".yaml", ".yml", ".md", ".jsonl"],
        help="要处理的文件扩展名（默认：.py .yaml .yml .md .jsonl）"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    extensions = set(ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions)
    files = collect_files(args.paths, extensions)

    if not files:
        print("[提示] 未找到可处理的文件。", file=sys.stderr)
        sys.exit(1)

    print(f"[信息] 找到 {len(files)} 个文件:", file=sys.stderr)
    for f in files:
        print(f"  - {f}", file=sys.stderr)

    written = write_prompts(files, args.output)
    print(f"[完成] 已写入 {written} 个 prompt 块 -> {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()