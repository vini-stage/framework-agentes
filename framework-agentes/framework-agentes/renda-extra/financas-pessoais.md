# Agente: Finanças Pessoais — Vinícius

> **Status:** 🔲 Fase 2 (Semanas 4-5)  
> **Domínio:** Pessoal  
> **Input:** Extrato bancário, receitas, despesas, metas  
> **Output:** Dashboard financeiro, relatório mensal, projeções

## Objetivo
Organizar, analisar e projetar as finanças pessoais do Vinícius, integrando todas as fontes de renda (Stage Motors, AM CAR, empréstimos) e fornecendo visibilidade clara sobre gastos, poupança e crescimento patrimonial.

## Funcionalidades planejadas

### 1. Controle mensal
- Consolidar receitas de todas as fontes
- Categorizar despesas (fixas vs. variáveis)
- Calcular taxa de poupança mensal
- Comparar com meses anteriores

### 2. Visão patrimonial
- Patrimônio líquido atualizado (ativos - passivos)
- Evolução mês a mês (gráfico)
- Composição: imóveis, veículos, investimentos, recebíveis

### 3. Projeções
- Simulação de cenários (conservador, moderado, agressivo)
- Meta de patrimônio em 1, 3 e 5 anos
- Impacto de decisões (ex: comprar imóvel, investir X em ações)

### 4. Orçamento inteligente
- Sugerir alocação ideal baseada no perfil (50/30/20 adaptado)
- Alertar sobre categorias que estão acima da média
- Recomendar ajustes com base nas metas

## Formato de input sugerido
```
Mês/Ano: [MM/AAAA]

RECEITAS:
- Pró-labore Stage Motors: R$
- Pró-labore AM CAR: R$
- Dividendos/Lucros: R$
- Empréstimos (juros recebidos): R$
- Outras: R$

DESPESAS FIXAS:
- Moradia: R$
- Universidade: R$
- Plano de saúde: R$
- Academia: R$
- Outros fixos: R$

DESPESAS VARIÁVEIS:
- Alimentação: R$
- Transporte: R$
- Lazer: R$
- Vestuário: R$
- Outros: R$

INVESTIMENTOS/APORTES:
- [tipo]: R$

PATRIMÔNIO ATUALIZADO:
- Imóveis: R$
- Veículos: R$
- Investimentos: R$
- Recebíveis: R$
- Dívidas: R$
```

## Output padrão
- Dashboard interativo (React/HTML)
- Relatório resumido (.md ou .docx)
- Gráficos: composição de receita, despesas por categoria, evolução patrimonial

## Instruções
<!-- A ser detalhado na Fase 2 -->
