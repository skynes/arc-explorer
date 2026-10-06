# Текущее решение по маршрутизации — 2026-10-16

## Маршрутизация

```text
default  -> deepseek/deepseek-v4.1-flash
thinking -> openai/gpt-6.1-sol
```

## Правило выбора

`default` — самая дешёвая эффективная модель. `thinking` — самая дешёвая модель в высшем практическом quality-tier, с приоритетом успешного решения сложных задач.

Quality-сигнал — `Σ ARC median`: медиана official и community, если доступны обе оценки, иначе единственная доступная оценка. Community-only и free-preview строки остаются экспериментальными до проверки availability, privacy и воспроизводимости.

В этом срезе порог эффективности — `Σ ARC median ≥ 65%` и хотя бы official или independent evidence; community-only/free-preview строки не проходят в production default. Кандидат сравнивается на стандартном профиле `20k input / 4k output`. Затем учитываются tool calling, structured output, latency, стабильность provider и recovery после ошибок. Модель, которая дешевле только на длинном input и очень коротком output, указывается как условный маршрут.

## Почему default теперь V4.1 Flash

| Модель | ARC official | ARC community | Σ ARC median | Оценка 20k/4k |
|---|---:|---:|---:|---:|
| DeepSeek V4.1 Flash | 72,9% | 69,0% | **71,0%** | **~$0,00129** |
| DeepSeek V4 Flash 0731 | 61,4% | 68,5% | 65,0% | ~$0,00470 |
| GPT-6 Luna | 59,3% | 61,3% | 60,3% | ~$0,00400 |

V4.1 — лучший практический quality/value-кандидат в текущем наборе данных и дешевле Luna по текущей цене OpenRouter для стандартного профиля. Цена временная и должна быть перепроверена перед production.

## Почему thinking остаётся Sol

GPT-6.1 Sol имеет **94,2% official ARC-AGI-2** и стоимость около **$0,254 за ARC-задачу**. GPT-6 Astra немного выше — **95,0%**, но оценочная стоимость около **$1,12 за задачу**. Поэтому Sol — более дешёвая высокоэффективная эскалация при небольшой разнице в качестве.

## Условные альтернативы

- DeepSeek V4 Flash 0731 остаётся выгодным при очень длинном input и очень коротком output из-за исключительно дешёвого input.
- GPT-6 Luna остаётся compatibility fallback для workflows, где важнее предсказуемое поведение общего агента, tool calling или экономика большого output.
- MiMo и Space Bunny остаются community/experimental кандидатами до повторной проверки результатов и operational risks.

## Источники

- [ARC official против community](arc_agi2_dual_status_2026-10-16.ru.md)
- [Методика поиска и сравнения](search_methodology_2026-10-08.ru.md)
- [OpenRouter DeepSeek V4.1 Flash](https://openrouter.ai/deepseek/deepseek-v4.1-flash)
- [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
