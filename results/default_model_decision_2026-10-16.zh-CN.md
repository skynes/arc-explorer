# 当前路由决策 — 2026-10-16

## 路由

```text
default  -> deepseek/deepseek-v4.1-flash
thinking -> openai/gpt-6.1-sol
```

## 选择规则

`default` 是最便宜的有效模型。`thinking` 是最高实用质量档中最便宜的模型，并有意优先解决复杂任务的成功率。

质量信号使用 `Σ ARC median`：official 和 community 都存在时取中位数，否则使用唯一可用值。Community-only 和 free-preview 结果在完成 availability、privacy 和可重复性验证前保持实验状态。

本快照中，有效性门槛是 `Σ ARC median ≥ 65%`，并且至少有 official 或 independent evidence；community-only/free-preview 结果不进入 production default。Default 候选在标准 `20k input / 4k output` 画像下比较，然后检查 tool calling、structured output、latency、provider 稳定性和错误恢复。只在长 input、极短 output 下更便宜的模型单独作为条件性路由。

## 为什么 default 改为 V4.1 Flash

| 模型 | ARC official | ARC community | Σ ARC median | 20k/4k 估算 |
|---|---:|---:|---:|---:|
| DeepSeek V4.1 Flash | 72.9% | 69.0% | **71.0%** | **~$0.00129** |
| DeepSeek V4 Flash 0731 | 61.4% | 68.5% | 65.0% | ~$0.00470 |
| GPT-6 Luna | 59.3% | 61.3% | 60.3% | ~$0.00400 |

V4.1 是当前数据集中最佳 practical quality/value 候选，在标准画像下按当前 OpenRouter 价格低于 Luna。价格具有时效性，生产部署前必须重新获取。

## 为什么 thinking 仍然使用 Sol

GPT-6.1 Sol 的 **official ARC-AGI-2 为 94.2%**，估算 ARC 单任务成本约 **$0.254**。GPT-6 Astra 略高，为 **95.0%**，但估算成本约 **$1.12/任务**。因此 Sol 是更便宜的高效果升级方案，质量差距很小。

## 条件性替代方案

- DeepSeek V4 Flash 0731 在超长 input、极短 output 时仍有优势，因为 input 价格非常低。
- GPT-6 Luna 保留为 compatibility fallback，适用于更看重通用 agent 可预测行为、tool calling 或高 output 经济性的 workflow。
- MiMo 和 Space Bunny 在重复验证结果、可用性和运行风险前仍属于 community/experimental 候选。

## 来源

- [ARC official 与 community](arc_agi2_dual_status_2026-10-16.zh-CN.md)
- [搜索与比较方法](search_methodology_2026-10-08.zh-CN.md)
- [OpenRouter DeepSeek V4.1 Flash](https://openrouter.ai/deepseek/deepseek-v4.1-flash)
- [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
