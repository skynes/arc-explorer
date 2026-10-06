# DeepSeek V4 Flash 0731: DeepInfra vs OpenRouter — экономика

Дата расчёта: **2026-10-06**.

## Главное уточнение

Нельзя корректно говорить просто «DeepInfra в 2.8–4.3 раза дешевле OpenRouter» без указания маршрута.

OpenRouter на странице модели сейчас показывает:

- модельный/default route: **$0.0079/M input и $1.28/M output**;
- отдельный provider DeepInfra: **$0.06/M input и $0.18/M output**.

OpenRouter также позволяет выбрать конкретного provider через `provider.order` или `provider.only`. Поэтому есть три разных сравнения:

| Режим | Input / 1M | Output / 1M | Что сравниваем |
|---|---:|---:|---|
| OpenRouter default/listed route | $0.0079 | $1.28 | Текущий default price на странице модели |
| OpenRouter → DeepInfra | $0.06 | $0.18 | Тот же upstream DeepInfra через gateway |
| DeepInfra Direct API | $0.06 | $0.18 | Прямой API DeepInfra |

**Точный вывод:** экономия 2.8–4.3 раза относится к сравнению с OpenRouter default/listed route, а не гарантированно к OpenRouter, если он уже отправляет запрос на DeepInfra. При OpenRouter → DeepInfra token-rate почти тот же; тогда разница — в gateway, routing/fallback, биллинге и platform fee.

Источники: [OpenRouter model page](https://openrouter.ai/deepseek/deepseek-v4-flash-0731), [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [DeepInfra pricing](https://deepinfra.com/pricing).

## Формула

```text
cost = input_tokens / 1,000,000 * input_price
     + output_tokens / 1,000,000 * output_price
```

Расчёты ниже используют uncached tokens и USD. VAT, платёжные комиссии, скидки и retries не включены.

## Цена одного запроса

| Профиль | OpenRouter default | DeepInfra Direct | Разница | Экономия DeepInfra |
|---|---:|---:|---:|---:|
| 12k input / 1k output | $0.0013748 | $0.0009000 | −$0.0004748 | 34.5% / 1.53x |
| 20k input / 4k output | $0.0052780 | $0.0019200 | −$0.0033580 | 63.6% / 2.75x |
| 20k input / 10k output | $0.0129580 | $0.0030000 | −$0.0099580 | 76.8% / 4.32x |
| 100k input / 4k output | $0.0059100 | $0.0067200 | +$0.0008100 | DeepInfra дороже на 13.7% |
| 100k input / 20k output | $0.0263900 | $0.0096000 | −$0.0167900 | 63.6% / 2.75x |

### Проверка арифметики для обычного agent loop

Профиль: `20,000 input + 4,000 output`.

```text
OpenRouter = 20,000 / 1,000,000 * $0.0079
           + 4,000 / 1,000,000 * $1.28
           = $0.000158 + $0.005120
           = $0.005278

DeepInfra  = 20,000 / 1,000,000 * $0.06
           + 4,000 / 1,000,000 * $0.18
           = $0.001200 + $0.000720
           = $0.001920

Ограниченная экономия = $0.005278 / $0.001920 = 2.749x
Процентная экономия = 1 - $0.001920 / $0.005278 = 63.62%
```

## Точка безубыточности

Обозначим `r = output_tokens / input_tokens`.

DeepInfra дешевле default OpenRouter, когда:

```text
0.06 * input + 0.18 * output
    < 0.0079 * input + 1.28 * output

output / input > (0.06 - 0.0079) / (1.28 - 0.18)
output / input > 0.04736
```

То есть **DeepInfra дешевле, если output превышает примерно 4.74% от input**.

Эквивалентно:

- 20k input → достаточно больше примерно 947 output tokens;
- 100k input → достаточно больше примерно 4,736 output tokens;
- 1M input → достаточно больше примерно 47,364 output tokens.

Для agentic reasoning это обычно выполняется. Для RAG/длинного контекста с коротким ответом — нет.

## Экономия за месяц

### 10,000 обычных agent loops в месяц

Профиль каждого запроса: `20k input / 4k output`.

| Режим | Стоимость/месяц |
|---|---:|
| OpenRouter default | $52.78 |
| DeepInfra Direct | $19.20 |
| Экономия | **$33.58/месяц** |

### 100,000 обычных agent loops в месяц

| Режим | Стоимость/месяц |
|---|---:|
| OpenRouter default | $527.80 |
| DeepInfra Direct | $192.00 |
| Экономия | **$335.80/месяц** |

### 10,000 reasoning-heavy loops в месяц

Профиль: `20k input / 10k output`.

| Режим | Стоимость/месяц |
|---|---:|
| OpenRouter default | $129.58 |
| DeepInfra Direct | $30.00 |
| Экономия | **$99.58/месяц** |

### 10,000 длинных контекстов в месяц

Профиль: `100k input / 4k output`.

| Режим | Стоимость/месяц |
|---|---:|
| OpenRouter default | $59.10 |
| DeepInfra Direct | $67.20 |
| Переплата DeepInfra | **$8.10/месяц** |

## Что меняется при OpenRouter → DeepInfra

Если в запросе OpenRouter явно указать только DeepInfra:

```json
{
  "provider": {
    "only": ["deepinfra"],
    "allow_fallbacks": false
  }
}
```

то сравнение с прямым DeepInfra должно использовать `$0.06/$0.18` и с обеих сторон получится примерно одинаковая token-cost.

Тогда OpenRouter всё ещё даёт:

- единый API и единый ключ;
- автоматический fallback, если разрешить его;
- публичные latency/throughput/uptime метрики;
- замену provider без изменения приложения;
- централизованный usage tracking.

Прямой DeepInfra даёт:

- отсутствие дополнительного gateway;
- отдельные rate limits и billing;
- прямой контроль аккаунта провайдера;
- меньше зависимости от OpenRouter как дополнительного слоя.

У OpenRouter Standard сейчас заявлена platform fee **5.5%**, а в документации также указано, что provider pricing передаётся без model markup. Поэтому фактический итог зависит от того, где именно применяется fee к аккаунту и покупке credits. Для production нужно сравнивать не только прайс-лист, но и две реальные квитанции/usage records.

Если для грубой оценки считать эти 5.5% как добавку к OpenRouter model spend, обычный `20k/4k` меняется с `$0.005278` на `$0.005568`; отношение к DeepInfra становится **2.90x вместо 2.75x**. Это чувствительность расчёта, а не утверждение о конкретной строке invoice.

## Кэширование

В текущем snapshot OpenRouter показывает cache-read около `$0.0079/M`, а DeepInfra — около `$0.015/M` cached input. Если большая часть prompt попадает в cache, преимущество DeepInfra по input исчезает или уменьшается. Output-heavy вывод остаётся тем же: `$0.18/M` против `$1.28/M`.

Для повторяющегося агентного контекста нужно считать отдельно:

```text
uncached_input_tokens
cached_input_tokens
output_tokens
cache_hit_rate
```

## Когда выбирать DeepInfra Direct

Выбирать DeepInfra напрямую имеет смысл, если одновременно выполняются условия:

- output/input выше примерно 4.7%;
- нет большой экономии от OpenRouter prompt-cache;
- устраивает latency и tool/JSON compatibility;
- допустим single-provider risk или есть свой fallback;
- объём запросов оправдывает второй API key и отдельный monitoring.

Для нашего агента это означает:

```text
сложное reasoning с длинным ответом -> DeepInfra Direct
длинный input и короткое действие   -> OpenRouter
нужен fallback без своей логики      -> OpenRouter
нужна максимальная прозрачность cost -> Direct DeepInfra
```

## Как подтвердить реальной серией запросов

Нужно прогнать минимум 100–1,000 одинаковых запросов в трёх режимах:

1. OpenRouter default;
2. OpenRouter с `provider.only = ["deepinfra"]`;
3. DeepInfra Direct.

Для каждого запроса сохранять:

- prompt tokens;
- cached input tokens;
- completion/output tokens;
- reasoning tokens, если возвращаются отдельно;
- reported cost;
- provider/model ID;
- TTFT и total latency;
- output tok/s;
- retries, HTTP errors и timeout;
- correctness на ARC-задаче.

Ключевая проверка — сравнить фактический `usage.cost`, а не только цену в каталоге. Это также покажет, одинаковая ли версия/quantization реально отвечает через Direct и OpenRouter → DeepInfra.

## Итог

Фраза «DeepInfra дешевле OpenRouter в 2.8–4.3 раза» **верна только для output-heavy сценариев, если сравнивать прямой DeepInfra с текущим OpenRouter default/listed route**.

Более точная policy:

- `20k/4k`: DeepInfra дешевле примерно **2.75x**;
- `20k/10k`: DeepInfra дешевле примерно **4.32x**;
- `100k/4k`: OpenRouter дешевле примерно **1.14x**;
- OpenRouter, закреплённый на DeepInfra, по token-rate примерно равен Direct DeepInfra.

Для агентной системы я бы сделал routing по фактическому соотношению output/input: **при output/input > 5% отправлять в DeepInfra, при меньшем соотношении — оставлять OpenRouter**, но обязательно подтвердить это реальным A/B-run с usage и speed metrics.

## Источники

- [OpenRouter DeepSeek V4 Flash 0731](https://openrouter.ai/deepseek/deepseek-v4-flash-0731)
- [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
- [OpenRouter pricing](https://openrouter.ai/pricing)
- [OpenRouter support: provider pricing](https://openrouter.ai/support)
- [DeepInfra pricing](https://deepinfra.com/pricing)
