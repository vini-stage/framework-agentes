# Configuração — MCP Servers

## Conexões ativas

### Google Calendar
- **URL:** https://gcal.mcp.claude.com/mcp
- **Status:** Conectado
- **Uso:** Agendamento de entregas, lembretes de prazos acadêmicos, compromissos Stage Motors

### Gmail
- **URL:** https://gmail.mcp.claude.com/mcp
- **Status:** Conectado
- **Uso:** Envio de relatórios financeiros, trabalhos acadêmicos, propostas de freelance

## Conexões recomendadas (configurar quando disponível)

### Google Drive
- **Uso:** Salvar outputs (.docx, .pptx, .xlsx) diretamente em pastas organizadas
- **Estrutura de pastas sugerida:**
  - `/Stage Motors/Anúncios/[mês-ano]/`
  - `/Stage Motors/Financeiro/[mês-ano]/`
  - `/Stage Motors/Instagram/`
  - `/UNIFOR/[Disciplina]/[Trabalho]/`
  - `/Pessoal/Finanças/[mês-ano]/`
  - `/Freelance/[Cliente]/`

## Como usar nos agentes

Cada agente pode acessar MCP tools nativamente no Claude Code e Cowork.
Exemplo de uso no prompt do agente:
- "Após gerar o arquivo, salve no Google Drive na pasta correspondente"
- "Consulte o Google Calendar para verificar prazo de entrega"
- "Envie o relatório por Gmail para [destinatário]"
