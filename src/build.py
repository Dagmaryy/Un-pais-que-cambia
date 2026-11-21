# -*- coding: utf-8 -*-
"""Genera las 5 historias con datos en PDF separados (2 cuartillas c/u)."""
import os
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from fpdf import FPDF

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "pdf")
IMG = os.path.join(BASE, "img")
os.makedirs(OUT, exist_ok=True)
os.makedirs(IMG, exist_ok=True)

FD = "/usr/share/fonts/truetype/dejavu"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": "#333333",
    "axes.edgecolor": "#999999",
    "axes.labelcolor": "#333333",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
})

def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ---------------------------------------------------------------- charts
def fmt_label(fmt, v):
    return fmt(v) if callable(fmt) else fmt.format(v)

def chart_bars(fname, labels, values, colors, ylabel, fmt="{:g}", ylim=None, horiz=False, size=(7.4, 2.85)):
    fig, ax = plt.subplots(figsize=size)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    if horiz:
        bars = ax.barh(labels[::-1], values[::-1], color=colors[::-1], height=0.58, zorder=3)
        ax.set_xlabel(ylabel, fontsize=9.5)
        ax.grid(axis="x", color="#cccccc", lw=0.6, zorder=0)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=10.5, length=0)
        for b, v in zip(bars, values[::-1]):
            ax.text(v + max(values) * 0.02, b.get_y() + b.get_height() / 2,
                    fmt_label(fmt, v), va="center", ha="left", fontsize=11.5, fontweight="bold")
        ax.set_xlim(0, max(values) * 1.18)
    else:
        bars = ax.bar(labels, values, color=colors, width=0.55, zorder=3)
        ax.set_ylabel(ylabel, fontsize=9.5)
        ax.grid(axis="y", color="#cccccc", lw=0.6, zorder=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        ax.tick_params(labelsize=10.5, length=0)
        top = ylim or max(values) * 1.22
        ax.set_ylim(0, top)
        for b, v in zip(bars, values):
            ax.text(b.get_x() + b.get_width() / 2, v + top * 0.03,
                    fmt_label(fmt, v), ha="center", va="bottom", fontsize=12, fontweight="bold")
    fig.tight_layout(pad=0.4)
    path = os.path.join(IMG, fname)
    fig.savefig(path, dpi=210, transparent=True)
    plt.close(fig)
    return path

def chart_slope(fname, years, values, color, ylabel, size=(5.2, 2.6)):
    fig, ax = plt.subplots(figsize=size)
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    ax.plot(years, values, color=color, lw=2.6, marker="o", markersize=7, zorder=3)
    ax.set_ylabel(ylabel, fontsize=9.5)
    ax.grid(axis="y", color="#cccccc", lw=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xticks(years)
    ax.tick_params(labelsize=10.5, length=0)
    lo, hi = min(values), max(values)
    ax.set_ylim(lo - (hi - lo) * 0.55, hi + (hi - lo) * 0.75)
    for x, v in zip(years, values):
        ax.annotate(f"{v:g} %".replace(".", ","), (x, v), textcoords="offset points",
                    xytext=(0, 10), ha="center", fontsize=12, fontweight="bold")
    fig.tight_layout(pad=0.4)
    path = os.path.join(IMG, fname)
    fig.savefig(path, dpi=210, transparent=True)
    plt.close(fig)
    return path

def _save(fig, fname):
    fig.tight_layout(pad=0.4)
    path = os.path.join(IMG, fname)
    fig.savefig(path, dpi=210, transparent=True)
    plt.close(fig)
    return path

def chart_step(fname, labels, values, color, ylabel, fill="#B9D2EA"):
    fig, ax = plt.subplots(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    x = list(range(len(values)))
    ax.step(x, values, where="mid", color=color, lw=2.8, zorder=3)
    ax.fill_between(x, values, step="mid", color=fill, zorder=2)
    ax.plot(x, values, "o", color=color, markersize=8, zorder=4)
    for xi, v in zip(x, values):
        ax.annotate(f"{v:g} %".replace(".", ","), (xi, v), textcoords="offset points",
                    xytext=(0, 11), ha="center", fontsize=12.5, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel, fontsize=9.5)
    ax.set_ylim(0, max(values) * 1.28)
    ax.set_xlim(-0.55, len(values) - 0.45)
    ax.grid(axis="y", color="#cccccc", lw=0.6, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10.5, length=0)
    return _save(fig, fname)

def chart_lollipop(fname, labels, values, colors, ylabel):
    fig, ax = plt.subplots(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    x = list(range(len(values)))
    for xi, v, c in zip(x, values, colors):
        ax.plot([xi, xi], [0, v], color=c, lw=3.2, zorder=2, solid_capstyle="round")
        ax.plot([xi], [v], "o", color=c, markersize=13, zorder=3)
        ax.annotate(f"{v:g} %".replace(".", ","), (xi, v), textcoords="offset points",
                    xytext=(0, 13), ha="center", fontsize=12.5, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylabel(ylabel, fontsize=9.5)
    ax.set_ylim(0, max(values) * 1.3)
    ax.grid(axis="y", color="#cccccc", lw=0.6, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10.5, length=0)
    return _save(fig, fname)

def chart_area(fname, years, values, color, ylabel, fmt, highlight_last=None, note=None):
    fig, ax = plt.subplots(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    x = list(range(len(values)))
    ax.plot(x, values, color=color, lw=2.6, marker="o", markersize=6.5, zorder=4)
    ax.fill_between(x, values, color=color, alpha=0.18, zorder=2)
    for xi, v in zip(x, values):
        ax.annotate(fmt(v), (xi, v), textcoords="offset points", xytext=(0, 10),
                    ha="center", fontsize=12, fontweight="bold")
    if highlight_last is not None:
        ax.plot([x[-1]], [values[-1]], "o", color=highlight_last, markersize=10, zorder=5)
    if note:
        ax.annotate(note, (x[-2], values[-2]), textcoords="offset points", xytext=(-52, 22),
                    ha="center", fontsize=9.5, style="italic", color="#555555")
    ax.set_xticks(x); ax.set_xticklabels([str(y) for y in years])
    ax.set_ylabel(ylabel, fontsize=9.5)
    lo, hi = min(values), max(values)
    ax.set_ylim(lo - (hi - lo) * 0.55, hi + (hi - lo) * 0.6)
    ax.grid(axis="y", color="#cccccc", lw=0.6, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10.5, length=0)
    return _save(fig, fname)

def chart_waterfall(fname, colors):
    # millones: inicio 2023, +nacimientos, -defunciones, -saldo migratorio, fin 2024
    labels = ["2023", "Nacimientos", "Defunciones", "Saldo\nmigratorio", "2024"]
    totals = [10.055968, None, None, None, 9.748007]
    deltas = [None, 0.071358, -0.128098, -0.251221, None]
    texts = ["10.055.968", "+71.358", "-128.098", "-251.221", "9.748.007"]
    fig, ax = plt.subplots(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    cum = totals[0]
    bottoms, heights = [], []
    seq = [totals[0]]
    for d in deltas[1:4]:
        seq.append(seq[-1] + d)
    bottoms = [0, seq[0], seq[2], seq[3], 0]
    heights = [totals[0], deltas[1], -deltas[2], -deltas[3], totals[4]]
    bottoms[2] = seq[2]; bottoms[3] = seq[3]
    bottoms[1] = seq[0]
    heights[2] = -deltas[2]; heights[3] = -deltas[3]
    for i in range(5):
        ax.bar([i], [heights[i]], bottom=[bottoms[i]], color=colors[i], width=0.58, zorder=3)
        top = bottoms[i] + heights[i]
        ax.annotate(texts[i], (i, top), textcoords="offset points", xytext=(0, 5),
                    ha="center", fontsize=11, fontweight="bold")
    for i in range(4):
        y = seq[i] if i == 0 else seq[i]
        ax.plot([i + 0.29, i + 1 - 0.29], [seq[i], seq[i]], color="#999999", lw=1, ls=(0, (3, 2)), zorder=2)
    ax.set_xticks(range(5)); ax.set_xticklabels(labels)
    ax.set_ylabel("Millones de habitantes", fontsize=9.5)
    ax.set_ylim(9.3, 10.32)
    ax.grid(axis="y", color="#cccccc", lw=0.6, zorder=0)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10.5, length=0)
    return _save(fig, fname)

def chart_balance(fname):
    # componentes del cambio poblacional de 2024 (personas): barras a favor y en contra
    items = [("Nacimientos", 71358, "#617834"),
             ("Defunciones", -128098, "#8A4353"),
             ("Saldo migratorio", -251221, "#6A1A35"),
             ("Cambio neto", -307961, "#28441E")]
    fig, ax = plt.subplots(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    ys = list(range(len(items)))[::-1]
    for y, (label, v, c) in zip(ys, items):
        ax.barh([y], [v], color=c, height=0.58, zorder=3)
        txt = f"{v:+,}".replace(",", ".")
        if v >= 0:
            ax.annotate(txt, (v, y), textcoords="offset points", xytext=(6, 0),
                        va="center", fontsize=11, fontweight="bold", color="#333333")
        else:
            ax.annotate(txt, (0, y), textcoords="offset points", xytext=(-6, 0),
                        va="center", ha="right", fontsize=11, fontweight="bold", color="white")
    ax.axvline(0, color="#888888", lw=1)
    ax.set_yticks(ys); ax.set_yticklabels([i[0] for i in items])
    ax.set_xlim(-330000, 135000)
    ax.set_xticks([-300000, -200000, -100000, 0, 100000])
    ax.set_xticklabels(["-300 mil", "-200 mil", "-100 mil", "0", "100 mil"])
    ax.set_xlabel("Personas", fontsize=9.5)
    ax.grid(axis="x", color="#cccccc", lw=0.6, zorder=0)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10.5, length=0)
    return _save(fig, fname)

def chart_diverging(fname, c_left, c_right):
    fig, ax = plt.subplots(figsize=(5.2, 2.6))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    ax.barh([0], [-71358], color=c_left, height=0.52, zorder=3)
    ax.barh([0], [128098], color=c_right, height=0.52, zorder=3)
    ax.axvline(0, color="#888888", lw=1)
    ax.annotate("Nacimientos\n71.358", (-71358, 0), textcoords="offset points", xytext=(-6, 0),
                ha="right", va="center", fontsize=11, fontweight="bold")
    ax.annotate("Defunciones\n128.098", (128098, 0), textcoords="offset points", xytext=(6, 0),
                ha="left", va="center", fontsize=11, fontweight="bold")
    ax.set_xlim(-165000, 165000)
    ax.set_ylim(-0.55, 0.55)
    ax.axis("off")
    return _save(fig, fname)

def chart_dotrank(fname, labels, values, colors, mean, mean_label, mean_color="#B04C2C"):
    fig, ax = plt.subplots(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    y = list(range(len(values)))[::-1]
    for yi, v, c in zip(y, values, colors):
        ax.plot([0, v], [yi, yi], color=c, lw=2.2, alpha=0.45, zorder=2, solid_capstyle="round")
        ax.plot([v], [yi], "o", color=c, markersize=11, zorder=3)
        ax.annotate(f"{v:g} %".replace(".", ","), (v, yi), textcoords="offset points",
                    xytext=(10, 0), va="center", fontsize=11.5, fontweight="bold",
                    bbox=dict(fc="white", ec="none", pad=1.4))
    ax.axvline(mean, color=mean_color, lw=1.4, ls=(0, (4, 3)), zorder=1)
    ax.annotate(mean_label, (mean, len(values) - 0.5), textcoords="offset points", xytext=(5, 2),
                fontsize=9.5, color=mean_color, fontweight="bold", va="center")
    ax.set_ylim(-0.55, len(values) - 0.15)
    ax.set_yticks(y); ax.set_yticklabels(labels)
    ax.set_xlabel("% de la población con 60 años o más (2024)", fontsize=9.5)
    ax.set_xlim(0, max(values) * 1.22)
    ax.grid(axis="x", color="#cccccc", lw=0.6, zorder=0)
    for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10.5, length=0)
    return _save(fig, fname)

def chart_stacked(fname, segments):
    # segments: (label, value, color, textcolor)
    fig, ax = plt.subplots(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0); ax.set_facecolor("none")
    left = 0
    for label, v, c, tc in segments:
        ax.barh([0], [v], left=left, color=c, height=0.46, zorder=3)
        ax.annotate(f"{label}\n{v:g} %".replace(".", ","), (left + v / 2, 0), ha="center", va="center",
                    fontsize=10.5, fontweight="bold", color=tc, zorder=4)
        left += v
    ax.set_xlim(0, 100); ax.set_ylim(-0.5, 0.5)
    ax.axis("off")
    return _save(fig, fname)

def chart_pie_legend(fname, items):
    # items: (label, value, color)
    fig = plt.figure(figsize=(7.4, 2.85))
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0.03, 0.04, 0.42, 0.92]); ax.set_facecolor("none")
    vals = [v for _, v, _ in items]
    cols = [c for _, _, c in items]
    ax.pie(vals, colors=cols, startangle=90, counterclock=False,
           wedgeprops=dict(width=1, edgecolor="white", linewidth=2))
    ax2 = fig.add_axes([0.5, 0.04, 0.48, 0.92]); ax2.axis("off")
    for i, (label, v, c) in enumerate(items):
        yy = 0.78 - i * 0.3
        ax2.plot([0.02], [yy + 0.035], "s", color=c, markersize=13, transform=ax2.transAxes)
        ax2.text(0.09, yy, f"{label}: {v:g} %".replace(".", ","), transform=ax2.transAxes,
                 fontsize=12, fontweight="bold", va="center")
    path = os.path.join(IMG, fname)
    fig.savefig(path, dpi=210, transparent=True)
    plt.close(fig)
    return path

def chart_mapa(fname):
    import csv as _csv
    from matplotlib.patches import Polygon as _Poly
    from matplotlib.collections import PatchCollection
    from matplotlib.colors import LinearSegmentedColormap, Normalize
    datos = {}
    with open(os.path.join(BASE, "datos", "csv", "envejecimiento_provincias.csv"), encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            if row["anio"] == "2024" and row["provincia"] != "Cuba":
                datos[row["provincia"]] = float(row["grado_envejecimiento_pct"])
    geo = json.load(open(os.path.join(BASE, "datos", "fuentes", "provincias.geojson"), encoding="utf-8"))
    cmap = LinearSegmentedColormap.from_list("sabio", ["#F8F3E2", "#E7D356", "#A43C2F", "#472C3B"])
    norm = Normalize(21.5, 29.5)
    fig = plt.figure(figsize=(7.4, 2.9))
    fig.patch.set_alpha(0)
    ax = fig.add_axes([0.01, 0.17, 0.98, 0.82]); ax.set_facecolor("none")
    etiquetas = {"Villa Clara": (0, 7), "La Habana": (-14, 11), "Guantánamo": (0, 7)}
    for feat in geo["features"]:
        nombre = feat["properties"]["province"]
        geom = feat["geometry"]
        polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
        patches, cents = [], []
        for poly in polys:
            for ring in poly:
                patches.append(_Poly(ring, closed=True))
                cents.append((sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring), len(ring)))
        color = cmap(norm(datos[nombre])) if nombre in datos else "#E3E0D8"
        pc = PatchCollection(patches, facecolor=color, edgecolor="white", linewidths=0.5, zorder=2)
        ax.add_collection(pc)
        if nombre in etiquetas:
            cx, cy, _ = max(cents, key=lambda t: t[2])
            dx, dy = etiquetas[nombre]
            ax.annotate(f"{nombre}\n{datos[nombre]:g} %".replace(".", ","),
                        (cx, cy), textcoords="offset points", xytext=(dx, dy),
                        ha="center", fontsize=9.5, fontweight="bold", zorder=5,
                        bbox=dict(fc="white", ec="none", alpha=0.75, pad=1.2))
    ax.autoscale_view()
    ax.set_aspect(1.1)
    ax.axis("off")
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cax = fig.add_axes([0.27, 0.05, 0.46, 0.028])
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal", ticks=[22, 24, 26, 28])
    cb.ax.tick_params(labelsize=9, length=0)
    cb.outline.set_visible(False)
    cb.set_label("% de la población con 60 años o más (media nacional: 25,7 %)", fontsize=9.5)
    path = os.path.join(IMG, fname)
    fig.savefig(path, dpi=210, transparent=True)
    plt.close(fig)
    return path

# ---------------------------------------------------------------- pdf
class StoryPDF(FPDF):
    def __init__(self, cfg):
        super().__init__(orientation="P", unit="mm", format="Letter")
        self.cfg = cfg
        self.set_margins(18, 14, 18)
        self.set_auto_page_break(True, margin=16)
        ND = "/usr/share/fonts/truetype/noto"
        self.add_font("serif", "", os.path.join(ND, "NotoSerif-Regular.ttf"))
        self.add_font("serif", "B", os.path.join(ND, "NotoSerif-Bold.ttf"))
        self.add_font("serif", "I", os.path.join(ND, "NotoSerif-Italic.ttf"))
        self.add_font("sans", "", os.path.join(ND, "NotoSans-Regular.ttf"))
        self.add_font("sans", "B", os.path.join(ND, "NotoSans-Bold.ttf"))
        self.add_font("sans", "I", os.path.join(ND, "NotoSans-Italic.ttf"))

    def footer(self):
        self.set_y(-13)
        c = self.cfg
        self.set_draw_color(*hx(c["accent"]))
        self.set_line_width(0.4)
        self.line(18, self.get_y(), 198, self.get_y())
        self.ln(1.6)
        self.set_font("sans", "", 7.5)
        self.set_text_color(*hx("#666666"))
        self.cell(90, 4, f"Un país que cambia · Historia {c['num']} de 5")
        self.cell(0, 4, f"Página {self.page_no()}", align="R")

    def header_band(self):
        c = self.cfg
        self.set_fill_color(*hx(c["dark"]))
        self.rect(0, 0, 216, 50, "F")
        self.set_fill_color(*hx(c["accent"]))
        self.rect(0, 50, 216, 1.6, "F")
        self.set_y(8)
        self.set_font("sans", "B", 8.5)
        self.set_text_color(*hx(c["light"]))
        self.cell(0, 5, c["eyebrow"].upper(), align="C")
        self.ln(6.5)
        self.set_font("serif", "B", 19.5)
        self.set_text_color(*hx("#FFFFFF"))
        self.cell(0, 9.5, c["title"], align="C")
        self.ln(10.5)
        self.set_font("sans", "I", 9.3)
        self.set_text_color(*hx(c["light"]))
        self.multi_cell(0, 4.6, c["deck"], align="C")
        self.set_y(53.2)
        self.set_font("sans", "", 8)
        self.set_text_color(*hx("#666666"))
        self.cell(0, 4, "Por Dagmary Pérez Aguiar · La Habana, noviembre de 2026", align="R")
        self.set_y(60)

    def subhead(self, text):
        c = self.cfg
        self.ln(1.6)
        self.set_font("sans", "B", 11)
        self.set_text_color(*hx(c["dark"]))
        self.cell(0, 5.6, text)
        self.ln(5.9)

    def para(self, text):
        self.set_font("serif", "", 11)
        self.set_text_color(*hx("#2B2B2B"))
        self.multi_cell(0, 6.0, text, align="L")
        self.ln(1.1)

    def chips(self, items):
        c = self.cfg
        self.ln(1)
        y = self.get_y()
        w = (180 - 6 * (len(items) - 1)) / len(items)
        x = 18
        for big, small in items:
            self.set_fill_color(*hx(c["chip_bg"]))
            self.rect(x, y, w, 16.5, "F")
            self.set_xy(x, y + 1.8)
            self.set_font("sans", "B", 14.5)
            self.set_text_color(*hx(c["dark"]))
            self.cell(w, 7, big, align="C")
            self.set_xy(x, y + 9.6)
            self.set_font("sans", "", 7.6)
            self.set_text_color(*hx("#444444"))
            self.multi_cell(w, 3.4, small, align="C")
            x += w + 6
        self.set_y(y + 19.5)

    def esencial_box(self, text):
        c = self.cfg
        self.set_font("serif", "", 10.8)
        lines = self.multi_cell(168, 5.15, text, align="L", dry_run=True, output="LINES")
        h = len(lines) * 5.15 + 10.2
        if self.get_y() + h > 262:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*hx(c["chip_bg"]))
        self.rect(18, y, 180, h, "F")
        self.set_fill_color(*hx(c["accent"]))
        self.rect(18, y, 1.6, h, "F")
        self.set_xy(24, y + 2.6)
        self.set_font("sans", "B", 8.6)
        self.set_text_color(*hx(c["dark"]))
        self.cell(0, 4, "LO ESENCIAL")
        self.set_xy(24, y + 8.2)
        self.set_font("serif", "", 10.8)
        self.set_text_color(*hx("#2B2B2B"))
        self.multi_cell(168, 5.15, text, align="L")
        self.set_y(y + h + 2.5)

    def chart(self, title, path, source, w=170):
        c = self.cfg
        need = w * 2.85 / 7.4 + 16
        if self.get_y() + need > 262:
            self.add_page()
        self.ln(1.5)
        self.set_font("sans", "B", 10.5)
        self.set_text_color(*hx(c["dark"]))
        self.multi_cell(0, 5, title, align="L")
        self.ln(0.8)
        x = (216 - w) / 2
        self.image(path, x=x, w=w)
        self.ln(1)
        self.set_font("sans", "I", 7.6)
        self.set_text_color(*hx("#666666"))
        self.multi_cell(0, 3.6, source, align="L")
        self.ln(2)

    def chart_pair(self, left, right):
        """left/right: (title, path, source) side by side, each ~87mm wide."""
        c = self.cfg
        self.ln(1.5)
        y0 = self.get_y()
        for i, (title, path, source) in enumerate((left, right)):
            x = 18 + i * 91
            self.set_xy(x, y0)
            self.set_font("sans", "B", 9.6)
            self.set_text_color(*hx(c["dark"]))
            self.multi_cell(87, 4.6, title, align="L")
            yimg = self.get_y() + 0.8
            self.image(path, x=x, y=yimg, w=87)
            self.set_xy(x, yimg + 44.5)
            self.set_font("sans", "I", 7.3)
            self.set_text_color(*hx("#666666"))
            self.multi_cell(87, 3.4, source, align="L")
        self.set_y(y0 + 62)

    def ficha_box(self, ficha):
        c = self.cfg
        self.ln(2)
        rows = [("Audiencia", ficha["audiencia"]),
                ("Método", ficha["metodo"]),
                ("Lo que el dato no permite afirmar", ficha["limite"]),
                ("Y ahora, ¿qué?", ficha["accion"])]
        # medir altura total (con la misma fuente con la que se va a dibujar)
        self.set_font("sans", "", 8.3)
        total = 6.6
        rendered = []
        for label, text in rows:
            full = f"{label}: {text}"
            lines = self.multi_cell(172, 3.85, full, align="L", dry_run=True, output="LINES")
            rendered.append((label, full, len(lines)))
            total += len(lines) * 3.85 + 0.7
        if self.get_y() + total > 262:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*hx(c["chip_bg"]))
        self.rect(18, y, 180, total, "F")
        self.set_fill_color(*hx(c["dark"]))
        self.rect(18, y, 180, 6.4, "F")
        self.set_xy(22, y + 1.2)
        self.set_font("sans", "B", 8.6)
        self.set_text_color(*hx("#FFFFFF"))
        self.cell(0, 4, "FICHA DEL PRODUCTO · MODELO: AUDIENCIA · MENSAJE · EVIDENCIA · FORMATO · MEDIO · ACCIÓN")
        yy = y + 8.3
        for label, full, n in rendered:
            self.set_xy(22, yy)
            self.set_font("sans", "", 8.3)
            self.set_text_color(*hx("#333333"))
            self.multi_cell(172, 3.85, full, align="L")
            yy += n * 3.85 + 0.7
        self.set_y(y + total + 2)

    def sources_box(self, text):
        c = self.cfg
        self.ln(1.5)
        if self.get_y() + 18 > 262:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*hx(c["chip_bg"]))
        self.set_font("sans", "", 8)
        self.set_text_color(*hx("#444444"))
        # measure height first
        lines = self.multi_cell(172, 4.1, text, align="L", dry_run=True, output="LINES")
        h = len(lines) * 4.1 + 5
        self.rect(18, y, 180, h, "F")
        self.set_xy(22, y + 2.5)
        self.multi_cell(172, 4.1, text, align="L")
        self.set_y(y + h + 2)

# ---------------------------------------------------------------- historias
STORIES = []

# ---- 1 · El Héroe · Mujeres en la ciencia
STORIES.append(dict(
    num=1, archetype="El Héroe", slug="historia-1-el-heroe-mujeres-en-la-ciencia",
    eyebrow="Serie Un país que cambia · Historia 1 de 5",
    title="La ciencia cubana tiene nombre de mujer",
    deck="En el mundo, solo 33 de cada 100 personas investigadoras son mujeres. En Cuba, son 49 de cada 100.",
    dark="#583B59", accent="#F1607D", light="#FBD9CF", chip_bg="#FDF1EE",
    chips=[("33 %", "de las personas investigadoras del mundo son mujeres (UNESCO)"),
           ("Top 20", "Cuba está entre los 20 países con más investigadoras del mundo (UNESCO)"),
           ("54 %", "aprox., de la fuerza laboral del sector de la ciencia es femenina")],
    esencial="De cada 100 personas que investigan en Cuba, 49 son mujeres; en el mundo son 33. En la Academia de Ciencias pasaron de 1 de cada 4 asientos en el año 2000 a casi 2 de cada 5 hoy. Lo que falta es que lleguen también a los puestos donde se decide.",
    blocks=[
        ("p", "En la mayoría de los laboratorios del mundo pasa algo llamativo: de cada 100 personas que investigan, solo 33 son mujeres. Es el promedio planetario que calcula la UNESCO. Pero hay un archipiélago en el Caribe donde las cuentas salen distintas, y donde la heroína de esta historia no es una persona: son miles."),
        ("h", "La excepción caribeña"),
        ("p", "Cuba está entre los veinte países con mayor proporción de investigadoras del mundo, según el Informe Mundial de la Ciencia de la UNESCO. Aquí, firmar un artículo, dirigir un experimento o defender una patente es cosa de todos los días para miles de mujeres. Las mujeres representan alrededor del 54 % de la fuerza laboral del sector de la ciencia, y son el 49 % de las personas que investigan. No llegaron ayer: llevan décadas entrando por la puerta ancha de la universidad y quedándose en los institutos, los hospitales y los centros de estudio."),
        ("chart1", None),
        ("break", None),
        ("h", "La escalera que aún se sube"),
        ("p", "La paridad en la base no significa igualdad en la cima. En la Academia de Ciencias de Cuba, la proporción de mujeres entre sus miembros pasó del 25,9 % en el período 1998-2002 al 34 % en 2018-2023, y subió al 39 % en la etapa actual, 2024-2029. Cada peldaño costó unos veinte años de trabajo silencioso. Y todavía queda lo que ninguna de estas cifras cuenta: cuántas de ellas dirigen institutos y centros de investigación."),
        ("h", "El espejo regional"),
        ("p", "América Latina y el Caribe está entre las regiones más cercanas a la paridad entre investigadoras e investigadores, con un 45 %, y Cuba, con un 49 %, se sitúa por encima incluso de su región, según el Informe Mundial de la Ciencia de la UNESCO. El contraste con las academias de ciencia es todavía mayor: en el mundo, las mujeres ocupan como promedio solo el 12 % de los puestos en las academias nacionales; en la cubana ya son el 39 %."),
        ("chart2", None),
        ("h", "Por qué importa"),
        ("p", "Importa por una razón que los datos confirman una y otra vez: los equipos diversos se hacen preguntas diversas. Una investigadora que estudia la salud de las madres mira el problema desde dentro. Cuando la mitad del talento de un país se queda fuera del laboratorio, la ciencia pierde la mitad de sus preguntas. Cuba no se dio ese lujo: su ciencia se construyó, en buena medida, con manos de mujer."),
        ("p", "La heroína de los cuentos suele llevar capa y espada. Aquí lleva bata blanca, microscopio y una paciencia de décadas. La historia no está terminada (ese 39 % todavía no es el 50 %), pero tiene una protagonista que ya demostró de sobra que puede, y un camino que, peldaño a peldaño, sigue subiendo."),
    ],
    chart1=("La escalera de la Academia: mujeres entre sus miembros (%)",
            "academia.png",
            "Fuente: Academia de Ciencias de Cuba, composición de sus membresías por período."),
    chart2=("El espejo regional: mujeres entre las personas investigadoras (%)",
            "comparacion.png",
            "Fuente: UNESCO, Informe Mundial de la Ciencia (2021), datos de 2018 o el año más cercano disponible."),
    chart1_w=142, chart2_w=124,
    sources="Fuentes: UNESCO, Informe Mundial de la Ciencia (2021) y datos mundiales sobre mujeres en la investigación · Academia de Ciencias de Cuba, membresía por períodos · ONEI, Observatorio de Ciencia, Tecnología e Innovación (2024).",
    ficha=dict(
        audiencia="público general y, en especial, jóvenes que están eligiendo qué estudiar.",
        metodo="historia construida con datos secundarios ya publicados por UNESCO, la Academia de Ciencias de Cuba y la ONEI; no se recogieron datos nuevos y las cifras se citan tal como las publican las fuentes.",
        limite="En Cuba hay igualdad plena entre mujeres y hombres en la ciencia: los datos muestran paridad de participación, pero la presencia femenina disminuye en los niveles más altos, como la membresía de la Academia.",
        accion="si conoces a una niña o joven que duda de si la ciencia es para ella, cuéntale esta historia con sus cifras: en Cuba, 49 de cada 100 personas que investigan son mujeres."),
))

# ---- 2 · El Detective · La emigración
STORIES.append(dict(
    num=3, archetype="El Detective", slug="historia-3-el-detective-la-emigracion",
    eyebrow="Serie Un país que cambia · Historia 3 de 5",
    title="El caso de los millones que faltan",
    deck="Entre 2016 y 2024, Cuba perdió 1.491.217 habitantes. Vamos a resolver este misterio con las pistas que los datos nos dejaron.",
    dark="#28441E", accent="#6A1A35", light="#C8D0B8", chip_bg="#EEF2E4",
    chips=[("-251.221", "saldo migratorio externo de 2024 (ONEI)"),
           ("688", "salidas netas por día, como promedio, en 2024"),
           ("1.491.217", "habitantes menos que en el máximo de 2016")],
    esencial="Cuba perdió 307.961 habitantes en un solo año, 2024: se fueron muchas más personas de las que llegaron y murieron más de las que nacieron. La población que de verdad vive en el país bajó de 10.055.968 a 9.748.007. De los 168 municipios, solo uno creció.",
    blocks=[
        ("p", "La historia empieza con dos cifras. En 2016, Cuba tenía 11.239.224 habitantes, su máximo histórico según la Oficina Nacional de Estadística e Información (ONEI). Ocho años después, ese mismo país cuenta 9.748.007 habitantes. Entre un periodo y otro faltan casi un millón y medio de personas: el equivalente a borrar del mapa a la segunda y la tercera ciudades del país, juntas y enteras. La pregunta es simple: ¿dónde están?"),
        ("h", "Pista uno: no es un error de conteo"),
        ("p", "La primera sospecha recae sobre el informe: ¿y si el conteo está mal? Pero las cifras de la ONEI son consistentes año tras año: solo entre 2020 y 2024 la población se redujo en torno a 1,4 millones. No es un ajuste estadístico; es una hemorragia demográfica. Es verdad que las defunciones superan a los nacimientos, pero esa brecha, por sí sola, no alcanza para explicar un desplome tan rápido. Hace falta otra explicación."),
        ("chart1", None),
        ("break", None),
        ("h", "Pista dos: el saldo que señala al aeropuerto"),
        ("p", "La segunda pista tiene nombre técnico: saldo migratorio externo. Es la diferencia entre quienes entran al país y quienes salen para residir fuera. En 2024 ese saldo fue de -251.221 personas: en un solo año salieron un cuarto de millón de cubanos más de los que entraron. Es como si cada día de 2024 hubieran partido, en neto, unas 688 personas: un avión lleno tras otro, día tras día."),
        ("p", "La serie completa de la población efectiva (la que de verdad vive en el país: quien nació aquí o acumuló 180 días o más de estancia en el último año) dibuja la aceleración: el país se mantuvo por encima de los 11,1 millones hasta 2020 y luego la curva se despeña. Solo en 2024 el decrecimiento fue de 307.961 personas, unas 844 menos cada día como promedio, y el detalle más claro es geográfico: solo un municipio, Antilla, en Holguín, creció; el resto del mapa perdió habitantes."),
        ("chart2", None),
        ("h", "El escenario"),
        ("p", "Aquí no hay un solo culpable: hay un escenario. Una economía en crisis prolongada, salarios que no alcanzan, servicios que se deterioran y, al mismo tiempo, rutas migratorias abiertas hacia varios destinos. La emigración cubana no es nueva (viene en oleadas desde hace más de medio siglo), pero la oleada reciente es la mayor y la más rápida de las registradas. Y deja una huella en cada casa que se queda vacía: la población que permanece es, cada año, un poco más vieja."),
        ("p", "Los efectos apenas empiezan a verse: cada persona que se va deja un hueco en una familia, en un hospital, en una escuela y en la cola del pan. Los países no se vacían de golpe; se vacían persona a persona, maleta a maleta, hasta que un día la estadística lo grita. Detrás de cada número hay una puerta que se cerró. Contarlas, año tras año, es no dejar que se cierren en silencio."),
    ],
    chart1=("La caída: población de Cuba (millones de habitantes)",
            "caida.png",
            "Fuente: ONEI, población al cierre de cada año; 2023 y 2024, población con residencia efectiva. Eje vertical ampliado (no parte de cero) para apreciar la caída; entre 2016 y 2024 la diferencia es de 1.491.217 personas."),
    chart2=("Anatomía de 2024: así se perdieron 307.961 habitantes en un solo año",
            "cascada.png",
            "Fuente: ONEI, componentes del cambio poblacional de 2024. El cambio neto es la suma de los tres componentes."),
    chart1_w=134, chart2_w=116,
    sources="Fuentes: ONEI, Anuario Demográfico de Cuba y estimaciones de población residente (2016-2024) · ONEI, población con residencia efectiva y saldo migratorio externo 2024.",
    ficha=dict(
        audiencia="público general, con atención a las familias cubanas que tienen a alguien dentro o fuera de la isla.",
        metodo="historia construida con las series oficiales de población y migración publicadas por la ONEI; las diferencias entre años y el promedio diario son cálculos de la autora a partir de esas cifras.",
        limite="El saldo migratorio de 2024, -251.221 personas, es una diferencia neta entre salidas y entradas: no es el conteo de las personas que emigraron, y tampoco dice a qué países se fueron.",
        accion="antes de compartir cualquier cifra de emigración, comprueba su año y su fuente; y si tienes a alguien lejos, esta historia es un buen pretexto para llamarlo hoy."),
))

# ---- 3 · La Sombra · El turismo que no vuelve
STORIES.append(dict(
    num=5, archetype="La Sombra", slug="historia-5-la-sombra-el-turismo-que-no-vuelve",
    eyebrow="Serie Un país que cambia · Historia 5 de 5",
    title="Las playas que se quedaron esperando",
    deck="En 2018 Cuba recibió 4,6 millones de visitantes internacionales. En 2024 llegaron 2,2 millones.",
    dark="#074461", accent="#FDD503", light="#BFE3F2", chip_bg="#EAF6FB",
    chips=[("-48 %", "de visitantes en 2024 frente a 2019"),
           ("-17,8 %", "caída de las visitas de cubanos residentes en el exterior"),
           ("2018", "el año récord: 4,6 millones de visitantes")],
    esencial="En 2018 llegaron a Cuba 4,6 millones de visitantes; en 2024 llegaron 2,2 millones, menos de la mitad. La caída empezó antes de la pandemia y la recuperación posterior fue más débil que la de los países vecinos. Casi 4 de cada 10 visitantes vienen de un solo país: Canadá.",
    blocks=[
        ("p", "Hay una imagen que se repite en los polos turísticos del país: hoteles con la mitad de las luces encendidas, tumbonas alineadas frente a un mar perfecto y nadie tumbado en ellas. Durante años, el turismo fue el motor más visible de la economía cubana. Hoy ese motor tose, y la sombra de su caída se proyecta sobre miles de familias que vivían de él directa o indirectamente."),
        ("h", "La caída, en tres números"),
        ("p", "Primer número: 4,6 millones de visitantes internacionales en 2018, la mejor marca de la serie histórica. Segundo número: 4,2 millones en 2019, ya en descenso. Después llegó la pandemia y lo detuvo todo, como en medio mundo; eso no distingue a Cuba de nadie. Lo que la distingue es lo que pasó después: mientras el Caribe recuperaba a sus viajeros, Cuba cerró 2024 con 2,2 millones de visitantes, un 48 % menos que en 2019 y la peor cifra en 17 años si se apartan los años de la pandemia, según los datos de la ONEI recogidos por la agencia EFE. Dicho sin porcentajes: de cada diez visitantes que llegaron en 2018, en 2024 no vinieron ni cinco."),
        ("chart1", None),
        ("p", "El gráfico cuenta además un segundo acto que duele más: tras el fondo de 2022 (1,6 millones), el sector intentó levantarse en 2023 (2,4 millones) y volvió a caer en 2024. Ni siquiera se cumplió la meta oficial del año, que rondaba los 3 millones de visitantes. Y el mapa de los que sí vinieron se estrechó: Canadá, el país del que más visitantes llegan, aportó el 39 % de todos los visitantes de 2024, según el Ministerio de Turismo; cuando un solo mercado sostiene casi 4 de cada 10 llegadas, cualquier tropiezo de ese mercado afecta a la economía nacional."),
        ("h", "Ni los de casa vuelven"),
        ("p", "Entre quienes dejaron de venir están los propios cubanos que viven fuera del país: sus visitas cayeron un 17,8 %. Es el puente triste entre esta historia y el tema de la emigración: quien se fue no siempre regresa, ni siquiera de visita. La maleta que antes aterrizaba cargada de regalos, medicinas y ayuda para la familia ahora, muchas veces, ni siquiera despega."),
        ("h", "Lo que se pierde con cada avión vacío"),
        ("p", "Un visitante que no llega no es solo una estadística de aeropuerto. Es la casa particular que no se alquila esa semana, el restaurante privado que no llena sus mesas, el taxista que hace menos viajes, la artesana que vende menos piezas en el malecón. El turismo reparte sus ingresos entre miles de manos, muchas de ellas privadas y pequeñas, y por eso su caída se siente primero en los bolsillos más modestos."),
        ("p", "En los cuentos, la sombra anuncia que algo acecha. En los datos, anuncia consecuencias: menos divisas, menos empleo y menos motivos para quedarse. El mar, eso sí, sigue ahí, perfecto y paciente, como estuvo siempre. La pregunta que deja esta historia flotando en el aire es si los que faltan, turistas y emigrados, volverán algún día a contar a Cuba entre sus destinos, o si las playas tendrán que seguir esperando."),
    ],
    chart1=("El motor que se apaga: visitantes internacionales en Cuba (millones)",
            "turismo.png",
            "Fuente: ONEI, llegada de visitantes internacionales; datos de 2024 recogidos por la agencia EFE. Se omiten 2020 y 2021, los años del cierre por la pandemia."),
    chart1_w=132,
    sources="Fuentes: ONEI, estadísticas de turismo y llegada de visitantes internacionales (2018-2024) · Agencia EFE, balance turístico de Cuba en 2024 · Ministerio de Turismo, mercados emisores 2024.",
    ficha=dict(
        audiencia="público general y, en especial, quienes trabajan en el turismo o viven de él.",
        metodo="historia construida con las estadísticas de llegadas publicadas por la ONEI y recogidas por la agencia EFE, y con datos del Ministerio de Turismo sobre mercados emisores; el porcentaje de caída frente a 2019 es cálculo de la autora. Se omiten 2020 y 2021, los años del cierre por la pandemia.",
        limite="El turismo cayó por una sola causa: las cifras miden cuántos visitantes llegaron, no los motivos de quienes dejaron de venir; las causas son varias y estos datos, por sí solos, no las separan.",
        accion="si vives del turismo o conoces a quien vive de él, comparte esta historia con las cifras completas y su fuente: entender la caída, sin exagerarla ni esconderla, es el primer paso para revertirla."),
))

# ---- 4 · El Sabio · Los que no nacen y los que envejecen
STORIES.append(dict(
    num=2, archetype="El Sabio", slug="historia-2-el-sabio-los-que-no-nacen-y-los-que-envejecen",
    eyebrow="Serie Un país que cambia · Historia 2 de 5",
    title="Los que no nacen y los que envejecen",
    deck="En 2024 nacieron en Cuba 71.358 niños y murieron 128.098 personas. Entre la cuna y el cementerio, un país entero cambia de edad.",
    dark="#472C3B", accent="#A43C2F", light="#F5EDBB", chip_bg="#F8F3E2",
    chips=[("1,29", "hijos por mujer: la fecundidad más baja registrada"),
           ("1978", "último año en que Cuba alcanzó el nivel de reemplazo"),
           ("1,8", "defunciones por cada nacimiento en 2024")],
    esencial="En 2024 nacieron 71.358 bebés y murieron 128.098 personas: por cada 10 nacimientos hubo 18 muertes. Una de cada 4 personas tiene 60 años o más, y en Villa Clara casi 1 de cada 3. El país envejece en las 16 provincias, sin excepción.",
    blocks=[
        ("p", "Un sabio no levanta la voz: ha vivido bastante para reconocer una señal cuando la ve, así como Cuba ha visto pasar el tiempo, y esta historia se cuenta con dos relojes que marchan en sentidos opuestos: el de los nacimientos, cada vez más lento, y el de la vejez, cada vez más concurrido. Miremos los dos al mismo tiempo."),
        ("h", "La cuna que se vacía"),
        ("p", "En 2024 nacieron en Cuba 71.358 bebés, la cifra más baja en 65 años. La fecundidad cayó a 1,29 hijos por mujer, el mínimo registrado, y detrás hay una racha larguísima que pocos países pueden contar: Cuba no alcanza el nivel de reemplazo (los 2,1 hijos por mujer que necesita una población para mantenerse estable) desde 1978. Es decir, lleva casi medio siglo teniendo menos hijos de los necesarios para relevarse a sí misma. Las causas se entrelazan: mujeres que estudian y trabajan, viviendas que no alcanzan, proyectos de vida que se posponen y, cada vez más, jóvenes que hacen las maletas antes de hacer familia."),
        ("chartpair", None),
        ("break", None),
        ("h", "El otro extremo del pasillo"),
        ("p", "Mientras tanto, las defunciones de 2024 fueron 128.098: por cada bebé que llegó al mundo, se despidieron 1,8 personas. Y la población que permanece envejece a paso firme: en 2015, el 19,4 % de los cubanos tenía 60 años o más; al cierre de 2024 ya era el 25,7 %, una de cada cuatro personas. Villa Clara, La Habana y Sancti Spíritus encabezan la lista de las provincias más envejecidas, y la tendencia no perdona a ninguna."),
        ("p", "Dentro de La Habana, el municipio de Plaza de la Revolución alcanza un 36,8 % de población mayor: más de uno de cada tres vecinos tiene 60 años o más. La relación de dependencia (las personas en edad de no trabajar que tocan por cada mil en edad de trabajar) lo resume en una cifra incómoda: en 2024 había 710 personas en edades inactivas por cada 1.000 en edad de trabajar."),
        ("chart2", None),
        ("h", "Un éxito con factura"),
        ("p", "Pero hay que matizar. Que un país envejezca significa, antes que nada, que su gente vive más años, y eso es una conquista de la salud pública y de décadas de médicos y maestros. La factura llega después, y no es pequeña: más pensiones que sostener entre menos trabajadores, más cuidados que ofrecer entre menos hijos, más abuelos que viven solos porque los nietos, si los hay, viven en otro país."),
        ("p", "La lección es de paciencia y de escucha: los datos demográficos no gritan, dan señales con décadas de antelación. Cuba lleva desde 1978 dando la misma señal, que su población envejecería y se reduciría, y hoy esa señal es la realidad cotidiana de cada familia. Atenderla a tiempo (en políticas, en cuidados, en oportunidades para los jóvenes) marca la diferencia entre un país que envejece con dignidad y uno que envejece por descuido."),
    ],
    chartpair=(("La balanza de 2024: nacimientos frente a defunciones",
                "balanza.png",
                "Fuente: ONEI, Anuario Demográfico 2024."),
               ("Población de 60 años o más (% del total)",
                "envejecimiento.png",
                "Fuente: ONEI, indicadores demográficos 2015 y 2024.")),
    chart2_w=108,
    chart2=("El mapa de la vejez: población de 60 años o más por provincia, 2024 (%)",
            "mapa_envejecimiento.png",
            "Fuente: ONEI, El envejecimiento de la población. Cuba y sus territorios 2024, tabla 3 (grado de envejecimiento por provincias). Límites provinciales: GeoJSON abierto de Covid19CubaData."),
    sources="Fuentes: ONEI, Anuario Demográfico de Cuba 2024 e indicadores de envejecimiento poblacional · ONEI, El envejecimiento de la población. Cuba y sus territorios 2024 · ONEI / CEPDE, estudios sobre fecundidad y dinámica demográfica.",
    ficha=dict(
        audiencia="público general y, en especial, familias que cuidan o cuidarán a personas mayores.",
        metodo="historia construida con los indicadores demográficos oficiales de la ONEI (nacimientos, defunciones, fecundidad y envejecimiento); la razón entre defunciones y nacimientos es cálculo de la autora.",
        limite="Cuba tendrá una población determinada en 2050: estos datos describen 2024 y una tendencia de décadas, pero no predicen el futuro, que depende también de la migración y de las políticas que se adopten.",
        accion="haz la cuenta en tu propia familia: ¿quiénes tienen más de 60 años y quién los cuida o los cuidará? Conversarlo ahora, con los datos sobre la mesa, es parte de envejecer con dignidad."),
))

# ---- 5 · La Transformación · Las mipymes
STORIES.append(dict(
    num=4, archetype="La Transformación", slug="historia-4-la-transformacion-las-mipymes",
    eyebrow="Serie Un país que cambia · Historia 4 de 5",
    title="Los que se quedaron y emprendieron",
    deck="En septiembre de 2021 Cuba legalizó las mipymes privadas. A marzo de 2025 ya operaban 9.550: la transformación no llegó con un discurso, llegó abriendo locales.",
    dark="#24503C", accent="#E9B44C", light="#F5E3B0", chip_bg="#EDF4EE",
    chips=[("Sept. 2021", "se legalizan las mipymes privadas en Cuba"),
           ("9.550", "mipymes privadas operando a marzo de 2025"),
           ("+314", "nuevas en un solo trimestre (dic. 2024 a mar. 2025)")],
    esencial="En tres años y medio, Cuba pasó de no tener empresas privadas legales a registrar 9.550 mipymes que emplean a 262.000 personas, con 183.000 puestos nuevos. La mayoría de los socios tiene entre 36 y 59 años, y más de 7 de cada 10 son hombres.",
    blocks=[
        ("p", "Durante décadas, abrir un negocio privado en Cuba era imposible. Eso cambió con fecha exacta: septiembre de 2021, cuando las micro, pequeñas y medianas empresas privadas fueron legalizadas. Desde entonces, en miles de esquinas se repite la misma escena: una reja que se abre por primera vez, un cartel recién pintado, una población mirando nuevas ofertas."),
        ("h", "Nueve mil quinientos locales"),
        ("p", "A diciembre de 2024 operaban en el país 9.236 mipymes privadas; tres meses después, en marzo de 2025, ya eran 9.550, según los registros oficiales del Ministerio de Economía y Planificación. El ritmo (más de 300 nuevas en un solo trimestre) habla de una energía contenida durante años que por fin encontró cauce legal. No son grandes corporaciones: son el taller que arregla lo que ya no se puede importar, la dulcería del barrio, la pequeña fábrica que convierte la materia prima local en productos que antes, sencillamente, no aparecían en ninguna bodega."),
        ("chart1", None),
        ("break", None),
        ("h", "De qué están hechas"),
        ("p", "El gráfico muestra su retrato sectorial: la manufactura concentra el 30 % de las mipymes; el alojamiento y la comida, el 23 %; y la construcción, el 19 %. Entre las tres actividades suman casi tres de cada cuatro empresas. Es un retrato honesto de las necesidades del país: producir lo que falta, alimentar a la gente y construir o reparar lo que se cae."),
        ("h", "¿Quiénes emprenden, y a cuántos emplean?"),
        ("p", "El Ministerio de Economía y Planificación informó a la Asamblea Nacional que los nuevos actores económicos empleaban a 262.000 trabajadores, de los cuales 183.000 eran puestos nuevos (más que todos los habitantes de la ciudad de Matanzas, que son 137.303 según la ONEI), y que su aporte rondaba el 7,7 % del PIB, el valor de todo lo que el país produce en un año. El retrato de los socios también cuenta una historia: la mayoría tiene entre 36 y 59 años, y hay una brecha que conecta con la primera historia de esta serie, pero al revés: más del 74 % de los socios son hombres. Donde la ciencia cubana es femenina, el negocio privado es masculino."),
        ("chart2", None),
        ("h", "Transformarse no es fácil"),
        ("p", "Transformarse no promete milagros: promete cambio, y el cambio cuesta. Estas empresas nacen en medio de la misma crisis que empuja a otros a emigrar y no todas sobrevivirán; otras serán el empleador principal de su cuadra. Por primera vez en generaciones, montar un negocio es un proyecto de vida legal, visible y respetable para miles de cubanos."),
        ("p", "Y así se cierra el círculo de esta serie. Frente a los que se van, los que no vienen y los que no nacen, las mipymes son la respuesta de los que se quedan: apostar por el país desde un local que abre cada mañana. Lo que está aprendiendo a construir de nuevo, negocio a negocio y familia a familia, también es el país."),
    ],
    chart1=("El retrato sectorial: de qué son las mipymes privadas (%)",
            "sectores.png",
            "Fuente: ONEI / Ministerio de Economía y Planificación, mipymes privadas en operación (2025). Otras agrupa el resto de las actividades."),
    chart1_w=132, chart2_w=112,
    chart2=("¿Quiénes emprenden? Socios de los nuevos actores económicos por edad (%)",
            "socios.png",
            "Fuente: Ministerio de Economía y Planificación, informe a la Asamblea Nacional (2023), datos declarados por los propios actores."),
    sources="Fuentes: Ministerio de Economía y Planificación, registro de mipymes privadas (diciembre de 2024 y marzo de 2025) e informe a la Asamblea Nacional sobre nuevos actores económicos (2023) · ONEI, distribución por actividad económica · Marco legal de las mipymes, septiembre de 2021.",
    ficha=dict(
        audiencia="público general y, en especial, quienes se plantean emprender o ya tienen un negocio pequeño.",
        metodo="historia construida con el registro oficial de mipymes del Ministerio de Economía y Planificación y la distribución sectorial de la ONEI; el aumento trimestral es cálculo de la autora a partir de ambos cortes.",
        limite="Las mipymes están salvando la economía: el registro cuenta empresas en operación, pero no dice cuántas prosperan, cuánto venden ni cuántos empleos generan; eso estos datos no lo miden.",
        accion="la próxima vez que pases frente a un negocio privado nuevo, entra, compra algo si puedes y pregunta cómo empezó: detrás de cada uno de estos 9.550 locales hay una historia que merece ser contada."),
))

# ---------------------------------------------------------------- build
def build_charts():
    dec2 = lambda v: f"{v:.2f}".replace(".", ",")
    dec1 = lambda v: f"{v:.1f}".replace(".", ",")
    chart_step("academia.png", ["1998-2002", "2018-2023", "2024-2029"], [25.9, 34, 39],
               "#F1607D", "% de mujeres", fill="#FBD9E1")
    chart_area("caida.png", [2016, 2020, 2023, 2024], [11.24, 11.18, 10.06, 9.75],
               "#1B6031", "Millones de habitantes", dec2, highlight_last="#6A1A35")
    chart_balance("cascada.png")
    chart_area("turismo.png", [2018, 2019, 2022, 2023, 2024], [4.6, 4.2, 1.6, 2.4, 2.2],
               "#199ED9", "Millones de visitantes", dec1, highlight_last="#ED193F",
               note="intento de recuperación")
    chart_diverging("balanza.png", "#D6E169", "#472C3B")
    chart_slope("envejecimiento.png", [2015, 2024], [19.4, 25.7], "#A43C2F", "% de la población total")
    chart_stacked("sectores.png", [("Manufactura", 30, "#2E7D5B", "#FFFFFF"),
                                   ("Alojamiento\ny comida", 23, "#F08A5E", "#FFFFFF"),
                                   ("Construcción", 19, "#E9B44C", "#333333"),
                                   ("Otras", 28, "#C9D4CE", "#333333")])
    chart_bars("comparacion.png", ["Mundo", "América Latina\ny el Caribe", "Cuba"], [33, 45, 49],
               ["#7DBA98", "#C85B7A", "#F1607D"], "% de mujeres entre las personas investigadoras",
               horiz=True)
    chart_mapa("mapa_envejecimiento.png")
    chart_pie_legend("socios.png", [("36 a 59 años", 60.5, "#24503C"),
                                    ("18 a 35 años", 25.5, "#2E7D5B"),
                                    ("60 años o más", 14, "#E9B44C")])

def build_story(cfg):
    pdf = StoryPDF(cfg)
    pdf.add_page()
    pdf.header_band()
    pdf.chips(cfg["chips"])
    if cfg.get("esencial"):
        pdf.esencial_box(cfg["esencial"])
    for kind, text in cfg["blocks"]:
        if kind == "h":
            pdf.subhead(text)
        elif kind == "p":
            pdf.para(text)
        elif kind == "chart1":
            t, f, s = cfg["chart1"]
            pdf.chart(t, os.path.join(IMG, f), s, w=cfg.get("chart1_w", 170))
        elif kind == "chart2":
            t, f, s = cfg["chart2"]
            pdf.chart(t, os.path.join(IMG, f), s, w=cfg.get("chart2_w", 150))
        elif kind == "chartpair":
            (t1, f1, s1), (t2, f2, s2) = cfg["chartpair"]
            pdf.chart_pair((t1, os.path.join(IMG, f1), s1), (t2, os.path.join(IMG, f2), s2))
        elif kind == "break":
            pdf.add_page()
    accion = cfg["ficha"]["accion"]
    pdf.subhead("¿Y ahora qué?")
    pdf.para(accion[0].upper() + accion[1:])
    pdf.sources_box(cfg["sources"])
    path = os.path.join(OUT, cfg["slug"] + ".pdf")
    pdf.output(path)
    words = sum(len(t.split()) for k, t in cfg["blocks"] if k == "p")
    print(f"{cfg['slug']}: {pdf.page_no()} páginas, ~{words} palabras de texto corrido -> {path}")
    return path

if __name__ == "__main__":
    build_charts()
    for s in STORIES:
        build_story(s)
