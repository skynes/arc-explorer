# OpenRouter providers: GPT-6 Luna vs DeepSeek V4 Flash 0731

Дата snapshot: **2026-10-06**.

## Короткий вывод

Разница между моделями на уровне provider routing большая:

- **GPT-6 Luna:** 3 provider families — OpenAI, Azure, Amazon Bedrock. У стандартных OpenAI и Azure одинаковая цена `$0.10/$0.50`; выбор влияет в основном на latency, throughput и availability.
- **DeepSeek V4 Flash 0731:** 26 providers. Цена, latency и throughput сильно различаются. Для agentic/reasoning-нагрузки provider selection может изменить стоимость запроса в несколько раз.

## GPT-6 Luna

### Provider snapshot

| Provider | Tier/route | Input | Output | P50 latency | P50 throughput | Uptime |
|---|---|---:|---:|---:|---:|---:|
| OpenAI | Standard | $0.10/M | $0.50/M | 2.53 s | 61 tok/s | 100% |
| Azure | Standard | $0.10/M | $0.50/M | 4.06 s | 78 tok/s | 100% |
| OpenAI | Flex | $0.05/M | $0.25/M | 6.35 s | 48 tok/s | 92.13% |
| Azure | alternate | $0.11/M | $0.55/M | 2.48 s | 76 tok/s | 100% |
| Azure | alternate | $0.11/M | $0.55/M | 3.59 s | 121 tok/s | 100% |
| Amazon Bedrock | alternate | $0.11/M | $0.55/M | 5.27 s | 28 tok/s | 99.55% |
| OpenAI | Fast | $0.20/M | $1.00/M | 1.75 s | 105 tok/s | 100% |

### Что это означает

Для стандартного запроса `20k input / 4k output`:

| Route | Стоимость запроса |
|---|---:|
| OpenAI/Azure Standard | $0.00400 |
| OpenAI Flex | $0.00200 |
| Azure/Bedrock alternate | $0.00440 |
| OpenAI Fast | $0.00800 |

Рекомендация:

- default: **OpenAI Standard** — ниже latency, чем Azure Standard;
- если важен output throughput: **Azure Standard** показывает выше throughput;
- если важна цена и допустима задержка: **OpenAI Flex**, но uptime ниже и это не лучший production-default;
- Fast имеет смысл только когда wall-clock важнее token-cost.

GPT-6 Luna provider routing не даёт большого ценового преимущества, кроме Flex. Основная ценность OpenRouter здесь — failover между OpenAI/Azure/Bedrock.

## DeepSeek V4 Flash 0731

### Representative provider snapshot

| Provider | Input | Output | P50 latency | P50 throughput | Uptime |
|---|---:|---:|---:|---:|---:|
| Relace | $0.0079/M | $1.28/M | 0.82 s | 36 tok/s | 100% |
| OpenInference | $0.00869/M | $1.408/M | 1.04 s | 33 tok/s | 99.73% |
| Reka AI | $0.021/M | $0.528/M | 0.76 s | 64 tok/s | 100% |
| StreamLake, promo | $0.044/M | $0.132/M | 1.33 s | 41 tok/s | 100% |
| DeepInfra | $0.06/M | $0.18/M | 0.76 s | 36 tok/s | 99.89% |
| Baseten | $0.13/M | $0.26/M | 0.69 s | 114 tok/s | 98.53% |
| CoreWeave | $0.13/M | $0.28/M | 0.51 s | 86 tok/s | 99.67% |
| Cohere | $0.14/M | $0.28/M | 0.50 s | 134 tok/s | 99.59% |
| Together | $0.14/M | $0.28/M | 0.75 s | 52 tok/s | 99.97% |
| Nebius Token Factory | $0.14/M | $0.28/M | 0.74 s | 104 tok/s | 82.65% |
| SiliconFlow | $0.22/M | $0.66/M | 1.86 s | 52 tok/s | 99.73% |
| NovitaAI, 7% off | $0.4092/M | $1.228/M | 1.40 s | 48 tok/s | 100% |

OpenRouter page currently reports overall DeepSeek availability around 99.87% over 3 days and 99.85% over 24 hours. Provider metrics are rolling observations, not an SLA.

### Стоимость agent-normal запроса

Профиль: `20k input / 4k output`.

| Provider | Стоимость запроса | Относительно Relace |
|---|---:|---:|
| Relace | $0.005278 | 1.00x |
| Reka AI | $0.002532 | 2.09x дешевле |
| StreamLake promo | $0.001408 | 3.75x дешевле |
| DeepInfra | $0.001920 | 2.75x дешевле |
| Baseten | $0.003640 | 1.45x дешевле |
| CoreWeave | $0.003720 | 1.42x дешевле |
| Cohere/Together/Nebius | $0.003920 | 1.35x дешевле |
| SiliconFlow | $0.007040 | 1.33x дороже |
| Novita promo | $0.013096 | 2.48x дороже |

Цена считается по provider rates из таблицы. Promo-тарифы нельзя считать стабильной основой production-бюджета.

### Что выбирать для DeepSeek

- **Минимальная стабильная цена:** DeepInfra.
- **Цена + высокая скорость:** Baseten или Cohere; нужно проверить tool calling.
- **Максимальный throughput:** Cohere в текущем snapshot — 134 tok/s.
- **Минимальная latency:** CoreWeave/Cohere/Reka, но важен регион клиента.
- **Максимальная надёжность:** Together или DeepInfra по текущему uptime snapshot.
- **Promo/эксперимент:** StreamLake, но тариф может исчезнуть.

## Сравнение моделей на уровне provider layer

| Свойство | GPT-6 Luna | DeepSeek V4 Flash 0731 |
|---|---:|---:|
| Provider families | 3 | 26 |
| Standard input price range | $0.10–$0.10 | $0.0079–$0.44 |
| Standard output price range | $0.50–$0.50 | $0.18–$1.408 |
| Лучший observed throughput | 121 tok/s | 134 tok/s |
| Лучший observed latency | 1.75 s | 0.50 s |
| Availability, routed | 99.45% | 99.87% |
| Насколько важен provider choice | Средне | Очень сильно |

Для GPT-6 Luna выбор provider почти не меняет цену стандартной tier. Для DeepSeek одна и та же модель может иметь принципиально разную стоимость из-за upstream provider.

## Рекомендованные OpenRouter настройки

### GPT-6 Luna: стандартный production

Оставить default routing или предпочесть OpenAI:

```json
{
  "provider": {
    "order": ["openai", "azure"],
    "allow_fallbacks": true,
    "require_parameters": true
  }
}
```

### DeepSeek: дешёвый agent loop с fallback

```json
{
  "provider": {
    "order": ["deepinfra", "baseten", "together"],
    "allow_fallbacks": true,
    "require_parameters": true
  }
}
```

### DeepSeek: честный тест DeepInfra

```json
{
  "provider": {
    "only": ["deepinfra"],
    "allow_fallbacks": false,
    "require_parameters": true
  }
}
```

`require_parameters` важен для agent tests: он не должен отправлять запрос provider, который не поддерживает нужные tools или structured outputs.

## Итог

**Для GPT-6 Luna provider selection в основном влияет на скорость, а не на цену.** OpenAI Standard — разумный default; Azure стоит проверять на throughput.

**Для DeepSeek provider selection влияет и на цену, и на скорость.** DeepInfra — лучший стабильный cheap route; Baseten/Cohere — кандидаты на speed; StreamLake — экспериментальный promo route.

Нельзя сравнивать только model-level price OpenRouter. В следующем runner нужно сохранять фактический `provider_name`, `usage.cost`, latency, output tok/s и tool-call success для каждого запроса.

## Источники

- [GPT-6 Luna OpenRouter](https://openrouter.ai/openai/gpt-6-luna)
- [DeepSeek V4 Flash 0731 OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash-0731)
- [OpenRouter provider routing](https://openrouter.ai/docs/guides/routing/provider-selection)
