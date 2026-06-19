#!/usr/bin/env python3
"""Genera un mapa de Africa con las culturas del temario ubicadas geograficamente,
coloreando los territorios (paises actuales) y mostrando su nombre."""
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

# GeoJSON de paises (propiedad "name" con nombres tipo "Ivory Coast").
WORLD = os.path.join(os.path.dirname(__file__), "world.geojson")
WORLD_URL = ("https://raw.githubusercontent.com/johan/world.geo.json/"
             "master/countries.geo.json")

def ensure_world():
    """Descarga el geojson de paises si no existe en local."""
    if not os.path.exists(WORLD):
        print("descargando geojson de paises...")
        urllib.request.urlretrieve(WORLD_URL, WORLD)

AFRICA = {
    "Algeria","Angola","Burundi","Benin","Burkina Faso","Botswana",
    "Central African Republic","Ivory Coast","Cameroon",
    "Democratic Republic of the Congo","Republic of the Congo","Djibouti",
    "Egypt","Eritrea","Ethiopia","Gabon","Ghana","Guinea","Gambia",
    "Guinea Bissau","Guinea-Bissau","Equatorial Guinea","Kenya","Liberia","Libya",
    "Lesotho","Morocco","Madagascar","Mali","Mozambique","Mauritania","Malawi",
    "Namibia","Niger","Nigeria","Rwanda","Western Sahara","Sudan","South Sudan",
    "Senegal","Sierra Leone","Somalia","Somaliland","Swaziland","Chad","Togo",
    "Tunisia","Tanzania","Uganda","South Africa","Zambia","Zimbabwe",
}

# Territorios (paises actuales) donde se encuentran las culturas del temario.
# geojson_name: (region, nombre_a_mostrar)
# regiones: O=occidental, C=central, E=oriental/austral
RELEVANT_COUNTRIES = {
    "Mali": ("O", "MALI"),
    "Ivory Coast": ("O", "COSTA DE MARFIL"),
    "Burkina Faso": ("O", "BURKINA FASO"),
    "Guinea Bissau": ("O", "GUINEA-BISAU"),
    "Guinea-Bissau": ("O", "GUINEA-BISAU"),
    "Sierra Leone": ("O", "SIERRA LEONA"),
    "Liberia": ("O", "LIBERIA"),
    "Ghana": ("O", "GHANA"),
    "Benin": ("O", "BENIN"),
    "Togo": ("O", "TOGO"),
    "Nigeria": ("O", "NIGERIA"),
    "Cameroon": ("C", "CAMERUN"),
    "Equatorial Guinea": ("C", "GUINEA ECUAT."),
    "Gabon": ("C", "GABON"),
    "Republic of the Congo": ("C", "R. DEL CONGO"),
    "Democratic Republic of the Congo": ("C", "RD DEL CONGO"),
    "Angola": ("C", "ANGOLA"),
    "Ethiopia": ("E", "ETIOPIA"),
    "Chad": ("E", "CHAD"),
}

# (numero, nombre, pais, lon, lat, region)
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

REGION_COLORS = {"O": "#b8470e", "C": "#0f6b35", "E": "#5b2470"}   # puntos / nombres cultura
NEUTRAL_FILL = "#f1ead8"                                            # resto de Africa
REGION_NAMES = {
    "O": "Africa OCCIDENTAL",
    "C": "Africa CENTRAL",
    "E": "Africa ORIENTAL / AUSTRAL",
}

def make_palette(n):
    """Genera n colores pastel bien diferenciados (tonos repartidos por el circulo)."""
    cols = []
    # alternamos el orden de los tonos para que paises vecinos no queden parecidos
    order = []
    step = max(1, n // 3)
    for start in range(step):
        order.extend(range(start, n, step))
    for rank, i in enumerate(order):
        h = i / n
        # variamos un poco luminosidad/saturacion segun la posicion para mas contraste
        light = 0.80 if rank % 2 == 0 else 0.72
        sat = 0.55 if rank % 2 == 0 else 0.62
        r, g, b = colorsys.hls_to_rgb(h, light, sat)
        cols.append("#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255)))
    return cols

# Cada TERRITORIO (pais actual) recibe un color de relleno distinto.
TERRITORIES = []
for _k, (_region, _label) in RELEVANT_COUNTRIES.items():
    if _label not in TERRITORIES:
        TERRITORIES.append(_label)
_palette = make_palette(len(TERRITORIES))
COUNTRY_FILL = {label: _palette[i] for i, label in enumerate(TERRITORIES)}

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
    fig, ax = plt.subplots(figsize=(17, 12))

    # --- relleno de paises: territorios relevantes coloreados por region ---
    for feat in world["features"]:
        name = feat["properties"].get("name", "")
        if name not in AFRICA:
            continue
        rel = RELEVANT_COUNTRIES.get(name)
        if rel:
            region, label = rel
            face = COUNTRY_FILL[label]
            edge = "#4a4a4a"
            lw = 0.9
            z = 2
        else:
            face, edge, lw, z = NEUTRAL_FILL, "#9a9a9a", 0.6, 1
        polys = [MplPolygon(r, closed=True) for r in iter_polys(feat["geometry"])]
        pc = PatchCollection(polys, facecolor=face, edgecolor=edge,
                             linewidths=lw, zorder=z)
        ax.add_collection(pc)

    # --- nombre del territorio (pais actual) sobre el mapa, como rotulo de fondo ---
    for feat in world["features"]:
        name = feat["properties"].get("name", "")
        rel = RELEVANT_COUNTRIES.get(name)
        if not rel:
            continue
        region, label = rel
        cx, cy = ring_centroid(largest_ring(feat["geometry"]))
        ax.text(cx, cy, label, color="#2b2b2b", fontsize=8.0, alpha=0.6,
                fontstyle="italic", fontweight="bold", ha="center", va="center",
                zorder=3,
                path_effects=[pe.withStroke(linewidth=2.0, foreground="white")])

    # --- marcadores (punto de color por region) + nombre de la cultura ---
    texts = []
    for num, name, country, lon, lat, region in CULTURES:
        color = REGION_COLORS[region]
        ax.plot(lon, lat, "o", color=color, markersize=8.5,
                markeredgecolor="white", markeredgewidth=1.0, zorder=5)
        t = ax.text(lon, lat, name, color=color, fontsize=8.4,
                    fontweight="bold", ha="center", va="center", zorder=7,
                    path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])
        texts.append(t)

    # reubica los nombres de cultura para que NO se solapen, con lineas guia finas
    adjust_text(
        texts, ax=ax,
        expand=(1.25, 1.6),
        force_text=(0.5, 0.8),
        arrowprops=dict(arrowstyle="-", color="#555555", lw=0.6, alpha=0.8),
    )

    ax.set_xlim(-22, 54)
    ax.set_ylim(-14, 27)
    ax.set_aspect(1.18)
    ax.axis("off")
    ax.set_title("ARTE DE LOS PUEBLOS PRIMITIVOS - Culturas africanas y territorios actuales",
                 fontsize=17, fontweight="bold", pad=14)

    # leyenda: el color del PUNTO/nombre indica la region; cada territorio tiene su color
    handles = [Line2D([0], [0], marker="o", color="none",
                      markerfacecolor=REGION_COLORS[r], markersize=12,
                      markeredgecolor="white",
                      label=REGION_NAMES[r])
               for r in ("O", "C", "E")]
    handles.append(Line2D([0], [0], marker="s", color="none",
                          markerfacecolor="#e9e9e9", markersize=14,
                          markeredgecolor="#4a4a4a",
                          label="cada territorio coloreado = pais actual"))
    leg = ax.legend(handles=handles, loc="lower left", fontsize=10.5,
                    title="COLOR DEL PUNTO = REGION  |  RELLENO = TERRITORIO",
                    title_fontsize=10.5, frameon=True,
                    framealpha=0.95, borderpad=1.0, labelspacing=0.8)
    leg.get_frame().set_edgecolor("#999999")

    plt.subplots_adjust(left=0.02, right=0.98, top=0.93, bottom=0.02)
    out = "/projects/sandbox/estudio-negritos/mapa_culturas_africa.png"
    fig.savefig(out, dpi=170, bbox_inches="tight", facecolor="white")
    print("guardado:", out)

if __name__ == "__main__":
    main()
