"""vertex.ui.pages.design_system_demo — page interne de démonstration (§35).

Vitrine READONLY du Tactile Command Surface : boutons, chips, onglets, segmented,
bulles/badges, toggles, sliders, cartes sélectionnables. Aucune donnée, aucun ordre,
aucune logique métier — uniquement l'affichage des composants pour validation visuelle.
"""
from __future__ import annotations

from vertex.ui.shell import render_shell


def _btn_row():
    return (
        '<div class="vx-flex vx-wrap" style="gap:.5rem;align-items:center">'
        '<button class="vx-btn vx-btn-primary">Analyser</button>'
        '<button class="vx-btn vx-btn-secondary">Comparer</button>'
        '<button class="vx-btn">Voir le détail</button>'
        '<button class="vx-btn vx-btn-soft">Suivre</button>'
        '<button class="vx-btn vx-btn-ghost">Fermer</button>'
        '<button class="vx-btn vx-btn-danger">Supprimer</button>'
        '<button class="vx-btn vx-btn-icon" aria-label="Favori">★</button>'
        '<button class="vx-btn" disabled title="Comparaison indisponible : sélectionnez au moins deux contrats.">Comparer (désactivé)</button>'
        '</div>'
    )


def _states_row():
    return (
        '<div class="vx-flex vx-wrap" style="gap:.5rem;align-items:center">'
        '<button class="vx-btn vx-btn-primary" data-state="loading">Chargement</button>'
        '<button class="vx-btn" data-state="success">Réussi</button>'
        '<button class="vx-btn" data-state="error">Erreur</button>'
        '<button class="vx-btn vx-btn-sm vx-btn-primary">SM primary</button>'
        '<button class="vx-btn vx-btn-sm">SM</button>'
        '</div>'
    )


def _chips_row():
    chips = [('Actionnable', True, 5), ('À suivre', False, 12), ('Attaque', True, 8),
             ('Milieu', False, 6), ('Défense', False, 4), ('CALL', True, 7), ('PUT tactique', False, 1)]
    out = '<div class="vx-flex vx-wrap" style="gap:.4rem">'
    for label, active, n in chips:
        out += (f'<button class="vx-chip" aria-pressed="{"true" if active else "false"}">{label}'
                f'<span class="vx-filter-count">{n}</span></button>')
    out += '</div>'
    return out


def _bubbles_row():
    dec = ['ACHETER', 'ATTENDRE', 'REFUSER', 'RENFORCER', 'SURVEILLER']
    out = '<div class="vx-flex vx-wrap" style="gap:.4rem;align-items:center">'
    for d in dec:
        out += f'<span class="vx-badge vx-badge-decision" data-decision="{d}">{d}</span>'
    out += ('<span class="vx-badge">LIVE</span><span class="vx-badge" style="color:var(--vx-warning)">DELAYED</span>'
            '<span class="vx-badge" style="color:var(--vx-option,#806095)">CALL</span>'
            '<span class="vx-badge">82 <b class="vx-mono">/100</b></span></div>')
    return out


def _tabs_row():
    tabs = ['Vue d’ensemble', 'Macro', 'Secteurs', 'Breadth', 'Volatilité']
    out = '<nav class="vx-tabs" role="tablist" aria-label="Démo onglets">'
    for i, t in enumerate(tabs):
        out += f'<a class="vx-tab" role="tab" aria-selected="{"true" if i == 0 else "false"}" href="#">{t}</a>'
    out += '</nav>'
    return out


def _segmented_row():
    return (
        '<div class="vx-segmented" role="group" aria-label="Densité">'
        '<button aria-pressed="false">Compact</button>'
        '<button aria-pressed="true">Confort</button>'
        '<button aria-pressed="false">Dense</button></div>'
        '<div class="vx-segmented vx-ml2" role="group" aria-label="Vue" style="margin-left:.6rem">'
        '<button aria-pressed="true">Graphique</button>'
        '<button aria-pressed="false">Tableau</button></div>'
    )


def _cards_row():
    return (
        '<div class="vx-grid">'
        '<section class="vx-card vx-col-4" style="border-color:rgba(207,97,40,.45);box-shadow:0 6px 18px rgba(126,47,13,.18)">'
        '<div class="vx-flex"><b>Meilleur compromis</b><span class="vx-grow"></span>'
        '<span class="vx-badge vx-badge-decision" data-decision="ACHETER">Recommandé</span></div>'
        '<div class="vx-meta vx-mt1">Δ 0,45 · DTE 120 j · R:R 3</div></section>'
        '<section class="vx-card vx-col-4"><div class="vx-flex"><b>Plus défensif</b></div>'
        '<div class="vx-meta vx-mt1">Δ 0,60 · DTE 150 j · R:R 2</div></section>'
        '<section class="vx-card vx-col-4" style="opacity:.6"><div class="vx-flex"><b>Bloqué 🔒</b></div>'
        '<div class="vx-meta vx-mt1">Liquidité insuffisante (OI &lt; 100)</div></section>'
        '</div>'
    )


_STYLE = """
<style>
#vx-ds section.vx-card{margin-bottom:0}
#vx-ds .vx-ds-block{margin-bottom:1.4rem}
#vx-ds .vx-ds-block>.vx-meta{text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5rem}
#vx-ds .vx-range{width:220px;accent-color:var(--vx-orange-500,#cf6128)}
#vx-ds .vx-switch{width:40px;height:22px;border-radius:99px;background:var(--vx-surface-3,#17191b);
  border:1px solid var(--vx-border-soft,rgba(255,255,255,.08));position:relative;cursor:pointer;display:inline-block}
#vx-ds .vx-switch[data-on="1"]{background:var(--vx-orange-500,#cf6128)}
#vx-ds .vx-switch::after{content:"";position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:99px;
  background:#f4f1ec;transition:transform .16s ease}
#vx-ds .vx-switch[data-on="1"]::after{transform:translateX(18px)}
</style>
"""


def render() -> str:
    def block(title, body):
        return (f'<section class="vx-card vx-ds-block"><div class="vx-meta">{title}</div>{body}</section>')

    sliders = (
        '<div class="vx-flex vx-wrap" style="gap:1.2rem;align-items:center">'
        '<label>DTE <b class="vx-mono">120 j</b><br><input type="range" class="vx-range" min="60" max="270" value="120"></label>'
        '<label>Delta <b class="vx-mono">0,45</b><br><input type="range" class="vx-range" min="20" max="85" value="45"></label>'
        '<label>IV Rank <b class="vx-mono">72</b><br><input type="range" class="vx-range" min="0" max="100" value="72"></label>'
        '<label>Score min <b class="vx-mono">70</b><br><input type="range" class="vx-range" min="0" max="100" value="70"></label>'
        '</div>')
    toggles = (
        '<div class="vx-flex vx-wrap" style="gap:1.4rem;align-items:center">'
        '<label class="vx-flex" style="gap:.5rem"><span class="vx-switch" data-on="1" role="switch" aria-checked="true"></span> Annotations</label>'
        '<label class="vx-flex" style="gap:.5rem"><span class="vx-switch" data-on="0" role="switch" aria-checked="false"></span> Benchmark</label>'
        '<label class="vx-flex" style="gap:.5rem"><span class="vx-switch" data-on="1" role="switch" aria-checked="true"></span> Événements</label>'
        '</div>')

    content = (
        _STYLE
        + '<div class="vx-page-header"><div><h1>Design System — Command Surface</h1>'
        '<div class="vx-sub">Vitrine READONLY des contrôles tactiles (boutons, chips, onglets, bulles, sliders). Aucune donnée, aucun ordre.</div></div></div>'
        + '<div id="vx-ds">'
        + block('Boutons — hiérarchie', _btn_row())
        + block('Boutons — états', _states_row())
        + block('Chips / filtres', _chips_row() + '<div class="vx-mt2"><button class="vx-btn vx-btn-sm vx-btn-ghost">Effacer les filtres</button></div>')
        + block('Bulles & badges (décision / statut / score)', _bubbles_row())
        + block('Onglets', _tabs_row())
        + block('Segmented controls', _segmented_row())
        + block('Toggles / switches', toggles)
        + block('Sliders', sliders)
        + block('Cartes sélectionnables (Contract Optimizer)', _cards_row())
        + '</div>'
        + '<script>document.querySelectorAll("#vx-ds .vx-switch").forEach(function(s){'
          's.addEventListener("click",function(){var on=s.dataset.on==="1";s.dataset.on=on?"0":"1";'
          's.setAttribute("aria-checked",String(!on));});});</script>'
    )
    return render_shell(title='Design System', active='system', space_label='Système',
                        sub_label='Design System', content=content, page_label='design-system')
