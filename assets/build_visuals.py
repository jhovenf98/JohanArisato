"""Build the map-style SVGs used in the profile README.

    python assets/build_visuals.py path/to/uhf42_shade.geojson

The banner draws NYC's 42 UHF neighborhoods from the real data in
who-gets-the-shade, colored by heat-related ER visit rate.
"""
import json
from html import escape
import math
import sys
from pathlib import Path

from shapely.geometry import shape

OUT = Path(__file__).parent
NAME = "Johan Fernandez"

BG = "#0a0f1a"
GRID = "#1b2a3d"
INK = "#e6edf3"
MUTED = "#7d8fa3"
CYAN = "#3fd0e0"
# Sequential ramp, low → high heat ER rate (deep teal → cyan → amber → coral)
RAMP = ["#123241", "#14546a", "#1a7f8e", "#3fb6b0", "#9bd38a", "#f2c45a", "#f28a4b", "#e8534a"]


def ramp(t):
    t = min(max(t, 0), 1) * (len(RAMP) - 1)
    return RAMP[int(round(t))]


def projector(bounds, x0, y0, w, h):
    minx, miny, maxx, maxy = bounds
    k = math.cos(math.radians((miny + maxy) / 2))
    sx = w / ((maxx - minx) * k)
    sy = h / (maxy - miny)
    s = min(sx, sy)
    ox = x0 + (w - (maxx - minx) * k * s) / 2
    oy = y0 + (h - (maxy - miny) * s) / 2

    def p(lon, lat):
        return ox + (lon - minx) * k * s, oy + (maxy - lat) * s

    return p


def path_d(geom, p):
    polys = [geom] if geom.geom_type == "Polygon" else list(geom.geoms)
    parts = []
    for poly in polys:
        for ring in [poly.exterior, *poly.interiors]:
            pts = [p(x, y) for x, y in ring.coords]
            parts.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    return "".join(parts)


def banner(geojson_path):
    g = json.load(open(geojson_path))
    feats = [(shape(f["geometry"]).simplify(0.0012, preserve_topology=True), f["properties"]) for f in g["features"]]
    rates = [pr["heat_ed_rate"] for _, pr in feats]
    lo, hi = min(rates), max(rates)
    minx = min(gm.bounds[0] for gm, _ in feats); miny = min(gm.bounds[1] for gm, _ in feats)
    maxx = max(gm.bounds[2] for gm, _ in feats); maxy = max(gm.bounds[3] for gm, _ in feats)
    W, H = 1200, 420
    p = projector((minx, miny, maxx, maxy), 640, 30, 520, 360)

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>',
         '<defs><pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
         f'<circle cx="1" cy="1" r="1" fill="{GRID}"/></pattern>'
         '<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#dots)"/>']

    # Graticule every 0.1°
    lon = math.ceil(minx * 10) / 10
    while lon <= maxx:
        x, _ = p(lon, miny)
        s.append(f'<line x1="{x:.1f}" y1="22" x2="{x:.1f}" y2="{H-22}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{x+3:.1f}" y="{H-26}" fill="{MUTED}" font-size="10">{abs(lon):.1f}°W</text>')
        lon = round(lon + 0.1, 2)
    lat = math.ceil(miny * 10) / 10
    while lat <= maxy:
        _, y = p(minx, lat)
        s.append(f'<line x1="610" y1="{y:.1f}" x2="{W-20}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        s.append(f'<text x="{W-70}" y="{y-4:.1f}" fill="{MUTED}" font-size="10">{lat:.1f}°N</text>')
        lat = round(lat + 0.1, 2)

    # Neighborhoods
    s.append('<g stroke="#0a0f1a" stroke-width="1.2" stroke-linejoin="round">')
    for gm, pr in feats:
        t = (pr["heat_ed_rate"] - lo) / (hi - lo)
        s.append(f'<path d="{path_d(gm, p)}" fill="{ramp(t)}"><title>{escape(pr["name"])}: {pr["heat_ed_rate"]:.1f} heat ER visits per 100k</title></path>')
    s.append('</g>')

    # Crosshair on the highest-rate neighborhood
    gm, pr = max(feats, key=lambda f: f[1]["heat_ed_rate"])
    cx, cy = p(*gm.representative_point().coords[0])
    s.append(f'<g stroke="{CYAN}" fill="none" filter="url(#glow)">'
             f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="9" stroke-width="1.5">'
             '<animate attributeName="r" values="7;15;7" dur="3s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values="1;0.2;1" dur="3s" repeatCount="indefinite"/></circle>'
             f'<line x1="{cx-22:.1f}" y1="{cy:.1f}" x2="{cx-12:.1f}" y2="{cy:.1f}" stroke-width="1.5"/>'
             f'<line x1="{cx+12:.1f}" y1="{cy:.1f}" x2="{cx+22:.1f}" y2="{cy:.1f}" stroke-width="1.5"/>'
             f'<line x1="{cx:.1f}" y1="{cy-22:.1f}" x2="{cx:.1f}" y2="{cy-12:.1f}" stroke-width="1.5"/>'
             f'<line x1="{cx:.1f}" y1="{cy+12:.1f}" x2="{cx:.1f}" y2="{cy+22:.1f}" stroke-width="1.5"/></g>')
    label = escape(pr["name"].replace("  ", " ").upper())
    tx, ty = 632, cy - 70
    s.append(f'<polyline points="{cx-10:.1f},{cy-10:.1f} {tx+120:.1f},{ty+12:.1f} {tx:.1f},{ty+12:.1f}" fill="none" stroke="{CYAN}" stroke-width="1"/>')
    s.append(f'<text x="{tx}" y="{ty-4:.1f}" fill="{CYAN}" font-size="15">{label}</text>')
    s.append(f'<text x="{tx}" y="{ty+32:.1f}" fill="{INK}" font-size="14">{pr["heat_ed_rate"]:.1f} heat ER visits / 100k</text>')

    # Scan line sweeping the map
    s.append(f'<rect x="610" y="22" width="{W-630}" height="2" fill="{CYAN}" opacity="0.35">'
             f'<animate attributeName="y" values="22;{H-24};22" dur="9s" repeatCount="indefinite"/></rect>')

    SANS = 'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif"'
    s.append(f'<text x="56" y="72" fill="{CYAN}" font-size="16" letter-spacing="3">// URBAN DATA SCIENCE · GEOAI</text>')
    s.append(f'<text x="52" y="140" fill="{INK}" font-size="60" font-weight="700" {SANS}>{NAME}</text>')
    s.append(f'<text x="56" y="186" fill="{INK}" font-size="24" {SANS}>Spatial ML for housing, heat and</text>')
    s.append(f'<text x="56" y="218" fill="{INK}" font-size="24" {SANS}>infrastructure: who gets what in cities?</text>')
    rows = [("ORIGIN", "San Diego, CA · 32.9°N 117.2°W"),
            ("TARGET", "New York, NY · 40.7°N 74.0°W"),
            ("STACK ", "Python · PostGIS · PySAL · ArcGIS")]
    for i, (k, v) in enumerate(rows):
        y = 266 + i * 28
        s.append(f'<text x="56" y="{y}" font-size="18"><tspan fill="{MUTED}">{k}</tspan><tspan fill="{INK}" x="150">{v}</tspan></text>')

    lx, ly = 56, 360
    for i, c in enumerate(RAMP):
        s.append(f'<rect x="{lx + i*20}" y="{ly}" width="20" height="10" fill="{c}"/>')
    s.append(f'<text x="{lx}" y="{ly+28}" fill="{MUTED}" font-size="13">{lo:.1f}</text>')
    s.append(f'<text x="{lx + len(RAMP)*20}" y="{ly+28}" fill="{MUTED}" font-size="13" text-anchor="end">{hi:.1f}</text>')
    s.append(f'<text x="{lx + len(RAMP)*20 + 14}" y="{ly+10}" fill="{MUTED}" font-size="13">heat ER visits per 100k · NYC UHF42</text>')
    s.append(f'<text x="{lx + len(RAMP)*20 + 14}" y="{ly+28}" fill="{MUTED}" font-size="13">NYC Environment &amp; Health Data Portal</text>')
    s.append('</svg>')
    (OUT / "banner.svg").write_text("\n".join(s))


def network():
    """Transit-map style diagram: data lines → database hub → project stations."""
    W, H = 900, 500
    SANS = '-apple-system,Segoe UI,Helvetica,Arial,sans-serif'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{SANS}">',
         f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>',
         '<defs><pattern id="d2" width="24" height="24" patternUnits="userSpaceOnUse">'
         f'<circle cx="1" cy="1" r="1" fill="{GRID}"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" rx="14" fill="url(#d2)"/>',
         f'<text x="36" y="48" fill="{CYAN}" font-size="17" letter-spacing="3" font-family="ui-monospace,Menlo,monospace">// SYSTEM MAP</text>']
    hx, hy = 400, 260
    rows = [  # color, source, project, detail, status, y
        ("#3fb6b0", "NYC health data", "Who Gets the Shade?", "ranking rules & equity", "LIVE · REAL DATA", 130),
        ("#f2c45a", "SD Housing Element", "Will It Get Built?", "housing realization", "TESTING · SYNTHETIC", 260),
        ("#e8534a", "Resident reports", "CurbCall", "whose problems get heard", "PROTOTYPE", 390),
    ]
    for color, src, proj, sub, status, y in rows:
        s.append(f'<path d="M50,{y} H150 C240,{y} 250,{hy} {hx-60},{hy}" stroke="{color}" stroke-width="9" fill="none" stroke-linecap="round"/>')
        s.append(f'<path d="M{hx+60},{hy} C{hx+150},{hy} {hx+160},{y} {hx+200},{y} H{hx+210}" stroke="{color}" stroke-width="9" fill="none" stroke-linecap="round"/>')
        s.append(f'<circle cx="50" cy="{y}" r="11" fill="{BG}" stroke="{color}" stroke-width="5"/>')
        s.append(f'<text x="36" y="{y-24}" fill="{INK}" font-size="18">{escape(src)}</text>')
        px = hx + 210
        s.append(f'<circle cx="{px}" cy="{y}" r="13" fill="{BG}" stroke="{color}" stroke-width="6"/>')
        s.append(f'<text x="{px+26}" y="{y-6}" fill="{INK}" font-size="22" font-weight="700">{escape(proj)}</text>')
        s.append(f'<text x="{px+26}" y="{y+18}" fill="{MUTED}" font-size="17">{escape(sub)}</text>')
        tw = len(status) * 9 + 20
        s.append(f'<rect x="{px+26}" y="{y+30}" width="{tw}" height="24" rx="12" fill="none" stroke="{color}" stroke-width="1.5"/>')
        s.append(f'<text x="{px+26+tw/2}" y="{y+47}" fill="{color}" font-size="13" text-anchor="middle" font-family="ui-monospace,Menlo,monospace">{status}</text>')
    s.append(f'<rect x="{hx-80}" y="{hy-40}" width="160" height="80" rx="40" fill="{BG}" stroke="{INK}" stroke-width="5"/>')
    s.append(f'<text x="{hx}" y="{hy-4}" fill="{INK}" font-size="17" font-weight="700" text-anchor="middle">geoai-cities-db</text>')
    s.append(f'<text x="{hx}" y="{hy+20}" fill="{MUTED}" font-size="14" text-anchor="middle">GeoPackage · PostGIS</text>')
    s.append(f'<text x="36" y="{H-28}" fill="{MUTED}" font-size="16">All three feed the GeoAI for Cities research site.</text>')
    s.append('</svg>')
    (OUT / "system_map.svg").write_text("\n".join(s))


if __name__ == "__main__":
    banner(sys.argv[1])
    network()
