# Прямые API для open-weight моделей — snapshot 2026-10-06

## Вывод

Универсального сервиса, который всегда дешевле OpenRouter, нет. Но для конкретных моделей разница заметная:

1. **DeepSeek V4 Flash 0731:** самый интересный прямой API сейчас — **DeepInfra**. Он дороже OpenRouter default route по input, но примерно в 7 раз дешевле по output. Для reasoning/output-heavy агента это даёт экономию примерно 2.8–4.3 раза на типовых профилях. Важно: OpenRouter можно закрепить на provider DeepInfra, тогда сравнивать нужно одинаковый upstream rate, а не model-level default price.
2. **GLM-5.3-Flash:** Together, Baseten, DeepInfra и Novita показывают примерно `$0.15/$0.50`, то есть дешевле OpenRouter не получается. Выбирать нужно по latency, rate limits и стабильности.
3. **GPT-OSS-120B и GPT-OSS-20B:** в текущем snapshot OpenRouter уже очень дешёвый — прямые HF routes обычно не дешевле. Groq и Cerebras нужны ради скорости, а не экономии.
4. **Qwen3.8-27B:** DeepInfra и Chutes могут быть немного дешевле OpenRouter, особенно при большом output.
5. **SiliconFlow:** интересен для китайской инфраструктуры, RMB-тарифов и временных off-peak цен, но текущие страницы показывают другие model IDs и тарифные окна, поэтому напрямую смешивать его с USD-ценами нельзя.

Главный кандидат для первой практической проверки: **OpenRouter default vs OpenRouter→DeepInfra vs DeepInfra Direct** на DeepSeek V4 Flash 0731. Второй тест: **Chutes против OpenRouter на Qwen3.8-27B и Qwen3-32B**.

## Сравнение цен на одинаковых моделях

Все суммы — USD за 1M токенов, если не указано иное. OpenRouter — наш live catalog snapshot из `data/raw/openrouter_models.json`. Direct API — официальные страницы провайдеров или текущий каталог Hugging Face для конкретного provider route.

### DeepSeek V4 Flash 0731

| Сервис | Input | Output | Оценка |
|---|---:|---:|---|
| OpenRouter `deepseek/deepseek-v4-flash-0731` | $0.009 | $1.28 | Очень дешёвый input, дорогой output |
| DeepInfra | $0.06 | $0.18 | Лучший найденный вариант для output-heavy |
| Baseten | $0.13 | $0.26 | Быстрый route по HF snapshot |
| Together AI | $0.14 | $0.28 | Сбалансированный direct route |
| Fireworks AI | $0.22 | $0.66 | Дороже DeepInfra/Together |
| Novita AI | $0.44 | $1.32 | Не лучший по цене |
| Chutes | $0.44 | $1.32 | TEE/privacy, но не price leader |

Тариф DeepInfra подтверждён на его pricing page: `$0.06` input и `$0.18` output. Тарифы остальных routes для одной и той же модели также видны в live HF provider catalog.

### GLM-5.3-Flash

| Сервис | Input | Output | Оценка |
|---|---:|---:|---|
| OpenRouter | $0.15 | $0.50 | Базовый ориентир |
| Together AI | $0.15 | $0.50 | Та же цена |
| Baseten | $0.15 | $0.50 | Та же цена; в snapshot выше throughput |
| DeepInfra | $0.15 | $0.50 | Та же цена |
| Novita AI | $0.15 | $0.50 | Та же цена |
| Fireworks AI | $0.15 | $0.50 | Та же цена |

Для GLM нужно выбирать не по цене токена, а по реально измеренным `TTFT`, output tok/s, retries, error rate и доступности нужных tool/structured-output функций.

### GPT-OSS-120B

| Сервис | Input | Output | Оценка |
|---|---:|---:|---|
| OpenRouter | $0.037 | $0.17 | В текущем snapshot дешевле прямых routes по input |
| HF/DeepInfra | $0.04 | $0.17 | Почти то же, но не дешевле OpenRouter |
| HF/Novita | $0.05 | $0.25 | Дороже |
| Fireworks AI | $0.15 | $0.60 | Дороже, возможно другой operational profile |
| Groq | $0.15 | $0.75 | Очень быстро, не дёшево |
| Cerebras | $0.35 | $0.75 | Максимальная скорость, не дёшево |

### Qwen3.8-27B

| Сервис | Input | Output | Оценка |
|---|---:|---:|---|
| OpenRouter `qwen/qwen3.8-27b` | $0.425 | $2.55 | Ориентир |
| HF/DeepInfra | $0.20 | $2.50 | Немного дешевле по обоим тарифам |
| Chutes | $0.24 | $2.20 | Лучший найденный output price; TEE route |
| HF/Cerebras | $0.99 | $1.49 | Очень быстрый, но input дороже |
| SiliconFlow | ¥3 input / ¥12 output | RMB | Другой регион/тарифный рынок, нужна отдельная проверка |

## Стоимость одинакового агентного запроса

### DeepSeek V4 Flash 0731: OpenRouter против DeepInfra

Числа ниже обновлены по текущей странице OpenRouter, где default/listed route показывает `$0.0079/$1.28`. Это не то же самое, что OpenRouter с принудительным `provider.only: ["deepinfra"]`: при pinned DeepInfra нужно сравнивать одинаковые `$0.06/$0.18`.

| Профиль | OpenRouter | DeepInfra | Экономия DeepInfra |
|---|---:|---:|---:|
| 12k input / 1k output | $0.001375 | $0.000900 | 1.53x |
| 20k input / 4k output | $0.005278 | $0.001920 | 2.75x |
| 20k input / 10k output | $0.012958 | $0.003000 | 4.32x |
| 100k input / 4k output | $0.005910 | $0.006720 | OpenRouter дешевле на 1.14x |

Вывод: **DeepInfra выгоднее, когда агент много думает и генерирует output. OpenRouter выгоднее, когда в запросе огромный input и короткий output.**

### Qwen3.8-27B: OpenRouter против DeepInfra и Chutes

| Профиль | OpenRouter | HF/DeepInfra | Chutes |
|---|---:|---:|---:|
| 20k input / 4k output | $0.018700 | $0.014000 | $0.013600 |
| 20k input / 10k output | $0.034600 | $0.029000 | $0.027000 |
| 100k input / 4k output | $0.052500 | $0.030000 | $0.032800 |

Для Qwen3.8-27B выигрыш есть, но абсолютные суммы небольшие. Важнее проверить, не съедается ли он latency, лимитами и отличием backend/quantization.

## Кто за что хорош

### DeepInfra

Лучший кандидат на экономию:

- прямой OpenAI-compatible API;
- нет долгосрочного контракта и upfront commitment на token pricing;
- DeepSeek V4 Flash 0731 — `$0.06/$0.18`;
- в HF snapshot также есть дешёвый GPT-OSS, Qwen и другие open models;
- особенно выгоден для reasoning-heavy сценариев с большим output.

Минусы: нужно отдельно проверить tool calling, structured outputs, rate limits, latency distribution и реальную доступность конкретной версии модели.

Источник: [DeepInfra pricing](https://deepinfra.com/pricing), [HF provider catalog](https://huggingface.co/inference/models).

### Together AI

Хороший production provider с большим каталогом open models и отдельными режимами serverless, provisioned throughput и dedicated inference. На текущем прайсе:

- GLM-5.3-Flash — `$0.15/$0.50`;
- DeepSeek V4 Flash 0731 — `$0.14/$0.28`;
- GPT-OSS-120B — `$0.15/$0.60`;
- есть dedicated GPU и batch/throughput варианты.

Для DeepSeek он проигрывает DeepInfra по цене, но может быть полезнее при предсказуемой production-нагрузке и необходимости более управляемой инфраструктуры.

Источник: [Together AI pricing](https://www.together.ai/pricing).

### Baseten

Baseten особенно интересен как быстрый route:

- DeepSeek V4 Flash 0731 — около `$0.13/$0.26`;
- GLM-5.3-Flash — `$0.15/$0.50`;
- каталог также предлагает dedicated/autoscaling deployment для своих или custom моделей.

Это не очевидный price leader, но хороший кандидат для speed test. Нужно учитывать rate limit и cold-start поведение в реальном аккаунте.

Источник: [Baseten pricing](https://www.baseten.co/pricing/).

### Novita AI

Novita имеет большой каталог open models и прямые тарифы, но для выбранных моделей не лидирует по стоимости:

- DeepSeek V4 Flash 0731 — `$0.44/$1.32`;
- GPT-OSS-120B — `$0.05/$0.25`;
- GPT-OSS-20B — `$0.04/$0.15`;
- GLM-5.3-Flash — `$0.15/$0.50`.

Novita стоит держать как дополнительный fallback и источник сравнения availability, но не как основной cheapest route для DeepSeek.

Источник: [Novita pricing](https://novita.ai/pricing).

### Fireworks AI

Fireworks удобен как production/enterprise provider с большим каталогом и готовыми playground/API. Для текущих моделей его цены обычно не ниже OpenRouter:

- DeepSeek V4 Flash 0731 — около `$0.22/$0.66`;
- GPT-OSS-120B — `$0.15/$0.60`;
- GLM-5.3-Flash — `$0.15/$0.50`.

Это скорее выбор за стабильность, tooling и enterprise-возможности, а не за минимальную цену токена.

Источники: [Fireworks pricing](https://fireworks.ai/pricing), [Fireworks model catalog](https://fireworks.ai/models).

### Groq и Cerebras

Эти сервисы нужно проверять ради скорости:

- Groq показывает около 500 tok/s для GPT-OSS-120B;
- Cerebras показывает около 3,000 tok/s для GPT-OSS-120B и около 1,850 tok/s для Qwen3.8-27B;
- но их listed token prices заметно выше DeepInfra и OpenRouter.

Они могут быть дешевле не по `$ / token`, а по **стоимости времени**: если агенту важен SLA и короткое wall-clock время, высокая скорость может уменьшить стоимость рабочего процесса. Это нужно считать по фактическому output и цене инфраструктуры.

Источники: [Groq supported models](https://console.groq.com/docs/models), [Cerebras pricing](https://www.cerebras.ai/pricing).

### Chutes

Chutes интересен по двум причинам:

- публичный API без subscription/minimum/markup tiers;
- private chute в TEE с оплатой GPU по секундам и автоматическим отключением idle instances.

Текущие public rates:

- Qwen3-32B — `$0.104/$0.416`;
- Qwen3.8-27B — `$0.24/$2.20`;
- DeepSeek V4 Flash 0731 — `$0.44/$1.32`.

Chutes не дешевле DeepInfra для DeepSeek, но может быть полезен для TEE, приватного deployment и self-host-подобного режима без постоянной оплаты простаивающей GPU.

Источник: [Chutes pricing](https://chutes.ai/pricing).

### SiliconFlow

SiliconFlow стоит проверить отдельно, если важны китайские регионы, RMB-оплата и китайские open models. На pricing page сейчас видны, например:

- DeepSeek V4 Flash: примерно ¥1.5/¥4.5 в off-peak и ¥3/¥9 в обычные часы;
- Qwen3.8-27B: примерно ¥3/¥12;
- есть бесплатные или временно бесплатные модели.

Но у SiliconFlow нужно внимательно сверять:

- точный model ID (`DeepSeek-V4-Flash` не всегда равен `DeepSeek-V4-Flash-0731`);
- единицы и порядок input/output;
- временные тарифные окна;
- регион обработки данных и доступность из нашей инфраструктуры.

Поэтому пока это **кандидат на отдельный regional benchmark**, а не готовый победитель глобального сравнения.

Источник: [SiliconFlow pricing](https://cloud-rd.siliconflow.cn/pricing).

### Replicate

Replicate полезен для большого каталога community-моделей и кастомных deployments, но для text-agent API обычно не является самым дешёвым путём:

- public models в основном тарифицируются за фактическое compute time;
- private/deployment models оплачиваются за время, пока instance online, включая idle;
- для некоторых моделей есть token pricing;
- есть cold boots и shared queues.

Это хороший инструмент для редких custom workloads и экспериментов, но не первый кандидат для постоянного agent loop.

Источник: [Replicate pricing](https://replicate.com/pricing), [billing behavior](https://replicate.com/docs/topics/billing).

## Итоговый рейтинг для нашей задачи

### Если нужна минимальная цена

1. **DeepSeek V4 Flash 0731 → DeepInfra** — особенно при большом output/reasoning.
2. **Qwen3.8-27B → Chutes или HF/DeepInfra** — проверить реальную latency и качество.
3. **GLM-5.3-Flash → любой удобный route** — цена почти одинаковая, выбирать по скорости и стабильности.

### Если нужна скорость

1. **GPT-OSS-120B → Cerebras или Groq**.
2. **Qwen3.8-27B → Cerebras**.
3. **DeepSeek/GLM → Baseten** как speed-oriented route.

### Если нужен production fallback

Рекомендованный набор ключей:

```text
primary cheap:     DeepInfra
second route:      OpenRouter
GLM route:         Together или Baseten
speed route:       Groq или Cerebras
private/TEE:       Chutes
regional fallback: SiliconFlow
```

## Что добавить в следующий скрипт

Нужно расширить `arc-explorer`, чтобы каждый ARC-run сохранял не только model ID, но и provider route:

```text
provider
provider_model_id
input_price_per_million
output_price_per_million
first_token_latency
total_latency
output_tokens_per_second
retries
http_status
tool_call_success
structured_output_success
```

Тестировать нужно одну и ту же модель у разных провайдеров, иначе сравнение provider и model смешивается. Первый обязательный matrix:

```text
DeepSeek V4 Flash 0731: OpenRouter / DeepInfra / Together / Baseten
GLM-5.3-Flash:          OpenRouter / Together / Baseten / DeepInfra
GPT-OSS-120B:           OpenRouter / DeepInfra / Groq / Cerebras
Qwen3.8-27B:            OpenRouter / DeepInfra / Chutes / Cerebras
```

## Источники

- [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models)
- [DeepInfra pricing](https://deepinfra.com/pricing)
- [Together AI pricing](https://www.together.ai/pricing)
- [Baseten pricing](https://www.baseten.co/pricing/)
- [Novita AI pricing](https://novita.ai/pricing)
- [Fireworks pricing](https://fireworks.ai/pricing)
- [Fireworks model catalog](https://fireworks.ai/models)
- [Chutes pricing](https://chutes.ai/pricing)
- [SiliconFlow pricing](https://cloud-rd.siliconflow.cn/pricing)
- [Hugging Face provider catalog](https://huggingface.co/inference/models)
- [Groq supported models](https://console.groq.com/docs/models)
- [Cerebras pricing](https://www.cerebras.ai/pricing)
- [Replicate pricing](https://replicate.com/pricing)
