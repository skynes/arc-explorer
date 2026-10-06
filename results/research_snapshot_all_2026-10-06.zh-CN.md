# arc-explorer — 完整研究摘要

日期：**2026-10-06**。除非特别说明，价格单位为美元。

英文主版本：[English snapshot](research_snapshot_all_2026-10-06.en.md)。俄语完整笔记：[Русский snapshot](research_snapshot_all_2026-10-06.md)。

## 当前决策

没有一个模型同时在质量、价格、速度和稳定性上都最好。建议使用 routing：

```text
通用付费 agent                 -> GPT-6 Luna
ARC 性价比 / 长 input          -> DeepSeek V4 Flash 0731
reasoning-heavy output         -> DeepSeek + DeepInfra
优先质量                       -> GLM-5.3-Flash
困难任务升级                   -> GPT-6.1 Sol
hosted open-weight benchmark   -> GPT-OSS-120B
便宜 planner / pre-check       -> GPT-OSS-20B 或 Llama-3.1-8B
self-host pilot                -> Qwen3.8-27B
```

## ARC-AGI-2 Verified

| 模型 | Score | ARC cost/task |
|---|---:|---:|
| GPT-6 Astra | 95.0% | ~$1.12 |
| GPT-6.1 Sol | 94.2% | ~$0.254 |
| Dots3-Note Preview | 76.8% | ~$0.08 estimate |
| GLM-5.3-Flash | 65.8% | ~$0.093 |
| DeepSeek V4 Flash 0731 | 61.4% | ~$0.042 |
| GPT-5.6 Luna | 59.6% | ~$0.177 |
| GPT-6 Luna | 59.3% | ~$0.062 |

Community 结果是自报数据，不能直接与 Verified semi-private 排名混合。不同 split、prompt、ensemble 和预算都会影响结果。

## OpenRouter 与 DeepInfra 经济性

当前 OpenRouter default route 约为 `$0.0079/$1.28`，DeepInfra 约为 `$0.06/$0.18`。

| Profile | OpenRouter | DeepInfra | 结论 |
|---|---:|---:|---|
| 12k / 1k | $0.001375 | $0.000900 | DeepInfra 便宜 1.53x |
| 20k / 4k | $0.005278 | $0.001920 | DeepInfra 便宜 2.75x |
| 20k / 10k | $0.012958 | $0.003000 | DeepInfra 便宜 4.32x |
| 100k / 4k | $0.005910 | $0.006720 | OpenRouter 便宜 13.7% |

分界点：

```text
output / input > 4.74%  -> DeepInfra 更便宜
output / input < 4.74%  -> OpenRouter 更便宜
```

如果在 OpenRouter 中固定使用 DeepInfra provider，则 upstream token price 基本相同；此时 OpenRouter 的优势是统一 API、fallback 和 routing，Direct DeepInfra 的优势是直接 billing 和少一层 gateway。

## Provider 差异

GPT-6 Luna 主要由 OpenAI、Azure、Amazon Bedrock 提供。OpenAI/Azure Standard 价格相同，差异主要是 latency、throughput 和 availability。

DeepSeek V4 Flash 0731 有 26 个 providers，价格差异很大：

- Relace：`$0.0079/$1.28`；
- DeepInfra：`$0.06/$0.18`；
- Baseten：`$0.13/$0.26`，速度较高；
- Cohere：`$0.14/$0.28`，当前 throughput 很高；
- Together：`$0.14/$0.28`；
- StreamLake promo：`$0.044/$0.132`，不应当作为长期预算基础。

## Open-weight 与部署

- GPT-OSS-120B：主要 hosted open-weight benchmark。
- GPT-OSS-20B、Llama-3.1-8B：便宜 planner/classifier/pre-check。
- Qwen3.8-27B：最现实的 self-host pilot。
- GLM-5.3-Flash、DeepSeek V4 Flash：能力强，但模型总规模使 self-host 成本较高。
- Cocoon：适合研究 confidential/decentralized compute，但还没有稳定、可比较的公开 token 价格表和 production SLA。

## 下一步测试矩阵

```text
DeepSeek: OpenRouter default / OpenRouter->DeepInfra / Direct DeepInfra
GPT-6 Luna: OpenAI Standard / Azure Standard
GPT-OSS-120B: OpenRouter / DeepInfra / Groq / Cerebras
Qwen3.8-27B: OpenRouter / DeepInfra / Chutes
```

每个请求保存 model、provider、input/output/cache tokens、cost、TTFT、total latency、output tok/s、retries、错误、tool-call success、structured-output success 和 ARC correctness。

详细报告：

- [English full snapshot](research_snapshot_all_2026-10-06.en.md)
- [Русский full notes](research_snapshot_all_2026-10-06.md)
- [Provider comparison](openrouter_provider_comparison_gpt6_luna_deepseek_2026-10-06.md)
- [DeepInfra economics](deepseek_deepinfra_vs_openrouter_economics_2026-10-06.md)
