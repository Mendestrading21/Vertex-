"""vertex.ui.pages.widget_lab — /widget-lab : LABORATOIRE du Design System.

Route AUTONOME, hors produit Vertex : elle ne rend AUCUNE donnée réelle et
n'appelle AUCUN moteur. Toutes les valeurs sont des ÉCHANTILLONS de design,
clairement étiquetés, servant à voir / comparer / tester / choisir les widgets
de la bibliothèque (`docs/visual/VERTEX_WIDGET_LIBRARY.md`).

Chaque widget est présenté en variantes (V1…Vn) + bande d'états. L'utilisateur
marque chaque variante Officiel / Référence / Rejeté (persisté localStorage), et
peut exporter ses choix. La Widget Library est la seule source de vérité du DS.
"""
from __future__ import annotations

import math

# ── Échantillons de design (JAMAIS des données réelles) ───────────────────
SPARK_UP = [41, 43, 42, 46, 49, 47, 52, 50, 55, 58, 57, 60, 62, 59, 63, 66, 64, 68]
SPARK_DN = [66, 63, 64, 60, 57, 58, 54, 52, 49, 47, 48, 45, 43, 46, 42, 40, 41, 39]
MOM = [4.2, 9.3, 9.2, 6.5]           # 1S / 1M / 1T / 1A (%)
SECTORS = [('Software', 48, 1.3), ('Big Tech', 37, -0.3), ('Semiconducteurs', 31, -1.6),
           ('Énergie', 44, 0.8), ('Santé', 28, -0.6), ('Finance', 40, 0.4)]


# ── Utilitaires SVG ────────────────────────────────────────────────────────
def _pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def _arc(cx, cy, r, d0, d1):
    x0, y0 = _pol(cx, cy, r, d0)
    x1, y1 = _pol(cx, cy, r, d1)
    large = 1 if abs(d1 - d0) > 180 else 0
    return f'M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f}'


_gid = [0]


def _uid():
    _gid[0] += 1
    return 'wl' + str(_gid[0])


# ══ FORMES SIGNATURE ═══════════════════════════════════════════════════════

def aura(name, conf, tone='go', size=170):
    """S-form AURA — halo radial (régime), température = état, anneau = confiance."""
    col = {'go': 'var(--vx-positive)', 'risk': 'var(--vx-negative)',
           'wait': 'var(--vx-warning)', 'off': 'var(--vx-text-muted)'}[tone]
    uid = _uid()
    cx = cy = size / 2
    r = size / 2 - 14
    a0, a1 = 130, 130 + max(2, conf / 100 * 280)
    ring = _arc(cx, cy, r, a0, a1)
    track = _arc(cx, cy, r, 130, 410)
    return f'''<div class="wl-aura" style="width:{size}px;height:{size}px">
  <svg viewBox="0 0 {size} {size}" width="{size}" height="{size}">
    <defs><radialGradient id="{uid}" cx="50%" cy="46%" r="55%">
      <stop offset="0" stop-color="{col}" stop-opacity=".55"/>
      <stop offset="55%" stop-color="{col}" stop-opacity=".12"/>
      <stop offset="100%" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>
    <circle cx="{cx}" cy="{cy}" r="{r-2}" fill="url(#{uid})"/>
    <path d="{track}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="3" stroke-linecap="round"/>
    <path d="{ring}" fill="none" stroke="var(--vx-ember-500)" stroke-width="3" stroke-linecap="round"/>
  </svg>
  <div class="wl-aura-txt"><span class="n">{name}</span><span class="c">{conf}% confiance</span></div>
</div>'''


def comb(vals, size=132, mirror=False, show_vals=False):
    """S-form COMB — peigne momentum multi-horizon."""
    labels = ['1S', '1M', '1T', '1A']
    mx = max(6, max(abs(v) for v in vals))
    bars = ''
    for lab, v in zip(labels, vals):
        h = max(12, abs(v) / mx * 100)
        col = 'var(--vx-positive)' if v >= 0 else 'var(--vx-negative)'
        val = f'<b>{v:+.1f}</b>' if show_vals else ''
        if mirror:
            up = h / 2 if v >= 0 else 0
            dn = h / 2 if v < 0 else 0
            bar = (f'<span class="up" style="height:{up:.0f}%;background:{col}"></span>'
                   f'<span class="dn" style="height:{dn:.0f}%;background:{col}"></span>')
            bars += f'<span class="wl-comb-b wl-comb-b--m">{val}{bar}<span class="l">{lab}</span></span>'
        else:
            bars += (f'<span class="wl-comb-b">{val}<span class="i" style="height:{h:.0f}%;'
                     f'background:{col}"></span><span class="l">{lab}</span></span>')
    return f'<div class="wl-comb{" wl-comb--m" if mirror else ""}" style="width:{size}px">{bars}</div>'


def sparkline(vals, tone='up', h=44, w=150, dot=True):
    """S-form SPARKLINE+ — ligne + aire dégradée + point actif."""
    mn, mx = min(vals), max(vals)
    rng = (mx - mn) or 1
    uid = _uid()
    pad = 3
    xs = [i / (len(vals) - 1) * w for i in range(len(vals))]
    ys = [h - pad - (v - mn) / rng * (h - 2 * pad) for v in vals]
    line = ' '.join(f'{x:.1f},{y:.1f}' for x, y in zip(xs, ys))
    area = f'0,{h} ' + line + f' {w},{h}'
    col = {'up': 'var(--vx-positive)', 'down': 'var(--vx-negative)',
           'tech': 'var(--vx-technical)', 'brand': 'var(--vx-ember-500)'}[tone]
    d = (f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="2.6" fill="{col}"/>' if dot else '')
    return f'''<svg class="wl-spark" viewBox="0 0 {w} {h}" width="{w}" height="{h}" preserveAspectRatio="none">
  <defs><linearGradient id="{uid}" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{col}" stop-opacity=".30"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>
  <polygon points="{area}" fill="url(#{uid})"/>
  <polyline points="{line}" fill="none" stroke="{col}" stroke-width="1.9" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>{d}</svg>'''


def dial(val, mx=100, label='', reading='', unit='%', bands=None, size=150):
    """S-form DIAL — jauge semi-circulaire à bandes sémantiques."""
    bands = bands or [(40, 'var(--vx-negative)'), (70, 'var(--vx-warning)'), (100, 'var(--vx-positive)')]
    cx, cy, r = size / 2, size * 0.62, size / 2 - 16
    segs = ''
    prev = 0
    for to, col in bands:
        a0 = 180 + prev / mx * 180
        a1 = 180 + to / mx * 180
        segs += f'<path d="{_arc(cx,cy,r,a0,a1)}" fill="none" stroke="{col}" stroke-opacity=".24" stroke-width="9"/>'
        prev = to
    va = 180 + min(val, mx) / mx * 180
    valcol = next(c for t, c in bands if val <= t) if val <= bands[-1][0] else bands[-1][1]
    nx, ny = _pol(cx, cy, r, va)
    return f'''<svg class="wl-dial" viewBox="0 0 {size} {size*0.75:.0f}" width="{size}" height="{size*0.75:.0f}">
  {segs}
  <path d="{_arc(cx,cy,r,180,va)}" fill="none" stroke="{valcol}" stroke-width="9" stroke-linecap="round"/>
  <circle cx="{nx:.1f}" cy="{ny:.1f}" r="4.5" fill="var(--vx-ember-500)"/>
  <text x="{cx}" y="{cy-16}" text-anchor="middle" fill="var(--vx-text-primary)" font-size="26" font-weight="800" style="font-variant-numeric:tabular-nums">{val:g}{unit}</text>
  <text x="{cx}" y="{cy+2}" text-anchor="middle" fill="var(--vx-text-muted)" font-size="10" letter-spacing=".4">{label}</text>
</svg>{f'<div class="wl-dial-read">{reading}</div>' if reading else ''}'''


def rail(pct, left='', mid='', right='', tone='seq'):
    """S-form RAIL — position sur un axe borné, marqueur ember."""
    pct = max(0, min(100, pct))
    fill = ('linear-gradient(90deg,var(--vx-positive),var(--vx-warning),var(--vx-negative))'
            if tone == 'stress' else 'linear-gradient(90deg,var(--vx-negative),var(--vx-warm-depth),var(--vx-positive))')
    return f'''<div class="wl-rail-wrap">
  <div class="wl-rail"><span class="fill" style="background:{fill}"></span><span class="mark" style="left:{pct:.0f}%"></span></div>
  <div class="wl-rail-sc"><span>{left}</span><span>{mid}</span><span>{right}</span></div></div>'''


def ring(val, mx=100, unit='%', sub=''):
    """S-form RING — métrique bornée compacte."""
    r, c = 34, 2 * math.pi * 34
    off = c * (1 - min(val, mx) / mx)
    col = 'var(--vx-positive)' if val >= 55 else 'var(--vx-warning)' if val >= 45 else 'var(--vx-negative)'
    return f'''<svg class="wl-ring" viewBox="0 0 84 84" width="84" height="84">
  <circle cx="42" cy="42" r="{r}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="7"/>
  <circle cx="42" cy="42" r="{r}" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"
    stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90 42 42)"/>
  <text x="42" y="40" text-anchor="middle" fill="var(--vx-text-primary)" font-size="18" font-weight="800" style="font-variant-numeric:tabular-nums">{val:g}{unit}</text>
  <text x="42" y="55" text-anchor="middle" fill="var(--vx-text-muted)" font-size="8">{sub}</text></svg>'''


def spine(pct, label=''):
    """S-form SPINE — conviction verticale qui se remplit (ember)."""
    pct = max(0, min(100, pct))
    return f'''<div class="wl-spine"><div class="col"><i style="height:{pct:.0f}%"></i></div>
  <div class="wl-spine-l"><b>{pct:g}</b><span>{label}</span></div></div>'''


def thermocline(vix, h=150):
    """S-form THERMOCLINE — volatilité = profondeur (calme haut → stress bas)."""
    depth = max(0, min(100, (vix - 10) / 30 * 100))
    return f'''<div class="wl-thermo" style="height:{h}px">
  <div class="col"><span class="mark" style="top:{depth:.0f}%"></span></div>
  <div class="wl-thermo-sc"><span>10</span><span>25</span><span>40+</span></div>
  <div class="wl-thermo-v">{vix:g}<small>VIX</small></div></div>'''


def tide(pct):
    """S-form TIDE — participation = marée montante/descendante."""
    lvl = max(0, min(100, pct))
    top = 100 - lvl
    col = 'var(--vx-positive)' if pct >= 55 else 'var(--vx-warning)' if pct >= 45 else 'var(--vx-negative)'
    uid = _uid()
    return f'''<svg class="wl-tide" viewBox="0 0 120 100" width="120" height="100" preserveAspectRatio="none">
  <defs><linearGradient id="{uid}" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{col}" stop-opacity=".42"/><stop offset="1" stop-color="{col}" stop-opacity=".08"/></linearGradient></defs>
  <path d="M0,{top} Q30,{top-6} 60,{top} T120,{top} L120,100 L0,100 Z" fill="url(#{uid})"/>
  <path d="M0,{top} Q30,{top-6} 60,{top} T120,{top}" fill="none" stroke="{col}" stroke-width="2"/>
  <line x1="0" y1="45" x2="120" y2="45" stroke="rgba(255,255,255,.18)" stroke-dasharray="3 3" stroke-width="1"/>
  <text x="60" y="{min(top-6,90):.0f}" text-anchor="middle" fill="var(--vx-text-primary)" font-size="15" font-weight="800">{pct:g}%</text></svg>'''


def reactor(score, contribs):
    """S-form REACTOR — composition pondérée (cœur + barres contributrices)."""
    core_col = 'var(--vx-ember-500)' if score >= 55 else 'var(--vx-warning)'
    bars = ''
    for lab, val, w in contribs:
        pc = max(6, min(100, val))
        bars += (f'<div class="wl-reactor-row"><span class="k">{lab}<small>{w}%</small></span>'
                 f'<span class="bar"><i style="width:{pc:.0f}%"></i></span><span class="v">{val:g}</span></div>')
    return f'''<div class="wl-reactor">
  <div class="core" style="--c:{core_col}"><b>{score:g}</b><span>santé</span></div>
  <div class="rods">{bars}</div></div>'''


def ledge(pts, best_i=0):
    """S-form LEDGE — scatter qualité×timing à corniche gagnante + labels directs."""
    W, H = 260, 180
    dots = ''
    labs = ''
    for i, (sym, x, y, tone) in enumerate(pts):
        px = 20 + x / 100 * (W - 30)
        py = H - 22 - y / 100 * (H - 40)
        col = {'buy': 'var(--vx-positive)', 'avoid': 'var(--vx-negative)',
               'neutral': 'var(--vx-warm-grey)'}[tone]
        if i == best_i:
            col = 'var(--vx-ember-500)'
        dots += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{6 if i==best_i else 5}" fill="{col}" stroke="rgba(255,255,255,.2)"/>'
        if x >= 55 and y >= 55:
            labs += f'<text x="{px+8:.1f}" y="{py-6:.1f}" fill="{"var(--vx-ember-400)" if i==best_i else "rgba(248,245,243,.9)"}" font-size="10" font-weight="700">{sym}</text>'
    xc = 20 + 55 / 100 * (W - 30)
    yc = H - 22 - 55 / 100 * (H - 40)
    return f'''<svg class="wl-ledge" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect x="{xc:.0f}" y="14" width="{W-xc-6:.0f}" height="{yc-14:.0f}" fill="rgba(255,109,41,.05)"/>
  <line x1="{xc:.1f}" y1="14" x2="{xc:.1f}" y2="{H-20}" stroke="rgba(255,255,255,.12)" stroke-dasharray="4 4"/>
  <line x1="16" y1="{yc:.1f}" x2="{W-6}" y2="{yc:.1f}" stroke="rgba(255,255,255,.12)" stroke-dasharray="4 4"/>
  <text x="{W-8}" y="26" text-anchor="end" fill="rgba(255,255,255,.3)" font-size="9" font-weight="700">À ÉTUDIER</text>
  <text x="18" y="{H-8}" fill="rgba(255,255,255,.3)" font-size="9" font-weight="700">À ÉVITER</text>
  {dots}{labs}
  <text x="{W/2}" y="{H-4}" text-anchor="middle" fill="var(--vx-text-muted)" font-size="9">qualité →</text></svg>'''


def orbit(items):
    """S-form ORBIT — rotation sectorielle à queue de comète."""
    W, H = 260, 180
    body = ''
    for sym, x, y, tone in items:
        px = 20 + x / 100 * (W - 30)
        py = H - 22 - (y + 3) / 6 * (H - 40)
        py = max(16, min(H - 22, py))
        col = {'lead': 'var(--vx-positive)', 'lag': 'var(--vx-negative)', 'mid': 'var(--vx-warm-grey)'}[tone]
        tx, ty = px - 14, py + 8
        body += (f'<line x1="{tx:.1f}" y1="{ty:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="{col}" stroke-opacity=".4" stroke-width="2"/>'
                 f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{col}"/>'
                 f'<text x="{px+7:.1f}" y="{py+3:.1f}" fill="rgba(248,245,243,.85)" font-size="9">{sym}</text>')
    return f'''<svg class="wl-ledge" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <line x1="{W/2}" y1="14" x2="{W/2}" y2="{H-20}" stroke="rgba(255,255,255,.1)" stroke-dasharray="4 4"/>
  <line x1="16" y1="{H/2-4}" x2="{W-6}" y2="{H/2-4}" stroke="rgba(255,255,255,.1)" stroke-dasharray="4 4"/>
  <text x="{W-8}" y="24" text-anchor="end" fill="rgba(255,255,255,.28)" font-size="8" font-weight="700">LEADING</text>
  <text x="18" y="{H-8}" fill="rgba(255,255,255,.28)" font-size="8" font-weight="700">LAGGING</text>
  {body}</svg>'''


# ══ WIDGETS COMPOSÉS (HTML) ════════════════════════════════════════════════

def kpi(label, val, delta, tone='up', spark=None):
    dc = {'up': 'pos', 'down': 'neg', 'flat': 'mut'}[tone]
    sp = f'<div class="wl-kpi-spark">{sparkline(spark, tone if tone != "flat" else "tech", 34, 130)}</div>' if spark else ''
    return f'''<div class="wl-kpi"><span class="l">{label}</span><span class="v">{val}</span>
  <span class="d {dc}">{delta}</span>{sp}</div>'''


def grade_seal(g):
    hot = g in ('S+', 'S')
    return f'<span class="wl-grade{" hot" if hot else ""}">{g}</span>'


def live_pill(state='live'):
    lab = {'live': 'Live', 'delayed': 'Différé', 'frozen': 'Figé', 'fallback': 'Démo'}[state]
    return f'<span class="wl-live" data-live="{state}"><span class="dot"></span>{lab}</span>'


def slab(verdict, tone, lines):
    kv = ''.join(f'<div class="kv"><span>{k}</span><b>{v}</b></div>' for k, v in lines)
    return f'''<div class="wl-slab"><div class="wl-slab-v" data-tone="{tone}">{verdict}</div>{kv}</div>'''


def dominant(sym, grade, sub, score, metrics):
    ms = ''.join(f'<div class="m{" hot" if hot else ""}"><span>{k}</span><b>{v}</b></div>'
                 for k, v, hot in metrics)
    return f'''<div class="wl-dom">
  <div class="wl-dom-l"><span class="badge">Opportunité dominante</span>
    <div class="tk"><span class="sym">{sym}</span>{grade_seal(grade)}</div>
    <div class="sub">{sub}</div><div class="score"><b>{score}</b><span>/100</span></div>
    {comb(MOM, 120)}</div>
  <div class="wl-dom-r"><div class="grid">{ms}</div>
    <button class="wl-cta">Ouvrir le dossier {sym} →</button></div></div>'''


def comparison(rows):
    head = '<tr><th>Critère</th><th class="best">ACN ★</th><th>AFL</th><th>AOS</th></tr>'
    body = ''
    for name, vals, mx in rows:
        best = max(vals)
        cells = ''
        for i, v in enumerate(vals):
            win = v == best
            w = max(6, v / mx * 100)
            cells += (f'<td><span class="cmp {"win" if win else ""}"><span class="rail">'
                      f'<i style="width:{w:.0f}%"></i></span><span class="n">{v:g}</span></span></td>')
        body += f'<tr><td class="mt">{name}</td>{cells}</tr>'
    return f'<table class="wl-cmp"><thead>{head}</thead><tbody>{body}</tbody></table>'


def funnel(stages):
    top = max(s[1] for s in stages)
    W = 200
    rows = ''
    for i, (lab, val) in enumerate(stages):
        w0 = 26 + (W - 26) * val / top
        nxt = stages[i + 1][1] if i + 1 < len(stages) else val * 0.86
        w1 = 26 + (W - 26) * nxt / top
        col = 'var(--vx-positive)' if i == len(stages) - 1 else 'var(--vx-warm-grey)'
        y = i * 32
        rows += (f'<polygon points="{(W-w0)/2:.0f},{y} {(W+w0)/2:.0f},{y} {(W+w1)/2:.0f},{y+26} {(W-w1)/2:.0f},{y+26}" fill="{col}" fill-opacity=".8"/>'
                 f'<text x="{W/2}" y="{y+17}" text-anchor="middle" fill="#161316" font-size="12" font-weight="800">{val}</text>'
                 f'<text x="6" y="{y+17}" fill="var(--vx-text-secondary)" font-size="10">{lab}</text>')
    return f'<svg viewBox="0 0 {W} {len(stages)*32}" width="100%" style="max-width:240px">{rows}</svg>'


# ══ FORMES SIGNATURE — ART DIRECTION 02 ════════════════════════════════════
# Palettes locales (l'orange reste réservé à l'identité/interaction/point actif).
_EM = 'var(--vx-positive)'
_RB = 'var(--vx-negative)'
_AM = 'var(--vx-warning)'
_VI = 'var(--vx-option)'
_CY = 'var(--vx-technical)'
_GY = 'var(--vx-warm-grey)'
_LIME = '#B6F04A'
_MAG = '#F06AC4'


def horizon_band(tone, name, phase):
    """HORIZON BAND — régime comme un horizon à changement de phase."""
    col = {'go': _EM, 'risk': _RB, 'wait': _AM, 'off': _GY}[tone]
    uid = _uid()
    return f'''<div style="width:220px"><svg viewBox="0 0 220 110" width="220" height="110">
  <defs><linearGradient id="{uid}" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{col}" stop-opacity=".32"/><stop offset="60%" stop-color="{col}" stop-opacity=".06"/>
    <stop offset="100%" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>
  <rect width="220" height="66" fill="url(#{uid})"/>
  <circle cx="168" cy="52" r="16" fill="{col}" opacity=".85" class="wl-glow" style="--wl-acc:{col}"/>
  <line x1="0" y1="66" x2="220" y2="66" stroke="{col}" stroke-width="1.5" opacity=".6"/>
  <line x1="0" y1="66" x2="220" y2="66" stroke="var(--vx-ember-500)" stroke-width="0" />
  <path d="M0,66 Q55,60 110,66 T220,66 L220,110 L0,110 Z" fill="rgba(0,0,0,.25)"/>
  <text x="12" y="26" fill="var(--vx-text-primary)" font-size="15" font-weight="800">{name}</text>
  <text x="12" y="88" fill="var(--vx-text-muted)" font-size="10">{phase}</text></svg></div>'''


def pressure_field(name, tone, conf):
    """PRESSURE FIELD — carte thermodynamique (iso-barres de pression)."""
    col = {'go': _EM, 'risk': _RB, 'wait': _AM, 'off': _GY}[tone]
    rings = ''.join(f'<circle cx="90" cy="82" r="{18+i*13}" fill="none" stroke="{col}" '
                    f'stroke-opacity="{0.35-i*0.045:.2f}" stroke-width="{2.2-i*0.15:.1f}"/>' for i in range(6))
    return f'''<div style="width:180px"><svg viewBox="0 0 180 150" width="180" height="150">
  {rings}
  <circle cx="90" cy="82" r="7" fill="{col}" class="wl-glow" style="--wl-acc:{col}"/>
  <text x="90" y="20" text-anchor="middle" fill="var(--vx-text-primary)" font-size="13" font-weight="800">{name}</text>
  <text x="90" y="142" text-anchor="middle" fill="var(--vx-text-muted)" font-size="9.5">pression {conf}% · haute={_ptone(tone)}</text></svg></div>'''


def _ptone(t):
    return {'go': 'porteur', 'risk': 'défensif', 'wait': 'transition', 'off': 'indéterminé'}[t]


def regime_capsule(name, tone, tension):
    """REGIME CAPSULE — pilule compacte à tension latérale."""
    col = {'go': _EM, 'risk': _RB, 'wait': _AM, 'off': _GY}[tone]
    return f'''<div style="display:flex;align-items:center;gap:12px;width:230px">
  <div style="flex:1;padding:10px 14px;border-radius:999px;background:rgba(0,0,0,.3);border:1px solid var(--vx-border-soft)">
    <div style="font-size:15px;font-weight:800;color:{col}">{name}</div>
    <div style="font-size:10px;color:var(--vx-text-muted)">régime · tension {tension}%</div></div>
  <div style="width:8px;height:56px;border-radius:5px;background:rgba(0,0,0,.35);overflow:hidden;display:flex;align-items:flex-end">
    <i style="display:block;width:100%;height:{tension}%;background:{col}"></i></div></div>'''


def signal_bloom(strength, tone):
    """SIGNAL BLOOM / OPPORTUNITY BEACON — floraison radiale de pétales."""
    col = {'go': _EM, 'brand': 'var(--vx-ember-500)', 'opt': _VI}[tone]
    n = 12
    petals = ''
    for i in range(n):
        a = i / n * 360
        ln = 18 + strength / 100 * 34
        x1, y1 = _pol(75, 75, 14, a)
        x2, y2 = _pol(75, 75, 14 + ln, a)
        op = 0.35 + 0.5 * (i % 3 == 0)
        petals += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="2.4" stroke-linecap="round"/>'
    return f'''<div style="width:150px"><svg viewBox="0 0 150 150" width="150" height="150">
  {petals}<circle cx="75" cy="75" r="10" fill="{col}" class="wl-glow" style="--wl-acc:{col}"/>
  <text x="75" y="79" text-anchor="middle" fill="#161316" font-size="11" font-weight="800">{strength}</text></svg>
  <div style="text-align:center;font-size:10px;color:var(--vx-text-muted);margin-top:2px">force du signal</div></div>'''


def risk_crater(level):
    """RISK CRATER — cratère : anneaux qui s'enfoncent vers un cœur rubis."""
    rings = ''.join(f'<ellipse cx="80" cy="{40+i*7}" rx="{70-i*11}" ry="{20-i*3}" fill="none" '
                    f'stroke="{_RB}" stroke-opacity="{0.18+i*0.13:.2f}" stroke-width="1.6"/>' for i in range(5))
    return f'''<div style="width:170px"><svg viewBox="0 0 160 120" width="160" height="120">
  {rings}<ellipse cx="80" cy="75" rx="16" ry="6" fill="{_RB}" class="wl-glow" style="--wl-acc:{_RB}"/>
  <text x="80" y="16" text-anchor="middle" fill="var(--vx-text-primary)" font-size="13" font-weight="800">Risque {level}</text>
  <text x="80" y="112" text-anchor="middle" fill="var(--vx-text-muted)" font-size="9.5">profondeur = sévérité</text></svg></div>'''


def momentum_ribs(vals):
    """MOMENTUM RIBS — cage thoracique : côtes courbes par horizon."""
    labels = ['1S', '1M', '1T', '1A']
    mx = max(6, max(abs(v) for v in vals))
    ribs = ''
    for i, (lab, v) in enumerate(zip(labels, vals)):
        y = 22 + i * 22
        w = 30 + abs(v) / mx * 90
        col = _LIME if v >= 0 else _RB
        ribs += (f'<path d="M20,{y} Q{20+w/2},{y-12} {20+w},{y}" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" opacity=".9"/>'
                 f'<text x="6" y="{y+3}" fill="var(--vx-text-muted)" font-size="9">{lab}</text>'
                 f'<text x="{24+w}" y="{y+3}" fill="var(--vx-text-secondary)" font-size="9" style="font-variant-numeric:tabular-nums">{v:+.1f}</text>')
    return f'<div style="width:200px"><svg viewBox="0 0 200 116" width="200" height="116"><line x1="20" y1="10" x2="20" y2="106" stroke="var(--vx-ember-500)" stroke-width="2" opacity=".7"/>{ribs}</svg></div>'


def conviction_pillar(pct):
    """CONVICTION PILLAR — pilier segmenté (distinct du Spine plein)."""
    segs = 10
    filled = round(pct / 100 * segs)
    cells = ''.join(f'<div style="height:9px;border-radius:2px;background:{"linear-gradient(90deg,var(--vx-ember-500),var(--vx-ember-400))" if i < filled else "rgba(255,255,255,.06)"}"></div>'
                    for i in range(segs - 1, -1, -1))
    return f'''<div style="display:flex;align-items:flex-end;gap:12px">
  <div style="display:flex;flex-direction:column;gap:3px;width:30px">{cells}</div>
  <div style="display:flex;flex-direction:column;justify-content:flex-end"><b style="font-size:26px;font-weight:850;font-variant-numeric:tabular-nums">{pct}</b>
    <span style="font-size:10px;color:var(--vx-text-muted)">conviction</span></div></div>'''


def vol_rift(vol):
    """VOLATILITY RIFT — faille/fissure dont l'ouverture = volatilité."""
    w = 6 + vol / 40 * 30
    col = _VI if vol < 20 else _RB
    return f'''<div style="width:150px"><svg viewBox="0 0 150 130" width="150" height="130">
  <path d="M75,6 L{75-w/2:.0f},40 L{75+w/3:.0f},66 L{75-w/2.2:.0f},96 L75,124" fill="none" stroke="{col}" stroke-width="2.5" class="wl-glow" style="--wl-acc:{col}"/>
  <path d="M75,6 L{75+w/2:.0f},40 L{75-w/3:.0f},66 L{75+w/2.2:.0f},96 L75,124" fill="none" stroke="{col}" stroke-width="2.5" opacity=".7"/>
  <text x="75" y="70" text-anchor="middle" fill="var(--vx-text-primary)" font-size="16" font-weight="800" style="font-variant-numeric:tabular-nums">{vol:g}</text></svg>
  <div style="text-align:center;font-size:10px;color:var(--vx-text-muted)">faille de volatilité</div></div>'''


def countdown_ring(dte, total=30, label='Résultats'):
    """CATALYST COUNTDOWN RING — anneau de compte à rebours vers l'événement."""
    r, c = 32, 2 * math.pi * 32
    off = c * (dte / total)
    col = _RB if dte <= 3 else _AM if dte <= 10 else _CY
    return f'''<div style="width:120px;text-align:center"><svg viewBox="0 0 80 80" width="96" height="96">
  <circle cx="40" cy="40" r="{r}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="6"/>
  <circle cx="40" cy="40" r="{r}" fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"
    stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90 40 40)"/>
  <text x="40" y="38" text-anchor="middle" fill="var(--vx-text-primary)" font-size="19" font-weight="800">J-{dte}</text>
  <text x="40" y="52" text-anchor="middle" fill="var(--vx-text-muted)" font-size="8">{label}</text></svg></div>'''


def drawdown_canyon(series):
    """DRAWDOWN CANYON — profil de creux « sous l'eau »."""
    w, h = 200, 90
    mx = min(series)
    pts = ' '.join(f'{i/(len(series)-1)*w:.1f},{-v/mx*(h-10):.1f}' for i, v in enumerate(series))
    area = f'0,0 {pts} {w},0'
    return f'''<div style="width:{w}px"><svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <line x1="0" y1="1" x2="{w}" y2="1" stroke="rgba(255,255,255,.2)" stroke-dasharray="3 3"/>
  <polygon points="{area}" fill="{_RB}" fill-opacity=".16"/>
  <polyline points="{pts}" fill="none" stroke="{_RB}" stroke-width="1.8"/>
  <text x="4" y="{h-6}" fill="var(--vx-text-muted)" font-size="9">creux max {mx:g}%</text></svg></div>'''


def constellation(points):
    """PORTFOLIO CONSTELLATION — positions = étoiles reliées, taille = poids."""
    w, h = 220, 130
    stars = ''
    links = ''
    for i, (sym, x, y, r, pl) in enumerate(points):
        px, py = 12 + x / 100 * (w - 24), 12 + y / 100 * (h - 24)
        col = _EM if pl >= 0 else _RB
        if i:
            ppx, ppy = 12 + points[i - 1][1] / 100 * (w - 24), 12 + points[i - 1][2] / 100 * (h - 24)
            links += f'<line x1="{ppx:.1f}" y1="{ppy:.1f}" x2="{px:.1f}" y2="{py:.1f}" stroke="rgba(231,226,218,.18)" stroke-width="1"/>'
        stars += (f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r}" fill="{col}" fill-opacity=".85"/>'
                  f'<text x="{px+r+3:.1f}" y="{py+3:.1f}" fill="rgba(231,226,218,.8)" font-size="8.5">{sym}</text>')
    return f'<div style="width:{w}px"><svg viewBox="0 0 {w} {h}" width="{w}" height="{h}">{links}{stars}</svg></div>'


def greek_field():
    """GREEK VECTOR FIELD — champ de flèches (delta/gamma/theta/vega)."""
    W, H = 200, 120
    arr = ''
    import math as _m
    for gx in range(5):
        for gy in range(3):
            cx, cy = 24 + gx * 40, 22 + gy * 34
            ang = (gx - 2) * 22 + (gy - 1) * 14
            ex, ey = cx + 13 * _m.cos(_m.radians(ang)), cy + 13 * _m.sin(_m.radians(ang))
            col = _VI if gy != 1 else _RB
            arr += f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{col}" stroke-width="1.8" stroke-opacity=".7"/><circle cx="{ex:.1f}" cy="{ey:.1f}" r="1.6" fill="{col}"/>'
    return f'<div style="width:{W}px"><svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">{arr}<text x="6" y="{H-4}" fill="var(--vx-text-muted)" font-size="9">Δ Γ Θ ν — champ de sensibilité</text></svg></div>'


def payoff_terrain():
    """PAYOFF TERRAIN — payoff comme relief (perte corail / gain émeraude)."""
    W, H = 220, 110
    be = 130
    return f'''<div style="width:{W}px"><svg viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs><linearGradient id="pl" x1="0" x2="1"><stop offset="0" stop-color="{_RB}" stop-opacity=".22"/><stop offset="1" stop-color="{_RB}" stop-opacity="0"/></linearGradient>
    <linearGradient id="pg" x1="0" x2="1"><stop offset="0" stop-color="{_EM}" stop-opacity="0"/><stop offset="1" stop-color="{_EM}" stop-opacity=".28"/></linearGradient></defs>
  <rect x="0" y="55" width="{be}" height="{H-55}" fill="url(#pl)"/><rect x="{be}" y="0" width="{W-be}" height="{H}" fill="url(#pg)"/>
  <polyline points="0,80 {be},80 {W},18" fill="none" stroke="var(--vx-text-primary)" stroke-width="2"/>
  <line x1="{be}" y1="0" x2="{be}" y2="{H}" stroke="var(--vx-ember-500)" stroke-width="1.5" stroke-dasharray="3 3"/>
  <text x="{be+4}" y="14" fill="var(--vx-ember-400)" font-size="9">breakeven</text>
  <text x="6" y="{H-6}" fill="{_RB}" font-size="9">perte max</text>
  <text x="{W-6}" y="30" text-anchor="end" fill="{_EM}" font-size="9">gain</text></svg></div>'''


def thesis_pulse(state):
    """THESIS PULSE — battement ECG de la thèse (intacte/surveiller/invalidée)."""
    col = {'ok': _EM, 'watch': _AM, 'ko': _RB}[state]
    path = ('M0,30 L40,30 L48,30 L54,10 L60,50 L66,30 L90,30 L96,22 L102,38 L108,30 L200,30'
            if state != 'ko' else 'M0,30 L60,30 L68,12 L76,48 L84,30 L120,30 L200,30')
    lab = {'ok': 'thèse intacte', 'watch': 'à surveiller', 'ko': 'invalidée — plate'}[state]
    return f'''<div style="width:210px"><svg viewBox="0 0 200 60" width="200" height="60">
  <path d="{path}" fill="none" stroke="{col}" stroke-width="2" class="wl-glow" style="--wl-acc:{col}"/>
  </svg><div style="font-size:10px;color:{col};text-align:center">{lab}</div></div>'''


def confidence_lens(conf):
    """CONFIDENCE LENS — diaphragme dont l'ouverture = confiance."""
    open_r = 8 + conf / 100 * 26
    blades = ''.join(f'<line x1="46" y1="46" x2="{_pol(46,46,40,i*60)[0]:.1f}" y2="{_pol(46,46,40,i*60)[1]:.1f}" stroke="rgba(255,255,255,.1)" stroke-width="6"/>' for i in range(6))
    return f'''<div style="width:110px;text-align:center"><svg viewBox="0 0 92 92" width="100" height="100">
  <circle cx="46" cy="46" r="40" fill="none" stroke="var(--vx-border-strong)" stroke-width="2"/>{blades}
  <circle cx="46" cy="46" r="{open_r:.0f}" fill="var(--vx-ember-soft)" stroke="var(--vx-ember-500)" stroke-width="2"/>
  <text x="46" y="50" text-anchor="middle" fill="var(--vx-text-primary)" font-size="15" font-weight="800">{conf}%</text></svg>
  <div style="font-size:9.5px;color:var(--vx-text-muted)">confiance</div></div>'''


def weather_tile(cond, icon, metric, sub, tone):
    """MARKET WEATHER TILE — tuile météo de marché (Apple-like)."""
    col = {'go': _EM, 'risk': _RB, 'wait': _AM, 'off': _GY}[tone]
    return f'''<div style="width:150px;padding:14px;border-radius:14px;background:radial-gradient(120% 90% at 80% 0%,{col}22,transparent 60%),rgba(0,0,0,.2)">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <span style="font-size:11px;color:var(--vx-text-secondary)">{cond}</span><span style="font-size:22px">{icon}</span></div>
  <div style="font-size:30px;font-weight:800;color:var(--vx-text-primary);font-variant-numeric:tabular-nums;margin-top:6px">{metric}</div>
  <div style="font-size:10px;color:{col}">{sub}</div></div>'''


def scenario_triad():
    """SCENARIO TRIAD — 3 volets proportionnels à la probabilité."""
    return f'''<div style="display:flex;gap:6px;width:280px">
  <div style="flex:1;padding:9px;border-radius:10px;background:rgba(255,95,105,.1);border:1px solid rgba(255,95,105,.25)">
    <div style="font-size:9px;color:{_RB}">PESSIMISTE</div><b style="font-size:16px;color:{_RB}">−12 %</b><div style="font-size:9px;color:var(--vx-text-muted)">p≈20 %</div></div>
  <div style="flex:1.6;padding:9px;border-radius:10px;background:rgba(255,109,41,.08);border:1px solid var(--vx-border-strong)">
    <div style="font-size:9px;color:var(--vx-ember-400)">PROBABLE</div><b style="font-size:18px">+8 %</b><div style="font-size:9px;color:var(--vx-text-muted)">p≈55 %</div></div>
  <div style="flex:1;padding:9px;border-radius:10px;background:rgba(46,214,161,.1);border:1px solid rgba(46,214,161,.25)">
    <div style="font-size:9px;color:{_EM}">EXCEPTIONNEL</div><b style="font-size:16px;color:{_EM}">+34 %</b><div style="font-size:9px;color:var(--vx-text-muted)">p≈25 %</div></div></div>'''


def score_decomp(parts):
    """SCORE DECOMPOSITION — barre empilée des sous-scores."""
    tot = sum(p[1] for p in parts)
    segs = ''.join(f'<div class="wl-tip" data-tip="{k} {v}" style="width:{v/tot*100:.0f}%;background:{c}"></div>' for k, v, c in parts)
    leg = ' '.join(f'<span style="font-size:9.5px;color:var(--vx-text-muted)"><i style="display:inline-block;width:8px;height:8px;border-radius:2px;background:{c};margin-right:3px"></i>{k}</span>' for k, v, c in parts)
    return f'''<div style="width:220px"><div style="font-size:24px;font-weight:850;font-variant-numeric:tabular-nums">{tot}<span style="font-size:12px;color:var(--vx-text-muted)">/40</span></div>
  <div style="display:flex;height:12px;border-radius:6px;overflow:hidden;margin:8px 0;gap:1px">{segs}</div>
  <div style="display:flex;gap:8px;flex-wrap:wrap">{leg}</div></div>'''


def committee(votes):
    """COMMITTEE CONSENSUS — accord/désaccord des membres."""
    dots = ''.join(f'<span class="wl-tip" data-tip="{n}" style="width:16px;height:16px;border-radius:50%;display:inline-grid;place-items:center;font-size:9px;background:{_EM if v=="+" else _RB if v=="-" else _GY};color:#161316;font-weight:800">{v}</span>' for n, v in votes)
    agree = sum(1 for _, v in votes if v == '+')
    return f'''<div style="width:200px"><div style="font-size:13px;font-weight:750;margin-bottom:8px">Consensus {agree}/{len(votes)} <span style="color:var(--vx-text-muted);font-size:11px">favorable</span></div>
  <div style="display:flex;gap:5px">{dots}</div></div>'''


def concentration_tower(weights):
    """CONCENTRATION TOWER — tour empilée par poids (HHI)."""
    cells = ''.join(f'<div class="wl-tip" data-tip="{k} {v}%" style="height:{v*1.6:.0f}px;background:{c};border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:9px;color:#161316;font-weight:700">{v}%</div>' for k, v, c in weights)
    return f'''<div style="display:flex;align-items:flex-end;gap:14px">
  <div style="display:flex;flex-direction:column-reverse;gap:2px;width:52px">{cells}</div>
  <div><b style="font-size:20px">HHI 0,31</b><div style="font-size:10px;color:{_AM}">concentration modérée</div></div></div>'''


def bias_heatmap():
    """BIAS HEATMAP — carte des biais récurrents (jour × type)."""
    import itertools
    vals = [2, 0, 1, 3, 0, 1, 0, 2, 1, 0, 0, 1, 3, 1, 0, 2, 0, 1, 0, 1]
    cells = ''
    it = iter(vals)
    for r in range(4):
        for c in range(5):
            v = next(it)
            col = f'rgba(255,109,41,{0.08+v*0.22:.2f})' if v else 'rgba(255,255,255,.04)'
            cells += f'<div class="wl-tip" data-tip="{v} occurrence(s)" style="width:20px;height:20px;border-radius:4px;background:{col}"></div>'
    return f'<div style="width:130px"><div style="display:grid;grid-template-columns:repeat(5,20px);gap:4px">{cells}</div><div style="font-size:9px;color:var(--vx-text-muted);margin-top:6px">biais × jour · foncé = récurrent</div></div>'


def freshness_matrix(sources):
    """SOURCE FRESHNESS MATRIX — grille d'états de fraîcheur des sources."""
    rows = ''
    for name, state in sources:
        col = {'live': _EM, 'delayed': _AM, 'frozen': _GY, 'off': _RB}[state]
        rows += f'<div style="display:flex;align-items:center;gap:8px;font-size:11px"><span style="width:8px;height:8px;border-radius:50%;background:{col}"></span><span style="flex:1;color:var(--vx-text-secondary)">{name}</span><span style="color:var(--vx-text-muted);font-size:10px">{state}</span></div>'
    return f'<div style="width:180px;display:flex;flex-direction:column;gap:7px">{rows}</div>'


def engine_spine(engines):
    """ENGINE STATUS SPINE — colonne des moteurs (santé)."""
    rows = ''
    for name, ok in engines:
        col = _EM if ok else _RB
        rows += f'<div style="display:flex;align-items:center;gap:8px"><span style="width:3px;height:22px;border-radius:2px;background:{col}"></span><span style="flex:1;font-size:11.5px">{name}</span><span style="font-size:10px;color:{col}">{"OK" if ok else "ERR"}</span></div>'
    return f'<div style="width:180px;display:flex;flex-direction:column;gap:6px">{rows}</div>'


def readonly_seal():
    """READONLY SEAL — sceau de garantie lecture seule."""
    return f'''<div style="width:120px;text-align:center"><svg viewBox="0 0 100 100" width="96" height="96">
  <circle cx="50" cy="50" r="42" fill="none" stroke="var(--vx-ember-500)" stroke-width="2.5"/>
  <circle cx="50" cy="50" r="34" fill="rgba(255,109,41,.06)" stroke="var(--vx-ember-500)" stroke-width="1" stroke-dasharray="2 3"/>
  <text x="50" y="46" text-anchor="middle" fill="var(--vx-ember-400)" font-size="13" font-weight="850">READ</text>
  <text x="50" y="62" text-anchor="middle" fill="var(--vx-ember-400)" font-size="13" font-weight="850">ONLY</text></svg>
  <div style="font-size:9.5px;color:var(--vx-text-muted)">aucun ordre possible</div></div>'''


def data_reactor(score):
    """DATA INTEGRITY REACTOR — cœur de fiabilité + barres de qualité."""
    return reactor(score, [('IBKR', 90 if score > 50 else 0, 40), ('Scan', 82, 30), ('IA', 70, 20), ('Cache', 60, 10)])


def progress_ladder(levels):
    """PROGRESS LADDER — échelons de progression (Journal)."""
    rows = ''
    for i, w in enumerate(levels):
        col = _AM if i < 3 else _GY
        rows += (f'<div style="display:flex;align-items:center;gap:8px">'
                 f'<span style="width:20px;font-size:9px;color:var(--vx-text-muted)">N{i+1}</span>'
                 f'<span style="flex:1;height:7px;border-radius:4px;background:rgba(0,0,0,.35);overflow:hidden">'
                 f'<i style="display:block;height:100%;width:{w}%;background:{col}"></i></span></div>')
    return f'<div style="display:flex;flex-direction:column-reverse;gap:4px;width:170px">{rows}</div>'


# ══ GRAMMAIRE BOURSIÈRE — briques financières natives ══════════════════════
def _foot(source='scan', fresh='il y a 12 s', mode='delayed'):
    """Pied financier universel : source · fraîcheur · mode (honnêteté §7)."""
    dot = {'live': _EM, 'delayed': _AM, 'demo': 'var(--vx-ember-500)'}[mode]
    return (f'<div style="display:flex;align-items:center;gap:6px;margin-top:8px;font-size:9.5px;color:var(--vx-text-faint)">'
            f'<span style="width:6px;height:6px;border-radius:50%;background:{dot}"></span>{source} · {fresh}</div>')


def _concl(text, tone='go'):
    """Conclusion de trading (couple Verdict+Preuve §8)."""
    col = {'go': _EM, 'risk': _RB, 'wait': _AM, 'opt': _VI, 'neutral': _GY}[tone]
    return f'<div style="margin-top:8px;font-size:11px;font-weight:650;color:{col}">▸ {text}</div>'


def _hdr(name, price=None, chg=None):
    """En-tête financier : nom + prix + variation (niveau 1)."""
    ch = ''
    if chg is not None:
        c = _EM if chg >= 0 else _RB
        ch = f'<span style="font-size:12px;font-weight:700;color:{c};font-variant-numeric:tabular-nums">{chg:+.2f}%</span>'
    pr = f'<span style="font-size:16px;font-weight:800;color:#F0EBE4;font-variant-numeric:tabular-nums">{price}</span>' if price else ''
    return (f'<div style="display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:8px">'
            f'<span style="font-size:12px;font-weight:650;color:var(--vx-text-secondary)">{name}</span>'
            f'<span style="display:flex;gap:8px;align-items:baseline">{pr}{ch}</span></div>')


# Échantillon OHLC (design) : ~22 séances haussières avec un gap.
OHLC = [(100, 103, 99, 102, 40), (102, 104, 100, 101, 38), (101, 102, 97, 98, 55),
        (98, 100, 96, 99, 48), (99, 103, 98, 103, 60), (103, 106, 102, 105, 52),
        (105, 107, 103, 104, 44), (104, 105, 100, 101, 58), (101, 104, 100, 103, 50),
        (103, 108, 103, 107, 72), (110, 113, 109, 112, 95), (112, 114, 110, 111, 60),
        (111, 113, 108, 109, 54), (109, 112, 108, 112, 66), (112, 116, 111, 115, 78),
        (115, 118, 114, 117, 70), (117, 119, 115, 116, 50), (116, 120, 115, 119, 82),
        (119, 122, 118, 121, 76), (121, 123, 119, 120, 58), (120, 124, 119, 123, 84),
        (123, 126, 122, 125, 90)]


def candles(data=OHLC, entry=118, stop=108, target=132, resistance=126,
            ma=(5, 10), event_idx=10, gap_idx=10, w=280, h=140, compact=False,
            name='NVDA', question='Le prix confirme-t-il la cassure ?'):
    """CANDLESTICK SNAPSHOT — chandeliers compacts : corps/mèches + volume + MM +
    niveaux entrée/stop/objectif/résistance + gap + événement + bougie active."""
    highs = [d[1] for d in data]
    lows = [d[2] for d in data]
    closes = [d[3] for d in data]
    vols = [d[4] for d in data]
    lv = [x for x in (entry, stop, target, resistance) if x is not None]
    mn = min(lows + lv)
    mx = max(highs + lv)
    rng = (mx - mn) or 1
    volH = 0 if compact else 26
    pH = h - volH - 6
    n = len(data)
    cw = (w - 6) / n
    bw = cw * 0.62
    def Y(v):
        return 4 + pH - (v - mn) / rng * (pH - 8)
    body = ''
    # gap highlight
    if gap_idx and not compact:
        gx = 3 + gap_idx * cw
        body += f'<rect x="{gx-cw:.1f}" y="4" width="{cw:.1f}" height="{pH}" fill="rgba(255,200,87,.06)"/>'
    for i, (o, hi, lo, c, v) in enumerate(data):
        x = 3 + i * cw + cw / 2
        col = _EM if c >= o else _RB
        active = i == n - 1
        body += f'<line x1="{x:.1f}" y1="{Y(hi):.1f}" x2="{x:.1f}" y2="{Y(lo):.1f}" stroke="{col}" stroke-width="1"/>'
        yb, yt = Y(min(o, c)), Y(max(o, c))
        outline = 'stroke="var(--vx-ember-500)" stroke-width="1"' if active else ''
        body += (f'<rect x="{x-bw/2:.1f}" y="{yt:.1f}" width="{bw:.1f}" height="{max(1,yb-yt):.1f}" '
                 f'fill="{col}" {outline} rx="0.5"/>')
        if volH:
            vy = h - v / max(vols) * (volH - 4)
            body += f'<rect x="{x-bw/2:.1f}" y="{vy:.1f}" width="{bw:.1f}" height="{h-vy:.1f}" fill="{col}" fill-opacity=".28"/>'
    # MM
    for period, mc in zip(ma, (_CY, _AM)):
        pts = []
        for i in range(n):
            if i + 1 >= period:
                seg = closes[i + 1 - period:i + 1]
                pts.append(f'{3+i*cw+cw/2:.1f},{Y(sum(seg)/period):.1f}')
        if pts:
            body += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{mc}" stroke-width="1.2" stroke-opacity=".8"/>'
    # niveaux
    def hline(val, col, lab):
        y = Y(val)
        return (f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}" stroke="{col}" stroke-width="1" stroke-dasharray="4 3" stroke-opacity=".7"/>'
                f'<text x="{w-2}" y="{y-2:.1f}" text-anchor="end" fill="{col}" font-size="8">{lab} {val:g}</text>')
    lvl = ''
    if not compact:
        if entry: lvl += hline(entry, 'var(--vx-ember-500)', 'entrée')
        if stop: lvl += hline(stop, _RB, 'stop')
        if target: lvl += hline(target, _EM, 'objectif')
        if resistance: lvl += hline(resistance, _AM, 'R')
    ev = ''
    if event_idx is not None and not compact:
        ex = 3 + event_idx * cw + cw / 2
        ev = f'<path d="M{ex-4:.1f},{h-volH-3:.1f} L{ex+4:.1f},{h-volH-3:.1f} L{ex:.1f},{h-volH-9:.1f} Z" fill="{_VI}"/>'
    last = closes[-1]
    chg = (last / closes[-2] - 1) * 100
    svg = f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}" style="max-width:{w}px">{body}{lvl}{ev}</svg>'
    if compact:
        return f'<div style="width:{w}px">{_hdr(name, f"{last:g}", chg)}{svg}</div>'
    tgt = f'objectif +{(target-last)/last*100:.1f}%' if target else 'objectif n/d'
    stp = f'stop −{(last-stop)/last*100:.1f}%' if stop else 'stop n/d'
    more = (f'<div class="wl-more">MM5/MM10 · volume {vols[-1]} · gap J-{n-1-gap_idx if gap_idx else "—"} · '
            f'{tgt} · {stp}</div>')
    if resistance and stop:
        concl = _concl('Cassure confirmée au-dessus de ' + str(resistance) + ' — entrée valide, invalidation ' + str(stop), 'go')
    else:
        concl = _concl(f'Tendance haussière — {n} clôtures au-dessus de la MM10', 'go')
    return (f'<div style="width:{w}px">{_hdr(name+" · "+str(n)+" séances", f"{last:g}", chg)}{svg}'
            f'{concl}{more}{_foot("scan · clôtures", "il y a 3 min", "delayed")}</div>')


def price_ladder(price=119.2, entry=118, stop=108, targets=(126, 132), resistance=126):
    """PRICE LADDER — échelle de prix : niveaux + distances en %."""
    lv = sorted([('Objectif 2', targets[1], _EM), ('Objectif 1', targets[0], _EM),
                 ('Résistance', resistance, _AM), ('Prix', price, 'var(--vx-ember-500)'),
                 ('Entrée', entry, 'var(--vx-ember-400)'), ('Stop', stop, _RB)],
                key=lambda x: -x[1])
    rows = ''
    for lab, val, col in lv:
        d = (val - price) / price * 100
        cur = 'font-weight:800;background:rgba(255,109,41,.1)' if lab == 'Prix' else ''
        rows += (f'<div class="wl-tip" data-tip="{lab} {val:g} ({d:+.1f}%)" style="display:flex;align-items:center;gap:8px;padding:3px 6px;border-radius:5px;{cur}">'
                 f'<span style="width:8px;height:8px;border-radius:2px;background:{col}"></span>'
                 f'<span style="flex:1;font-size:11px;color:var(--vx-text-secondary)">{lab}</span>'
                 f'<span style="font-size:12px;font-weight:700;color:#F0EBE4;font-variant-numeric:tabular-nums">{val:g}</span>'
                 f'<span style="width:52px;text-align:right;font-size:10px;color:{"var(--vx-text-muted)" if lab=="Prix" else col};font-variant-numeric:tabular-nums">{d:+.1f}%</span></div>')
    return (f'<div style="width:220px">{rows}'
            f'{_concl("R:R "+f"{(targets[0]-entry)/(entry-stop):.1f}"+" — asymétrie favorable", "go")}</div>')


def market_tape(items):
    """MARKET TAPE — bandeau de flux : tickers · variation · volume."""
    cells = ''
    for sym, chg, vol in items:
        col = _EM if chg >= 0 else _RB
        cells += (f'<span style="display:inline-flex;align-items:center;gap:5px;padding:0 12px;border-right:1px solid var(--vx-border-soft)">'
                  f'<b style="font-size:12px;color:var(--vx-ember-400)">{sym}</b>'
                  f'<span style="font-size:11px;color:{col};font-variant-numeric:tabular-nums">{chg:+.1f}%</span>'
                  f'<span style="font-size:9px;color:var(--vx-text-faint)">{vol}</span></span>')
    return (f'<div style="width:260px;overflow:hidden"><div style="display:flex;white-space:nowrap;animation:wltape 18s linear infinite">{cells}{cells}</div></div>'
            f'<style>@keyframes wltape{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}@media(prefers-reduced-motion:reduce){{[style*=wltape]{{animation:none!important}}}}</style>')


def orderflow_ribbon(buy=62, sell=38):
    """ORDER-FLOW RIBBON — pression acheteurs/vendeurs + déséquilibre."""
    imb = buy - sell
    dom = 'acheteurs' if imb > 0 else 'vendeurs'
    return (f'<div style="width:230px">{_hdr("Pression d’ordres")}'
            f'<div style="display:flex;height:16px;border-radius:5px;overflow:hidden">'
            f'<div class="wl-tip" data-tip="Acheteurs {buy}%" style="width:{buy}%;background:{_EM};display:flex;align-items:center;justify-content:flex-start;padding-left:6px;font-size:9px;color:#0a0a0a;font-weight:700">{buy}%</div>'
            f'<div class="wl-tip" data-tip="Vendeurs {sell}%" style="width:{sell}%;background:{_RB};display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font-size:9px;color:#0a0a0a;font-weight:700">{sell}%</div></div>'
            f'{_concl(f"Déséquilibre +{imb} — dominance {dom}", "go" if imb>0 else "risk")}'
            f'<div class="wl-more">liquidité 1,2 M · dominance stable 3 séances</div>{_foot("order-flow", "il y a 4 s", "live")}</div>')


def vol_cone(current=18, pctile=42):
    """VOLATILITY CONE — vol actuelle vs enveloppe historique + percentile."""
    W, H = 220, 110
    top = [(0, 30), (55, 45), (110, 55), (165, 62), (220, 66)]
    bot = [(0, 30), (55, 20), (110, 16), (165, 14), (220, 13)]
    tp = ' '.join(f'{x},{y}' for x, y in top)
    bp = ' '.join(f'{x},{y}' for x, y in reversed(bot))
    cx = 90
    cy = 22 + (100 - current) / 100 * 40
    return (f'<div style="width:{W}px">{_hdr("Volatilité implicite", f"{current}%")}'
            f'<svg viewBox="0 0 {W} {H}" width="100%" height="{H}" style="max-width:{W}px">'
            f'<polygon points="{tp} {bp}" fill="{_VI}" fill-opacity=".12" stroke="{_VI}" stroke-opacity=".4" stroke-width="1"/>'
            f'<circle cx="{cx}" cy="{cy:.0f}" r="4" fill="var(--vx-ember-500)"/>'
            f'<text x="{cx+7}" y="{cy+3:.0f}" fill="var(--vx-ember-400)" font-size="9">actuel</text>'
            f'<text x="6" y="{H-4}" fill="var(--vx-text-muted)" font-size="9">3M · 6M · 1A</text></svg>'
            f'{_concl(f"{pctile}ᵉ percentile — vol modérée, primes correctes", "opt")}</div>')


def rs_path(series):
    """RELATIVE-STRENGTH PATH — actif vs benchmark : accélération/divergence."""
    W, H = 240, 100
    mn, mx = min(series), max(series)
    rng = (mx - mn) or 1
    z = H - (0 - mn) / rng * H if mn < 0 < mx else H / 2
    pts = ' '.join(f'{i/(len(series)-1)*W:.1f},{H-(v-mn)/rng*(H-6)-3:.1f}' for i, v in enumerate(series))
    up = series[-1] > 0
    return (f'<div style="width:{W}px">{_hdr("Force relative vs S&P 500")}'
            f'<svg viewBox="0 0 {W} {H}" width="100%" height="{H}" style="max-width:{W}px">'
            f'<line x1="0" y1="{z:.0f}" x2="{W}" y2="{z:.0f}" stroke="rgba(255,255,255,.18)" stroke-dasharray="3 3"/>'
            f'<polyline points="{pts}" fill="none" stroke="{_CY}" stroke-width="1.8"/>'
            f'<circle cx="{W}" cy="{H-(series[-1]-mn)/rng*(H-6)-3:.1f}" r="3" fill="var(--vx-ember-500)"/></svg>'
            f'{_concl("Surperforme — RS croissante au-dessus de 0" if up else "Sous-performe — divergence baissière", "go" if up else "risk")}</div>')


def rr_terrain(maxloss=-8, prob=12, exc=34, be=132):
    """RISK/REWARD TERRAIN — perte max / gain probable / exceptionnel + zones."""
    W, H = 240, 110
    return (f'<div style="width:{W}px">{_hdr("Asymétrie du plan")}'
            f'<svg viewBox="0 0 {W} {H}" width="100%" height="{H}" style="max-width:{W}px">'
            f'<defs><linearGradient id="rrl" x1="0" x2="1"><stop offset="0" stop-color="{_RB}" stop-opacity=".22"/><stop offset="1" stop-color="{_RB}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="rrg" x1="0" x2="1"><stop offset="0" stop-color="{_EM}" stop-opacity="0"/><stop offset="1" stop-color="{_EM}" stop-opacity=".26"/></linearGradient></defs>'
            f'<rect x="0" y="60" width="96" height="{H-60}" fill="url(#rrl)"/><rect x="96" y="0" width="{W-96}" height="{H}" fill="url(#rrg)"/>'
            f'<polyline points="0,86 96,86 {W},20" fill="none" stroke="#F0EBE4" stroke-width="2"/>'
            f'<line x1="96" y1="0" x2="96" y2="{H}" stroke="var(--vx-ember-500)" stroke-dasharray="3 3"/>'
            f'<text x="4" y="{H-6}" fill="{_RB}" font-size="9">max {maxloss}%</text>'
            f'<text x="{W-4}" y="30" text-anchor="end" fill="{_EM}" font-size="9">exc. +{exc}%</text>'
            f'<text x="100" y="14" fill="var(--vx-ember-400)" font-size="9">BE {be}</text></svg>'
            f'{_concl(f"Gain probable +{prob}% vs risque {maxloss}% — R:R "+f"{exc/abs(maxloss):.1f}", "go")}</div>')


def position_health_strip(sym='AAPL', pl=8.4, thesis='intacte', catalyst='Résultats J-5', inval='185,0'):
    """POSITION HEALTH STRIP — P&L · thèse · catalyseur · invalidation · action."""
    tcol = {'intacte': _EM, 'surveiller': _AM, 'invalidée': _RB}[thesis]
    plc = _EM if pl >= 0 else _RB
    return (f'<div style="width:250px;display:flex;flex-direction:column;gap:6px">'
            f'<div style="display:flex;align-items:center;gap:8px"><b style="font-size:14px;color:var(--vx-ember-400)">{sym}</b>'
            f'<span style="font-size:15px;font-weight:800;color:{plc};font-variant-numeric:tabular-nums">{pl:+.1f}%</span>'
            f'<span style="margin-left:auto;font-size:10px;padding:2px 8px;border-radius:999px;color:{tcol};border:1px solid {tcol}">thèse {thesis}</span></div>'
            f'<div style="display:flex;gap:12px;font-size:11px;color:var(--vx-text-secondary)"><span>⚡ {catalyst}</span><span>⛔ inval. {inval}</span></div>'
            f'<div style="display:flex;gap:8px"><button class="wl-tip" data-tip="Ouvrir le dossier" style="font:inherit;font-size:11px;padding:5px 10px;border-radius:8px;border:1px solid var(--vx-ember-500);background:transparent;color:var(--vx-ember-400);cursor:pointer">Réévaluer →</button></div>'
            f'{_concl("Gagnant sur thèse intacte — conserver, ne pas vendre au seul motif du gain", "go")}</div>')


def breadth_field(a50=63, a200=51, adv=312, dec=188, nh=42, nl=9):
    """MARKET BREADTH FIELD — champ de participation + adv/decline + divergence."""
    dots = ''
    on = round(a50 / 100 * 40)
    for i in range(40):
        col = _EM if i < on else 'rgba(255,255,255,.07)'
        dots += f'<span style="width:8px;height:8px;border-radius:2px;background:{col}"></span>'
    return (f'<div style="width:230px">{_hdr("Participation du marché")}'
            f'<div style="display:grid;grid-template-columns:repeat(10,8px);gap:4px;margin-bottom:8px">{dots}</div>'
            f'<div style="display:flex;gap:14px;font-size:11px;color:var(--vx-text-secondary);font-variant-numeric:tabular-nums">'
            f'<span>&gt;MM50 <b style="color:#F0EBE4">{a50}%</b></span><span>&gt;MM200 <b style="color:#F0EBE4">{a200}%</b></span>'
            f'<span>A/D <b style="color:{_EM}">{adv}</b>/<b style="color:{_RB}">{dec}</b></span></div>'
            f'{_concl("Hausse partagée — participation saine >55%", "go")}'
            f'<div class="wl-more">nouveaux hauts {nh} / bas {nl} · aucune divergence</div></div>')


def liquidity_depth(bid=118.4, ask=118.6, vol=1250, oi=8400):
    """LIQUIDITY DEPTH — bid/ask · spread · volume · OI · qualité d’exécution."""
    spread = (ask - bid) / ((ask + bid) / 2) * 100
    rows = ''
    for lab, val, col in [('Ask', ask, _RB), ('', (ask + bid) / 2, 'var(--vx-ember-500)'), ('Bid', bid, _EM)]:
        w = 40 + (val - bid) / (ask - bid) * 60 if ask != bid else 60
        rows += (f'<div style="display:flex;align-items:center;gap:8px"><span style="width:26px;font-size:9px;color:var(--vx-text-muted)">{lab}</span>'
                 f'<span style="flex:1;height:8px;background:rgba(0,0,0,.3);border-radius:3px;overflow:hidden"><i style="display:block;height:100%;width:{w:.0f}%;background:{col};opacity:.7"></i></span>'
                 f'<span style="width:44px;text-align:right;font-size:10px;color:#F0EBE4;font-variant-numeric:tabular-nums">{val:g}</span></div>')
    return (f'<div style="width:230px">{_hdr("Profondeur / liquidité")}{rows}'
            f'<div style="display:flex;gap:14px;font-size:10px;color:var(--vx-text-secondary);margin-top:6px;font-variant-numeric:tabular-nums"><span>spread {spread:.2f}%</span><span>vol {vol}</span><span>OI {oi}</span></div>'
            f'{_concl("Spread serré — exécution correcte" if spread < 0.4 else "Spread large — prudence", "go" if spread < 0.4 else "wait")}</div>')


def correlation_web(nodes):
    """MARKET CORRELATION WEB — corrélations entre actifs."""
    W, H = 200, 140
    cx, cy = W / 2, H / 2
    body = f'<circle cx="{cx}" cy="{cy}" r="16" fill="var(--vx-ember-soft)" stroke="var(--vx-ember-500)"/><text x="{cx}" y="{cy+3}" text-anchor="middle" fill="var(--vx-ember-400)" font-size="9" font-weight="700">SPX</text>'
    for i, (sym, corr) in enumerate(nodes):
        a = i / len(nodes) * 360
        x, y = _pol(cx, cy, 56, a)
        col = _EM if corr > 0.3 else _RB if corr < -0.3 else _GY
        op = 0.2 + abs(corr) * 0.6
        body += (f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{col}" stroke-opacity="{op:.2f}" stroke-width="{1+abs(corr)*2:.1f}"/>'
                 f'<circle cx="{x:.0f}" cy="{y:.0f}" r="12" fill="rgba(0,0,0,.4)" stroke="{col}"/>'
                 f'<text x="{x:.0f}" y="{y+3:.0f}" text-anchor="middle" fill="#F0EBE4" font-size="8">{sym}</text>')
    return (f'<div style="width:{W}px"><svg viewBox="0 0 {W} {H}" width="100%" height="{H}" style="max-width:{W}px">{body}</svg>'
            f'{_concl("Corrélations élevées — diversification faible", "wait")}</div>')


def earnings_gap_map(gaps):
    """EARNINGS GAP MAP — historique des gaps post-résultats."""
    bars = ''
    mx = max(abs(g) for g in gaps)
    for i, g in enumerate(gaps):
        col = _EM if g >= 0 else _RB
        h = abs(g) / mx * 34
        y = 40 - h if g >= 0 else 40
        bars += f'<rect class="wl-tip" data-tip="T{i+1}: {g:+.0f}%" x="{i*22+6}" y="{y:.0f}" width="14" height="{h:.0f}" fill="{col}" rx="2"/>'
    return (f'<div style="width:{len(gaps)*22+12}px">{_hdr("Gaps post-résultats")}'
            f'<svg viewBox="0 0 {len(gaps)*22+12} 84" width="100%" height="84"><line x1="0" y1="40" x2="{len(gaps)*22+12}" y2="40" stroke="rgba(255,255,255,.15)"/>{bars}</svg>'
            f'{_concl("Réaction volatile aux résultats — risque événementiel élevé", "risk")}</div>')


def sr_spine(price=119, levels=None):
    """SUPPORT/RESISTANCE SPINE — colonne de niveaux techniques."""
    levels = levels or [('R2', 132, _AM), ('R1', 126, _AM), ('Prix', 119, 'var(--vx-ember-500)'), ('S1', 112, _EM), ('S2', 105, _EM)]
    mn = min(l[1] for l in levels)
    mx = max(l[1] for l in levels)
    rows = ''
    for lab, val, col in sorted(levels, key=lambda x: -x[1]):
        y = (mx - val) / (mx - mn) * 90
        rows += (f'<div style="position:absolute;top:{y:.0f}px;left:0;right:0;display:flex;align-items:center;gap:6px">'
                 f'<span style="width:22px;font-size:9px;color:{col}">{lab}</span>'
                 f'<span style="flex:1;height:2px;background:{col};opacity:.6"></span>'
                 f'<span style="font-size:10px;color:#F0EBE4;font-variant-numeric:tabular-nums">{val:g}</span></div>')
    return (f'<div style="width:160px">{_hdr("Supports / résistances")}'
            f'<div style="position:relative;height:104px">{rows}</div>'
            f'{_concl("Prix coincé sous R1 126 — cassure = signal", "wait")}</div>')


def catalyst_runway(events=None):
    """CATALYST RUNWAY — piste de décollage des catalyseurs : DTE + impact."""
    events = events or [('Résultats', 3, 'high'), ('Fed', 9, 'high'),
                        ('Ex-div', 14, 'low'), ('Guidance', 26, 'med')]
    horizon = max(e[1] for e in events) or 1
    icol = {'high': _RB, 'med': _AM, 'low': _GY}
    marks = ''
    for lab, dte, imp in events:
        left = dte / horizon * 100
        c = icol[imp]
        marks += (f'<div class="wl-tip" data-tip="{lab} · J-{dte} · impact {imp}" '
                  f'style="position:absolute;left:{left:.0f}%;top:0;transform:translateX(-50%);text-align:center">'
                  f'<span style="display:block;width:2px;height:26px;margin:0 auto;background:{c};opacity:.8"></span>'
                  f'<span style="display:block;width:9px;height:9px;border-radius:50%;background:{c};margin:2px auto 0"></span>'
                  f'<span style="display:block;font-size:8px;color:var(--vx-text-muted);margin-top:2px">J-{dte}</span></div>')
    nxt = min(events, key=lambda e: e[1])
    return (f'<div style="width:250px">{_hdr("Prochains catalyseurs")}'
            f'<div style="position:relative;height:56px;border-left:2px solid var(--vx-ember-500)">'
            f'<div style="position:absolute;left:0;right:0;top:12px;height:1px;background:rgba(255,255,255,.12)"></div>{marks}</div>'
            f'{_concl(f"{nxt[0]} dans {nxt[1]} j — risque événementiel imminent" if nxt[1] <= 5 else f"{nxt[0]} dans {nxt[1]} j — fenêtre dégagée", "risk" if nxt[1] <= 5 else "go")}'
            f'<div class="wl-more">4 catalyseurs · fenêtre 26 j · 2 à fort impact</div>{_foot("calendrier", "aujourd’hui", "delayed")}</div>')


# ── États honnêtes (bande d'états) ─────────────────────────────────────────
def _state(kind):
    m = {
        'loading': ('<div class="wl-skel"></div>', 'loading'),
        'empty': ('Aucune donnée — prochaine action proposée', 'empty'),
        'insufficient': ('Données insuffisantes — Vertex ne tranche pas', 'insufficient'),
        'stale': ('Périmé · il y a 3 h', 'stale'),
        'demo': ('DÉMO — échantillon', 'demo'),
        'live': (live_pill('live'), 'live'),
        'offline': ('Hors-ligne · dernière valeur il y a 12 min', 'offline'),
        'error': ('Erreur moteur — réessayer', 'error'),
    }
    body, cls = m[kind]
    return f'<div class="wl-state wl-state--{cls}"><span class="lab">{kind}</span><div class="body">{body}</div></div>'


# ══ REGISTRE DES BENCHES ═══════════════════════════════════════════════════
# Chaque bench : (id, nom, famille, question, [(vlabel, html)...], [états])
def _benches():
    ALL_STATES = ['loading', 'empty', 'insufficient', 'stale', 'demo', 'live']
    return [
        ('W01', 'Regime Aura', 'Régime', 'Dans quel régime, avec quelle confiance ? (variantes = concepts distincts)', [
            ('V1 · halo + grammaire', (
                '<div style="width:210px">' + aura('Tendance haussière', 68, 'go') +
                '<div style="display:flex;gap:10px;margin-top:6px;font-size:10px;color:var(--vx-text-secondary);font-variant-numeric:tabular-nums">'
                '<span>SPX <b style="color:#F0EBE4">>MM200</b></span>'
                '<span>Breadth <b style="color:var(--vx-positive)">63%</b></span>'
                '<span>VIX <b style="color:#F0EBE4">14,6</b></span></div>' +
                _concl('Régime porteur — risque neuf autorisé, invalidation SPX < MM50 (5 780)', 'go') +
                '<div class="wl-more">RS marché +2,1% · 63% >MM50 · A/D 312/188 · aucune divergence</div>' +
                _foot('scan · indices', 'il y a 20 s', 'delayed') + '</div>'), 'smoked'),
            ('V2 · horizon de phase', horizon_band('go', 'Tendance', 'phase haussière · vent porteur'), 'polished'),
            ('V3 · brume indéterminée', aura('Indéterminé', 0, 'off'), 'frosted'),
            ('V4 · capsule à tension', regime_capsule('Chop', 'wait', 52), 'metal'),
            ('V5 · champ de pression', pressure_field('Risk-Off', 'risk', 44), 'deepblack'),
            ('V6 · tuile météo', weather_tile('Environnement', '⛅', 'Chop', 'vent latéral · prudence', 'wait'), 'matte'),
        ], ALL_STATES),
        ('W04', 'Risk-of-Day Verdict (Slab)', 'Régime', 'Peut-on prendre du risque neuf ?', [
            ('V1', slab('RISK-OFF', 'risk', [('Régime', 'Tendance'), ('Participation', '50 % >MM50'), ('VIX', '12,7 · calme')])),
            ('V2 · porteur', slab('RISK-ON', 'go', [('Régime', 'Tendance haussière'), ('Breadth', '61 %'), ('VIX', '11,8')])),
        ], ['loading', 'empty', 'demo', 'live']),
        ('W07', 'Momentum Comb', 'Momentum', 'La poussée tient-elle du court au long ?', [
            ('V1 · peigne', comb(MOM)),
            ('V2 · miroir', comb([4.2, -2.1, 9.2, -3.5], mirror=True)),
            ('V3 · valeurs', comb(MOM, show_vals=True)),
        ], ['loading', 'empty']),
        ('W08', 'Trend Ribbon (Sparkline+)', 'Momentum', 'La tendance reste-t-elle exploitable ?', [
            ('V1 · hausse', sparkline(SPARK_UP, 'up')),
            ('V2 · baisse', sparkline(SPARK_DN, 'down')),
            ('V3 · brand', sparkline(SPARK_UP, 'brand')),
            ('V4 · sans dot', sparkline(SPARK_UP, 'tech', dot=False)),
        ], ['loading', 'empty', 'insufficient']),
        ('W17', 'Breadth Tide', 'Breadth', 'La participation s’élargit-elle ?', [
            ('V1 · marée haute', tide(62)),
            ('V2 · étroite', tide(38)),
            ('V3 · anneau', ring(52, sub='>MM50')),
        ], ['loading', 'empty', 'stale']),
        ('W21', 'Health Reactor', 'Breadth', 'D’où vient le score de santé ?', [
            ('V1', reactor(37, [('>MM50', 50, 30), ('>MM200', 45, 25), ('Breadth', 52, 25), ('Adv/Déc', 40, 20)])),
        ], ['loading', 'insufficient']),
        ('W12', 'Sector Rotation Orbit', 'Rotation', 'Qui entre en leadership ?', [
            ('V1 · comètes', orbit([('SW', 62, 1.3, 'lead'), ('BT', 45, -0.3, 'mid'), ('SE', 31, -1.6, 'lag'), ('EN', 55, 0.8, 'lead')])),
        ], ['loading', 'insufficient']),
        ('W35', 'Asymmetry Ledge (Scatter)', 'Opportunité', 'Où sont les meilleures asymétries ?', [
            ('V1 · corniche', ledge([('ACN', 82, 90, 'buy'), ('AFL', 74, 88, 'buy'), ('MMM', 60, 78, 'neutral'), ('XY', 30, 25, 'avoid'), ('ZW', 45, 40, 'avoid')], 0)),
        ], ['loading', 'empty']),
        ('W23', 'Stress Thermocline', 'Volatilité', 'Eaux calmes ou zone de stress ?', [
            ('V1 · colonne', thermocline(12.7)),
            ('V2 · stress', thermocline(31)),
        ], ['loading', 'empty']),
        ('W24', 'Dial (VIX / borné)', 'Volatilité', 'Niveau d’une métrique bornée ?', [
            ('V1 · VIX', dial(12.7, 50, 'VIX', 'volatilité comprimée', '', [(15, 'var(--vx-positive)'), (25, 'var(--vx-warning)'), (50, 'var(--vx-negative)')])),
            ('V2 · confiance', dial(68, 100, 'confiance', 'signal modéré')),
        ], ['loading', 'empty']),
        ('W05', 'Rail (axe borné)', 'Régime', 'Position sur un axe bipolaire ?', [
            ('V1 · risk', rail(30, 'RISK-OFF', 'écart −11', 'RISK-ON')),
            ('V2 · stress', rail(9, '10', '25', '40+', 'stress')),
            ('V3 · défense', rail(45, 'Défense', 'Neutre', 'Attaque')),
        ], ['loading', 'empty']),
        ('W38', 'Conviction Spine', 'Opportunité', 'Force de conviction ?', [
            ('V1', spine(72, 'conviction')),
            ('V2 · faible', spine(28, 'conviction')),
        ], ['loading', 'insufficient']),
        ('W33', 'Opportunity Dominant Slab', 'Opportunité', 'Meilleure asymétrie, et pourquoi ?', [
            ('V1', dominant('ACN', 'S', 'Technology · 198,00 · BUY', 84,
                            [('Asymétrie', '27', True), ('Prob. gain', '60 %', True), ('R:R visé', '6', False), ('Edge', '58/100', False)])),
        ], ['loading', 'empty', 'demo']),
        ('W37', 'Comparison Matrix', 'Opportunité', 'Lequel offre la meilleure asymétrie ?', [
            ('V1', comparison([('Score', [84, 81, 74], 100), ('Asymétrie', [27, 20, 31], 50),
                               ('Prob. gain %', [60, 55, 61], 100), ('R:R', [6, 6, 9], 8)])),
        ], ['loading', 'insufficient']),
        ('W36', 'Selection Funnel', 'Opportunité', 'Que reste-t-il après filtrage ?', [
            ('V1', funnel([('Univers', 20), ('Éligibles', 20), ('Radar', 8), ('Prioritaires', 7), ('Actionnables', 2)])),
        ], ['loading', 'insufficient']),
        ('W29', 'Premium Index Card', 'Marchés', 'Où en est l’indice dans sa plage ?', [
            ('V1 · hausse', f'<div class="wl-idx" data-dir="up"><div class="top"><span class="mono">S&P</span><span class="nm">S&P 500</span><span class="rel">près du haut</span></div><div class="vr"><span class="val">6 000</span><span class="chg pos">+1,67 %</span></div>{sparkline(SPARK_UP,"up",40,150)}<div class="ft"><b>plage 5 891–6 500</b></div></div>'),
            ('V2 · baisse', f'<div class="wl-idx" data-dir="down"><div class="top"><span class="mono">DJIA</span><span class="nm">Dow Jones</span><span class="rel">près du bas</span></div><div class="vr"><span class="val">44 000</span><span class="chg neg">−0,59 %</span></div>{sparkline(SPARK_DN,"down",40,150)}<div class="ft"><b>plage 39 069–45 325</b></div></div>'),
        ], ['loading', 'empty']),
        ('W07b', 'Momentum Ribs', 'Momentum', 'Le momentum est-il cohérent entre horizons ?', [
            ('V1 · côtes', momentum_ribs(MOM)),
            ('V2 · retournement', momentum_ribs([4.2, -2.1, 9.2, -3.5])),
        ], ['loading', 'empty']),
        ('W23b', 'Volatility Rift', 'Volatilité', 'La volatilité menace-t-elle ?', [
            ('V1 · comprimée', vol_rift(12.7)),
            ('V2 · expansion', vol_rift(31)),
        ], ['loading', 'empty']),
        ('W-RC', 'Risk Crater', 'Volatilité', 'Quelle est la sévérité du risque ?', [
            ('V1 · cratère', risk_crater('élevé')),
        ], ['loading', 'insufficient']),
        ('W-OB', 'Opportunity Beacon (Signal Bloom)', 'Opportunité', 'La force du signal justifie-t-elle l’attention ?', [
            ('V1 · floraison', signal_bloom(72, 'go')),
            ('V2 · identité', signal_bloom(58, 'brand')),
            ('V3 · options', signal_bloom(64, 'opt')),
        ], ['loading', 'empty', 'demo']),
        ('W38b', 'Conviction Pillar', 'Opportunité', 'Quelle force de conviction ? (variante segmentée)', [
            ('V1 · pilier', conviction_pillar(72)),
            ('V2 · faible', conviction_pillar(28)),
        ], ['loading', 'insufficient']),
        ('W41', 'Catalyst Countdown Ring', 'Catalyseurs', 'Dans combien de temps le prochain catalyseur ?', [
            ('V1 · imminent', countdown_ring(3)),
            ('V2 · proche', countdown_ring(9)),
            ('V3 · lointain', countdown_ring(22)),
        ], ['loading', 'empty']),

        # ═══ ANALYSE ═══
        ('W44', 'Verdict Slab', 'Analyse', 'J’entre, j’attends ou j’évite ?', [
            ('V1 · entrer', slab('ENTRER', 'go', [('Score', '32/40'), ('Niveau', 'S'), ('Confiance', '72 %'), ('Entrée', '198,4'), ('Invalidation', '188,0')])),
            ('V2 · éviter', slab('ÉVITER', 'risk', [('Score', '14/40'), ('Niveau', 'B'), ('Confiance', '40 %'), ('Note', 'timing défavorable')])),
        ], ['loading', 'insufficient', 'demo']),
        ('W45', 'Scenario Triad', 'Analyse', 'Que risque-t-on, qu’attend-on, que peut-on gagner ?', [
            ('V1 · triptyque', scenario_triad()),
        ], ['loading', 'insufficient']),
        ('W-TP', 'Thesis Pulse', 'Analyse', 'La thèse tient-elle ?', [
            ('V1 · intacte', thesis_pulse('ok')),
            ('V2 · surveiller', thesis_pulse('watch')),
            ('V3 · invalidée', thesis_pulse('ko')),
        ], ['loading', 'empty']),
        ('W-SD', 'Score Decomposition', 'Analyse', 'D’où vient le score /40 ?', [
            ('V1 · empilée', score_decomp([('Fonda', 11, _EM), ('Techn', 9, _CY), ('Momentum', 8, _AM), ('Risque', 4, _RB)])),
        ], ['loading', 'insufficient']),
        ('W-CC', 'Committee Consensus', 'Analyse', 'Le comité est-il d’accord ?', [
            ('V1 · votes', committee([('Fonda', '+'), ('Tech', '+'), ('Momentum', '+'), ('Risque', '-'), ('Macro', '=')])),
        ], ['loading', 'insufficient']),
        ('W-CL', 'Confidence Lens', 'Analyse', 'Quelle confiance dans le verdict ?', [
            ('V1 · diaphragme', confidence_lens(72)),
            ('V2 · faible', confidence_lens(34)),
        ], ['loading', 'insufficient']),

        # ═══ PORTEFEUILLE ═══
        ('W-PC', 'Allocation Constellation', 'Portefeuille', 'Où est concentré mon capital ?', [
            ('V1 · constellation', constellation([('NVDA', 20, 30, 11, 1), ('AAPL', 45, 55, 8, 1), ('XOM', 68, 35, 6, -1), ('JPM', 82, 62, 5, 1), ('PFE', 55, 80, 4, -1)])),
        ], ['loading', 'empty']),
        ('W-CT', 'Concentration Tower', 'Portefeuille', 'Suis-je trop concentré ?', [
            ('V1 · tour', concentration_tower([('NVDA', 32, 'var(--vx-ember-500)'), ('AAPL', 22, _GY), ('JPM', 16, _GY), ('Autres', 30, 'rgba(255,255,255,.1)')])),
        ], ['loading', 'insufficient']),
        ('W-DC', 'Drawdown Canyon', 'Portefeuille', 'À quel point suis-je descendu ?', [
            ('V1 · canyon', drawdown_canyon([0, -2, -5, -9, -14, -11, -7, -12, -6, -3, -1, -4])),
        ], ['loading', 'insufficient']),
        ('W-WG', 'Winner / Loser Guardrails', 'Portefeuille', 'Gérer les gagnants, protéger contre les perdants', [
            ('V1 · gagnant', f'<div style="width:210px"><div style="font-size:11px;color:{_EM};font-weight:700">GAGNANT · NVDA +48 %</div><div style="font-size:11px;color:var(--vx-text-secondary);margin:6px 0">Paliers : <b style="color:{_EM}">+20 +30 +50 +75 +100</b></div><div style="font-size:10px;color:var(--vx-text-muted)">Réévaluer selon la thèse — jamais vendre au seul motif du gain.</div></div>', 'polished'),
            ('V2 · perdant', f'<div style="width:210px"><div style="font-size:11px;color:{_RB};font-weight:700">GARDE-FOU · perte −12 %</div><div style="font-size:12px;color:var(--vx-text-primary);margin:6px 0;font-weight:650">Ne pas renforcer une position perdante.</div><div style="font-size:10px;color:var(--vx-text-muted)">Invalidation atteinte → sortie disciplinée.</div></div>', 'deepblack'),
        ], ['loading', 'empty']),

        # ═══ OPTIONS ═══
        ('W50', 'Payoff Terrain', 'Options', 'Que rapporte/coûte ce contrat ?', [
            ('V1 · relief', payoff_terrain()),
        ], ['loading', 'insufficient', 'demo']),
        ('W51', 'Greek Vector Field', 'Options', 'Comment le contrat réagit-il ?', [
            ('V1 · champ', greek_field()),
        ], ['loading', 'insufficient']),
        ('W-LL', 'Liquidity Lens', 'Options', 'Le contrat est-il liquide ?', [
            ('V1 · spread', ring(78, unit='', sub='liquidité')),
        ], ['loading', 'insufficient']),
        ('W-TB', 'Theta Burn Track', 'Options', 'Combien coûte chaque jour d’attente ?', [
            ('V1 · érosion', sparkline([60, 57, 53, 48, 42, 35, 27, 18], 'down', 44, 160)),
        ], ['loading', 'insufficient']),

        # ═══ JOURNAL ═══
        ('W-DR', 'Discipline Ring', 'Journal', 'Est-ce que je suis mon process ?', [
            ('V1 · anneau', ring(82, unit='', sub='discipline')),
            ('V2 · pilier', conviction_pillar(82)),
        ], ['loading', 'insufficient']),
        ('W-BH', 'Bias Heatmap', 'Journal', 'Quels biais reviennent ?', [
            ('V1 · carte', bias_heatmap()),
        ], ['loading', 'empty']),
        ('W-PL', 'Progress Ladder', 'Journal', 'Où en est ma progression ?', [
            ('V1 · échelons', progress_ladder([100, 90, 70, 40, 15])),
        ], ['loading', 'insufficient']),

        # ═══ SYSTÈME ═══
        ('W68', 'Data Integrity Reactor', 'Système', 'Puis-je faire confiance aux données ?', [
            ('V1 · fiable', data_reactor(84)),
            ('V2 · démo', data_reactor(30)),
        ], ['loading', 'demo', 'offline']),
        ('W-FM', 'Source Freshness Matrix', 'Système', 'Quelles sources sont fraîches ?', [
            ('V1 · matrice', freshness_matrix([('IBKR (TWS)', 'delayed'), ('Scan moteur', 'live'), ('Actualités', 'live'), ('Calendrier', 'frozen')])),
        ], ['loading', 'offline']),
        ('W-ES', 'Engine Status Spine', 'Système', 'Les moteurs tournent-ils ?', [
            ('V1 · colonne', engine_spine([('Scan', True), ('Décision', True), ('Options', True), ('Scénarios', False)])),
        ], ['loading', 'error']),
        ('W-RS', 'READONLY Seal', 'Système', 'Vertex peut-il passer un ordre ?', [
            ('V1 · sceau', readonly_seal()),
        ], ['live']),

        # ═══ FINANCE NATIVE (P03) — objets de marché propriétaires ═══
        # Chandeliers : NON réservés à Analyse (présents Analyse/Marchés/Opportunité).
        ('W-CAN', 'Candlestick Snapshot', 'Analyse', 'Le prix confirme-t-il la cassure au-dessus de la résistance ?', [
            ('V1 · chandeliers + niveaux', candles(), 'deepblack'),
            ('V2 · sans événement', candles(event_idx=None, gap_idx=None, name='ACN', resistance=124, target=130), 'smoked'),
        ], ['loading', 'insufficient', 'stale', 'demo']),
        ('W-CANM', 'Candlestick — Indice', 'Marchés', 'L’indice tient-il sa plage haussière ?', [
            ('V1 · S&P 500', candles(name='S&P 500', entry=None, stop=None, target=None, resistance=None, event_idx=None), 'polished'),
        ], ['loading', 'empty', 'stale']),
        ('W-CANC', 'Candlestick — Carte compacte', 'Opportunité', 'Aperçu prix instantané (format carte) ?', [
            ('V1 · compact', candles(compact=True, name='NVDA'), 'metal'),
            ('V2 · compact baissier', candles(compact=True, name='PFE', data=list(reversed(OHLC))), 'smoked'),
        ], ['loading', 'empty']),
        ('W-SRS', 'Support / Resistance Spine', 'Analyse', 'Quels niveaux encadrent le prix ?', [
            ('V1 · colonne', sr_spine()),
        ], ['loading', 'insufficient']),
        ('W-PLD', 'Price Ladder', 'Analyse', 'Où sont entrée, stop, objectifs vs prix ?', [
            ('V1 · échelle', price_ladder()),
        ], ['loading', 'insufficient', 'demo']),
        ('W-TAPE', 'Market Tape', 'Marchés', 'Que fait le marché à l’instant ?', [
            ('V1 · bandeau', market_tape([('SPX', 1.67, '3,1 Md'), ('NDX', 2.1, '2,4 Md'), ('AAPL', -0.6, '58 M'),
                                          ('NVDA', 3.4, '112 M'), ('XOM', 0.4, '19 M'), ('VIX', -4.2, '—')])),
        ], ['loading', 'empty', 'stale']),
        ('W-CW', 'Market Correlation Web', 'Marchés', 'Mes actifs bougent-ils ensemble ?', [
            ('V1 · toile', correlation_web([('NVDA', 0.82), ('AAPL', 0.61), ('XOM', -0.44), ('TLT', -0.7), ('GLD', 0.12)])),
        ], ['loading', 'insufficient']),
        ('W-RSP', 'Relative-Strength Path', 'Momentum', 'L’actif surperforme-t-il son indice ?', [
            ('V1 · surperformance', rs_path([-1.2, -0.4, 0.3, 0.9, 1.6, 2.1, 2.8, 3.4])),
            ('V2 · divergence', rs_path([1.1, 0.6, 0.2, -0.3, -0.9, -1.4, -1.8, -2.3])),
        ], ['loading', 'insufficient']),
        ('W-BF', 'Market Breadth Field', 'Breadth', 'La hausse est-elle partagée ?', [
            ('V1 · champ', breadth_field()),
            ('V2 · étroite', breadth_field(a50=41, a200=38, adv=180, dec=320, nh=12, nl=48)),
        ], ['loading', 'insufficient', 'stale']),
        ('W-VC', 'Volatility Cone', 'Volatilité', 'La vol implicite est-elle chère ?', [
            ('V1 · cône', vol_cone()),
            ('V2 · tendue', vol_cone(current=34, pctile=88)),
        ], ['loading', 'insufficient']),
        ('W-OFR', 'Order-Flow Ribbon', 'Opportunité', 'Qui domine, acheteurs ou vendeurs ?', [
            ('V1 · live acheteurs', orderflow_ribbon(62, 38)),
            ('V2 · vendeurs', orderflow_ribbon(41, 59)),
        ], ['loading', 'empty', 'live']),
        ('W-RRT', 'Risk / Reward Terrain', 'Opportunité', 'L’asymétrie penche-t-elle en ma faveur ?', [
            ('V1 · relief', rr_terrain()),
        ], ['loading', 'insufficient']),
        ('W-PHS', 'Position Health Strip', 'Portefeuille', 'Cette position va-t-elle bien ?', [
            ('V1 · gagnant', position_health_strip('AAPL', 8.4, 'intacte'), 'polished'),
            ('V2 · surveiller', position_health_strip('XOM', -3.1, 'surveiller', 'Résultats J-2', '96,0'), 'metal'),
        ], ['loading', 'empty', 'insufficient']),
        ('W-LD', 'Liquidity Depth', 'Options', 'Puis-je exécuter proprement ?', [
            ('V1 · profondeur', liquidity_depth()),
            ('V2 · spread large', liquidity_depth(bid=4.1, ask=4.8, vol=120, oi=340)),
        ], ['loading', 'insufficient']),
        ('W-EGM', 'Earnings Gap Map', 'Catalyseurs', 'Le titre réagit-il violemment aux résultats ?', [
            ('V1 · gaps', earnings_gap_map([6, -4, 9, 2, -7, 11, -3, 5])),
        ], ['loading', 'insufficient', 'demo']),
        ('W-CR', 'Catalyst Runway', 'Catalyseurs', 'Quel catalyseur arrive, et quand ?', [
            ('V1 · piste', catalyst_runway()),
        ], ['loading', 'empty', 'stale']),

        ('O-1', 'Primitives — KPI · Grade · Live · Delta', 'Primitives', 'Les briques atomiques', [
            ('KPI glass', kpi('S&P 500', '6 000', '+1,67 %', 'up', SPARK_UP)),
            ('KPI flat', kpi('Taux 10 ans', '3,00 %', '−0,02 pts', 'flat')),
            ('Grade seals', grade_seal('S+') + ' ' + grade_seal('S') + ' ' + grade_seal('A') + ' ' + grade_seal('B')),
            ('Live pills', live_pill('live') + ' ' + live_pill('delayed') + ' ' + live_pill('frozen') + ' ' + live_pill('fallback')),
        ], ['loading', 'empty']),
    ]


# Accents de famille (mirroir du CSS wl-bench[data-fam]) pour les pastilles.
FAM_ACCENT = {
    'Régime': 'var(--vx-positive)', 'Momentum': '#B6F04A', 'Breadth': 'var(--vx-positive)',
    'Rotation': 'var(--vx-warm-grey)', 'Volatilité': 'var(--vx-option)',
    'Opportunité': 'var(--vx-positive)', 'Marchés': 'var(--vx-technical)',
    'Analyse': 'var(--vx-warning)', 'Portefeuille': '#E7E2DA', 'Options': 'var(--vx-option)',
    'Journal': 'var(--vx-warning)', 'Système': 'var(--vx-technical)', 'Primitives': 'var(--vx-warm-grey)',
}


# ── Page ───────────────────────────────────────────────────────────────────
def render() -> str:
    benches = _benches()
    families = []
    for b in benches:
        if b[2] not in families:
            families.append(b[2])
    nav = ''.join(f'<a href="#fam-{i}" class="wl-navchip">{f}</a>' for i, f in enumerate(families))

    # Matières cyclées si non spécifiées → chaque variante porte une matière distincte.
    MATS = ['smoked', 'polished', 'deepblack', 'metal', 'frosted', 'matte']
    sections = ''
    last_fam = None
    for (wid, name, fam, q, variants, states) in benches:
        if fam != last_fam:
            fi = families.index(fam)
            sw = FAM_ACCENT.get(fam, 'var(--vx-warm-grey)')
            sections += f'<h2 id="fam-{fi}" class="wl-fam">{fam}<span class="wl-fam-swatch" style="background:{sw}"></span></h2>'
            last_fam = fam
        tiles = ''
        for vi, v in enumerate(variants):
            vlabel, html = v[0], v[1]
            mat = v[2] if len(v) > 2 else MATS[vi % len(MATS)]
            live = ' data-live="1"' if 'live' in vlabel.lower() else ''
            vid = f'{wid}-{vlabel.split(" ")[0]}'
            tiles += f'''<div class="wl-tile" data-wid="{vid}">
      <div class="wl-tile-head"><span class="vlab">{vlabel}</span>
        <span class="wl-verdict">
          <button data-v="official" title="Officiel">◎</button>
          <button data-v="reference" title="Référence">★</button>
          <button data-v="rejected" title="Rejeté">✕</button></span></div>
      <div class="wl-stage"><div class="wl-surf wl-surf--{mat}"{live}><span class="wl-mat-tag">{mat}</span>{html}</div></div></div>'''
        strip = ''.join(_state(s) for s in states)
        sections += f'''<section class="wl-bench" data-fam="{fam}">
    <div class="wl-bench-head"><span class="wl-id">{wid}</span><span class="wl-name">{name}</span>
      <span class="wl-q">{q}</span></div>
    <div class="wl-variants">{tiles}</div>
    <div class="wl-states-label">États</div>
    <div class="wl-states">{strip}</div></section>'''

    css = _CSS
    js = _JS
    return f'''<!doctype html><html lang="fr" data-theme="dark"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vertex · Widget Lab</title>
<link rel="stylesheet" href="/static/vertex/css/tokens.css">
<style>{css}</style></head>
<body class="wl">
<header class="wl-top">
  <div class="wl-brand"><span class="wl-logo">V</span> <b>VERTEX</b> · Widget Lab
    <span class="wl-tag">Design System — source de vérité</span></div>
  <div class="wl-actions">
    <span class="wl-legend"><span class="official">◎ Officiel</span> <span class="reference">★ Référence</span> <span class="rejected">✕ Rejeté</span></span>
    <button id="wl-mobile" class="wl-btn ghost">Aperçu mobile</button>
    <button id="wl-export" class="wl-btn">Exporter mes choix</button>
    <button id="wl-reset" class="wl-btn ghost">Réinitialiser</button></div>
</header>
<div class="wl-subbar">
  <div class="wl-nav">{nav}</div>
  <div class="wl-note">⚠️ Laboratoire de design — <b>toutes les valeurs sont des échantillons</b>, aucune donnée réelle, aucun moteur. N’appartient pas au produit Vertex.</div>
</div>
<main class="wl-main">{sections}</main>
<dialog id="wl-modal"><h3>Mes choix (à copier)</h3><textarea id="wl-out" rows="14" readonly></textarea>
  <div class="wl-modal-actions"><button id="wl-copy" class="wl-btn">Copier</button><button id="wl-close" class="wl-btn ghost">Fermer</button></div></dialog>
<script>{js}</script>
</body></html>'''


_CSS = r'''
*{box-sizing:border-box}
.wl{margin:0;background:var(--vx-canvas);color:var(--vx-text-primary);
  font-family:var(--vx-font);-webkit-font-smoothing:antialiased;line-height:1.5;
  --wl-noise:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
.wl-top{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:16px;
  padding:12px 22px;background:rgba(16,14,15,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--vx-border-soft)}
.wl-brand{display:flex;align-items:center;gap:10px;font-size:15px;color:var(--vx-text-secondary)}
.wl-brand b{color:var(--vx-text-primary);letter-spacing:.02em}
.wl-logo{display:grid;place-items:center;width:30px;height:30px;border-radius:8px;font-weight:800;color:var(--vx-ember-ink);background:var(--vx-brand-gradient)}
.wl-tag{font-size:11px;color:var(--vx-text-muted);border-left:1px solid var(--vx-border-default);padding-left:10px;margin-left:4px}
.wl-actions{display:flex;align-items:center;gap:12px}
.wl-legend{font-size:11px;display:flex;gap:10px}
.wl-legend .official{color:var(--vx-ember-400)}.wl-legend .reference{color:var(--vx-technical)}.wl-legend .rejected{color:var(--vx-negative)}
.wl-btn{font:inherit;font-size:12px;padding:7px 12px;border-radius:9px;border:1px solid var(--vx-border-strong);
  background:var(--vx-surface-elevated);color:var(--vx-text-primary);cursor:pointer}
.wl-btn:hover{border-color:var(--vx-ember-500)}
.wl-btn.ghost{background:transparent;color:var(--vx-text-muted)}
.wl-subbar{position:sticky;top:55px;z-index:19;background:rgba(5,7,12,.9);backdrop-filter:blur(8px);border-bottom:1px solid var(--vx-border-soft);padding:8px 22px}
.wl-nav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:6px}
.wl-navchip{font-size:11.5px;text-decoration:none;color:var(--vx-text-secondary);padding:4px 11px;border-radius:999px;
  border:1px solid var(--vx-border-soft);background:var(--vx-surface)}
.wl-navchip:hover{border-color:var(--vx-ember-500);color:var(--vx-ember-400)}
.wl-note{font-size:11px;color:var(--vx-warning)}
.wl-main{max-width:1400px;margin:0 auto;padding:22px}
.wl-fam{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--vx-text-muted);
  margin:30px 2px 12px;padding-bottom:8px;border-bottom:1px solid var(--vx-border-soft)}
.wl-bench{background:linear-gradient(180deg,rgba(37,29,27,.5),rgba(22,19,22,.5));border:1px solid var(--vx-border-soft);
  border-radius:16px;padding:16px 18px;margin-bottom:18px}
.wl-bench-head{display:flex;align-items:baseline;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.wl-id{font-size:11px;font-weight:800;color:var(--vx-ember-400);background:var(--vx-ember-soft);border:1px solid rgba(255,109,41,.25);padding:2px 8px;border-radius:7px}
.wl-name{font-size:16px;font-weight:750}
.wl-q{font-size:12.5px;color:var(--vx-text-muted);font-style:italic}
.wl-variants{display:flex;flex-wrap:wrap;gap:14px}
.wl-tile{background:var(--vx-surface);border:1.5px solid var(--vx-border-soft);border-radius:13px;padding:10px;
  min-width:180px;transition:border-color .18s,box-shadow .18s}
.wl-tile[data-verdict="official"]{border-color:var(--vx-ember-500);box-shadow:0 0 0 1px var(--vx-ember-500),0 8px 22px -12px rgba(255,109,41,.5)}
.wl-tile[data-verdict="reference"]{border-color:var(--vx-technical);box-shadow:0 0 0 1px var(--vx-technical)}
.wl-tile[data-verdict="rejected"]{border-color:var(--vx-negative);opacity:.55}
.wl-tile-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
.wl-tile .vlab{font-size:11px;color:var(--vx-text-secondary);font-weight:600}
.wl-verdict{display:flex;gap:3px}
.wl-verdict button{width:24px;height:24px;border-radius:6px;border:1px solid var(--vx-border-soft);background:var(--vx-surface-elevated);
  color:var(--vx-text-muted);cursor:pointer;font-size:12px;line-height:1;padding:0}
.wl-verdict button:hover{border-color:var(--vx-ember-500);color:var(--vx-ember-400)}
.wl-tile[data-verdict="official"] .wl-verdict button[data-v="official"]{color:var(--vx-ember-400);border-color:var(--vx-ember-500)}
.wl-tile[data-verdict="reference"] .wl-verdict button[data-v="reference"]{color:var(--vx-technical);border-color:var(--vx-technical)}
.wl-tile[data-verdict="rejected"] .wl-verdict button[data-v="rejected"]{color:var(--vx-negative);border-color:var(--vx-negative)}
.wl-stage{display:grid;place-items:center;min-height:120px;overflow-x:auto}
.wl-surf>*{max-width:100%}
.wl-cmp{max-width:none}
.wl-states-label{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--vx-text-faint);margin:16px 0 8px}
.wl-states{display:flex;flex-wrap:wrap;gap:8px}
.wl-state{min-width:130px;border:1px dashed var(--vx-border-soft);border-radius:10px;padding:8px;background:rgba(0,0,0,.2)}
.wl-state .lab{font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--vx-text-faint);display:block;margin-bottom:5px}
.wl-state .body{font-size:11px;color:var(--vx-text-secondary);min-height:24px;display:flex;align-items:center}
.wl-state--demo .body{color:var(--vx-ember-400)}
.wl-state--insufficient .body,.wl-state--empty .body{color:var(--vx-text-muted)}
.wl-state--stale .body{color:var(--vx-warning)}
.wl-state--offline .body{color:var(--vx-text-muted)}
.wl-state--error .body{color:var(--vx-negative)}
.wl-skel{width:100%;height:22px;border-radius:6px;background:linear-gradient(100deg,rgba(255,255,255,.03),rgba(255,255,255,.09),rgba(255,255,255,.03));
  background-size:200% 100%;animation:wlsh 1.4s ease-in-out infinite}
@keyframes wlsh{0%{background-position:200% 0}100%{background-position:-200% 0}}

/* ── formes ── */
.wl-aura{position:relative;display:grid;place-items:center}
.wl-aura-txt{position:absolute;text-align:center;display:flex;flex-direction:column}
.wl-aura-txt .n{font-size:15px;font-weight:800;color:var(--vx-text-primary);max-width:120px;line-height:1.1}
.wl-aura-txt .c{font-size:10.5px;color:var(--vx-text-muted);margin-top:3px}
.wl-comb{display:flex;gap:6px;align-items:flex-end;height:90px}
.wl-comb-b{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:3px;height:100%}
.wl-comb-b .i{width:70%;border-radius:3px 3px 0 0;min-height:10px}
.wl-comb-b .l{font-size:9px;color:var(--vx-text-faint)}
.wl-comb-b b{font-size:10px;font-weight:700;color:var(--vx-text-secondary);font-variant-numeric:tabular-nums}
.wl-comb--m .wl-comb-b--m{justify-content:center;position:relative}
.wl-comb--m .up{width:70%;border-radius:3px 3px 0 0}.wl-comb--m .dn{width:70%;border-radius:0 0 3px 3px}
.wl-spark{display:block}
.wl-dial{display:block;margin:0 auto}
.wl-dial-read{font-size:11px;color:var(--vx-text-muted);text-align:center;margin-top:4px;max-width:150px}
.wl-rail-wrap{width:180px}
.wl-rail{position:relative;height:10px;border-radius:6px;background:rgba(0,0,0,.35);overflow:hidden}
.wl-rail .fill{position:absolute;inset:0;opacity:.5}
.wl-rail .mark{position:absolute;top:-3px;width:4px;height:16px;border-radius:3px;background:var(--vx-ember-500);transform:translateX(-50%);box-shadow:0 0 8px var(--vx-ember-glow)}
.wl-rail-sc{display:flex;justify-content:space-between;font-size:9.5px;color:var(--vx-text-muted);margin-top:5px}
.wl-ring{display:block}
.wl-spine{display:flex;align-items:flex-end;gap:10px;height:120px}
.wl-spine .col{width:26px;height:100%;border-radius:8px;background:rgba(0,0,0,.35);display:flex;align-items:flex-end;overflow:hidden}
.wl-spine .col i{width:100%;background:linear-gradient(180deg,var(--vx-ember-400),var(--vx-ember-600));border-radius:8px}
.wl-spine-l{display:flex;flex-direction:column;justify-content:flex-end}
.wl-spine-l b{font-size:24px;font-weight:800;font-variant-numeric:tabular-nums}
.wl-spine-l span{font-size:10px;color:var(--vx-text-muted)}
.wl-thermo{display:flex;align-items:center;gap:10px}
.wl-thermo .col{position:relative;width:22px;height:100%;border-radius:11px;
  background:linear-gradient(180deg,var(--vx-positive),var(--vx-warning),var(--vx-negative))}
.wl-thermo .mark{position:absolute;left:-3px;right:-3px;height:4px;border-radius:3px;background:var(--vx-ember-500);box-shadow:0 0 8px var(--vx-ember-glow)}
.wl-thermo-sc{display:flex;flex-direction:column;justify-content:space-between;height:100%;font-size:9px;color:var(--vx-text-muted)}
.wl-thermo-v{font-size:22px;font-weight:800;font-variant-numeric:tabular-nums}
.wl-thermo-v small{font-size:10px;color:var(--vx-text-muted);margin-left:3px}
.wl-tide{display:block}
.wl-reactor{display:flex;gap:16px;align-items:center;width:100%;max-width:360px}
.wl-reactor .core{width:78px;height:78px;flex:0 0 78px;border-radius:50%;display:grid;place-items:center;flex-direction:column;
  border:2px solid var(--c);box-shadow:0 0 22px -6px var(--c),inset 0 0 18px -8px var(--c)}
.wl-reactor .core b{font-size:26px;font-weight:800;line-height:1}.wl-reactor .core span{font-size:9px;color:var(--vx-text-muted)}
.wl-reactor .rods{flex:1;display:flex;flex-direction:column;gap:7px}
.wl-reactor-row{display:grid;grid-template-columns:88px 1fr 26px;align-items:center;gap:8px}
.wl-reactor-row .k{font-size:11px;color:var(--vx-text-secondary)}.wl-reactor-row .k small{color:var(--vx-text-faint);margin-left:4px}
.wl-reactor-row .bar{height:6px;border-radius:4px;background:rgba(0,0,0,.35);overflow:hidden}
.wl-reactor-row .bar i{display:block;height:100%;background:var(--vx-warm-grey);border-radius:4px}
.wl-reactor-row .v{font-size:11px;font-weight:700;text-align:right;font-variant-numeric:tabular-nums}
.wl-ledge{display:block}
.wl-kpi{min-width:150px;padding:12px;border-radius:12px;background:var(--vx-surface-elevated);border:1px solid var(--vx-border-soft);display:flex;flex-direction:column;gap:3px}
.wl-kpi .l{font-size:11px;color:var(--vx-text-muted)}
.wl-kpi .v{font-size:20px;font-weight:800;font-variant-numeric:tabular-nums}
.wl-kpi .d{font-size:12px;font-weight:700}.wl-kpi .d.pos{color:var(--vx-positive)}.wl-kpi .d.neg{color:var(--vx-negative)}.wl-kpi .d.mut{color:var(--vx-text-muted)}
.wl-grade{display:inline-grid;place-items:center;min-width:26px;height:24px;padding:0 8px;border-radius:8px;font-weight:800;font-size:13px;color:var(--vx-text-primary);border:1px solid var(--vx-border-strong)}
.wl-grade.hot{color:var(--vx-ember-ink);background:var(--vx-brand-gradient);border:none}
.wl-live{display:inline-flex;align-items:center;gap:6px;font-size:11px;padding:3px 10px;border-radius:999px;border:1px solid var(--vx-border-soft);background:rgba(0,0,0,.25);color:var(--vx-text-secondary)}
.wl-live .dot{width:7px;height:7px;border-radius:50%;background:var(--vx-text-muted)}
.wl-live[data-live="live"] .dot{background:var(--vx-positive);box-shadow:0 0 0 3px rgba(46,214,161,.18),0 0 8px var(--vx-positive);animation:wlpulse 1.8s ease-in-out infinite}
.wl-live[data-live="delayed"] .dot{background:var(--vx-warning)}.wl-live[data-live="fallback"] .dot{background:var(--vx-ember-500)}
@keyframes wlpulse{0%,100%{opacity:1}50%{opacity:.5}}
.wl-slab{min-width:220px}
.wl-slab-v{font-size:26px;font-weight:850;margin-bottom:8px}
.wl-slab-v[data-tone="risk"]{color:var(--vx-negative)}.wl-slab-v[data-tone="go"]{color:var(--vx-positive)}
.wl-slab .kv{display:flex;justify-content:space-between;gap:12px;font-size:12px;padding:3px 0;border-bottom:1px dashed var(--vx-border-soft)}
.wl-slab .kv span{color:var(--vx-text-muted)}.wl-slab .kv b{color:var(--vx-text-primary)}
.wl-dom{display:grid;grid-template-columns:1fr 1.3fr;gap:0;width:100%;max-width:640px;border:1px solid var(--vx-border-strong);border-radius:14px;overflow:hidden;
  background:radial-gradient(120% 120% at 100% 0%,rgba(255,109,41,.12),transparent 55%),linear-gradient(180deg,rgba(37,29,27,.6),rgba(22,19,22,.6))}
.wl-dom-l{padding:14px;border-right:1px solid var(--vx-border-soft);display:flex;flex-direction:column;gap:8px}
.wl-dom-l .badge{font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--vx-ember-400)}
.wl-dom-l .tk{display:flex;align-items:center;gap:10px}.wl-dom-l .sym{font-size:30px;font-weight:850}
.wl-dom-l .sub{font-size:12px;color:var(--vx-text-secondary)}
.wl-dom-l .score b{font-size:38px;font-weight:850;font-variant-numeric:tabular-nums}.wl-dom-l .score span{font-size:12px;color:var(--vx-text-muted);margin-left:4px}
.wl-dom-r{padding:14px;display:flex;flex-direction:column;gap:10px}
.wl-dom-r .grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.wl-dom-r .m{padding:8px 10px;border-radius:10px;background:var(--vx-surface);border:1px solid var(--vx-border-soft)}
.wl-dom-r .m.hot{border-color:rgba(255,109,41,.4)}.wl-dom-r .m.hot b{color:var(--vx-ember-400)}
.wl-dom-r .m span{display:block;font-size:10px;color:var(--vx-text-muted)}.wl-dom-r .m b{font-size:17px;font-weight:750;font-variant-numeric:tabular-nums}
.wl-cta{margin-top:auto;font:inherit;font-size:13px;font-weight:650;padding:9px 14px;border-radius:10px;border:none;color:var(--vx-ember-ink);background:var(--vx-brand-gradient);cursor:pointer}
.wl-idx{min-width:210px;padding:12px;border-radius:12px;position:relative;overflow:hidden;background:linear-gradient(180deg,rgba(37,29,27,.6),rgba(22,19,22,.55));border:1px solid var(--vx-border-soft)}
.wl-idx::after{content:"";position:absolute;left:0;top:12px;bottom:12px;width:3px;border-radius:3px;background:var(--vx-warm-grey)}
.wl-idx[data-dir="up"]::after{background:var(--vx-positive)}.wl-idx[data-dir="down"]::after{background:var(--vx-negative)}
.wl-idx .top{display:flex;align-items:center;gap:8px;margin-bottom:6px}
.wl-idx .mono{font-size:10px;font-weight:800;color:var(--vx-ember-400);background:var(--vx-ember-soft);border:1px solid rgba(255,109,41,.2);padding:2px 6px;border-radius:6px}
.wl-idx .nm{font-size:12px;font-weight:650}.wl-idx .rel{margin-left:auto;font-size:10px;color:var(--vx-text-secondary);border:1px solid var(--vx-border-soft);border-radius:999px;padding:2px 7px}
.wl-idx .vr{display:flex;align-items:baseline;gap:8px}.wl-idx .val{font-size:22px;font-weight:800;font-variant-numeric:tabular-nums}
.wl-idx .chg{font-size:12px;font-weight:700}.wl-idx .chg.pos{color:var(--vx-positive)}.wl-idx .chg.neg{color:var(--vx-negative)}
.wl-idx .ft{font-size:11px;color:var(--vx-text-muted);margin-top:6px}
.wl-cmp{border-collapse:separate;border-spacing:0;font-size:12px;min-width:320px}
.wl-cmp th,.wl-cmp td{padding:6px 10px;text-align:left;border-bottom:1px solid var(--vx-border-soft)}
.wl-cmp th{font-size:11px;color:var(--vx-text-muted)}.wl-cmp th.best{color:var(--vx-ember-400);font-weight:750}
.wl-cmp td.mt{color:var(--vx-text-secondary)}
.wl-cmp .cmp{display:flex;align-items:center;gap:6px}.wl-cmp .rail{flex:1;min-width:40px;height:6px;border-radius:4px;background:rgba(0,0,0,.35);overflow:hidden}
.wl-cmp .rail i{display:block;height:100%;background:var(--vx-warm-grey);border-radius:4px}.wl-cmp .cmp.win .rail i{background:var(--vx-ember-500)}
.wl-cmp .n{font-size:11px;font-weight:700;min-width:28px;text-align:right;font-variant-numeric:tabular-nums}.wl-cmp .cmp.win .n{color:var(--vx-ember-400)}

/* ═══ MATIÈRES (6 tiers) — chaque variante peut porter une matière distincte ═══ */
.wl-surf{position:relative;border-radius:14px;padding:14px;width:100%;overflow:hidden;
  border:1px solid var(--wl-eo,rgba(0,0,0,.55));
  box-shadow:0 12px 30px -16px rgba(0,0,0,.75), inset 0 1px 0 var(--wl-ei,rgba(255,255,255,.05));
  transition:transform .18s cubic-bezier(.23,1,.32,1),box-shadow .18s,border-color .18s}
.wl-surf::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:var(--wl-noise);
  background-size:140px;opacity:.035;mix-blend-mode:overlay}
.wl-surf:hover{transform:translateY(-2px);box-shadow:0 18px 44px -18px rgba(0,0,0,.85),inset 0 1px 0 var(--wl-ei,rgba(255,255,255,.07))}
.wl-surf:focus-within{box-shadow:0 22px 50px -18px rgba(0,0,0,.9),0 0 0 1px var(--wl-eo)}
.wl-surf--matte{background:linear-gradient(180deg,#1b1719,#141012);--wl-ei:rgba(255,255,255,.04)}
.wl-surf--smoked{background:linear-gradient(180deg,rgba(36,29,30,.62),rgba(20,17,19,.5));-webkit-backdrop-filter:blur(12px) saturate(1.12);backdrop-filter:blur(12px) saturate(1.12);--wl-ei:rgba(255,255,255,.06)}
.wl-surf--polished{background:linear-gradient(180deg,rgba(44,35,33,.72),rgba(22,18,20,.6));--wl-ei:rgba(255,255,255,.10)}
.wl-surf--polished::after{content:"";position:absolute;left:0;right:0;top:0;height:42%;pointer-events:none;
  background:linear-gradient(180deg,rgba(255,255,255,.07),transparent)}
.wl-surf--deepblack{background:radial-gradient(130% 100% at 50% -12%,rgba(44,26,18,.28),#07060a 68%);--wl-ei:rgba(255,255,255,.03);--wl-eo:#000}
.wl-surf--metal{background:linear-gradient(115deg,#251e1c,#1a1517 38%,#241c1a 60%,#150f0e);--wl-ei:rgba(255,224,196,.09)}
.wl-surf--metal::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(115deg,rgba(255,220,190,.05),transparent 30%,rgba(255,220,190,.04) 70%,transparent)}
.wl-surf--frosted{background:linear-gradient(180deg,rgba(64,56,58,.34),rgba(30,26,30,.3));-webkit-backdrop-filter:blur(18px) saturate(1.2) brightness(1.05);backdrop-filter:blur(18px) saturate(1.2) brightness(1.05);--wl-ei:rgba(255,255,255,.13)}
/* étiquette de matière + glow local sur la donnée active */
.wl-mat-tag{position:absolute;top:8px;right:8px;z-index:2;font-size:8.5px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--vx-text-faint);background:rgba(0,0,0,.35);border:1px solid var(--vx-border-soft);border-radius:6px;padding:2px 6px}
.wl-glow{filter:drop-shadow(0 0 5px var(--wl-acc,var(--vx-ember-glow)))}
/* LIVE : léger balayage de matière */
.wl-surf[data-live="1"]::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.05) 50%,transparent 70%);
  background-size:250% 100%;animation:wlsheen 4s linear infinite}
@keyframes wlsheen{0%{background-position:200% 0}100%{background-position:-60% 0}}

/* ═══ PALETTES PAR FAMILLE (l'orange reste réservé à l'identité/interaction) ═══ */
.wl-bench{--acc:var(--vx-warm-grey)}
.wl-bench[data-fam="Régime"]{--acc:var(--vx-positive)}
.wl-bench[data-fam="Momentum"]{--acc:#B6F04A}          /* vert citron — force */
.wl-bench[data-fam="Breadth"]{--acc:var(--vx-positive)}
.wl-bench[data-fam="Rotation"]{--acc:var(--vx-warm-grey)}
.wl-bench[data-fam="Volatilité"]{--acc:var(--vx-option)} /* violet électrique */
.wl-bench[data-fam="Opportunité"]{--acc:var(--vx-positive)}
.wl-bench[data-fam="Marchés"]{--acc:var(--vx-technical)}
.wl-bench[data-fam="Analyse"]{--acc:var(--vx-warning)}
.wl-bench[data-fam="Portefeuille"]{--acc:#E7E2DA}        /* blanc cassé — constellation */
.wl-bench[data-fam="Options"]{--acc:var(--vx-option)}
.wl-bench[data-fam="Journal"]{--acc:var(--vx-warning)}
.wl-bench[data-fam="Système"]{--acc:var(--vx-technical)}
.wl-fam-swatch{display:inline-block;width:10px;height:10px;border-radius:3px;background:var(--acc);vertical-align:middle;margin-left:6px}

/* ═══ MICRO-INTERACTIONS ═══ */
.wl-more{max-height:0;opacity:0;overflow:hidden;transition:max-height .2s cubic-bezier(.23,1,.32,1),opacity .2s;
  font-size:11px;color:var(--vx-text-muted)}
.wl-surf:hover .wl-more,.wl-surf:focus-within .wl-more{max-height:60px;opacity:1;margin-top:6px}
.wl-tip{position:relative}
.wl-tip::after{content:attr(data-tip);position:absolute;left:50%;bottom:calc(100% + 8px);transform:translateX(-50%) translateY(4px);
  background:var(--vx-surface-elevated);color:var(--vx-text-secondary);border:1px solid var(--vx-border-strong);border-radius:9px;
  padding:6px 9px;font-size:11px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .16s,transform .16s;z-index:9;
  box-shadow:0 10px 26px -12px rgba(0,0,0,.8)}
.wl-tip:hover::after{opacity:1;transform:translateX(-50%) translateY(0)}

/* ═══ APERÇU MOBILE ═══ */
.wl--mobile .wl-variants{flex-direction:column}
.wl--mobile .wl-tile{width:390px;max-width:100%}
.wl--mobile .wl-stage{min-height:auto}
.wl--mobile .wl-mobonly{display:block}
.wl-mobonly{display:none}
.wl--mobile .wl-deskonly{display:none}

/* reveal */
.wl-stage>*{animation:wlrev .22s cubic-bezier(.23,1,.32,1) both}
@keyframes wlrev{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
#wl-modal{background:var(--vx-surface-elevated);color:var(--vx-text-primary);border:1px solid var(--vx-border-strong);border-radius:14px;padding:18px;max-width:520px;width:90%}
#wl-modal::backdrop{background:rgba(0,0,0,.6)}
#wl-modal textarea{width:100%;background:var(--vx-canvas);color:var(--vx-text-secondary);border:1px solid var(--vx-border-soft);border-radius:8px;padding:8px;font-family:var(--vx-font-mono);font-size:11px}
.wl-modal-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:10px}
.wl-actions{flex-wrap:wrap}
@media (max-width:640px){.wl-dom{grid-template-columns:1fr}.wl-dom-l{border-right:none;border-bottom:1px solid var(--vx-border-soft)}
  .wl-top{flex-direction:column;align-items:flex-start;gap:8px}.wl-subbar{top:auto;position:static}
  .wl-actions{width:100%}.wl-legend{display:none}}
@media (prefers-reduced-motion:reduce){.wl-stage>*,.wl-live .dot,.wl-skel{animation:none!important}}
'''

_JS = r'''
(function(){
  var KEY='vxWidgetLabVerdicts';
  var store={};try{store=JSON.parse(localStorage.getItem(KEY)||'{}');}catch(e){}
  function apply(){document.querySelectorAll('.wl-tile').forEach(function(t){
    var v=store[t.dataset.wid];if(v)t.setAttribute('data-verdict',v);else t.removeAttribute('data-verdict');});}
  function save(){localStorage.setItem(KEY,JSON.stringify(store));}
  document.addEventListener('click',function(e){
    var btn=e.target.closest('.wl-verdict button');
    if(btn){var tile=btn.closest('.wl-tile');var wid=tile.dataset.wid;var v=btn.dataset.v;
      if(store[wid]===v){delete store[wid];}else{store[wid]=v;}
      save();apply();return;}
  });
  var exportBtn=document.getElementById('wl-export');
  if(exportBtn)exportBtn.addEventListener('click',function(){
    var lines=Object.keys(store).sort().map(function(k){return k+' → '+store[k];});
    var out='VERTEX WIDGET LAB — choix\n'+(lines.length?lines.join('\n'):'(aucun choix)');
    document.getElementById('wl-out').value=out;
    var m=document.getElementById('wl-modal');if(m.showModal)m.showModal();});
  var resetBtn=document.getElementById('wl-reset');
  if(resetBtn)resetBtn.addEventListener('click',function(){
    if(confirm('Réinitialiser tous les choix ?')){store={};save();apply();}});
  var copyBtn=document.getElementById('wl-copy');
  if(copyBtn)copyBtn.addEventListener('click',function(){
    var ta=document.getElementById('wl-out');ta.select();try{document.execCommand('copy');}catch(e){}
    if(navigator.clipboard)navigator.clipboard.writeText(ta.value);copyBtn.textContent='Copié ✓';
    setTimeout(function(){copyBtn.textContent='Copier';},1200);});
  var closeBtn=document.getElementById('wl-close');
  if(closeBtn)closeBtn.addEventListener('click',function(){document.getElementById('wl-modal').close();});
  var mobBtn=document.getElementById('wl-mobile');
  if(mobBtn)mobBtn.addEventListener('click',function(){
    document.querySelector('.wl-main').classList.toggle('wl--mobile');
    mobBtn.classList.toggle('active');
    mobBtn.textContent=document.querySelector('.wl-main').classList.contains('wl--mobile')?'Aperçu desktop':'Aperçu mobile';});
  apply();
})();
'''
