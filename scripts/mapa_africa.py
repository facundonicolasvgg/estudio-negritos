#!/usr/bin/env python3
"""Genera un mapa de Africa con TODOS los territorios (paises actuales) coloreados
cada uno de un color distinto y etiquetados con su nombre actual en espanol.
Encima se situan las culturas del temario."""
import json
import os
import colorsys
import urllib.request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
from adjustText import adjust_text

# GeoJSON de paises (propiedad "name" con nombres en ingles tipo "Ivory Coast").
WORLD = os.path.join(os.path.dirname(__file__), "world.geojson")
WORLD_URL = ("https://raw.githubusercontent.com/johan/world.geo.json/"
             "master/countries.geo.json")

def ensure_world():
    """Descarga el geojson de paises si no existe en local."""
    if not os.path.exists(WORLD):
        print("descargando geojson de paises...")
        urllib.request.urlretrieve(WORLD_URL, WORLD)

# TODOS los paises africanos: nombre en geojson (ingles) -> nombre ACTUAL en espanol.
AFRICA_NAMES = {
    "Algeria": "ARGELIA",
    "Angola": "ANGOLA",
    "Benin": "BENIN",
    "Botswana": "BOTSUANA",
    "Burkina Faso": "BURKINA FASO",
    "Burundi": "BURUNDI",
    "Cameroon": "CAMERUN",
    "Central African Republic": "REP.\nCENTROAFRICANA",
    "Chad": "CHAD",
    "Democratic Republic of the Congo": "RD DEL CONGO",
    "Djibouti": "YIBUTI",
    "Egypt": "EGIPTO",
    "Equatorial Guinea": "GUINEA ECUAT.",
    "Eritrea": "ERITREA",
    "Ethiopia": "ETIOPIA",
    "Gabon": "GABON",
    "Gambia": "GAMBIA",
    "Ghana": "GHANA",
    "Guinea": "GUINEA",
    "Guinea Bissau": "GUINEA-BISAU",
    "Ivory Coast": "COSTA DE MARFIL",
    "Kenya": "KENIA",
    "Lesotho": "LESOTO",
    "Liberia": "LIBERIA",
    "Libya": "LIBIA",
    "Madagascar": "MADAGASCAR",
    "Malawi": "MALAUI",
    "Mali": "MALI",
    "Mauritania": "MAURITANIA",
    "Morocco": "MARRUECOS",
    "Mozambique": "MOZAMBIQUE",
    "Namibia": "NAMIBIA",
    "Niger": "NIGER",
    "Nigeria": "NIGERIA",
    "Republic of the Congo": "R. DEL CONGO",
    "Rwanda": "RUANDA",
    "Senegal": "SENEGAL",
    "Sierra Leone": "SIERRA LEONA",
    "Somalia": "SOMALIA",
    "Somaliland": "SOMALILANDIA",
    "South Africa": "SUDAFRICA",
    "South Sudan": "SUDAN DEL SUR",
    "Sudan": "SUDAN",
    "Swaziland": "ESUATINI",
    "Togo": "TOGO",
    "Tunisia": "TUNEZ",
    "Uganda": "UGANDA",
    "United Republic of Tanzania": "TANZANIA",
    "Western Sahara": "SAHARA OCC.",
    "Zambia": "ZAMBIA",
    "Zimbabwe": "ZIMBABUE",
}

# (numero, nombre, pais, lon, lat, region)  region: O=occidental C=central E=oriental/austral
CULTURES = [
    # --- Africa occidental ---
    (1,  "Bambara / Bamana", "Mali", -6.5, 13.2, "O"),
    (2,  "Dogon (Bandiagara)", "Mali", -3.35, 14.45, "O"),
    (3,  "Tellem", "Mali", -3.1, 14.9, "O"),
    (4,  "Djenne-Djeno", "Mali", -4.9, 13.55, "O"),
    (5,  "Senufo", "Costa de Marfil", -5.9, 9.8, "O"),
    (6,  "Bwa / Nunuma", "Burkina Faso", -3.4, 12.0, "O"),
    (7,  "Mossi", "Burkina Faso", -1.2, 12.5, "O"),
    (8,  "Lobi", "Burkina Faso / Ghana", -3.2, 10.2, "O"),
    (9,  "Bidyogo (Bissagos)", "Guinea-Bisau", -16.4, 11.3, "O"),
    (10, "Mende (Sande)", "Sierra Leona", -11.8, 8.0, "O"),
    (11, "Dan", "C. de Marfil / Liberia", -8.3, 6.7, "O"),
    (12, "We-Guere", "Costa de Marfil", -7.5, 6.0, "O"),
    (13, "Gouro / Guro", "Costa de Marfil", -6.3, 7.4, "O"),
    (14, "Baule", "Costa de Marfil (centro)", -4.7, 7.4, "O"),
    (15, "Asante / Akan", "Ghana (Kumasi)", -1.5, 6.6, "O"),
    (16, "Dahomey-Fon / Vudu (Ewe-Fon)", "Rep. Benin / Togo", 1.9, 7.3, "O"),
    (17, "Yoruba", "Nigeria (SO)", 3.7, 7.9, "O"),
    (18, "Ife", "Nigeria", 4.9, 7.0, "O"),
    (19, "Reino de Benin (Edo)", "Nigeria", 5.7, 6.0, "O"),
    (20, "Nok", "Nigeria (Niger-Benue)", 8.2, 9.6, "O"),
    (21, "Igbo (rio Cross)", "Nigeria (SE)", 7.6, 6.2, "O"),
    (22, "Ibibio", "Nigeria (SE)", 7.9, 4.8, "O"),
    # --- Africa central ---
    (23, "Musgum", "Camerun (N)", 15.0, 10.6, "C"),
    (24, "Fang (Byeri)", "Camerun/G.Ecu./Gabon", 11.6, 1.7, "C"),
    (25, "Kota", "Gabon / Congo", 13.7, -0.6, "C"),
    (26, "Kongo / Vili", "desemboc. Congo", 13.2, -5.6, "C"),
    (27, "Teke", "Rep. Congo", 15.6, -3.0, "C"),
    (28, "Yaka", "RD Congo / Angola", 17.6, -6.6, "C"),
    (29, "Pende", "RD Congo", 19.4, -7.2, "C"),
    (30, "Songye", "RD Congo", 24.2, -5.6, "C"),
    (31, "Mangbetu", "RD Congo (NE)", 27.8, 3.2, "C"),
    # --- Africa oriental / austral ---
    (32, "Bodi / Mursi / Surma", "Etiopia (valle del Omo)", 35.9, 6.2, "E"),
    (33, "Sara / Saracat", "Chad", 18.4, 9.2, "E"),
]

REGION_COLORS = {"O": "#7a1f00", "C": "#063d1e", "E": "#3a0f4a"}   # punto/nombre de cultura
REGION_NAMES = {
    "O": "Africa OCCIDENTAL",
    "C": "Africa CENTRAL",
    "E": "Africa ORIENTAL / AUSTRAL",
}

def make_palette(n):
    """n colores bien diferenciados; se intercalan los tonos para que paises
    contiguos en la lista no salgan parecidos."""
    step = max(1, round(n / 3.0))
    order, seen = [], set()
    for start in range(step):
        i = start
        while i < n:
            if i not in seen:
                order.append(i); seen.add(i)
            i += step
    cols = []
    for rank, i in enumerate(order):
        h = i / float(n)
        light = 0.78 if rank % 2 == 0 else 0.70
        sat = 0.58 if rank % 3 else 0.68
        r, g, b = colorsys.hls_to_rgb(h, light, sat)
        cols.append("#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255)))
    return cols

# un color distinto por cada pais africano
_afr_sorted = sorted(AFRICA_NAMES.keys())
_palette = make_palette(len(_afr_sorted))
COUNTRY_FILL = {name: _palette[i] for i, name in enumerate(_afr_sorted)}

# ajustes finos de posicion de la etiqueta del pais (dx, dy en grados)
LABEL_NUDGE = {
    "Gambia": (-2.6, 0.0),
    "Equatorial Guinea": (-1.2, -1.2),
    "Guinea Bissau": (-1.6, 0.0),
    "Togo": (-0.2, -1.0),
    "Benin": (0.2, -1.0),
    "Rwanda": (-0.8, 0.1),
    "Burundi": (-0.8, -0.4),
    "Lesotho": (0.4, -0.3),
    "Swaziland": (1.8, -0.2),
    "Djibouti": (1.8, 0.2),
}

def iter_polys(geom):
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            yield ring
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                yield ring

def ring_area(ring):
    a = 0.0
    n = len(ring)
    for i in range(n - 1):
        a += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1]
    return abs(a) * 0.5

def ring_centroid(ring):
    x = [p[0] for p in ring]
    y = [p[1] for p in ring]
    n = len(ring)
    A = cx = cy = 0.0
    for i in range(n - 1):
        cross = x[i] * y[i + 1] - x[i + 1] * y[i]
        A += cross
        cx += (x[i] + x[i + 1]) * cross
        cy += (y[i] + y[i + 1]) * cross
    A *= 0.5
    if abs(A) < 1e-9:
        return sum(x) / n, sum(y) / n
    return cx / (6 * A), cy / (6 * A)

def largest_ring(geom):
    best, best_area = None, -1.0
    for ring in iter_polys(geom):
        a = ring_area(ring)
        if a > best_area:
            best_area, best = a, ring
    return best

def main():
    ensure_world()
    world = json.load(open(WORLD))
    fig, ax = plt.subplots(figsize=(18, 13))

    # --- relleno: CADA pais africano con su propio color ---
    for feat in world["features"]:
        name = feat["properties"].get("name", "")
        if name not in AFRICA_NAMES:
            continue
        face = COUNTRY_FILL[name]
        polys = [MplPolygon(r, closed=True) for r in iter_polys(feat["geometry"])]
        pc = PatchCollection(polys, facecolor=face, edgecolor="#3a3a3a",
                             linewidths=0.8, zorder=2)
        ax.add_collection(pc)

    # --- etiqueta con el NOMBRE ACTUAL (espanol) de cada pais ---
    for feat in world["features"]:
        name = feat["properties"].get("name", "")
        if name not in AFRICA_NAMES:
            continue
        label = AFRICA_NAMES[name]
        cx, cy = ring_centroid(largest_ring(feat["geometry"]))
        dx, dy = LABEL_NUDGE.get(name, (0.0, 0.0))
        ax.text(cx + dx, cy + dy, label, color="#1c1c1c", fontsize=7.6,
                fontweight="bold", ha="center", va="center", zorder=4,
                linespacing=0.9,
                path_effects=[pe.withStroke(linewidth=2.2, foreground="white")])

    # --- culturas del temario: punto de color por region + nombre ---
    texts = []
    for num, name, country, lon, lat, region in CULTURES:
        color = REGION_COLORS[region]
        ax.plot(lon, lat, "o", color=color, markersize=8.0,
                markeredgecolor="white", markeredgewidth=1.0, zorder=6)
        t = ax.text(lon, lat, name, color=color, fontsize=8.0,
                    fontweight="bold", ha="center", va="center", zorder=8,
                    path_effects=[pe.withStroke(linewidth=2.4, foreground="white")])
        texts.append(t)

    adjust_text(
        texts, ax=ax,
        expand=(1.25, 1.6),
        force_text=(0.5, 0.8),
        arrowprops=dict(arrowstyle="-", color="#444444", lw=0.6, alpha=0.85),
    )

    ax.set_xlim(-22, 54)
    ax.set_ylim(-37, 39)
    ax.set_aspect(1.12)
    ax.axis("off")
    ax.set_title("AFRICA - territorios actuales (cada pais un color) y culturas del temario",
                 fontsize=18, fontweight="bold", pad=14)

    handles = [Line2D([0], [0], marker="o", color="none",
                      markerfacecolor=REGION_COLORS[r], markersize=12,
                      markeredgecolor="white", label=REGION_NAMES[r])
               for r in ("O", "C", "E")]
    leg = ax.legend(handles=handles, loc="lower left", fontsize=11,
                    title="COLOR DEL PUNTO = REGION de la cultura",
                    title_fontsize=11, frameon=True,
                    framealpha=0.95, borderpad=1.0, labelspacing=0.7)
    leg.get_frame().set_edgecolor("#999999")

    plt.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.02)
    out = "/projects/sandbox/estudio-negritos/mapa_culturas_africa.png"
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor="white")
    print("guardado:", out)

if __name__ == "__main__":
    main()
