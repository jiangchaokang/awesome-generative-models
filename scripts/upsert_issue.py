#!/usr/bin/env python3
"""Create or update a deduplicated GitHub Issue by exact title and label.

Never prints any token. Gracefully exits 0 on API errors so scheduled jobs
never turn red due to Issue API hiccups.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

USER_AGENT = "awesome-generative-models/6.0"


def _github_request(
    method: str,
    url: str,
    token: str,
    payload: dict | None = None,
) -> tuple[int, dict | list | None]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            return int(getattr(resp, "status", 200) or 200), json.loads(body) if body else None
    except HTTPError as exc:
        return int(exc.code or 0), None
    except (URLError, TimeoutError, OSError):
        return 0, None


def upsert_issue(
    *,
    repo: str,
    title: str,
    label: str,
    body: str,
    token: str,
) -> str:
    base = f"https://api.github.com/repos/{repo}"
    query = urlencode({"state": "open", "labels": label, "per_page": 50})
    status, issues = _github_request("GET", f"{base}/issues?{query}", token)
    if status == 200 and isinstance(issues, list):
        for issue in issues:
            if isinstance(issue, dict) and issue.get("title") == title and "pull_request" not in issue:
                number = issue["number"]
                _github_request("PATCH", f"{base}/issues/{number}", token, {"body": body})
                return f"updated:#{number}"

    # Ensure label exists (ignore error if already exists)
    _github_request("POST", f"{base}/labels", token, {"name": label, "color": "D93F0B"})

    c_status, created = _github_request(
        "POST",
        f"{base}/issues",
        token,
        {"title": title, "body": body, "labels": [label]},
    )
    if c_status in {200, 201} and isinstance(created, dict):
        return f"created:#{created.get('number')}"
    return f"skipped:http_{c_status}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or update a deduplicated GitHub Issue.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file", type=Path, default=None)
    args = parser.parse_args()

    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    token = (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or "").strip()
    if not repo or not token:
        print("[upsert-issue] GITHUB_REPOSITORY or GITHUB_TOKEN not set; skipping.")
        return 0

    body = args.body
    if args.body_file and args.body_file.exists():
        body = args.body_file.read_text(encoding="utf-8")

    result = upsert_issue(repo=repo, title=args.title, label=args.label, body=body, token=token)
    print(f"[upsert-issue] {result} ({args.title})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
