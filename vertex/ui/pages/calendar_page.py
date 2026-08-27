"""vertex.ui.pages.calendar_page — le CALENDRIER (Vertex 2.0).

« Qu'est-ce qui arrive, quand, quels instruments ou positions sont concernés,
et quelle préparation analytique est nécessaire ? »

CE QUE CETTE PAGE COMPOSE
    `GET /cal-feed` — l'unique source d'événements agrégés du produit :
      · `items[]`  résultats     `{sym, date, dte, score, grade, verdict}`
      · `macro[]`  macro         `{kind, date, label, importance, source,
                                   approx, note, dte}`
      · `macro_couverture{}`     jusqu'où le calendrier officiel est publié
      · `updated`                heure de dernière construction du lot

    La vue `/opportunities?view=calendar` consommait déjà ces données. Elle
    reste servie : cette page ne la remplace pas, elle donne au calendrier la
    surface transversale que la navigation lui promet.

DEUX HONNÊTETÉS PARTICULIÈRES
    1. `/cal-feed` ne porte AUCUN champ `ts`. Trois pages du produit écrivent
       `cal.ts || Date.now()` et affichent donc l'heure du NAVIGATEUR comme
       fraîcheur de la donnée — une fraîcheur fausse, toujours verte. Cette
       page n'imite pas ce comportement : elle affiche `updated`, qui existe,
       et déclare l'horodatage absent quand il l'est. Corriger l'endpoint
       relève du backend et sort du périmètre de cette refonte ; le besoin est
       consigné.
    2. Le calendrier macro officiel a une DATE DE FIN de publication. Au-delà,
       le moteur ne rend plus que des dates approximatives, qu'il marque comme
       telles. La page affiche cette couverture au lieu de laisser croire à un
       horizon infini.

CE QUI N'A AUCUNE SOURCE, ET QUI EST DIT
    Dividendes et ex-dates · expirations d'options et OPEX · catalyseurs
    non-résultats · revues planifiées. Ces catégories sont annoncées absentes.
    Aucune n'est fabriquée pour remplir une grille.

Lecture seule. Aucun moteur, aucun endpoint, aucun store n'est créé.
"""
from __future__ import annotations

from vertex.ui import vx2
from vertex.ui.shell import render_shell

_VIEWS = (
    ('today', "Aujourd'hui"),
    ('week', 'Semaine'),
    ('month', 'Mois'),
    ('agenda', 'Agenda'),
    ('portfolio', 'Portefeuille'),
    ('macro', 'Macro'),
    ('options', 'Options'),
)

#: Catégories du contrat de calendrier, et leur source RÉELLE.
#: `None` = aucune source dans le produit. C'est affiché, pas dissimulé.
_CATEGORIES = (
    ('macro', 'Macro et banques centrales', '/cal-feed → macro[]',
     'Décisions de politique monétaire, emploi et inflation. Les dates '
     'officiellement publiées sont distinguées des dates de règle, marquées '
     '« approximative ».'),
    ('earnings', 'Résultats', '/cal-feed → items[]',
     'Date de publication par titre, avec le verdict du moteur pour ce titre '
     'et le repérage des positions exposées.'),
    ('dividends', 'Dividendes et ex-dates', None,
     'Aucune source de dividende n\'alimente Vertex. La catégorie est déclarée '
     'absente plutôt qu\'affichée vide comme si aucun dividende n\'existait.'),
    ('expiries', 'Expirations d\'options', 'positions déclarées → exp',
     'Les échéances de VOS contrats déclarés sont datées et regroupées dans la '
     'sous-vue Options. En revanche, aucun agrégat de marché n\'est produit et '
     'aucune date d\'OPEX n\'est détectée : le calendrier ne connaît que ce que '
     'vous avez déclaré.'),
    ('catalysts', 'Catalyseurs hors résultats', None,
     'Journées investisseurs, lancements, régulatoire, entrées en indice : le '
     'moteur sait les classer, mais aucune source ne les fournit.'),
    ('reviews', 'Revues planifiées', None,
     'Aucune date de prochaine revue n\'est persistée par Vertex. Les thèses '
     'portent une exigence de revue, jamais une échéance datée.'),
)


def _tabs(view: str) -> str:
    return vx2.tabs(
        [{'label': lbl, 'href': f'/calendar?view={vid}', 'actif': vid == view}
         for vid, lbl in _VIEWS],
        libelle='Vues du Calendrier')


#: Horizon par défaut : sept jours. Assez pour préparer, assez court pour rester
#: une liste et non un annuaire.
_HORIZON_DEFAUT = '7'


def _chip_horizon(valeur: str, libelle: str, actif: bool) -> str:
    """Chip d'horizon. L'attribut `data-cal-horizon` est écrit LITTÉRALEMENT :
    câblé par délégation dans `calendar.js` (`[data-cal-horizon]`), et lisible
    comme tel par quiconque ouvre ce fichier."""
    presse = 'true' if actif else 'false'
    return (f'<button type="button" class="vx2-chip" data-cal-horizon="{valeur}" '
            f'aria-pressed="{presse}">{libelle}</button>')


def _chip_categorie(valeur: str, libelle: str, actif: bool) -> str:
    """Chip de type d'événement — délégation `[data-cal-cat]` dans `calendar.js`."""
    presse = 'true' if actif else 'false'
    return (f'<button type="button" class="vx2-chip" data-cal-cat="{valeur}" '
            f'aria-pressed="{presse}">{libelle}</button>')


def _filtres() -> str:
    horizons = ''.join(
        _chip_horizon(h, lbl, h == _HORIZON_DEFAUT)
        for h, lbl in (('0', "Aujourd'hui"), ('7', '7 jours'), ('14', '14 jours'),
                       ('30', '30 jours'), ('120', '120 jours')))
    cats = ''.join(
        _chip_categorie(c, lbl, c == '')
        for c, lbl in (('', 'Tout'), ('macro', 'Macro'), ('earnings', 'Résultats')))
    return vx2.context_bar([
        {'label': 'Horizon', 'contenu':
            f'<div class="vx2-context-group">{horizons}</div>'},
        {'label': 'Type', 'contenu': f'<div class="vx2-context-group">{cats}</div>'},
        {'label': 'Périmètre', 'contenu':
            '<button type="button" class="vx2-chip" id="vx-cal-mine" '
            'data-cal-mine="1" aria-pressed="false">Mes positions seulement</button>'},
        {'label': 'Fraîcheur', 'contenu': '<span id="vx-cal-fraicheur">'
            + vx2.badge_etat('missing', texte='Chargement…') + '</span>'},
    ])


def _couverture_bloc() -> str:
    return ('<div id="vx-cal-couverture">'
            + vx2.bandeau('Couverture du calendrier officiel en cours de lecture…',
                          kind='neutre')
            + '</div>')


def _categories_table() -> str:
    lignes = []
    for _cid, label, source, note in _CATEGORIES:
        lignes.append([
            f'<b>{label}</b>',
            vx2.badge_etat('live', texte='Alimentée') if source
            else vx2.badge_etat('missing', texte='Aucune source'),
            note,
            f'<code>{source}</code>' if source else vx2.valeur(None),
        ])
    return vx2.table(
        colonnes=[{'titre': 'Catégorie', 'sticky': True},
                  {'titre': 'État'},
                  {'titre': 'Ce que Vertex sait, ou ne sait pas'},
                  {'titre': 'Source'}],
        lignes=lignes,
        libelle='Couverture du calendrier par catégorie d\'événement')


_VIEW_CONTENT = (
    '<div class="vx2-grid">'
    '<div class="vx2-col-8">'
    '<div class="vx2-surface">'
    '<div class="vx2-card-head"><div>'
    '<h2 class="vx2-card-title">Chronologie</h2>'
    '<p class="vx2-card-question">Qu\'est-ce qui arrive, et qu\'est-ce que cela touche ?</p>'
    '</div><div id="vx-cal-compte"></div></div>'
    '<div id="vx-cal-timeline">'
    '<div class="vx2-skeleton" style="height:280px"></div>'
    '</div></div></div>'
    '<div class="vx2-col-4">'
    '<div class="vx2-surface">'
    '<div class="vx2-card-head"><div>'
    '<h2 class="vx2-card-title">Ce qui touche le portefeuille</h2>'
    '<p class="vx2-card-question">Quels événements concernent ce que je détiens ?</p>'
    '</div></div>'
    '<div id="vx-cal-positions">'
    '<div class="vx2-skeleton" style="height:180px"></div>'
    '</div></div></div>'
    '<div class="vx2-col-12" id="vx-cal-table"></div>'
    '</div>')


_STYLE = """
<style>
#vx-content .vx2-table code,#vx-content .vx2-hyp code{font-family:var(--vx-font-mono);
  font-size:11.5px;color:var(--vx-smoke)}
#vx-content .vx-cal-jour{display:flex;flex-direction:column;gap:8px;
  padding:12px 0;border-bottom:1px solid var(--vx2-line-faint)}
#vx-content .vx-cal-jour:last-child{border-bottom:0}
#vx-content .vx-cal-jour-tete{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
#vx-content .vx-cal-jour-date{font-family:var(--vx-font-mono);font-size:12.5px;
  font-weight:600;color:var(--vx-ink);font-variant-numeric:tabular-nums}
#vx-content .vx-cal-jour-dte{font-size:11px;color:var(--vx-text-faint);
  font-family:var(--vx-font-mono)}
#vx-content .vx-cal-ev{display:flex;align-items:flex-start;gap:10px;
  padding:7px 10px;border-radius:var(--vx2-r-control);
  background:var(--vx-glass-subtle);border:1px solid var(--vx2-line-faint)}
#vx-content .vx-cal-ev[data-expose="1"]{border-color:rgba(221,162,59,.34)}
#vx-content .vx-cal-ev-corps{min-width:0;display:flex;flex-direction:column;gap:2px}
#vx-content .vx-cal-ev-titre{font-size:13px;color:var(--vx-ink);font-weight:500}
#vx-content .vx-cal-ev-meta{font-size:11px;color:var(--vx-text-faint)}
</style>
"""

_PAGE_JS = '<script src="/static/vertex/js/pages/calendar.js" defer></script>'


def render(view: str = 'today') -> str:
    if view not in dict(_VIEWS):
        view = 'today'
    label = dict(_VIEWS)[view]
    content = (
        _STYLE
        + f'<div class="vx2-page" data-cal-view="{view}">'
        + vx2.page_header(
            surtitre='Piloter',
            titre='Calendrier',
            question='Qu\'est-ce qui arrive, quand, et quels instruments ou '
                     'positions sont concernés ?',
            actions=vx2.bouton('Voir les opportunités', href='/opportunities',
                               variante='ghost'))
        + _filtres()
        + _tabs(view)
        + _couverture_bloc()
        + _VIEW_CONTENT
        + vx2.section(
            titre='Couverture du calendrier',
            note='ce qui est alimenté, et ce qui n\'a aucune source',
            corps=_categories_table())
        + '</div>')
    return render_shell(
        title='Calendrier', active='calendar', space_label='Calendrier',
        sub_label=label, page_label='Calendrier',
        content=content, page_js=_PAGE_JS)


__all__ = ['render']
