#!/usr/bin/env python3
"""Draw the two charts on the Escape the Valley narrator results page.

Reads src/data/etv-narrator.json (numbers copied from the public rnd receipts) and
writes two static SVGs into public/results/. Standard library only.

    python public/site/scripts/etv_narrator_charts.py        (from the repo root)

Each SVG draws its own panel, so text and background always pair, in light or dark
mode: an <img> cannot inherit the page's colours, and a page theme that disagrees
with the OS setting would otherwise leave dark text on a dark page.
"""
import json
import os
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
DATA = os.path.join(SITE, "src", "data", "etv-narrator.json")
OUT = os.path.join(SITE, "public", "results")

STYLE = """<style>
  .bg{fill:#fafafa}.t{fill:#1f2328;font:14px system-ui,-apple-system,"Segoe UI",sans-serif}
  .h{font-size:16px;font-weight:600}.s{font-size:12px;fill:#59616b}
  .ax{stroke:#8b949e;stroke-width:1}.gr{stroke:#d0d7de;stroke-width:1}.zero{stroke:#1f2328;stroke-width:1.5;stroke-dasharray:5 3}
  .c1{fill:#2f7fd1;stroke:#2f7fd1}.c2{fill:#d98a1c}.c3{fill:#8a5cc2}
  @media (prefers-color-scheme:dark){
    .bg{fill:#16181d}.t{fill:#e6e9ee}.s{fill:#a3acb8}.ax{stroke:#7d8590}.gr{stroke:#2f353d}.zero{stroke:#e6e9ee}
    .c1{fill:#5aa2ee;stroke:#5aa2ee}.c2{fill:#eea443}.c3{fill:#a98ae0}}
</style>"""


def head(w, h, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{escape(title)}</title>'
            f'<desc id="d">{escape(desc)}</desc>{STYLE}<rect class="bg" width="{w}" height="{h}" rx="8"/>')


def text(x, y, s, cls="t", anchor="start", extra=""):
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'


def chart_cloud(d):
    rows = d["rows"]
    w, rowh, top, left, right = 760, 52, 74, 290, 30
    h = top + rowh * len(rows) + 78
    lo_ax, hi_ax = -4, 9
    pw = w - left - right

    def X(v):
        return left + (v - lo_ax) / (hi_ax - lo_ax) * pw

    title = "Local against cloud: paired difference in good lines"
    desc = "; ".join(f'{r["label"]}: {r["diff"]:+.1f} points (95% interval {r["lo"]:+.1f} to {r["hi"]:+.1f})' for r in rows)
    o = [head(w, h, title, desc), text(20, 28, title, "t h"),
         text(20, 48, "Points of good lines against the local 4B on the same turns. Right of zero: cloud better.", "s")]
    bottom = top + rowh * len(rows)
    for v in range(lo_ax, hi_ax + 1, 2):
        o.append(f'<line class="gr" x1="{X(v):.1f}" y1="{top-10}" x2="{X(v):.1f}" y2="{bottom}"/>')
        o.append(text(X(v), bottom + 20, f"{v:+d}" if v else "0", "t", "middle"))
    o.append(f'<line class="zero" x1="{X(0):.1f}" y1="{top-10}" x2="{X(0):.1f}" y2="{bottom}"/>')
    o.append(f'<line class="ax" x1="{left}" y1="{bottom}" x2="{w-right}" y2="{bottom}"/>')
    for i, r in enumerate(rows):
        cy = top + rowh * i + rowh / 2
        o.append(text(left - 14, cy + 5, r["label"], "t", "end"))
        o.append(f'<line class="c1" stroke-width="3" x1="{X(r["lo"]):.1f}" y1="{cy:.1f}" x2="{X(r["hi"]):.1f}" y2="{cy:.1f}"/>')
        for e in (r["lo"], r["hi"]):
            o.append(f'<line class="c1" stroke-width="3" x1="{X(e):.1f}" y1="{cy-6:.1f}" x2="{X(e):.1f}" y2="{cy+6:.1f}"/>')
        o.append(f'<circle class="c1" cx="{X(r["diff"]):.1f}" cy="{cy:.1f}" r="6"/>')
        o.append(text(X(r["hi"]) + 8, cy - 9, f'{r["diff"]:+.1f}', "t", "start", 'style="font-size:12px"'))
    o.append(text(left + pw / 2, bottom + 42, "Paired difference, percentage points (dot) with 95% interval (whiskers)", "t", "middle"))
    o.append(text(20, h - 12, "Source: rnd experiments/etv-narrator/cloud-claude/RUN-RECORD.md; results/s4-says-what-happened/RESCORE-checker2-2026-11-13.md", "s"))
    o.append("</svg>")
    return "\n".join(o)


def chart_speed(d):
    rows = d["rows"]
    w, h, top, left, right, bottom_pad = 760, 420, 74, 70, 30, 110
    ph = h - top - bottom_pad
    ymax = 14

    def Y(v):
        return top + ph - v / ymax * ph

    pw = w - left - right
    gw = pw / len(rows)
    bw = 34
    series = [("brief", "Brief", "c1"), ("standard", "Standard", "c2"), ("rich", "Rich", "c3")]
    title = "Speed by hardware: seconds per turn (p50)"
    desc = "; ".join(f'{r["placement"]}: Brief {r["brief"]:.2f}, Standard {r["standard"]:.2f}, Rich {r["rich"]:.2f}' for r in rows)
    o = [head(w, h, title, desc), text(20, 28, title, "t h"),
         text(20, 48, "Local 4B model, Fireside voice. Lower is faster.", "s")]
    for v in range(0, ymax + 1, 2):
        o.append(f'<line class="gr" x1="{left}" y1="{Y(v):.1f}" x2="{w-right}" y2="{Y(v):.1f}"/>')
        o.append(text(left - 8, Y(v) + 4, str(v), "t", "end"))
    o.append(f'<line class="ax" x1="{left}" y1="{Y(0):.1f}" x2="{w-right}" y2="{Y(0):.1f}"/>')
    o.append(text(18, top + ph / 2, "Seconds per turn (p50)", "t", "middle", f'transform="rotate(-90 18 {top+ph/2:.1f})"'))
    for gi, r in enumerate(rows):
        gx = left + gi * gw + gw / 2
        for si, (key, _, cls) in enumerate(series):
            bx = gx + (si - 1) * (bw + 4) - bw / 2
            v = r[key]
            o.append(f'<rect class="{cls}" x="{bx:.1f}" y="{Y(v):.1f}" width="{bw}" height="{Y(0)-Y(v):.1f}" rx="2"/>')
            lab = f"{v:.2f}" if v < 1 else f"{v:.1f}"
            o.append(text(bx + bw / 2, Y(v) - 5, lab, "t", "middle", 'style="font-size:12px"'))
        o.append(text(gx, Y(0) + 22, r["placement"], "t", "middle"))
    lx = left
    for key, name, cls in series:
        o.append(f'<rect class="{cls}" x="{lx}" y="{h-58}" width="14" height="14" rx="2"/>')
        o.append(text(lx + 20, h - 46, name))
        lx += 110
    o.append(text(20, h - 12, "Source: rnd experiments/etv-narrator/results/s4-says-what-happened/RUN-RECORD.md (latency with fewer layers on the GPU)", "s"))
    o.append("</svg>")
    return "\n".join(o)


def main():
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    os.makedirs(OUT, exist_ok=True)
    for name, svg in (("etv-narrator-local-vs-cloud.svg", chart_cloud(data["local_vs_cloud"])),
                      ("etv-narrator-speed-by-hardware.svg", chart_speed(data["speed_by_hardware"]))):
        with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(svg + "\n")
        print("wrote", name)


if __name__ == "__main__":
    main()
