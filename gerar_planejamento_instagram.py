from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, NextPageTemplate
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus.flowables import HRFlowable
import os

# ===== PALETA MONOCROMATICA (baseada na logo) =====
PRETO = HexColor("#000000")
BRANCO = HexColor("#FFFFFF")
GRAFITE = HexColor("#141414")
CINZA_ESCURO = HexColor("#2A2A2A")
CINZA_MEDIO = HexColor("#8A8A8A")
PRATA = HexColor("#C0C0C0")
DOURADO = HexColor("#C9A84C")        # Cor auxiliar — destaques, preços, CTAs
DOURADO_CLARO = HexColor("#E6C874")  # Versão mais clara para fundos escuros
VERMELHO = HexColor("#E63946")  # Uso muito raro

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO_WHITE = os.path.join(BASE, "logo_white_trim.png")
LOGO_BLACK = os.path.join(BASE, "logo_black_trim.png")

output_path = os.path.join(BASE, "Stage_Motors_Planejamento_Instagram_07-12_Abril.pdf")

# ===== DOC TEMPLATE COM DUAS PAGINAS NOMEADAS (dark / light) =====
# Resolve o bug onde o fundo desalinhava do conteudo quando havia overflow.
# Cada secao usa NextPageTemplate + PageBreak pra trocar o fundo junto com o conteudo.

frame_main = Frame(2*cm, 2*cm, A4[0] - 4*cm, A4[1] - 4.5*cm, id='main',
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

styles = getSampleStyleSheet()

# ===== ESTILOS PARA FUNDO PRETO =====
title_dark = ParagraphStyle('TitleDark', parent=styles['Title'], fontName='Helvetica-Bold',
                            fontSize=32, textColor=BRANCO, spaceAfter=4, alignment=TA_CENTER, leading=36)
subtitle_dark = ParagraphStyle('SubtitleDark', parent=styles['Normal'], fontName='Helvetica',
                               fontSize=11, textColor=DOURADO_CLARO, spaceAfter=16, alignment=TA_CENTER, leading=14)
h1_dark = ParagraphStyle('H1Dark', parent=styles['Heading1'], fontName='Helvetica-Bold',
                         fontSize=18, textColor=BRANCO, spaceBefore=14, spaceAfter=8, leading=22)
h2_dark = ParagraphStyle('H2Dark', parent=styles['Heading2'], fontName='Helvetica-Bold',
                         fontSize=15, textColor=BRANCO, spaceBefore=12, spaceAfter=6, leading=18)
h3_dark = ParagraphStyle('H3Dark', parent=styles['Heading3'], fontName='Helvetica-Bold',
                         fontSize=11, textColor=DOURADO_CLARO, spaceBefore=8, spaceAfter=4, leading=14)
body_dark = ParagraphStyle('BodyDark', parent=styles['Normal'], fontName='Helvetica',
                           fontSize=9.5, textColor=BRANCO, spaceBefore=2, spaceAfter=3, leading=13)
caption_dark = ParagraphStyle('CaptionDark', parent=styles['Normal'], fontName='Helvetica',
                              fontSize=9, textColor=HexColor("#E8E8E8"), spaceBefore=1, spaceAfter=1,
                              leading=12, leftIndent=10)
roteiro_dark = ParagraphStyle('RoteiroDark', parent=styles['Normal'], fontName='Courier',
                              fontSize=8.5, textColor=PRATA, spaceBefore=1, spaceAfter=1, leading=11,
                              leftIndent=12, backColor=GRAFITE)
small_dark = ParagraphStyle('SmallDark', parent=styles['Normal'], fontName='Helvetica-Oblique',
                            fontSize=8, textColor=CINZA_MEDIO, spaceBefore=2, spaceAfter=2)

# ===== ESTILOS PARA FUNDO BRANCO =====
title_light = ParagraphStyle('TitleLight', parent=styles['Title'], fontName='Helvetica-Bold',
                             fontSize=28, textColor=PRETO, spaceAfter=4, alignment=TA_CENTER, leading=32)
h1_light = ParagraphStyle('H1Light', parent=styles['Heading1'], fontName='Helvetica-Bold',
                          fontSize=18, textColor=PRETO, spaceBefore=14, spaceAfter=8, leading=22)
h2_light = ParagraphStyle('H2Light', parent=styles['Heading2'], fontName='Helvetica-Bold',
                          fontSize=15, textColor=PRETO, spaceBefore=12, spaceAfter=6, leading=18)
h3_light = ParagraphStyle('H3Light', parent=styles['Heading3'], fontName='Helvetica-Bold',
                          fontSize=11, textColor=HexColor("#8A7020"), spaceBefore=8, spaceAfter=4, leading=14)
body_light = ParagraphStyle('BodyLight', parent=styles['Normal'], fontName='Helvetica',
                            fontSize=9.5, textColor=PRETO, spaceBefore=2, spaceAfter=3, leading=13)
caption_light = ParagraphStyle('CaptionLight', parent=styles['Normal'], fontName='Helvetica',
                               fontSize=9, textColor=HexColor("#2A2A2A"), spaceBefore=1, spaceAfter=1,
                               leading=12, leftIndent=10)
roteiro_light = ParagraphStyle('RoteiroLight', parent=styles['Normal'], fontName='Courier',
                               fontSize=8.5, textColor=HexColor("#3A3A3A"), spaceBefore=1, spaceAfter=1,
                               leading=11, leftIndent=12, backColor=HexColor("#F0F0F0"))
small_light = ParagraphStyle('SmallLight', parent=styles['Normal'], fontName='Helvetica-Oblique',
                             fontSize=8, textColor=HexColor("#6A6A6A"), spaceBefore=2, spaceAfter=2)

# Mapeamento pagina -> tema (dark/light)
# Capa = dark
# Pag 2 (paleta) = dark
# Dias alternam: Seg dark, Ter light, Qua dark, Qui light, Sex dark, Sab light
# Final = dark
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
    canvas_obj.drawCentredString(A4[0]/2, 1.2*cm,
        "STAGE MOTORS   |   @stage.motors   |   (85) 99934-2715   |   Av. Coronel Miguel Dias, 356 - Guararapes, Fortaleza/CE")
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
    canvas_obj.drawCentredString(A4[0]/2, 1.2*cm,
        "STAGE MOTORS   |   @stage.motors   |   (85) 99934-2715   |   Av. Coronel Miguel Dias, 356 - Guararapes, Fortaleza/CE")
    canvas_obj.setFillColor(HexColor("#8A7020"))
    canvas_obj.setFont("Helvetica-Bold", 8)
    canvas_obj.drawRightString(A4[0] - 2*cm, 1.2*cm, f"{page_num:02d}")
    canvas_obj.restoreState()

doc = BaseDocTemplate(
    output_path,
    pagesize=A4,
    topMargin=2.5*cm,
    bottomMargin=2*cm,
    leftMargin=2*cm,
    rightMargin=2*cm,
    pageTemplates=[
        PageTemplate(id='dark',  frames=[frame_main], onPage=draw_bg_dark),
        PageTemplate(id='light', frames=[frame_main], onPage=draw_bg_light),
    ]
)

def hr_dark():
    return HRFlowable(width="100%", thickness=0.8, color=DOURADO, spaceBefore=6, spaceAfter=6)

def hr_light():
    return HRFlowable(width="100%", thickness=0.8, color=DOURADO, spaceBefore=6, spaceAfter=6)

def reels_block(dia, data, título, roteiro_lines, caption_lines, áudio="", nota="", theme="dark"):
    if theme == "dark":
        h2, h3, body, cap, roteiro, small, hr = h2_dark, h3_dark, body_dark, caption_dark, roteiro_dark, small_dark, hr_dark
    else:
        h2, h3, body, cap, roteiro, small, hr = h2_light, h3_light, body_light, caption_light, roteiro_light, small_light, hr_light

    elements = []
    elements.append(Paragraph(f"{dia} {data}", h2))
    elements.append(Paragraph(f"REELS  //  {título}", h3))
    if nota:
        elements.append(Paragraph(f"{nota}", small))
    elements.append(Spacer(1, 3))
    elements.append(Paragraph("<b>ROTEIRO</b>", body))
    for line in roteiro_lines:
        elements.append(Paragraph(line, roteiro))
    if áudio:
        elements.append(Spacer(1, 2))
        elements.append(Paragraph(f"<b>Áudio:</b> {áudio}", small))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("<b>CAPTION</b>", body))
    for line in caption_lines:
        elements.append(Paragraph(line, cap))
    elements.append(hr())
    return elements

def stories_block(dia, data, stories_list, theme="dark"):
    if theme == "dark":
        h2, h3, body, small, hr = h2_dark, h3_dark, body_dark, small_dark, hr_dark
        cap_color = HexColor("#E8E8E8")
    else:
        h2, h3, body, small, hr = h2_light, h3_light, body_light, small_light, hr_light
        cap_color = HexColor("#2A2A2A")

    cap_style = ParagraphStyle('capstyle', parent=body, textColor=cap_color, leftIndent=10, fontSize=9, leading=12)

    elements = []
    elements.append(Paragraph(f"STORIES  //  {dia} {data}", h3))
    for i, st in enumerate(stories_list, 1):
        tipo = st.get("tipo", "")
        desc = st.get("desc", "")
        texto = st.get("texto", "")
        cta = st.get("cta", "")
        visual = st.get("visual", "")

        elements.append(Paragraph(f"<b>&bull; Story {i}  //  {tipo}</b>", body))
        if desc:
            elements.append(Paragraph(desc, cap_style))
        if texto:
            elements.append(Paragraph(f'<b>Texto na tela:</b> "{texto}"', cap_style))
        if visual:
            elements.append(Paragraph(f"<b>Visual:</b> {visual}", small))
        if cta:
            elements.append(Paragraph(f"<b>CTA:</b> {cta}", small))
        elements.append(Spacer(1, 2))
    elements.append(hr())
    return elements

# ================================
# CONSTRUIR DOCUMENTO
# ================================
story = []

# =========== PAGINA 1 - CAPA ===========
story.append(Spacer(1, 100))
# Logo grande centralizada
logo_img = RLImage(LOGO_WHITE, width=10*cm, height=2.8*cm, kind='proportional')
logo_img.hAlign = 'CENTER'
story.append(logo_img)
story.append(Spacer(1, 40))
story.append(Paragraph("PLANEJAMENTO INSTAGRAM", title_dark))
story.append(Paragraph("Semana de 07 a 12 de Abril de 2026", subtitle_dark))
story.append(Spacer(1, 30))
# Linha divisora
story.append(HRFlowable(width="30%", thickness=1.5, color=DOURADO, hAlign='CENTER'))
story.append(Spacer(1, 30))
story.append(Paragraph("6 REELS  //  30 STORIES  //  36 PEÇAS DE CONTEÚDO",
                       ParagraphStyle('cover', parent=body_dark, fontSize=10, alignment=TA_CENTER, textColor=PRATA)))
story.append(NextPageTemplate("dark"))
story.append(PageBreak())

# =========== PAGINA 2 - RESUMO DA SEMANA ===========
story.append(Spacer(1, 10))
story.append(Paragraph("RESUMO DA SEMANA", h1_dark))
story.append(hr_dark())

resumo_data = [
    ["DIA", "REELS", "STORIES", "CARRO"],
    ["Seg 07/04", "Vitrine Tiggo 8", "5 stories", "Chery Tiggo 8 Founders"],
    ["Ter 08/04", "Educativo: câmbios", "5 stories", "—"],
    ["Qua 09/04", "Bastidores", "5 stories", "Compass + Passat + Tiggo"],
    ["Qui 10/04", "Vitrine Passat", "5 stories", "VW Passat Highline"],
    ["Sex 11/04", "Vitrine Compass", "5 stories", "Jeep Compass"],
    ["Sab 12/04", "Comparativo 3 carros", "5 stories", "Os 3 juntos"],
]
resumo_table = Table(resumo_data, colWidths=[2.5*cm, 5*cm, 2.5*cm, 6.5*cm])
resumo_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DOURADO),
    ('TEXTCOLOR', (0, 0), (-1, 0), PRETO),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 10),
    ('BACKGROUND', (0, 1), (-1, -1), GRAFITE),
    ('TEXTCOLOR', (0, 1), (-1, -1), BRANCO),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.4, CINZA_ESCURO),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
]))
story.append(resumo_table)
story.append(Spacer(1, 20))

# Paleta de cores
story.append(Paragraph("IDENTIDADE VISUAL", h1_dark))
story.append(hr_dark())
story.append(Paragraph("A paleta nasce da logo: monocromática, minimalista, alto contraste. Zero floreio.", body_dark))
story.append(Spacer(1, 10))

# Swatches de cor
def color_cell(hex_val, nome, uso):
    label = ParagraphStyle('sw', parent=body_dark, fontSize=8, textColor=BRANCO, alignment=TA_CENTER, leading=10)
    sub = ParagraphStyle('sw2', parent=label, textColor=PRATA, fontSize=7)
    inner = Table(
        [[""], [Paragraph(f"<b>{hex_val}</b>", label)], [Paragraph(nome, label)], [Paragraph(uso, sub)]],
        colWidths=[3*cm],
        rowHeights=[1.5*cm, 0.45*cm, 0.4*cm, 0.4*cm]
    )
    bg_color = HexColor(hex_val)
    # Se for preto puro, usar borda branca. Se for branco, borda cinza
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
        ('TOPPADDING', (0, 1), (-1, -1), 2),
    ]))
    return inner

cores = [
    ("#000000", "Preto", "Fundo"),
    ("#FFFFFF", "Branco", "Texto"),
    ("#141414", "Grafite", "Cards"),
    ("#C0C0C0", "Prata", "Detalhes"),
    ("#C9A84C", "Dourado", "Acento"),
]
palette_row = Table([[color_cell(h, n, u) for h, n, u in cores]], colWidths=[3.2*cm]*5)
palette_row.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
story.append(palette_row)
story.append(Spacer(1, 12))
story.append(Paragraph(
    "<b>Tipografia:</b>  Rajdhani Bold / Oswald Bold (títulos - condensada, pegada automotiva)   //   Inter Regular / Montserrat (corpo)   //   CAPS + Extra Bold para preços e CTAs",
    small_dark))
story.append(NextPageTemplate("dark"))
story.append(PageBreak())

# =========== PAGINA 3 - SEGUNDA (DARK) ===========
story.append(Spacer(1, 10))
story.extend(reels_block(
    "SEGUNDA", "07/04",
    "Vitrine - Chery Tiggo 8 Founders Edition",
    [
        "[0-3s] Carro de frente, câmera subindo lentamente",
        '        Texto: "CHERY TIGGO 8 FOUNDERS EDITION" (branco, condensada)',
        "[3-8s] Volta ao redor do carro (traseira, lateral)",
        '        Texto: "Versão especial de lançamento"',
        "[8-15s] Interior: central 12.3\", câmera 360, teto solar abrindo",
        '        Texto: "Central 12.3\" | Câmera 360 | Teto panorâmico"',
        "[15-20s] Banco traseiro (7 lugares), detalhe do câmbio",
        '         Texto: "R$ 137.900 | Financiamos | Aceitamos troca"',
        "[20-25s] Logo Stage Motors branca + fade out",
    ],
    [
        "Chery Tiggo 8 Founders Edition 2023 disponível na Stage Motors.",
        "",
        "&bull; Motor 1.6 turbo 187 cv, câmbio DCT de dupla embreagem",
        "&bull; Teto solar panorâmico, câmera 360, central 12.3\"",
        "&bull; 7 lugares, alerta de ponto cego, frenagem automática",
        "&bull; R$ 137.900 — financiamos e aceitamos troca",
        "",
        "Esse SUV entrega mais que muito carro de marca premium.",
        "",
        "WhatsApp: (85) 99934-2715",
        "Av. Coronel Miguel Dias, 356 — Guararapes",
    ],
    áudio="Instrumental trending, ritmo medio — imponente mas não esportivo",
    theme="dark"
))
story.extend(stories_block("SEGUNDA", "07/04", [
    {"tipo": "Bom dia + Carro do dia",
     "desc": "Foto da Tiggo 8 no pátio com luz natural da manhã.",
     "texto": "Bom dia. Olha quem tá esperando você na Stage.",
     "visual": "Fundo preto, texto branco condensado, logo no canto",
     "cta": ""},
    {"tipo": "Enquete - Interação",
     "desc": "Close no teto solar panorâmico da Tiggo 8 abrindo.",
     "texto": "Teto solar: essencial ou dispensável?",
     "visual": "Enquete com 2 opções: 'Não vivo sem' / 'Tanto faz'",
     "cta": "Enquete interativa"},
    {"tipo": "Detalhe do carro",
     "desc": "Vídeo curto mostrando a central 12.3\" e a câmera 360.",
     "texto": "Central 12.3\" + Câmera 360 graus",
     "visual": "Texto branco sobre foto escurecida, logo pequena",
     "cta": ""},
    {"tipo": "Preço + Condições",
     "desc": "Foto da Tiggo 8 de frente, angulo baixo.",
     "texto": "R$ 137.900  |  Financiamos  |  Aceitamos troca",
     "visual": "Preço grande em branco, dados em prata menor",
     "cta": "Arrasta pra cima / Link WhatsApp"},
    {"tipo": "CTA Final",
     "desc": "Foto do interior com bancos em couro.",
     "texto": "Quer conhecer de perto? Chama no WhatsApp.",
     "visual": "Link clicável com botão branco sobre fundo escuro",
     "cta": "Link direto: (85) 99934-2715"},
], theme="dark"))
story.append(NextPageTemplate("light"))
story.append(PageBreak())

# =========== PAGINA 4 - TERÇA (LIGHT) ===========
story.append(Spacer(1, 10))
story.extend(reels_block(
    "TERÇA", "08/04",
    "Educativo - CVT vs DCT vs Torque Converter",
    [
        "[0-3s] Você na câmera ou texto: \"Você sabe a diferença entre esses 3 câmbios?\"",
        "[3-10s] \"CVT — sem marchas fixas, econômico, suave\" + b-roll de câmbio CVT",
        "[10-17s] \"DCT — dupla embreagem, trocas rápidas\" + close do câmbio da Tiggo 8",
        "[17-24s] \"Tiptronic — conversor de torque, confortável\" + close do câmbio do Passat",
        "[24-30s] \"Qual você prefere? Comenta aqui\" + Logo Stage",
    ],
    [
        "Câmbio automático não e tudo igual. Sabia disso?",
        "",
        "&bull; CVT — sem marchas fixas, prioriza economia",
        "&bull; DCT — dupla embreagem, trocas rápidas e precisas",
        "&bull; Tiptronic — conversor de torque, o mais confortável",
        "",
        "Aqui na Stage Motors a gente explica tudo antes de você decidir.",
        "Qual desses você prefere? Comenta aqui!",
        "",
        "WhatsApp: (85) 99934-2715",
        "Av. Coronel Miguel Dias, 356 — Guararapes",
    ],
    áudio="Áudio educativo, ritmo leve e moderno",
    nota="Conecta com o estoque: Tiggo 8 (DCT), Passat (Tiptronic)",
    theme="light"
))
story.extend(stories_block("TERÇA", "08/04", [
    {"tipo": "Bom dia + Teaser do Reels",
     "desc": "Print ou frame do Reels educativo de hoje.",
     "texto": "Você sabe a diferença entre CVT, DCT e Tiptronic?",
     "visual": "Fundo claro, texto preto condensado, ícone de play",
     "cta": "Fica ligado no Reels de hoje!"},
    {"tipo": "Dica rápida #1",
     "desc": "Card visual simples.",
     "texto": "CVT = sem marchas fixas, economia no dia a dia",
     "visual": "Card branco com texto preto + detalhe prata",
     "cta": ""},
    {"tipo": "Dica rápida #2",
     "desc": "Card visual simples.",
     "texto": "DCT = dupla embreagem, troca rápida, mais esportivo",
     "visual": "Card branco com texto preto + detalhe prata",
     "cta": ""},
    {"tipo": "Dica rápida #3",
     "desc": "Card visual simples.",
     "texto": "Tiptronic = conversor de torque, conforto puro",
     "visual": "Card branco com texto preto + detalhe prata",
     "cta": ""},
    {"tipo": "Quiz interativo",
     "desc": "Foto do câmbio da Tiggo 8.",
     "texto": "E aí, qual câmbio e esse?",
     "visual": "Quiz com 3 opções: CVT / DCT / Tiptronic",
     "cta": "Quiz do Instagram"},
], theme="light"))
story.append(NextPageTemplate("dark"))
story.append(PageBreak())

# =========== PAGINA 5 - QUARTA (DARK) ===========
story.append(Spacer(1, 10))
story.extend(reels_block(
    "QUARTA", "09/04",
    "Bastidores - O que chegou essa semana",
    [
        "[0-3s] Você andando pelo pátio, câmera na mão",
        '        Texto: "O que chegou na Stage essa semana"',
        "[3-8s] Mostra a Compass chegando/estacionada",
        '        Texto: "Jeep Compass — chegando fresquinha"',
        "[8-13s] Corta pro Passat no pátio",
        '         Texto: "Passat Highline 2.0 TSI 220cv"',
        "[13-18s] Mostra a Tiggo 8",
        '          Texto: "Tiggo 8 Founders Edition"',
        "[18-25s] Você de frente: \"Qual desses quer ver em detalhe?\" + Logo",
    ],
    [
        "Olha o que tá rolando no pátio da Stage essa semana.",
        "",
        "Jeep Compass novinha chegando, Passat Highline 220cv",
        "e Tiggo 8 Founders Edition esperando por você.",
        "",
        "Qual desses merece um vídeo só dele? Comenta aqui!",
        "",
        "WhatsApp: (85) 99934-2715",
        "Av. Coronel Miguel Dias, 356 — Guararapes",
    ],
    áudio="Música energética, vibe de bastidores",
    nota="Serve como 'pesquisa' — o mais comentado vira destaque",
    theme="dark"
))
story.extend(stories_block("QUARTA", "09/04", [
    {"tipo": "Bom dia + Bastidores",
     "desc": "Vídeo curto do pátio de manhã, carros sendo organizados.",
     "texto": "Bom dia direto do pátio da Stage.",
     "visual": "Vídeo natural, autêntico, sem edição pesada",
     "cta": ""},
    {"tipo": "Carro chegando",
     "desc": "Vídeo ou foto da Compass chegando na loja.",
     "texto": "Olha quem acabou de chegar...",
     "visual": "Suspense — não mostra o carro inteiro ainda",
     "cta": "Chuta qual carro é!"},
    {"tipo": "Reveal da Compass",
     "desc": "Foto ou vídeo mostrando a Compass completa.",
     "texto": "Jeep Compass nova no estoque.",
     "visual": "Foto com moldura branca fina, logo no canto",
     "cta": "Quer saber mais? Responde esse story!"},
    {"tipo": "Preparação do carro",
     "desc": "Vídeo da lavagem/polimento de um dos carros.",
     "texto": "Preparando tudo pra ficar no padrao Stage.",
     "visual": "Vídeo real, bastidores da preparação",
     "cta": ""},
    {"tipo": "Contagem de estoque",
     "desc": "Panoramica do pátio mostrando os carros.",
     "texto": "Quantos carros você consegue contar?",
     "visual": "Enquete com opções numéricas",
     "cta": "Enquete: 10-15 / 15-20 / 20-30 / 30+"},
], theme="dark"))
story.append(NextPageTemplate("light"))
story.append(PageBreak())

# =========== PAGINA 6 - QUINTA (LIGHT) ===========
story.append(Spacer(1, 10))
story.extend(reels_block(
    "QUINTA", "10/04",
    "Vitrine - VW Passat Highline 2.0 TSI 220cv",
    [
        "[0-3s] Close nos faróis acendendo (fundo escuro)",
        '        Texto: "VOLKSWAGEN PASSAT HIGHLINE"',
        "[3-8s] Câmera deslizando pela lateral do sedan",
        '        Texto: "2.0 TSI | 220 cv | Tiptronic"',
        "[8-15s] Interior: painel, couro, Climatronic, teto solar",
        '         Texto: "Teto solar | Couro | ACC | Park Assist"',
        "[15-22s] Detalhe do motor, rodas, acabamento",
        '          Texto: "Sedan premium alemão, feito pra quem entende"',
        "[22-28s] Angulo traseiro, câmera afastando",
        '          Texto: "R$ 134.900 | Financiamos | Aceitamos troca"',
    ],
    [
        "Volkswagen Passat Highline 2.0 TSI 220cv — sedan alemão com presenca.",
        "",
        "&bull; Motor 2.0 TSI 220 cv, câmbio Tiptronic",
        "&bull; Teto solar panorâmico, bancos em couro, ACC",
        "&bull; Park Assist, Climatronic 3 zonas, 8 airbags",
        "&bull; R$ 134.900 — financiamos e aceitamos troca",
        "",
        "Quem dirige um Passat não volta atrás.",
        "",
        "WhatsApp: (85) 99934-2715",
        "Av. Coronel Miguel Dias, 356 — Guararapes",
    ],
    áudio="Instrumental sofisticado, ritmo lento — perfil premium",
    theme="light"
))
story.extend(stories_block("QUINTA", "10/04", [
    {"tipo": "Bom dia + Carro do dia",
     "desc": "Foto do Passat de frente com luz natural.",
     "texto": "Sedan alemão no pátio da Stage hoje.",
     "visual": "Foto com filtro leve, texto preto condensado",
     "cta": ""},
    {"tipo": "Detalhe interno",
     "desc": "Vídeo curto do interior: painel, couro, teto solar.",
     "texto": "Esse acabamento é outro nível.",
     "visual": "Close nos detalhes premium",
     "cta": ""},
    {"tipo": "Dado tecnico",
     "desc": "Card visual com specs.",
     "texto": "2.0 TSI  |  220 cv  |  Tiptronic  |  Park Assist  |  ACC",
     "visual": "Card branco com ícones e texto preto",
     "cta": ""},
    {"tipo": "Enquete de engajamento",
     "desc": "Foto do Passat vs outro sedan do estoque.",
     "texto": "Passat Highline ou [outro]: qual você levaria?",
     "visual": "Foto dividida ao meio, enquete 2 opções",
     "cta": "Enquete interativa"},
    {"tipo": "Preço + CTA",
     "desc": "Foto do Passat angulo traseiro, elegante.",
     "texto": "R$ 134.900  |  Chama no WhatsApp",
     "visual": "Preço grande em preto + botão de link",
     "cta": "Link direto pro WhatsApp"},
], theme="light"))
story.append(NextPageTemplate("dark"))
story.append(PageBreak())

# =========== PAGINA 7 - SEXTA (DARK) ===========
story.append(Spacer(1, 10))
story.extend(reels_block(
    "SEXTA", "11/04",
    "Vitrine - Jeep Compass",
    [
        "[0-3s] Compass de frente, angulo baixo (imponência)",
        '        Texto: "JEEP COMPASS"',
        "[3-8s] Lateral e traseira",
        "        Texto: versão + motorização (completar quando tiver dados)",
        "[8-15s] Interior: central, bancos, teto solar (se tiver)",
        "         Texto: 2-3 opcionais destaque",
        "[15-20s] Detalhe da tração 4x4 ou seletor de terreno",
        '          Texto: "R$ [preço] | Financiamos"',
        "[20-25s] Logo Stage Motors",
    ],
    [
        "Jeep Compass [versão] [ano] disponível na Stage Motors.",
        "",
        "&bull; [Destaque 1]",
        "&bull; [Destaque 2]",
        "&bull; [Destaque 3]",
        "&bull; R$ [preço] — financiamos e aceitamos troca",
        "",
        "WhatsApp: (85) 99934-2715",
        "Av. Coronel Miguel Dias, 356 — Guararapes",
        "",
        "(Completar caption quando tiver os dados da Compass)",
    ],
    nota="Completar roteiro e caption quando a Compass chegar",
    theme="dark"
))
story.extend(stories_block("SEXTA", "11/04", [
    {"tipo": "Bom dia + Sextou",
     "desc": "Vídeo do pátio com música animada.",
     "texto": "Sextou na Stage Motors. Bora fechar negócio?",
     "visual": "Vídeo curto, vibe energética",
     "cta": ""},
    {"tipo": "Compass em destaque",
     "desc": "Foto ou vídeo da Compass já preparada.",
     "texto": "Jeep Compass pronta e esperando dono.",
     "visual": "Foto com moldura branca fina",
     "cta": ""},
    {"tipo": "Interior da Compass",
     "desc": "Vídeo mostrando interior e opcionais.",
     "texto": "Olha esse interior...",
     "visual": "Close nos detalhes que mais impressionam",
     "cta": ""},
    {"tipo": "Caixa de perguntas",
     "desc": "Fundo preto com logo Stage branca.",
     "texto": "Pergunta sobre carros? Manda aqui.",
     "visual": "Caixa de perguntas do Instagram",
     "cta": "Caixa de perguntas — gera DMs"},
    {"tipo": "Resposta a perguntas + CTA",
     "desc": "Responder 1-2 perguntas que chegaram.",
     "texto": "Respondendo vocês (+ preço/condições da Compass)",
     "visual": "Texto sobre fundo preto, preço em branco",
     "cta": "Link WhatsApp"},
], theme="dark"))
story.append(NextPageTemplate("light"))
story.append(PageBreak())

# =========== PAGINA 8 - SÁBADO (LIGHT) ===========
story.append(Spacer(1, 10))
story.extend(reels_block(
    "SÁBADO", "12/04",
    "Comparativo - 3 carros disponíveis",
    [
        "[0-3s] Texto: \"3 carros disponíveis na Stage Motors\"",
        "[3-10s] Tiggo 8 — 2-3 takes rapidos",
        '         Texto: "Chery Tiggo 8 Founders | 7 lugares | R$ 137.900"',
        "[10-17s] Compass — 2-3 takes",
        '          Texto: "Jeep Compass [versão] | R$ [preço]"',
        "[17-24s] Passat — 2-3 takes",
        '          Texto: "Passat Highline 220cv | R$ 134.900"',
        "[24-30s] \"Qual você levaria? Comenta 1, 2 ou 3!\" + Logo",
    ],
    [
        "Qual desses você levaria? Comenta 1, 2 ou 3!",
        "",
        "1 — Chery Tiggo 8 Founders Edition — 7 lugares, câmera 360, R$ 137.900",
        "2 — Jeep Compass [versão] — [destaque], R$ [preço]",
        "3 — VW Passat Highline 220cv — sedan premium alemão, R$ 134.900",
        "",
        "Todos disponíveis pra financiamento e aceitamos troca.",
        "",
        "WhatsApp: (85) 99934-2715",
        "Av. Coronel Miguel Dias, 356 — Guararapes",
    ],
    áudio="Áudio trending, energetico — gera engajamento",
    nota="Reels comparativo gera muito comentário — impulsiona alcance",
    theme="light"
))
story.extend(stories_block("SÁBADO", "12/04", [
    {"tipo": "Bom dia + Sabadão",
     "desc": "Vídeo do pátio, movimento de sábado.",
     "texto": "Sabadão e dia de visita. A Stage tá aberta.",
     "visual": "Vídeo natural, clima de movimento",
     "cta": ""},
    {"tipo": "Comparativo visual",
     "desc": "Foto dos 3 carros lado a lado.",
     "texto": "1, 2 ou 3?",
     "visual": "Numeracao grande e bold sobre cada carro",
     "cta": "Enquete: 1 / 2 / 3"},
    {"tipo": "Detalhe Tiggo 8",
     "desc": "1 foto/vídeo rápido de destaque.",
     "texto": "Opção 1: Chery Tiggo 8  |  7 lugares  |  R$ 137.900",
     "visual": "Card com foto + dados condensados",
     "cta": ""},
    {"tipo": "Detalhe Compass",
     "desc": "1 foto/vídeo rápido de destaque.",
     "texto": "Opção 2: Jeep Compass  |  [destaque]  |  R$ [preço]",
     "visual": "Card com foto + dados condensados",
     "cta": ""},
    {"tipo": "Detalhe Passat + CTA final",
     "desc": "1 foto/vídeo rápido + CTA de fechamento.",
     "texto": "Opção 3: Passat Highline 220cv  |  R$ 134.900",
     "visual": "Card + botão WhatsApp destacado",
     "cta": "Já escolheu? Chama no WhatsApp!"},
], theme="light"))
story.append(NextPageTemplate("dark"))
story.append(PageBreak())

# =========== PAGINA 9 - ESTRATÉGIA (DARK) ===========
story.append(Spacer(1, 10))
story.append(Paragraph("ESTRATÉGIA E DICAS", h1_dark))
story.append(hr_dark())

story.append(Paragraph("<b>HORÁRIOS IDEAIS EM FORTALEZA</b>", h3_dark))
story.append(Paragraph("&bull;  Reels: 11h-13h  ou  18h-20h", body_dark))
story.append(Paragraph("&bull;  Stories: distribuir ao longo do dia (manhã, almoço, tarde, noite)", body_dark))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>REGRAS DE OURO DOS STORIES</b>", h3_dark))
dicas_stories = [
    "&bull;  1. Poste o primeiro story até as 9h — ativa o algoritmo pro dia todo",
    "&bull;  2. Use pelo menos 1 elemento interativo por dia (enquete, quiz, pergunta, slider)",
    "&bull;  3. Misture fotos, vídeos e cards — variedade mantem atenção",
    "&bull;  4. Último story do dia sempre com CTA (WhatsApp, DM, link)",
    "&bull;  5. Responda toda DM que vier dos stories em até 1h",
    "&bull;  6. Reposte nos stories quando publicar um Reels novo",
]
for d in dicas_stories:
    story.append(Paragraph(d, body_dark))
story.append(Spacer(1, 10))

story.append(Paragraph("<b>DESTAQUES FIXOS SUGERIDOS (BOLINHAS DO PERFIL)</b>", h3_dark))
destaques = [
    "&bull;  Estoque — stories dos carros disponíveis (atualizar semanalmente)",
    "&bull;  Financiamento — como funciona, simulação, dicas",
    "&bull;  Entregas — prova social, clientes recebendo o carro",
    "&bull;  Sobre nos — quem e a Stage, valores, equipe",
    "&bull;  Dicas — conteúdo educativo salvo",
]
for d in destaques:
    story.append(Paragraph(d, body_dark))
story.append(Spacer(1, 12))

story.append(Paragraph("<b>METAS DA SEMANA</b>", h3_dark))
metas_data = [
    ["MÉTRICA", "META"],
    ["Reels publicados", "6"],
    ["Stories publicados", "30 (5/dia)"],
    ["Alcance de Reels", "+20% vs semana anterior"],
    ["DMs recebidos", "Responder em até 1h"],
    ["Comentários respondidos", "100% em até 1h"],
]
metas_table = Table(metas_data, colWidths=[6*cm, 7*cm])
metas_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DOURADO),
    ('TEXTCOLOR', (0, 0), (-1, 0), PRETO),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('BACKGROUND', (0, 1), (-1, -1), GRAFITE),
    ('TEXTCOLOR', (0, 1), (-1, -1), BRANCO),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('GRID', (0, 0), (-1, -1), 0.4, CINZA_ESCURO),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
]))
story.append(metas_table)

# BUILD
doc.build(story)
print(f"PDF gerado: {output_path}")
