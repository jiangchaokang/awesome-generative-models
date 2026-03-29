#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from catalog_common import (
    ALLOWED_TASKS,
    ARTIFACT_META,
    CONDITIONING_VOCAB,
    DOMAIN_VOCAB,
    FILE_ARTIFACT,
    METHOD_VOCAB,
    REPRESENTATION_VOCAB,
    ROOT,
    arxiv_year_from_url,
    has_cjk,
    load_records,
    normalize_title,
    normalize_whitespace,
    parse_github_repo,
    sentence_count,
    slugify,
)

CACHE_DIR = ROOT / "metadata" / "cache"
VALIDATION_DIR = ROOT / "metadata" / "validation"
BACKUP_ROOT = VALIDATION_DIR / "backups"

SEARCH_URL_TOKENS = [
    "scholar.google.com",
    "github.com/search",
    "google.com/search",
    "bing.com/search",
]

SOFT_FAIL_DOMAINS = {
    "openreview.net",
    "proceedings.iclr.cc",
    "openaccess.thecvf.com",
    "www.openaccess.thecvf.com",
}

GITHUB_API_SOFT_CODES = {401, 403, 404, 429}


def location(rec: dict) -> str:
    meta = ARTIFACT_META[rec["artifact"]]
    return f'{meta["dir"]}/{rec["id"]} ({rec["_source_file"]}:{rec["_lineno"]})'


def record_key(rec: dict) -> tuple[str, int]:
    return rec["_source_file"], int(rec["_lineno"])


def is_search_placeholder(url: str) -> bool:
    lowered = (url or "").lower()
    return any(token in lowered for token in SEARCH_URL_TOKENS)


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def make_request(url: str, accept: str = "application/json,text/html,*/*") -> Request:
    return Request(
        url,
        headers={
            "User-Agent": "awesome-generative-models/4.0",
            "Accept": accept,
            "Cache-Control": "no-cache",
        },
    )


def http_probe(url: str, timeout: int = 20, retries: int = 1) -> dict:
    domain = urlparse(url).netloc.lower()
    last_soft_warning: dict | None = None

    for _ in range(retries + 1):
        try:
            with urlopen(make_request(url), timeout=timeout) as response:
                response.read(256)
                return {
                    "ok": True,
                    "status": int(getattr(response, "status", 200) or 200),
                    "final_url": response.geturl(),
                }
        except HTTPError as exc:
            if exc.code in {403, 429}:
                return {
                    "ok": True,
                    "status": exc.code,
                    "final_url": getattr(exc, "url", url),
                    "warning": f"HTTP {exc.code}: blocked by the remote host, but the URL may still be valid.",
                }
            if exc.code in {500, 502, 503, 504} and domain in SOFT_FAIL_DOMAINS:
                last_soft_warning = {
                    "ok": True,
                    "status": exc.code,
                    "final_url": url,
                    "warning": f"HTTP {exc.code}: transient upstream failure on {domain}; treating as soft warning.",
                }
                continue
            return {"ok": False, "status": exc.code, "final_url": url, "error": f"HTTP {exc.code}"}
        except URLError as exc:
            return {"ok": False, "status": 0, "final_url": url, "error": str(exc.reason)}
        except Exception as exc:
            return {"ok": False, "status": 0, "final_url": url, "error": str(exc)}

    if last_soft_warning:
        return last_soft_warning
    return {"ok": False, "status": 0, "final_url": url, "error": "Unknown network error"}


def parse_star_count(html: str) -> int:
    patterns = [
        re.compile(r'([\d,]+)\s+stars', re.I),
        re.compile(r'"stargazerCount":\s*([0-9]+)', re.I),
    ]
    for pattern in patterns:
        match = pattern.search(html)
        if match:
            try:
                return int(match.group(1).replace(",", ""))
            except Exception:
                pass
    return 0


def github_repo_html_meta(url: str, timeout: int = 20) -> dict:
    full_name = parse_github_repo(url)
    if not full_name:
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "error": "Repo URL is not a canonical GitHub repository URL.",
        }

    try:
        with urlopen(make_request(url, accept="text/html,*/*"), timeout=timeout) as response:
            html = response.read(400_000).decode("utf-8", errors="ignore")
            final_url = response.geturl()
            final_full_name = parse_github_repo(final_url) or full_name
            archived = "This repository was archived by the owner" in html
            return {
                "ok": True,
                "status": int(getattr(response, "status", 200) or 200),
                "final_url": final_url,
                "full_name": final_full_name,
                "stars": parse_star_count(html),
                "pushed_at": "",
                "archived": archived,
                "license": "",
            }
    except HTTPError as exc:
        if exc.code in {403, 429}:
            return {
                "ok": True,
                "status": exc.code,
                "final_url": getattr(exc, "url", url),
                "full_name": full_name,
                "stars": 0,
                "pushed_at": "",
                "archived": False,
                "license": "",
                "warning": f"GitHub HTML probe HTTP {exc.code}; repo may still be valid.",
            }
        return {
            "ok": False,
            "status": exc.code,
            "final_url": url,
            "full_name": full_name,
            "error": f"GitHub HTML HTTP {exc.code}",
        }
    except URLError as exc:
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "full_name": full_name,
            "error": str(exc.reason),
        }
    except Exception as exc:
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "full_name": full_name,
            "error": str(exc),
        }


def github_repo_meta(url: str, token: str, timeout: int = 20) -> dict:
    full_name = parse_github_repo(url)
    if not full_name:
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "error": "Repo URL is not a canonical GitHub repository URL.",
        }

    api_url = f"https://api.github.com/repos/{full_name}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-generative-models/4.0",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(api_url, headers=headers)

    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "ok": True,
                "status": int(getattr(response, "status", 200) or 200),
                "final_url": url,
                "full_name": data.get("full_name", full_name),
                "stars": int(data.get("stargazers_count", 0) or 0),
                "pushed_at": data.get("pushed_at", ""),
                "archived": bool(data.get("archived", False)),
                "license": (data.get("license") or {}).get("spdx_id", ""),
            }
    except HTTPError as exc:
        if exc.code in GITHUB_API_SOFT_CODES:
            fallback = github_repo_html_meta(url, timeout=timeout)
            if fallback["ok"]:
                fallback["warning"] = f"GitHub API HTTP {exc.code}; validated via HTML fallback."
                return fallback
        return {
            "ok": False,
            "status": exc.code,
            "final_url": url,
            "full_name": full_name,
            "error": f"GitHub API HTTP {exc.code}",
        }
    except URLError:
        fallback = github_repo_html_meta(url, timeout=timeout)
        if fallback["ok"]:
            fallback["warning"] = "GitHub API unreachable; validated via HTML fallback."
            return fallback
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "full_name": full_name,
            "error": "GitHub API unreachable and HTML fallback failed",
        }
    except Exception as exc:
        fallback = github_repo_html_meta(url, timeout=timeout)
        if fallback["ok"]:
            fallback["warning"] = f"GitHub API exception ({exc}); validated via HTML fallback."
            return fallback
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "full_name": full_name,
            "error": str(exc),
        }


def validate_record_schema(rec: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in ("id", "title", "venue", "task", "summary"):
        if not rec.get(field):
            errors.append(f"{location(rec)}: missing required field `{field}`.")

    if rec.get("task") and rec["task"] not in ALLOWED_TASKS[rec["artifact"]]:
        allowed = ", ".join(sorted(ALLOWED_TASKS[rec["artifact"]]))
        errors.append(
            f"{location(rec)}: task `{rec['task']}` is not allowed for `{rec['artifact']}`. Allowed: {allowed}."
        )

    unknown_domains = [x for x in rec["domain"] if x not in DOMAIN_VOCAB]
    unknown_repr = [x for x in rec["representation"] if x not in REPRESENTATION_VOCAB]
    unknown_methods = [x for x in rec["method"] if x not in METHOD_VOCAB]
    unknown_cond = [x for x in rec["conditioning"] if x not in CONDITIONING_VOCAB]

    if unknown_domains:
        errors.append(f"{location(rec)}: unknown domain tags: {unknown_domains}.")
    if unknown_repr:
        errors.append(f"{location(rec)}: unknown representation tags: {unknown_repr}.")
    if unknown_methods:
        errors.append(f"{location(rec)}: unknown method tags: {unknown_methods}.")
    if unknown_cond:
        errors.append(f"{location(rec)}: unknown conditioning tags: {unknown_cond}.")

    for text_field in ("title", "venue", "summary", "task", "scope_note"):
        if has_cjk(rec.get(text_field, "")):
            errors.append(f"{location(rec)}: `{text_field}` must be English-only.")

    for tag_field in ("domain", "representation", "method", "conditioning", "orgs"):
        joined = " ".join(rec.get(tag_field, []))
        if has_cjk(joined):
            errors.append(f"{location(rec)}: `{tag_field}` must be English-only.")

    summary_sentences = sentence_count(rec.get("summary", ""))
    if summary_sentences < 1 or summary_sentences > 3:
        errors.append(f"{location(rec)}: `summary` must contain 1–3 English sentences; found {summary_sentences}.")

    if rec["year"] and rec["year"] < 2025:
        if rec.get("active_since", 0) < 2025:
            errors.append(f"{location(rec)}: pre-2025 entry must have `active_since >= 2025`.")
        if not rec.get("scope_note"):
            errors.append(f"{location(rec)}: pre-2025 entry must have a non-empty `scope_note`.")

    if rec.get("open_source") and not rec.get("repo"):
        errors.append(f"{location(rec)}: `open_source: true` requires an exact `repo` URL.")

    if not any([rec.get("paper"), rec.get("repo"), rec.get("homepage")]):
        errors.append(f"{location(rec)}: at least one exact link among `paper`, `repo`, or `homepage` is required.")

    for link_field in ("paper", "repo", "homepage"):
        url = rec.get(link_field, "")
        if url and is_search_placeholder(url):
            errors.append(f"{location(rec)}: `{link_field}` cannot be a search-result URL: {url}")

    if rec.get("paper") and "arxiv.org" in rec["paper"].lower() and "arxiv" in rec["venue"].lower():
        arxiv_year = arxiv_year_from_url(rec["paper"])
        if arxiv_year and rec["year"] and arxiv_year != rec["year"]:
            errors.append(
                f"{location(rec)}: venue year `{rec['year']}` does not match arXiv paper year `{arxiv_year}`."
            )

    if not rec.get("paper"):
        warnings.append(f"{location(rec)}: missing `paper` link.")
    if rec.get("featured") and not rec.get("orgs"):
        warnings.append(f"{location(rec)}: featured entries should include `orgs`.")
    if rec.get("open_source") and rec.get("repo") and not parse_github_repo(rec["repo"]):
        warnings.append(f"{location(rec)}: open-source repo is not a canonical GitHub repo URL; verify manually.")

    return errors, warnings


def validate_duplicates(records: list[dict]) -> tuple[list[str], set[tuple[str, int]]]:
    errors: list[str] = []
    invalid_keys: set[tuple[str, int]] = set()

    seen_ids: dict[str, str] = {}
    seen_titles: dict[str, str] = {}
    seen_papers: dict[str, str] = {}
    seen_repos: dict[str, str] = {}

    for rec in records:
        rloc = location(rec)
        rkey = record_key(rec)

        rid = rec["id"]
        if rid in seen_ids:
            errors.append(f"{rloc}: duplicate id with {seen_ids[rid]}.")
            invalid_keys.add(rkey)
        else:
            seen_ids[rid] = rloc

        title_key = normalize_title(rec["title"])
        if title_key in seen_titles:
            errors.append(f"{rloc}: duplicate normalized title with {seen_titles[title_key]}.")
            invalid_keys.add(rkey)
        else:
            seen_titles[title_key] = rloc

        if rec.get("paper"):
            paper_key = rec["paper"].rstrip("/")
            if paper_key in seen_papers:
                errors.append(f"{rloc}: duplicate paper URL with {seen_papers[paper_key]}.")
                invalid_keys.add(rkey)
            else:
                seen_papers[paper_key] = rloc

        if rec.get("repo"):
            repo_key = parse_github_repo(rec["repo"]) or rec["repo"].rstrip("/")
            if repo_key in seen_repos:
                errors.append(f"{rloc}: duplicate repo URL with {seen_repos[repo_key]}.")
                invalid_keys.add(rkey)
            else:
                seen_repos[repo_key] = rloc

    return errors, invalid_keys


def verify_links(
    records: list[dict],
    token: str,
    timeout: int,
    skip_network: bool,
) -> tuple[list[str], list[str], dict, dict, set[tuple[str, int]]]:
    errors: list[str] = []
    warnings: list[str] = []
    repo_stats: dict[str, dict] = {}
    link_report: dict[str, dict] = {}
    invalid_keys: set[tuple[str, int]] = set()

    if skip_network:
        return errors, warnings, repo_stats, link_report, invalid_keys

    for rec in records:
        rloc = location(rec)
        rkey = record_key(rec)
        report_item: dict[str, dict] = {}

        if rec.get("paper"):
            paper_probe = http_probe(rec["paper"], timeout=timeout, retries=1)
            report_item["paper"] = paper_probe
            if not paper_probe["ok"]:
                errors.append(f"{rloc}: paper URL failed validation: {paper_probe['error']}")
                invalid_keys.add(rkey)
            elif paper_probe.get("warning"):
                warnings.append(f"{rloc}: paper URL warning: {paper_probe['warning']}")

        if rec.get("repo"):
            if parse_github_repo(rec["repo"]):
                repo_probe = github_repo_meta(rec["repo"], token=token, timeout=timeout)
            else:
                repo_probe = http_probe(rec["repo"], timeout=timeout, retries=1)

            report_item["repo"] = repo_probe
            if not repo_probe["ok"]:
                errors.append(f"{rloc}: repo URL failed validation: {repo_probe['error']}")
                invalid_keys.add(rkey)
            else:
                if repo_probe.get("warning"):
                    warnings.append(f"{rloc}: repo URL warning: {repo_probe['warning']}")
                if repo_probe.get("full_name"):
                    repo_stats[repo_probe["full_name"]] = {
                        "stars": int(repo_probe.get("stars", 0) or 0),
                        "pushed_at": repo_probe.get("pushed_at", ""),
                        "archived": bool(repo_probe.get("archived", False)),
                        "license": repo_probe.get("license", ""),
                    }
                    if repo_probe.get("archived"):
                        warnings.append(f"{rloc}: repository is archived.")

        if rec.get("homepage"):
            home_probe = http_probe(rec["homepage"], timeout=timeout, retries=1)
            report_item["homepage"] = home_probe
            if not home_probe["ok"]:
                errors.append(f"{rloc}: homepage URL failed validation: {home_probe['error']}")
                invalid_keys.add(rkey)
            elif home_probe.get("warning"):
                warnings.append(f"{rloc}: homepage URL warning: {home_probe['warning']}")

        link_report[rloc] = report_item

    return errors, warnings, repo_stats, link_report, invalid_keys


def run_validation_pass(
    records: list[dict],
    token: str,
    timeout: int,
    skip_network: bool,
) -> tuple[list[str], list[str], dict, dict, set[tuple[str, int]]]:
    errors: list[str] = []
    warnings: list[str] = []
    invalid_keys: set[tuple[str, int]] = set()

    for rec in records:
        rec_errors, rec_warnings = validate_record_schema(rec)
        errors.extend(rec_errors)
        warnings.extend(rec_warnings)
        if rec_errors:
            invalid_keys.add(record_key(rec))

    dup_errors, dup_invalid = validate_duplicates(records)
    errors.extend(dup_errors)
    invalid_keys |= dup_invalid

    link_errors, link_warnings, repo_stats, link_report, link_invalid = verify_links(
        records=records,
        token=token,
        timeout=timeout,
        skip_network=skip_network,
    )
    errors.extend(link_errors)
    warnings.extend(link_warnings)
    invalid_keys |= link_invalid

    return errors, warnings, repo_stats, link_report, invalid_keys


def render_report(records: list[dict], errors: list[str], warnings: list[str], repo_stats: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Validation Report",
        "",
        f"- Generated: `{now}`",
        f"- Records checked: **{len(records)}**",
        f"- Blocking errors: **{len(errors)}**",
        f"- Warnings: **{len(warnings)}**",
        "",
        "## Blocking Errors",
        "",
    ]
    if errors:
        lines.extend([f"- {item}" for item in errors])
    else:
        lines.append("- None.")
    lines.extend(["", "## Warnings", ""])
    if warnings:
        lines.extend([f"- {item}" for item in warnings])
    else:
        lines.append("- None.")
    lines.extend(["", "## Refreshed GitHub Repo Stats", ""])
    if repo_stats:
        lines.extend(["| Repo | Stars | Last Push | Archived | License |", "|:--|--:|:--|:--:|:--|"])
        for full_name, stats in sorted(
            repo_stats.items(),
            key=lambda item: (-int(item[1].get("stars", 0)), item[0].lower()),
        ):
            lines.append(
                f"| `{full_name}` | {int(stats.get('stars', 0))} | {stats.get('pushed_at', '')[:10]} | "
                f"{'Yes' if stats.get('archived') else 'No'} | {stats.get('license', '') or '—'} |"
            )
    else:
        lines.append("- No GitHub repo stats were refreshed.")
    lines.append("")
    return "\n".join(lines)


def prompt_yes_no(question: str) -> bool:
    try:
        answer = input(question).strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes"}


def prune_invalid_records(invalid_keys: set[tuple[str, int]]) -> tuple[Path, dict[str, int]]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / timestamp / "data"
    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "data", backup_dir, dirs_exist_ok=True)

    removed_counts: dict[str, int] = defaultdict(int)

    for file_name in FILE_ARTIFACT:
        path = ROOT / "data" / file_name
        if not path.exists():
            continue

        kept_lines: list[str] = []
        with path.open("r", encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    kept_lines.append(line.rstrip("\n"))
                    continue

                if (file_name, lineno) in invalid_keys:
                    removed_counts[file_name] += 1
                    continue

                kept_lines.append(line.rstrip("\n"))

        path.write_text("\n".join(kept_lines).rstrip() + "\n", encoding="utf-8")

    return backup_dir, dict(removed_counts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate catalog data and exact links.")
    parser.add_argument("--skip-network", action="store_true", help="Skip URL / GitHub API verification.")
    parser.add_argument("--write-cache", action="store_true", help="Write link and repo caches.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout in seconds.")
    parser.add_argument("--interactive-clean", action="store_true", help="Prompt to prune invalid rows after reporting errors.")
    parser.add_argument("--prune-invalid", action="store_true", help="Prune invalid rows without prompting, then re-run validation.")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN", "").strip()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

    def persist(records: list[dict], errors: list[str], warnings: list[str], repo_stats: dict, link_report: dict, invalid_keys: set[tuple[str, int]]) -> None:
        report = render_report(records, errors, warnings, repo_stats)
        (VALIDATION_DIR / "latest.md").write_text(report.rstrip() + "\n", encoding="utf-8")
        if args.write_cache:
            write_json(CACHE_DIR / "repo_stats.json", repo_stats)
            write_json(CACHE_DIR / "link_report.json", link_report)
            write_json(
                CACHE_DIR / "invalid_records.json",
                {
                    "records": [
                        {"source_file": sf, "lineno": ln}
                        for sf, ln in sorted(invalid_keys)
                    ]
                },
            )

    records = load_records()
    errors, warnings, repo_stats, link_report, invalid_keys = run_validation_pass(
        records=records,
        token=token,
        timeout=args.timeout,
        skip_network=args.skip_network,
    )
    persist(records, errors, warnings, repo_stats, link_report, invalid_keys)

    print(f"[validate] records={len(records)} errors={len(errors)} warnings={len(warnings)}")
    if errors:
        print("\n[validate] blocking errors:")
        for item in errors:
            print(f"  - {item}")
    if warnings:
        print("\n[validate] warnings:")
        for item in warnings:
            print(f"  - {item}")

    should_prune = False
    if errors and args.prune_invalid:
        should_prune = True
    elif errors and args.interactive_clean and sys.stdin.isatty():
        should_prune = prompt_yes_no("\nPrune invalid rows now? [y/N]: ")

    if should_prune and invalid_keys:
        backup_dir, removed = prune_invalid_records(invalid_keys)
        print(f"\n[validate] pruned invalid rows. Backup written to: {backup_dir}")
        for file_name, count in sorted(removed.items()):
            print(f"  - {file_name}: removed {count}")

        records = load_records()
        errors, warnings, repo_stats, link_report, invalid_keys = run_validation_pass(
            records=records,
            token=token,
            timeout=args.timeout,
            skip_network=args.skip_network,
        )
        persist(records, errors, warnings, repo_stats, link_report, invalid_keys)
        print(f"\n[validate] after prune -> records={len(records)} errors={len(errors)} warnings={len(warnings)}")

    if errors:
        print("[validate] blocking errors found. See metadata/validation/latest.md", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()