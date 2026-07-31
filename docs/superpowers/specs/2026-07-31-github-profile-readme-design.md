# GitHub profile README — design spec

**Date:** 2026-07-31
**Repo:** `jjpp01x/jjpp01x` (GitHub profile repo — name must match username)
**Status:** approved, implementing

## Goal

A GitHub profile README that positions Jose Palacios Beórtegui as a **deep-tech analyst who
builds**, aimed primarily at MNTY Technology Ventures (Zürich) — *Research Fellowship: Analyst,
Deep Tech* — and secondarily at international technical recruiters.

## Decisions taken during brainstorming

| # | Decision | Chosen | Rejected alternatives |
|---|---|---|---|
| 1 | Positioning | **Deep-tech analyst who builds the tools he evaluates with** | "AI Engineer" (mirrors reference profile but unsupported by work history); generic "Business + IA" hybrid (too diffuse) |
| 2 | Visual register | **Editorial restraint** — static header, tables, discreet monochrome badges, GitHub stats cards | Animated wave/typing SVG, skillicons, visitor counter (reads junior; conflicts with analyst framing) |
| 3 | Language | **English README**, Spanish LinkedIn post | Spanish README (closes Swiss doors); bilingual README (doubles length, desyncs) |
| 4 | Experience timeline | **Stated explicitly and used as the argument** — "built April–July 2026, verify it" | Omitting dates (evasive; data is one click away); blurring with academic years (the weak claim MNTY screens for) |
| 5 | Repo scope | Four featured tools + compact foundations | See exclusions below |

### Rationale for #1 and #4

MNTY's stated bar is candidates who can *"distinguish a strong technical claim from a weak one
and explain it clearly."* A README opening with an unsupported seniority claim fails that bar in
its first line. Stating the three-month window and inviting verification is both honest and the
stronger argument: density of shipped, tested, deployed work beats claimed tenure.

## Scope

### Featured (4 tools, one thesis: *a technical claim should be checkable*)

| Tool | Question it answers | Verified evidence |
|---|---|---|
| DD-Copilot | Is this deep-tech startup's technical claim credible? | 26 tests, 34 commits, citation verification against source, worked Isomorphic Labs example |
| AI Readiness Matrix | Buy, rent or build — and where does that conclusion break? | 47 tests, 12 commits, 10,000 Dirichlet scenarios (seeded), flip points per criterion |
| Model Card Auditor | Is this model documented well enough to depend on? | 39 tests, 45 commits, 6 required fields, 0–100 score, CI gate |
| AI Safety Incident Tracker | How do AI systems actually fail in production? | 36 tests, 23 incidents, 18 organisations, live Streamlit deployment |

**Aggregate for featured work is generated, not written.** Two corrections were made while
building:

1. The earlier 196/340 figures included `ig-agent` and `Pagina_Web_CV`, which are out of the
   featured set. Only claim numbers that match what is shown.
2. A first implementation counted tests by grepping for `def test_`. It disagreed with
   `pytest --collect-only` in both directions (45 vs 26 in one repo, 20 vs 36 in another) because
   of parametrised tests and uncollected files. A number a reader cannot reproduce is exactly the
   failure mode this profile argues against, so the script now installs each suite and reports
   what pytest actually collects. First verified run: **175 tests, 102 commits** (2026-07-31).

### Secondary
- `josepalacios.site` (`Pagina_Web_CV`) — linked, not featured
- `Ski-resort-ticketing-system`, `heierling` — compact "Foundations" section

### Excluded, with reasons
- **`ig-agent`** — not published. Instagram automation conflicts with platform ToS and the repo
  is unaudited for credentials. No upside for the analyst framing; real downside.
- **Soluciones TDAH** — personal health context, out of scope for a professional profile.
- **`oratoria-coach`** — personal, low relevance to the analyst positioning.
- **`career-ops`** — a fork of a third-party project (Santiago Fernández de Valderrama et al.);
  Jose has 0 commits. Left as an unfeatured fork. See `project_portfolio_autoria` memory.
- **`Level4-Computing-engeniering`** — renamed to `level4-computing-engineering` (two typos in
  the original name); coursework, not featured.

## README structure

1. **Header** — name, positioning line, location, links (site / LinkedIn / email). Static.
2. **The short version** — one paragraph on the BA Business Management + BSc Applied Computing
   combination as the differentiator.
3. **Verification banner** — build window + explicit invitation to check.
4. **Four tools, one thesis** — table, plus one `<details>` block per tool with three headings:
   *what it does · why it's built this way · what it does not do*. The third heading is the
   analyst signature: declare limitations before someone finds them.
5. **How I evaluate technology** — the differentiating section. Five principles extracted from
   the actual codebases, not generic:
   1. Assumptions are versioned, not implied
   2. Asymmetric costs beat symmetric metrics
   3. A weighted matrix without sensitivity analysis is an opinion with decimals
   4. Every row traces to a primary source
   5. Limitations are declared before the conclusion, not after the objection
6. **Stack** — grouped, discreet badges.
7. **Foundations** — education + earlier engineering coursework.
8. **Writing** — link to articles on josepalacios.site.
9. **Stats** — GitHub stats cards, theme-aware.

## Technical requirements

- `<picture>` + `prefers-color-scheme` so images work in light and dark themes
- `alt` text on every image
- `<details>` for density without noise
- No visitor counter, no typing SVG, no animated header
- Auto-updating metrics block delimited by `<!-- METRICS:START -->` / `<!-- METRICS:END -->`

## Auto-update workflow

`.github/workflows/refresh-metrics.yml` — weekly schedule + `workflow_dispatch`.

`scripts/refresh_metrics.py`:
1. For each featured repo: query the GitHub API for commit count and last-push date; shallow-clone
   and count test functions by grep (`def test_` / `it(` / `test(`).
2. Write `data/metrics.json`.
3. Regenerate the block between the METRICS markers in `README.md`.
4. Stamp the "last verified" date.

The point is thematic as well as practical: the README that claims verifiability keeps its own
numbers verified.

## Other deliverables

- **Rename** `Level4-Computing-engeniering` → `level4-computing-engineering` (GitHub preserves
  redirects from the old URL).
- **Website link** — prominent link from `josepalacios.site` to the GitHub profile, beyond the
  existing nav icon.
- **LinkedIn post** — Spanish, built on the "four tools, one thesis" frame, closing with an
  explicit invitation to verify the numbers.

## Out of scope

- Publishing `ig-agent` or `oratoria-coach`
- Any redesign of josepalacios.site beyond adding the link
- Certifications section (none to list yet; adding an empty one would weaken the page)
