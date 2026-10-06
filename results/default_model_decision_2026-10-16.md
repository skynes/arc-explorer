# Current routing decision — 2026-10-16

## Routing

```text
default  -> deepseek/deepseek-v4.1-flash
thinking -> openai/gpt-6.1-sol
```

## Selection rule

`default` is the cheapest effective model. `thinking` is the cheapest model in the highest practical quality tier, with a deliberate bias toward solving difficult tasks successfully.

The quality signal is `Σ ARC median`: the median of official and community scores when both exist, or the only available score. Community-only and free-preview rows remain experimental until availability, privacy, and repeatability are measured.

For this snapshot, the effectiveness floor is `Σ ARC median ≥ 65%` plus at least official or independent evidence; community-only/free-preview rows do not qualify for the production default. Candidates are compared on the standard `20k input / 4k output` request profile. Price is then checked alongside tool calling, structured output, latency, provider stability, and failure recovery. A model that is cheaper only for long input and very short output is reported as a conditional route.

## Why V4.1 Flash is now default

| Model | ARC official | ARC community | Σ ARC median | Estimated 20k/4k cost |
|---|---:|---:|---:|---:|
| DeepSeek V4.1 Flash | 72.9% | 69.0% | **71.0%** | **~$0.00129** |
| DeepSeek V4 Flash 0731 | 61.4% | 68.5% | 65.0% | ~$0.00470 |
| GPT-6 Luna | 59.3% | 61.3% | 60.3% | ~$0.00400 |

V4.1 is the strongest practical quality/value candidate in the current evidence set and is cheaper than Luna on the current OpenRouter listing for the standard profile. The price is time-sensitive and must be refreshed before production rollout.

## Why Sol remains thinking

GPT-6.1 Sol has **94.2% official ARC-AGI-2** at approximately **$0.254 per ARC task**. GPT-6 Astra is slightly higher at **95.0%**, but its estimated ARC cost is approximately **$1.12 per task**. Sol is therefore the cheaper high-effectiveness escalation with only a small quality gap to the maximum-quality option.

## Conditional alternatives

- DeepSeek V4 Flash 0731 remains attractive for very long input and very short output because its input price is exceptionally low.
- GPT-6 Luna remains a compatibility fallback for workflows where predictable general-agent behavior, tool calling, or output-heavy economics are more important than the current ARC/value ranking.
- MiMo and Space Bunny remain community/experimental candidates until independent results are repeated and operational risks are measured.

## Sources

- [ARC official versus community report](arc_agi2_dual_status_2026-10-16.md)
- [Search and comparison methodology](search_methodology_2026-10-08.md)
- [OpenRouter DeepSeek V4.1 Flash](https://openrouter.ai/deepseek/deepseek-v4.1-flash)
- [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
