"""vertex.ui.pages.options_intel_page — l'espace Options Intelligence (§18).

Question : « Où est la meilleure convexité, à quel prix de volatilité, et
quel événement la menace ? » Accessible via /options — PAS un 9e espace de
navigation : la barre reste à huit espaces, cette page est un approfondissement
d'Opportunités (le nav met « Opportunités » en actif). Sous-vues (?view=) :
overview · volatility · radar · events.

Le module Python n'invente aucun chiffre : il assemble le squelette + le
script client ; toutes les données viennent de /api/options/* (moteurs purs
volatility/expected_move/event_risk/overview). Donnée absente → état honnête.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell

_VIEWS = (
    ('overview', 'Vue d’ensemble'),
    ('volatility', 'Volatilité'),
    ('radar', 'Radar contrats'),
    ('scenarios', 'Scénarios'),
    ('events', 'Événements'),
)


def _tabs(view: str) -> str:
    items = []
    for vid, label in _VIEWS:
        sel = 'true' if vid == view else 'false'
        items.append('<a class="vx-tab" role="tab" href="?view=%s" '
                     'aria-selected="%s" data-view-tab="%s">%s</a>' % (vid, sel, vid, label))
    return ('<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Options">'
            + ''.join(items) + '</nav>')


_STYLE = """
<style>
#vx-content .vx-stats-row{display:flex;flex-wrap:wrap;gap:.75rem 1.5rem;padding:.4rem 0}
#vx-content .vx-stat{display:flex;flex-direction:column;min-width:92px}
#vx-content .vx-stat-label{font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--vx-text-dim,#8a837a)}
#vx-content .vx-stat-value{font-size:20px;font-weight:650;color:var(--vx-text,#efe7dc);margin-top:.15rem}
#vx-content .vx-verdict{padding:.2rem 0}
#vx-content .vx-lead{font-size:16px;line-height:1.45;margin:.35rem 0 .2rem;color:var(--vx-text,#efe7dc)}
#vx-content .vx-verdict .vx-sub{color:var(--vx-text-dim,#8a837a);font-size:13.5px}
#vx-content .vx-muted{color:var(--vx-text-dim,#8a837a);font-size:12.5px}
.vx-badge[data-tone="pos"]{color:var(--vx-positive,#38b879);border-color:var(--vx-positive,#38b879)}
.vx-badge[data-tone="neg"]{color:var(--vx-negative,#dc5f52);border-color:var(--vx-negative,#dc5f52)}
.vx-badge[data-tone="neutral"]{color:var(--vx-text-dim,#c8ad8d);border-color:var(--vx-border,#3a332c)}
#vx-content .vx-demo-tag{display:inline-block;font-size:11px;font-weight:650;letter-spacing:.03em;
  color:var(--vx-orange-500,#cf6128);border:1px solid var(--vx-orange-500,#cf6128);border-radius:999px;
  padding:.1rem .55rem;margin-bottom:.6rem}
#vx-content .vx-field{display:flex;flex-direction:column;gap:.3rem;max-width:260px;margin-bottom:.6rem}
#vx-content .vx-field span{font-size:12px;color:var(--vx-text-dim,#8a837a)}
.vx-explain h3{font-size:16px;margin:0 0 .5rem}
.vx-explain h4{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--vx-text-dim,#8a837a);margin:.9rem 0 .3rem}
.vx-explain .vx-grid2{display:grid;grid-template-columns:1fr 1fr;gap:1rem}
.vx-explain ul{margin:.2rem 0;padding-left:1.1rem}
.vx-explain li{margin:.15rem 0;font-size:13.5px}
@media(max-width:640px){.vx-explain .vx-grid2{grid-template-columns:1fr}}
#vx-content .vx-opt-hero-grid{display:grid;grid-template-columns:220px 1fr;gap:1.6rem;align-items:center}
#vx-content .vx-opt-gauge{display:flex;flex-direction:column;gap:.45rem;align-items:flex-start}
#vx-content .vx-opt-gauge-score{font-size:44px;font-weight:700;line-height:1;color:var(--vx-text,#f1efeb)}
#vx-content .vx-opt-gauge-score small{font-size:16px;color:var(--vx-text-dim,#817c75);font-weight:500}
#vx-content .vx-opt-gauge-score[data-tone="pos"]{color:var(--vx-positive,#39b978)}
#vx-content .vx-opt-gauge-score[data-tone="neg"]{color:var(--vx-negative,#dc6254)}
#vx-content .vx-opt-gauge-track{width:100%;height:7px;border-radius:4px;background:rgba(255,255,255,.06);overflow:hidden}
#vx-content .vx-opt-gauge-track i{display:block;height:100%;border-radius:4px;background:var(--vx-orange-500,#cf6128);transition:width .32s ease}
#vx-content .vx-opt-gauge-track i[data-tone="pos"]{background:var(--vx-positive,#39b978)}
#vx-content .vx-opt-gauge-track i[data-tone="neg"]{background:var(--vx-negative,#dc6254)}
#vx-content .vx-opt-dims{display:flex;flex-direction:column;gap:.5rem}
#vx-content .vx-opt-dim{display:grid;grid-template-columns:140px 1fr 42px;gap:.6rem;align-items:center;font-size:13px}
#vx-content .vx-opt-dim-l{color:var(--vx-text-dim,#b6b1aa)}
#vx-content .vx-opt-dim-bar{height:6px;border-radius:4px;background:rgba(255,255,255,.06);overflow:hidden}
#vx-content .vx-opt-dim-bar i{display:block;height:100%;background:var(--vx-copper-light,#b9683d);border-radius:4px;transition:width .3s ease}
#vx-content .vx-opt-dim-v{text-align:right;color:var(--vx-text,#f1efeb);font-variant-numeric:tabular-nums}
#vx-content .vx-opt-pulse{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem;padding-top:.9rem;border-top:1px solid rgba(255,255,255,.06)}
#vx-content .vx-opt-chip{font-size:12px;padding:.25rem .6rem;border-radius:999px;background:var(--vx-surface-2,#1d1f22);color:var(--vx-text-dim,#b6b1aa)}
#vx-content .vx-opt-chip b{color:var(--vx-text,#f1efeb);font-weight:600}
@media(max-width:720px){#vx-content .vx-opt-hero-grid{grid-template-columns:1fr}}
</style>
"""

_HEADER = """
<div class="vx-page-header">
  <div><h1>Options Intelligence</h1>
  <div class="vx-sub">Où est la meilleure convexité, à quel prix de volatilité, et quel événement la menace ?</div></div>
  <div class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="/opportunities?view=options">← Opportunités · Options</a></div>
</div>
%%TABS%%
<div id="vx-demo-banner"></div>
"""

_LOADING = '<div class="vx-skeleton" style="height:120px"></div>'

_VIEW_CONTENT = {
    'overview': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12 vx-opt-hero" id="vx-opt-hero" aria-label="Environnement options">
    <div class="vx-card-header"><span class="vx-card-title">Environnement pour l'achat d'options</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm vx-btn-ghost" data-explain="environment">Comprendre ce graphique</button></span></div>
    <div id="vx-opt-hero-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-12" id="vx-opt-counters" aria-label="Compteurs options">
    <div class="vx-card-header"><span class="vx-card-title">Tableau d'options — synthèse</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm vx-btn-ghost" data-explain="overview">Comprendre ce graphique</button></span></div>
    <div id="vx-opt-counters-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-12" id="vx-opt-verdict" aria-label="Lecture dominante">
    <div class="vx-card-header"><span class="vx-card-title">Lecture dominante</span></div>
    <div id="vx-opt-verdict-body">%%LOADING%%</div>
  </section>
  <section class="vx-card vx-col-12" id="vx-opt-radar-lite" aria-label="Meilleurs contrats">
    <div class="vx-card-header"><span class="vx-card-title">Meilleurs contrats (radar)</span>
      <span class="vx-actions"><a class="vx-btn vx-btn-sm vx-btn-ghost" href="?view=radar">Tout voir →</a></span></div>
    <div id="vx-opt-radar-lite-body">%%LOADING%%</div>
  </section>
</div>
""",
    'volatility': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" aria-label="Sélecteur de titre">
    <div class="vx-card-header"><span class="vx-card-title">Volatilité par sous-jacent</span></div>
    <div class="vx-card-body">
      <label class="vx-field"><span>Symbole</span>
        <input id="vx-opt-vol-sym" class="vx-input" placeholder="ex. AAPL" maxlength="12" autocomplete="off"></label>
      <button class="vx-btn vx-btn-sm" id="vx-opt-vol-go">Interpréter</button>
    </div>
  </section>
  <section class="vx-card vx-col-12" id="vx-opt-vol-out" aria-label="Interprétation volatilité">
    <div class="vx-card-header"><span class="vx-card-title">Les options sont-elles chères ?</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm vx-btn-ghost" data-explain="volatility">Comprendre ce graphique</button></span></div>
    <div id="vx-opt-vol-out-body"><div class="vx-empty">Choisis un symbole présent dans le tableau d'options.</div></div>
  </section>
  <div class="vx-col-6" id="vx-opt-term"></div>
  <div class="vx-col-6" id="vx-opt-cone"></div>
  <div class="vx-col-6" id="vx-opt-oi"></div>
  <div class="vx-col-6" id="vx-opt-smile"></div>
</div>
""",
    'radar': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" id="vx-opt-radar" aria-label="Radar des contrats">
    <div class="vx-card-header"><span class="vx-card-title">Radar des contrats — qualité décroissante</span></div>
    <div id="vx-opt-radar-body">%%LOADING%%</div>
  </section>
</div>
""",
    'scenarios': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" aria-label="Sélecteur de titre">
    <div class="vx-card-header"><span class="vx-card-title">Scénarios du meilleur contrat</span></div>
    <div class="vx-card-body">
      <label class="vx-field"><span>Symbole</span>
        <input id="vx-opt-sc-sym" class="vx-input" placeholder="ex. GOOGL" maxlength="12" autocomplete="off"></label>
      <button class="vx-btn vx-btn-sm" id="vx-opt-sc-go">Simuler</button>
    </div>
  </section>
  <section class="vx-card vx-col-12" id="vx-opt-sc-out" aria-label="Scénarios">
    <div class="vx-card-header"><span class="vx-card-title">Que vaudra le contrat selon le spot, le temps et l'IV ?</span></div>
    <div id="vx-opt-sc-out-body"><div class="vx-empty">Choisis un symbole présent dans le tableau d'options.</div></div>
  </section>
</div>
""",
    'events': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" aria-label="Sélecteur de titre">
    <div class="vx-card-header"><span class="vx-card-title">Risque d'événement par titre</span></div>
    <div class="vx-card-body">
      <label class="vx-field"><span>Symbole</span>
        <input id="vx-opt-ev-sym" class="vx-input" placeholder="ex. AAPL" maxlength="12" autocomplete="off"></label>
      <button class="vx-btn vx-btn-sm" id="vx-opt-ev-go">Évaluer</button>
    </div>
  </section>
  <section class="vx-card vx-col-12" id="vx-opt-ev-out" aria-label="Interprétation événement">
    <div class="vx-card-header"><span class="vx-card-title">Un événement menace-t-il l'échéance ?</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm vx-btn-ghost" data-explain="event_risk">Comprendre ce graphique</button></span></div>
    <div id="vx-opt-ev-out-body"><div class="vx-empty">Choisis un symbole présent dans le tableau d'options.</div></div>
  </section>
</div>
""",
}

# Composants graphiques options + dépendances (bar/heatmap) — sinon VXCharts.thetaCard /
# ivSensitivityCard / scenarioMatrix sont undefined sur cette page (console-risk).
_PAGE_JS = (
    '<script src="/static/vertex/js/charts/bar-chart.js" defer></script>'
    '<script src="/static/vertex/js/charts/heatmap.js" defer></script>'
    '<script src="/static/vertex/js/charts/option-scenarios.js" defer></script>'
    '<script src="/static/vertex/js/charts/option-theta.js" defer></script>'
    '<script src="/static/vertex/js/charts/option-iv-sensitivity.js" defer></script>'
    '<script src="/static/vertex/js/pages/options-intel.js" defer></script>'
)


def render(view: str = 'overview') -> str:
    view = view if view in dict(_VIEWS) else 'overview'
    content = (_STYLE + _HEADER.replace('%%TABS%%', _tabs(view))
               + _VIEW_CONTENT[view].replace('%%LOADING%%', _LOADING))
    return render_shell(
        title='Options Intelligence',
        active='options',                  # espace principal Options (9e entrée nav)
        space_label='Options',
        sub_label='Options Intelligence',
        page_label='options:%s' % view,
        content=content,
        page_js=_PAGE_JS)


__all__ = ['render']
