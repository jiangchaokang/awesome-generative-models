
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
