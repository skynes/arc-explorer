# arc-explorer — полный research snapshot

Дата фиксации: **2026-10-06**. Валюта цен: USD, если не указано иное.

Это сводная запись всех исследований по ARC-AGI-2, OpenRouter, провайдерам, open-weight моделям и альтернативам запуска. Детальные расчёты сохранены в отдельных отчётах и связаны ниже.

## 1. Главный вывод для агентной системы

Единственной лучшей модели по всем критериям нет. Практичнее использовать routing по типу задачи:

```text
обычный платный агент       -> GPT-6 Luna
ARC value / длинный input   -> DeepSeek V4 Flash 0731
много reasoning/output      -> DeepSeek через DeepInfra
качество выше цены          -> GLM-5.3-Flash
сложная эскалация           -> GPT-6.1 Sol
быстрый open-weight          -> GPT-OSS-120B через Cerebras/Groq
дешёвый pre-check            -> GPT-OSS-20B или Llama-3.1-8B
private/self-host pilot      -> Qwen3.8-27B
```

## 2. ARC-AGI-2 Verified: официальный результат

Основной сравнимый источник — ARC Prize Verified semi-private evaluation. Эти цифры нельзя смешивать с community self-reported и Kaggle team leaderboard без отдельной маркировки.

| Модель | ARC-AGI-2 score | ARC cost/task | Роль |
|---|---:|---:|---|
| GPT-6 Astra | 95.0% | ~$1.12 | Максимальное качество, дорого |
| GPT-6.1 Sol | 94.2% | ~$0.254 | Сложная эскалация |
| Dots3-Note Preview | 76.8% | ~$0.08 estimate | Экспериментальный free/low-cost вариант |
| GLM-5.3-Flash | 65.8% | ~$0.093 | Лучший quality/cost среди сильных tested candidates |
| DeepSeek V4 Flash 0731 | 61.4% | ~$0.042 | Лучший ARC value среди выбранных |
| GPT-5.6 Luna 2026-07-30 | 59.6% | ~$0.177 | Дороже при близком score |
| GPT-6 Luna | 59.3% | ~$0.062 | Общий баланс для агента |

### Community data

Community leaderboard хранится отдельно, потому что это self-reported/unverified data. Найденные результаты нельзя напрямую ранжировать рядом с Verified:

- semi-private community submissions: примерно 29.4% и 26.0% в найденных записях;
- Noemon 92.5% относится к Public Train и не является сопоставимым semi-private результатом;
- community score может использовать другой prompt, ensemble, budget или hardware.

Подробности: [ARC official + community report](arc_agi2_results_2026-10-06.md).

## 3. OpenRouter: цены и роль моделей

Текущие ориентиры OpenRouter snapshot:

| Модель | Input / 1M | Output / 1M | Роль |
|---|---:|---:|---|
| DeepSeek V4 Flash 0731 | ~$0.0079–0.009 | $1.28 | Input-heavy или длинный reasoning через дешёвого provider |
| GPT-6 Luna | $0.10 | $0.50 | Основной универсальный агент |
| GLM-5.3-Flash | $0.15 | $0.50 | Более качественный open-weight candidate |
| GPT-5.6 Luna | $0.20 | $1.20 | Не лучший value среди текущих вариантов |
| GPT-6.1 Sol | $2.00 | $10.00 | Эскалация сложных задач |
| GPT-6 Astra | $10.00 | $50.00 | Максимальное качество, высокая цена |
| Dots3-Note Preview | free | free | Rate limits и availability risk |

OpenRouter page и Models API могут показывать слегка отличающиеся effective/default values. Для production нужно сохранять фактический `usage.cost` из ответа, а не только каталог.

Подробности: [OpenRouter snapshot](openrouter_snapshot_2026-10-06.md), [OpenRouter cost test](openrouter_cost_test_2026-10-06.md).

## 4. OpenRouter cost-test

Тест моделировал одинаковые token profiles:

```text
arc_short:       12k input / 1k output
agent_normal:    20k input / 4k output
agent_reasoning: 20k input / 10k output
long_context:    100k input / 4k output
```

Зафиксированная policy:

- GPT-6 Luna — платный default agent;
- DeepSeek — длинный input и быстрый helper;
- GLM-5.3-Flash — если качество важнее небольшой разницы в цене;
- GPT-6.1 Sol — escalation;
- Dots — только экспериментальный free route.

Тест стоимости не заменяет ARC run: для качества нужен одинаковый ARC split, одинаковый prompt и одинаковый retry/timeout policy.

## 5. DeepInfra vs OpenRouter: точная экономика

Текущий OpenRouter model page показывает default/listed route примерно `$0.0079/$1.28`, а provider DeepInfra — `$0.06/$0.18`.

### Стоимость запроса

| Профиль | OpenRouter default | DeepInfra Direct | Результат |
|---|---:|---:|---|
| 12k / 1k | $0.001375 | $0.000900 | DeepInfra 1.53x дешевле |
| 20k / 4k | $0.005278 | $0.001920 | DeepInfra 2.75x дешевле |
| 20k / 10k | $0.012958 | $0.003000 | DeepInfra 4.32x дешевле |
| 100k / 4k | $0.005910 | $0.006720 | OpenRouter дешевле на 13.7% |

Точка безубыточности:

```text
output / input > 4.74%  -> DeepInfra дешевле
output / input < 4.74%  -> OpenRouter дешевле
```

Ключевое уточнение: OpenRouter может сам отправить запрос на DeepInfra через `provider.only` или `provider.order`. В режиме OpenRouter → DeepInfra token-rate примерно такой же, как в Direct DeepInfra; преимущество прямого API тогда — отдельный billing и отсутствие gateway/platform layer. OpenRouter даёт единый API, fallback и routing.

Подробности: [DeepInfra vs OpenRouter economics](deepseek_deepinfra_vs_openrouter_economics_2026-10-06.md).

## 6. Provider comparison внутри OpenRouter

### GPT-6 Luna

Основные providers: OpenAI, Azure, Amazon Bedrock.

- OpenAI Standard: `$0.10/$0.50`, latency 2.53 s, 61 tok/s;
- Azure Standard: `$0.10/$0.50`, latency 4.06 s, 78 tok/s;
- OpenAI Flex: `$0.05/$0.25`, latency 6.35 s, uptime 92.13%;
- OpenAI Fast: `$0.20/$1.00`, latency 1.75 s, 105 tok/s.

Вывод: цена Standard provider почти одинаковая, поэтому у GPT-6 Luna provider choice в основном про latency, throughput и failover.

### DeepSeek V4 Flash 0731

OpenRouter показывает 26 providers. Представительные routes:

- Relace: `$0.0079/$1.28`, 0.82 s, 36 tok/s;
- DeepInfra: `$0.06/$0.18`, 0.76 s, 36 tok/s;
- Baseten: `$0.13/$0.26`, 0.69 s, 114 tok/s;
- Cohere: `$0.14/$0.28`, 0.50 s, 134 tok/s;
- Together: `$0.14/$0.28`, 0.75 s, 52 tok/s;
- StreamLake promo: `$0.044/$0.132`, 1.33 s, 41 tok/s.

Вывод: для DeepSeek provider choice одновременно меняет цену и скорость. Для agentic output-heavy маршрута стоит начать с DeepInfra; для speed — проверить Cohere/Baseten; promo routes не считать постоянным production budget.

Подробности: [Provider comparison GPT-6 Luna vs DeepSeek](openrouter_provider_comparison_gpt6_luna_deepseek_2026-10-06.md).

## 7. Open-weight models

### Основные кандидаты

| Модель | Практическая роль | Ограничение |
|---|---|---|
| GPT-OSS-120B | Сильный hosted open-weight agent | Direct routes не всегда дешевле OpenRouter |
| GPT-OSS-20B | Дешёвый planner/router | Качество ниже 120B |
| Qwen3.8-27B | Реалистичный self-host candidate | Output API price выше маленьких моделей |
| Qwen3-32B | Практичный open-weight baseline | Ограниченный context относительно новых моделей |
| Llama-3.1-8B | Самый дешёвый pre-check | Не кандидат на максимальный ARC score |
| GLM-5.3-Flash | Сильная open-weight quality option | 321B-class self-host очень дорогой |
| DeepSeek V4 Flash 0731 | ARC value и long context | 284B total parameters, multi-GPU deployment |
| Kimi-K3 | Сильный большой open model | Слишком дорогой для дешёвого default |
| Ling-3.0-flash | Большой hybrid reasoning model | Рекомендуется multi-GPU cluster |

В HF provider snapshot GPT-OSS-120B показывал примерно `$0.04/$0.17` у DeepInfra, `$0.05/$0.25` у Novita, `$0.15/$0.75` у Groq и `$0.35/$0.75` у Cerebras. GPT-OSS-20B дешевле, но нужно отдельно измерять ARC quality.

## 8. Сервисы дешевле или альтернативнее OpenRouter

### DeepInfra

Главный direct API кандидат для DeepSeek output-heavy. Сильная сторона — низкая output price. Нужны отдельные тесты tool calling, JSON schema, rate limits и latency.

### Together AI

Хороший production provider с serverless, provisioned throughput и dedicated inference. Часто не дешевле DeepInfra, но удобен для стабильной нагрузки.

### Baseten

Важен как speed-oriented provider. Для DeepSeek в текущем snapshot около 114 tok/s, для GLM-5.3-Flash — около 119 tok/s. Нужно проверить реальные лимиты аккаунта.

### Novita AI

Большой каталог, но для DeepSeek V4 Flash 0731 текущая цена заметно выше DeepInfra. Полезен как fallback.

### Fireworks AI

Production/enterprise tooling и большой каталог, но обычно не price leader для выбранных моделей.

### Groq и Cerebras

Нужны ради скорости. GPT-OSS-120B у Cerebras/Groq может быть значительно быстрее, но token price выше DeepInfra/OpenRouter.

### Chutes

Public token API и private TEE deployment. Интересен для Qwen3.8-27B/Qwen3-32B и privacy, но DeepSeek route не самый дешёвый.

### SiliconFlow

Интересен для RMB-регионов, китайских моделей и off-peak тарифов. Нельзя напрямую смешивать с USD-сравнением без проверки model ID, курса, региона и времени тарификации.

### Hugging Face

HF Inference Providers — единый gateway без собственной model markup по словам HF; цена зависит от upstream provider. Dedicated Inference Endpoints оплачиваются за час GPU, поэтому выгодны при постоянной нагрузке, а не при редких запросах.

### Replicate

Хорош для community/custom models и редких workloads, но public/deployment billing по compute time и cold starts обычно не оптимальны для постоянного agent loop.

Подробности: [Direct open-weight API providers](direct_open_weight_api_providers_2026-10-06.md).

## 9. GPU и self-host economics

Ориентиры из исследованных прайсов:

- RunPod A100 80GB: около `$1.59/h`;
- RunPod L40S: около `$1.09/h`;
- Modal A100: около `$2.50/h`;
- HF A100 Endpoint: около `$2.50/h`;
- HF GLM-5.3-Flash recipe: 8×H200, около `$40/h`.

При 730 часах:

```text
RunPod A100 ≈ $1,161.70/month
Modal/HF A100 ≈ $1,825/month
HF GLM recipe ≈ $29,200/month
```

Self-host становится выгоден при устойчивой загрузке GPU, batching и большом объёме запросов. При нерегулярном трафике token API обычно дешевле.

## 10. Cocoon

Cocoon интересен как confidential/decentralized compute network с TON payments, TEE и worker/proxy architecture.

На момент snapshot:

- официальные docs не дают стабильной публичной таблицы `$ / 1M input` и `$ / 1M output`;
- deployment требует специализированного confidential hardware, включая TDX и H100-class GPU для worker-сценария;
- это не такой же turnkey multi-provider API, как OpenRouter;
- Cocoon стоит тестировать для privacy и decentralized compute, но не выбирать как основной production route без pilot с реальным cost, latency и uptime.

## 11. Скорость — обязательная метрика

Каждый будущий тест должен сохранять:

```text
model_id
provider_name
provider_model_id
input_tokens
cached_input_tokens
output_tokens
reasoning_tokens
reported_cost
TTFT
total_latency
output_tokens_per_second
retries
HTTP status/errors
tool_call_success
structured_output_success
ARC correctness
```

Текущий runner уже сохраняет cost, provider, retries, latency и output tok/s. Следующее расширение — streaming TTFT и отдельный direct-provider adapter.

## 12. Финальная routing policy на сегодня

```text
1. GPT-6 Luna OpenAI Standard — обычный универсальный agent.
2. DeepSeek V4 Flash 0731 DeepInfra — если output/input > 5%.
3. DeepSeek OpenRouter — если input очень длинный, output короткий или нужен fallback.
4. GLM-5.3-Flash — если quality важнее минимального token cost.
5. GPT-6.1 Sol — hard escalation.
6. GPT-OSS-120B — open-weight benchmark и дешёвая альтернатива.
7. Qwen3.8-27B — self-host pilot.
8. Llama-3.1-8B/GPT-OSS-20B — cheap classifier/planner.
```

## 13. Следующий эксперимент

Запустить одинаковый ARC subset минимум в трёх режимах:

```text
DeepSeek OpenRouter default
DeepSeek OpenRouter -> DeepInfra only
DeepSeek Direct DeepInfra
GPT-6 Luna OpenAI Standard
GPT-6 Luna Azure Standard
GPT-OSS-120B DeepInfra/Groq/Cerebras
Qwen3.8-27B OpenRouter/DeepInfra/Chutes
```

Критерии ranking:

```text
quality score
cost per solved task
cost per request
total latency
TTFT
output tok/s
availability
retries/errors
tool-call reliability
```

## 14. Все сохранённые детальные отчёты

- [ARC official + community](arc_agi2_results_2026-10-06.md)
- [OpenRouter snapshot](openrouter_snapshot_2026-10-06.md)
- [OpenRouter cost test](openrouter_cost_test_2026-10-06.md)
- [Decision snapshot](decision_snapshot_2026-10-06.md)
- [Open weights, HF, GPU, Cocoon](hosting_alternatives_open_weights_2026-10-06.md)
- [Direct open-weight API providers](direct_open_weight_api_providers_2026-10-06.md)
- [DeepInfra vs OpenRouter economics](deepseek_deepinfra_vs_openrouter_economics_2026-10-06.md)
- [GPT-6 Luna vs DeepSeek providers](openrouter_provider_comparison_gpt6_luna_deepseek_2026-10-06.md)

## 15. Основные внешние источники

- [ARC Prize leaderboard](https://arcprize.org/leaderboard)
- [ARC Prize community leaderboard](https://arcprize.org/leaderboard/community)
- [OpenRouter DeepSeek V4 Flash 0731](https://openrouter.ai/deepseek/deepseek-v4-flash-0731)
- [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
- [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
- [OpenRouter pricing](https://openrouter.ai/pricing)
- [DeepInfra pricing](https://deepinfra.com/pricing)
- [Hugging Face provider catalog](https://huggingface.co/inference/models)
- [Hugging Face Endpoints pricing](https://huggingface.co/docs/inference-endpoints/pricing)
- [Together AI pricing](https://www.together.ai/pricing)
- [Baseten pricing](https://www.baseten.co/pricing/)
- [Novita pricing](https://novita.ai/pricing)
- [Fireworks pricing](https://fireworks.ai/pricing)
- [Chutes pricing](https://chutes.ai/pricing)
- [SiliconFlow pricing](https://cloud-rd.siliconflow.cn/pricing)
- [RunPod pricing](https://www.runpod.io/pricing)
- [Modal pricing](https://modal.com/pricing)
- [Cocoon](https://cocoon.org/)
