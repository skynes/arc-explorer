# Open weights, Hugging Face, GPU rental и Cocoon — snapshot 2026-10-06

## Короткий вывод

Для агентной системы сейчас разумно разделить задачу на два слоя:

1. **Без DevOps и с маленьким/средним трафиком:** прямой Hugging Face Inference Provider или API конкретного провайдера. Это иногда дешевле OpenRouter, но не всегда.
2. **С постоянной нагрузкой:** self-host открытой модели на арендованном GPU. Экономия появляется только при хорошей загрузке GPU; при простое API обычно дешевле.

### Мой текущий shortlist

| Сценарий | Что проверять первым | Почему |
|---|---|---|
| Дешёвый сильный hosted open-weight агент | `openai/gpt-oss-120b` через DeepInfra/Novita | В live-каталоге HF примерно $0.04–0.05 input и $0.17–0.25 output за 1M токенов; есть tool calling и structured output |
| Максимум скорости | `openai/gpt-oss-120b` через Cerebras/Groq | В каталоге HF зафиксированы очень высокие throughput, но цена выше и это нужно подтвердить своим workload |
| Дешёвый помощник/маршрутизатор | `openai/gpt-oss-20b`, `Llama-3.1-8B-Instruct`, `Qwen3-4B-Instruct-2507` | Низкая цена, быстрые ответы, подходят для классификации, pre-processing и простых tool calls |
| Доступный self-host | `Qwen3.8-27B` или модель класса 27–32B | Реалистичная цель для одной большой GPU; не требует кластера уровня 321B-модели |
| Сохранить текущий ARC-quality без самостоятельной инфраструктуры | DeepSeek V4 Flash / GLM-5.3-Flash через лучшего прямого провайдера | Большие MoE-модели открыты, но их самостоятельно размещать дорого и сложно |
| Приватный/децентрализованный эксперимент | Cocoon | Интересная confidential compute-сеть, но пока нет публичной сопоставимой token-price таблицы и это не turnkey API |

Главная практическая рекомендация: **для следующего теста добавить `gpt-oss-120b`, `gpt-oss-20b`, `Qwen3.8-27B` и `Llama-3.1-8B-Instruct`; затем прогнать их на одном и том же наборе ARC-задач, с одинаковым prompt и отдельным замером score, latency, output tok/s, retries и cost.** Сейчас у нас есть цены и инфраструктурные данные, но не независимый ARC-AGI-2 run для этих моделей.

## Что значит «открытые веса»

Открытые веса не означают, что модель дёшево запускать самостоятельно. Нужно учитывать:

- размер весов и KV-cache;
- число GPU и объём VRAM;
- quantization и возможную потерю качества;
- throughput при одном запросе и при batch-нагрузке;
- простой GPU и cold start;
- стоимость хранения, трафика, observability и эксплуатации.

Например, `GLM-5.3-Flash` и `DeepSeek-V4-Flash-0731` открыты, но это всё равно очень крупные MoE-модели. Наличие веса в Hugging Face не делает их эквивалентом 8B или 27B модели по стоимости self-host.

## Live-цены Hugging Face Inference Providers

Цены ниже — снимок каталога Hugging Face на 2026-10-06, USD за 1M input/output tokens. Это serverless API через провайдера, а не цена аренды собственной GPU. Latency и throughput — значения, которые каталог HF показывает для соответствующего provider route; это не гарантия для нашего prompt или региона.

| Модель | Provider route | Input | Output | Latency | Output tok/s | Комментарий |
|---|---:|---:|---:|---:|---:|---|
| DeepSeek-V4-Flash-0731 | DeepInfra | $0.06 | $0.18 | 0.36 s | 33 | Самый дешёвый найденный HF route |
| DeepSeek-V4-Flash-0731 | Baseten | $0.13 | $0.26 | 0.36 s | 167 | Лучший live throughput в текущем snapshot |
| DeepSeek-V4-Flash-0731 | Together | $0.14 | $0.28 | 0.45 s | 46 | Сбалансированный route |
| DeepSeek-V4-Flash-0731 | Novita | $0.44 | $1.32 | 0.88 s | 104 | Существенно дороже |
| GLM-5.3-Flash | Together | $0.15 | $0.50 | 0.30 s | 64 | Та же базовая цена, что в OpenRouter API snapshot |
| GLM-5.3-Flash | Baseten | $0.15 | $0.50 | 0.36 s | 119 | Лучший throughput из показанных |
| GLM-5.3-Flash | DeepInfra | $0.15 | $0.50 | 0.57 s | 27 | Дешевле не по прайсу, а возможен выигрыш по доступности/маршруту |
| `gpt-oss-120b` | DeepInfra | $0.04 | $0.17 | 0.88 s | 48 | Самая интересная цена среди сильных open-weight кандидатов |
| `gpt-oss-120b` | Novita | $0.05 | $0.25 | 0.52 s | 65 | Дешёвый альтернативный route |
| `gpt-oss-120b` | Groq | $0.15 | $0.75 | 0.29 s | 425 | Быстро, но дороже |
| `gpt-oss-120b` | Cerebras | $0.35 | $0.75 | 0.16 s | 1,078 | Максимальная скорость в каталоге, цена заметно выше |
| `gpt-oss-20b` | DeepInfra | $0.03 | $0.14 | 0.28 s | 98 | Дешёвый агентный baseline |
| `gpt-oss-20b` | Groq | $0.10 | $0.50 | 0.29 s | 687 | Быстрый route |
| Llama-3.1-8B-Instruct | Novita | $0.02 | $0.05 | 0.47 s | 172 | Очень дешёвый простой baseline |
| Llama-3.1-8B-Instruct | DeepInfra | $0.02 | $0.05 | 0.45 s | 25 | Цена та же, throughput другой |
| Qwen3.8-27B | DeepInfra | $0.20 | $2.50 | 0.48 s | 56 | Интересен как self-host-класс, но hosted output дороже |
| Qwen3.8-27B | Novita | $0.42 | $3.00 | 0.68 s | 40 | Дороже DeepInfra |
| Gemma-4-31B-it | Novita | $0.14 | $0.40 | 0.73 s | 35 | Практичный средний open-weight вариант |
| Kimi-K3 | Together | $2.70 | $13.50 | 2.84 s | 47 | Слишком дорогой для дешёвого default-agent |

Источник таблицы: [Hugging Face Inference Providers — Supported Models](https://huggingface.co/inference/models). HF пишет, что при использовании provider routing не добавляет собственную наценку, но тариф и SLA определяет конкретный провайдер.

## Сравнение DeepSeek через OpenRouter и HF

В текущем OpenRouter snapshot для `DeepSeek V4 Flash 0731` было около `$0.0103/M input` и `$1.28/M output`. В HF-каталоге DeepInfra — `$0.06/M input` и `$0.18/M output`.

Это важный пример: HF не дешевле по каждому типу токенов. Он дороже на input, но намного дешевле на output.

| Профиль | OpenRouter DeepSeek | HF DeepInfra DeepSeek | Кто дешевле |
|---|---:|---:|---|
| 12k input / 1k output | ~$0.001404 | ~$0.000900 | HF, ~1.56x |
| 20k input / 4k output | ~$0.005326 | ~$0.001920 | HF, ~2.77x |
| 20k input / 10k output | ~$0.013006 | ~$0.003000 | HF, ~4.34x |
| 100k input / 4k output | ~$0.006150 | ~$0.006720 | OpenRouter, ~1.09x |

Расчёт использует формулу:

```text
cost = input_tokens / 1_000_000 * input_price
     + output_tokens / 1_000_000 * output_price
```

Вывод: для агентного цикла с большим reasoning/output прямой HF provider может быть дешевле OpenRouter; для длинного повторяющегося контекста и короткого ответа OpenRouter может выиграть из-за очень дешёвого input.

## Модели с открытыми весами, которые стоит добавить в ARC-тест

### `openai/gpt-oss-120b`

Это официальный open-weight выпуск OpenAI для reasoning и agentic workflows. HF предоставляет совместимый с OpenAI API доступ, tool calling, structured outputs и reasoning controls. В текущем HF-каталоге диапазон заметно различается по провайдеру: примерно `$0.04/$0.17` у DeepInfra, `$0.05/$0.25` у Novita, `$0.15/$0.75` у Groq и `$0.35/$0.75` у Cerebras.

Это **главный кандидат для честного сравнения с дорогими hosted-моделями**, но его нужно проверить на ARC-AGI-2: token-price и качество на ARC — разные свойства.

Источники: [официальная инструкция OpenAI gpt-oss на HF](https://huggingface.co/docs/inference-providers/en/guides/gpt-oss), [карточка gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b).

### `openai/gpt-oss-20b`

Практичный недорогой агентный baseline. В текущем каталоге HF DeepInfra показывает около `$0.03/$0.14`, а Novita около `$0.04/$0.15`. Его стоит использовать как router/planner и для простых задач, но не предполагать, что он сохранит качество GPT-6 Luna или GLM на сложных ARC-пазлах.

### `Qwen3.8-27B`

Хороший кандидат именно для self-host эксперимента: 27B-класс заметно реалистичнее для одной большой GPU, чем 120B–321B модели. В HF-каталоге есть provider route DeepInfra около `$0.20/$2.50`, а официальная HF Endpoint-рецептура показывает размещение на одной A100 за примерно `$2.50/h` с возможностью scale-to-zero.

Это не означает, что endpoint автоматически дешевле API: при малом трафике оплата простаивающей GPU проиграет token billing. Зато модель удобна для controlled benchmark, приватных данных и постоянной нагрузки.

Источники: [карточка Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B), [HF Endpoint recipe](https://endpoints.huggingface.co/new/Qwen/Qwen3.8-27B?recipe=russet-croissant-3555p81s).

### `Llama-3.1-8B-Instruct`

Это не претендент на максимальное ARC-качество, а нижняя граница стоимости и latency. В HF snapshot около `$0.02/$0.05`, при этом один из routes показывает примерно 172 output tok/s. Его полезно включить как дешёвый pre-check: классифицировать запрос, извлекать структуру, выбрать tool или решить, нужна ли эскалация.

Источник: [HF provider page](https://huggingface.co/inference/models?model=meta-llama%2FLlama-3.1-8B-Instruct).

### `GLM-5.3-Flash` и `DeepSeek-V4-Flash-0731`

Обе модели имеют открытые веса и сильны по текущим ARC-данным, но self-host для них не равен запуску 8B модели:

- для DeepSeek V4 Flash 0731 OpenRouter показывает примерно 284B total и около 13B active parameters;
- GLM-5.3-Flash — примерно 321B-класс; официальная HF Endpoint-рецептура показывает 8×H200 и около `$40/h` за работающую реплику;
- HF provider API проще и часто экономичнее, пока нет постоянной высокой загрузки кластера.

Для GLM-5.3-Flash официальная HF provider цена около `$0.15/$0.50`, поэтому переход с OpenRouter на HF не даёт автоматической экономии. Проверять нужно конкретный provider route, latency, retries и реальную итоговую цену.

Источник размера и deployment-рецептуры: [HF GLM-5.3-Flash Endpoint](https://endpoints.huggingface.co/new/zai-org/GLM-5.3-Flash).

### `Kimi-K3`, `MiniMax M2.5`, `Ling-3.0-flash`

Это важные популярные open-weight направления, но для текущей цели они не являются первыми кандидатами на дешёвый self-host:

- **Kimi-K3**: в HF каталоге около `$2.70/$13.50` у Together и выше у других routes; модель очень крупная, поэтому hosted API разумнее локального запуска для большинства небольших команд.
- **MiniMax M2.5**: официальная карточка описывает модель как agent-native open model и приводит ориентир для M2.5 Lightning около `$0.30/$2.40`; перед сравнением надо зафиксировать, относится ли этот тариф к конкретному API route, а не к self-host.
- **Ling-3.0-flash**: 124B total и 5.1B active; карточка рекомендует 4× 141GB-class GPU для low-latency recipe или 8×H100 для 80GB-карт. Это интересная модель для крупного inference-кластера, но не дешёвый одиночный сервер.

Источники: [Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3), [MiniMax M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5), [Ling-3.0-flash](https://huggingface.co/inclusionAI/Ling-3.0-flash).

## Где запускать дешевле OpenRouter

### 1. Hugging Face Inference Providers

Это самый простой следующий шаг:

- единый OpenAI-compatible endpoint;
- доступ к множеству provider routes;
- нет обязательного self-host;
- можно выбирать provider отдельно для цены и скорости;
- HF сообщает, что сам не добавляет markup к цене провайдера.

Ограничение: стоимость, rate limits, availability и tool support всё равно зависят от выбранного provider. Для production agent нужно логировать provider в каждом запросе, иначе сравнение будет нечестным.

Источник: [HF Inference Providers pricing](https://huggingface.co/docs/inference-providers/pricing).

### 2. Dedicated Hugging Face Inference Endpoint

Оплата идёт за время работы реплики, а не за число токенов. По текущей таблице HF:

- T4 — около `$0.50/h`;
- L4 — около `$0.80/h`;
- A10G — около `$1.00/h`;
- L40S — около `$1.80/h`;
- A100 — около `$2.50/h`;
- GLM-5.3-Flash в официальном recipe — 8×H200, около `$40/h`.

При 730 часах в месяце одна A100 за `$2.50/h` — примерно `$1,825/month`, а GLM recipe 8×H200 — примерно `$29,200/month`, ещё до storage, traffic и operations. Scale-to-zero снижает простой, но добавляет cold start.

Источник: [HF Inference Endpoints pricing](https://huggingface.co/docs/inference-endpoints/pricing), [autoscaling](https://huggingface.co/docs/inference-endpoints/guides/autoscaling).

### 3. RunPod, Modal и Vast.ai

Для controlled self-host benchmark они интереснее HF Endpoint, потому что можно выбирать образ, vLLM/SGLang, quantization и свои логи.

| Платформа | Ориентир из текущего прайса | Практический смысл |
|---|---:|---|
| RunPod Pod | A100 80GB около `$1.59/h`, L40S около `$1.09/h`, H100 PCIe около `$2.89/h` | Дешевле dedicated HF для постоянного GPU; нужно самому поддерживать deployment |
| Modal | A100 около `$2.50/h`, L40S около `$1.95/h`, L4 около `$0.80/h`, H100 около `$3.95/h` | Удобный serverless/scale-to-zero workflow; меньше ручной инфраструктуры |
| Vast.ai | Marketplace, оплата посекундно; interruptible обычно существенно дешевле | Минимальная цена возможна, но preemption и разброс качества хостов повышают риск |

Пример monthly cost без простоев:

```text
RunPod A100: 1.59 * 730 ≈ $1,161.70/month
Modal/HF A100: 2.50 * 730 ≈ $1,825/month
RunPod H100 PCIe: 2.89 * 730 ≈ $2,109.70/month
```

Источники: [RunPod pricing](https://www.runpod.io/pricing), [Modal pricing](https://modal.com/pricing), [Vast.ai pricing model](https://github.com/vast-ai/docs/blob/main/guides/pricing.mdx).

### 4. Cocoon

Cocoon — сеть confidential compute, связанная с Telegram/TON. Официальные документы описывают динамически выставляемую цену за compute request, оплату через TON, worker/proxy в TEE и проверку attestation.

Но на сегодня это не выглядит как простой более дешёвый OpenRouter для агентной системы:

- официальные docs описывают marketplace-механику, но не дают публичной стабильной таблицы `$ / 1M input` и `$ / 1M output`, сопоставимой с OpenRouter;
- deployment требует Linux с TDX-capable CPU, confidential GPU и для реального worker-сценария H100+ класса;
- официальная документация ориентирована на deployment worker/proxy, а не на готовый multi-provider API с понятным SLA;
- сторонние Cocoon-клиенты существуют, но это не официальный SLA и не подтверждение качества/доступности сети.

Итог: Cocoon стоит исследовать для приватности, TON-экономики и долгосрочной децентрализации. Для текущего дешёвого production-agent сначала нужны маленький pilot, измеренные latency/availability и фактический TON cost per token.

Источники: [Cocoon](https://cocoon.org/), [developers](https://cocoon.org/developers), [deployment](https://cocoon.org/docs/deployment), [architecture](https://cocoon.org/architecture), [Telegram announcement](https://t.me/s/durov/465).

## Когда self-host действительно дешевле API

Сравнивать нужно не «цена GPU в час против цены API», а полную стоимость при реальной нагрузке:

```text
C_self_host = GPU_hourly * running_hours
            + storage
            + network
            + monitoring
            + engineering/ops

C_api = input_tokens / 1M * input_price
      + output_tokens / 1M * output_price
```

Self-host обычно выигрывает, если одновременно выполняются условия:

- GPU загружена большую часть времени;
- есть batching или много параллельных агентов;
- модель достаточно компактна для доступного числа GPU;
- простой и cold start не ломают SLA;
- команда готова поддерживать vLLM/SGLang, обновления и failover.

Для одного агента с нерегулярными запросами сначала использовать API. Для постоянной очереди задач — запускать controlled benchmark на RunPod/Modal и считать фактические tokens/sec и requests/hour.

## Рекомендованная схема маршрутизации

```text
простая классификация / pre-check  -> Llama-3.1-8B или gpt-oss-20b
обычный дешёвый агент               -> GPT-6 Luna или gpt-oss-120b
длинный input / короткий output     -> DeepSeek через маршрут с дешёвым input
сложное reasoning                   -> GLM-5.3-Flash
максимально трудная задача          -> GPT-6.1 Sol
постоянная высокая нагрузка         -> Qwen3.8-27B self-host pilot
приватный эксперимент               -> Cocoon pilot после проверки SLA
```

Это пока policy по цене и инфраструктуре, а не итоговый ranking качества. Open-weight-кандидаты нужно добавить в `run_openrouter_arc.py` и прогнать на том же ARC split. Для каждого запуска сохранять:

- ARC score;
- cost per solved task и cost per request;
- total latency и TTFT;
- output tokens/sec;
- provider route;
- retries, errors, availability;
- peak VRAM/GPU-hours для self-host.

## Источники

- [Hugging Face Inference Providers pricing](https://huggingface.co/docs/inference-providers/pricing)
- [Hugging Face Inference Endpoints pricing](https://huggingface.co/docs/inference-endpoints/pricing)
- [HF supported models and live provider metrics](https://huggingface.co/inference/models)
- [OpenAI gpt-oss guide on HF](https://huggingface.co/docs/inference-providers/en/guides/gpt-oss)
- [OpenAI gpt-oss-120b model card](https://huggingface.co/openai/gpt-oss-120b)
- [Qwen3.8-27B model card](https://huggingface.co/Qwen/Qwen3.8-27B)
- [GLM-5.3-Flash Endpoint recipe](https://endpoints.huggingface.co/new/zai-org/GLM-5.3-Flash)
- [DeepSeek V4 Flash on OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash-20260731)
- [RunPod pricing](https://www.runpod.io/pricing)
- [Modal pricing](https://modal.com/pricing)
- [Vast.ai pricing documentation](https://github.com/vast-ai/docs/blob/main/guides/pricing.mdx)
- [Cocoon official site](https://cocoon.org/)
- [Cocoon deployment docs](https://cocoon.org/docs/deployment)
