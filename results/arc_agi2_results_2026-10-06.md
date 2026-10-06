# ARC-AGI-2: official и community результаты

Дата среза: **2026-10-06**. Основная выборка для официального сравнения — `v2_Semi_Private`, то есть 120 semi-private задач ARC-AGI-2. Community-результаты вынесены отдельно и не смешиваются с ARC Prize Verified.

## Короткий вывод

- Среди пяти первоначально выбранных моделей лучший официальный результат — **GPT-6.1 Sol: 94.2%**, ориентировочно **$0.254 за задачу**.
- По официальному score/$ среди этих пяти лидирует **DeepSeek V4 Flash 0731: 61.4% при $0.042 за задачу**.
- Если смотреть шире официального leaderboard, интересный компромисс — **Dots3-Note Preview: 76.8% и оценка около $0.08 за задачу**. Его нужно перепроверить live-fetch и отдельно учитывать, что цена на странице ARC — оценочная.
- Максимальный официальный score в текущем срезе — **GPT-6 Astra: 95.0%**, но стоимость около **$1.12 за задачу**.

## ARC Prize Verified

| Модель | ARC-AGI-2 | Стоимость ARC, $/task | score/$ | Статус |
|---|---:|---:|---:|---|
| GPT-6 Astra | 95.0% | 1.12 | 84.8 | official verified |
| GPT-6.1 Sol | 94.2% | 0.254 | 370.9 | official verified |
| Claude Opus 5.5 High | 93.3% | 0.408 | 228.7 | official verified |
| Gemini 3.7 Flash High | 84.6% | 0.25 | 338.4 | official verified |
| Dots3-Note Preview | 76.8% | ~0.08 est. | ~960.0 | official verified |
| GLM-5.3-Flash | 65.8% | 0.093 | 707.5 | official verified |
| DeepSeek V4 Flash 0731 | 61.4% | 0.042 | 1461.9 | official verified |
| GPT-5.6 Luna 2026-07-30 | 59.6% | 0.177 | 336.7 | official verified |
| GPT-6 Luna | 59.3% | 0.062 | 956.5 | official verified |

`score/$` — это процентных пунктов ARC score на один доллар; это не вероятность успеха и не цена полного пользовательского запроса.

Пять строк из исходной задачи также сохранены машинно в [`data/processed/arc_agi2_comparison.csv`](../data/processed/arc_agi2_comparison.csv) и [`data/processed/arc_agi2_comparison.json`](../data/processed/arc_agi2_comparison.json). Сейчас эти два файла используют контрольный snapshot, пока не выполнен live-fetch.

## Community / self-reported

Эти записи — публикации сообщества и агентных систем. Они не равны чистому single-model API run и не имеют того же статуса, что ARC Prize Verified.

| Submission | Набор | Score | Заявленная стоимость | Комментарий |
|---|---|---:|---:|---|
| MiMo-V2.6-Flash | Public / independent | 66.6% | ~$0.003–$0.011/task* | Оценка через OpenRouter для одного запроса; не заявленная автором и не ARC Prize Verified |
| Noemon's agentic ARC-AGI 2 Solver, Gemini 3.1 Pro | Public Train | 92.5% | ~$3.90/task | Высокий score, но другая выборка; напрямую с semi-private не сравнивать |
| Evolutionary Test-Time Compute with Natural Language Instructions, Grok-4 | Semi-Private | 29.4% | $3,648 reported | Агентная/эволюционная система |
| Efficient Evolutionary Program Synthesis, Grok-4 | Semi-Private | 26.0% | $476.40 reported | Лучший из найденных semi-private community по reported score/$ |
| Tiny Recursive Model | Public | 7.8% | $252 reported | Не API-модель в том же смысле, что строки выше |
| Hierarchical Reasoning Model | Semi-Private | 2.0% | $201 reported | Архитектура/система, а не обычный API run |

Важное ограничение: `reported cost` в YAML — это поле автора submission. Его нельзя автоматически считать той же метрикой `$ per task`, которую публикует официальный leaderboard.

### Оценка стоимости MiMo через OpenRouter

В неофициальной записи MiMo указана только результативность 66.6%, без фактического ARC cost/task. Поэтому для таблицы использован отдельный диапазон оценки одного API-запроса на одну задачу по каталожным ценам OpenRouter `$0.10/M` input и `$0.28/M` output:

| Профиль на задачу | Расчёт | Оценка |
|---|---|---:|
| 20k input / 4k output | `20,000 × $0.10/M + 4,000 × $0.28/M` | ~$0.0031 |
| 20k input / 10k output | `20,000 × $0.10/M + 10,000 × $0.28/M` | ~$0.0048 |
| 100k input / 4k output | `100,000 × $0.10/M + 4,000 × $0.28/M` | ~$0.0111 |

`*` Это не официальный ARC Prize cost/task: оценка не включает retries, tool calls, ensemble/test-time compute, provider overhead или несколько запросов на одну задачу. Фактический показатель можно получить только из OpenRouter `usage.cost` при воспроизводимом прогоне с зафиксированным prompt, reasoning budget и provider route.

## Источники

- [ARC-AGI-2 описание и разбиение данных](https://arcprize.org/arc-agi/2)
- [Официальный ARC Prize leaderboard](https://arcprize.org/leaderboard)
- [Официальные JSON models](https://arcprize.org/media/data/models.json) и [evaluations](https://arcprize.org/media/data/evaluations.json)
- [GPT-6.1 Sol](https://arcprize.org/results/openai-gpt-6-1-sol)
- [GPT-6 Astra](https://arcprize.org/results/openai-gpt-6)
- [Dots3-Note Preview](https://arcprize.org/results/dots-studio-dots3-note-prev-max)
- [DeepSeek V4 Flash 0731](https://arcprize.org/results/deepseek-v4-flash-0731)
- [GLM-5.3-Flash](https://arcprize.org/results/zai-glm-5-3-flash)
- [GPT-6 Luna](https://arcprize.org/results/openai-gpt-6-luna)
- [GPT-5.6 Luna 2026-07-30](https://arcprize.org/results/openai-gpt-5-6-luna-2026-07-30)
- [Community leaderboard](https://arcprize.org/leaderboard/community)
- [Community leaderboard repository и правила верификации](https://github.com/arcprize/ARC-AGI-Community-Leaderboard)
- [Noemon YAML](https://github.com/arcprize/ARC-AGI-Community-Leaderboard/blob/main/submissions/noemon-gemini-agentic/submission.yaml)
- [Efficient EEP YAML](https://github.com/arcprize/ARC-AGI-Community-Leaderboard/blob/main/submissions/efficient-evolutionary-program-synthesis/submission.yaml)
- [Natural-language ETC YAML](https://github.com/arcprize/ARC-AGI-Community-Leaderboard/blob/main/submissions/evolutionary-test-time-compute-with-natural-language/submission.yaml)

## Что запускать для обновления

```powershell
cd arc-explorer
python scripts/fetch_arc.py --force
python scripts/fetch_community.py --keep-going
python scripts/compare_arc.py
```
