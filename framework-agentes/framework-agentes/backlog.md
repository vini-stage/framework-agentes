# Backlog — Ideias para implementar depois

## 1. Automação de publicação nos portais via Chrome MCP

**Prioridade:** Alta
**Dependência:** Ativar Integrador Web no Revenda Mais + mapear telas

### Contexto
Hoje o Vinícius sobe anúncios manualmente 1 a 1 em cada portal (OLX, NaPista, Mobiauto, site Lua4). O agente de anúncios já gera o texto, mas a publicação ainda é manual.

### Solução proposta (Opção 3 — Híbrida)
1. Ativar o Integrador Web no Revenda Mais pra OLX, NaPista e Mobiauto
2. Agente gera o texto do anúncio (já funciona)
3. Claude in Chrome preenche os campos no Revenda Mais automaticamente
4. Claude in Chrome faz upload das fotos da pasta do veículo
5. Seleciona os portais e clica enviar → publicado em todos de uma vez

### O que o Claude in Chrome faria
- Preencher campos de texto (título, descrição, preço, dados técnicos)
- Upload de fotos da pasta `estoque/[carro]/fotos/`
- Selecionar dropdowns (marca, modelo, câmbio, combustível)
- Marcar checkboxes dos portais
- Clicar "Enviar"

### Pré-requisitos
- [ ] Conseguir prints das telas do Revenda Mais (cadastro de veículo + integrador)
- [ ] Confirmar quais portais já estão configurados no Revenda Mais
- [ ] Verificar com a Lua4 se ela puxa estoque do Revenda Mais

### Pesquisa já feita
- API do Revenda Mais é **somente leitura** (GET /inventory, GET /vehicles/sold, GET /vehicles/site)
- Limite de 300 requests/mês
- OLX tem API pública (developers.olx.com.br) — alternativa direta
- Mobiauto tem API REST via Easycar — precisa solicitar acesso
- NaPista não tem API pública — só via integrador
- Lua4 é plataforma fechada sem API pública

### Economia estimada
~5 min por carro × 40 carros/mês = ~3,3 horas/mês a mais de economia
