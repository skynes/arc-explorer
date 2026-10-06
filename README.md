# ARC-explorer

![ARC-AGI-2 leaderboard chart](results/chart_06_10_26.png)

| Recommendation | Verification | Model | ARC official / Verified | ARC community average | ARC cost/task | OpenRouter catalog price | Research date | Σ ARC median (%) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Highest ARC quality, not cheap — thinking escalation | ✅ | GPT-6.1 Sol | 94.2% | 66.9% (n=1) | ~$0.254 | ~$2/M input; $10/M output | 2026-10-16 | 80.6% |
| Default — cheapest effective model | ✅ | DeepSeek V4.1 Flash | 72.9% | 69.0% (n=1) | — | ~$0.0357/M input; $0.1428/M output† | 2026-10-16 | 71.0% |
| ARC community candidate | 🟨* | MiMo-V2.6-Flash | — | 66.6% (n=1) | ~$0.003–$0.011 est.* | ~$0.10/M input; $0.28/M output | 2026-10-16 | 66.6% |
| ARC value / long-input alternative | ✅ | DeepSeek V4 Flash 0731 | 61.4% | 68.5% (n=1) | ~$0.042 | ~$0.0044/M input; $1.152/M output | 2026-10-16 | 65.0% |
| General-agent compatibility fallback | ✅ | GPT-6 Luna | 59.3% | 61.3% (n=1) | ~$0.062 | ~$0.10/M input; $0.50/M output | 2026-10-16 | 60.3% |

`✅` ARC Prize Verified official result · `🟨*` no ARC Prize Verified result in this table. `ARC official / Verified` and `ARC community average` are intentionally separate. Community averages use independent/community observations only; `(n=1)` means the current source set contains one comparable observation, so it is not evidence of repeatability ([source](https://www.trustthebench.com/benchmarks/arc-agi-2)).

`*` MiMo has no reported ARC cost/task in the unofficial result. The displayed range is an OpenRouter one-request estimate from `$0.10/M` input and `$0.28/M` output: 20k/4k tokens ≈ `$0.0031`, 20k/10k ≈ `$0.0048`, and 100k/4k ≈ `$0.0111` per task ([OpenRouter pricing](https://openrouter.ai/xiaomi/mimo-v2.6-flash-20260921)). It is not an official ARC Prize cost and excludes retries, tools, ensembles, and provider overhead.

`Σ ARC median` is the median of the official and community scores when both exist; with two values this is the same midpoint as their arithmetic mean. If only one exists, it uses the available score. It is an ARC quality indicator, not a cost-quality score; prices remain separate so recommendations can distinguish quality from operating cost. ARC cost/task is excluded when unavailable or not comparable. V4.1's `†` price is a current OpenRouter listing/discount and may change.

Machine-readable routing configuration: [GitHub last.json](https://github.com/skynes/arc-explorer/blob/main/last.json) · [raw last.json](https://raw.githubusercontent.com/skynes/arc-explorer/main/last.json)

---

Reproducible research toolkit for comparing ARC-AGI-2 results, community submissions, OpenRouter economics, provider routing, open-weight models, and alternative inference platforms.

Primary documentation language: **English**. Translations:

- [Русский](README.ru.md)
- [简体中文](README.zh-CN.md)

## What this project tracks

1. **ARC Prize Verified** — official ARC-AGI-2 semi-private results.
2. **Community results** — kept separate because they are self-reported and not directly comparable with Verified.
3. **Kaggle** — competition submissions, not automatically equivalent to a single API-model evaluation.
4. **OpenRouter** — model catalog, provider routing, prices, latency, throughput, and availability.
5. **Direct providers** — DeepInfra, Together, Baseten, Novita, Fireworks, Chutes, SiliconFlow, Groq, Cerebras, and others.
6. **Open-weight hosting** — Hugging Face, GPU rental, self-hosting, and Cocoon.

## Quick start

Requires Python 3.11+.

```powershell
cd arc-explorer
python -m pip install -r requirements.txt

python scripts/fetch_arc.py
python scripts/fetch_community.py
python scripts/fetch_kaggle.py
python scripts/fetch_openrouter.py --all
python scripts/compare_arc.py
python scripts/compare_openrouter_costs.py
python -m pytest -q
```

For a real ARC run through OpenRouter:

```powershell
$env:OPENROUTER_API_KEY = "..."
python scripts/run_openrouter_arc.py `
  --dataset path\to\arc-agi-2\public_eval `
  --model deepseek/deepseek-v4-flash-0731 `
  --model openai/gpt-6-luna `
  --model z-ai/glm-5.3-flash `
  --delay 1
```

Each run can record score, token usage, reported cost, provider, retries, errors, total latency, and output tokens/sec. Streaming TTFT is the next planned runner extension.

## Current research conclusion

- **GPT-6.1 Sol** is the highest-quality option in this table and remains the `thinking` escalation model, but it is expensive.
- **DeepSeek V4.1 Flash** is now the `default`: the cheapest effective model under the current standard profile, with 72.9% official, 69.0% independent, and a lower current OpenRouter price than Luna.
- **GPT-6 Luna** is retained as a general-agent compatibility fallback when predictable behavior, tool workflows, or output-heavy economics matter more than the current ARC/value ranking.
- **GPT-6 Astra** remains the absolute ARC-AGI-2 Verified score leader, but is reserved for maximum-quality runs because it is much more expensive.
- **DeepSeek V4 Flash 0731** remains the long-input/short-output alternative: input is exceptionally cheap, but output is expensive.
- **MiMo-V2.6-Flash** remains an unverified community candidate; its low estimated cost is attractive but its evidence is only one independent observation.
- **Space Bunny Alpha** is an experimental free-preview candidate from an anonymous provider and is not a production recommendation.
- **GLM-5.3-Flash** is the quality-oriented open-weight candidate.
- **Independent ARC screen:** **GLM 5.3 Flash** is the strongest paid candidate that is strictly no more expensive than Luna; **QwQ 32B** and **Nemotron free** endpoints are experimental backup candidates.
- **GPT-6.1 Sol** is the hard-task escalation model.
- **GPT-OSS-120B** is the main hosted open-weight benchmark candidate.
- **Qwen3.8-27B** is the most practical self-host pilot candidate.

For DeepSeek, provider selection matters substantially. DeepInfra can be cheaper than the current OpenRouter default route when output is more than roughly 4.74% of input. If OpenRouter is explicitly pinned to the same DeepInfra provider, token pricing is approximately the same; the difference is then routing, fallback, billing, and platform overhead.

## Model selection methodology

`default` and `thinking` are role-based routes, not a claim that one model wins every workload.

- **Default = cheapest effective model.** For this snapshot, the effectiveness floor is `Σ ARC median ≥ 65%` plus at least official or independent evidence; community-only/free-preview rows do not qualify for the production default. Compute `Σ ARC median` as the median of official and community scores when both exist, or the available score otherwise. Among qualifying models, choose the lowest estimated cost for the standard `20k input / 4k output` profile. Re-check tool calling, structured output, latency, provider reliability, and current price before production use.
- **Thinking = cheapest high-effectiveness escalation.** Select the strongest practical quality tier using official evidence first; when a near-top model is materially cheaper than the absolute maximum, choose the cheaper one. This is why GPT-6.1 Sol remains `thinking`: 94.2% official at a much lower ARC cost than GPT-6 Astra.
- **Conditional routes remain explicit.** DeepSeek V4 Flash 0731 can win for very long input and very short output because of its low input price. A free or community-only model is experimental until availability, privacy, and repeatability are measured.

## Research snapshots

- [Full research snapshot — English primary](results/research_snapshot_all_2026-10-06.en.md)
- [Русский full snapshot](results/research_snapshot_all_2026-10-06.md)
- [中文 full summary](results/research_snapshot_all_2026-10-06.zh-CN.md)
- [ARC-AGI-2 official and community results](results/arc_agi2_results_2026-10-06.md)
- [Independent ARC candidates vs GPT-6 Luna](results/community_arc_candidates_vs_gpt6_luna_2026-10-08.md)
- [ARC official versus community averages — 2026-10-16](results/arc_agi2_dual_status_2026-10-16.md)
- [Search and comparison methodology](results/search_methodology_2026-10-08.md)
- [OpenRouter catalog snapshot](results/openrouter_snapshot_2026-10-06.md)
- [OpenRouter cost test](results/openrouter_cost_test_2026-10-06.md)
- [Decision snapshot](results/decision_snapshot_2026-10-06.md)
- [Open weights, Hugging Face, GPU rental, and Cocoon](results/hosting_alternatives_open_weights_2026-10-06.md)
- [Direct open-weight API providers](results/direct_open_weight_api_providers_2026-10-06.md)
- [DeepSeek: DeepInfra vs OpenRouter economics](results/deepseek_deepinfra_vs_openrouter_economics_2026-10-06.md)
- [OpenRouter providers: GPT-6 Luna vs DeepSeek](results/openrouter_provider_comparison_gpt6_luna_deepseek_2026-10-06.md)
- [Default model decision rationale — English](results/default_model_decision_2026-10-06.en.md)
- [Current routing decision — 2026-10-16](results/default_model_decision_2026-10-16.md)

## Repository layout

```text
config/      Model aliases and comparison configuration
data/        Snapshots and ignored live/raw data
results/     Dated research reports
scripts/     Fetchers, comparisons, cost tests, and ARC runner
tests/       Unit tests for parsers and cost calculations
```

Live downloads and generated processed data are ignored by Git; dated snapshots and Markdown reports are tracked.

## Reproducibility and language policy

- Every research update receives a date-stamped Markdown snapshot.
- English is the primary project language for new documentation.
- Russian and Simplified Chinese translations are maintained for public-facing summaries and research indexes.
- Source data must remain separated by verification status: official, community, Kaggle, provider catalog, and measured run.
- Prices and provider performance are time-sensitive; every result must include retrieval date and source URL.

## Sources

- [ARC Prize leaderboard](https://arcprize.org/leaderboard)
- [ARC Prize community leaderboard](https://arcprize.org/leaderboard/community)
- [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models)
- [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
- [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers/pricing)

## License

This project is released under the [MIT License](LICENSE).

## Contributions

Corrections, source updates, provider measurements, new model comparisons, and improvement proposals are welcome. Please include the retrieval date, source URL, model/provider IDs, and enough context to reproduce the result.
