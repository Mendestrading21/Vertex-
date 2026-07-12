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

_PAGE_JS = '<script src="/static/vertex/js/pages/options-intel.js" defer></script>'


def render(view: str = 'overview') -> str:
    view = view if view in dict(_VIEWS) else 'overview'
    content = (_STYLE + _HEADER.replace('%%TABS%%', _tabs(view))
               + _VIEW_CONTENT[view].replace('%%LOADING%%', _LOADING))
    return render_shell(
        title='Options Intelligence',
        active='opportunities',            # reste dans les 8 espaces (approfondissement)
        space_label='Options Intelligence',
        sub_label='Approfondissement d’Opportunités',
        page_label='options:%s' % view,
        content=content,
        page_js=_PAGE_JS)


__all__ = ['render']
