"""vertex.ui.pages.options_intel_page — l'espace Options Intelligence (§18).

Question : « Où est la meilleure convexité, à quel prix de volatilité, et
quel événement la menace ? » Accessible via /options — ESPACE PRINCIPAL
CANONIQUE n°6 (le nav met « Options » en actif). Plus de double rattachement
ambigu à Opportunités. Sous-vues visibles (?view=) : structure · positioning ·
leaps · positions · volatility · events. Les anciens liens overview/radar/
scenarios restent servis et rattachés visuellement à Structure.

Le module Python n'invente aucun chiffre : il assemble le squelette + le
script client ; toutes les données viennent de /api/options/* (moteurs purs
volatility/expected_move/event_risk/overview). Donnée absente → état honnête.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell

# Onglets VISIBLES (canoniques PR n°6) — Structure d'abord : la Carte-Verdict
# Options répond « cette structure offre-t-elle une asymétrie suffisante ? ».
_VIEWS = (
    ('structure', 'Structure'),
    ('positioning', 'Positionnement'),
    ('leaps', 'LEAPS'),
    ('positions', 'Mes positions'),
    ('volatility', 'Volatilité'),
    ('events', 'Événements'),
)
# Vues encore servies (routes 200, contenu intact) mais hors barre d'onglets :
# overview/radar/scenarios restent accessibles/testées, absorbées par Structure.
_LEGACY_VIEWS = (
    ('overview', 'Vue d’ensemble'),
    ('radar', 'Radar contrats'),
    ('scenarios', 'Scénarios'),
)
_ALL_VIEWS = _VIEWS + _LEGACY_VIEWS
_VIEW_PARENT = {'overview': 'structure', 'radar': 'structure', 'scenarios': 'structure'}


def _tabs(view: str) -> str:
    items = []
    selected_view = _VIEW_PARENT.get(view, view)
    for vid, label in _VIEWS:
        sel = 'true' if vid == selected_view else 'false'
        items.append('<a class="vx-tab" role="tab" href="?view=%s" '
                     'aria-selected="%s" data-view-tab="%s">%s</a>' % (vid, sel, vid, label))
    return ('<nav class="vx-tabs" role="tablist" aria-label="Sous-vues Options">'
            + ''.join(items) + '</nav>')


_STYLE = ""  # styles Options migrés dans le CSS partagé canonique

_HEADER = """
<header class="vx-page-lead">
  <div class="vx-page-lead__main">
    <div class="vx-page-lead__eyebrow">Intelligence de convexité</div>
    <h1>Options</h1>
    <p class="vx-page-lead__summary">Mesurer l’asymétrie, le prix de la volatilité et le risque d’événement avant toute décision.</p>
    <div class="vx-page-lead__meta"><span class="vx-readonly-shield">Analyse uniquement · aucun ordre</span></div>
  </div>
</header>
%%TABS%%
<section class="vx-card vx-options-context vx-mt3" aria-label="Contexte du sous-jacent">
  <div class="vx-options-context__copy">
    <span class="vx-card-title">Sous-jacent actif</span>
    <span class="vx-meta">Conservé entre les vues Structure, Positionnement, LEAPS, Volatilité et Événements.</span>
  </div>
  <label class="vx-field vx-options-context__field"><span>Symbole</span>
    <input id="vx-options-symbol" class="vx-input" placeholder="ex. AAPL" maxlength="12" autocomplete="off" aria-label="Sous-jacent actif"></label>
  <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-options-apply">Actualiser l’analyse</button>
</section>
<div id="vx-demo-banner"></div>
"""

_LOADING = '<div class="vx-skeleton" style="height:120px"></div>'

_VIEW_CONTENT = {
    'structure': """
<div class="vx-options-local-bridge" hidden>
  <input id="vx-os-sym" tabindex="-1"><button id="vx-os-go" type="button">Actualiser</button>
</div>
<div id="vx-os-chips" class="vx-options-shortcuts vx-mt3" aria-label="Sous-jacents du tableau"></div>
<div id="vx-os-verdict" class="vx-mt3">%%LOADING%%</div>
<div id="vx-os-scenarios" class="vx-mt3"></div>
<div class="vx-hero-grid vx-mt3">
  <section class="vx-card vx-hero-main" aria-label="Payoff à l'échéance">
    <div class="vx-card-header"><span class="vx-card-title">Payoff à l'échéance</span>
      <span class="vx-chart-question">Où gagne / perd la structure selon le cours ?</span></div>
    <div id="vx-os-payoff"><div class="vx-empty">Choisis un sous-jacent présent dans le tableau d'options.</div></div>
  </section>
  <aside class="vx-card vx-insight-rail" aria-label="Sensibilités">
    <div class="vx-card-header"><span class="vx-card-title">Sensibilités (Greeks)</span></div>
    <div id="vx-os-greeks"><div class="vx-empty">—</div></div>
  </aside>
</div>
<details class="vx-disclosure vx-mt3">
  <summary>Comparer les contrats et voir la méthode</summary>
  <div class="vx-disclosure__body" id="vx-os-compare"></div>
</details>
""",
    'positioning': """
<div class="vx-options-local-bridge" hidden>
  <input id="vx-gx-sym" tabindex="-1"><button id="vx-gx-go" type="button">Actualiser</button>
</div>
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" aria-label="Radar de positionnement">
    <div class="vx-card-header"><span class="vx-card-title">Positionnement dealer — radar GEX</span>
      <span class="vx-chart-question">Tous les titres du tableau, classés par |net GEX|. Clique une ligne pour le détail.</span></div>
    <div id="vx-gx-radar">%%LOADING%%</div>
  </section>
</div>
<div id="vx-gx-thesis" class="vx-mt3"></div>
<div id="vx-gx-tiles" class="vx-mt3"></div>
<div class="vx-hero-grid vx-mt3">
  <section class="vx-card vx-hero-main" aria-label="GEX par strike">
    <div class="vx-card-header"><span class="vx-card-title">GEX par strike</span>
      <span class="vx-chart-question">Call GEX (+) vs Put GEX (−) — concentration de l'exposition gamma.</span></div>
    <div id="vx-gx-bars"><div class="vx-empty">Choisis un sous-jacent présent dans le tableau d'options.</div></div>
  </section>
  <aside class="vx-card vx-insight-rail" aria-label="Flux notable">
    <div class="vx-card-header"><span class="vx-card-title">Flux notable</span>
      <span class="vx-chart-question">Gros premium négocié du cycle (volume × prime) — pas un flux tick-par-tick.</span></div>
    <div id="vx-gx-flow"><div class="vx-empty">—</div></div>
  </aside>
</div>
<details class="vx-disclosure vx-mt3">
  <summary>Historique quotidien et copilote</summary>
  <div class="vx-disclosure__body vx-grid">
  <section class="vx-card vx-col-7" aria-label="GEX quotidien">
    <div class="vx-card-header"><span class="vx-card-title">GEX quotidien — le gamma s'empile-t-il&nbsp;?</span>
      <span class="vx-chart-question">Net GEX jour après jour (journal réel — un point par jour analysé, jamais inventé).</span></div>
    <div id="vx-gx-daily"><div class="vx-empty">L'historique se construit à chaque analyse — reviens demain pour la tendance.</div></div>
  </section>
  <section class="vx-card vx-col-5" aria-label="Copilote d'analyse">
    <div class="vx-card-header"><span class="vx-card-title">Copilote d'analyse</span>
      <span class="vx-chart-question">Pose une question — réponse ancrée dans les chiffres réels. Lecture seule, aucun ordre.</span></div>
    <div class="vx-card-body">
      <label class="vx-field" style="max-width:100%"><span>Ta question</span>
        <input id="vx-cp-q" class="vx-input" placeholder="ex. Que dit le positionnement sur ce titre ?" maxlength="500" autocomplete="off"></label>
      <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-cp-go">Demander au copilote</button>
      <div id="vx-cp-out" class="vx-mt2"></div>
    </div>
  </section>
  </div>
</details>
""",
    'leaps': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" aria-label="Scanner LEAPS">
    <div class="vx-card-header"><span class="vx-card-title">Scanner LEAPS — quels contrats longue échéance sont conformes&nbsp;?</span>
      <span class="vx-chart-question">Échéance 180–540 jours · hors-mandat visible · probabilité de doublement estimée, jamais présentée comme certaine.</span></div>
    <div class="vx-card-body vx-flex vx-wrap" style="gap:.6rem;align-items:flex-end">
      <label class="vx-field"><span>Filtre titre (optionnel)</span>
        <input id="vx-sc-sym" class="vx-input" placeholder="ex. NVDA" maxlength="12" autocomplete="off"></label>
      <button class="vx-btn vx-btn-sm vx-btn-primary" id="vx-sc-go">Scanner</button>
    </div>
    <div id="vx-sc-out" class="vx-mt2">%%LOADING%%</div>
  </section>
</div>
<details class="vx-disclosure vx-mt3">
  <summary>Comparer un horizon plus court</summary>
  <div class="vx-disclosure__body">
    <div id="vx-sc-tabs" class="vx-flex vx-wrap" style="gap:6px" role="group" aria-label="Univers d’options">
      <button class="vx-btn vx-btn-sm" data-universe="LEAPS">LEAPS · 180–540 j</button>
      <button class="vx-btn vx-btn-sm vx-btn-ghost" data-universe="SWING">Swing · 60–180 j</button>
      <button class="vx-btn vx-btn-sm vx-btn-ghost" data-universe="TACTICAL">Tactique · 20–60 j</button>
    </div>
    <p class="vx-meta vx-mt2">Ces horizons restent des comparaisons avancées ; la vue conserve LEAPS comme mandat principal.</p>
  </div>
</details>
<div class="vx-options-local-bridge" hidden>
  <input id="vx-lp-sym" tabindex="-1"><button id="vx-lp-go" type="button">Actualiser</button>
</div>
<div id="vx-lp-chips" class="vx-options-shortcuts vx-mt3" aria-label="Sous-jacents du tableau"></div>
<div id="vx-lp-out" class="vx-mt3"><div class="vx-empty">Choisis un sous-jacent pour lire ses contrats longue échéance.</div></div>
""",
    'positions': """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" aria-label="Exposition des positions options">
    <div class="vx-card-header"><span class="vx-card-title">Exposition et échéances</span>
      <span class="vx-readonly-shield">Suivi uniquement · aucun ordre</span></div>
    <p class="vx-card-conclusion">Repère d’abord les échéances proches, les pertes à contrôler et les positions dont les données sont incomplètes.</p>
  </section>
</div>
<div id="vx-op-body" class="vx-mt3">%%LOADING%%</div>
""",
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
<div class="vx-options-local-bridge" hidden>
  <input id="vx-opt-vol-sym" tabindex="-1"><button id="vx-opt-vol-go" type="button">Actualiser</button>
</div>
<div class="vx-hero-grid vx-mt3">
  <div class="vx-hero-main" id="vx-opt-term"></div>
  <aside class="vx-card vx-insight-rail" id="vx-opt-vol-out" aria-label="Interprétation volatilité">
    <div class="vx-card-header"><span class="vx-card-title">Les options sont-elles chères ?</span>
      <span class="vx-actions"><button class="vx-btn vx-btn-sm vx-btn-ghost" data-explain="volatility">Comprendre ce graphique</button></span></div>
    <div id="vx-opt-vol-out-body"><div class="vx-empty">Choisis un symbole présent dans le tableau d'options.</div></div>
  </aside>
</div>
<details class="vx-disclosure vx-mt3">
  <summary>Cône estimé, intérêt ouvert et smile</summary>
  <div class="vx-disclosure__body vx-grid">
    <div class="vx-col-4" id="vx-opt-cone"></div>
    <div class="vx-col-4" id="vx-opt-oi"></div>
    <div class="vx-col-4" id="vx-opt-smile"></div>
  </div>
</details>
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
<div class="vx-options-local-bridge" hidden>
  <input id="vx-opt-sc-sym" tabindex="-1"><button id="vx-opt-sc-go" type="button">Actualiser</button>
</div>
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" id="vx-opt-sc-out" aria-label="Scénarios">
    <div class="vx-card-header"><span class="vx-card-title">Que vaudra le contrat selon le spot, le temps et l'IV ?</span></div>
    <div id="vx-opt-sc-out-body"><div class="vx-empty">Choisis un symbole présent dans le tableau d'options.</div></div>
  </section>
  <section class="vx-card vx-col-12" id="vx-opt-strat" aria-label="Stratégies multi-jambes">
    <div class="vx-card-header"><span class="vx-card-title">Stratégies multi-jambes</span>
      <span class="vx-chart-question">Spreads, straddle, iron condor — payoff, probabilité de profit, gain/perte max & greeks (depuis le board d&#8217;options, aucun ordre)</span></div>
    <div id="vx-opt-strategies"><div class="vx-empty">Choisis un symbole pour construire les stratégies depuis le board.</div></div>
  </section>
</div>
""",
    'events': """
<div class="vx-options-local-bridge" hidden>
  <input id="vx-opt-ev-sym" tabindex="-1"><button id="vx-opt-ev-go" type="button">Actualiser</button>
</div>
<div class="vx-grid vx-mt3">
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
    '<script src="/static/vertex/js/pages/options-structure.js" defer></script>'
    '<script src="/static/vertex/js/pages/options-gex.js" defer></script>'
    '<script src="/static/vertex/js/pages/options-scanner.js" defer></script>'
    '<script src="/static/vertex/js/pages/options-context.js" defer></script>'
)


def render(view: str = 'structure') -> str:
    view = view if view in dict(_ALL_VIEWS) else 'structure'
    content = (_STYLE + _HEADER.replace('%%TABS%%', _tabs(view))
               + _VIEW_CONTENT[view].replace('%%LOADING%%', _LOADING))
    return render_shell(
        title='Options',
        active='options',                  # espace principal canonique (n°6 / 8)
        space_label='Options',
        sub_label=dict(_ALL_VIEWS).get(view, 'Structure'),
        page_label='options:%s' % view,
        content=content,
        page_js=_PAGE_JS)


__all__ = ['render']
