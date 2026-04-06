# Template DRE — Stage Motors

> Plano de contas padrão pra fechamento mensal. Usar como referência ao alimentar o agente financeiro.

---

## Estrutura

### 1. RECEITAS

| Conta | Descrição | Observação |
|-------|-----------|------------|
| 1.1 | Venda de veículos | Valor bruto da nota/recibo de venda |
| 1.2 | Venda de acessórios | Se houver (tapete, película, som) |
| 1.3 | Comissão de seguro | Se indicar seguradora parceira |
| 1.4 | Comissão de consórcio | Se indicar consórcio parceiro |
| 1.5 | Outras receitas | Qualquer entrada não classificada acima |

### 2. DEDUÇÕES DA RECEITA

| Conta | Descrição |
|-------|-----------|
| 2.1 | Devoluções e cancelamentos |
| 2.2 | Impostos sobre venda (se houver — Simples/MEI geralmente já está embutido) |

### 3. CUSTO DOS VEÍCULOS VENDIDOS (CMV)

> Regra de ouro: **só conta o custo dos carros que foram VENDIDOS no mês**, não do estoque em aberto.

| Conta | Descrição |
|-------|-----------|
| 3.1 | Valor de aquisição do veículo (leilão, particular, troca) |
| 3.2 | Reparo mecânico necessário pra venda |
| 3.3 | Funilaria e pintura (quando for no AM CAR interno, usar custo real) |
| 3.4 | Lavagem, polimento, higienização |
| 3.5 | Documentação (transferência, IPVA quitado pela loja) |
| 3.6 | Frete/guincho para trazer o carro ao pátio |
| 3.7 | Avaliação e vistoria de entrada |

### 4. DESPESAS OPERACIONAIS

#### 4.1 Pessoal
- Salários + encargos (CLT)
- Pró-labore sócios
- Comissão de vendedores
- Comissão de indicadores/parceiros
- Benefícios (VT, VR, plano de saúde)

#### 4.2 Ocupação
- Aluguel do pátio
- Condomínio
- IPTU (se não embutido no aluguel)

#### 4.3 Utilidades
- Energia elétrica
- Água
- Internet
- Telefone / celular corporativo

#### 4.4 Marketing
- Instagram Ads
- Facebook Ads
- OLX destaque (impulsionamento)
- Mobiauto / NaPista (planos pagos)
- Site próprio (hospedagem, domínio)
- Material gráfico (placas, adesivos)
- Fotos profissionais (se terceirizar)

#### 4.5 Administrativo
- Contador / escritório contábil
- Honorários advogados
- Cartório e tabelionato
- Softwares (Revenda Mais, outros)
- Material de escritório

#### 4.6 Manutenção do pátio
- Limpeza e jardinagem
- Segurança / monitoramento
- Pequenos reparos na estrutura

#### 4.7 Veículos de uso da loja
- Combustível (test drive, busca de carros)
- Manutenção da frota de uso
- Pedágio e estacionamento

#### 4.8 Outros
- Doações, cortesias, eventuais

### 5. RESULTADO FINANCEIRO

| Conta | Descrição |
|-------|-----------|
| 5.1 | Despesas bancárias (tarifas, IOF, TED/PIX) |
| 5.2 | Juros pagos (se tiver financiamento de estoque) |
| 5.3 | Receita de aplicação financeira |

### 6. IMPOSTOS SOBRE O LUCRO

| Conta | Descrição |
|-------|-----------|
| 6.1 | DAS Simples Nacional (ou IRPJ/CSLL se Lucro Presumido) |

---

## Exemplo preenchido (mês fictício)

```
RECEITA BRUTA                               R$ 820.000,00
  Venda de veículos                         R$ 815.000,00
  Comissão de seguro                        R$   5.000,00

(−) DEDUÇÕES                                R$       0,00

(=) RECEITA LÍQUIDA                         R$ 820.000,00

(−) CMV                                     R$ 710.000,00
  Aquisição veículos vendidos               R$ 690.000,00
  Preparação/reparos                        R$  14.000,00
  Documentação                              R$   6.000,00

(=) LUCRO BRUTO                             R$ 110.000,00
    Margem bruta: 13,4%

(−) DESPESAS OPERACIONAIS                   R$  52.800,00
  Pessoal                                   R$  22.000,00
    Pró-labore sócios                       R$  12.000,00
    Comissões                               R$  10.000,00
  Ocupação (aluguel)                        R$   8.500,00
  Utilidades                                R$   1.200,00
  Marketing                                 R$   6.500,00
  Administrativo                            R$   3.400,00
  Manutenção pátio                          R$   1.800,00
  Combustível/deslocamento                  R$   1.400,00
  Softwares                                 R$     800,00
  Outras                                    R$     500,00

(=) EBITDA                                  R$  57.200,00
    Margem EBITDA: 7,0%

(−) Despesas financeiras                    R$     450,00
(+) Receitas financeiras                    R$     180,00

(=) RESULTADO ANTES DE IMPOSTOS             R$  56.930,00

(−) DAS Simples (~6%)                       R$  49.200,00
    (sobre receita bruta de venda)

(=) LUCRO LÍQUIDO                           R$   7.730,00
    Margem líquida: 0,9%
```

**Observação:** o DAS do Simples Nacional para revenda de veículos usados tem regra específica (geralmente sobre margem, não receita bruta) — confirmar com o contador a fórmula exata antes de usar no cálculo real.

---

## Métricas de apoio do mês exemplo

- Veículos vendidos: **6**
- Ticket médio: R$ 135.833,33
- Margem bruta por veículo: R$ 18.333,33
- Giro de estoque médio: **48 dias**
- Break-even operacional: **3 veículos/mês** (só pra cobrir despesas operacionais)

---

## Regras de preenchimento

1. **Data do fato gerador manda.** Venda de 31/03 com recebimento em 02/04 entra em março.
2. **Despesa vai pelo regime de competência.** Aluguel de abril pago em 05/04 é despesa de abril.
3. **Troca de carro:** o valor da troca vira custo de aquisição do carro que entrou no estoque. A venda do carro que saiu registra o valor cheio (não o valor líquido da troca).
4. **AM CAR (funilaria interna):** quando o reparo é feito no AM CAR, usar o custo de materiais + mão de obra a valor de custo — não o valor que o AM CAR cobraria de terceiros.
5. **Pró-labore ≠ lucro distribuído.** Pró-labore é despesa operacional; lucro distribuído sai depois do lucro líquido.
