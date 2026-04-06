"""
Stage Motors — Atualizador de Dashboard Financeiro
===================================================
Uso:
    python atualizar_dashboard.py
    python atualizar_dashboard.py --pasta C:/caminho/dos/exports
    python atualizar_dashboard.py --sem-abrir

Espera encontrar na pasta (Downloads por padrão):
  - Demonstracao de Resultados no Exercicio (DRE)_*.PDF
  - Lista Gerencial de Veiculos Vendidos com Dados Da Venda_*.XLS
  - Listagem de Estoque_*.XLS  (ou Lista Gerencial de Estoque com Margem_*.XLS)
  - Lista Gerencial de Entrada de Estoque por Periodo com Fornecedor_*.XLS
  - Lista Gerencial de Veiculos com Lancamentos_*.XLS
  - Contas a Pagar_*.XLS  (opcional)
"""

import os, sys, re, json, glob, argparse, webbrowser
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date

# =========================================================
# CONFIG
# =========================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_JSON = os.path.join(SCRIPT_DIR, 'dashboard-data.json')
DASHBOARD_HTML = os.path.join(SCRIPT_DIR, 'dashboard.html')
DEFAULT_DOWNLOADS = os.path.expanduser('~/Downloads')

MESES_PT = {'jan':'01','fev':'02','mar':'03','abr':'04','mai':'05','jun':'06',
            'jul':'07','ago':'08','set':'09','out':'10','nov':'11','dez':'12'}
MESES_LABEL = ['','Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']

# Categorização de despesas do Revenda Mais → categorias do dashboard
DESP_MAP = {
    'COMISSÕES SOBRE VENDAS': 'pessoal',
    'FUNCIONÁRIOS - AJUDA DE CUSTO': 'pessoal',
    'FUNCIONÁRIOS - HORAS EXTRAS': 'pessoal',
    'FUNCIONÁRIOS - LAVADOR E POLIDOR': 'pessoal',
    'FUNCIONÁRIOS - SALÁRIOS ADMINISTRATIVO': 'pessoal',
    'FUNCIONÁRIOS - 13O. SALÁRIO': 'pessoal',
    'FUNCIONÁRIOS - GRATIFICAÇÕES': 'pessoal',
    'MOVIMENTAÇÃO - PRÓ-LABORE': 'pro_labore',
    'INFRAESTRUTURA - ALUGUÉIS': 'ocupacao',
    'INFRAESTRUTURA - CONSTRUÇÃO': 'ocupacao',
    'INFRAESTRUTURA - SEGURANÇA': 'ocupacao',
    'INFRAESTRUTURA - ÁGUA': 'utilidades',
    'INFRAESTRUTURA - ÁGUA/ENERGIA ELÉTRICA': 'utilidades',
    'INFRAESTRUTURA - INTERNET': 'utilidades',
    'MARKETING - PUBLICIDADE': 'marketing',
    'MARKETING - BRINDES': 'marketing',
    'ADMINISTRATIVAS - CONTADOR': 'administrativo',
    'ADMINISTRATIVAS - SOFTWARE': 'administrativo',
    'ADMINISTRATIVAS - SEGUROS': 'administrativo',
    'ADMINISTRATIVAS - MATERIAL DE ESCRITÓRIO': 'administrativo',
    'ADMINISTRATIVAS - MATERIAL DE LIMPEZA E CANTINA': 'administrativo',
    'ADMINISTRATIVAS - ASSOCIAÇÕES E SINDICATOS': 'administrativo',
    'ADMINISTRATIVAS - UBER/TAXI': 'administrativo',
    'ADMINISTRATIVAS - CORREIOS': 'administrativo',
    'ADMINISTRATIVAS - OUTRAS': 'administrativo',
    'CONFRATERNIZAÇÃO': 'administrativo',
    'PRODUTOS LAVACAR': 'administrativo',
    'IMPOSTOS - COFINS': 'impostos',
    'IMPOSTOS - CSLL': 'impostos',
    'IMPOSTOS - DARF': 'impostos',
    'IMPOSTOS - FGTS': 'impostos',
    'IMPOSTOS - FGTS ADM': 'impostos',
    'IMPOSTOS - ICMS': 'impostos',
    'IMPOSTOS - INSS': 'impostos',
    'IMPOSTOS - IRPJ': 'impostos',
    'IMPOSTOS - ISS': 'impostos',
    'IMPOSTOS - PIS': 'impostos',
    'MANUTENÇÃO - EQUIPAMENTOS': 'manutencao',
    'MANUTENÇÃO - VEICULOS GARANTIA': 'manutencao',
    'VEÍCULOS - COMBUSTÍVEIS E LUBRIFICANTES': 'veiculos_uso',
    'MOVIMENTAÇÃO - EMPRÉSTIMOS': 'financeiras',
    'INVESTIMENTOS - EQUIPAMENTOS': 'investimentos',
    'INVESTIMENTOS - OUTROS': 'investimentos',
    'DESPESAS HME': 'administrativo',
}

# Nomes amigáveis pra cada linha (para itens dentro das categorias)
DESP_LABEL = {
    'COMISSÕES SOBRE VENDAS': 'Comissões sobre vendas',
    'FUNCIONÁRIOS - AJUDA DE CUSTO': 'Ajuda de custo',
    'FUNCIONÁRIOS - HORAS EXTRAS': 'Horas extras',
    'FUNCIONÁRIOS - LAVADOR E POLIDOR': 'Lavador/polidor',
    'FUNCIONÁRIOS - SALÁRIOS ADMINISTRATIVO': 'Salários administrativo',
    'FUNCIONÁRIOS - 13O. SALÁRIO': '13º salário',
    'FUNCIONÁRIOS - GRATIFICAÇÕES': 'Gratificações',
    'MOVIMENTAÇÃO - PRÓ-LABORE': 'Pró-labore sócios',
    'INFRAESTRUTURA - ALUGUÉIS': 'Aluguéis',
    'INFRAESTRUTURA - CONSTRUÇÃO': 'Construção',
    'INFRAESTRUTURA - SEGURANÇA': 'Segurança',
    'INFRAESTRUTURA - ÁGUA': 'Água',
    'INFRAESTRUTURA - ÁGUA/ENERGIA ELÉTRICA': 'Energia elétrica',
    'INFRAESTRUTURA - INTERNET': 'Internet',
    'MARKETING - PUBLICIDADE': 'Publicidade',
    'MARKETING - BRINDES': 'Brindes',
    'ADMINISTRATIVAS - CONTADOR': 'Contador',
    'ADMINISTRATIVAS - SOFTWARE': 'Software',
    'ADMINISTRATIVAS - SEGUROS': 'Seguros',
    'ADMINISTRATIVAS - MATERIAL DE ESCRITÓRIO': 'Material escritório',
    'ADMINISTRATIVAS - MATERIAL DE LIMPEZA E CANTINA': 'Limpeza/cantina',
    'ADMINISTRATIVAS - ASSOCIAÇÕES E SINDICATOS': 'Associações',
    'ADMINISTRATIVAS - UBER/TAXI': 'Uber/táxi',
    'ADMINISTRATIVAS - CORREIOS': 'Correios',
    'ADMINISTRATIVAS - OUTRAS': 'Outras',
    'CONFRATERNIZAÇÃO': 'Confraternização',
    'PRODUTOS LAVACAR': 'Lavacar (produtos)',
    'MANUTENÇÃO - EQUIPAMENTOS': 'Equipamentos',
    'MANUTENÇÃO - VEICULOS GARANTIA': 'Veículos em garantia',
    'VEÍCULOS - COMBUSTÍVEIS E LUBRIFICANTES': 'Combustível/lubrificantes',
    'MOVIMENTAÇÃO - EMPRÉSTIMOS': 'Empréstimos',
    'INVESTIMENTOS - EQUIPAMENTOS': 'Equipamentos',
    'INVESTIMENTOS - OUTROS': 'Outros',
    'DESPESAS HME': 'HME',
}

# =========================================================
# HELPERS
# =========================================================
def num(s):
    if s is None or s == '': return 0
    try: return float(str(s).strip().replace('.', '').replace(',', '.'))
    except: return 0

def num_xls(s):
    """Número de XLS (usa ponto como decimal, sem separador de milhar)."""
    if s is None or s == '': return 0
    try: return float(str(s))
    except: return 0

def iso(s):
    if not s: return None
    return s.split('T')[0] if 'T' in s else s

def find_file(pasta, pattern):
    matches = glob.glob(os.path.join(pasta, pattern))
    return max(matches, key=os.path.getmtime) if matches else None

def pct(n, d):
    return round(n / d * 100, 1) if d else 0

# =========================================================
# XLS PARSER (SpreadsheetML / XML 2003)
# =========================================================
NS = 'urn:schemas-microsoft-com:office:spreadsheet'

def read_xls_rows(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for ws in root.iter('{%s}Worksheet' % NS):
        rows = []
        for row in ws.iter('{%s}Row' % NS):
            cur = 0
            cells = {}
            for cell in row.findall('{%s}Cell' % NS):
                idx_attr = cell.get('{%s}Index' % NS)
                if idx_attr: cur = int(idx_attr)
                else: cur += 1
                data = cell.find('{%s}Data' % NS)
                cells[cur] = data.text if (data is not None and data.text is not None) else ''
            rows.append(cells)
        return rows
    return []

def g(row, i): return row.get(i, '')

# =========================================================
# DRE PARSER (PDF via PyMuPDF)
# =========================================================
def parse_dre_pdf(path):
    """Parseia DRE do Revenda Mais (PDF). Retorna: meses (list), vendas_mes, receita_ops, outras_receitas, despesas, resultados."""
    import fitz
    doc = fitz.open(path)
    lines = []
    for p in doc:
        lines.extend(p.get_text().split('\n'))
    lines = [l.strip() for l in lines if l.strip()]

    # Detectar meses no header (ex: "Mar 2026", "Fev 2026", "Jan 2026")
    meses = []
    for l in lines:
        m = re.match(r'^(Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez)\s+(\d{4})$', l)
        if m and len(meses) < 3:
            mes_num = MESES_PT[m.group(1).lower()]
            meses.append(f'{m.group(2)}-{mes_num}')
    # Meses vêm ao contrário no PDF (mais recente primeiro)
    meses_reversed = list(reversed(meses))  # jan, fev, mar

    # Parsear linhas de dados: DESCRICAO seguida de N números (1 por mês + total)
    n_meses = len(meses)
    records = []
    i = 0
    skip_labels = {'Descrição', 'Página:', 'Vendas Veiculos', 'Receita Operacional',
                   'Outras Receitas', 'Despesas', 'Resultado', 'STAGE MOTORS TRADE',
                   'DEMONSTRAÇÃO DE RESULTADOS NO EXERCÍCIO (DRE)'}

    while i < len(lines):
        l = lines[i]
        # Pula headers e linhas irrelevantes
        if any(l.startswith(sk) for sk in skip_labels) or re.match(r'^\d+\s*$', l) or l in ('/', 'Total'):
            i += 1; continue
        # Tenta mes header (já capturado acima)
        if re.match(r'^(Jan|Fev|Mar|Abr|Mai|Jun|Jul|Ago|Set|Out|Nov|Dez)\s+\d{4}$', l):
            i += 1; continue
        # Tenta data/usuario
        if re.match(r'^\d+ de \w+ de \d{4}', l) or l.startswith('Usuário:'):
            i += 1; continue

        # Verifica se as próximas linhas são números
        if i + n_meses + 1 < len(lines):
            vals = []
            valid = True
            for j in range(1, n_meses + 2):  # n_meses + total
                s = lines[i + j].strip()
                try:
                    v = float(s.replace('.', '').replace(',', '.'))
                    vals.append(v)
                except ValueError:
                    valid = False
                    break
            if valid and len(vals) == n_meses + 1:
                # vals = [mais_recente, ..., mais_antigo, total]
                # Reverter pra [mais_antigo, ..., mais_recente]
                mes_vals = list(reversed(vals[:n_meses]))
                total = vals[-1]
                # Verificar se total ~= sum(mes_vals)
                if abs(sum(mes_vals) - total) < 2 or all(v == 0 for v in mes_vals):
                    records.append({
                        'descricao': l,
                        'valores': dict(zip(meses_reversed, mes_vals)),
                        'total': total
                    })
                    i += n_meses + 2
                    continue
        i += 1

    return meses_reversed, records

def build_dre_from_records(meses, records):
    """Transforma records em estrutura DRE por mês."""
    result = {}
    for mes in meses:
        result[mes] = {
            'vendas_qtd': 0,
            'margem_bruta_media_veiculo': 0,
            'receita_venda_veiculos': 0,
            'entrada_mercadorias': 0,
            'custo_lancamentos': 0,
            'receita_despachante': 0,
            'custo_despachante': 0,
            'margem_bruta': 0,
            'outras_receitas': {},
            'outras_receitas_total': 0,
            'despesas_raw': {},
            'despesas_total': 0,
            'resultado': 0,
        }

    for rec in records:
        desc = rec['descricao']
        for mes in meses:
            v = rec['valores'][mes]
            d = result[mes]
            if desc == 'TOTAL DE VENDAS DO MÊS':
                d['vendas_qtd'] = int(v)
            elif desc == 'MARGEM BRUTA MÉDIA POR VEÍCULO':
                d['margem_bruta_media_veiculo'] = v
            elif desc == 'RECEITA COM VENDAS':
                d['receita_venda_veiculos'] = v
            elif desc == 'ENTRADA DAS MERCADORIAS VENDIDAS':
                d['entrada_mercadorias'] = v
            elif desc == 'CUSTO DE LANÇAMENTOS':
                d['custo_lancamentos'] = v
            elif desc == 'RECEITA COM DESPACHANTE':
                d['receita_despachante'] = v
            elif desc == 'CUSTO COM DESPACHANTE':
                d['custo_despachante'] = v
            elif desc == 'MARGEM BRUTA':
                d['margem_bruta'] = v
            elif desc in ('COMISSÕES VENDA CONSIGNADO', 'OUTRAS RECEITA FINANCEIRAS',
                          'RECEITA PLUS SOBRE FINANCIAMENTOS', 'RECEITA SOBRE TRANSFERÊNCIA DE DOCUMENTOS',
                          'RETORNO SOBRE FINANCIAMENTO'):
                d['outras_receitas'][desc] = v
            elif desc == 'TOTAIS' and d['outras_receitas_total'] == 0 and d['despesas_total'] == 0:
                d['outras_receitas_total'] = v
            elif desc in DESP_MAP:
                d['despesas_raw'][desc] = abs(v)
            elif desc == 'TOTAIS' and d['outras_receitas_total'] > 0:
                d['despesas_total'] = abs(v)
            elif desc == 'TOTAL:':
                d['resultado'] = v

    # Preencher totais faltantes
    for mes in meses:
        d = result[mes]
        if d['outras_receitas_total'] == 0:
            d['outras_receitas_total'] = sum(d['outras_receitas'].values())
        if d['despesas_total'] == 0:
            d['despesas_total'] = sum(d['despesas_raw'].values())

    return result

def categorize_despesas(despesas_raw):
    """Agrupa despesas raw por categoria e retorna dict com {cat: {total, itens}}."""
    cats = defaultdict(lambda: {'total': 0, 'itens': {}})
    for desc, val in despesas_raw.items():
        cat = DESP_MAP.get(desc, 'administrativo')
        label = DESP_LABEL.get(desc, desc)
        cats[cat]['total'] += val
        cats[cat]['itens'][label] = val
    # Arredondar totais
    for c in cats:
        cats[c]['total'] = round(cats[c]['total'], 2)
    return dict(cats)

# =========================================================
# VENDIDOS PARSER
# =========================================================
def parse_vendidos(path):
    rows = read_xls_rows(path)
    vendidos = []
    for r in rows:
        cod = g(r, 2)
        if cod and str(cod).isdigit() and len(str(cod)) >= 6:
            venda = num_xls(g(r, 26))
            lucro = num_xls(g(r, 29))
            vendidos.append({
                'codigo': cod,
                'data_venda': iso(g(r, 4)),
                'modelo': g(r, 5),
                'ano': g(r, 6),
                'placa': g(r, 8),
                'data_compra': iso(g(r, 12)),
                'dias_estoque': int(num_xls(g(r, 14))),
                'compra': -num_xls(g(r, 15)),
                'lancamentos': -num_xls(g(r, 20)),
                'comissao': -num_xls(g(r, 23)),
                'custo_total': -num_xls(g(r, 24)),
                'valor_anuncio': num_xls(g(r, 25)),
                'venda': venda,
                'lucro': lucro,
                'margem_pct': round((lucro / venda) * 100, 2) if venda > 0 else 0,
                'cidade': g(r, 34),
            })
    return vendidos

# =========================================================
# ESTOQUE PARSER
# =========================================================
def parse_estoque(path):
    rows = read_xls_rows(path)
    estoque = []
    for r in rows:
        cod = g(r, 2)
        if cod and str(cod).isdigit() and len(str(cod)) >= 6:
            estoque.append({
                'codigo': cod,
                'marca': g(r, 4),
                'modelo': g(r, 5),
                'ano': g(r, 6),
                'placa': g(r, 8),
                'tipo': g(r, 11),
                'data_compra': iso(g(r, 12)),
                'dias_estoque': int(num_xls(g(r, 15))),
                'compra': -num_xls(g(r, 18)),
                'lancamentos_ate_agora': -num_xls(g(r, 22)),
                'valor_anuncio': num_xls(g(r, 25)),
                'fipe_atual': num_xls(g(r, 29)),
                'margem_esperada': num_xls(g(r, 31)),
            })
    return estoque

# =========================================================
# ENTRADAS (FORNECEDORES) PARSER
# =========================================================
def parse_entradas(path):
    rows = read_xls_rows(path)
    entradas = []
    for r in rows:
        cod = g(r, 1)
        if cod and str(cod).isdigit() and len(str(cod)) >= 6:
            entradas.append({
                'codigo': cod,
                'data_compra': iso(g(r, 17)),
                'marca': g(r, 3),
                'modelo': g(r, 4),
                'situacao': g(r, 11),
                'tipo': g(r, 13),
                'compra': -num_xls(g(r, 20)),
                'fornecedor': g(r, 32),
            })
    return entradas

# =========================================================
# GERA INSIGHTS AUTOMÁTICOS
# =========================================================
def gerar_insights_mes(mes_id, d, vendidos_mes, prev_d=None):
    insights = []
    n = d['veiculos_vendidos']
    rec = d['receita_bruta']
    res = d['resultado']
    mb = d['margem_bruta_pct']

    if res < 0:
        insights.append(f"Mês no vermelho: resultado de R$ {res:,.0f}. Margem bruta de {mb}%.".replace(',','.'))
    else:
        insights.append(f"Mês positivo: resultado de R$ {res:,.0f} com {n} carros vendidos e margem bruta de {mb}%.".replace(',','.'))

    if prev_d:
        delta_res = res - prev_d['resultado']
        sinal = '+' if delta_res > 0 else ''
        insights.append(f"Variação vs mês anterior: {sinal}R$ {delta_res:,.0f} no resultado.".replace(',','.'))

    if d.get('giro_estoque_dias'):
        insights.append(f"Giro médio de estoque: {d['giro_estoque_dias']:.0f} dias.")

    if d.get('lancamentos_por_veiculo'):
        insights.append(f"Lançamentos por veículo: R$ {d['lancamentos_por_veiculo']:,.0f}.".replace(',','.'))

    # Top/bottom vendas do mês
    if vendidos_mes:
        top = max(vendidos_mes, key=lambda x: x['lucro'])
        bot = min(vendidos_mes, key=lambda x: x['lucro'])
        insights.append(f"Melhor venda: {top['modelo'][:30]} ({top['margem_pct']:.1f}%, R$ {top['lucro']:,.0f}, {top['dias_estoque']}d).".replace(',','.'))
        if bot['lucro'] < 0:
            insights.append(f"Pior venda: {bot['modelo'][:30]} ({bot['margem_pct']:.1f}%, R$ {bot['lucro']:,.0f}, {bot['dias_estoque']}d).".replace(',','.'))

    return insights

def gerar_insights_estoque(estoque):
    capital = sum(e['valor_compra'] for e in estoque)
    criticos = [e for e in estoque if e['dias_parado'] >= 180]
    altos = [e for e in estoque if e['dias_parado'] >= 90]
    insights = [
        f"Capital parado em estoque: R$ {capital:,.0f} em {len(estoque)} carros.".replace(',','.'),
    ]
    if altos:
        cap_90 = sum(e['valor_compra'] for e in altos)
        insights.append(f"{len(altos)} carros com +90 dias (R$ {cap_90:,.0f} travados).".replace(',','.'))
    if criticos:
        top3 = sorted(criticos, key=lambda x: -x['dias_parado'])[:3]
        nomes = ', '.join(f"{e['veiculo']} ({e['dias_parado']}d)" for e in top3)
        insights.append(f"Carros críticos (+180d): {nomes}.")
    acima60 = [e for e in estoque if e['dias_parado'] >= 60]
    if acima60:
        insights.append(f"{len(acima60)} carros ({round(len(acima60)/len(estoque)*100)}% do estoque) acima de 60 dias.")
    return insights

# =========================================================
# MONTAGEM DO JSON FINAL
# =========================================================
def build_dashboard(pasta, dre_pdf, vendidos_xls, estoque_xls, entradas_xls):
    print('Parseando DRE PDF...')
    meses, records = parse_dre_pdf(dre_pdf)
    dre_data = build_dre_from_records(meses, records)
    print(f'  Meses detectados: {meses}')

    print('Parseando vendidos...')
    vendidos = parse_vendidos(vendidos_xls)
    print(f'  {len(vendidos)} veículos vendidos')

    print('Parseando estoque...')
    estoque_raw = parse_estoque(estoque_xls)
    print(f'  {len(estoque_raw)} carros em estoque')

    print('Parseando entradas/fornecedores...')
    entradas = parse_entradas(entradas_xls)
    print(f'  {len(entradas)} entradas')

    # Agregações de vendas por mês
    by_month = defaultdict(lambda: {'n':0,'venda':0,'lucro':0,'dias':[],'lanc':0})
    for v in vendidos:
        m = v['data_venda'][:7] if v['data_venda'] else '?'
        by_month[m]['n'] += 1
        by_month[m]['venda'] += v['venda']
        by_month[m]['lucro'] += v['lucro']
        by_month[m]['dias'].append(v['dias_estoque'])
        by_month[m]['lanc'] += v['lancamentos']

    # Montar dados_por_periodo
    dados_por_periodo = {}
    for mes in meses:
        d = dre_data[mes]
        rec_bruta = d['receita_venda_veiculos'] + d['receita_despachante']
        cmv = abs(d['entrada_mercadorias']) + abs(d['custo_lancamentos']) + abs(d['custo_despachante'])
        n_veic = d['vendas_qtd']
        mb = d['margem_bruta']
        despesas_cat = categorize_despesas(d['despesas_raw'])
        desp_total = sum(c['total'] for c in despesas_cat.values())
        resultado = mb + d['outras_receitas_total'] - desp_total

        periodo = {
            'veiculos_vendidos': n_veic,
            'receita_bruta': rec_bruta,
            'receita_venda_veiculos': d['receita_venda_veiculos'],
            'receita_despachante': d['receita_despachante'],
            'cmv': cmv,
            'cmv_entrada_mercadorias': abs(d['entrada_mercadorias']),
            'cmv_custo_lancamentos': abs(d['custo_lancamentos']),
            'cmv_custo_despachante': abs(d['custo_despachante']),
            'lucro_bruto': mb,
            'margem_bruta_pct': pct(mb, rec_bruta),
            'margem_bruta_por_veiculo': round(mb / n_veic, 2) if n_veic else 0,
            'outras_receitas_total': d['outras_receitas_total'],
            'despesas': despesas_cat,
            'despesas_total': round(desp_total, 2),
            'resultado': round(resultado, 2),
            'margem_liquida_pct': pct(resultado, rec_bruta),
        }

        # Adicionar giro/ticket/lancamentos dos XLS
        if mes in by_month and by_month[mes]['n'] > 0:
            bm = by_month[mes]
            periodo['giro_estoque_dias'] = round(sum(bm['dias'])/len(bm['dias']), 1) if bm['dias'] else None
            periodo['ticket_medio'] = round(bm['venda'] / bm['n'], 0)
            periodo['lancamentos_por_veiculo'] = round(bm['lanc'] / bm['n'], 0)

        dados_por_periodo[mes] = periodo

    # Q trimestral
    ano = meses[0][:4]
    q_id = None
    if len(meses) == 3:
        # Detectar qual trimestre
        m_nums = [int(m.split('-')[1]) for m in meses]
        if m_nums == [1,2,3]: q_id = f'Q1-{ano}'
        elif m_nums == [4,5,6]: q_id = f'Q2-{ano}'
        elif m_nums == [7,8,9]: q_id = f'Q3-{ano}'
        elif m_nums == [10,11,12]: q_id = f'Q4-{ano}'

    if q_id:
        # Somar os 3 meses
        q = {}
        sum_keys = ['veiculos_vendidos', 'receita_bruta', 'receita_venda_veiculos', 'receita_despachante',
                     'cmv', 'cmv_entrada_mercadorias', 'cmv_custo_lancamentos', 'cmv_custo_despachante',
                     'lucro_bruto', 'outras_receitas_total', 'despesas_total', 'resultado']
        for k in sum_keys:
            q[k] = sum(dados_por_periodo[m][k] for m in meses)
        q['margem_bruta_pct'] = pct(q['lucro_bruto'], q['receita_bruta'])
        q['margem_bruta_por_veiculo'] = round(q['lucro_bruto'] / q['veiculos_vendidos'], 2) if q['veiculos_vendidos'] else 0
        q['margem_liquida_pct'] = pct(q['resultado'], q['receita_bruta'])
        # Agregar despesas por categoria
        q_desp = defaultdict(lambda: {'total': 0, 'itens': defaultdict(float)})
        for m in meses:
            for cat, data in dados_por_periodo[m]['despesas'].items():
                q_desp[cat]['total'] += data['total']
                for item, val in data['itens'].items():
                    q_desp[cat]['itens'][item] += val
        q['despesas'] = {k: {'total': round(v['total'], 2), 'itens': dict(v['itens'])} for k, v in q_desp.items()}
        # Giro
        all_dias = [v['dias_estoque'] for v in vendidos]
        q['giro_estoque_dias'] = round(sum(all_dias)/len(all_dias), 1) if all_dias else None
        q['ticket_medio'] = round(sum(v['venda'] for v in vendidos) / len(vendidos), 0) if vendidos else 0
        q['lancamentos_por_veiculo'] = round(sum(v['lancamentos'] for v in vendidos) / len(vendidos), 0) if vendidos else 0
        dados_por_periodo[q_id] = q

    # Periodos disponíveis
    periodos_disp = [{'id': m, 'label': f'{MESES_LABEL[int(m.split("-")[1])]} / {m[:4]}', 'tipo': 'mensal'} for m in meses]
    if q_id:
        periodos_disp.append({'id': q_id, 'label': q_id.replace('-', ' / '), 'tipo': 'trimestral'})

    # Histórico mensal
    historico = [{'periodo': m, 'receita': dados_por_periodo[m]['receita_venda_veiculos'],
                  'lucro_liquido': dados_por_periodo[m]['resultado'],
                  'veiculos': dados_por_periodo[m]['veiculos_vendidos'],
                  'margem_bruta': dados_por_periodo[m]['lucro_bruto']} for m in meses]

    # Vendas detalhadas
    vendas_detalhe = [{
        'codigo': v['codigo'], 'data': v['data_venda'], 'veiculo': v['modelo'], 'ano': v['ano'],
        'placa': v['placa'], 'valor_venda': v['venda'], 'valor_compra': v['compra'],
        'lancamentos': v['lancamentos'], 'comissao': v['comissao'], 'valor_anuncio': v['valor_anuncio'],
        'lucro': v['lucro'], 'margem_pct': v['margem_pct'], 'dias_em_estoque': v['dias_estoque'],
        'cidade': v['cidade']
    } for v in vendidos]

    # Estoque formatado
    estoque_out = []
    for e in sorted(estoque_raw, key=lambda x: -x['dias_estoque']):
        alerta = 'CRÍTICO (+180d)' if e['dias_estoque'] >= 180 else (
            'ALTO (+90d)' if e['dias_estoque'] >= 90 else (
            'MÉDIO (+60d)' if e['dias_estoque'] >= 60 else 'OK'))
        estoque_out.append({
            'codigo': e['codigo'], 'veiculo': f"{e['marca']} {e['modelo']}".strip(),
            'ano': e['ano'], 'placa': e['placa'], 'tipo': e['tipo'],
            'data_compra': e['data_compra'], 'dias_parado': e['dias_estoque'],
            'valor_compra': e['compra'], 'lancamentos_ate_agora': e['lancamentos_ate_agora'],
            'preco_anuncio': e['valor_anuncio'], 'fipe_atual': e['fipe_atual'],
            'margem_esperada': e['margem_esperada'], 'alerta': alerta
        })

    # Fornecedores
    fornec = defaultdict(lambda: {'n': 0, 'valor': 0, 'carros': []})
    for e in entradas:
        if e['fornecedor']:
            fornec[e['fornecedor']]['n'] += 1
            fornec[e['fornecedor']]['valor'] += e['compra']
            fornec[e['fornecedor']]['carros'].append(f"{e['marca']} {e['modelo']}")
    top_forn = sorted(
        [{'nome': k, 'qtd': v['n'], 'valor_total': v['valor'], 'carros': v['carros']} for k, v in fornec.items()],
        key=lambda x: -x['valor_total']
    )[:15]

    # Insights automáticos
    insights_por_periodo = {}
    for i, mes in enumerate(meses):
        vend_mes = [v for v in vendidos if v['data_venda'] and v['data_venda'].startswith(mes)]
        prev = dados_por_periodo[meses[i-1]] if i > 0 else None
        insights_por_periodo[mes] = gerar_insights_mes(mes, dados_por_periodo[mes], vend_mes, prev)
    if q_id:
        insights_por_periodo[q_id] = [
            f"Resultado do trimestre: R$ {dados_por_periodo[q_id]['resultado']:,.0f}.".replace(',','.'),
            f"{dados_por_periodo[q_id]['veiculos_vendidos']} carros vendidos, ticket médio R$ {dados_por_periodo[q_id].get('ticket_medio',0):,.0f}.".replace(',','.'),
            f"Margem bruta média por veículo: R$ {dados_por_periodo[q_id]['margem_bruta_por_veiculo']:,.0f}.".replace(',','.'),
        ]

    insights_est = gerar_insights_estoque(estoque_out)

    # JSON final
    periodo_mais_recente = meses[-1]
    final = {
        'meta': {
            'loja': 'Stage Motors',
            'periodo_atual': periodo_mais_recente,
            'tipo': 'fechado',
            'atualizado_em': date.today().isoformat(),
            'moeda': 'BRL',
            'fonte': 'Revenda Mais (auto-import)'
        },
        'periodos_disponiveis': periodos_disp,
        'dados_por_periodo': dados_por_periodo,
        'historico_mensal': historico,
        'vendas_detalhe': vendas_detalhe,
        'estoque_parado': estoque_out,
        'top_fornecedores': top_forn,
        'insights_por_periodo': insights_por_periodo,
        'insights_estoque': insights_est,
        'acao_sugerida': ''
    }
    return final

# =========================================================
# INJETAR NO HTML
# =========================================================
def inject_into_html(data):
    if not os.path.exists(DASHBOARD_HTML):
        print(f'AVISO: {DASHBOARD_HTML} não encontrado, pulando injeção.')
        return
    compact = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    with open(DASHBOARD_HTML, 'r', encoding='utf-8') as f:
        html = f.read()
    html = re.sub(
        r'(<script id="embedded-data" type="application/json">)(.*?)(</script>)',
        lambda m: m.group(1) + compact + m.group(3),
        html, count=1, flags=re.DOTALL
    )
    with open(DASHBOARD_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Dados injetados no dashboard.html ({len(compact):,} chars)')

# =========================================================
# MAIN
# =========================================================
def main():
    parser = argparse.ArgumentParser(description='Atualiza dashboard financeiro Stage Motors')
    parser.add_argument('--pasta', default=DEFAULT_DOWNLOADS, help='Pasta com os exports do Revenda Mais')
    parser.add_argument('--sem-abrir', action='store_true', help='Não abrir o navegador depois')
    args = parser.parse_args()

    pasta = args.pasta
    print(f'Buscando exports em: {pasta}')
    print('=' * 60)

    # Descobrir arquivos
    dre_pdf = find_file(pasta, 'Demonstracao de Resultados no Exercicio (DRE)_*.PDF')
    vendidos_xls = find_file(pasta, 'Lista Gerencial de Veiculos Vendidos com Dados Da Venda_*.XLS')
    estoque_xls = find_file(pasta, 'Lista Gerencial de Estoque com Margem_*.XLS')
    entradas_xls = find_file(pasta, 'Lista Gerencial de Entrada de Estoque por Periodo com Fornecedor_*.XLS')

    # Verificar obrigatórios
    missing = []
    if not dre_pdf: missing.append('DRE (PDF)')
    if not vendidos_xls: missing.append('Veículos Vendidos (XLS)')
    if not estoque_xls: missing.append('Estoque com Margem (XLS)')
    if not entradas_xls: missing.append('Entrada por Fornecedor (XLS)')

    if missing:
        print(f'\n❌ FALTANDO: {", ".join(missing)}')
        print(f'\nExporte do Revenda Mais e coloque em: {pasta}')
        print('Arquivos esperados:')
        print('  1. Demonstracao de Resultados no Exercicio (DRE)_*.PDF')
        print('  2. Lista Gerencial de Veiculos Vendidos com Dados Da Venda_*.XLS')
        print('  3. Lista Gerencial de Estoque com Margem_*.XLS')
        print('  4. Lista Gerencial de Entrada de Estoque por Periodo com Fornecedor_*.XLS')
        sys.exit(1)

    print(f'DRE:        {os.path.basename(dre_pdf)}')
    print(f'Vendidos:   {os.path.basename(vendidos_xls)}')
    print(f'Estoque:    {os.path.basename(estoque_xls)}')
    print(f'Entradas:   {os.path.basename(entradas_xls)}')
    print()

    # Gerar
    data = build_dashboard(pasta, dre_pdf, vendidos_xls, estoque_xls, entradas_xls)

    # Salvar JSON
    with open(DASHBOARD_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'\n✅ dashboard-data.json salvo')
    print(f'   {len(data["vendas_detalhe"])} vendas | {len(data["estoque_parado"])} estoque | {len(data["top_fornecedores"])} fornecedores')

    # Injetar no HTML
    inject_into_html(data)

    # Resumo
    per = data['dados_por_periodo'][data['meta']['periodo_atual']]
    print(f'\n📊 Período mais recente: {data["meta"]["periodo_atual"]}')
    print(f'   Receita: R$ {per["receita_bruta"]:,.0f}'.replace(',','.'))
    print(f'   Resultado: R$ {per["resultado"]:,.0f}'.replace(',','.'))
    print(f'   Veículos: {per["veiculos_vendidos"]}')

    # Abrir navegador
    if not args.sem_abrir:
        url = 'file:///' + DASHBOARD_HTML.replace('\\', '/')
        print(f'\n🌐 Abrindo: {url}')
        webbrowser.open(url)

    print('\n✅ Concluído!')

if __name__ == '__main__':
    main()
