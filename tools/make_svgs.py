"""Generate the Domain Prime system diagram: hero + one highlighted variant per engine, light and dark.

Run from this checkout with the folder that holds all five checkouts:
    python tools/make_svgs.py ..
Writes <folder>/<repo>/docs/*.svg for domainprime and each engine.
"""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])

THEMES = {
    "light": dict(ink="#1f2328", quiet="#59636e", edge="#afb8c1", accent="#0969da",
                  ins="#e8590c", cf="#1a8f5c", env="#1d3f8f", bg="#ffffff"),
    "dark": dict(ink="#e6edf3", quiet="#9198a1", edge="#59636e", accent="#4493f8",
                 ins="#f0883e", cf="#3fb950", env="#79a7ff", bg="#0d1117"),
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

# focus: None (hero), 'insitu', 'cf', 'envoy', 'bf'
def build(t, focus=None):
    dim = 0.22
    def op(kind):
        return 1 if focus in (None, kind) else dim
    # tree outline fades only slightly when an engine is the focus
    tree_op = 1 if focus is None else 0.55
    o = []
    a = o.append
    W, H = 760, 452
    a(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
      f'font-family="{FONT}" font-size="13" role="img" aria-label="Domain Prime system diagram">')
    a('<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
      f'<path d="M0 0L10 5L0 10z" fill="{t["env"]}"/></marker></defs>')

    def rect(x, y, w, h, stroke, dash=False, tint=False, sw=1.25, opacity=1):
        fill = f'fill="{stroke}" fill-opacity="0.12"' if tint else 'fill="none"'
        d = ' stroke-dasharray="5 4"' if dash else ''
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" {fill} stroke="{stroke}" '
                f'stroke-width="{2 if tint else sw}"{d} opacity="{opacity}"/>')

    def text(x, y, s, size=13, weight=400, fill=None, anchor="middle", opacity=1):
        return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill or t["ink"]}" '
                f'text-anchor="{anchor}" opacity="{opacity}">{s}</text>')

    def dots(x2, y):
        return (f'<circle cx="{x2-28}" cy="{y+14}" r="4.5" fill="{t["ins"]}" opacity="{op("insitu")}"/>'
                f'<circle cx="{x2-14}" cy="{y+14}" r="4.5" fill="{t["cf"]}" opacity="{op("cf")}"/>')

    # tree structure
    a(f'<g fill="none" stroke="{t["edge"]}" stroke-width="1.25" opacity="{tree_op}">'
      '<path d="M380 88V110H190V132"/><path d="M380 110H640V132"/><path d="M430 110V132"/>'
      '<path d="M190 184V210H110V244"/><path d="M190 210H270V244"/><path d="M430 184V244"/></g>')
    # envoy routes
    env_w = 2.5 if focus == "envoy" else 1.75
    a(f'<g fill="none" stroke="{t["env"]}" stroke-width="{env_w}" stroke-dasharray="5 4" opacity="{op("envoy")}">'
      '<path d="M394 88V122"/><path d="M204 132V122H654V132"/><path d="M444 122V132"/>'
      '<path d="M204 184V226"/><path d="M124 244V226H284V244"/><path d="M444 184V244"/></g>')

    # Domain Prime (top nexus)
    a(rect(270, 24, 220, 64, t["accent"], tint=True, opacity=tree_op))
    a(dots(490, 24))
    a(text(380, 52, "Domain Prime", weight=600, opacity=tree_op))
    a(text(380, 72, "top nexus: see the whole system", size=11.5, opacity=tree_op))

    def node(x, y, w, name, kind, dash=False, extra_op=None):
        nop = tree_op if extra_op is None else extra_op
        cx = x + (w - 28) / 2
        a(rect(x, y, w, 52, t["edge"] if not (dash and focus == "bf") else t["accent"],
               dash=dash, sw=2 if (dash and focus == "bf") else 1.25, opacity=nop))
        a(dots(x + w, y))
        a(text(cx, y + 22, name, weight=600, opacity=nop))
        a(text(cx, y + 40, kind, size=11.5, fill=t["quiet"], opacity=nop))

    node(115, 132, 150, "Clients", "nexus, and a node")
    node(355, 132, 150, "Personal", "nexus, and a node")
    bf_op = 1 if focus in (None, "bf") else tree_op
    node(565, 132, 150, "Brain Forge", "optional vault node", dash=True, extra_op=bf_op)
    node(40, 244, 140, "Client A", "node")
    node(200, 244, 140, "Client B", "node")
    node(360, 244, 140, "Book draft", "node")

    # legend
    def legend(x, kind, color, name, line, mark):
        lop = op(kind)
        a(rect(x, 336, 224, 56, color, tint=True, opacity=lop))
        if mark == "dot":
            a(f'<circle cx="{x+16}" cy="{356}" r="4.5" fill="{color}" opacity="{lop}"/>')
            nx = x + 28
        else:
            a(f'<line x1="{x+12}" y1="356" x2="{x+24}" y2="356" stroke="{color}" stroke-width="2" '
              f'stroke-dasharray="4 3" opacity="{lop}"/>')
            nx = x + 32
        a(text(nx, 360, name, weight=600, anchor="start", opacity=lop))
        a(text(x + 16, 380, line, size=11.5, anchor="start", opacity=lop))

    legend(24, "insitu", t["ins"], "Insitu", "rules and skills, picked per chair", "dot")
    legend(268, "cf", t["cf"], "Context Forge", "session memory, kept per chair", "dot")
    legend(512, "envoy", t["env"], "Envoy", "mail and status, via each nexus", "line")

    a(text(380, 420, "Solid lines: the tree. Dashed: Envoy. Nodes never talk directly;", size=11.5, fill=t["quiet"]))
    a(text(380, 438, "a nexus passes mail on, and the top sees every chair.", size=11.5, fill=t["quiet"]))
    a('</svg>')
    return "\n".join(o)

targets = {
    None: ("domainprime/docs", "system"),
    "insitu": ("insitu/docs", "domain-prime"),
    "cf": ("context-forge/docs", "domain-prime"),
    "envoy": ("envoy/docs", "domain-prime"),
    "bf": ("brain-forge/docs", "domain-prime"),
}
for focus, (folder, stem) in targets.items():
    for theme, t in THEMES.items():
        p = OUT / folder / f"{stem}-{theme}.svg"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(build(t, focus))
        print(p)
