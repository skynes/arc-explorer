# 独立 ARC-AGI-2 结果中优于 GPT-6 Luna 且价格不更高的候选

研究日期：**2026-10-08**。

筛选条件：独立/用户类 ARC-AGI-2 结果高于仓库基准 **GPT-6 Luna：59.3%**，并且 OpenRouter 的 input、output 价格都不高于 Luna 的 `$0.10/M` input 和 `$0.50/M` output。以下 ARC 结果不是 ARC Prize Verified。ARC Prize 说明 community 分数通常是 self-reported；ARC-AGI-1/2 semi-private 结果才是 ARC Prize 运行并验证的部分。

## 严格符合条件的模型

本仓库使用的 `20k input / 4k output` profile 下，Luna 约为 `$0.004`。

| 模型 | 独立 ARC-AGI-2 | 相对 Luna | OpenRouter ID | Input / output | 20k/4k 估算 | 判断 |
|---|---:|---:|---|---:|---:|---|
| GLM 5.3 Flash | 72.2% | +12.9 个百分点 / +21.8% | `z-ai/glm-5.3-flash` | $0.04 / $0.50 | ~$0.0028 | 最强的付费严格候选 |
| Llama 4 Scout | 69.0% | +9.7 个百分点 / +16.4% | `meta-llama/llama-4-scout` | $0.10 / $0.30 | ~$0.0032 | 价格好；tools 取决于 provider |
| NVIDIA Nemotron 3 Ultra (free) | 67.5% | +8.2 个百分点 / +13.8% | `nvidia/nemotron-3-ultra-550b-a55b:free` | free / free | $0.0000 | 实验性 backup；free endpoint 有限制 |
| QwQ 32B (free) | 67.2% | +7.9 个百分点 / +13.3% | `qwen/qwq-32b:free` | free / free | $0.0000 | 便宜的 ARC 候选；模型较旧且有 rate limits |
| MiMo-V2.6-Flash | 66.6% | +7.3 个百分点 / +12.3% | `xiaomi/mimo-v2.6-flash` | $0.10 / $0.28 | ~$0.0031 | 当前已跟踪的低价 general 候选 |
| NVIDIA Nemotron 3 Super (free) | 65.9% | +6.6 个百分点 / +11.1% | `nvidia/nemotron-3-super-120b-a12b:free` | free / free | $0.0000 | 有潜力的 free backup；需压测 availability |
| Gemma 3 27B* | 65.5% | +6.2 个百分点 / +10.5% | `google/gemma-3-27b-it` | $0.08 / $0.16 | ~$0.0022 | 很便宜，但 community row 是 preview 标记 |
| Llama 3.3 70B Instruct | 62.8% | +3.5 个百分点 / +5.9% | `meta-llama/llama-3.3-70b-instruct` | $0.10 / $0.32 | ~$0.0033 | 较旧，agent 能力较弱 |

ARC 分数来自 [TrustTheBench](https://www.trustthebench.com/benchmarks/arc-agi-2) 的独立观察；价格和 ID 来自 [OpenRouter catalog](https://openrouter.ai/openai/gpt-6-luna)。相对百分比为 `(模型 score − 59.3) / 59.3`；百分点是直接 score 差值。

## 重要例外：DeepSeek V4 Flash 0731

TrustTheBench 为 DeepSeek V4 Flash 0731 列出独立结果 **68.5%**。但 OpenRouter 约为 `$0.018/M` input、`$1.28/M` output。因此 input 更便宜，但 output 是 Luna 的 2.56 倍。它不是严格的价格匹配，只适合长 input、短 output 场景。

## 当前结论

1. **GLM 5.3 Flash** 是最值得首先进行付费 A/B 测试的 Luna 替代：在严格价格集合中独立 ARC score 最高，`20k/4k` profile 约便宜 30%。
2. **MiMo-V2.6-Flash** 仍是更稳妥的低价 general 替代。
3. **QwQ 32B free** 和 **Nemotron free** 适合 pre-check/backup，不建议马上作为 production default，因为有 rate limits 且不是 Verified 结果。
4. 这些 ARC 观察不能证明模型全面优于 Luna：prompt、snapshot、reasoning budget 以及 public/private split 可能不同。

## 来源

- [ARC Prize Community Leaderboard policy](https://arcprize.org/leaderboard/community)
- [TrustTheBench ARC-AGI-2](https://www.trustthebench.com/benchmarks/arc-agi-2)
- [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
- [OpenRouter GLM 5.3 Flash](https://openrouter.ai/z-ai/glm-5.3-flash)
- [OpenRouter Llama 4 Scout](https://openrouter.ai/meta-llama/llama-4-scout)
- [OpenRouter MiMo-V2.6-Flash](https://openrouter.ai/xiaomi/mimo-v2.6-flash)
- [OpenRouter Nemotron 3 Ultra free](https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free)
- [OpenRouter Nemotron 3 Super free](https://openrouter.ai/nvidia/nemotron-3-super-120b-a12b:free)
- [OpenRouter QwQ 32B free](https://openrouter.ai/qwen/qwq-32b:free)
- [OpenRouter Gemma 3 27B](https://openrouter.ai/google/gemma-3-27b-it)
- [OpenRouter Llama 3.3 70B Instruct](https://openrouter.ai/meta-llama/llama-3.3-70b-instruct)

\* В TrustTheBench строка называется **Gemma 3 27B Preview**; цена OpenRouter относится к текущему `google/gemma-3-27b-it`, поэтому перед production нужно проверить exact snapshot.
