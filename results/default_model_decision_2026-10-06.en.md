# Default model decision — 2026-10-06

Status: **fixed for the current snapshot**.

## Routing decision

```text
default  -> openai/gpt-6-luna
thinking -> openai/gpt-6.1-sol
```

This decision treats `default` as the normal general-agent model, including translation and output-heavy tasks. It is not a claim that one model is cheapest for every possible token distribution.

## Why GPT-6 Luna is the default

The current ARC-AGI-2 Verified comparison gives DeepSeek V4 Flash 0731 both a higher score and a lower estimated ARC cost than GPT-6 Luna:

| Model | ARC-AGI-2 Verified | Estimated ARC cost/task |
|---|---:|---:|
| DeepSeek V4 Flash 0731 | 61.4% | ~$0.042 |
| GPT-6 Luna | 59.3% | ~$0.062 |

DeepSeek is therefore ahead by 2.1 percentage points and costs approximately 32% less in this ARC comparison. This makes DeepSeek the ARC/value winner, but the ARC graph does not measure general translation quality, tool workflows, or output-heavy agent economics. The default is therefore GPT-6 Luna for the broader agent workload, while DeepSeek remains the preferred ARC-oriented alternative.

## Why this is not a universal price claim

The current OpenRouter catalog prices have different input/output economics:

| Model | Input / 1M tokens | Output / 1M tokens |
|---|---:|---:|
| DeepSeek V4 Flash 0731 | $0.0079 | $1.28 |
| GPT-6 Luna | $0.10 | $0.50 |

Let `I` be input tokens and `O` be output tokens. The catalog break-even point is:

```text
0.0079I + 1.28O = 0.10I + 0.50O
O / I = 0.0921 / 0.78 = 11.8%
```

- Below roughly **11.8% output/input**, DeepSeek is cheaper because its input price is much lower.
- Above roughly **11.8% output/input**, GPT-6 Luna can be cheaper because its output price is lower.

Examples from the current catalog snapshot:

| Token profile | DeepSeek | GPT-6 Luna | Cheaper option |
|---|---:|---:|---|
| 12k input / 1k output | ~$0.00138 | ~$0.00170 | DeepSeek |
| 20k input / 4k output | ~$0.00528 | ~$0.00400 | GPT-6 Luna |
| 100k input / 4k output | ~$0.00591 | ~$0.01200 | DeepSeek |

The ARC task cost and OpenRouter token cost are different measurements. The ARC graph establishes DeepSeek as the better ARC value; the token break-even rule explains why GPT-6 Luna remains a reasonable general-agent default.

## Why GPT-6.1 Sol is `thinking`

GPT-6.1 Sol remains the hard-task escalation model:

- ARC-AGI-2 Verified: **94.2%**;
- estimated ARC cost: **~$0.254/task**;
- OpenRouter catalog price: approximately **$2/M input and $10/M output**.

It is substantially more expensive than the default, so it should be used after a failed attempt, a low-confidence result, or a task classified as difficult.

## Role of DeepSeek V4 Flash 0731

DeepSeek is not removed from the comparison. It remains the ARC/value alternative for long inputs and short or moderate outputs, where its very low input price matters and its ARC result is stronger.

GPT-6 Luna remains the default because the current evidence is more relevant to a general agent with substantial output, translation-style responses, and predictable tool-oriented behavior. The project does not yet have enough same-task replays to claim that either model is universally better for tools or reliability.

## Measurement policy

The next controlled comparison should record, for identical tasks:

1. task success;
2. input and output tokens;
3. billed cost;
4. time to first token and total latency;
5. output tokens per second;
6. provider route, retries, and errors.

Community and unapproved ARC results remain separate from the Verified leaderboard. Prices and provider performance are time-sensitive and must be refreshed before changing this routing decision.

## Sources

- [ARC-AGI-2 official and community results](arc_agi2_results_2026-10-06.md)
- [OpenRouter cost test](openrouter_cost_test_2026-10-06.md)
- [OpenRouter providers: GPT-6 Luna vs DeepSeek](openrouter_provider_comparison_gpt6_luna_deepseek_2026-10-06.md)
- [DeepSeek: DeepInfra vs OpenRouter economics](deepseek_deepinfra_vs_openrouter_economics_2026-10-06.md)
