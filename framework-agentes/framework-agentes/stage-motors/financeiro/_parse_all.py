import xml.etree.ElementTree as ET
import json
from collections import defaultdict

base = r'C:/Users/Vinicius/Downloads/'
NS = 'urn:schemas-microsoft-com:office:spreadsheet'

def read_rows(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for ws in root.iter('{%s}Worksheet' % NS):
        rows = []
        for row in ws.iter('{%s}Row' % NS):
            cur = 0
            cells = {}
            for cell in row.findall('{%s}Cell' % NS):
                idx = cell.get('{%s}Index' % NS)
                if idx: cur = int(idx)
                else: cur += 1
                data = cell.find('{%s}Data' % NS)
                cells[cur] = data.text if (data is not None and data.text is not None) else ''
            rows.append(cells)
        return rows

def g(r, i): return r.get(i, '')
def num(s):
    if s is None or s == '': return 0
    try: return float(str(s).replace(',', '.'))
    except: return 0
def iso(s):
    if not s: return None
    return s.split('T')[0] if 'T' in s else s

# ==== VENDIDOS ====
rows = read_rows(base + 'Lista Gerencial de Veiculos Vendidos com Dados Da Venda_05042026.XLS')
vendidos = []
for r in rows:
    cod = g(r, 2)
    if cod and str(cod).isdigit() and len(str(cod)) >= 6:
        venda = num(g(r, 26))
        lucro = num(g(r, 29))
        vendidos.append({
            'codigo': cod,
            'data_venda': iso(g(r, 4)),
            'modelo': g(r, 5),
            'ano': g(r, 6),
            'placa': g(r, 8),
            'data_compra': iso(g(r, 12)),
            'dias_estoque': int(num(g(r, 14))),
            'compra': -num(g(r, 15)),
            'lancamentos': -num(g(r, 20)),
            'comissao': -num(g(r, 23)),
            'custo_total': -num(g(r, 24)),
            'valor_anuncio': num(g(r, 25)),
            'venda': venda,
            'lucro': lucro,
            'margem_pct': round((lucro / venda) * 100, 2) if venda > 0 else 0,
            'cidade': g(r, 34),
        })

# ==== ESTOQUE COM MARGEM ====
rows = read_rows(base + 'Lista Gerencial de Estoque com Margem_05042026.XLS')
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
            'dias_estoque': int(num(g(r, 15))),
            'compra': -num(g(r, 18)),
            'lancamentos_ate_agora': -num(g(r, 22)),
            'valor_anuncio': num(g(r, 25)),
            'fipe_atual': num(g(r, 29)),
            'margem_esperada': num(g(r, 31)),
        })

# ==== ENTRADAS POR FORNECEDOR ====
rows = read_rows(base + 'Lista Gerencial de Entrada de Estoque por Periodo com Fornecedor_05042026.XLS')
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
            'compra': -num(g(r, 20)),
            'fornecedor': g(r, 32),
        })

# ==== LANÇAMENTOS ====
rows = read_rows(base + 'Lista Gerencial de Veiculos com Lancamentos_05042026.XLS')
lancamentos_por_car = {}
cur_cod = None
for r in rows:
    c2 = g(r, 2)
    if c2 and str(c2).isdigit() and len(str(c2)) >= 6:
        cur_cod = c2
        lancamentos_por_car[cur_cod] = []
    elif cur_cod and c2 and c2 != 'Data' and 'T' in str(c2):
        lancamentos_por_car[cur_cod].append({
            'data': iso(c2),
            'descricao': g(r, 3),
            'valor': num(g(r, 30)),
        })

# ==== CONTAS A PAGAR ====
rows = read_rows(base + 'Contas a Pagar_05042026.XLS')
contas_pagar = []
for r in rows:
    v1 = g(r, 1)
    if v1 and 'T' in str(v1):
        contas_pagar.append({
            'vencimento': iso(v1),
            'dre': g(r, 2),
            'fornecedor': g(r, 4),
            'descricao': g(r, 5),
            'valor': num(g(r, 9)),
        })

# Save
all_data = {
    'vendidos': vendidos,
    'estoque_atual': estoque,
    'entradas': entradas,
    'lancamentos_por_carro': lancamentos_por_car,
    'contas_a_pagar': contas_pagar,
}
out = r'C:/Users/Vinicius/Desktop/framework/framework-agentes/framework-agentes/stage-motors/financeiro/_raw_all.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

# ==== ANÁLISES ====
print(f'Vendidos: {len(vendidos)}')
print(f'Estoque atual: {len(estoque)} carros')
print(f'Entradas no período: {len(entradas)}')
print(f'Lançamentos: {sum(len(v) for v in lancamentos_por_car.values())}')
print(f'Contas a pagar: {len(contas_pagar)}')

by_month = defaultdict(lambda: {'n':0,'venda':0,'lucro':0,'dias':[],'lanc':0,'compra':0})
for v in vendidos:
    m = v['data_venda'][:7]
    by_month[m]['n'] += 1
    by_month[m]['venda'] += v['venda']
    by_month[m]['lucro'] += v['lucro']
    by_month[m]['dias'].append(v['dias_estoque'])
    by_month[m]['lanc'] += v['lancamentos']
    by_month[m]['compra'] += v['compra']

print('\n=== Vendas por mes ===')
for m in sorted(by_month):
    d = by_month[m]
    print(f'  {m}: {d["n"]} carros | venda R$ {d["venda"]:>10,.0f} | lucro R$ {d["lucro"]:>8,.0f} | dias_med {sum(d["dias"])/len(d["dias"]):.0f} | lanc/carro R$ {d["lanc"]/d["n"]:,.0f}')

print('\n=== Top 5 maiores lucros ===')
for v in sorted(vendidos, key=lambda x: x['lucro'], reverse=True)[:5]:
    print(f'  R$ {v["lucro"]:>8,.0f} ({v["margem_pct"]:.1f}%) {v["modelo"][:35]} | {v["data_venda"]} | {v["dias_estoque"]}d')

print('\n=== Bottom 5 menores lucros ===')
for v in sorted(vendidos, key=lambda x: x['lucro'])[:5]:
    print(f'  R$ {v["lucro"]:>8,.0f} ({v["margem_pct"]:.1f}%) {v["modelo"][:35]} | {v["data_venda"]} | {v["dias_estoque"]}d | lanc R$ {v["lancamentos"]:,.0f}')

print(f'\n=== Estoque atual: {len(estoque)} carros ===')
print(f'Capital parado: R$ {sum(e["compra"] for e in estoque):,.0f}')
parados = sorted([e for e in estoque if e['dias_estoque'] > 60], key=lambda x: -x['dias_estoque'])
print(f'Com +60 dias: {len(parados)}')
for p in parados[:10]:
    print(f'  {p["dias_estoque"]:>3}d {p["marca"]} {p["modelo"][:30]:30s} | compra R$ {p["compra"]:>8,.0f} | anuncio R$ {p["valor_anuncio"]:>8,.0f}')

print('\n=== Top fornecedores ===')
fornecedores = defaultdict(lambda: {'n':0,'valor':0})
for e in entradas:
    if e['fornecedor']:
        fornecedores[e['fornecedor']]['n'] += 1
        fornecedores[e['fornecedor']]['valor'] += e['compra']
for f, d in sorted(fornecedores.items(), key=lambda x: -x[1]['valor'])[:10]:
    print(f'  {f[:45]:45s} {d["n"]:>2}x R$ {d["valor"]:>10,.0f}')

print(f'\n=== Contas a pagar: {len(contas_pagar)} — R$ {sum(c["valor"] for c in contas_pagar):,.0f} ===')
sim_dre = [c for c in contas_pagar if c['dre'] == 'SIM']
nao_dre = [c for c in contas_pagar if c['dre'] == 'NÃO']
print(f'  DRE=SIM (despesas): {len(sim_dre)} — R$ {sum(c["valor"] for c in sim_dre):,.0f}')
print(f'  DRE=NÃO (compras de estoque): {len(nao_dre)} — R$ {sum(c["valor"] for c in nao_dre):,.0f}')
