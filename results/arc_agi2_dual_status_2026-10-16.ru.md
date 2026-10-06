# ARC-AGI-2: official и community averages

Дата исследования: **2026-10-16**.

В этом снимке два ARC-показателя разделены:

- **ARC official / Verified** — официальный результат ARC Prize Verified, обычно на semi-private тесте;
- **Среднее ARC community** — среднее арифметическое сопоставимых independent/community наблюдений без включения official score;
- **Σ ARC median** — медиана official и community, если доступны обе оценки, иначе единственная доступная оценка.

`n=1` означает, что сейчас есть только одно сопоставимое независимое наблюдение. Это среднее одного значения, а не устойчивое статистическое подтверждение.

| OpenRouter ID | ARC official / Verified | Среднее ARC community | Σ ARC median | n | Статус | Цена OpenRouter за 1M input / output | Примечание |
|---|---:|---:|---:|---:|---|---:|---|
| `openai/gpt-6.1-sol` | 94,2% | 66,9% | **80,6%** | 1 | ✅ official + independent | ~$2 / $10 | Official и independent запуски несопоставимы напрямую |
| `deepseek/deepseek-v4.1-flash` | 72,9% | 69,0% | **71,0%** | 1 | ✅ official + independent | ~$0,0357 / $0,1428† | Лучший практический quality/value-кандидат в группе |
| `stealth/space-bunny-alpha` | — | 70,4% | **70,4%** | 1 | 🟨* только independent | бесплатный preview | Анонимная stealth-модель, official ARC не найдена |
| `xiaomi/mimo-v2.6-flash` | — | 66,6% | **66,6%** | 1 | 🟨* только independent | ~$0,10 / $0,28 | Official ARC Prize результат не найден |
| `xiaomi/mimo-v2.5` | — | 65,7% | **65,7%** | 1 | 🟨* только independent | ~$0,119 / $0,238 | Official ARC Prize результат не найден |
| `deepseek/deepseek-v4-flash-0731` | 61,4% | 68,5% | **65,0%** | 1 | ✅ official + independent | ~$0,00441 / $1,152 | Независимый результат намного выше official |
| `openai/gpt-6-luna` | 59,3% | 61,3% | **60,3%** | 1 | ✅ official + independent | ~$0,10 / $0,50 | Базовая general-agent модель репозитория |

Community-значения взяты из independent snapshot **TrustTheBench от 2026-08-29** ([ARC-AGI-2](https://www.trustthebench.com/benchmarks/arc-agi-2)). Это не ARC Prize Verified и не устойчивое среднее по нескольким прогонам.

`†` Цена V4.1 — текущая скидочная/каталожная цена OpenRouter и может измениться.

## Интерпретация

- **GPT-6.1 Sol** имеет максимальный Σ ARC median, но из-за цены остаётся моделью для эскалации.
- **DeepSeek V4.1 Flash** — лучший практический quality/value-кандидат: 72,9% official, 69,0% independent и текущая цена ниже Luna в OpenRouter.
- **Space Bunny Alpha** имеет лучший independent результат в этой небольшой группе, но остаётся анонимной бесплатной preview-моделью без ARC Prize подтверждения. OpenRouter указывает, что она работает у анонимного стороннего провайдера и prompts/completions могут сохраняться ([страница модели](https://openrouter.ai/stealth/space-bunny-alpha)).
- У **DeepSeek V4 Flash 0731** большая разница между official и community; нужно проверять harness, prompt, split, reasoning effort и число задач.
- Для MiMo-V2.5 и MiMo-V2.6-Flash есть независимые наблюдения, но official ARC Prize результат в этом снимке не найден.

При двух значениях `Σ ARC median` — центральная точка между official и community; при одной доступной оценке используется она. Это показатель ARC quality, а не цена/качество. Цены OpenRouter остаются отдельными и зависят от даты.

## Правило усреднения

Для независимых/community score `s1 ... sn`:

```text
community_average = (s1 + s2 + ... + sn) / n
```

Official score никогда не добавляется в это среднее. Для каждого нового результата сохраняются URL, дата, snapshot модели, harness, split, reasoning setting и `n`. Если протоколы существенно отличаются, значения не объединяются в одно среднее.

Источники: [ARC Prize V4.1](https://arcprize.org/results/deepseek-v4-1-flash), [ARC Prize V4 Flash 0731](https://arcprize.org/results/deepseek-v4-flash-0731), [TrustTheBench](https://www.trustthebench.com/benchmarks/arc-agi-2), [OpenRouter](https://openrouter.ai/deepseek/deepseek-v4.1-flash).
