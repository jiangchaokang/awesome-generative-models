#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from catalog_common import (
    ARTIFACT_META,
    ROOT,
    load_records,
    parse_github_repo,
)

OUTPUT_DIR = ROOT / "docs" / "explorer"
REPO_STATS_FILE = ROOT / "metadata" / "cache" / "repo_stats.json"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def read_repo_stats() -> dict:
    if not REPO_STATS_FILE.exists():
        return {}

    try:
        return json.loads(REPO_STATS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def public_record(record: dict, repo_stats: dict) -> dict:
    repository = parse_github_repo(record.get("repo", ""))
    stats = repo_stats.get(repository, {}) if repository else {}

    return {
        "id": record["id"],
        "title": record["title"],
        "summary": record["summary"],
        "artifact": record["artifact"],
        "artifact_title": ARTIFACT_META[record["artifact"]]["title"],
        "task": record.get("task", ""),
        "venue": record.get("venue", ""),
        "year": int(record.get("year", 0) or 0),
        "published_at": record.get("published_at", ""),
        "domain": record.get("domain", []),
        "representation": record.get("representation", []),
        "method": record.get("method", []),
        "conditioning": record.get("conditioning", []),
        "orgs": record.get("orgs", []),
        "paper": record.get("paper", ""),
        "repo": record.get("repo", ""),
        "homepage": record.get("homepage", ""),
        "open_source": bool(record.get("open_source", False)),
        "featured": bool(record.get("featured", False)),
        "stars": int(stats.get("stars", record.get("stars", 0)) or 0),
    }


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description"
        content="Search and filter recent generative-model research.">
  <title>Awesome Generative Models Explorer</title>
  <link rel="stylesheet" href="styles.css">
  <script src="app.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#results">Skip to results</a>

  <header class="hero">
    <div class="hero-inner">
      <p class="eyebrow">Research catalog</p>
      <h1>Awesome Generative Models</h1>
      <p class="hero-copy">
        Search recent work across image, video, 3D assets,
        3D scenes, and interactive 4D worlds.
      </p>
      <div class="hero-links">
        <a href="https://github.com/jiangchaokang/awesome-generative-models">
          GitHub repository
        </a>
        <a href="https://github.com/jiangchaokang/awesome-generative-models/blob/main/CONTRIBUTING.md">
          Contribute
        </a>
      </div>
      <p id="catalog-status" class="catalog-status" aria-live="polite"></p>
    </div>
  </header>

  <main>
    <section class="controls" aria-label="Catalog filters">
      <label class="search-field">
        <span>Search</span>
        <input id="query"
               type="search"
               placeholder="Title, summary, organization, method…"
               autocomplete="off">
      </label>

      <label>
        <span>Artifact</span>
        <select id="artifact">
          <option value="">All artifacts</option>
        </select>
      </label>

      <label>
        <span>Task</span>
        <select id="task">
          <option value="">All tasks</option>
        </select>
      </label>

      <label>
        <span>Domain</span>
        <select id="domain">
          <option value="">All domains</option>
        </select>
      </label>

      <label>
        <span>Method</span>
        <select id="method">
          <option value="">All methods</option>
        </select>
      </label>

      <label>
        <span>Organization</span>
        <select id="organization">
          <option value="">All organizations</option>
        </select>
      </label>

      <label>
        <span>Sort</span>
        <select id="sort">
          <option value="newest">Newest first</option>
          <option value="featured">Featured first</option>
          <option value="stars">Most GitHub stars</option>
          <option value="title">Title A–Z</option>
        </select>
      </label>

      <label class="checkbox-field">
        <input id="open-source" type="checkbox">
        <span>Open source only</span>
      </label>

      <button id="reset" type="button">Reset filters</button>
    </section>

    <section class="results-header">
      <h2 id="result-count">Loading catalog…</h2>
    </section>

    <section id="results"
             class="result-grid"
             aria-live="polite"
             aria-busy="true"></section>

    <div class="load-more-wrap">
      <button id="load-more" type="button" hidden>Load more</button>
    </div>
  </main>

  <footer>
    <p>
      Exact links are validated automatically, but final catalog inclusion
      remains human-reviewed.
    </p>
  </footer>
</body>
</html>
"""


CSS = """
:root {
  color-scheme: light dark;
  --background: #f6f8fb;
  --surface: #ffffff;
  --surface-muted: #eef2f7;
  --text: #172033;
  --muted: #5d687a;
  --border: #d9e0ea;
  --primary: #3157d5;
  --primary-hover: #2444b5;
  --featured: #f59e0b;
  --shadow: 0 12px 32px rgba(19, 33, 68, 0.08);
  --radius: 16px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #0d1117;
    --surface: #161b22;
    --surface-muted: #21262d;
    --text: #e6edf3;
    --muted: #9da7b3;
    --border: #30363d;
    --primary: #7c9cff;
    --primary-hover: #a8bcff;
    --shadow: none;
  }
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--background);
  color: var(--text);
  font-family:
    Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", sans-serif;
  line-height: 1.6;
}

a {
  color: var(--primary);
}

button,
input,
select {
  font: inherit;
}

.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
}

.skip-link:focus {
  left: 1rem;
  top: 1rem;
  z-index: 100;
  padding: 0.75rem 1rem;
  background: var(--surface);
  border-radius: 8px;
}

.hero {
  color: white;
  background:
    radial-gradient(circle at 85% 15%, rgba(98, 126, 255, 0.8), transparent 28%),
    linear-gradient(135deg, #101b46, #244fc4 62%, #3d69e8);
}

.hero-inner {
  width: min(1180px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 4.5rem 0 4rem;
}

.eyebrow {
  margin: 0;
  color: #c8d5ff;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1 {
  max-width: 850px;
  margin: 0.4rem 0 0;
  font-size: clamp(2.5rem, 7vw, 5rem);
  line-height: 1.05;
}

.hero-copy {
  max-width: 720px;
  margin: 1.25rem 0;
  color: #e5ebff;
  font-size: 1.15rem;
}

.hero-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.hero-links a {
  padding: 0.7rem 1rem;
  color: white;
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
}

.catalog-status {
  min-height: 1.5rem;
  margin-top: 1rem;
  color: #cdd8ff;
}

main {
  width: min(1180px, calc(100% - 2rem));
  margin: -1.75rem auto 4rem;
}

.controls {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1rem;
  padding: 1.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.controls label {
  display: grid;
  gap: 0.4rem;
  color: var(--muted);
  font-size: 0.85rem;
  font-weight: 700;
}

.search-field {
  grid-column: span 2;
}

input[type="search"],
select {
  width: 100%;
  min-height: 44px;
  padding: 0.65rem 0.75rem;
  color: var(--text);
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 10px;
}

.checkbox-field {
  display: flex !important;
  align-items: center;
  gap: 0.6rem !important;
  min-height: 44px;
  align-self: end;
}

.checkbox-field input {
  width: 1.1rem;
  height: 1.1rem;
}

button {
  min-height: 44px;
  align-self: end;
  padding: 0.65rem 1rem;
  color: white;
  cursor: pointer;
  background: var(--primary);
  border: 0;
  border-radius: 10px;
  font-weight: 700;
}

button:hover {
  background: var(--primary-hover);
}

.results-header {
  display: flex;
  justify-content: space-between;
  margin: 2rem 0 1rem;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.paper-card {
  display: flex;
  flex-direction: column;
  min-width: 0;
  padding: 1.35rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.paper-card.featured {
  border-color: var(--featured);
}

.card-heading {
  margin: 0;
  font-size: 1.2rem;
  line-height: 1.35;
}

.card-heading a {
  color: var(--text);
  text-decoration: none;
}

.card-heading a:hover {
  color: var(--primary);
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin: 0.8rem 0;
}

.badge {
  padding: 0.2rem 0.55rem;
  color: var(--muted);
  background: var(--surface-muted);
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
}

.badge-featured {
  color: #1f2937;
  background: #fbbf24;
}

.summary {
  flex: 1;
  color: var(--muted);
}

.card-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  margin-top: 1rem;
}

.card-links a {
  padding: 0.45rem 0.7rem;
  text-decoration: none;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
}

.load-more-wrap {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
}

.empty-state {
  grid-column: 1 / -1;
  padding: 3rem;
  text-align: center;
  color: var(--muted);
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

footer {
  padding: 2rem 1rem;
  text-align: center;
  color: var(--muted);
  border-top: 1px solid var(--border);
}

@media (max-width: 900px) {
  .controls {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .result-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 560px) {
  .hero-inner {
    padding: 3rem 0;
  }

  main {
    width: min(100% - 1rem, 1180px);
  }

  .controls {
    grid-template-columns: 1fr;
  }

  .search-field {
    grid-column: auto;
  }
}
"""


JS = """
const PAGE_SIZE = 48;

const elements = {
  query: document.querySelector("#query"),
  artifact: document.querySelector("#artifact"),
  task: document.querySelector("#task"),
  domain: document.querySelector("#domain"),
  method: document.querySelector("#method"),
  organization: document.querySelector("#organization"),
  sort: document.querySelector("#sort"),
  openSource: document.querySelector("#open-source"),
  reset: document.querySelector("#reset"),
  results: document.querySelector("#results"),
  resultCount: document.querySelector("#result-count"),
  loadMore: document.querySelector("#load-more"),
  catalogStatus: document.querySelector("#catalog-status"),
};

let records = [];
let visibleCount = PAGE_SIZE;

function arrayValues(key) {
  return [...new Set(records.flatMap((record) => record[key] || []))]
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b));
}

function scalarValues(key) {
  return [...new Set(records.map((record) => record[key]))]
    .filter(Boolean)
    .sort((a, b) => String(a).localeCompare(String(b)));
}

function appendOptions(select, values, labels = {}) {
  for (const value of values) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = labels[value] || value;
    select.append(option);
  }
}

function searchableText(record) {
  return [
    record.title,
    record.summary,
    record.venue,
    record.task,
    ...(record.domain || []),
    ...(record.method || []),
    ...(record.representation || []),
    ...(record.conditioning || []),
    ...(record.orgs || []),
  ].join(" ").toLowerCase();
}

function recordDate(record) {
  return record.published_at || `${record.year || 0}-01-01`;
}

function selectedRecords() {
  const query = elements.query.value.trim().toLowerCase();
  const artifact = elements.artifact.value;
  const task = elements.task.value;
  const domain = elements.domain.value;
  const method = elements.method.value;
  const organization = elements.organization.value;
  const openSource = elements.openSource.checked;

  const filtered = records.filter((record) => {
    if (query && !searchableText(record).includes(query)) return false;
    if (artifact && record.artifact !== artifact) return false;
    if (task && record.task !== task) return false;
    if (domain && !(record.domain || []).includes(domain)) return false;
    if (method && !(record.method || []).includes(method)) return false;
    if (organization && !(record.orgs || []).includes(organization)) {
      return false;
    }
    if (openSource && !record.open_source) return false;
    return true;
  });

  const sort = elements.sort.value;

  filtered.sort((left, right) => {
    if (sort === "featured") {
      return (
        Number(right.featured) - Number(left.featured) ||
        recordDate(right).localeCompare(recordDate(left)) ||
        left.title.localeCompare(right.title)
      );
    }

    if (sort === "stars") {
      return (
        Number(right.stars || 0) - Number(left.stars || 0) ||
        left.title.localeCompare(right.title)
      );
    }

    if (sort === "title") {
      return left.title.localeCompare(right.title);
    }

    return (
      recordDate(right).localeCompare(recordDate(left)) ||
      Number(right.featured) - Number(left.featured) ||
      Number(right.stars || 0) - Number(left.stars || 0) ||
      left.title.localeCompare(right.title)
    );
  });

  return filtered;
}

function badge(text, className = "") {
  const node = document.createElement("span");
  node.className = `badge ${className}`.trim();
  node.textContent = text;
  return node;
}

function externalLink(label, href) {
  if (!href) return null;

  const link = document.createElement("a");
  link.href = href;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = label;
  return link;
}

function buildCard(record) {
  const card = document.createElement("article");
  card.className = `paper-card ${record.featured ? "featured" : ""}`.trim();

  const heading = document.createElement("h3");
  heading.className = "card-heading";

  const primaryLink = record.paper || record.homepage || record.repo;
  if (primaryLink) {
    const link = externalLink(record.title, primaryLink);
    heading.append(link);
  } else {
    heading.textContent = record.title;
  }

  const badges = document.createElement("div");
  badges.className = "badges";

  if (record.featured) {
    badges.append(badge("Editor’s pick", "badge-featured"));
  }

  badges.append(badge(record.artifact_title));
  if (record.task) badges.append(badge(record.task));
  if (record.published_at) {
    badges.append(badge(record.published_at));
  } else if (record.year) {
    badges.append(badge(String(record.year)));
  }
  if (record.open_source) badges.append(badge("Open source"));
  if (record.stars) badges.append(badge(`★ ${record.stars}`));

  const summary = document.createElement("p");
  summary.className = "summary";
  summary.textContent = record.summary;

  const links = document.createElement("div");
  links.className = "card-links";

  const paper = externalLink("Paper", record.paper);
  const repository = externalLink("Code", record.repo);
  const homepage = externalLink("Project", record.homepage);

  for (const link of [paper, repository, homepage]) {
    if (link) links.append(link);
  }

  card.append(heading, badges, summary, links);
  return card;
}

function syncUrl() {
  const params = new URLSearchParams();

  const mappings = [
    ["q", elements.query.value.trim()],
    ["artifact", elements.artifact.value],
    ["task", elements.task.value],
    ["domain", elements.domain.value],
    ["method", elements.method.value],
    ["org", elements.organization.value],
    ["sort", elements.sort.value === "newest" ? "" : elements.sort.value],
    ["open", elements.openSource.checked ? "1" : ""],
  ];

  for (const [key, value] of mappings) {
    if (value) params.set(key, value);
  }

  const query = params.toString();
  history.replaceState(null, "", query ? `?${query}` : location.pathname);
}

function render() {
  const filtered = selectedRecords();
  const shown = filtered.slice(0, visibleCount);

  elements.results.replaceChildren();

  if (!shown.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No papers match the current filters.";
    elements.results.append(empty);
  } else {
    const fragment = document.createDocumentFragment();
    for (const record of shown) {
      fragment.append(buildCard(record));
    }
    elements.results.append(fragment);
  }

  elements.resultCount.textContent =
    `${filtered.length} ${filtered.length === 1 ? "paper" : "papers"}`;

  elements.loadMore.hidden = visibleCount >= filtered.length;
  elements.results.setAttribute("aria-busy", "false");

  syncUrl();
}

function resetFilters() {
  elements.query.value = "";
  elements.artifact.value = "";
  elements.task.value = "";
  elements.domain.value = "";
  elements.method.value = "";
  elements.organization.value = "";
  elements.sort.value = "newest";
  elements.openSource.checked = false;
  visibleCount = PAGE_SIZE;
  render();
}

function restoreState() {
  const params = new URLSearchParams(location.search);

  elements.query.value = params.get("q") || "";
  elements.artifact.value = params.get("artifact") || "";
  elements.task.value = params.get("task") || "";
  elements.domain.value = params.get("domain") || "";
  elements.method.value = params.get("method") || "";
  elements.organization.value = params.get("org") || "";
  elements.sort.value = params.get("sort") || "newest";
  elements.openSource.checked = params.get("open") === "1";
}

async function start() {
  const response = await fetch("catalog.json");
  if (!response.ok) {
    throw new Error(`Unable to load catalog.json: HTTP ${response.status}`);
  }

  const payload = await response.json();
  records = payload.records || [];

  const artifactLabels = Object.fromEntries(
    records.map((record) => [record.artifact, record.artifact_title])
  );

  appendOptions(
    elements.artifact,
    scalarValues("artifact"),
    artifactLabels
  );
  appendOptions(elements.task, scalarValues("task"));
  appendOptions(elements.domain, arrayValues("domain"));
  appendOptions(elements.method, arrayValues("method"));
  appendOptions(elements.organization, arrayValues("orgs"));

  restoreState();

  elements.catalogStatus.textContent =
    `${records.length} papers · generated ${payload.generated_at}`;

  const controls = [
    elements.query,
    elements.artifact,
    elements.task,
    elements.domain,
    elements.method,
    elements.organization,
    elements.sort,
    elements.openSource,
  ];

  for (const control of controls) {
    control.addEventListener("input", () => {
      visibleCount = PAGE_SIZE;
      render();
    });
    control.addEventListener("change", () => {
      visibleCount = PAGE_SIZE;
      render();
    });
  }

  elements.reset.addEventListener("click", resetFilters);
  elements.loadMore.addEventListener("click", () => {
    visibleCount += PAGE_SIZE;
    render();
  });

  render();
}

start().catch((error) => {
  elements.results.setAttribute("aria-busy", "false");
  elements.resultCount.textContent = "Catalog unavailable";

  const message = document.createElement("p");
  message.className = "empty-state";
  message.textContent = error.message;
  elements.results.replaceChildren(message);
});
"""


def main() -> None:
    repo_stats = read_repo_stats()
    records = [
        public_record(record, repo_stats)
        for record in load_records()
    ]

    records.sort(
        key=lambda record: (
            not record["featured"],
            record["published_at"] or f"{record['year']:04d}-01-01",
            record["stars"],
            record["title"].lower(),
        ),
        reverse=True,
    )

    payload = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M UTC"
        ),
        "records": records,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    write_text(OUTPUT_DIR / "index.html", HTML)
    write_text(OUTPUT_DIR / "styles.css", CSS)
    write_text(OUTPUT_DIR / "app.js", JS)
    write_text(
        OUTPUT_DIR / "catalog.json",
        json.dumps(payload, indent=2, ensure_ascii=False),
    )

    print(
        f"[explorer] wrote {len(records)} records to "
        f"{OUTPUT_DIR.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()