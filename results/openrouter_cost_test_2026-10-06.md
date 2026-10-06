# OpenRouter cost test

Retrieved: `2026-10-06T06:42:26Z`  
Pricing source: `OpenRouter catalog pricing`  
Cache-read ratio: `0.00`  
Multiplier: `1000` requests  

This is a deterministic token-cost simulation. It does not measure model quality or actual provider routing cost returned by a request.

## Catalog prices

| Model | OpenRouter ID | Input / M | Output / M | Cache read / M | Status |
|---|---|---:|---:|---:|---|
| DeepSeek V4 Flash 0731 | `deepseek/deepseek-v4-flash-0731` | $0.009000 | $1.280000 | $0.009000 | ok |
| GLM-5.3-Flash | `z-ai/glm-5.3-flash` | $0.150000 | $0.500000 | $0.030000 | ok |
| GPT-6 Luna | `openai/gpt-6-luna` | $0.100000 | $0.500000 | $0.010000 | ok |
| GPT-5.6 Luna | `openai/gpt-5.6-luna` | $0.200000 | $1.200000 | $0.020000 | ok |
| GPT-6.1 Sol | `openai/gpt-6.1-sol` | $2.000000 | $10.000000 | $0.100000 | ok |
| GPT-6.1 Sol Pro | `openai/gpt-6.1-sol-pro` | $2.000000 | $10.000000 | $0.100000 | ok |
| GPT-6 Astra | `openai/gpt-6-astra` | $10.000000 | $50.000000 | $1.000000 | ok |
| Dots3-Note Preview free | `dots-studio/dots-3-note-preview:free` | $0.000000 | $0.000000 | — | ok |

## Cost scenarios

### ARC-like short answer
Input: `12,000` tokens; output: `1,000` tokens.

| Rank | Model | $/request | $/multiplier |
|---:|---|---:|---:|
| 1 | `Dots3-Note Preview free` | $0.000000 | $0.000000 |
| 2 | `DeepSeek V4 Flash 0731` | $0.001388 | $1.388000 |
| 3 | `GPT-6 Luna` | $0.001700 | $1.700000 |
| 4 | `GLM-5.3-Flash` | $0.002300 | $2.300000 |
| 5 | `GPT-5.6 Luna` | $0.003600 | $3.600000 |
| 6 | `GPT-6.1 Sol` | $0.034000 | $34.000000 |
| 7 | `GPT-6.1 Sol Pro` | $0.034000 | $34.000000 |
| 8 | `GPT-6 Astra` | $0.170000 | $170.000000 |

Winner by cost: **Dots3-Note Preview free** ($0.000000 per request).

### Agent normal loop
Input: `20,000` tokens; output: `4,000` tokens.

| Rank | Model | $/request | $/multiplier |
|---:|---|---:|---:|
| 1 | `Dots3-Note Preview free` | $0.000000 | $0.000000 |
| 2 | `GPT-6 Luna` | $0.004000 | $4.000000 |
| 3 | `GLM-5.3-Flash` | $0.005000 | $5.000000 |
| 4 | `DeepSeek V4 Flash 0731` | $0.005300 | $5.300000 |
| 5 | `GPT-5.6 Luna` | $0.008800 | $8.800000 |
| 6 | `GPT-6.1 Sol` | $0.080000 | $80.000000 |
| 7 | `GPT-6.1 Sol Pro` | $0.080000 | $80.000000 |
| 8 | `GPT-6 Astra` | $0.400000 | $400.000000 |

Winner by cost: **Dots3-Note Preview free** ($0.000000 per request).

### Agent reasoning-heavy loop
Input: `20,000` tokens; output: `10,000` tokens.

| Rank | Model | $/request | $/multiplier |
|---:|---|---:|---:|
| 1 | `Dots3-Note Preview free` | $0.000000 | $0.000000 |
| 2 | `GPT-6 Luna` | $0.007000 | $7.000000 |
| 3 | `GLM-5.3-Flash` | $0.008000 | $8.000000 |
| 4 | `DeepSeek V4 Flash 0731` | $0.012980 | $12.980000 |
| 5 | `GPT-5.6 Luna` | $0.016000 | $16.000000 |
| 6 | `GPT-6.1 Sol` | $0.140000 | $140.000000 |
| 7 | `GPT-6.1 Sol Pro` | $0.140000 | $140.000000 |
| 8 | `GPT-6 Astra` | $0.700000 | $700.000000 |

Winner by cost: **Dots3-Note Preview free** ($0.000000 per request).

### Long context, short action
Input: `100,000` tokens; output: `4,000` tokens.

| Rank | Model | $/request | $/multiplier |
|---:|---|---:|---:|
| 1 | `Dots3-Note Preview free` | $0.000000 | $0.000000 |
| 2 | `DeepSeek V4 Flash 0731` | $0.006020 | $6.020000 |
| 3 | `GPT-6 Luna` | $0.012000 | $12.000000 |
| 4 | `GLM-5.3-Flash` | $0.017000 | $17.000000 |
| 5 | `GPT-5.6 Luna` | $0.024800 | $24.800000 |
| 6 | `GPT-6.1 Sol` | $0.240000 | $240.000000 |
| 7 | `GPT-6.1 Sol Pro` | $0.240000 | $240.000000 |
| 8 | `GPT-6 Astra` | $1.200000 | $1200.000000 |

Winner by cost: **Dots3-Note Preview free** ($0.000000 per request).

## Interpretation

For a production decision, combine this table with the runner's actual `usage`, `cost_usd`, latency and task correctness. OpenRouter provider discounts and routing can make the effective cost differ from the catalog field.

Source: [OpenRouter Models API](https://openrouter.ai/docs/api/api-reference/models/get-models).
