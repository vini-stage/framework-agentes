"""
Brandbook Stage Motors — Identidade Visual
Gera um PDF de apresentacao da ID visual pra arquivar/compartilhar.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
    TableStyle, PageBreak, Image as RLImage, NextPageTemplate
)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# ===== PALETA =====
PRETO = HexColor("#000000")
BRANCO = HexColor("#FFFFFF")
GRAFITE = HexColor("#141414")
CINZA_ESCURO = HexColor("#2A2A2A")
CINZA_MEDIO = HexColor("#8A8A8A")
PRATA = HexColor("#C0C0C0")
DOURADO = HexColor("#C9A84C")
DOURADO_CLARO = HexColor("#E6C874")
DOURADO_ESCURO = HexColor("#8A7020")

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO_WHITE = os.path.join(BASE, "logo_white_trim.png")
LOGO_BLACK = os.path.join(BASE, "logo_black_trim.png")
OUTPUT = os.path.join(BASE, "Stage_Motors_Brandbook.pdf")

# ===== FRAME =====
frame_main = Frame(2*cm, 2*cm, A4[0] - 4*cm, A4[1] - 4.5*cm, id='main',
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

# ===== BACKGROUNDS =====
def draw_bg_dark(canvas_obj, doc_):
    page_num = canvas_obj.getPageNumber()
    canvas_obj.saveState()
    canvas_obj.setFillColor(PRETO)
    canvas_obj.rect(0, 0, A4[0], A4[1], fill=True, stroke=False)
    canvas_obj.setStrokeColor(DOURADO)
    canvas_obj.setLineWidth(1.2)
    canvas_obj.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)
    try:
        canvas_obj.drawImage(LOGO_WHITE, A4[0] - 4.5*cm, A4[1] - 1.4*cm,
                             width=2.5*cm, height=0.7*cm,
                             preserveAspectRatio=True, anchor='ne', mask='auto')
    except Exception:
        pass
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.setFillColor(CINZA_MEDIO)
    canvas_obj.drawString(2*cm, 1.2*cm, "BRANDBOOK  //  STAGE MOTORS")
    canvas_obj.setFillColor(DOURADO)
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawRightString(A4[0] - 2*cm, 1.2*cm, f"{page_num:02d}")
    canvas_obj.restoreState()

def draw_bg_light(canvas_obj, doc_):
    page_num = canvas_obj.getPageNumber()
    canvas_obj.saveState()
    canvas_obj.setFillColor(BRANCO)
    canvas_obj.rect(0, 0, A4[0], A4[1], fill=True, stroke=False)
    canvas_obj.setStrokeColor(DOURADO)
    canvas_obj.setLineWidth(1.2)
    canvas_obj.line(2*cm, A4[1] - 1.5*cm, A4[0] - 2*cm, A4[1] - 1.5*cm)
    try:
        canvas_obj.drawImage(LOGO_BLACK, A4[0] - 4.5*cm, A4[1] - 1.4*cm,
                             width=2.5*cm, height=0.7*cm,
                             preserveAspectRatio=True, anchor='ne', mask='auto')
    except Exception:
        pass
    canvas_obj.setFont("Helvetica", 7)
    canvas_obj.setFillColor(HexColor("#4A4A4A"))
    canvas_obj.drawString(2*cm, 1.2*cm, "BRANDBOOK  //  STAGE MOTORS")
    canvas_obj.setFillColor(DOURADO_ESCURO)
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawRightString(A4[0] - 2*cm, 1.2*cm, f"{page_num:02d}")
    canvas_obj.restoreState()

doc = BaseDocTemplate(
    OUTPUT, pagesize=A4,
    topMargin=2.5*cm, bottomMargin=2*cm,
    leftMargin=2*cm, rightMargin=2*cm,
    pageTemplates=[
        PageTemplate(id='dark',  frames=[frame_main], onPage=draw_bg_dark),
        PageTemplate(id='light', frames=[frame_main], onPage=draw_bg_light),
    ]
)

styles = getSampleStyleSheet()

# ===== ESTILOS DARK =====
title_dark = ParagraphStyle('TitleDark', parent=styles['Title'], fontName='Helvetica-Bold',
                            fontSize=36, textColor=BRANCO, spaceAfter=6, alignment=TA_CENTER, leading=40)
subtitle_dark = ParagraphStyle('SubDark', parent=styles['Normal'], fontName='Helvetica',
                               fontSize=12, textColor=DOURADO_CLARO, alignment=TA_CENTER, leading=16)
h1_dark = ParagraphStyle('H1D', parent=styles['Heading1'], fontName='Helvetica-Bold',
                         fontSize=22, textColor=BRANCO, spaceBefore=10, spaceAfter=6, leading=26)
h2_dark = ParagraphStyle('H2D', parent=styles['Heading2'], fontName='Helvetica-Bold',
                         fontSize=13, textColor=DOURADO_CLARO, spaceBefore=12, spaceAfter=6, leading=16)
body_dark = ParagraphStyle('BD', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=10, textColor=BRANCO, leading=14, spaceAfter=4)
caption_dark = ParagraphStyle('CD', parent=styles['Normal'], fontName='Helvetica-Oblique',
                              fontSize=8.5, textColor=PRATA, leading=12, spaceAfter=2)

# ===== ESTILOS LIGHT =====
title_light = ParagraphStyle('TL', parent=styles['Title'], fontName='Helvetica-Bold',
                             fontSize=36, textColor=PRETO, spaceAfter=6, alignment=TA_CENTER, leading=40)
h1_light = ParagraphStyle('H1L', parent=styles['Heading1'], fontName='Helvetica-Bold',
                          fontSize=22, textColor=PRETO, spaceBefore=10, spaceAfter=6, leading=26)
h2_light = ParagraphStyle('H2L', parent=styles['Heading2'], fontName='Helvetica-Bold',
                          fontSize=13, textColor=DOURADO_ESCURO, spaceBefore=12, spaceAfter=6, leading=16)
body_light = ParagraphStyle('BL', parent=styles['Normal'], fontName='Helvetica',
                            fontSize=10, textColor=PRETO, leading=14, spaceAfter=4)
caption_light = ParagraphStyle('CL', parent=styles['Normal'], fontName='Helvetica-Oblique',
                               fontSize=8.5, textColor=HexColor("#4A4A4A"), leading=12, spaceAfter=2)

def hr_gold(width="100%"):
    return HRFlowable(width=width, thickness=1.2, color=DOURADO, spaceBefore=6, spaceAfter=10)

story = []

# ================================================================
# PG 1 — CAPA
# ================================================================
story.append(Spacer(1, 100))
logo_img = RLImage(LOGO_WHITE, width=11*cm, height=3*cm, kind='proportional')
logo_img.hAlign = 'CENTER'
story.append(logo_img)
story.append(Spacer(1, 40))
story.append(Paragraph("BRANDBOOK", title_dark))
story.append(Paragraph("Identidade Visual — Instagram & Comunicação", subtitle_dark))
story.append(Spacer(1, 30))
story.append(HRFlowable(width="30%", thickness=1.5, color=DOURADO, hAlign='CENTER'))
story.append(Spacer(1, 30))
story.append(Paragraph("Versão 1.0  //  Abril 2026",
                       ParagraphStyle('v', parent=body_dark, alignment=TA_CENTER, textColor=PRATA, fontSize=9)))
story.append(NextPageTemplate('dark'))
story.append(PageBreak())

# ================================================================
# PG 2 — ESSÊNCIA DA MARCA
# ================================================================
story.append(Spacer(1, 8))
story.append(Paragraph("ESSÊNCIA DA MARCA", h1_dark))
story.append(hr_gold("20%"))
story.append(Spacer(1, 6))

story.append(Paragraph("POSICIONAMENTO", h2_dark))
story.append(Paragraph(
    "Revenda de seminovos premium em Fortaleza/CE. Atendimento consultivo, "
    "estoque curado, confiança e transparência. Carros que entregam mais "
    "do que o preço sugere.", body_dark))

story.append(Paragraph("PERSONALIDADE", h2_dark))
story.append(Paragraph(
    "&bull;  Direto e sem firula — fala o que precisa, mostra o que tem", body_dark))
story.append(Paragraph(
    "&bull;  Sofisticado mas acessível — premium sem ser arrogante", body_dark))
story.append(Paragraph(
    "&bull;  Automotivo de verdade — entende de carro, não só vende", body_dark))
story.append(Paragraph(
    "&bull;  Minimalista — menos é mais, foco no produto", body_dark))

story.append(Paragraph("TOM DE VOZ", h2_dark))
story.append(Paragraph(
    "Primeira pessoa do singular ou plural informal (eu/a gente). Frases curtas. "
    "Linguagem de quem entende de carro falando pra quem quer entender. "
    "Zero clichê de vendedor. Nunca grita, nunca implora.", body_dark))

story.append(Paragraph("O QUE A GENTE NUNCA FAZ", h2_dark))
story.append(Paragraph("&bull;  Emoji exagerado, caixa alta gritando, promessa vazia", body_dark))
story.append(Paragraph("&bull;  Fundo colorido vibrante, filtros saturados, texto em arco", body_dark))
story.append(Paragraph("&bull;  Mentir sobre revisão, procedência, único dono ou IPVA", body_dark))
story.append(NextPageTemplate('light'))
story.append(PageBreak())

# ================================================================
# PG 3 — LOGO (fundo branco, mostra logo preta)
# ================================================================
story.append(Spacer(1, 8))
story.append(Paragraph("LOGO", h1_light))
story.append(hr_gold("20%"))

story.append(Paragraph("APLICAÇÃO PRIMÁRIA — FUNDO CLARO", h2_light))
story.append(Paragraph(
    "Sobre fundos brancos ou claros, usar a logo em preto puro (#000000) "
    "com fundo transparente. Manter área de respiro mínima equivalente à altura "
    "da palavra MOTORS em todos os lados.", body_light))
story.append(Spacer(1, 10))

logo_preto_display = RLImage(LOGO_BLACK, width=10*cm, height=2.8*cm, kind='proportional')
logo_preto_display.hAlign = 'CENTER'
story.append(logo_preto_display)
story.append(Spacer(1, 14))

story.append(Paragraph("TAMANHO MÍNIMO", h2_light))
story.append(Paragraph(
    "&bull;  Digital: 120 px de largura (legibilidade de STAGE MOTORS)", body_light))
story.append(Paragraph(
    "&bull;  Impresso: 2,5 cm de largura", body_light))

story.append(Paragraph("O QUE NÃO FAZER COM A LOGO", h2_light))
story.append(Paragraph("&bull;  Distorcer, rotacionar, trocar a fonte ou adicionar efeito (sombra, brilho, bevel)", body_light))
story.append(Paragraph("&bull;  Usar sobre imagem com baixo contraste — sempre garantir fundo limpo ou escurecido", body_light))
story.append(Paragraph("&bull;  Mudar as cores fora da paleta oficial (preto, branco ou dourado em casos especiais)", body_light))
story.append(NextPageTemplate('dark'))
story.append(PageBreak())

# ================================================================
# PG 4 — LOGO EM FUNDO ESCURO
# ================================================================
story.append(Spacer(1, 8))
story.append(Paragraph("LOGO  //  FUNDO ESCURO", h1_dark))
story.append(hr_gold("20%"))

story.append(Paragraph("APLICAÇÃO SECUNDÁRIA — FUNDO ESCURO", h2_dark))
story.append(Paragraph(
    "Sobre fundos pretos ou escuros, usar a logo em branco puro (#FFFFFF) "
    "com fundo transparente. É a versão mais usada no Instagram.", body_dark))
story.append(Spacer(1, 14))

logo_branco_display = RLImage(LOGO_WHITE, width=10*cm, height=2.8*cm, kind='proportional')
logo_branco_display.hAlign = 'CENTER'
story.append(logo_branco_display)
story.append(Spacer(1, 18))

story.append(Paragraph("ARQUIVOS FONTE", h2_dark))
story.append(Paragraph("&bull;  <b>logo_white_trim.png</b> — logo branca, fundo transparente (para fundos escuros)", body_dark))
story.append(Paragraph("&bull;  <b>logo_black_trim.png</b> — logo preta, fundo transparente (para fundos claros)", body_dark))
story.append(Paragraph("&bull;  PDF original arquivado na pasta framework", body_dark))
story.append(NextPageTemplate('dark'))
story.append(PageBreak())

# ================================================================
# PG 5 — PALETA DE CORES
# ================================================================
story.append(Spacer(1, 8))
story.append(Paragraph("PALETA DE CORES", h1_dark))
story.append(hr_gold("20%"))

def color_cell(hex_val, nome, uso, text_on_bg="#FFFFFF"):
    label_big = ParagraphStyle('lb', parent=body_dark, fontSize=10, alignment=TA_CENTER,
                               textColor=HexColor(text_on_bg), leading=12)
    label_small = ParagraphStyle('ls', parent=body_dark, fontSize=7.5, alignment=TA_CENTER,
                                 textColor=PRATA, leading=10)
    nome_style = ParagraphStyle('nm', parent=body_dark, fontSize=9, alignment=TA_CENTER,
                                textColor=BRANCO, leading=11, fontName='Helvetica-Bold')
    inner = Table(
        [[Paragraph(f"<b>{hex_val}</b>", label_big)],
         [Paragraph(nome, nome_style)],
         [Paragraph(uso, label_small)]],
        colWidths=[3.2*cm],
        rowHeights=[2.6*cm, 0.55*cm, 0.55*cm]
    )
    bg_color = HexColor(hex_val)
    if hex_val == "#000000":
        border = BRANCO
    elif hex_val == "#FFFFFF":
        border = PRATA
    else:
        border = CINZA_MEDIO
    inner.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), bg_color),
        ('BACKGROUND', (0, 1), (0, -1), GRAFITE),
        ('BOX', (0, 0), (0, 0), 1, border),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
    ]))
    return inner

story.append(Paragraph("CORES PRIMÁRIAS", h2_dark))
primarias = [
    ("#000000", "Preto", "Fundo principal"),
    ("#FFFFFF", "Branco", "Texto e logo"),
    ("#C9A84C", "Dourado", "Acento premium"),
]
row1 = Table([[color_cell(h, n, u) for h, n, u in primarias]], colWidths=[3.5*cm]*3)
row1.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
story.append(row1)
story.append(Spacer(1, 14))

story.append(Paragraph("CORES DE APOIO", h2_dark))
apoio = [
    ("#141414", "Grafite", "Cards, seções"),
    ("#2A2A2A", "Cinza Escuro", "Divisores"),
    ("#8A8A8A", "Cinza Médio", "Texto secundário"),
    ("#C0C0C0", "Prata", "Detalhes metálicos"),
]
row2 = Table([[color_cell(h, n, u) for h, n, u in apoio]], colWidths=[3.5*cm]*4)
row2.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
story.append(row2)
story.append(Spacer(1, 14))

story.append(Paragraph("REGRA 70/25/5", h2_dark))
story.append(Paragraph(
    "&bull;  <b>70%</b>  Preto (#000000) — fundo dominante, respiro, peso visual", body_dark))
story.append(Paragraph(
    "&bull;  <b>25%</b>  Branco (#FFFFFF) — logo, títulos, corpo de texto", body_dark))
story.append(Paragraph(
    "&bull;  <b>5%</b>   Dourado (#C9A84C) — preços, CTAs, linhas de destaque", body_dark))
story.append(NextPageTemplate('light'))
story.append(PageBreak())

# ================================================================
# PG 6 — TIPOGRAFIA
# ================================================================
story.append(Spacer(1, 8))
story.append(Paragraph("TIPOGRAFIA", h1_light))
story.append(hr_gold("20%"))

story.append(Paragraph("FAMÍLIAS OFICIAIS", h2_light))

fontes_data = [
    ["USO", "FAMÍLIA", "PESO", "CARACTERÍSTICA"],
    ["Títulos / Headlines", "Rajdhani  ou  Oswald", "Bold / SemiBold", "Condensada, pegada automotiva"],
    ["Destaques curtos", "Bebas Neue", "Regular", "Alta condensação, impacto"],
    ["Corpo de texto", "Inter  ou  Montserrat", "Regular / Medium", "Leitura limpa, versátil"],
    ["Preços e CTAs", "Rajdhani", "Bold  //  CAPS", "Números fortes, confiança"],
]
ft = Table(fontes_data, colWidths=[4*cm, 4.5*cm, 3*cm, 5.5*cm])
ft.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DOURADO),
    ('TEXTCOLOR', (0, 0), (-1, 0), PRETO),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor("#F7F7F7")),
    ('TEXTCOLOR', (0, 1), (-1, -1), PRETO),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 8.5),
    ('GRID', (0, 0), (-1, -1), 0.4, HexColor("#D0D0D0")),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(ft)
story.append(Spacer(1, 14))

story.append(Paragraph("HIERARQUIA RECOMENDADA", h2_light))
story.append(Paragraph("&bull;  <b>H1 (título principal):</b>  32-40pt,  Rajdhani Bold,  UPPERCASE,  tracking +20", body_light))
story.append(Paragraph("&bull;  <b>H2 (subtítulo):</b>  18-22pt,  Rajdhani SemiBold", body_light))
story.append(Paragraph("&bull;  <b>Preço:</b>  28-36pt,  Rajdhani Bold,  UPPERCASE", body_light))
story.append(Paragraph("&bull;  <b>Corpo:</b>  11-14pt,  Inter Regular,  entrelinha 1.4", body_light))

story.append(Paragraph("LINKS DE DOWNLOAD", h2_light))
story.append(Paragraph("&bull;  Rajdhani — Google Fonts: fonts.google.com/specimen/Rajdhani", body_light))
story.append(Paragraph("&bull;  Oswald — Google Fonts: fonts.google.com/specimen/Oswald", body_light))
story.append(Paragraph("&bull;  Bebas Neue — Google Fonts: fonts.google.com/specimen/Bebas+Neue", body_light))
story.append(Paragraph("&bull;  Inter — Google Fonts: fonts.google.com/specimen/Inter", body_light))
story.append(NextPageTemplate('dark'))
story.append(PageBreak())

# ================================================================
# PG 7 — APLICAÇÕES INSTAGRAM
# ================================================================
story.append(Spacer(1, 8))
story.append(Paragraph("APLICAÇÕES  //  INSTAGRAM", h1_dark))
story.append(hr_gold("20%"))

story.append(Paragraph("FEED", h2_dark))
story.append(Paragraph(
    "&bull;  Fundo preto dominante, foto do carro em alto contraste", body_dark))
story.append(Paragraph(
    "&bull;  Logo branca pequena no canto superior (10-12% da largura)", body_dark))
story.append(Paragraph(
    "&bull;  Texto em Rajdhani Bold, branco puro", body_dark))
story.append(Paragraph(
    "&bull;  Preço e CTA em dourado (#C9A84C) quando usado", body_dark))

story.append(Paragraph("STORIES", h2_dark))
story.append(Paragraph(
    "&bull;  Variação 70% dark / 30% light ao longo do dia (ritmo visual)", body_dark))
story.append(Paragraph(
    "&bull;  Sempre 1 elemento interativo por dia: enquete, quiz, pergunta, slider", body_dark))
story.append(Paragraph(
    "&bull;  Último story do dia com CTA (WhatsApp, DM, link)", body_dark))

story.append(Paragraph("REELS", h2_dark))
story.append(Paragraph(
    "&bull;  Primeiros 3 segundos: frame preto com texto branco condensado (hook)", body_dark))
story.append(Paragraph(
    "&bull;  Transições cortadas no beat do áudio", body_dark))
story.append(Paragraph(
    "&bull;  Encerramento sempre com logo Stage branca + CTA em dourado", body_dark))

story.append(Paragraph("CARDS E ARTES", h2_dark))
story.append(Paragraph(
    "&bull;  Fundo preto puro, sem gradiente vibrante", body_dark))
story.append(Paragraph(
    "&bull;  Moldura: linha dourada de 1-2px ou nenhuma moldura", body_dark))
story.append(Paragraph(
    "&bull;  Foto do carro ocupando 60-70% da arte", body_dark))
story.append(NextPageTemplate('dark'))
story.append(PageBreak())

# ================================================================
# PG 8 — CONTATO / FECHAMENTO
# ================================================================
story.append(Spacer(1, 8))
story.append(Paragraph("CONTATO OFICIAL", h1_dark))
story.append(hr_gold("20%"))
story.append(Spacer(1, 10))

contato_data = [
    ["CANAL", "DADO"],
    ["Instagram", "@stage.motors"],
    ["WhatsApp", "(85) 99934-2715"],
    ["Endereço", "Av. Coronel Miguel Dias, 356 — Guararapes, Fortaleza/CE"],
]
ct = Table(contato_data, colWidths=[4*cm, 12.5*cm])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DOURADO),
    ('TEXTCOLOR', (0, 0), (-1, 0), PRETO),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), GRAFITE),
    ('TEXTCOLOR', (0, 1), (-1, -1), BRANCO),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.4, CINZA_ESCURO),
    ('TOPPADDING', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ('LEFTPADDING', (0, 0), (-1, -1), 12),
]))
story.append(ct)
story.append(Spacer(1, 30))

story.append(Paragraph(
    "Este brandbook é um documento vivo. Sempre que uma nova aplicação "
    "ou regra surgir, atualizar aqui pra manter a consistência da marca.",
    caption_dark))
story.append(Spacer(1, 40))

# Logo final centralizada
logo_final = RLImage(LOGO_WHITE, width=6*cm, height=1.6*cm, kind='proportional')
logo_final.hAlign = 'CENTER'
story.append(logo_final)
story.append(Spacer(1, 8))
story.append(Paragraph("— padrão Stage. sempre. —",
                       ParagraphStyle('end', parent=body_dark, alignment=TA_CENTER,
                                      textColor=DOURADO_CLARO, fontSize=9,
                                      fontName='Helvetica-Oblique')))

# BUILD
doc.build(story)
print(f"PDF gerado: {OUTPUT}")
