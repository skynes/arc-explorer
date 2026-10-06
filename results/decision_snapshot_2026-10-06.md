# Decision snapshot — 2026-10-06

Зафиксированное состояние сравнения ARC-AGI-2 и OpenRouter на **2026-10-06**.

## Итоговый выбор для агентной системы

### Если нужна одна платная модель

**GPT-6 Luna** — текущий default для общего агентного цикла, включая output-heavy и translation-style задачи:

- OpenRouter: около `$0.10/M input` и `$0.50/M output`;
- при большом output может быть дешевле DeepSeek;
- в текущем сравнении сохраняет сильный баланс скорости, tool calling и structured outputs.

### Когда выбрать DeepSeek

**DeepSeek V4 Flash 0731** остаётся ARC/value-альтернативой:

- ARC-AGI-2 Verified: `61.4%` против `59.3%` у GPT-6 Luna;
- оценочная стоимость ARC-задачи: около `$0.042` против `$0.062`;
- длинный input и короткий или средний output;
- низкая input-cost и высокая скорость на подходящих provider routes.

Выбор зависит от отношения output/input: при output/input ниже примерно `11.8%` DeepSeek дешевле, выше этого порога GPT-6 Luna может быть выгоднее.

### Когда выбрать GLM

**GLM-5.3-Flash** — кандидат на более качественный основной агент, если небольшая разница в стоимости допустима. Его ARC-AGI-2 score и OpenRouter agentic-метрики выше, чем у DeepSeek и GPT-6 Luna в текущем сравнении.

## ARC-AGI-2 official

| Модель | Score | ARC cost/task |
|---|---:|---:|
| GPT-6.1 Sol | 94.2% | ~$0.254 |
| GLM-5.3-Flash | 65.8% | ~$0.093 |
| DeepSeek V4 Flash 0731 | 61.4% | ~$0.042 |
| GPT-5.6 Luna 2026-07-30 | 59.6% | ~$0.177 |
| GPT-6 Luna | 59.3% | ~$0.062 |

Эти значения относятся к ARC Prize Verified semi-private evaluation и не являются OpenRouter token pricing.

## OpenRouter cost-test

Каталожное сравнение выполнено для ARC-like и agentic token profiles:

| Профиль | Самый дешёвый платный вариант |
|---|---|
| 12k input / 1k output | DeepSeek — ~$0.001388/request |
| 20k input / 4k output | GPT-6 Luna — ~$0.004000/request |
| 20k input / 10k output | GPT-6 Luna — ~$0.007000/request |
| 100k input / 4k output | DeepSeek — ~$0.006020/request |

Dots3-Note Preview free имеет нулевую цену, но остаётся экспериментальным вариантом из-за rate limits и free-endpoint availability.

## Зафиксированная схема routing

```text
Основной агент:        openai/gpt-6-luna
ARC value/длинный input: deepseek/deepseek-v4-flash-0731
Качество выше цены:    z-ai/glm-5.3-flash
Сложная эскалация:     openai/gpt-6.1-sol
Эксперименты:          dots-studio/dots-3-note-preview:free
```

## Ограничения snapshot

- OpenRouter price fields могут меняться из-за provider routing, скидок и effective price.
- Cost-test моделирует токены; он ещё не заменяет реальный ARC run с одинаковыми задачами.
- Community results не являются ARC Prize Verified; public train и semi-private нельзя напрямую ранжировать вместе.

## Скорость — обязательная метрика дальше

В следующих runs сравниваем не только score и cost, но также total latency, output tokens/sec, provider route, retries/errors и availability. Для streaming-запусков дополнительно фиксируем TTFT — time to first token.

## Артефакты

- [ARC-AGI-2 official + community](arc_agi2_results_2026-10-06.md)
- [OpenRouter snapshot](openrouter_snapshot_2026-10-06.md)
- [OpenRouter cost-test](openrouter_cost_test_2026-10-06.md)
- [Live OpenRouter raw catalog](../data/raw/openrouter_models.json)
- [Cost comparison JSON](../data/processed/openrouter_cost_comparison.json)
- [Default model decision rationale — English](default_model_decision_2026-10-06.en.md)

## Источники

- [ARC Prize leaderboard](https://arcprize.org/leaderboard)
- [ARC Prize community leaderboard](https://arcprize.org/leaderboard/community)
- [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models)
- [DeepSeek V4 Flash 0731](https://openrouter.ai/deepseek/deepseek-v4-flash-0731)
- [GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
- [GLM 5.3 Flash](https://openrouter.ai/z-ai/glm-5.3-flash)
