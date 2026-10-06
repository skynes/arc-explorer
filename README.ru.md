# ARC-explorer

![График ARC-AGI-2](results/chart_06_10_26.png)

| Рекомендация | Статус | Модель | ARC official / Verified | Среднее ARC community | Стоимость ARC/задачу | Цена в каталоге OpenRouter | Дата исследования | Σ ARC median (%) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| Максимальное качество ARC, но дорого — thinking-эскалация | ✅ | GPT-6.1 Sol | 94,2% | 66,9% (n=1) | ~$0,254 | ~$2/M input; $10/M output | 2026-10-16 | 80,6% |
| Default — самая дешёвая эффективная модель | ✅ | DeepSeek V4.1 Flash | 72,9% | 69,0% (n=1) | — | ~$0,0357/M input; $0,1428/M output† | 2026-10-16 | 71,0% |
| ARC community candidate | 🟨* | MiMo-V2.6-Flash | — | 66,6% (n=1) | ~$0,003–$0,011 оц.* | ~$0,10/M input; $0,28/M output | 2026-10-16 | 66,6% |
| ARC value / альтернатива для длинного input | ✅ | DeepSeek V4 Flash 0731 | 61,4% | 68,5% (n=1) | ~$0,042 | ~$0,0044/M input; $1,152/M output | 2026-10-16 | 65,0% |
| Fallback для совместимости общего агента | ✅ | GPT-6 Luna | 59,3% | 61,3% (n=1) | ~$0,062 | ~$0,10/M input; $0,50/M output | 2026-10-16 | 60,3% |

`✅` официальный результат ARC Prize Verified · `🟨*` в этой таблице нет ARC Prize Verified результата. `ARC official / Verified` и `Среднее ARC community` намеренно разделены. Среднее считается только по independent/community наблюдениям; `(n=1)` означает один сопоставимый результат и не доказывает воспроизводимость ([источник](https://www.trustthebench.com/benchmarks/arc-agi-2)).

`*` В неофициальном результате для MiMo стоимость ARC-задачи не указана. Диапазон выше — оценка OpenRouter для одного запроса на задачу по `$0,10/M` input и `$0,28/M` output: 20k/4k токенов ≈ `$0,0031`, 20k/10k ≈ `$0,0048`, 100k/4k ≈ `$0,0111` за задачу ([цены OpenRouter](https://openrouter.ai/xiaomi/mimo-v2.6-flash-20260921)). Это не официальная стоимость ARC Prize; retries, tools, ensemble и overhead провайдера не включены.

`Σ ARC median` — медиана official и community score, если доступны обе оценки; при двух значениях она совпадает с их средним арифметическим. Если есть только одна, используется доступная оценка. Это показатель качества ARC, а не цена/качество; цены остаются отдельными, чтобы рекомендации различали качество и эксплуатационные расходы. Стоимость ARC-задачи исключается, если она отсутствует или несопоставима. Цена V4.1 со знаком `†` — текущая скидочная цена OpenRouter и может измениться.

Машиночитаемая конфигурация маршрутизации: [GitHub last.json](https://github.com/skynes/arc-explorer/blob/main/last.json) · [raw last.json](https://raw.githubusercontent.com/skynes/arc-explorer/main/last.json)

---

Воспроизводимый исследовательский набор для сравнения ARC-AGI-2, community submissions, экономики OpenRouter, provider routing, open-weight моделей и альтернативных inference-платформ.

Основной язык документации — **английский**: [README.md](README.md). Китайская версия: [README.zh-CN.md](README.zh-CN.md).

## Что отслеживается

1. **ARC Prize Verified** — официальные semi-private результаты ARC-AGI-2.
2. **Community** — self-reported результаты, которые не смешиваются с Verified.
3. **Kaggle** — конкурсные submissions, не всегда эквивалентные тесту одной API-модели.
4. **OpenRouter** — каталог, provider routing, цены, latency, throughput и availability.
5. **Прямые провайдеры** — DeepInfra, Together, Baseten, Novita, Fireworks, Chutes, SiliconFlow, Groq, Cerebras и другие.
6. **Open-weight hosting** — Hugging Face, GPU rental, self-host и Cocoon.

## Быстрый запуск

Требуется Python 3.11+.

```powershell
cd arc-explorer
python -m pip install -r requirements.txt
python scripts/fetch_arc.py
python scripts/fetch_community.py
python scripts/fetch_kaggle.py
python scripts/fetch_openrouter.py --all
python scripts/compare_arc.py
python scripts/compare_openrouter_costs.py
python -m pytest -q
```

`run_openrouter_arc.py` сохраняет score, token usage, cost, provider, retries, errors, latency и output tokens/sec. Следующее расширение — TTFT для streaming-запросов.

## Текущий вывод

- GPT-6.1 Sol — самое высокое качество в этой таблице и thinking-эскалация, но модель дорогая.
- DeepSeek V4.1 Flash теперь `default`: самая дешёвая эффективная модель по текущему стандартному профилю, с 72,9% official, 69,0% independent и ценой OpenRouter ниже Luna.
- GPT-6 Luna сохранён как fallback для совместимости общего агента, когда важнее предсказуемые tool workflows или экономика большого output, чем текущий ARC/value-рейтинг.
- DeepSeek V4 Flash 0731 — альтернатива для длинного input и короткого output: input очень дешёвый, output дорогой.
- MiMo-V2.6-Flash — community-кандидат без official-подтверждения; цена привлекательна, но есть только одно independent-наблюдение.
- Space Bunny Alpha — экспериментальный free-preview от анонимного provider, не production-рекомендация.
- GLM-5.3-Flash — кандидат с приоритетом качества.
- Независимый ARC-screen: GLM 5.3 Flash — лучший платный кандидат, который строго не дороже Luna; QwQ 32B и Nemotron free — экспериментальные backup-кандидаты.
- GPT-6.1 Sol — эскалация сложных задач.
- GPT-OSS-120B — главный hosted open-weight кандидат.
- Qwen3.8-27B — практичный self-host pilot.

Для DeepSeek provider selection существенно влияет на цену. DeepInfra может быть дешевле текущего default-route OpenRouter, если output превышает примерно 4.74% от input. Если OpenRouter закреплён именно на DeepInfra, token-cost примерно одинаков; различаются routing, fallback, billing и platform overhead.

## Методика выбора моделей

`default` и `thinking` — это роли маршрутизации, а не утверждение, что одна модель выигрывает любую нагрузку.

- **Default = самая дешёвая эффективная модель.** В этом срезе порог эффективности — `Σ ARC median ≥ 65%` и хотя бы official или independent evidence; community-only/free-preview строки не подходят для production default. `Σ ARC median` — медиана official и community, если доступны обе оценки, иначе доступная оценка. Среди прошедших порог кандидатов выбирается минимальная оценочная стоимость для профиля `20k input / 4k output`. Перед production нужно перепроверить tool calling, structured output, latency, стабильность provider и цену.
- **Thinking = самая дешёвая модель высокого качества для эскалации.** Сначала выбирается сильный quality-tier по official evidence; если модель почти максимального качества заметно дешевле абсолютного лидера, выбирается она. Поэтому `thinking` остаётся GPT-6.1 Sol: 94,2% official при существенно меньшей ARC-стоимости, чем GPT-6 Astra.
- **Условные маршруты указываются отдельно.** DeepSeek V4 Flash 0731 может выигрывать на очень длинном input и очень коротком output из-за дешёвого input. Free/community-only модели остаются экспериментальными до проверки availability, privacy и воспроизводимости.

## Отчёты

- [Полный research snapshot](results/research_snapshot_all_2026-10-06.md)
- [ARC official и community](results/arc_agi2_results_2026-10-06.md)
- [Независимые ARC-кандидаты против GPT-6 Luna](results/community_arc_candidates_vs_gpt6_luna_2026-10-08.ru.md)
- [ARC official против community averages — 2026-10-16](results/arc_agi2_dual_status_2026-10-16.ru.md)
- [Методика поиска и сравнения](results/search_methodology_2026-10-08.ru.md)
- [OpenRouter snapshot](results/openrouter_snapshot_2026-10-06.md)
- [OpenRouter cost test](results/openrouter_cost_test_2026-10-06.md)
- [Decision snapshot](results/decision_snapshot_2026-10-06.md)
- [Open weights, HF, GPU и Cocoon](results/hosting_alternatives_open_weights_2026-10-06.md)
- [Direct open-weight API providers](results/direct_open_weight_api_providers_2026-10-06.md)
- [DeepInfra vs OpenRouter economics](results/deepseek_deepinfra_vs_openrouter_economics_2026-10-06.md)
- [GPT-6 Luna vs DeepSeek providers](results/openrouter_provider_comparison_gpt6_luna_deepseek_2026-10-06.md)
- [Default model decision rationale — English](results/default_model_decision_2026-10-06.en.md)
- [Текущее решение по маршрутизации — 2026-10-16](results/default_model_decision_2026-10-16.ru.md)

## Структура

```text
config/      aliases моделей и настройки сравнений
data/        snapshots и игнорируемые live/raw данные
results/     датированные отчёты
scripts/     fetchers, сравнения, cost tests и ARC runner
tests/       unit-тесты
```

Новые документы пишутся на английском и сопровождаются русской и китайской публичными сводками. Цены и provider metrics всегда получают дату и URL источника.

## Лицензия

Проект распространяется по [лицензии MIT](LICENSE).

## Участие в проекте

Исправления, обновления источников, измерения провайдеров, сравнения новых моделей и предложения по улучшению приветствуются. Желательно указывать дату получения данных, URL источника, ID модели/провайдера и контекст для воспроизведения результата.
