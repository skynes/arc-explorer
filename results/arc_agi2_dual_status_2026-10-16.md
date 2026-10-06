# ARC-AGI-2 official versus community averages

Research date: **2026-10-16**.

This snapshot keeps two ARC numbers separate:

- **ARC official / Verified** — the ARC Prize Verified result, normally a semi-private evaluation;
- **ARC community average** — the arithmetic mean of comparable independent/community observations, excluding official scores;
- **Σ ARC median** — the median of the official and community values when both exist, or the one available value.

`n=1` is shown deliberately. It means that the current source set has one comparable independent observation, so the value is a one-observation mean rather than a robust estimate of repeatability.

| OpenRouter ID | ARC official / Verified | ARC community average | Σ ARC median | n | Verification | OpenRouter price per 1M input / output | Notes |
|---|---:|---:|---:|---:|---|---:|---|
| `openai/gpt-6.1-sol` | 94.2% | 66.9% | **80.6%** | 1 | ✅ official + independent | ~$2 / $10 | Official and independent setups are not equivalent |
| `deepseek/deepseek-v4.1-flash` | 72.9% | 69.0% | **71.0%** | 1 | ✅ official + independent | ~$0.0357 / $0.1428† | Strongest practical quality/value candidate in this group |
| `stealth/space-bunny-alpha` | — | 70.4% | **70.4%** | 1 | 🟨* independent only | free preview | Anonymous stealth model; no official ARC result found |
| `xiaomi/mimo-v2.6-flash` | — | 66.6% | **66.6%** | 1 | 🟨* independent only | ~$0.10 / $0.28 | No ARC Prize Verified result found |
| `xiaomi/mimo-v2.5` | — | 65.7% | **65.7%** | 1 | 🟨* independent only | ~$0.119 / $0.238 | No ARC Prize Verified result found |
| `deepseek/deepseek-v4-flash-0731` | 61.4% | 68.5% | **65.0%** | 1 | ✅ official + independent | ~$0.00441 / $1.152 | Independent result is much higher than official |
| `openai/gpt-6-luna` | 59.3% | 61.3% | **60.3%** | 1 | ✅ official + independent | ~$0.10 / $0.50 | Repository general-agent baseline |

The community values above are from the **2026-08-29 independent snapshot** on [TrustTheBench ARC-AGI-2](https://www.trustthebench.com/benchmarks/arc-agi-2). They are not ARC Prize Verified results and should not be treated as a statistically stable multi-run average.

`†` V4.1's price is a current OpenRouter listing/discount and may change.

## Interpretation

- **GPT-6.1 Sol** has the highest Σ ARC median in this table, but its price makes it an escalation model rather than the default.
- **DeepSeek V4.1 Flash** is the best practical quality/value candidate: 72.9% official, 69.0% independent, and a lower current OpenRouter price than Luna.
- **Space Bunny Alpha** has the best independent number in this small group, but it is anonymous, free-preview, and unverified by ARC Prize. OpenRouter says it is operated by an anonymous third-party provider and that prompts/completions may be retained by the provider ([model page](https://openrouter.ai/stealth/space-bunny-alpha)).
- **DeepSeek V4 Flash 0731** has a large official/community gap; this is a reason to inspect harness, prompt, split, reasoning effort, and task count before using the community value for a decision.
- MiMo-V2.5 and MiMo-V2.6-Flash have independent observations but no official ARC Prize result located in this snapshot.

For two values, `Σ ARC median` is the midpoint of official and community; for one available value, it is that value. This is an ARC-quality indicator, not a cost-quality index. OpenRouter prices remain separate and time-sensitive.

## Averaging rule

For a model with independent/community scores `s1 ... sn`:

```text
community_average = (s1 + s2 + ... + sn) / n
```

Official scores are never included in this average. Each future row should add a source URL, retrieval date, model snapshot, harness, split, reasoning setting, and `n`. If observations use materially different protocols, the table should show separate protocol groups instead of merging them.

## Sources

- [ARC Prize DeepSeek V4.1 Flash — official result](https://arcprize.org/results/deepseek-v4-1-flash)
- [ARC Prize DeepSeek V4 Flash 0731 — official result](https://arcprize.org/results/deepseek-v4-flash-0731)
- [ARC Prize leaderboard](https://arcprize.org/leaderboard)
- [TrustTheBench ARC-AGI-2 independent snapshot](https://www.trustthebench.com/benchmarks/arc-agi-2)
- [OpenRouter DeepSeek V4.1 Flash](https://openrouter.ai/deepseek/deepseek-v4.1-flash)
- [OpenRouter Space Bunny Alpha](https://openrouter.ai/stealth/space-bunny-alpha)
- [OpenRouter DeepSeek V4 Flash 0731](https://openrouter.ai/deepseek/deepseek-v4-flash-0731)
- [OpenRouter MiMo-V2.6-Flash](https://openrouter.ai/xiaomi/mimo-v2.6-flash)
- [OpenRouter MiMo-V2.5](https://openrouter.ai/xiaomi/mimo-v2.5)
