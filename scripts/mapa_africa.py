#!/usr/bin/env python3
"""Genera un mapa de Africa con las culturas del temario ubicadas geograficamente."""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from matplotlib.lines import Line2D

WORLD = "/tmp/world.geojson"

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

# (numero, nombre, pais, lon, lat, region)
# regiones: O=occidental, C=central, E=oriental/austral
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

REGION_COLORS = {"O": "#d35400", "C": "#1e8449", "E": "#6c3483"}
REGION_NAMES = {
    "O": "Africa OCCIDENTAL",
    "C": "Africa CENTRAL",
    "E": "Africa ORIENTAL / AUSTRAL",
}

def iter_polys(geom):
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            yield ring
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            for ring in poly:
                yield ring

def main():
    world = json.load(open(WORLD))
    fig, ax = plt.subplots(figsize=(17, 12))

    patches = []
    for feat in world["features"]:
        name = feat["properties"].get("name", "")
        if name not in AFRICA:
            continue
        for ring in iter_polys(feat["geometry"]):
            patches.append(MplPolygon(ring, closed=True))
    pc = PatchCollection(patches, facecolor="#f4ecd8", edgecolor="#8a8a8a",
                         linewidths=0.7, zorder=1)
    ax.add_collection(pc)

    # marcadores numerados
    for num, name, country, lon, lat, region in CULTURES:
        color = REGION_COLORS[region]
        ax.plot(lon, lat, "o", color=color, markersize=15,
                markeredgecolor="white", markeredgewidth=1.2, zorder=4)
        ax.text(lon, lat, str(num), color="white", fontsize=8.5,
                fontweight="bold", ha="center", va="center", zorder=5)

    ax.set_xlim(-22, 54)
    ax.set_ylim(-12, 26)   # foco en la franja subsahariana de las culturas
    ax.set_aspect(1.18)
    ax.axis("off")
    ax.set_title("ARTE DE LOS PUEBLOS PRIMITIVOS - Culturas africanas del temario",
                 fontsize=17, fontweight="bold", pad=14)

    # leyenda lateral agrupada por region
    x0 = 1.005
    y = 0.985
    fig.text(x0, y, "LEYENDA", fontsize=13, fontweight="bold",
             transform=ax.transAxes)
    y -= 0.045
    for region in ("O", "C", "E"):
        fig.text(x0, y, REGION_NAMES[region], fontsize=11, fontweight="bold",
                 color=REGION_COLORS[region], transform=ax.transAxes)
        y -= 0.034
        for num, name, country, lon, lat, r in CULTURES:
            if r != region:
                continue
            fig.text(x0 + 0.01, y, f"{num}. {name}  -  {country}",
                     fontsize=9.0, transform=ax.transAxes, va="top")
            y -= 0.0285
        y -= 0.012

    plt.subplots_adjust(left=0.01, right=0.70, top=0.93, bottom=0.02)
    out = "/projects/sandbox/estudio-negritos/mapa_culturas_africa.png"
    fig.savefig(out, dpi=160, bbox_inches="tight", facecolor="white")
    print("guardado:", out)

if __name__ == "__main__":
    main()
