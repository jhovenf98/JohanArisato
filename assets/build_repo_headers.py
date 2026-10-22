"""Build the map-style header SVGs for each project repository.

    python assets/build_repo_headers.py <dir containing the project repos>

Writes assets/header.svg into who-gets-the-shade, housing-site-realization,
curbcall and geoai-for-cities. Shares its palette with build_visuals.py.
"""
import json
import random
import sys
from html import escape
from pathlib import Path

from shapely.geometry import shape

sys.path.insert(0, str(Path(__file__).parent))
from build_visuals import BG, CYAN, GRID, INK, MUTED, RAMP, path_d, projector, ramp  # noqa: E402

W, H = 1200, 340
SANS = "-apple-system,Segoe UI,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def frame(kicker, title_lines, finding_lines, status, status_color, right):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{SANS}">',
         f'<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>',
         '<defs><pattern id="g" width="24" height="24" patternUnits="userSpaceOnUse">'
         f'<circle cx="1" cy="1" r="1" fill="{GRID}"/></pattern></defs>',
         f'<rect width="{W}" height="{H}" rx="16" fill="url(#g)"/>',
         f'<text x="48" y="60" fill="{CYAN}" font-size="16" letter-spacing="3" font-family="{MONO}">{escape(kicker)}</text>']
    y = 112
    for line in title_lines:
        s.append(f'<text x="46" y="{y}" fill="{INK}" font-size="42" font-weight="700">{escape(line)}</text>')
        y += 48
    y += 6
    for line in finding_lines:
        s.append(f'<text x="48" y="{y}" fill="{INK}" font-size="21" opacity="0.88">{escape(line)}</text>')
        y += 29
    tw = len(status) * 10 + 28
    s.append(f'<rect x="48" y="{H-58}" width="{tw}" height="30" rx="15" fill="none" stroke="{status_color}" stroke-width="1.8"/>')
    s.append(f'<text x="{48 + tw/2}" y="{H-37}" fill="{status_color}" font-size="15" text-anchor="middle" font-family="{MONO}">{escape(status)}</text>')
    s.extend(right)
    s.append('</svg>')
    return "\n".join(s)


def nyc_right(geojson):
    feats = [(shape(f["geometry"]).simplify(0.0015, preserve_topology=True), f["properties"])
             for f in json.load(open(geojson))["features"]]
    b = (min(g.bounds[0] for g, _ in feats), min(g.bounds[1] for g, _ in feats),
         max(g.bounds[2] for g, _ in feats), max(g.bounds[3] for g, _ in feats))
    p = projector(b, 860, 24, 310, 292)
    lo = min(pr["heat_ed_rate"] for _, pr in feats); hi = max(pr["heat_ed_rate"] for _, pr in feats)
    out = ['<g stroke="#0a0f1a" stroke-width="1" stroke-linejoin="round">']
    for g, pr in feats:
        out.append(f'<path d="{path_d(g, p)}" fill="{ramp((pr["heat_ed_rate"] - lo) / (hi - lo))}"/>')
    out.append('</g>')
    for g, pr in feats:
        if pr.get("top10_share", 0) >= 0.9:
            out.append(f'<path d="{path_d(g, p)}" fill="none" stroke="{CYAN}" stroke-width="2.2">'
                       '<animate attributeName="stroke-opacity" values="1;0.2;1" dur="2.6s" repeatCount="indefinite"/></path>')
    return out


def sd_right(geojson):
    feats = json.load(open(geojson))["features"]
    random.seed(7)
    feats = random.sample(feats, 1400)
    pts = [(shape(f["geometry"]).centroid, f["properties"]["p_realized"]) for f in feats]
    b = (min(q.x for q, _ in pts), min(q.y for q, _ in pts), max(q.x for q, _ in pts), max(q.y for q, _ in pts))
    p = projector(b, 850, 30, 320, 280)
    out = []
    for q, pr in sorted(pts, key=lambda t: t[1]):
        x, y = p(q.x, q.y)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{ramp(min(pr / 0.6, 1))}"/>')
    out.append(f'<text x="1170" y="322" fill="{MUTED}" font-size="13" text-anchor="end">sites colored by predicted probability · synthetic sample</text>')
    out.append(f'<rect x="850" y="24" width="320" height="2" fill="{CYAN}" opacity="0.35">'
               '<animate attributeName="y" values="24;300;24" dur="8s" repeatCount="indefinite"/></rect>')
    return out


def stations_right(names, colors):
    out = []
    x0, x1, y = 840, 1150, 170
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{GRID}" stroke-width="10" stroke-linecap="round"/>')
    step = (x1 - x0) / (len(names) - 1)
    for i in range(len(names) - 1):
        out.append(f'<line x1="{x0 + i*step}" y1="{y}" x2="{x0 + (i+1)*step}" y2="{y}" stroke="{colors[i]}" stroke-width="10" stroke-linecap="round"/>')
    path = f"M{x0},{y} H{x1}"
    out.append(f'<circle r="7" fill="{INK}" stroke="{CYAN}" stroke-width="3">'
               f'<animateMotion dur="4s" repeatCount="indefinite" path="{path}"/></circle>')
    for i, n in enumerate(names):
        x = x0 + i * step
        out.append(f'<circle cx="{x}" cy="{y}" r="15" fill="{BG}" stroke="{colors[min(i, len(colors)-1)]}" stroke-width="6"/>')
        dy = -34 if i % 2 == 0 else 50
        out.append(f'<text x="{x}" y="{y+dy}" fill="{INK}" font-size="19" font-weight="700" text-anchor="middle">{escape(n)}</text>')
    return out


def main(root):
    root = Path(root)
    shade = root / "who-gets-the-shade"
    (shade / "assets").mkdir(exist_ok=True)
    (shade / "assets/header.svg").write_text(frame(
        "// WORKING PAPER · NYC · 42 NEIGHBORHOODS",
        ["Who Gets the Shade?"],
        ["Heat illness tracks poverty (r = 0.59), not heat.",
         "The ranking rule moves the poorest neighborhoods",
         "from 4 to 9 of the first 10 planted."],
        "LIVE · REAL DATA", "#3fb6b0", nyc_right(shade / "data/uhf42_shade_results.geojson")))

    hsr = root / "housing-site-realization"
    (hsr / "assets").mkdir(exist_ok=True)
    (hsr / "assets/header.svg").write_text(frame(
        "// SPATIAL ML · SAN DIEGO HOUSING ELEMENT",
        ["Will It Get Built?"],
        ["Which inventoried housing sites actually get built,",
         "and can a spatially validated model beat the",
         "city's capacity assumptions?"],
        "TESTING · SYNTHETIC DATA", "#f2c45a", sd_right(hsr / "outputs/sample/site_predictions.geojson")))

    cc = root / "curbcall"
    (cc / "assets").mkdir(exist_ok=True)
    (cc / "assets/header.svg").write_text(frame(
        "// CIVIC TECH PROTOTYPE · SAN DIEGO",
        ["CurbCall"],
        ["Snap it. Vote it. Get it fixed.",
         "If residents vote on what to fix first,",
         "whose problems get heard?"],
        "PROTOTYPE · NOT YET TESTED", "#e8534a",
        stations_right(["Snap", "Vote", "Rank", "Fix"], ["#e8534a", "#f2c45a", "#3fb6b0"])))

    gfc = root / "geoai-for-cities"
    (gfc / "assets").mkdir(exist_ok=True)
    (gfc / "assets/header.svg").write_text(frame(
        "// RESEARCH SITE · ARTICLE SERIES",
        ["GeoAI for Cities"],
        ["What GeoAI is, and who benefits when",
         "cities use it to rank and decide."],
        "ONGOING", CYAN,
        stations_right(["Define", "Measure", "Rank", "Decide"], ["#3fb6b0", "#f2c45a", "#e8534a"])))


if __name__ == "__main__":
    main(sys.argv[1])
