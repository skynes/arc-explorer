# OpenRouter: срез цен и моделей

Дата среза: **2026-10-06**. Ниже указана list pricing из live-ответа `GET https://openrouter.ai/api/v1/models`, сохранённого в [`data/raw/openrouter_models.json`](../data/raw/openrouter_models.json). Это цены за 1M токенов, а не ARC Prize cost-per-task. Они зависят от provider routing, скидок, cache hit rate и соотношения input/output токенов.

## Текущий каталог

| Модель | OpenRouter ID | Input / 1M | Output / 1M | Context | Примечание |
|---|---|---:|---:|---:|---|
| Dots3-Note Preview (free) | `dots-studio/dots-3-note-preview:free` | free | free | 512K | Rate-limited; страница указывает уход 31 Dec 2026 |
| DeepSeek V4 Flash 0731 | `deepseek/deepseek-v4-flash-0731` | $0.0103 | $1.28 | 1.0M | API list price; web-карточка может показывать другой provider/weighted price |
| GLM 5.3 Flash | `z-ai/glm-5.3-flash` | $0.15 | $0.50 | 1.0M | API list price; на странице есть provider discount, например DeepInfra $0.075/$0.25 |
| GPT-6 Luna | `openai/gpt-6-luna` | $0.10 | $0.50 | 1.1M | Flex: $0.05/$0.25 |
| GPT-5.6 Luna | `openai/gpt-5.6-luna` | $0.20 | $1.20 | 1.1M | Flex: $0.10/$0.60 |
| GPT-6.1 Sol | `openai/gpt-6.1-sol` | $2.00 | $10.00 | 1.1M | Flex: $1/$5; Pro — отдельный ID и обычно дороже по reasoning tokens |
| GPT-6 Astra | `openai/gpt-6-astra` | $10.00 | $50.00 | 1.1M | Максимальный класс из найденных; Flex/провайдеры могут менять effective price |

## Что это меняет в выборе

1. **Самый дешёвый запуск — Dots free**, но его нельзя считать бесплатным production SLA: у free endpoints есть rate limits и заметно ниже availability, чем у платных маршрутов.
2. **Самый дешёвый платный input в live API — DeepSeek V4 Flash 0731**. Однако output стоит заметно дороже input, поэтому для ARC-задач надо измерить фактический output/reasoning token расход.
3. **GLM 5.3 Flash** выглядит наиболее интересным недорогим платным кандидатом по ARC score среди исходной пятёрки, но его API list input price выше GPT-6 Luna. При этом отдельные provider routes и discounts могут менять effective price.
4. **GPT-6.1 Sol** — качество, но не экономичность: его OpenRouter token price намного выше стоимости ARC Prize task-run. Это разные сценарии биллинга и не противоречие.

### DeepSeek против GPT-5.6 Luna

В стандартном OpenRouter routing:

```text
DeepSeek  = 0.0103 × input_M + 1.28 × output_M
GPT-5.6   = 0.20   × input_M + 1.20 × output_M
```

GPT-5.6 Luna становится дешевле только если `output_tokens / input_tokens > 2.37`. Для ARC это нетипично: условие требует, чтобы ответ был более чем в 2.37 раза длиннее prompt. Поэтому для обычного ARC-запуска **DeepSeek дешевле по полной сумме**.

У GPT-5.6 Luna есть Flex-маршрут `$0.10/$0.60`. Там break-even примерно `output/input > 0.132`: если модель генерирует очень длинный reasoning/output относительно ARC prompt, Flex может оказаться дешевле DeepSeek. Это нужно проверять фактическими token usage из runner, а не только карточкой модели.

## Важная методологическая оговорка

Нельзя делить ARC score на цену OpenRouter за 1M токенов без фиксированного сценария. Для корректного OpenRouter comparison нужно для каждой модели сохранить:

- одинаковый prompt и одинаковый набор ARC-AGI-2 задач;
- input tokens, output tokens и reasoning tokens;
- routing/provider и дату запроса;
- latency, timeout, errors и повторные попытки;
- точность решения задачи и стоимость именно этого запуска.

После этого можно считать `tasks_solved / dollar`, `score / dollar` и confidence interval. Пока этот файл — каталог цен, а не повторный ARC benchmark.

## Источники OpenRouter

- [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models)
- [DeepSeek V4 Flash 0731](https://openrouter.ai/deepseek/deepseek-v4-flash-20260731)
- [GLM 5.3 Flash](https://openrouter.ai/z-ai/glm-5.3-flash)
- [GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
- [GPT-5.6 Luna](https://openrouter.ai/openai/gpt-5.6-luna)
- [GPT-6.1 Sol](https://openrouter.ai/openai/gpt-6.1-sol)
- [GPT-6.1 Sol Pro](https://openrouter.ai/openai/gpt-6.1-sol-pro)
- [GPT-6 Astra](https://openrouter.ai/openai/gpt-6-astra)
- [Dots3-Note Preview free](https://openrouter.ai/dots-studio/dots-3-note-preview:free)

## Обновление через скрипт

```powershell
cd arc-explorer
python scripts/fetch_openrouter.py --all
```

Результат API сохранится в `data/raw/openrouter_models.json`, а отфильтрованные модели — в `data/processed/openrouter_models.json`. В текущем live-fetch найдено 464 записи.
