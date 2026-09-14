<h1 align="center">Jose Palacios Beórtegui</h1>

<p align="center">
  <strong>Deep-tech analyst who builds the tools he evaluates with.</strong><br/>
  Technical due diligence · evaluation frameworks · AI risk assessment
</p>

<p align="center">
  <a href="https://josepalacios.site"><img src="https://img.shields.io/badge/Website-josepalacios.site-1E2761?style=flat-square" alt="Website: josepalacios.site"/></a>
  <a href="https://www.linkedin.com/in/jose-palacios-beortegui/"><img src="https://img.shields.io/badge/LinkedIn-Connect-1E2761?style=flat-square" alt="LinkedIn profile"/></a>
  <a href="mailto:palaciosbeortegui@gmail.com"><img src="https://img.shields.io/badge/Email-palaciosbeortegui@gmail.com-1E2761?style=flat-square" alt="Email: palaciosbeortegui@gmail.com"/></a>
  <img src="https://img.shields.io/badge/Based%20in-Z%C3%BCrich,%20Switzerland-6B7899?style=flat-square" alt="Based in Zürich, Switzerland"/>
</p>

---

## The short version

I work at the point where a technical claim meets a financial decision.

I hold a **BA (Hons) Business Management** and I am completing a **BSc (Hons) Applied Computing**,
both at the University of Wales Trinity Saint David. That combination is the whole point: I can
read a whitepaper and price the risk hiding in it, and then ship the pipeline that checks whether
its citations actually say what it claims they say.

Most evaluation work fails in one of two directions — analysts who cannot verify what they are
told, or engineers who can build anything but cannot say which thing is worth building. I am
trying to be useful in the gap.

> ### Everything below was built between April and August 2026.
> Commit history, test counts and live deployments are all public. **Check them.** A profile that
> asks you to trust its numbers is exactly the kind of claim the tools below exist to catch.

---

## Six tools, one thesis

**A technical claim should be checkable.** Each of these answers one question that comes up in
real technical due diligence.

<!-- METRICS:START -->

| | Tool | The question it answers | Evidence |
|---|---|---|---|
| 📡 | **[Signal Radar](https://github.com/jjpp01x/signal-radar)** | Is this research area actually emerging, or is the whole field just growing? | 194 tests · 4,113 papers · 66 topics · 1 survives a 10,000-permutation test |
| 🔍 | **[DD-Copilot](https://github.com/jjpp01x/dd-copilot)** | Is this deep-tech startup's technical claim credible? | 78 tests · every citation verified against the source text |
| 🎯 | **[Expert Probe](https://github.com/jjpp01x/expert-probe)** | What should I ask the expert that could prove this claim wrong? | 109 tests · 8–10 falsifiable questions · confidence recomputed without an LLM |
| ⚖️ | **[AI Readiness Matrix](https://github.com/jjpp01x/ai-readiness-matrix)** | Buy, rent or build — and where does that conclusion break? | 51 tests · 10,000 seeded scenarios · flip point per criterion |
| ✅ | **[Model Card Auditor](https://github.com/jjpp01x/model-card-auditor)** | Is this model documented well enough to depend on? | 51 tests · 6 required fields · fails the CI build below threshold |
| 🛡️ | **[AI Safety Incident Tracker](https://github.com/jjpp01x/ai-safety-incidents)** | How do AI systems actually fail in production? | 48 tests · 23 incidents · [live dashboard](https://ai-safety-incidents.streamlit.app) |

**531 tests across the six tools**, counted as `pytest --collect-only` reports them —
the same number you get if you clone the repos and run the suites yourself. Refreshed weekly by
[`refresh-metrics.yml`](.github/workflows/refresh-metrics.yml); last verified 2026-09-14.

<!-- METRICS:END -->

<br/>

<details>
<summary><strong>Signal Radar</strong> — separating an emerging topic from a growing field</summary>

<br/>

**What it does.** Ingests arXiv, clusters papers into topics, and tests whether a topic's growth is
distinguishable from the growth of the corpus around it. On 4,113 papers from 2023–2026 it found 66
topics; exactly one cleared significance — vision-language-action robotic manipulation, growing
5.00× year-on-year against a 1.58× corpus baseline, q = 0.007 after Benjamini-Hochberg across all 66
contrasts. The output is a two-page brief a partner can read in one sitting.

**Why it's built this way.** A growth ratio on its own is decoration: a topic can grow simply because
the literature grew. So publication dates are shuffled across the whole corpus 10,000 times with
cluster membership held fixed, and the observed growth is compared against that null. The tool also
refuses to issue a verdict when the permutation count makes the smallest achievable q exceed alpha —
below that floor the arithmetic, not the evidence, would be deciding every result.

**What it does not do.** It measures attention, not viability. A 5× rise in papers is equally
consistent with "this is about to work" and with "everyone has realised the previous approach fails".
There are no patents, no funding data and no institutional affiliations — arXiv does not supply them.

`Python` · `DuckDB` · `UMAP + HDBSCAN` · `sentence-transformers` · **[read the brief →](https://github.com/jjpp01x/signal-radar/blob/main/briefs/2026-08-01-embodied-vla-manipulation.md)**

</details>
<details>
<summary><strong>DD-Copilot</strong> — from a startup's public material to a decision-ready brief</summary>

<br/>

**What it does.** Takes a URL, a PDF or pasted text from a deep-tech startup and produces a
five-section technical due-diligence brief: executive summary, what the startup says, what it does
*not* say, questions for the next founder call, and a justified confidence level.

**Why it's built this way.** The interesting part of diligence is not the summary — it is the
gap between the claim and the evidence. So the pipeline runs a dedicated fuzzy-match check of every
citation against the source text before anything reaches the report, and carries a fixed checklist
of risks the source failed to address: technology readiness level, hardware and vendor dependency,
reproducibility, regulatory exposure.

**What it does not do.** It does not assess market size, team or commercial traction, and it cannot
see anything the startup did not publish. It is one input to a diligence process, not the process.

`LlamaIndex (RAG)` · `Claude` · `Typer CLI` · `Streamlit` · 8 modules, ingest → report

</details>
<details>
<summary><strong>Expert Probe</strong> — turning unresolved claims into questions that can fail</summary>

<br/>

**What it does.** Takes the claims DD-Copilot could not settle — the *plausible* and the
*unsupported* ones — and turns them into an 8–10 question script for an expert call. Afterwards it
maps the notes from that call back onto the claims and recomputes a confidence figure.

**Why it's built this way.** Refuting a claim raises confidence exactly as much as confirming it
does: the figure measures the quality of the evidence, not the health of the company, and
deterioration of the thesis is reported on a separate axis so the two are never fused into one
number. The recomputation is a formula with no LLM in it — determinism where it is needed, language
where it is not. Notes are anonymised before any prompt is built, and the mapping step accepts only
an `AnonymizedNote`, so the boundary is held by the type system rather than by a runtime check alone.

**What it does not do.** It does not conduct the interview, score the expert, or decide anything. It
produces questions whose answers would change your mind, which are the only ones worth the call.

`Python` · `Pydantic` · `cryptography` · consumes DD-Copilot's `--json` output

</details>
<details>
<summary><strong>AI Readiness Matrix</strong> — buy, rent or build, with the conclusion stress-tested</summary>

<br/>

**What it does.** A reproducible technology-evaluation engine. The decision criteria live in
versioned YAML with a written rubric for every 1–5 level; the report is *generated* from the data,
never hand-written. Worked case: a ski-equipment retailer choosing a demand-forecasting approach.

**Why it's built this way.** Anyone can assemble a weighted matrix that confirms the winner they
already had in mind. What is defensible is showing the range of weights over which the conclusion
survives. So the engine computes, for each criterion, the exact weight at which the winner would
change — and then perturbs all weights at once via Dirichlet sampling over 10,000 seeded scenarios
to report how often each option wins. The case also rejects symmetric error metrics: over- and
under-forecasting do not cost the same when unsold stock is liquidated at a discount, so the
criteria are built around asymmetric (pinball) loss rather than MAPE.

**What it does not do.** It does not benchmark the tools itself. Scores come from documented
evidence, and figures that are estimates are marked `estimated` in the output rather than
presented as measurements.

`Python` · `YAML` · `Streamlit` · Dirichlet sensitivity analysis · fixed seed, exactly reproducible

</details>
<details>
<summary><strong>Model Card Auditor</strong> — documentation risk, enforced in CI</summary>

<br/>

**What it does.** Audits the model card of any Hugging Face model against six required
documentation fields — limitations, bias, training data, licence, context length, benchmarks —
scores completeness 0–100, renders a documentation-risk report, and can fail a CI build when the
score drops below a threshold.

**Why it's built this way.** Extraction runs regex-first over the card's headed sections and only
falls back to an LLM classification call when the regex misses. That is a deliberate cost decision:
the common case should not pay for inference. Scoring is weightable per field because not every
consumer cares equally about every gap.

**What it does not do.** It measures whether a model is *documented*, not whether it is *good*. A
well-written card for a poor model scores highly, and that is the intended behaviour — it is a
documentation-risk tool.

`Python` · `Hugging Face Hub` · regex + LLM fallback · CI gate

</details>
<details>
<summary><strong>AI Safety Incident Tracker</strong> — how production AI actually fails</summary>

<br/>

**What it does.** Classifies 23 public, documented failures of production AI systems (2015–2025)
across 18 organisations by failure mode and severity, with a root-cause study of one real case: the
model supply chain across OpenAI and Hugging Face (2023–2024), four incidents with a common cause
and seven controls that would have prevented it.

**Why it's built this way.** It is deliberately not a headline aggregator. Every row traces to a
primary source, the severity rubric is written down before it is applied, and the limitations are
declared in the dashboard itself — before anyone quotes a figure from it.

**What it does not do.** 23 incidents is not a statistically representative sample of AI failure,
and the dataset says so explicitly. It supports pattern recognition, not base rates.

`Python` · `Streamlit` · `pandas` · **[live dashboard →](https://ai-safety-incidents.streamlit.app)**

</details>

---

## How I evaluate technology

These are not aspirations — each one is visible in the code above.

**1 · Assumptions are versioned, not implied.**
If a number came from a judgement call, that judgement belongs in a file with a rubric next to it,
where it can be changed and the result regenerated. A spreadsheet cell nobody can trace is not
evidence.

**2 · Asymmetric costs beat symmetric metrics.**
Most forecasting tooling optimises MAPE or RMSE by default. Most businesses do not lose the same
amount from an over-estimate as from an under-estimate. Choosing the loss function *is* the
analysis; everything after it is arithmetic.

**3 · A weighted matrix without sensitivity analysis is an opinion with decimals.**
The useful question is never "which option won" — it is "how much would the weights have to move
before the answer flips". If that number is small, the recommendation is fragile and should be
reported as fragile.

**4 · Every row traces to a primary source.**
A claim that cannot be walked back to where it came from is a rumour with formatting. This is the
one rule that admits no exceptions.

**5 · Limitations are declared before the conclusion, not after the objection.**
Stating what your analysis cannot support is not hedging — it is the part that makes the rest of it
usable. Work that only reveals its weaknesses under challenge was never decision-ready.

---

## Stack

**Analysis & AI**
![Python](https://img.shields.io/badge/Python-1E2761?style=flat-square&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-1E2761?style=flat-square&logo=pandas&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-2E3D7A?style=flat-square)
![Claude](https://img.shields.io/badge/Claude-2E3D7A?style=flat-square&logo=anthropic&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-2E3D7A?style=flat-square&logo=huggingface&logoColor=white)
![RAG](https://img.shields.io/badge/RAG-2E3D7A?style=flat-square)

**Building & shipping**
![Streamlit](https://img.shields.io/badge/Streamlit-1E2761?style=flat-square&logo=streamlit&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-1E2761?style=flat-square&logo=pytest&logoColor=white)
![Git](https://img.shields.io/badge/Git-1E2761?style=flat-square&logo=git&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-1E2761?style=flat-square&logo=githubactions&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-2E3D7A?style=flat-square&logo=sqlite&logoColor=white)

**Web**
![HTML5](https://img.shields.io/badge/HTML5-2E3D7A?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-2E3D7A?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-2E3D7A?style=flat-square&logo=javascript&logoColor=black)

---

## Foundations

**BA (Hons) Business Management** — University of Wales Trinity Saint David, 2021–2025
**BSc (Hons) Applied Computing** — University of Wales Trinity Saint David, in progress

Earlier engineering coursework, kept public because the reasoning still holds up:

- **[Ski resort ticketing system](https://github.com/jjpp01x/Ski-resort-ticketing-system)** — session ticketing in C with SQLite persistence
- **[heierling](https://github.com/jjpp01x/heierling)** — inventory management for a ski-boot retailer
- **[josepalacios.site](https://github.com/jjpp01x/Pagina_Web_CV)** — this portfolio, hand-written, W3C-validated, ES/EN/DE

Languages: Spanish (native) · English · German

---

## Writing

I publish analysis at **[josepalacios.site/articulos.html](https://josepalacios.site/articulos.html)** —
technical pieces written the same way as the tools above: sourced, and explicit about what they do
not cover.

---

## Activity

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api?username=jjpp01x&show_icons=true&hide_border=true&theme=github_dark&hide_title=true"/>
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api?username=jjpp01x&show_icons=true&hide_border=true&theme=graywhite&hide_title=true"/>
    <img src="https://github-readme-stats.vercel.app/api?username=jjpp01x&show_icons=true&hide_border=true&hide_title=true" alt="GitHub statistics for jjpp01x" width="420"/>
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=jjpp01x&layout=compact&hide_border=true&theme=github_dark&hide_title=true"/>
    <source media="(prefers-color-scheme: light)" srcset="https://github-readme-stats.vercel.app/api/top-langs/?username=jjpp01x&layout=compact&hide_border=true&theme=graywhite&hide_title=true"/>
    <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=jjpp01x&layout=compact&hide_border=true&hide_title=true" alt="Most used languages by jjpp01x" width="330"/>
  </picture>
</p>

---

<p align="center">
  <sub>
    Open to <strong>deep-tech analyst</strong> and <strong>AI evaluation</strong> roles in Switzerland.<br/>
    <a href="https://josepalacios.site">josepalacios.site</a> ·
    <a href="mailto:palaciosbeortegui@gmail.com">palaciosbeortegui@gmail.com</a>
  </sub>
</p>
