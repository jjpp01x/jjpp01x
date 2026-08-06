#!/usr/bin/env python3
"""Refresh the metrics block in README.md from the featured repositories.

Clones each featured repo into a temporary directory, counts commits and test
functions, writes data/metrics.json, and regenerates the table between the
METRICS markers in README.md.

The point is thematic as well as practical: a README that claims its numbers are
verifiable should not carry numbers that quietly go stale.

Usage:
    python scripts/refresh_metrics.py [--check]

    --check   Exit 1 if README.md would change, without writing (for CI).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
METRICS_JSON = ROOT / "data" / "metrics.json"

OWNER = "jjpp01x"
START = "<!-- METRICS:START -->"
END = "<!-- METRICS:END -->"

# Order here is the order in the rendered table.
FEATURED = [
    {
        "repo": "signal-radar",
        "icon": "📡",
        "name": "Signal Radar",
        "question": "Is this research area actually emerging, or is the whole field just growing?",
        "evidence": "4,113 papers · 66 topics · 1 survives a 10,000-permutation test",
    },
    {
        "repo": "dd-copilot",
        "icon": "🔍",
        "name": "DD-Copilot",
        "question": "Is this deep-tech startup's technical claim credible?",
        "evidence": "every citation verified against the source text",
    },
    {
        "repo": "expert-probe",
        "icon": "🎯",
        "name": "Expert Probe",
        "question": "What should I ask the expert that could prove this claim wrong?",
        "evidence": "8–10 falsifiable questions · confidence recomputed without an LLM",
    },
    {
        "repo": "ai-readiness-matrix",
        "icon": "⚖️",
        "name": "AI Readiness Matrix",
        "question": "Buy, rent or build — and where does that conclusion break?",
        "evidence": "10,000 seeded scenarios · flip point per criterion",
    },
    {
        "repo": "model-card-auditor",
        "icon": "✅",
        "name": "Model Card Auditor",
        "question": "Is this model documented well enough to depend on?",
        "evidence": "6 required fields · fails the CI build below threshold",
    },
    {
        "repo": "ai-safety-incidents",
        "icon": "🛡️",
        "name": "AI Safety Incident Tracker",
        "question": "How do AI systems actually fail in production?",
        "evidence": "23 incidents · [live dashboard](https://ai-safety-incidents.streamlit.app)",
    },
]

# Spelled out in the prose line below the table. Derived from FEATURED, never
# hardcoded: the previous version said "four" and stayed wrong for two repos.
NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
}

# pytest 9 ends with "N tests collected in 0.6s"; pytest 8 instead prints one
# "path/to/test_file.py: N" line per file and no summary. Handle both.
COLLECTED = re.compile(r"(\d+)\s+tests?\s+collected")
PER_FILE = re.compile(r"^\S+\.py:\s*(\d+)\s*$", re.MULTILINE)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    return subprocess.run(
        cmd, cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def count_tests(path: Path) -> int | None:
    """Return the number of tests pytest actually collects.

    This is deliberately not a grep for `def test_`. The README asks readers to
    verify its numbers, so the number has to be the one they get when they run
    the suite themselves — grep and pytest disagree in both directions once
    parametrised tests and uncollected files are involved. Returns None when the
    suite cannot be installed, so the caller can omit the figure rather than
    print an unverifiable one.
    """
    venv = path / ".metrics-venv"
    py = venv / "bin" / "python"
    try:
        run([sys.executable, "-m", "venv", str(venv)])
        pip = [str(py), "-m", "pip", "install", "-q"]

        # The venv ships whatever pip the host python bundles, which on older
        # interpreters cannot build a PEP 621 pyproject at all. Upgrade first.
        run(pip + ["--upgrade", "pip"])

        for req in ("requirements.txt", "requirements-dev.txt"):
            if (path / req).exists():
                run(pip + ["-r", req], cwd=path)
        if (path / "pyproject.toml").exists():
            # Non-editable: editable installs need a setuptools backend, and
            # these projects do not all use one.
            run(pip + ["."], cwd=path)
        run(pip + ["pytest"])

        out = subprocess.run(
            [str(py), "-m", "pytest", "--collect-only", "-q"],
            cwd=path, capture_output=True, text=True,
        ).stdout
        if match := COLLECTED.search(out):
            return int(match.group(1))
        if per_file := PER_FILE.findall(out):
            return sum(int(n) for n in per_file)
        return None
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"warning: could not collect tests in {path.name}: {exc}", file=sys.stderr)
        return None


def collect() -> dict:
    repos: dict[str, dict] = {}
    with tempfile.TemporaryDirectory() as tmp:
        for item in FEATURED:
            name = item["repo"]
            dest = Path(tmp) / name
            url = f"https://github.com/{OWNER}/{name}.git"
            try:
                run(["git", "clone", "--quiet", url, str(dest)])
            except subprocess.CalledProcessError:
                print(f"warning: could not clone {name}, skipping", file=sys.stderr)
                continue
            repos[name] = {
                "commits": int(run(["git", "rev-list", "--count", "HEAD"], cwd=dest)),
                "tests": count_tests(dest),
                "last_commit": run(
                    ["git", "log", "-1", "--format=%ad", "--date=short"], cwd=dest
                ),
            }

    return {
        "generated": date.today().isoformat(),
        "method": "tests as collected by `pytest --collect-only`",
        "repos": repos,
        "total_tests": sum(r["tests"] or 0 for r in repos.values()),
        "total_commits": sum(r["commits"] for r in repos.values()),
    }


def render(metrics: dict) -> str:
    lines = [
        START,
        "",
        "| | Tool | The question it answers | Evidence |",
        "|---|---|---|---|",
    ]
    for item in FEATURED:
        data = metrics["repos"].get(item["repo"])
        tests = f"{data['tests']} tests · " if data and data["tests"] else ""
        lines.append(
            f"| {item['icon']} | **[{item['name']}]"
            f"(https://github.com/{OWNER}/{item['repo']})** | "
            f"{item['question']} | {tests}{item['evidence']} |"
        )

    total = metrics["total_tests"]
    lines += [
        "",
        f"**{total} tests across the {NUMBER_WORDS.get(len(FEATURED), len(FEATURED))} tools**, counted as `pytest --collect-only` reports them —",
        "the same number you get if you clone the repos and run the suites yourself. Refreshed weekly by",
        f"[`refresh-metrics.yml`](.github/workflows/refresh-metrics.yml); last verified {metrics['generated']}.",
        "",
        END,
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    metrics = collect()
    if not metrics["repos"]:
        print("error: no repositories could be read", file=sys.stderr)
        return 1

    text = README.read_text()
    if START not in text or END not in text:
        print(f"error: markers {START} / {END} not found in README.md", file=sys.stderr)
        return 1

    updated = re.sub(
        rf"{re.escape(START)}.*?{re.escape(END)}",
        lambda _: render(metrics),
        text,
        flags=re.DOTALL,
    )

    if args.check:
        if updated != text:
            print("README.md is out of date — run scripts/refresh_metrics.py")
            return 1
        print("README.md is up to date")
        return 0

    METRICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps(metrics, indent=2) + "\n")
    README.write_text(updated)
    print(f"updated: {metrics['total_tests']} tests across {len(metrics['repos'])} repos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
