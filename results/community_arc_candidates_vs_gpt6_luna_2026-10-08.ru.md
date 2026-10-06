# Независимые ARC-AGI-2 кандидаты против GPT-6 Luna

Дата исследования: **2026-10-08**.

Проверены независимые пользовательские результаты ARC-AGI-2 выше базового результата **GPT-6 Luna: 59,3%**, при условии, что цены OpenRouter по input и output не выше Luna: `$0,10/M` input и `$0,50/M` output. Эти ARC-результаты не являются ARC Prize Verified. ARC Prize отдельно отмечает, что community scores обычно self-reported; полу-приватные ARC-AGI-1/2 результаты — те, которые ARC Prize запускает и проверяет.

## Строго подходящие модели

В профиле репозитория `20k input / 4k output` Luna стоит примерно `$0,004` за запрос.

| Модель | Независимый ARC-AGI-2 | Разница с Luna | OpenRouter ID | Input / output | Оценка 20k/4k | Оценка |
|---|---:|---:|---|---:|---:|---|
| GLM 5.3 Flash | 72,2% | +12,9 п.п. / +21,8% | `z-ai/glm-5.3-flash` | $0,04 / $0,50 | ~$0,0028 | Лучший платный строгий кандидат |
| Llama 4 Scout | 69,0% | +9,7 п.п. / +16,4% | `meta-llama/llama-4-scout` | $0,10 / $0,30 | ~$0,0032 | Хорошая цена; tools зависят от provider |
| NVIDIA Nemotron 3 Ultra (free) | 67,5% | +8,2 п.п. / +13,8% | `nvidia/nemotron-3-ultra-550b-a55b:free` | free / free | $0,0000 | Экспериментальный backup; free endpoint ограничен |
| QwQ 32B (free) | 67,2% | +7,9 п.п. / +13,3% | `qwen/qwq-32b:free` | free / free | $0,0000 | Дешёвый ARC-кандидат; старая модель и rate limits |
| MiMo-V2.6-Flash | 66,6% | +7,3 п.п. / +12,3% | `xiaomi/mimo-v2.6-flash` | $0,10 / $0,28 | ~$0,0031 | Лучший уже отслеживаемый недорогой general-кандидат |
| NVIDIA Nemotron 3 Super (free) | 65,9% | +6,6 п.п. / +11,1% | `nvidia/nemotron-3-super-120b-a12b:free` | free / free | $0,0000 | Перспективный free backup; проверить под нагрузкой |
| Gemma 3 27B* | 65,5% | +6,2 п.п. / +10,5% | `google/gemma-3-27b-it` | $0,08 / $0,16 | ~$0,0022 | Очень дёшево, но community row помечена preview |
| Llama 3.3 70B Instruct | 62,8% | +3,5 п.п. / +5,9% | `meta-llama/llama-3.3-70b-instruct` | $0,10 / $0,32 | ~$0,0033 | Старая и более слабая agent-модель |

ARC scores собраны как независимые наблюдения на [TrustTheBench](https://www.trustthebench.com/benchmarks/arc-agi-2). Цены и ID взяты из [каталога OpenRouter](https://openrouter.ai/openai/gpt-6-luna). Относительный процент: `(score модели − 59,3) / 59,3`; процентные пункты — обычная разница score.

## Важное исключение: DeepSeek V4 Flash 0731

TrustTheBench показывает независимый результат **68,5%** для DeepSeek V4 Flash 0731. Но OpenRouter указывает примерно `$0,018/M` input и `$1,28/M` output. Поэтому input намного дешевле, а output в 2,56 раза дороже Luna. Это не строгий ценовой match: модель выгодна только при длинном input и коротком output.

## Текущий вывод

1. **GLM 5.3 Flash** — первая модель для платного A/B-теста вместо Luna: лучший независимый ARC score среди строгих ценовых кандидатов и примерно на 30% дешевле в профиле `20k/4k`.
2. **MiMo-V2.6-Flash** остаётся более осторожной недорогой general-альтернативой.
3. **QwQ 32B free** и **Nemotron free** подходят для pre-check/backup, но пока не для основного production default из-за rate limits и отсутствия Verified-статуса.
4. Эти ARC-наблюдения не доказывают общего превосходства над Luna: prompts, snapshots, reasoning budget и public/private split могут различаться.

## Источники

- [ARC Prize Community Leaderboard policy](https://arcprize.org/leaderboard/community)
- [TrustTheBench ARC-AGI-2](https://www.trustthebench.com/benchmarks/arc-agi-2)
- [OpenRouter GPT-6 Luna](https://openrouter.ai/openai/gpt-6-luna)
- [OpenRouter GLM 5.3 Flash](https://openrouter.ai/z-ai/glm-5.3-flash)
- [OpenRouter Llama 4 Scout](https://openrouter.ai/meta-llama/llama-4-scout)
- [OpenRouter MiMo-V2.6-Flash](https://openrouter.ai/xiaomi/mimo-v2.6-flash)
- [OpenRouter Nemotron 3 Ultra free](https://openrouter.ai/nvidia/nemotron-3-ultra-550b-a55b:free)
- [OpenRouter Nemotron 3 Super free](https://openrouter.ai/nvidia/nemotron-3-super-120b-a12b:free)
- [OpenRouter QwQ 32B free](https://openrouter.ai/qwen/qwq-32b:free)
- [OpenRouter Gemma 3 27B](https://openrouter.ai/google/gemma-3-27b-it)
- [OpenRouter Llama 3.3 70B Instruct](https://openrouter.ai/meta-llama/llama-3.3-70b-instruct)

\* В TrustTheBench строка называется **Gemma 3 27B Preview**; цена OpenRouter относится к текущему `google/gemma-3-27b-it`, exact snapshot нужно перепроверить перед production.
