"""vertex.ui.pages.tracking_page — l'espace SUIVIS (§17).

« Que valent mes idées suivies depuis que je les ai marquées ? » Accessible via
/tracking — PAS un 9e espace de navigation : approfondissement du Portefeuille
(le nav met « Portefeuille » en actif). Tout gain affiché est HYPOTHÉTIQUE et
étiqueté comme tel — jamais un gain encaissé. Données réelles via /api/tracking.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell

_STYLE = """
<style>
#vx-content .vx-hypo{display:inline-block;font-size:11px;font-weight:650;letter-spacing:.03em;
  color:var(--vx-warning,#dda23b);border:1px solid var(--vx-warning,#dda23b);border-radius:999px;
  padding:.12rem .6rem}
#vx-content .vx-trk-note{color:var(--vx-text-dim,#8a837a);font-size:12.5px;margin:.4rem 0 0}
#vx-content .vx-pos{color:var(--vx-positive,#36c889)}
#vx-content .vx-neg{color:var(--vx-negative,#ed655c)}
#vx-content .vx-muted{color:var(--vx-text-dim,#8a837a)}
#vx-content .vx-stat{display:flex;flex-direction:column;min-width:88px}
#vx-content .vx-stat-label{font-size:11.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--vx-text-dim,#8a837a)}
#vx-content .vx-stat-value{font-size:20px;font-weight:650;color:var(--vx-text,#efe7dc);margin-top:.15rem}
</style>
"""

_HEADER = """
<div class="vx-page-header">
  <div><h1>Suivis</h1>
  <div class="vx-sub">Que valent mes idées suivies depuis que je les ai marquées ?</div></div>
  <div class="vx-actions"><span class="vx-hypo">Rendements 100 % hypothétiques</span>
    <a class="vx-btn vx-btn-sm vx-btn-ghost" href="/portfolio">← Portefeuille</a></div>
</div>
<div id="vx-demo-banner"></div>
"""

_CONTENT = """
<div class="vx-grid vx-mt3">
  <section class="vx-card vx-col-12" id="vx-trk-summary" aria-label="Résumé des suivis">
    <div class="vx-card-header"><span class="vx-card-title">Résumé</span></div>
    <div id="vx-trk-summary-body"><div class="vx-skeleton" style="height:60px"></div></div>
  </section>
  <div class="vx-col-12" id="vx-trk-chart"></div>
  <section class="vx-card vx-col-12" id="vx-trk-active" aria-label="Suivis actifs">
    <div class="vx-card-header"><span class="vx-card-title">Suivis actifs</span></div>
    <div id="vx-trk-active-body"><div class="vx-skeleton" style="height:160px"></div></div>
    <p class="vx-trk-note">Un suivi est une idée marquée : Vertex mesure sa performance
      <b>hypothétique</b> depuis l'horodatage du suivi, contre SPY. Ce n'est jamais une
      position réelle ni un gain encaissé.</p>
  </section>
  <section class="vx-card vx-col-12" id="vx-trk-stopped" aria-label="Suivis clôturés">
    <div class="vx-card-header"><span class="vx-card-title">Suivis clôturés (historique)</span></div>
    <div id="vx-trk-stopped-body"><div class="vx-empty">—</div></div>
  </section>
</div>
"""

_PAGE_JS = '<script src="/static/vertex/js/pages/tracking.js" defer></script>'


def render() -> str:
    content = _STYLE + _HEADER + _CONTENT
    return render_shell(
        title='Suivis', active='portfolio', space_label='Suivis',
        sub_label='Approfondissement du Portefeuille', page_label='tracking',
        content=content, page_js=_PAGE_JS)


__all__ = ['render']
