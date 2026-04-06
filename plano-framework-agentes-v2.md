# Plano de execução v2 — Framework multi-agentes IA

**Versão:** 2.0 | **Data:** Abril 2026  
**Para:** Vinícius — Stage Motors / UNIFOR / Renda Extra  
**Stack:** Claude Code + Cowork + MCP Servers

---

## Resumo executivo

Framework com 10 agentes especializados organizados em 3 domínios (Stage Motors, Universidade, Renda Extra + Pessoal), construído em 4 fases ao longo de 8 semanas. Custo mensal estimado entre R$110 e R$550.

**Alterações da v1:**
- ❌ Removido: Agente SDR/WhatsApp
- ✅ Adicionado: Assistente de Conteúdo Instagram (Stage Motors)
- ✅ Adicionado: Agente de Finanças Pessoais

---

## 1. Mapa de agentes (10 agentes)

### Stage Motors (3 agentes)
| # | Agente | Função |
|---|--------|--------|
| 1 | Criador de Anúncios | Textos para OLX + Instagram por veículo |
| 2 | Assistente Instagram | Calendário editorial, captions, hashtags, estratégia |
| 3 | Analista Financeiro | DRE, margem por veículo, break-even, dashboards |

### Universidade (3 agentes)
| # | Agente | Função |
|---|--------|--------|
| 4 | Redator ABNT | Resenhas, relatórios, artigos formatados |
| 5 | Gerador de Slides | Apresentações .pptx no estilo navy/gold |
| 6 | Pesquisador Acadêmico | Busca de fontes, fichamentos, revisão bibliográfica |

### Renda Extra + Pessoal (4 agentes)
| # | Agente | Função |
|---|--------|--------|
| 7 | Criador de Conteúdo | Posts para redes sociais pessoais/projetos |
| 8 | Finanças Pessoais | Controle de receitas/despesas, patrimônio, projeções |
| 9 | Polymarket Bot | Upgrades do bot de trading (3 melhorias mapeadas) |
| 10 | Propostas Freelance | Geração de propostas comerciais de automação |

---

## 2. Custos detalhados

### 2.1 Infraestrutura base

| Item | Custo mensal | Observação |
|------|-------------|------------|
| Claude Pro | R$110/mês (~US$20) | Suficiente para começar |
| Claude Max 5x | R$550/mês (~US$100) | Se bater limite do Pro com frequência |
| Claude Max 20x | R$1.100/mês (~US$200) | Só se virar ferramenta central diária |

**Recomendação:** Comece no Pro. O limite reseta a cada 5h.

### 2.2 Ferramentas complementares

| Ferramenta | Custo | Fase |
|------------|-------|------|
| VPS para bots (Polymarket) | ~R$50–100/mês | Fase 4 |
| Domínio + hosting (freelance) | ~R$30/mês | Fase 4 |

### 2.3 Custo total por fase

| Fase | Período | Custo mensal |
|------|---------|-------------|
| Fase 0 — Fundação | Semana 1 | R$110 (só Pro) |
| Fase 1 — Anúncios Stage | Semanas 2-3 | R$110 |
| Fase 2 — Instagram + Financeiro + Finanças Pessoais | Semanas 4-5 | R$110 |
| Fase 3 — Universidade | Semanas 6-7 | R$110 |
| Fase 4 — Renda Extra | Semana 8 | R$160–240 |

**Custo total das 8 semanas: ~R$220 (2 meses de Pro)**  
Sem contar ferramentas opcionais da Fase 4.

---

## 3. Cronograma de execução

### ✅ Fase 0 — Fundação (Semana 1) — CONCLUÍDA

| Tarefa | Status |
|--------|--------|
| Criar estrutura de pastas do framework | ✅ Feito |
| Escrever prompt do orquestrador central | ✅ Feito |
| Criar arquivos de contexto (Stage, UNIFOR, Pessoal) | ✅ Feito |
| Configurar guia de estilo unificado | ✅ Feito |
| Documentar MCP connections | ✅ Feito |
| Criar stubs de todos os 10 agentes | ✅ Feito |
| Template de anúncio OLX | ✅ Feito |

**Entregáveis:** 17 arquivos, estrutura completa pronta para desenvolvimento.

---

### Fase 1 — Stage Motors: Anúncios (Semanas 2-3)
**ROI:** ~30h/mês economizadas (40 carros × 45min de economia)

| Tarefa | Status |
|--------|--------|
| Detalhar prompt do agente de anúncios OLX | ✅ Feito |
| Definir estrutura de pasta por carro | ✅ Feito |
| Criar prompt para caption Instagram do veículo | ✅ Feito |
| Testar com 5 carros reais do estoque | ✅ Feito |
| Ajustar com base nos resultados | ✅ Feito |

**Total: ~9h | 3-4 sessões**

**Como fazer:** Para cada carro, você cria uma pasta com fotos + dados.txt. O agente gera título OLX otimizado, descrição com palavras-chave, preço sugerido (FIPE), e caption pra Instagram. Usa Cowork pra ler fotos e PDFs.

---

### Fase 2 — Instagram + Financeiros (Semanas 4-5)

#### Assistente Instagram Stage Motors

| Tarefa | Tempo |
|--------|-------|
| Definir personas e pilares de conteúdo da Stage | 1h |
| Criar prompt com calendário editorial | 2h |
| Gerar 1 semana de conteúdo de teste (6 posts) | 2h |
| Refinar tom de voz e formato com base nos testes | 1h |

**Total: ~6h | 2-3 sessões**

**Como fazer:** O agente recebe o briefing da semana (carros em destaque, promoções, eventos) e gera um pacote com 6 posts: caption + hashtags + sugestão de formato (feed/reels/stories/carrossel). Diferente do agente de anúncios (que é por veículo), este é estratégico e recorrente.

#### Analista Financeiro Stage Motors

| Tarefa | Tempo |
|--------|-------|
| Definir template DRE padrão Stage | 1h |
| Criar prompt do agente financeiro | 3h |
| Construir dashboard interativo (React) | 3h |
| Testar com dados dos últimos 3 meses | 2h |

**Total: ~9h | 3-4 sessões**

#### Finanças Pessoais (NOVO)

| Tarefa | Tempo |
|--------|-------|
| Definir categorias de receita/despesa | 1h |
| Criar prompt do agente de finanças pessoais | 2h |
| Montar template de input mensal | 1h |
| Construir dashboard de patrimônio (React) | 3h |
| Testar com dados reais do mês atual | 1h |

**Total: ~8h | 3 sessões**

**Como fazer:** Você preenche um template mensal com receitas (Stage, AM CAR, empréstimos), despesas por categoria, e ativos/passivos. O agente gera: dashboard interativo com evolução patrimonial, taxa de poupança, projeção em cenários, e recomendações de alocação.

---

### Fase 3 — Universidade (Semanas 6-7)

| Agente | Tempo | Entregável |
|--------|-------|------------|
| Redator ABNT | 8h | Prompt + template .docx |
| Gerador de Slides | 6h | Prompt + template .pptx navy/gold |
| Pesquisador Acadêmico | 4h | Prompt + regras de busca |

**Total: ~18h | 6-7 sessões**

---

### Fase 4 — Renda Extra (Semana 8)

| Agente | Tempo | Entregável |
|--------|-------|------------|
| Criador de Conteúdo | 4h | Prompt + testes |
| Polymarket Bot (upgrades) | 4h | Bot atualizado + paper trading |
| Propostas Freelance | 5h | Prompt + landing page |

**Total: ~13h | 4-5 sessões**

---

## 4. Resumo geral

| Métrica | Valor |
|---------|-------|
| Total de agentes | 10 |
| Tempo total de construção | ~63h em 8 semanas |
| Horas por semana | ~8h (2-3 sessões) |
| Investimento mensal (início) | R$110 |
| Investimento mensal (máx) | R$240-590 |
| Economia estimada (Stage Motors) | 30h+/mês |
| Economia estimada (UNIFOR) | 15-20h/mês |

---

## 5. Priorização por ROI

| # | Agente | Impacto | Esforço | ROI | Prioridade |
|---|--------|---------|---------|-----|------------|
| 1 | Anúncios OLX/Instagram | ★★★★★ | Médio | ★★★★★ | Fase 1 |
| 2 | Assistente Instagram Stage | ★★★★☆ | Baixo | ★★★★☆ | Fase 2 |
| 3 | Financeiro Stage | ★★★★☆ | Médio | ★★★★☆ | Fase 2 |
| 4 | Finanças Pessoais | ★★★★☆ | Médio | ★★★★☆ | Fase 2 |
| 5 | Redator ABNT | ★★★★☆ | Médio | ★★★★☆ | Fase 3 |
| 6 | Slides | ★★★☆☆ | Baixo | ★★★☆☆ | Fase 3 |
| 7 | Pesquisa | ★★☆☆☆ | Baixo | ★★★☆☆ | Fase 3 |
| 8 | Conteúdo genérico | ★★★☆☆ | Baixo | ★★☆☆☆ | Fase 4 |
| 9 | Polymarket Bot | ★★☆☆☆ | Baixo | ★★☆☆☆ | Fase 4 |
| 10 | Freelance | ★★★★☆ | Médio | ★★★☆☆ | Fase 4 |

---

## 6. Próximo passo

**Fase 0 concluída.** Próximo: **Fase 1 — Agente de Anúncios da Stage Motors.**

Quando estiver pronto, diga: **"Bora fase 1"**
