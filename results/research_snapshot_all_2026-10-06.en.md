# arc-explorer — complete research snapshot

Date: **2026-10-06**. Prices are USD unless noted otherwise.

This is the English primary summary of the ARC-AGI-2, OpenRouter, provider, open-weight, and hosting research. The Russian canonical notes are in [research_snapshot_all_2026-10-06.md](research_snapshot_all_2026-10-06.md); a Chinese summary is in [research_snapshot_all_2026-10-06.zh-CN.md](research_snapshot_all_2026-10-06.zh-CN.md).

## Executive decision

There is no single winner on quality, price, speed, and reliability. Use routing:

```text
general paid agent              -> GPT-6 Luna
ARC value / long input          -> DeepSeek V4 Flash 0731
reasoning-heavy output          -> DeepSeek via DeepInfra
quality over price              -> GLM-5.3-Flash
hard escalation                 -> GPT-6.1 Sol
hosted open-weight benchmark    -> GPT-OSS-120B
cheap planner / pre-check       -> GPT-OSS-20B or Llama-3.1-8B
self-host pilot                 -> Qwen3.8-27B
```

## ARC-AGI-2 Verified

| Model | Score | ARC cost/task | Use |
|---|---:|---:|---|
| GPT-6 Astra | 95.0% | ~$1.12 | Highest quality, expensive |
| GPT-6.1 Sol | 94.2% | ~$0.254 | Hard escalation |
| Dots3-Note Preview | 76.8% | ~$0.08 est. | Experimental |
| GLM-5.3-Flash | 65.8% | ~$0.093 | Quality/value candidate |
| DeepSeek V4 Flash 0731 | 61.4% | ~$0.042 | Best ARC value among selected models |
| GPT-5.6 Luna | 59.6% | ~$0.177 | Weak value versus Luna |
| GPT-6 Luna | 59.3% | ~$0.062 | General agent balance |

Community results remain separate because they are self-reported and may use different prompts, budgets, ensembles, or splits. A 92.5% Public Train result is not comparable with Verified semi-private results.

## OpenRouter economics

Current model-level price landmarks:

| Model | Input/M | Output/M |
|---|---:|---:|
| DeepSeek V4 Flash 0731 | ~$0.0079–0.009 | $1.28 |
| GPT-6 Luna | $0.10 | $0.50 |
| GLM-5.3-Flash | $0.15 | $0.50 |
| GPT-5.6 Luna | $0.20 | $1.20 |
| GPT-6.1 Sol | $2.00 | $10.00 |
| GPT-6 Astra | $10.00 | $50.00 |

Catalog and web pages can expose different effective/default values. Production measurements must store the response `usage.cost`, model, provider, and date.

## DeepInfra versus OpenRouter for DeepSeek

OpenRouter currently lists a default route around `$0.0079/$1.28` and DeepInfra around `$0.06/$0.18`.

| Profile | OpenRouter default | DeepInfra Direct | Result |
|---|---:|---:|---|
| 12k input / 1k output | $0.001375 | $0.000900 | DeepInfra 1.53x cheaper |
| 20k input / 4k output | $0.005278 | $0.001920 | DeepInfra 2.75x cheaper |
| 20k input / 10k output | $0.012958 | $0.003000 | DeepInfra 4.32x cheaper |
| 100k input / 4k output | $0.005910 | $0.006720 | OpenRouter 13.7% cheaper |

Break-even:

```text
output / input > 4.74%  -> DeepInfra is cheaper
output / input < 4.74%  -> OpenRouter is cheaper
```

This is not a universal “DeepInfra beats OpenRouter” claim. If OpenRouter is pinned to the same DeepInfra provider, the upstream token rate is approximately the same; OpenRouter then adds routing/fallback convenience, while Direct DeepInfra gives direct billing and one less gateway.

## Provider comparison

### GPT-6 Luna

GPT-6 Luna is served by OpenAI, Azure, and Amazon Bedrock. OpenAI and Azure Standard have the same `$0.10/$0.50` price. OpenAI Standard currently shows lower latency than Azure Standard, while Azure shows higher throughput. Flex is half price but slower and less available; Fast is roughly twice the Standard price.

### DeepSeek V4 Flash 0731

DeepSeek has 26 listed providers and much larger price dispersion:

- Relace: `$0.0079/$1.28`, 36 tok/s;
- DeepInfra: `$0.06/$0.18`, 36 tok/s;
- Baseten: `$0.13/$0.26`, 114 tok/s;
- Cohere: `$0.14/$0.28`, 134 tok/s;
- Together: `$0.14/$0.28`, 52 tok/s;
- StreamLake promotional route: `$0.044/$0.132`.

For an output-heavy agent, start with DeepInfra. For speed, benchmark Cohere and Baseten. Treat promotional rates as temporary.

## Open-weight models and alternatives

- **GPT-OSS-120B:** main hosted open-weight benchmark; HF routes ranged roughly from `$0.04/$0.17` to much faster but more expensive Groq/Cerebras routes.
- **GPT-OSS-20B / Llama-3.1-8B:** cheap planner, classifier, or pre-check models.
- **Qwen3.8-27B:** practical self-host candidate for one large GPU.
- **GLM-5.3-Flash / DeepSeek V4 Flash:** strong open-weight models, but their total model sizes make self-hosting expensive.
- **Cocoon:** promising confidential/decentralized compute, but no stable public comparable token-price table or production SLA was found.

Direct provider conclusions:

- DeepInfra: best first test for output-heavy DeepSeek.
- Together/Baseten: production and speed alternatives.
- Groq/Cerebras: speed-first, not cost-first.
- Chutes: useful for Qwen and private TEE deployments.
- SiliconFlow: regional/RMB candidate requiring separate model-ID and time-window validation.
- Hugging Face: useful unified provider layer; dedicated endpoints are hourly GPU billing.
- Replicate: useful for custom/community models, usually not cheapest for a constant agent loop.

## Self-host economics

Approximate GPU references:

- RunPod A100 80GB: ~$1.59/hour;
- Modal A100: ~$2.50/hour;
- HF A100 Endpoint: ~$2.50/hour;
- HF GLM-5.3-Flash recipe: 8×H200, ~$40/hour.

Self-host wins only with sustained utilization, batching, and enough traffic. For intermittent agent requests, token APIs are usually cheaper.

## Measurement policy

Every future run must store:

```text
model_id, provider_name, provider_model_id
input_tokens, cached_input_tokens, output_tokens, reasoning_tokens
reported_cost, TTFT, total_latency, output_tokens_per_second
retries, HTTP errors, tool-call success, structured-output success
ARC correctness and split identity
```

Next matrix:

```text
DeepSeek: OpenRouter default / OpenRouter->DeepInfra / Direct DeepInfra
GPT-6 Luna: OpenAI Standard / Azure Standard
GPT-OSS-120B: OpenRouter / DeepInfra / Groq / Cerebras
Qwen3.8-27B: OpenRouter / DeepInfra / Chutes
```

## Detailed reports and sources

- [Russian full snapshot](research_snapshot_all_2026-10-06.md)
- [ARC official and community](arc_agi2_results_2026-10-06.md)
- [OpenRouter snapshot](openrouter_snapshot_2026-10-06.md)
- [OpenRouter cost test](openrouter_cost_test_2026-10-06.md)
- [Open weights, HF, GPU, and Cocoon](hosting_alternatives_open_weights_2026-10-06.md)
- [Direct provider comparison](direct_open_weight_api_providers_2026-10-06.md)
- [DeepInfra economics](deepseek_deepinfra_vs_openrouter_economics_2026-10-06.md)
- [GPT-6 Luna vs DeepSeek providers](openrouter_provider_comparison_gpt6_luna_deepseek_2026-10-06.md)

Sources: [ARC Prize](https://arcprize.org/leaderboard), [OpenRouter DeepSeek](https://openrouter.ai/deepseek/deepseek-v4-flash-0731), [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna), [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [DeepInfra](https://deepinfra.com/pricing), [Hugging Face Providers](https://huggingface.co/inference/models).
