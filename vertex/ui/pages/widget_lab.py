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


# ── États honnêtes (bande d'états) ─────────────────────────────────────────
def _state(kind):
    m = {
        'loading': ('<div class="wl-skel"></div>', 'loading'),
        'empty': ('Aucune donnée — prochaine action proposée', 'empty'),
        'insufficient': ('Données insuffisantes — Vertex ne tranche pas', 'insufficient'),
        'stale': ('Périmé · il y a 3 h', 'stale'),
        'demo': ('DÉMO — échantillon', 'demo'),
        'live': (live_pill('live'), 'live'),
    }
    body, cls = m[kind]
    return f'<div class="wl-state wl-state--{cls}"><span class="lab">{kind}</span><div class="body">{body}</div></div>'


# ══ REGISTRE DES BENCHES ═══════════════════════════════════════════════════
# Chaque bench : (id, nom, famille, question, [(vlabel, html)...], [états])
def _benches():
    ALL_STATES = ['loading', 'empty', 'insufficient', 'stale', 'demo', 'live']
    return [
        ('W01', 'Regime Aura', 'Régime', 'Dans quel régime, avec quelle confiance ?', [
            ('V1 · halo', aura('Tendance haussière', 68, 'go')),
            ('V2 · défensif', aura('Risk-Off', 44, 'risk')),
            ('V3 · indéterminé', aura('Indéterminé', 0, 'off')),
            ('V4 · compact', aura('Chop', 52, 'wait', 130)),
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
        ('O-1', 'Primitives — KPI · Grade · Live · Delta', 'Primitives', 'Les briques atomiques', [
            ('KPI glass', kpi('S&P 500', '6 000', '+1,67 %', 'up', SPARK_UP)),
            ('KPI flat', kpi('Taux 10 ans', '3,00 %', '−0,02 pts', 'flat')),
            ('Grade seals', grade_seal('S+') + ' ' + grade_seal('S') + ' ' + grade_seal('A') + ' ' + grade_seal('B')),
            ('Live pills', live_pill('live') + ' ' + live_pill('delayed') + ' ' + live_pill('frozen') + ' ' + live_pill('fallback')),
        ], ['loading', 'empty']),
    ]


# ── Page ───────────────────────────────────────────────────────────────────
def render() -> str:
    benches = _benches()
    families = []
    for b in benches:
        if b[2] not in families:
            families.append(b[2])
    nav = ''.join(f'<a href="#fam-{i}" class="wl-navchip">{f}</a>' for i, f in enumerate(families))

    sections = ''
    last_fam = None
    for (wid, name, fam, q, variants, states) in benches:
        if fam != last_fam:
            fi = families.index(fam)
            sections += f'<h2 id="fam-{fi}" class="wl-fam">{fam}</h2>'
            last_fam = fam
        tiles = ''
        for vlabel, html in variants:
            vid = f'{wid}-{vlabel.split(" ")[0]}'
            tiles += f'''<div class="wl-tile" data-wid="{vid}">
      <div class="wl-tile-head"><span class="vlab">{vlabel}</span>
        <span class="wl-verdict">
          <button data-v="official" title="Officiel">◎</button>
          <button data-v="reference" title="Référence">★</button>
          <button data-v="rejected" title="Rejeté">✕</button></span></div>
      <div class="wl-stage">{html}</div></div>'''
        strip = ''.join(_state(s) for s in states)
        sections += f'''<section class="wl-bench">
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
  font-family:var(--vx-font);-webkit-font-smoothing:antialiased;line-height:1.5}
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
.wl-stage{display:grid;place-items:center;min-height:120px;padding:8px;border-radius:9px;background:rgba(0,0,0,.16);overflow-x:auto}
.wl-stage>*{max-width:100%}
.wl-cmp{max-width:none}
.wl-states-label{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--vx-text-faint);margin:16px 0 8px}
.wl-states{display:flex;flex-wrap:wrap;gap:8px}
.wl-state{min-width:130px;border:1px dashed var(--vx-border-soft);border-radius:10px;padding:8px;background:rgba(0,0,0,.2)}
.wl-state .lab{font-size:9.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--vx-text-faint);display:block;margin-bottom:5px}
.wl-state .body{font-size:11px;color:var(--vx-text-secondary);min-height:24px;display:flex;align-items:center}
.wl-state--demo .body{color:var(--vx-ember-400)}
.wl-state--insufficient .body,.wl-state--empty .body{color:var(--vx-text-muted)}
.wl-state--stale .body{color:var(--vx-warning)}
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

/* reveal */
.wl-stage>*{animation:wlrev .22s cubic-bezier(.23,1,.32,1) both}
@keyframes wlrev{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
#wl-modal{background:var(--vx-surface-elevated);color:var(--vx-text-primary);border:1px solid var(--vx-border-strong);border-radius:14px;padding:18px;max-width:520px;width:90%}
#wl-modal::backdrop{background:rgba(0,0,0,.6)}
#wl-modal textarea{width:100%;background:var(--vx-canvas);color:var(--vx-text-secondary);border:1px solid var(--vx-border-soft);border-radius:8px;padding:8px;font-family:var(--vx-font-mono);font-size:11px}
.wl-modal-actions{display:flex;gap:8px;justify-content:flex-end;margin-top:10px}
@media (max-width:640px){.wl-dom{grid-template-columns:1fr}.wl-dom-l{border-right:none;border-bottom:1px solid var(--vx-border-soft)}
  .wl-top{flex-direction:column;align-items:flex-start;gap:8px}.wl-subbar{top:96px}}
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
  apply();
})();
'''
