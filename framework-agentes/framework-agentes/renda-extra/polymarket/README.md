# Polymarket Bot — Upgrades Pendentes

> **Status:** 🔲 Fase 4 (Semana 8)  
> **Domínio:** Renda Extra

## Upgrades a aplicar

Prompt salvo para os 3 upgrades:

> "Preciso que você melhore o bot com 3 upgrades:
> 1. ANALYZER.PY — regra de entrada market_price <= model_probability * 0.5;
> 2. TRADER.PY — saída automática quando market_price >= model_probability * 0.9 OU days_to_expiry <= 7;
> 3. LOGGER.PY — Sharpe Ratio com log returns."

## Regras adicionais já definidas
- Só entrar em mercados com expiração ≤7 dias
- Value-based entry: market_price ≤ model_probability × 0.5
- Take profit: market_price ≥ model_probability × 0.9
- Forced exit: 1 dia antes da expiração
- Logging: Sharpe Ratio com log returns

## Arquivos a modificar
- `analyzer.py` — Regra de entrada
- `trader.py` — Lógica de saída automática
- `logger.py` — Sharpe Ratio
