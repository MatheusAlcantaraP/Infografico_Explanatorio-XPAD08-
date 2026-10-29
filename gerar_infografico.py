"""Infográfico explanatório - Tema 7 (iniciação científica e tecnológica, UNIFEI).

Gera infografico_iniciacao.png e infografico_iniciacao.pdf nesta pasta.
Todos os números vêm de duas fontes públicas (ver bloco FONTES no rodapé):
  - UFES: Salazar et al., Rev. Bras. Pesq. Saúde 22(4), 2020
  - UFSJ/PROPE: Acompanhamento de egressos do Programa de IC (2015-2023)
"""
import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams["font.family"] = "Arial"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["hatch.linewidth"] = 1.0

# ---------------------------------------------------------------- dados
# UFES (coorte PIIC 2012/13): ingresso em pós-graduação, % do grupo.
# Para quem não fez IC o artigo informa apenas "menos de 10%" (mestrado)
# e "menos de 2%" (doutorado): as barras usam esses limites superiores.
UFES = {
    "labels": ["Bolsistas de IC\n(n = 612)", "Voluntários de IC\n(n = 441)",
               "Sem IC, amostra\n(n = 467)"],
    "mestrado": [47.2, 42.6, 10.0],
    "doutorado": [22.7, 17.7, 2.0],
}

# UFSJ: contagens por resposta, egressos 2020-21 (n=289) e 2022-23 (n=115).
UFSJ_2021 = {"desempenho": 151, "trabalho": 50, "pos": 47, "parte": 31, "nao": 10}
UFSJ_2023 = {"desempenho": 61, "trabalho": 12, "pos": 29, "parte": 9, "nao": 4}
N_UFSJ = 289 + 115
contrib = {k: UFSJ_2021[k] + UFSJ_2023[k] for k in UFSJ_2021}
assert sum(contrib.values()) == N_UFSJ == 404
pct = {k: 100 * v / N_UFSJ for k, v in contrib.items()}
hero = 100 * (contrib["desempenho"] + contrib["trabalho"] + contrib["pos"]) / N_UFSJ

# Competências (contagens somadas dos dois relatórios)
congresso = 100 * (146 + 65) / N_UFSJ
tcc = 100 * (70 + 36) / N_UFSJ
artigo = 100 * (66 + 28) / N_UFSJ

print("hero", round(hero, 1), "| congresso", round(congresso, 1),
      "| tcc", round(tcc, 1), "| artigo", round(artigo, 1))
print({k: round(v, 1) for k, v in pct.items()})


def br(v, nd=1):
    return f"{v:.{nd}f}".replace(".", ",")


# ---------------------------------------------------------------- estilo
SURF, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#706f69"
GRID, BASE, PANEL = "#e1e0d9", "#c3c2b7", "#f1f0ec"
BLUE, BLUE_L = "#2a78d6", "#86b6ef"
NAVY, BLUE_D, BLUE_100 = "#0d366b", "#1c5cab", "#cde2fb"

W, H = 10.0, 26.15
fig = plt.figure(figsize=(W, H), facecolor=SURF)
bg = fig.add_axes([0, 0, 1, 1])
bg.set_xlim(0, W)
bg.set_ylim(H, 0)  # 1 unidade = 1 polegada, y cresce para baixo
bg.axis("off")
CONTENT_SHIFT = 0.0


def T(x, y, s, size=11, color=INK, weight="normal", ha="left", va="top",
      wrap=None, ls=1.3):
    if wrap:
        s = "\n".join(textwrap.fill(p, wrap) for p in s.split("\n"))
    bg.text(x, y - CONTENT_SHIFT, s, fontsize=size, color=color, fontweight=weight, ha=ha,
            va=va, linespacing=ls)
    return y + (s.count("\n") + 1) * size * ls / 72


def add_content_patch(patch):
    if isinstance(patch, Circle):
        x, y = patch.center
        patch.set_center((x, y - CONTENT_SHIFT))
    else:
        patch.set_y(patch.get_y() - CONTENT_SHIFT)
    bg.add_patch(patch)


def AX(x, y, w, h):
    y -= CONTENT_SHIFT
    a = fig.add_axes([x / W, 1 - (y + h) / H, w / W, h / H])
    a.set_facecolor(SURF)
    return a


def badge(x, y, n, color=BLUE):
    add_content_patch(Circle((x, y), 0.2, color=color))
    T(x, y, str(n), size=13, color="white", weight="bold", ha="center",
      va="center")


def style_barh(a, xmax, ticks):
    for s in ("top", "right", "bottom"):
        a.spines[s].set_visible(False)
    a.spines["left"].set_color(BASE)
    a.set_xlim(0, xmax)
    a.set_xticks(ticks)
    a.set_xticklabels([f"{t}%" for t in ticks], fontsize=8.5, color=MUTED)
    a.xaxis.grid(True, color=GRID, linewidth=0.8)
    a.set_axisbelow(True)
    a.tick_params(axis="x", length=0, pad=4)
    a.tick_params(axis="y", length=0, pad=8, labelsize=10, labelcolor=INK)


# ---------------------------------------------------------------- cabeçalho
bg.add_patch(Rectangle((0, 0), W, 2.2, color=NAVY))
y = T(0.6, 0.4,
      "Na UFES, 47% dos bolsistas de IC entraram no mestrado. "
      "Sem IC, menos de 10%.",
      size=23, color="white", weight="bold", wrap=50, ls=1.18)
T(0.6, y + 0.12,
  "Iniciação científica e tecnológica é a porta de entrada para a pesquisa e "
  "a inovação durante a graduação. Na UNIFEI, o primeiro passo é procurar um "
  "orientador.",
  size=14, color=BLUE_100, wrap=80, ls=1.3)

CONTENT_SHIFT = 1.4

# ---------------------------------------------------------------- seção 1
badge(0.8, 4.4, 1)
T(1.15, 4.2, "Quem faz iniciação chega mais à pós-graduação", size=17, weight="bold")
T(1.15, 4.6,
  "Comparação de três grupos de estudantes da UFES, todos da mesma época "
  "(edital 2012/13), acompanhados até 2020 no Currículo Lattes.",
  size=10.5, color=INK2, wrap=100)

ys = [0, 1, 2]
colors = [BLUE, BLUE_L, GRID]
for title, key, ytop, xmax in (("Ingressaram no mestrado", "mestrado", 5.55, 60),
                               ("Ingressaram no doutorado", "doutorado", 8.0, 60)):
    T(0.6, ytop, title, size=12, weight="bold")
    a = AX(2.55, ytop + 0.35, 6.7, 1.55)
    vals = UFES[key]
    bars = a.barh(ys, vals, height=0.46, color=colors, linewidth=0)
    bars[2].set_hatch("////")
    bars[2].set_edgecolor(MUTED)
    bars[2].set_linewidth(0)
    a.set_ylim(2.6, -0.6)
    a.set_yticks(ys)
    a.set_yticklabels(UFES["labels"])
    style_barh(a, xmax, [0, 10, 20, 30, 40, 50])
    for i, v in enumerate(vals):
        if i < 2:
            a.text(v + 1.0, i, f"{br(v)}%", va="center", fontsize=11.5,
                   fontweight="bold", color=INK)
        else:
            lim = "10" if key == "mestrado" else "2"
            a.text(v + 1.0, i, f"menos de {lim}%", va="center", fontsize=10.5,
                   color=INK2)

# aviso de interpretação
add_content_patch(FancyBboxPatch((0.6, 10.4), 8.8, 1.2,
                                 boxstyle="round,pad=0,rounding_size=0.08",
                                 facecolor=PANEL, edgecolor="none"))
T(0.8, 10.53, "Associação, não causa", size=11, weight="bold")
T(0.8, 10.85,
  "O programa da UFES busca estudantes com bom desempenho, e quem ficou sem IC "
  "pode ter feito pesquisa por outros caminhos. Barras hachuradas mostram o "
  "limite superior informado no estudo (“menos de 10%” e “menos de 2%”). "
  "Bolsistas e voluntários têm as mesmas atividades; o que muda é a bolsa.",
  size=9.8, color=INK2, wrap=105, ls=1.3)

# ---------------------------------------------------------------- seção 2
badge(0.8, 12.2, 2)
T(1.15, 12.0, "Quem passou por lá diz que fez diferença", size=17, weight="bold")
T(1.15, 12.4,
  f"Egressos de IC da UFSJ que responderam à pesquisa institucional "
  f"(n = {N_UFSJ}; egressos de 2020–21 e 2022–23).",
  size=10.5, color=INK2, wrap=100)

# Separate the headline metric from the supporting response breakdown.
T(0.6, 13.15, f"{hero:.0f}%", size=68, color=BLUE, weight="bold", ls=1.0)
T(0.6, 14.3,
  "dizem que a IC ajudou no desempenho na graduação, na entrada na pós ou "
  "na admissão no trabalho",
  size=11, color=INK, wrap=30, ls=1.35)

T(3.95, 13.15, "A iniciação contribuiu com…", size=11.5, weight="bold")
a = AX(6.05, 13.5, 3.15, 2.1)
cats = ["Desempenho na\ngraduação", "Entrada na\npós-graduação",
        "Admissão no\ntrabalho", "Contribuiu\nem parte", "Não influenciou\nou sem resposta"]
keys = ["desempenho", "pos", "trabalho", "parte", "nao"]
vals = [pct[k] for k in keys]
cols = [BLUE, BLUE, BLUE, GRID, GRID]
a.barh(range(5), vals, height=0.5, color=cols, linewidth=0)
a.set_ylim(4.6, -0.6)
a.set_yticks(range(5))
a.set_yticklabels(cats)
style_barh(a, 70, [0, 20, 40, 60])
a.tick_params(axis="y", labelsize=9.3, pad=6)
for i, v in enumerate(vals):
    a.text(v + 1.5, i, f"{br(v)}%", va="center", fontsize=10.5,
           fontweight="bold" if i < 3 else "normal",
           color=INK if i < 3 else INK2)
T(3.95, 16.0, "Barras azuis: as três respostas que somam o destaque de "
  f"{hero:.0f}%. Cinza: demais respostas.", size=9, color=MUTED, wrap=75)

tiles = [(f"{congresso:.0f}%", "apresentaram o trabalho de IC em congresso ou evento"),
         (f"{tcc:.0f}%", "fizeram o TCC a partir do trabalho desenvolvido na IC"),
         (f"{artigo:.0f}%", "já publicaram um artigo com resultados da IC")]
add_content_patch(FancyBboxPatch((0.6, 16.65), 8.8, 1.55,
                                 boxstyle="round,pad=0,rounding_size=0.1",
                                 facecolor=PANEL, edgecolor="none"))
T(0.85, 16.78, "Outros resultados entre egressos", size=9.5,
  color=INK2, weight="bold")
tile_width = 8.8 / len(tiles)
for i, (num, lab) in enumerate(tiles):
    center = 0.6 + tile_width * (i + 0.5)
    if i:
        x_divider = 0.6 + tile_width * i
        add_content_patch(Rectangle((x_divider, 17.05), 0.012, 0.95, color=GRID))
    T(center, 16.99, num, size=26, color=BLUE, weight="bold",
      ha="center", ls=1.0)
    T(center, 17.48, lab, size=9.8, color=INK2, wrap=40,
      ha="center", ls=1.25)

T(0.6, 18.4,
  "Respostas autodeclaradas de cerca de 24% dos egressos; percentuais somados "
  "a partir das contagens do relatório da UFSJ (2020–21: n = 289; 2022–23: "
  "n = 115). Artigos de egressos recentes ainda estão em publicação. Só 7 "
  "respondentes (1,7%) eram bolsistas PIBITI: a evidência trata da iniciação "
  "científica em geral, e a vertente tecnológica tem menos dados.",
  size=8.8, color=MUTED, wrap=138, ls=1.3)

# ---------------------------------------------------------------- seção 3 (CTA)
add_content_patch(Rectangle((0, 19.5), W, 5.0, color=BLUE_D))
T(0.6, 19.85, "Seu próximo passo na UNIFEI", size=21, color="white", weight="bold")
T(0.6, 20.4,
  "Iniciação científica ou tecnológica: orientação, prática de pesquisa e "
  "inovação ainda na graduação.",
  size=11.5, color=BLUE_100, wrap=95)
steps = [
    ("Busque projetos da sua área e procure um orientador.",
     "O estudante só entra no programa se for selecionado por um orientador "
     "contemplado em edital da Diretoria de Pesquisa."),
    ("Acompanhe os editais da Diretoria de Pesquisa.",
     "Há bolsas PIBIC e PIBITI do CNPq, PIBIC UNIFEI, PIBIC FAPEMIG e o "
     "programa voluntário PIVIC (editais DIP 003, 005 e 007/2025)."),
    ("Bolsa CNPq: R$ 700 por mês, por 12 meses.*",
     "Valor de editais PIBITI de 2026; confirme no edital vigente da UNIFEI."),
]
for i, (h, b) in enumerate(steps):
    yy = 21.05 + i * 0.88
    add_content_patch(Circle((0.8, yy + 0.2), 0.2, color="white"))
    T(0.8, yy + 0.2, str(i + 1), size=13, color=BLUE_D, weight="bold",
      ha="center", va="center")
    T(1.2, yy, h, size=12.5, color="white", weight="bold")
    T(1.2, yy + 0.27, b, size=10.3, color=BLUE_100, wrap=92)
add_content_patch(Rectangle((0.6, 23.65), 8.8, 0.012, color=BLUE_100))
T(0.6, 23.8, "Procure um orientador e acompanhe os editais.", size=15,
  color="white", weight="bold")
T(9.4, 23.87, "prpi.unifei.edu.br/iniciacao-cientifica", size=10.5,
  color=BLUE_100, ha="right")

# ---------------------------------------------------------------- fontes
T(0.6, 24.95, "Fontes", size=10.5, weight="bold")
fontes = [
    "UFES: Salazar AD et al. Iniciação Científica na Universidade Federal do Espírito "
    "Santo: egressos e evolução. Rev. Bras. Pesq. Saúde 22(4):8–14, 2020. "
    "doi:10.47456/rbps.v22i4.35453.",
    "UFSJ: Pró-reitoria de Pesquisa e Pós-graduação. Acompanhamento de egressos do "
    "Programa de Iniciação Científica (2015–2023), ufsj.edu.br.",
    "UNIFEI: Diretoria de Pesquisa, páginas Iniciação Científica (prpi.unifei.edu.br) e "
    "Editais de Pesquisa (prpg.unifei.edu.br/editais-de-pesquisa), consultadas em 28/10/2026.",
    "*Valor da bolsa PIBITI/CNPq: Edital PROPPGI 07/2026 (UNILAB) e editais 2025/2026 de "
    "outras instituições.",
]
yy = 25.22
for f in fontes:
    yy = T(0.6, yy, "• " + f, size=8.2, color=INK2, wrap=150, ls=1.28) + 0.06

fig.savefig(os.path.join(OUT, "infografico_iniciacao.png"), dpi=200, facecolor=SURF)
fig.savefig(os.path.join(OUT, "infografico_iniciacao.pdf"), facecolor=SURF)
print("fim do conteúdo em y =", round(yy - CONTENT_SHIFT, 2), "de", H)