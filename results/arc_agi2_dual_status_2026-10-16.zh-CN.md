# ARC-AGI-2：official 与 community 平均值

研究日期：**2026-10-16**。

本快照将两个 ARC 指标分开保存：

- **ARC official / Verified**：ARC Prize Verified 官方结果，通常来自 semi-private 评测；
- **ARC community 平均值**：只对可比较的 independent/community 观察结果求算术平均，不包含 official score；
- **Σ ARC median**：official 和 community 都存在时取二者中位数，否则使用唯一可用值。

`n=1` 表示当前只有一个可比较的独立观察值，因此只是单个观察值的平均，不代表稳定的重复实验结论。

| OpenRouter ID | ARC official / Verified | ARC community 平均值 | Σ ARC median | n | 状态 | OpenRouter 每 1M input / output 价格 | 备注 |
|---|---:|---:|---:|---:|---|---:|---|
| `openai/gpt-6.1-sol` | 94.2% | 66.9% | **80.6%** | 1 | ✅ official + independent | ~$2 / $10 | official 与 independent 配置不可直接等同 |
| `deepseek/deepseek-v4.1-flash` | 72.9% | 69.0% | **71.0%** | 1 | ✅ official + independent | ~$0.0357 / $0.1428† | 本组最佳 practical quality/value 候选 |
| `stealth/space-bunny-alpha` | — | 70.4% | **70.4%** | 1 | 🟨* 仅 independent | 免费 preview | 匿名 stealth 模型，未找到 official ARC |
| `xiaomi/mimo-v2.6-flash` | — | 66.6% | **66.6%** | 1 | 🟨* 仅 independent | ~$0.10 / $0.28 | 未找到 ARC Prize Verified 结果 |
| `xiaomi/mimo-v2.5` | — | 65.7% | **65.7%** | 1 | 🟨* 仅 independent | ~$0.119 / $0.238 | 未找到 ARC Prize Verified 结果 |
| `deepseek/deepseek-v4-flash-0731` | 61.4% | 68.5% | **65.0%** | 1 | ✅ official + independent | ~$0.00441 / $1.152 | 独立结果明显高于 official |
| `openai/gpt-6-luna` | 59.3% | 61.3% | **60.3%** | 1 | ✅ official + independent | ~$0.10 / $0.50 | 仓库通用 agent 基准模型 |

Community 数值来自 **TrustTheBench 2026-08-29 independent snapshot**（[ARC-AGI-2](https://www.trustthebench.com/benchmarks/arc-agi-2)）。这些不是 ARC Prize Verified 结果，也不是多次运行后的稳定统计平均。

`†` V4.1 价格为 OpenRouter 当前目录/折扣价格，可能变化。

## 如何解读

- **GPT-6.1 Sol** 的 Σ ARC median 最高，但价格较高，因此作为升级模型而非 default。
- **DeepSeek V4.1 Flash** 是本组最佳 practical quality/value 候选：official 72.9%、independent 69.0%，当前 OpenRouter 价格低于 Luna。
- **Space Bunny Alpha** 在这组数据中有最高的 independent 分数，但它是匿名免费 preview 模型，没有 ARC Prize 验证。OpenRouter 表示它由匿名第三方运营，prompts/completions 可能被保存（[模型页面](https://openrouter.ai/stealth/space-bunny-alpha)）。
- **DeepSeek V4 Flash 0731** 的 official 与 community 差距很大，需要进一步核对 harness、prompt、split、reasoning effort 和任务数量。
- MiMo-V2.5 和 MiMo-V2.6-Flash 有独立观察结果，但本快照中没有找到 official ARC Prize 结果。

有两个值时，`Σ ARC median` 是 official 与 community 的中间值；只有一个可用值时使用该值。这是 ARC quality 指标，不是性价比指标。OpenRouter 价格单独记录，并且会随日期变化。

## 平均规则

对于 independent/community score `s1 ... sn`：

```text
community_average = (s1 + s2 + ... + sn) / n
```

Official score 永远不加入这个平均值。每个新结果都记录 URL、日期、模型 snapshot、harness、split、reasoning setting 和 `n`。如果测试协议存在明显差异，则分组展示，不合并为一个平均值。

来源：[ARC Prize V4.1](https://arcprize.org/results/deepseek-v4-1-flash)、[ARC Prize V4 Flash 0731](https://arcprize.org/results/deepseek-v4-flash-0731)、[TrustTheBench](https://www.trustthebench.com/benchmarks/arc-agi-2)、[OpenRouter](https://openrouter.ai/deepseek/deepseek-v4.1-flash)。
