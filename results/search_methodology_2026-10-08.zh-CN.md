# 搜索与比较方法

研究日期：**2026-10-08**。

本文固定本仓库寻找 ARC-AGI-2 候选模型、核验结果、计算 OpenRouter 成本以及比较速度和 agent 实用性的流程。

## 1. 先确定 baseline 和严格条件

当前比较以 **GPT-6 Luna** 为 baseline，使用 ARC-AGI-2。候选模型必须满足：ARC 分数高于 Luna，且 OpenRouter 的 input 和 output 单价都不高于 Luna。统一成本画像为 **20,000 input / 4,000 output tokens**，所有结论记录研究日期和来源。

如果问题改为长 input、短 output 等特殊流量，必须明确改变 token 画像。只在特定流量下更便宜的模型只能标记为 conditional alternative。

## 2. 发现 ARC 结果的顺序

1. **ARC Prize Verified leaderboard**：官方 ARC-AGI-2 semi-private 结果和 ARC cost/task。
2. **ARC Prize Community leaderboard 及其 submissions**：官方社区索引，但没有 ARC 明确确认时不能称为 Verified。
3. **TrustTheBench 等独立聚合器**：寻找官方模型表中没有的 user-like 测试。
4. **Kaggle ARC-AGI-2 leaderboard**：有参考价值，但 submission/system 分数不自动等于单个 API 模型的结果。
5. **GitHub、model card、provider 页面和公开报告**：寻找新候选和完整运行上下文。

搜索同时使用人类可读名称、alias 和精确 provider ID。搜索命中只是线索，必须再核对模型版本、数据 split、分数和来源 URL。

## 3. 先区分证据类型

| 类型 | 含义 | 用法 |
|---|---|---|
| `official_verified` | ARC Prize 运行或核验的结果 | 可以进入官方推荐表 |
| `community_self_reported` | 社区 submission 或自报结果 | 单独保存并标记 `🟨*` |
| `independent_aggregate` | 第三方聚合或用户测试 | 用于筛选，不能升级为官方结果 |
| `kaggle_submission` | Kaggle submission/system 分数 | 保留 submission 上下文 |
| `measured_run` | 本地通过 API/provider 重现实测 | 对该配置最有参考价值 |

Official、community、Kaggle 和 measured 数据不应无标签地混在同一分数中。

## 3a. Community 平均值规则

公开表格使用两个独立列：

- `ARC official / Verified`：存在时记录 ARC Prize 官方结果；
- `ARC community 平均值`：只对可比较的 independent/community 观察值求算术平均。

对于 `s1 ... sn`，显示 `(s1 + ... + sn) / n`，并在数值旁标出 `n`。Official score 永远不加入这个平均值。`n=1` 只是单次观察值的平均，不能描述为统计稳定。如果 prompt、harness、split、reasoning budget 或任务数量明显不同，则分成不同 protocol group，不合并。

## 4. 核验模型身份和上下文

每一行记录原始名称、版本或 snapshot、日期、精确 OpenRouter ID、ARC split、score、cost、URL，以及是否使用 system/ensemble、reasoning budget、prompt、tools、retries 和 sampling。Preview 名称、别名和 rolling provider ID 如果不能严格对应当前模型，就标记为 provisional。

## 5. 计算 OpenRouter 经济性

在研究日期读取 OpenRouter catalog/API 或精确模型页，记录 input/output/cache 单价、free/paid 状态、provider 可用性、rate limit、tool calling 和 structured output。

普通请求的估算公式：

```text
cost = input_tokens / 1,000,000 * input_price
     + output_tokens / 1,000,000 * output_price
```

在 `20k/4k` 画像下，Luna `$0.10/$0.50` 的一次请求约为 `$0.004`。这不等于 ARC cost/task，因为 ARC 可能包含 retries、tools、ensemble、hidden reasoning 和 provider overhead。不同流量下价格交叉时，要报告 break-even 条件，而不是宣称绝对赢家。

## 6. 分开比较质量、成本和速度

```text
百分点差 = candidate_score - baseline_score
相对提升 = (candidate_score - baseline_score) / baseline_score * 100
```

速度单独记录 total/average latency、TTFT、output tokens/sec、provider、route、retries、errors、timeouts 和 token usage。不同模型必须使用相同任务集、prompt、timeout、concurrency、temperature、max output 和 routing policy。不能从价格或 ARC 分数推断速度。

## 7. 推荐规则

先选择可比 benchmark，区分证据类型，再应用 score/price 严格条件，最后按质量、成本和运行稳定性排序。特定流量下才成立的结果单独标为 conditional。Free endpoint 在测量 availability 和 rate limit 前只作为 experimental backup。Production default 还必须考虑 tool calling、structured output、latency、provider 稳定性和错误恢复。

README 的 `Σ ARC median (%)` 是 official 和 community 分数都存在时的中位数；只有两个值时，中位数与二者的算术平均值相同。只有一个时使用现有分数。它是 ARC quality 指标，不是性价比指标；Token 价格和 ARC 单任务成本保持为独立列。Σ 不能覆盖 official/community 状态。

### 路由角色

- `default` 表示最便宜的有效模型，而不是任何情况下绝对价格最低的 endpoint。本快照中，有效性定义为 `Σ ARC median ≥ 65%`，并且至少有 official 或 independent evidence；community-only/free-preview 结果不进入 production default。候选还必须通过基本运行检查。先按标准 `20k input / 4k output` 画像最小化估算成本，再检查 tool calling、structured output、latency、provider 稳定性和当前价格。
- `thinking` 表示最高实用质量档中最便宜的模型。优先 official quality；如果接近最高质量的模型明显便宜于绝对最高质量模型，则选择便宜者。因此当前使用 GPT-6.1 Sol，而不是 GPT-6 Astra。
- 条件性路由单独保存：模型可能在长 input/短 output 时更便宜，但不适合作为高 output 调用的 default。Free 和 community-only 模型在完成 availability、privacy 和可重复性验证前保持实验状态。

## 8. 如何复现和更新

运行 fetcher 和比较脚本，记录日期、URL、模型 ID、token 假设和未解决的身份问题；`last.json` 只保留 `default`/`thinking` 短路由配置；然后运行 `git diff --check` 和测试：

```powershell
python scripts/fetch_arc.py
python scripts/fetch_community.py
python scripts/fetch_kaggle.py
python scripts/fetch_openrouter.py --all
python scripts/compare_arc.py
python scripts/compare_openrouter_costs.py
python -m pytest -q
```

独立 ARC 分数高于 Luna 不代表所有 agent 任务都更强，因为 prompt、split、snapshot、reasoning budget、tools、retries 和 ensemble 可能不同。因此表格必须明确区分 **official**、**independent**、**conditional**、**estimated** 和 **measured**。

来源：[ARC Prize](https://arcprize.org/leaderboard)、[Community policy](https://arcprize.org/leaderboard/community)、[TrustTheBench](https://www.trustthebench.com/benchmarks/arc-agi-2)、[Kaggle](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard)、[OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models)。
