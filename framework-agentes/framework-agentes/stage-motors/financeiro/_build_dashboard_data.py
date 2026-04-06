"""Gera dashboard-data.json consolidado com dados reais da Stage Motors Q1 2026."""
import json
from collections import defaultdict

with open(r'C:/Users/Vinicius/Desktop/framework/framework-agentes/framework-agentes/stage-motors/financeiro/_raw_all.json', 'r', encoding='utf-8') as f:
    raw = json.load(f)

vendidos = raw['vendidos']
estoque = raw['estoque_atual']
entradas = raw['entradas']
lancamentos = raw['lancamentos_por_carro']

# ====== Agregações por mês (vem da DRE + reconciliado com planilhas) ======
# Mantém os valores da DRE como fonte primária pra DRE, e usa planilhas pra detalhe

by_month = defaultdict(lambda: {'n':0,'venda':0,'lucro':0,'dias':[],'lanc':0,'compra':0})
for v in vendidos:
    m = v['data_venda'][:7]
    by_month[m]['n'] += 1
    by_month[m]['venda'] += v['venda']
    by_month[m]['lucro'] += v['lucro']
    by_month[m]['dias'].append(v['dias_estoque'])
    by_month[m]['lanc'] += v['lancamentos']
    by_month[m]['compra'] += v['compra']

# ====== DRE por período (igual ao anterior — dados da DRE PDF) ======
dados_por_periodo = {
    "2026-01": {
        "veiculos_vendidos": 9,
        "receita_bruta": 760950, "receita_venda_veiculos": 754100, "receita_despachante": 6850,
        "cmv": 711365.98, "cmv_entrada_mercadorias": 653265.00, "cmv_custo_lancamentos": 47505.01, "cmv_custo_despachante": 10595.97,
        "lucro_bruto": 49584.02, "margem_bruta_pct": 6.5, "margem_bruta_por_veiculo": 5509.34,
        "outras_receitas_total": 6708.57,
        "despesas": {
            "pessoal":           { "total": 11158.00, "itens": { "Comissões sobre vendas": 3175, "Ajuda de custo": 1620, "Horas extras": 0, "Lavador/polidor": 2621, "Salários administrativo": 3742 }},
            "pro_labore":        { "total": 13000.00, "itens": { "Pró-labore sócios": 13000 }},
            "ocupacao":          { "total": 9769.85,  "itens": { "Aluguéis": 7236.51, "Construção": 2333.34, "Segurança": 200 }},
            "utilidades":        { "total": 1217.96,  "itens": { "Água": 44, "Energia elétrica": 991.30, "Internet": 182.66 }},
            "marketing":         { "total": 4119.70,  "itens": { "Publicidade": 4119.70, "Brindes": 0 }},
            "administrativo":    { "total": 13850.87, "itens": { "Contador": 1021.25, "Software": 6868.06, "Seguros": 1750.46, "Material escritório": 55.80, "Limpeza/cantina": 1176.69, "Associações": 300, "Uber/táxi": 393.08, "Confraternização": 2285.53, "Correios": 0, "Outras": 0, "Lavacar (produtos)": 0 }},
            "impostos":          { "total": 15085.12, "itens": { "COFINS": 1610.39, "CSLL": 3498.03, "DARF": 31.45, "FGTS": 374.98, "FGTS ADM": 182, "ICMS": 1416.98, "INSS": 1500.53, "IRPJ": 5199.18, "ISS": 922.66, "PIS": 348.92 }},
            "manutencao":        { "total": 4791.31,  "itens": { "Equipamentos": 0, "Veículos em garantia": 4791.31 }},
            "veiculos_uso":      { "total": 258.52,   "itens": { "Combustível/lubrificantes": 258.52 }},
            "financeiras":       { "total": 8645.16,  "itens": { "Empréstimos": 8645.16 }},
            "investimentos":     { "total": 214.08,   "itens": { "Equipamentos": 0, "Outros": 214.08 }}
        },
        "despesas_total": 82110.57, "resultado": -25817.98, "margem_liquida_pct": -3.4
    },
    "2026-02": {
        "veiculos_vendidos": 12,
        "receita_bruta": 1252000, "receita_venda_veiculos": 1245600, "receita_despachante": 6400,
        "cmv": 1183777.99, "cmv_entrada_mercadorias": 1112012.80, "cmv_custo_lancamentos": 63615.52, "cmv_custo_despachante": 8149.67,
        "lucro_bruto": 68222.01, "margem_bruta_pct": 5.4, "margem_bruta_por_veiculo": 5685.17,
        "outras_receitas_total": 13536.71,
        "despesas": {
            "pessoal":           { "total": 11413.00, "itens": { "Comissões sobre vendas": 3350, "Ajuda de custo": 1500, "Horas extras": 200, "Lavador/polidor": 3121, "Salários administrativo": 3242 }},
            "pro_labore":        { "total": 13000.00, "itens": { "Pró-labore sócios": 13000 }},
            "ocupacao":          { "total": 9769.76,  "itens": { "Aluguéis": 7236.43, "Construção": 2333.33, "Segurança": 200 }},
            "utilidades":        { "total": 1080.29,  "itens": { "Água": 44, "Energia elétrica": 1036.29, "Internet": 0 }},
            "marketing":         { "total": 8186.25,  "itens": { "Publicidade": 5711.75, "Brindes": 2474.50 }},
            "administrativo":    { "total": 12997.92, "itens": { "Contador": 1090.60, "Software": 7436.91, "Seguros": 1750.46, "Limpeza/cantina": 122.35, "Associações": 300, "Uber/táxi": 547.56, "Confraternização": 262.44, "Lavacar (produtos)": 1487.60, "Material escritório": 0, "Correios": 0, "Outras": 0 }},
            "impostos":          { "total": 4942.09,  "itens": { "COFINS": 699.47, "FGTS": 398.40, "ICMS": 1480.20, "INSS": 1599.70, "ISS": 612.77, "PIS": 151.55, "CSLL": 0, "DARF": 0, "FGTS ADM": 0, "IRPJ": 0 }},
            "manutencao":        { "total": 5459.93,  "itens": { "Equipamentos": 0, "Veículos em garantia": 5459.93 }},
            "veiculos_uso":      { "total": 861.31,   "itens": { "Combustível/lubrificantes": 861.31 }},
            "financeiras":       { "total": 8668.61,  "itens": { "Empréstimos": 8668.61 }},
            "investimentos":     { "total": 1135.02,  "itens": { "Equipamentos": 920.98, "Outros": 214.04 }}
        },
        "despesas_total": 77514.18, "resultado": 4244.54, "margem_liquida_pct": 0.3
    },
    "2026-03": {
        "veiculos_vendidos": 11,
        "receita_bruta": 1398200, "receita_venda_veiculos": 1394900, "receita_despachante": 3300,
        "cmv": 1266512.68, "cmv_entrada_mercadorias": 1226590.23, "cmv_custo_lancamentos": 33946.96, "cmv_custo_despachante": 5975.49,
        "lucro_bruto": 131687.32, "margem_bruta_pct": 9.4, "margem_bruta_por_veiculo": 11971.57,
        "outras_receitas_total": 9199.20,
        "despesas": {
            "pessoal":           { "total": 9334.00,  "itens": { "Comissões sobre vendas": 2275, "Ajuda de custo": 1896, "Horas extras": 0, "Lavador/polidor": 1921, "Salários administrativo": 3242 }},
            "pro_labore":        { "total": 13000.00, "itens": { "Pró-labore sócios": 13000 }},
            "ocupacao":          { "total": 7436.43,  "itens": { "Aluguéis": 7236.43, "Construção": 0, "Segurança": 200 }},
            "utilidades":        { "total": 1205.19,  "itens": { "Água": 0, "Energia elétrica": 955.21, "Internet": 249.98 }},
            "marketing":         { "total": 2987.72,  "itens": { "Publicidade": 2987.72, "Brindes": 0 }},
            "administrativo":    { "total": 10375.58, "itens": { "Contador": 1090.60, "Software": 6846.16, "Seguros": 1750.50, "Limpeza/cantina": 144.58, "Associações": 300, "Correios": 29.70, "Outras": 214.04, "Uber/táxi": 0, "Confraternização": 0, "Material escritório": 0, "Lavacar (produtos)": 0 }},
            "impostos":          { "total": 5038.99,  "itens": { "COFINS": 818.45, "FGTS": 398.40, "ICMS": 1480.20, "INSS": 1639.44, "ISS": 525.17, "PIS": 177.33, "CSLL": 0, "DARF": 0, "FGTS ADM": 0, "IRPJ": 0 }},
            "manutencao":        { "total": 6946.12,  "itens": { "Equipamentos": 180, "Veículos em garantia": 6766.12 }},
            "veiculos_uso":      { "total": 369.29,   "itens": { "Combustível/lubrificantes": 369.29 }},
            "financeiras":       { "total": 6300.00,  "itens": { "Empréstimos": 6300 }},
            "investimentos":     { "total": 0,        "itens": { "Equipamentos": 0, "Outros": 0 }}
        },
        "despesas_total": 62993.32, "resultado": 77893.20, "margem_liquida_pct": 5.6
    },
    "Q1-2026": {
        "veiculos_vendidos": 32,
        "receita_bruta": 3411150, "receita_venda_veiculos": 3394600, "receita_despachante": 16550,
        "cmv": 3161656.65, "cmv_entrada_mercadorias": 2991868.03, "cmv_custo_lancamentos": 145067.49, "cmv_custo_despachante": 24721.13,
        "lucro_bruto": 249493.35, "margem_bruta_pct": 7.3, "margem_bruta_por_veiculo": 7796.67,
        "outras_receitas_total": 29444.48,
        "despesas": {
            "pessoal":           { "total": 31905.00, "itens": { "Comissões sobre vendas": 8800, "Ajuda de custo": 5016, "Horas extras": 200, "Lavador/polidor": 7663, "Salários administrativo": 10226 }},
            "pro_labore":        { "total": 39000.00, "itens": { "Pró-labore sócios": 39000 }},
            "ocupacao":          { "total": 26976.04, "itens": { "Aluguéis": 21709.37, "Construção": 4666.67, "Segurança": 600 }},
            "utilidades":        { "total": 3503.44,  "itens": { "Água": 88, "Energia elétrica": 2982.80, "Internet": 432.64 }},
            "marketing":         { "total": 15293.67, "itens": { "Publicidade": 12819.17, "Brindes": 2474.50 }},
            "administrativo":    { "total": 37224.37, "itens": { "Contador": 3202.45, "Software": 21151.13, "Seguros": 5251.42, "Limpeza/cantina": 1443.62, "Associações": 900, "Uber/táxi": 940.64, "Confraternização": 2547.97, "Lavacar (produtos)": 1487.60, "Material escritório": 55.80, "Correios": 29.70, "Outras": 214.04 }},
            "impostos":          { "total": 25066.20, "itens": { "COFINS": 3128.31, "CSLL": 3498.03, "DARF": 31.45, "FGTS": 1171.78, "FGTS ADM": 182, "ICMS": 4377.38, "INSS": 4739.67, "IRPJ": 5199.18, "ISS": 2060.60, "PIS": 677.80 }},
            "manutencao":        { "total": 17197.36, "itens": { "Equipamentos": 180, "Veículos em garantia": 17017.36 }},
            "veiculos_uso":      { "total": 1489.12,  "itens": { "Combustível/lubrificantes": 1489.12 }},
            "financeiras":       { "total": 23613.77, "itens": { "Empréstimos": 23613.77 }},
            "investimentos":     { "total": 1349.10,  "itens": { "Equipamentos": 920.98, "Outros": 428.12 }}
        },
        "despesas_total": 222618.07, "resultado": 56319.76, "margem_liquida_pct": 1.7
    }
}

# Adicionar stats de giro em cada período
for pid, d in by_month.items():
    dias_med = sum(d['dias']) / len(d['dias']) if d['dias'] else 0
    if pid in dados_por_periodo:
        dados_por_periodo[pid]['giro_estoque_dias'] = round(dias_med, 1)
        dados_por_periodo[pid]['ticket_medio'] = round(d['venda'] / d['n'], 0)
        dados_por_periodo[pid]['lancamentos_por_veiculo'] = round(d['lanc'] / d['n'], 0)

# Q1 agregado
all_dias = [v['dias_estoque'] for v in vendidos]
dados_por_periodo['Q1-2026']['giro_estoque_dias'] = round(sum(all_dias)/len(all_dias), 1)
dados_por_periodo['Q1-2026']['ticket_medio'] = round(sum(v['venda'] for v in vendidos) / 32, 0)
dados_por_periodo['Q1-2026']['lancamentos_por_veiculo'] = round(sum(v['lancamentos'] for v in vendidos) / 32, 0)

# ====== VENDAS DETALHADAS (enriquecidas com planilha) ======
vendas_detalhe = []
for v in vendidos:
    vendas_detalhe.append({
        "codigo": v['codigo'],
        "data": v['data_venda'],
        "veiculo": v['modelo'],
        "ano": v['ano'],
        "placa": v['placa'],
        "valor_venda": v['venda'],
        "valor_compra": v['compra'],
        "lancamentos": v['lancamentos'],
        "comissao": v['comissao'],
        "valor_anuncio": v['valor_anuncio'],
        "lucro": v['lucro'],
        "margem_pct": v['margem_pct'],
        "dias_em_estoque": v['dias_estoque'],
        "cidade": v['cidade']
    })

# ====== ESTOQUE PARADO ======
estoque_atual = sorted(estoque, key=lambda x: -x['dias_estoque'])
parados_90 = [e for e in estoque_atual if e['dias_estoque'] >= 90]
parados_60 = [e for e in estoque_atual if 60 <= e['dias_estoque'] < 90]
capital_parado_total = sum(e['compra'] for e in estoque_atual)
capital_parado_90 = sum(e['compra'] for e in parados_90)

# ====== INSIGHTS REAIS ======
insights_por_periodo = {
    "2026-01": [
        "Prejuízo de R$ 25.818 no mês apesar de vender 9 carros. Margem bruta de apenas 6,5%.",
        "Lançamentos por veículo: R$ 5.278 — média alta, indicando carros entrando com muita preparação necessária.",
        "Tempo médio de estoque: 76 dias. Carros como Eclipse Cross (207d) e Compass (87d) puxaram pra cima.",
        "Impostos pesaram R$ 15.085 com CSLL+IRPJ do trimestre anterior caindo em janeiro (R$ 8.697 só esses dois).",
        "Destaque positivo: VW Golf Highline vendeu com 22,2% de margem (R$ 18.198 de lucro) em 39 dias — mostra que tem mix que funciona."
    ],
    "2026-02": [
        "Saiu do vermelho por pouco: +R$ 4.244. Maior volume do trimestre (12 carros), mas margem ainda apertada (5,4%).",
        "L200 Triton parada 365 dias vendeu com prejuízo de R$ 13.236 + lançamentos de R$ 31.829. Case clássico de carro zumbi.",
        "Equinox Premier (199d, 7% acima do FIPE) virou com lucro quase zero (R$ 3.739 em 199 dias). Melhor ter vendido antes.",
        "Marketing saltou pra R$ 8.186 (brindes R$ 2.474 + publicidade R$ 5.711) — maior do tri. Vale medir o retorno.",
        "Impostos caíram 67% vs Jan — sem CSLL/IRPJ apurados neste mês."
    ],
    "2026-03": [
        "Mês redondo: lucro de R$ 77.893 (138% do resultado do tri inteiro). Margem bruta explodiu pra 9,4%.",
        "CHAVE DA VIRADA → Giro de estoque caiu pra 28 dias (vs 76 em Jan e 73 em Fev). Carros rodando 2,6x mais rápido.",
        "Lançamentos por veículo despencaram pra R$ 3.086 (−42% vs média Jan/Fev de R$ 5.290). Menos carro problema entrando.",
        "Top vendas do mês: Discovery Sport D200 (14,4%, R$ 34.159 lucro, 21d) e Ranger Ltd (14,5%, R$ 24.403, 28d).",
        "Manutenção em garantia subiu pra R$ 6.766 — contraste com o resto. Curadoria melhorou na entrada mas pós-venda ainda cobra.",
        "Despesas operacionais caíram pra R$ 62.993 (-23% vs Jan). Sem brindes, sem obra, sem investimento."
    ],
    "Q1-2026": [
        "Lucro líquido do trimestre: R$ 56.319. MAS sem Março (R$ 77.893), Q1 seria −R$ 21.573. Dependência crítica de 1 mês.",
        "32 carros vendidos, ticket médio R$ 106.081, giro médio 58 dias. Em Março o giro caiu pra 28 — se sustentar abril, o modelo muda de patamar.",
        "2 vendas destruíram R$ 25.497 de margem: L200 Triton (−R$13.236 em 365 dias) e Eclipse Cross (−R$12.261 em 207 dias). Padrão: carro que passa de 180 dias vira zumbi.",
        "Pró-labore R$ 39.000 no tri é a maior linha (17,5% despesas). Software R$ 21.151 (9,5%). Manutenção garantia R$ 17.017 (R$ 531/carro vendido).",
        "Despesas financeiras R$ 23.613 em juros de empréstimo no tri — peso relevante, entender origem (financiamento de estoque?)."
    ]
}

# ====== INSIGHTS DE ESTOQUE ATUAL ======
insights_estoque = [
    f"Capital parado em estoque: R$ {capital_parado_total:,.0f} em {len(estoque_atual)} carros.".replace(',', '.'),
    f"{len(parados_90)} carros com +90 dias (R$ {capital_parado_90:,.0f} travados) — {round(capital_parado_90/capital_parado_total*100, 1)}% do capital em estoque.".replace(',', '.'),
    "Top 3 carros zumbi: Duster 4x4 (708 dias!!), Bolt Premier (285d) e Mini JCW (268d) — juntos R$ 395.500 parados.",
    "Alerta de preço: Hyundai Creta (215d) e IX35 (145d) estão anunciados exatamente no valor de compra ou abaixo — prejuízo certo se vender.",
    "11 carros (39% do estoque) estão acima de 60 dias. Meta: derrubar pra <30% até fim de maio."
]

# ====== HISTÓRICO MENSAL ======
historico_mensal = [
    { "periodo": "2026-01", "receita": 754100, "lucro_liquido": -25817.98, "veiculos": 9, "margem_bruta": 49584.02 },
    { "periodo": "2026-02", "receita": 1245600, "lucro_liquido": 4244.54, "veiculos": 12, "margem_bruta": 68222.01 },
    { "periodo": "2026-03", "receita": 1394900, "lucro_liquido": 77893.20, "veiculos": 11, "margem_bruta": 131687.32 }
]

# ====== ESTOQUE PARADO FORMATADO ======
estoque_parado_out = []
for e in estoque_atual:
    alerta = 'CRÍTICO (+180d)' if e['dias_estoque'] >= 180 else ('ALTO (+90d)' if e['dias_estoque'] >= 90 else ('MÉDIO (+60d)' if e['dias_estoque'] >= 60 else 'OK'))
    estoque_parado_out.append({
        "codigo": e['codigo'],
        "veiculo": f"{e['marca']} {e['modelo']}".strip(),
        "ano": e['ano'],
        "placa": e['placa'],
        "tipo": e['tipo'],
        "data_compra": e['data_compra'],
        "dias_parado": e['dias_estoque'],
        "valor_compra": e['compra'],
        "lancamentos_ate_agora": e['lancamentos_ate_agora'],
        "preco_anuncio": e['valor_anuncio'],
        "fipe_atual": e['fipe_atual'],
        "margem_esperada": e['margem_esperada'],
        "alerta": alerta
    })

# ====== FORNECEDORES ======
fornec = defaultdict(lambda: {'n':0,'valor':0,'carros':[]})
for e in entradas:
    if e['fornecedor']:
        fornec[e['fornecedor']]['n'] += 1
        fornec[e['fornecedor']]['valor'] += e['compra']
        fornec[e['fornecedor']]['carros'].append(f"{e['marca']} {e['modelo']}")

top_fornecedores = sorted(
    [{"nome": k, "qtd": v['n'], "valor_total": v['valor'], "carros": v['carros']} for k, v in fornec.items()],
    key=lambda x: -x['valor_total']
)[:15]

# ====== MONTA JSON FINAL ======
final = {
    "meta": {
        "loja": "Stage Motors",
        "periodo_atual": "2026-03",
        "tipo": "fechado",
        "atualizado_em": "2026-04-05",
        "moeda": "BRL",
        "fonte": "DRE + 6 relatórios Revenda Mais (export 05/04/2026)"
    },
    "periodos_disponiveis": [
        { "id": "2026-01", "label": "Jan / 2026", "tipo": "mensal" },
        { "id": "2026-02", "label": "Fev / 2026", "tipo": "mensal" },
        { "id": "2026-03", "label": "Mar / 2026", "tipo": "mensal" },
        { "id": "Q1-2026",  "label": "Q1 / 2026", "tipo": "trimestral" }
    ],
    "dados_por_periodo": dados_por_periodo,
    "historico_mensal": historico_mensal,
    "vendas_detalhe": vendas_detalhe,
    "estoque_parado": estoque_parado_out,
    "top_fornecedores": top_fornecedores,
    "insights_por_periodo": insights_por_periodo,
    "insights_estoque": insights_estoque,
    "acao_sugerida": "Prioridade 1: liquidar os 3 carros zumbi do estoque atual (Duster 708d, Bolt 285d, Mini 268d) mesmo com margem reduzida — libera R$ 395.500. Prioridade 2: manter o giro de 28 dias alcançado em Março como padrão de abril. Prioridade 3: investigar por que a linha de manutenção em garantia subiu em Março (R$ 6.766) apesar da curadoria melhor na entrada."
}

out = r'C:/Users/Vinicius/Desktop/framework/framework-agentes/framework-agentes/stage-motors/financeiro/dashboard-data.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print('dashboard-data.json gerado')
print(f'  - {len(vendas_detalhe)} vendas')
print(f'  - {len(estoque_parado_out)} carros em estoque')
print(f'  - {len(top_fornecedores)} fornecedores')
print(f'  - {sum(len(v) for v in insights_por_periodo.values())} insights')
