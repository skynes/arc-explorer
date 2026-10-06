# Search and comparison methodology

Research date: **2026-10-08**.

This document describes how ARC-AGI-2 model candidates are discovered, verified, priced, compared, and promoted to a recommendation in this repository. The goal is to find models that are not only strong on ARC, but also practical for an agent: affordable, available, fast enough, and reproducible.

## 1. Start with an explicit comparison question

Every search begins with a baseline and a strict filter. For the current screen:

- baseline: **GPT-6 Luna**;
- benchmark: **ARC-AGI-2**;
- quality condition: candidate ARC score must be higher than the baseline;
- price condition: OpenRouter input price and output price must each be no higher than Luna's;
- common cost profile: **20,000 input tokens / 4,000 output tokens**;
- research date: recorded in the report and in every dated snapshot.

If the user asks a different question, the baseline, token profile, or strictness must be changed explicitly. A model that only wins under long-input/short-output traffic is reported as conditional, not as a universal winner.

## 2. Discover candidate ARC results

Search in this order:

1. **ARC Prize Verified leaderboard** — the primary source for official ARC-AGI-2 semi-private results and reported ARC cost/task.
2. **ARC Prize Community leaderboard and linked submissions** — official community index, but community scores remain separate from Verified unless ARC explicitly marks a result as verified.
3. **Independent benchmark aggregators** such as TrustTheBench — useful for finding user-like model rows that are not present in the official model leaderboard.
4. **Kaggle ARC-AGI-2 pages and leaderboards** — useful evidence, but a competition submission or system score is not automatically equivalent to a single API-model evaluation.
5. **GitHub repositories, model cards, provider pages, and public reports** — used to find new candidates and the exact evaluation context.

Search by both human-readable names and aliases. Then normalize every candidate to a canonical model name and an exact provider ID. A search hit is only a lead until the result, model variant, dataset split, and source URL are recorded.

## 3. Classify the evidence before comparing it

Each row receives one verification class:

| Class | Meaning | How it is used |
|---|---|---|
| `official_verified` | ARC Prize ran or verified the result on the relevant official evaluation | May appear in the official recommendation table |
| `community_self_reported` | Community submission or self-reported result | Kept separate and marked `🟨*` |
| `independent_aggregate` | Third-party benchmark collection or user-like evaluation | Useful for screening, never silently upgraded to official |
| `kaggle_submission` | Kaggle competition submission or system score | Reported with its submission context |
| `measured_run` | Reproduced locally through an API or provider | Strongest evidence for the exact prompt, route, and date used |

The official ARC leaderboard and community leaderboard are not interchangeable. A community score is not used to rewrite an official score, and an independent aggregate is not described as ARC Prize Verified.

## 3a. Community-average convention

Public tables expose both columns:

- `ARC official / Verified` — the official ARC Prize value, if one exists;
- `ARC community average` — the arithmetic mean of comparable independent/community observations only.

For observations `s1 ... sn`, the displayed value is `(s1 + ... + sn) / n`, with `n` shown beside the value. Official scores are never included in this mean. When `n=1`, the value is a one-observation mean and must not be described as statistically stable. If prompts, harnesses, splits, reasoning budgets, or task counts differ materially, observations are kept in separate protocol groups rather than merged.

## 4. Validate model identity and evaluation context

For every promising row, record:

- model name as published by the source;
- exact model version, release date, or snapshot label;
- OpenRouter model ID, including `:free` when applicable;
- benchmark name and split: ARC-AGI-2, public, semi-private, or another split;
- score, cost/task, date, and source URL;
- whether the row is a single model or a system/ensemble;
- reasoning budget, prompt format, retries, tools, and sampling settings when available.

Preview labels, aliases, and rolling provider IDs require a warning. For example, a community row labelled “Preview” must not be silently treated as the current production model with the same family name. If exact identity cannot be established, keep the candidate in the report but mark the comparison as provisional.

## 5. Verify OpenRouter economics

Use the OpenRouter model catalog/API or the exact model page captured on the research date. Record:

- canonical OpenRouter ID;
- input price per million tokens;
- output price per million tokens;
- cache-read price when relevant;
- free/paid status;
- provider availability, rate limits, tool calling, structured output, and routing notes.

For a non-cached request, estimate one request as:

```text
cost = input_tokens / 1,000,000 * input_price
     + output_tokens / 1,000,000 * output_price
```

For the repository's standard profile:

```text
20k input / 4k output
Luna = 20,000 / 1,000,000 * $0.10
     + 4,000 / 1,000,000 * $0.50
     = $0.004 per request
```

The estimate is not the same as ARC cost/task. ARC cost/task can include multiple attempts, retries, tools, ensembles, hidden reasoning, and provider overhead. When input and output prices cross over between models, show the break-even or traffic condition instead of declaring one model universally cheaper.

## 6. Compare quality, cost, and speed separately

Quality is reported in two forms:

```text
absolute difference = candidate_score - baseline_score       # percentage points
relative improvement = (candidate_score - baseline_score)
                       / baseline_score * 100                 # percent
```

Cost is reported as both catalog prices and the same-token-profile estimate. A model must not receive a quality advantage merely because its test used a different number of tasks, a larger reasoning budget, or an ensemble.

Speed is a separate dimension. A reproducible API run should record:

- total latency and average latency;
- time to first token when streaming support is available;
- output tokens per second;
- provider and route;
- retries, errors, timeouts, and availability;
- prompt and completion token counts.

The repository runner records latency, provider, usage, cost, retries, errors, and output tokens/sec. Compare models with the same task set, prompt, timeout, concurrency, temperature, maximum output, and provider-routing policy. Do not infer speed from catalog price or from a benchmark score.

## 7. Apply the recommendation rules

The decision process is:

1. Filter for the requested benchmark and a comparable evaluation context.
2. Separate official, community, independent, Kaggle, and measured results.
3. Apply the strict score and price conditions.
4. Sort strict matches by quality first, then by cost and operational reliability.
5. Report conditional winners separately, for example a model that is cheaper only when output is short.
6. Treat free endpoints as experimental backups until availability and rate limits are measured.
7. Recommend a production default only after considering tool calling, structured output, latency, provider stability, and failure recovery.
8. Escalate difficult tasks to a stronger thinking model when expected quality gain justifies the extra cost.

The `Σ ARC median (%)` value in the main README is the median of the official and community scores when both are available; with two values, this is the same midpoint as their arithmetic mean. If only one exists, the available score is used. It is an ARC-quality indicator, not a cost-quality score; token prices and ARC cost/task remain separate columns. It must not override the official/community status or operational caveats.

### Routing roles

- `default` means the cheapest effective model, not the absolute cheapest endpoint. In the current snapshot, effective means `Σ ARC median ≥ 65%` plus at least official or independent evidence; community-only/free-preview rows do not qualify for the production default. A candidate must also pass basic operational checks. The selection minimizes estimated cost for the standard `20k input / 4k output` profile, then checks tool calling, structured output, latency, provider reliability, and current price.
- `thinking` means the cheapest model in the highest practical quality tier. Official quality is prioritized; when a near-top model is materially cheaper than the absolute maximum-quality model, the cheaper model is selected. The current route therefore uses GPT-6.1 Sol rather than GPT-6 Astra.
- Conditional routes are kept separate: a model can be cheaper for long input/short output without being the default for output-heavy calls. Free and community-only models stay experimental until availability, privacy, and repeatability are measured.

## 8. Reproduce and update a result

For each update:

1. Run the relevant fetcher or manually capture the source if an endpoint is not machine-readable.
2. Save raw/processed data under the repository's data layout when appropriate; do not commit secrets or API keys.
3. Run the comparison and cost scripts.
4. Record retrieval date, URLs, exact IDs, assumptions, and unresolved identity issues in a dated Markdown report.
5. Update `last.json` only for the short routing configuration (`default` and `thinking`), not as a replacement for the research archive.
6. Update the three README summaries only after the dated report is complete.
7. Run `git diff --check` and the test suite before committing.

Typical local commands:

```powershell
python scripts/fetch_arc.py
python scripts/fetch_community.py
python scripts/fetch_kaggle.py
python scripts/fetch_openrouter.py --all
python scripts/compare_arc.py
python scripts/compare_openrouter_costs.py
python -m pytest -q
```

## 9. What the results do not prove

An independent ARC score above Luna does not prove that a model is generally better for every agent workload. ARC runs can differ in prompt, task subset, public/private split, model snapshot, reasoning budget, retry policy, tools, and ensemble strategy. A price estimate also does not include the whole application cost unless retries, failed calls, tool calls, caching, and provider overhead are measured.

The repository therefore uses cautious wording: **official**, **independent**, **conditional**, **estimated**, and **measured** are different claims and must remain visibly different in tables and conclusions.

## Primary sources

- [ARC Prize leaderboard](https://arcprize.org/leaderboard)
- [ARC Prize community policy](https://arcprize.org/leaderboard/community)
- [TrustTheBench ARC-AGI-2](https://www.trustthebench.com/benchmarks/arc-agi-2)
- [Kaggle ARC-AGI-2 competition](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard)
- [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models)
- [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
