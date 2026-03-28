from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "metadata" / "candidates"

QUERIES = {
    "image-2d": [
        "text-to-image",
        "image editing diffusion",
        "diffusion transformer image generation",
    ],
    "video": [
        "text-to-video",
        "image-to-video",
        "video editing diffusion",
    ],
    "3d-object-asset": [
        "text-to-3D",
        "image-to-3D",
        "3D shape generation",
    ],
    "3d-scene": [
        "3D scene generation",
        "indoor scene generation",
        "layout guided 3D scene",
    ],
    "4d-dynamic-scene-world": [
        "world model",
        "autonomous driving world model",
        "4D generation",
    ],
}


def arxiv_query(terms: list[str]) -> str:
    return " OR ".join(f'all:"{term}"' for term in terms)


def fetch_arxiv_entries(query: str, max_results: int = 25) -> list[dict]:
    url = (
        "http://export.arxiv.org/api/query?search_query="
        + quote(query)
        + f"&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    )
    req = Request(url, headers={"User-Agent": "awesome-generative-models/1.0"})
    with urlopen(req, timeout=30) as resp:
        xml_bytes = resp.read()

    root = ET.fromstring(xml_bytes)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    items = []
    for entry in root.findall("atom:entry", ns):
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split())
        summary = " ".join((entry.findtext("atom:summary", default="", namespaces=ns) or "").split())
        link = entry.findtext("atom:id", default="", namespaces=ns) or ""
        published = entry.findtext("atom:published", default="", namespaces=ns) or ""
        items.append(
            {
                "title": title,
                "summary": summary,
                "link": link,
                "published": published,
            }
        )
    return items


def dedupe(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for item in items:
        key = item["title"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def clean_cell(text: str, limit: int = 160) -> str:
    text = text.replace("|", "\\|").replace("\n", " ").strip()
    if len(text) > limit:
        return text[: limit - 1] + "…"
    return text


def build_report() -> str:
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=21)

    lines = [
        "# Daily candidate papers",
        "",
        "> Auto-generated from arXiv query feeds. **Manual review is required before adding anything to `data/*.jsonl`.**",
        "",
        f"- Generated at (UTC): `{now.strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- Candidate window: last `21` days",
        "",
    ]

    all_count = 0
    for area, terms in QUERIES.items():
        query = arxiv_query(terms)
        try:
            items = fetch_arxiv_entries(query)
        except Exception as exc:
            lines.extend(
                [
                    f"## {area}",
                    "",
                    f"- Fetch failed: `{exc}`",
                    "",
                ]
            )
            continue

        filtered = []
        for item in dedupe(items):
            try:
                published = datetime.fromisoformat(item["published"].replace("Z", "+00:00"))
            except Exception:
                continue
            if published >= since:
                item["published_dt"] = published
                filtered.append(item)

        filtered.sort(key=lambda x: x["published_dt"], reverse=True)
        all_count += len(filtered)

        lines.extend([f"## {area}", ""])
        if not filtered:
            lines.extend(["- No candidates in the last 21 days.", ""])
            continue

        lines.extend(
            [
                "| Date (UTC) | Title | Note |",
                "|---|---|---|",
            ]
        )
        for item in filtered:
            lines.append(
                f"| {item['published_dt'].strftime('%Y-%m-%d')} | "
                f"[{clean_cell(item['title'], 120)}]({item['link']}) | "
                f"{clean_cell(item['summary'])} |"
            )
        lines.append("")

    if all_count == 0:
        lines.extend(
            [
                "## Note",
                "",
                "No recent candidates were harvested. This may mean either:",
                "",
                "- there are genuinely no matching recent submissions, or",
                "- the feed query needs tuning.",
                "",
            ]
        )

    return "\n".join(lines)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (OUT_DIR / "latest.md").write_text(report.rstrip() + "\n", encoding="utf-8")
    (OUT_DIR / f"{today}.md").write_text(report.rstrip() + "\n", encoding="utf-8")
    print("[fetch_candidates] wrote metadata/candidates/latest.md")


if __name__ == "__main__":
    main()