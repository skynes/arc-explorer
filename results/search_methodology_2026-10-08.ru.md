# Методика поиска и сравнения

Дата исследования: **2026-10-08**.

Это протокол, по которому в репозитории ищутся кандидаты для ARC-AGI-2 и сравниваются качество, цена, скорость и пригодность для агентной системы.

## 1. Сначала задаём baseline и строгий фильтр

Для текущего сравнения:

- baseline: **GPT-6 Luna**;
- benchmark: **ARC-AGI-2**;
- результат кандидата должен быть выше результата baseline;
- input- и output-цены OpenRouter не должны быть выше цены Luna;
- общий профиль стоимости: **20 000 input / 4 000 output tokens**;
- дата и источники фиксируются в dated report.

Если меняется задача, явно меняются baseline, token-профиль или строгость фильтра. Модель, которая дешевле только при коротком output, считается условной альтернативой, а не универсальным победителем.

## 2. Где ищем результаты

Источники проверяем в таком порядке:

1. **ARC Prize Verified leaderboard** — официальный semi-private результат и ARC cost/task.
2. **ARC Prize Community leaderboard и связанные submissions** — community-результаты, но не Verified без явного подтверждения ARC.
3. **Независимые агрегаторы**, например TrustTheBench, чтобы находить user-like тесты, которых нет в официальной таблице.
4. **Kaggle ARC-AGI-2** — полезный источник, но submission или system score не равен автоматически тесту одной API-модели.
5. **GitHub, model cards, provider pages и публичные отчёты** — для новых кандидатов и контекста запуска.

Ищем и по названию, и по alias. Каждый найденный результат сначала является кандидатом на проверку: нужны модель, snapshot, split, score и URL.

## 3. Как маркируем доказательства

| Класс | Значение | Использование |
|---|---|---|
| `official_verified` | ARC Prize запустил или проверил результат | Может попасть в официальную таблицу |
| `community_self_reported` | Community submission или self-report | Отдельно, с `🟨*` |
| `independent_aggregate` | Сторонний агрегатор или пользовательский тест | Только screening, не называем Verified |
| `kaggle_submission` | Kaggle submission или system score | Показываем контекст submission |
| `measured_run` | Наш воспроизводимый API/provider запуск | Сильнейшее доказательство для конкретной конфигурации |

Official, community, Kaggle и measured данные не смешиваются в одну безымянную оценку.

## 3a. Правило community average

В публичных таблицах используются две отдельные колонки:

- `ARC official / Verified` — официальный результат ARC Prize, если он существует;
- `Среднее ARC community` — среднее арифметическое только сопоставимых independent/community наблюдений.

Для наблюдений `s1 ... sn` показывается `(s1 + ... + sn) / n`, а `n` указывается рядом со значением. Official score никогда не входит в это среднее. При `n=1` это среднее одного наблюдения, а не статистически устойчивый результат. Если отличаются prompt, harness, split, reasoning budget или число задач, результаты не объединяются и показываются отдельными protocol groups.

## 4. Проверяем точную модель

Для каждой строки записываем исходное название, версию или snapshot, дату, точный OpenRouter ID, ARC split, score, стоимость, URL и информацию о system/ensemble, reasoning budget, prompt, tools, retries и sampling. Preview-ярлыки и rolling provider IDs помечаем как provisional, если точное соответствие не доказано.

## 5. Считаем экономику OpenRouter

Проверяем catalog/API или точную страницу модели на дату исследования и сохраняем input price, output price, cache price, free/paid статус, providers, rate limits, tool calling и structured outputs.

Для обычного запроса:

```text
cost = input_tokens / 1,000,000 * input_price
     + output_tokens / 1,000,000 * output_price
```

Для общего профиля `20k/4k` Luna при `$0.10/$0.50` стоит примерно `$0.004`. Это не официальный ARC cost/task: в ARC могут входить retries, tools, ensemble, hidden reasoning и overhead. Если модели дешевле при разных traffic-профилях, указываем break-even, а не объявляем абсолютного победителя.

## 6. Отдельно сравниваем качество и скорость

```text
разница в п.п. = score кандидата - score baseline
относительное улучшение = (score кандидата - score baseline)
                         / score baseline * 100
```

Скорость — отдельная метрика: total latency, average latency, TTFT, output tokens/sec, provider, route, retries, errors, timeouts и token usage. Сравнение должно использовать одинаковые задачи, prompt, timeout, concurrency, temperature, max output и routing policy. Скорость нельзя выводить из цены или ARC score.

## 7. Правила рекомендации

Сначала оставляем только сопоставимый benchmark, разделяем статусы, применяем строгие score/price условия, затем сортируем по качеству, стоимости и operational reliability. Условные победители указываются отдельно. Free endpoints считаются experimental backup до проверки availability и rate limits. Production default выбирается только после проверки tool calling, structured output, latency, стабильности provider и recovery после ошибок.

`Σ ARC median (%)` в README — медиана official и community score, если доступны обе оценки; при двух значениях она совпадает с их средним арифметическим. Если доступна только одна оценка, используется она. Это показатель ARC quality, а не цена/качество; цены токенов и ARC cost/task остаются отдельными колонками. Σ не отменяет official/community статус.

### Роли маршрутизации

- `default` — самая дешёвая эффективная модель, а не любой самый дешёвый endpoint. В текущем срезе эффективность означает `Σ ARC median ≥ 65%` и хотя бы official или independent evidence; community-only/free-preview строки не проходят в production default. Кандидат также должен пройти базовые operational checks. Выбирается минимальная оценочная стоимость для стандартного профиля `20k input / 4k output`, затем проверяются tool calling, structured output, latency, стабильность provider и актуальная цена.
- `thinking` — самая дешёвая модель в высшем практическом quality-tier. Приоритет у official quality; если почти максимальная по качеству модель заметно дешевле абсолютного лидера, выбирается она. Поэтому сейчас используется GPT-6.1 Sol, а не GPT-6 Astra.
- Условные маршруты хранятся отдельно: модель может быть дешевле для длинного input и короткого output, но не подходить как default для output-heavy вызовов. Free и community-only модели остаются экспериментальными до проверки availability, privacy и воспроизводимости.

## 8. Обновление результата

Используем fetchers, сохраняем дату, URLs, IDs, assumptions и unresolved issues в dated Markdown report, обновляем `last.json` только для короткой конфигурации `default`/`thinking`, затем проверяем `git diff --check` и тесты:

```powershell
python scripts/fetch_arc.py
python scripts/fetch_community.py
python scripts/fetch_kaggle.py
python scripts/fetch_openrouter.py --all
python scripts/compare_arc.py
python scripts/compare_openrouter_costs.py
python -m pytest -q
```

Независимый ARC score выше Luna не доказывает общее превосходство: prompt, split, snapshot, reasoning budget, tools, retries и ensemble могли отличаться. Поэтому в таблицах всегда сохраняются слова **official**, **independent**, **conditional**, **estimated** и **measured**.

Источники: [ARC Prize](https://arcprize.org/leaderboard), [Community policy](https://arcprize.org/leaderboard/community), [TrustTheBench](https://www.trustthebench.com/benchmarks/arc-agi-2), [Kaggle](https://www.kaggle.com/competitions/arc-prize-2026-arc-agi-2/leaderboard), [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models).
