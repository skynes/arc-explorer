# Independent ARC-AGI-2 candidates versus GPT-6 Luna

Research date: **2026-10-08**.

This screen looks for independent/user-like ARC-AGI-2 results above the repository baseline for **GPT-6 Luna: 59.3%**, while requiring OpenRouter catalog input and output prices to be no higher than Luna's `$0.10/M` input and `$0.50/M` output. The ARC results below are not ARC Prize Verified results. ARC Prize states that community scores are self-reported unless noted otherwise; the ARC-AGI-1/2 semi-private results are the part it runs and verifies.

## Strict matches

The standard OpenRouter comparison profile used in this repository is `20k input / 4k output`. Luna costs about `$0.004` for that profile.

| Model | Independent ARC-AGI-2 | Difference vs Luna | OpenRouter ID | Input / output | 20k/4k estimate | Assessment |
|---|---:|---:|---|---:|---:|---|
| GLM 5.3 Flash | 72.2% | +12.9 pp / +21.8% | `z-ai/glm-5.3-flash` | $0.04 / $0.50 | ~$0.0028 | Strongest paid strict match |
| Llama 4 Scout | 69.0% | +9.7 pp / +16.4% | `meta-llama/llama-4-scout` | $0.10 / $0.30 | ~$0.0032 | Good price; tool calling is provider-dependent |
| NVIDIA Nemotron 3 Ultra (free) | 67.5% | +8.2 pp / +13.8% | `nvidia/nemotron-3-ultra-550b-a55b:free` | free / free | $0.0000 | Experimental backup; free endpoint is rate-limited and less available |
| QwQ 32B (free) | 67.2% | +7.9 pp / +13.3% | `qwen/qwq-32b:free` | free / free | $0.0000 | Cheap ARC candidate; old model and rate-limited |
| MiMo-V2.6-Flash | 66.6% | +7.3 pp / +12.3% | `xiaomi/mimo-v2.6-flash` | $0.10 / $0.28 | ~$0.0031 | Best existing low-cost general candidate |
| NVIDIA Nemotron 3 Super (free) | 65.9% | +6.6 pp / +11.1% | `nvidia/nemotron-3-super-120b-a12b:free` | free / free | $0.0000 | Promising free backup; verify availability under load |
| Gemma 3 27B* | 65.5% | +6.2 pp / +10.5% | `google/gemma-3-27b-it` | $0.08 / $0.16 | ~$0.0022 | Very cheap, but community row is a preview/snapshot label |
| Llama 3.3 70B Instruct | 62.8% | +3.5 pp / +5.9% | `meta-llama/llama-3.3-70b-instruct` | $0.10 / $0.32 | ~$0.0033 | Older, weaker agent candidate |

The ARC scores are independent observations aggregated by [TrustTheBench](https://www.trustthebench.com/benchmarks/arc-agi-2). Prices and model IDs are from the corresponding [OpenRouter catalog](https://openrouter.ai/openai/gpt-6-luna). The relative percentage is `(candidate score - 59.3) / 59.3`; percentage points are the direct score difference.

## Important non-match: DeepSeek V4 Flash 0731

TrustTheBench lists an independent **68.5%** result for DeepSeek V4 Flash 0731, which is above Luna. OpenRouter lists approximately `$0.018/M` input and `$1.28/M` output. Therefore it is much cheaper on input but **not** a strict price match: output is 2.56x Luna's price. It can still be cheaper for long-context, short-output requests, but it is not uniformly cheaper.

## Current decision

1. **GLM 5.3 Flash** is the first model to test as a paid Luna replacement: the strongest independent ARC result in this strict price set, with a 30% lower cost on the repository's `20k/4k` profile.
2. **MiMo-V2.6-Flash** remains the safer low-cost general alternative already tracked in the main table.
3. **QwQ 32B free** and **Nemotron free** models are useful pre-check/backup candidates, not yet production defaults because free endpoints are rate-limited and community scores are not verified.
4. These ARC observations should not be treated as proof that the models are generally better than Luna: the independent runs, prompts, snapshots, reasoning budgets, and public/private splits are not guaranteed to match.

## Sources

- [ARC Prize Community Leaderboard policy](https://arcprize.org/leaderboard/community)
- [TrustTheBench ARC-AGI-2 independent results](https://www.trustthebench.com/benchmarks/arc-agi-2)
- [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
- [OpenRouter GLM 5.3 Flash](https://openrouter.ai/z-ai/glm-5.3-flash)
- [OpenRouter Llama 4 Scout](https://openrouter.ai/meta-llama/llama-4-scout)
- [OpenRouter MiMo-V2.6-Flash](https://openrouter.ai/xiaomi/mimo-v2.6-flash)
- [OpenRouter Nemotron 3 Ultra free](https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free)
- [OpenRouter Nemotron 3 Super free](https://openrouter.ai/nvidia/nemotron-3-super-120b-a12b:free)
- [OpenRouter QwQ 32B free](https://openrouter.ai/qwen/qwq-32b:free)
- [OpenRouter Gemma 3 27B](https://openrouter.ai/google/gemma-3-27b-it)
- [OpenRouter Llama 3.3 70B Instruct](https://openrouter.ai/meta-llama/llama-3.3-70b-instruct)

\* TrustTheBench's row is labeled **Gemma 3 27B Preview**; the OpenRouter price is for the currently catalogued `google/gemma-3-27b-it` model and should be rechecked by exact snapshot before a production decision.
